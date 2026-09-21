"""services.northena — the direction governor (Doc 05).

Adapted from Akki-OS-V1/backend/services/northena/ into Extraction-Akki:
  - Persistence: MongoDB (donor · core.db) -> phase0/ JSON (this estate).
  - Solva boundary: donor imports services.solva_depth.admit_assist;
    Extraction-Akki does not have Solva yet — an honest stub returns
    pass-through-with-provenance until W5 lands Solver.

Public modules:
  - admit    · compile_and_freeze() + FrozenArtifact + AdmitOffender
  - gate     · route() — strict set-membership; no inferential path
  - converge · check() — done-condition beats budget; no learned stopping
  - ledger   · record() · list_rows_by_run() · list_open_runs()
  - admit_assist_stub · resolve_scope / defensibility_floor / preservation_depth
  - router   · FastAPI POST /api/thinklab/{admit,gate,converge}
                        + GET /api/thinklab/runs
                        + GET /api/thinklab/runs/{run_id}
"""
from services.northena import admit, gate, converge, ledger  # noqa: F401
