"""services.trace — governance audit timeline (Doc 15 §Trace).

REFERENCE-NOT-COPY (Design Law · load-bearing at W8 CP5): the Trace
surface reads existing on-disk records from every governance-lane
producer — northena_ledger · model_admission_records · approval_records ·
handoff_contracts · retention · breach_notifications · erasure_requests —
and returns them as a single chronologically-ordered timeline. It NEVER
duplicates or restructures the underlying records; it references them
by (kind, id, path) so audit trails remain on-record where the original
producer wrote them.
"""
from services.trace.timeline import TraceEntry, load_timeline

__all__ = ["TraceEntry", "load_timeline"]
