"""tests/invariants/test_m11w1_m9_files_untouched.py

M11-W1 · SO §3.8 additive-only discipline · no sealed M9 file modified.

Canon anchor (verbatim from R-18 · Tension (a) Option C ratification
2026-09-17T~15:45Z):
  "M11-W1 lands `services/data/repository.py` as the sole Motor
   importer.  Adapters at `services/enforce/<entity>_gate.py` (W3+)
   call the paired M9 refuser first, then a Repository op.  M9 sealed
   files are not modified."

Sealed M9 files at M11-W1 wave-open (banked here as byte-identity
invariant):
  36 files in `backend/services/platform_control_plane/`, sealed
  across M9 P1..P6 (2026-09-17 to 2026-09-18), banked SHA256 below.
  Any modification to any of these files after wave-open surfaces as
  a RED test → forces the change to be either reverted OR justified
  by a new owner ruling banked in DECISIONS.md that amends this
  invariant.

Test ID: test_m11w1_m9_platform_control_plane_files_sha256_pinned
"""
from __future__ import annotations

import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PCP_DIR = REPO_ROOT / "backend" / "services" / "platform_control_plane"

# --- SHA256 pins captured at M11-W1 wave-open · 2026-09-18T~11:40Z ---------
M9_SEALED_FILE_SHAS_AT_WAVE_OPEN = {
    "__init__.py": "324a021c3f7d144436f0e8faaab62d6fc2174d702c24a68d999963bf5109db65",
    "allocation_entity.py": "7d06f94ce0e24c77fd7ff5f2ec02d85eda72bcc0a0ba87599020ec6da3ef2fc1",
    "app_enablement.py": "a4c7e13c2af804f6849bc551f63c2f62189b6cf943ad32b10fa6a2f4b657f875",
    "app_entity.py": "5047ed04df63b429f99a54adc805cd0146c39a8567e2be3d04075ab0441d34e7",
    "app_revalidation.py": "c255195185a5e9f34f30fa285c0e6bb73d1eb0e8749c171389e3843b08469468",
    "audit_event.py": "5f4a1d388733bf11a1d8611b5527b13dc05ae3a6f18d853204380a72e643e742",
    "audit_event_types.py": "16fce047a4b5a71011dc386589941fd084de5397f0eb5fa0ed85e743be9092c6",
    "break_glass_session.py": "c8ee890d420831ab7e7887c30eb4e8657db701da328a3f305e32f31a85cac81d",
    "compute_integration.py": "7cc35db5d808a951d6319afc5f35ba33f895455230bd75f24ca1e6462b033300",
    "connection_test.py": "1d97e4f727b8fc45af37c204ac689887c2aa34530961dcac5b225f259ba4852b",
    "connector_entity.py": "6fdebf0cf978a0d83e5680c2c3cf75c6178eaef81f9553037d3e1361039c4e38",
    "connector_mode_lattice.py": "5cc0ef51b73df6fd879a9a802cf6fa1d3fada6aaf1a8b366d7f1afd11ce87e40",
    "cross_tenant_access_suite.py": "bc2968dbb4fc03799b0db23b25d63a4449012e830aaeb5f19e06e725e2be8930",
    "estate_entity.py": "93218a49fbbe05e3b6b1cc3374fafbbaaad13ea1b139cca1cbea43b044d780ea",
    "metering_ledger.py": "83be9f49b3f597b5d0370dcc1064cc186f24e04f35c36cdd487457e9e0330576",
    "mode_change_approval.py": "32a00054ed1e52bdd9723bf188e8c74099757a71591081a6f340cd25b8e5a897",
    "permission_evaluation.py": "4d5e1be942edaff5e28b5ad81bf6c9f5d06ed7eaf426b4dce6a4846b3246ad4b",
    "pilot_tenant_register.py": "2eea565edd84527b8bd41bf4d9c1fdece51bbc89aa94a1555290294893952a24",
    "preemption_contract.py": "abfa7c1768c39057e3a4aeceb67a16c5532d4c98b38840df012f420daca750ae",
    "provisioning_report.py": "d3334e92a89b733567e4b04ad1f403bd3dabe1f8b336ee6b179df5107c1ed40e",
    "role_assignment.py": "b7cc0a58d4638aacef215e6ba40d05f9694967eac7dbe1bee8e38f85b5c0e784",
    "role_registry.py": "cce6bb362e6a2401ffab59669b89b8369005cf5976ffdc391aac7ab3f4316c9c",
    "sandbox_offboarding.py": "b82ba91d7cd2c37166c9a5c745504853b960779e4e2da6cc673b6b5acab4eb07",
    "scheduler_admission.py": "af970e4e7a66a3d5047143719536b9101c02f9867416608770aea461a00309e0",
    "service_account_entity.py": "51fd3c2bddbb860ea1778c8ed46b133c452faad8b9137e621f463df2e52954ca",
    "session_binder.py": "8f34113ae5bf078bff518b86e76662517113d85c1ccf01a5855926f39f974b2a",
    "task_entity.py": "bddb32b73d5054742963fe06100dc65398520dc08ae2d1c0ea6fce473e05bba9",
    "task_invalidation.py": "71d331c5bb1ddf8cf8ea2c35c8ee203a7f2e8854e4e9185065ae157711cfb448",
    "task_scope_enforcement.py": "09c3c0c5d3c005fdc1628771dded5d3360396343ea54f11b2abbb98264b2e5da",
    "tenant_context.py": "af172230cb3d11b36b9f3e3f955c844a6465ba45b17e3d1bcbe204600357d78f",
    "tenant_entity.py": "7664a213cf04dc31b128208c7193becb8924b4e6b9e6e1809adaaa41fc853dfa",
    "tenant_lifecycle.py": "41d56f416822155da95e212d347e3bf6442728fa48a689e6a967e7ba5d9cac39",
    "theme_entity.py": "ce71e8e06833c78e894da6ba24537f3e3aac4ef059da330f2d23ef61a1c1ba13",
    "user_entity.py": "7ada96147401aaae00e889327bd78218a82e9ba391891fa56c7dabb60a785592",
    "wizard_state_machine.py": "ecbf44d0d9cf66a139cebb9004256b944a1e270ed02bbf02e7d07e9ff5dfe8b4",
    "workspace_entity.py": "fa3055911ec0a564feaa59d5eeb53397a9641aa7016a393fd8f1b4120acee015",
}


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m11w1_m9_platform_control_plane_files_sha256_pinned():
    """Every M9 sealed file's SHA256 must match the wave-open pin."""
    mismatches = []
    missing = []
    unexpected = []
    on_disk = {p.name for p in PCP_DIR.iterdir() if p.is_file() and p.suffix == ".py"}
    banked = set(M9_SEALED_FILE_SHAS_AT_WAVE_OPEN.keys())

    for name in banked - on_disk:
        missing.append(name)
    for name in on_disk - banked:
        unexpected.append(name)
    for name in banked & on_disk:
        actual = _sha256_of(PCP_DIR / name)
        expected = M9_SEALED_FILE_SHAS_AT_WAVE_OPEN[name]
        if actual != expected:
            mismatches.append((name, expected[:12], actual[:12]))

    problems = []
    if mismatches:
        problems.append(f"{len(mismatches)} SHA256 mismatch(es): "
                        + ", ".join(f"{n} banked={e}… live={a}…"
                                    for n, e, a in mismatches))
    if missing:
        problems.append(f"{len(missing)} M9 file(s) missing from tree: "
                        + ", ".join(sorted(missing)))
    if unexpected:
        problems.append(f"{len(unexpected)} unexpected new file(s) in "
                        f"platform_control_plane/: "
                        + ", ".join(sorted(unexpected)))

    assert not problems, (
        "M11-W1 SO §3.8 discipline violated: "
        + " ; ".join(problems)
        + " · any modification to a sealed M9 file requires an owner "
        "ruling banked in DECISIONS.md amending SO §3.8 and this "
        "test's banked SHAs."
    )
