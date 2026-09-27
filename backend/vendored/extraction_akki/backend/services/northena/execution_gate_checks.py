"""Bounded, typed calls to server-owned evidence producers; never workload RPCs."""
import asyncio
import inspect
from pydantic import ValidationError
from services.northena.execution_models import Held


def finite_timeout(value):
    if type(value) not in (int, float) or not 0 < value < float("inf"):
        raise ValueError("An explicit finite gate timeout is required.")


def async_provider(provider, methods, timeout):
    if provider is not None:
        finite_timeout(timeout)
        if not all(inspect.iscoroutinefunction(getattr(provider, name, None)) for name in methods):
            raise ValueError("Evidence producers require async metadata methods.")


def typed(value, model, reason):
    try:
        if not isinstance(value, model):
            raise ValueError("A typed receipt is required.")
        return model.model_validate_json(value.model_dump_json())
    except (ValidationError, ValueError, TypeError) as exc:
        raise Held(reason) from exc


async def bounded(fn, timeout, *args):
    try:
        return await asyncio.wait_for(fn(*args), timeout=timeout)
    except (TimeoutError, ConnectionError, OSError) as exc:
        raise Held("EVIDENCE_PRODUCER_UNAVAILABLE") from exc
    except (ValidationError, ValueError, TypeError) as exc:
        raise Held("EVIDENCE_RECEIPT_INVALID") from exc