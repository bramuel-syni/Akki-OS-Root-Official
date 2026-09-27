"""Worker-side bounded-batch accounting. Never instantiated to run data in E1.

The admitted worker must couple this guard to its own hard termination supervisor;
an RPC timeout or this cooperative counter alone is not proof of termination.
"""
import threading
from decimal import Decimal
from typing import Literal
from pydantic import model_validator
from services.northena.execution_models import Frozen, Hash, Name, Held
from services.activation.record_shapes import Quantity, quantities


class RuntimeEnvelope(Frozen):
    protocol: Literal["akki.runtime.limits/1"]
    request_sha256: Hash
    plan_ref: Hash
    reservation_ref: Hash
    runtime_id: Name
    operation_key: Name
    fence: int
    limits: tuple[Quantity, ...]
    starts_epoch: int
    stop_work_by_epoch: int
    terminate_by_epoch: int

    @model_validator(mode="after")
    def bounded(self):
        limits = quantities(self.limits)
        if (self.fence <= 0 or not self.starts_epoch < self.stop_work_by_epoch < self.terminate_by_epoch
                or ("wall_clock", "seconds") not in limits
                or self.terminate_by_epoch - self.starts_epoch > limits[("wall_clock", "seconds")]):
            raise ValueError("Termination window must fit within the effective ceiling.")
        return self


class RuntimeLimiter:
    def __init__(self, envelope, *, wall_clock, monotonic_clock):
        self.envelope = RuntimeEnvelope.model_validate_json(envelope.model_dump_json())
        self.wall_clock, self.monotonic_clock = wall_clock, monotonic_clock
        self.limits = quantities(envelope.limits)
        self.used = {k: Decimal(0) for k in self.limits}
        self.start_tick = monotonic_clock()
        self.lock = threading.Lock()
        self.stopped = False
        if wall_clock() < envelope.starts_epoch or wall_clock() >= envelope.stop_work_by_epoch:
            raise Held("RUNTIME_ADMISSION_WINDOW_INVALID")
        self.admission_elapsed = Decimal(str(wall_clock() - envelope.starts_epoch))

    def before_batch(self, upper_bounds):
        """Charge conservative upper bounds BEFORE reading/scanning/spending."""
        with self.lock:
            now, elapsed = self.wall_clock(), self.admission_elapsed + Decimal(str(self.monotonic_clock() - self.start_tick))
            allowed_elapsed = self.envelope.stop_work_by_epoch - self.envelope.starts_epoch
            if self.stopped or now >= self.envelope.stop_work_by_epoch or elapsed >= allowed_elapsed or elapsed < 0:
                self.stopped = True
                raise Held("RUNTIME_TERMINATION_REQUIRED")
            charges = quantities(upper_bounds)
            if any(k not in self.limits or k[0] == "wall_clock" for k in charges):
                self.stopped = True
                raise Held("RUNTIME_DIMENSION_NOT_ADMITTED")
            if any(self.used[k] + v > self.limits[k] for k, v in charges.items()):
                self.stopped = True
                raise Held("RUNTIME_LIMIT_WOULD_BE_EXCEEDED")
            for key, value in charges.items():
                self.used[key] += value
            self.used[("wall_clock", "seconds")] = elapsed

    def termination_observed(self):
        """Invoke after the worker supervisor confirms effect termination, not on RPC cancel."""
        with self.lock:
            self.stopped = True
            elapsed = self.admission_elapsed + Decimal(str(self.monotonic_clock() - self.start_tick))
            if elapsed < 0:
                raise Held("RUNTIME_CLOCK_INVALID")
            self.used[("wall_clock", "seconds")] = elapsed
            if (self.wall_clock() > self.envelope.terminate_by_epoch or
                    elapsed > self.envelope.terminate_by_epoch - self.envelope.starts_epoch):
                raise Held("RUNTIME_TERMINATION_CEILING_EXCEEDED")
            return tuple(Quantity(dimension=k[0], unit=k[1], quantity=str(v)) for k, v in self.used.items())