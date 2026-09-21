"""M11-W1 · akki.data package · repository primitive.

Canon anchors (verbatim):
  v1.0 B.2 (partial): "Primary datastore is Mongo, one database per
  tenant, all access via `services.data.repository` — the sole Motor
  importer."
  v1.0 D-01 (partial): "Tenant isolation invariant AKKI-DATA-001: a
  data-plane call whose document `tenant_id` mismatches the injected
  context tenant_id is refused."
  R-18 Tension (a) Option C (owner ruling 2026-09-17T~15:45Z, SO §3.8
  amended in place): "M11-W1 lands `services/data/repository.py` as
  the sole Motor importer.  Adapters at `services/enforce/<entity>
  _gate.py` (W3+) call the paired M9 refuser first, then a Repository
  op."
"""
