# Cross-repo service delta measurements

Legend: files/lines/last-commit per repo. Diff status computed against 'anchor' = repo with most files.


## service: `__init__.py`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 1 | 0 | 2026-07-02T02:38:29+00:00 |
| Akki-OS-V1 | 1 | 0 | 2026-07-02T02:38:29+00:00 |
| Extraction-Akki | 1 | 0 | 2026-07-02T02:38:29+00:00 |
| Akki-Executive-Core | 1 | 6 | 2026-05-02T03:54:14+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (1 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Akki-Executive-Core vs RMS-IQ-Core-2**: DIVERGED (missing_here=0, extra_here=0, content_diff=1)
    - files with SAME PATH BUT DIFFERENT CONTENT: 1
        - backend/services/__init__.py

## service: `artifact_store`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 4 | 577 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 4 | 577 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 4 | 577 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (4 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `auth`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 16 | 1736 | 2026-08-01T03:38:15+00:00 |
| Akki-OS-V1 | 15 | 1491 | 2026-07-08T15:18:59+00:00 |
| Extraction-Akki | 16 | 1736 | 2026-08-01T03:38:15+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (16 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: DIVERGED (missing_here=1, extra_here=0, content_diff=3)
    - files IN RMS-IQ-Core-2 MISSING FROM Akki-OS-V1: 1
        - backend/services/auth/demo_identity_seeder.py
    - files with SAME PATH BUT DIFFERENT CONTENT: 3
        - backend/services/auth/engineer_key_grant.py
        - backend/services/auth/engineer_key_grant_service.py
        - backend/services/auth/user_store.py
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `census_dimensions`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 5 | 383 | 2026-07-10T16:23:48+00:00 |
| Akki-OS-V1 | 5 | 383 | 2026-07-10T16:23:48+00:00 |
| Extraction-Akki | 5 | 383 | 2026-07-10T16:23:48+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (5 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `checker`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 6 | 751 | 2026-07-07T21:18:38+00:00 |
| Akki-OS-V1 | 6 | 751 | 2026-07-07T21:18:38+00:00 |
| Extraction-Akki | 6 | 751 | 2026-07-07T21:18:38+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (6 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `compliance`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 24 | 1948 | 2026-08-01T04:13:23+00:00 |
| Akki-OS-V1 | 23 | 1846 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 24 | 1948 | 2026-08-01T04:13:23+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (24 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: DIVERGED (missing_here=1, extra_here=0, content_diff=2)
    - files IN RMS-IQ-Core-2 MISSING FROM Akki-OS-V1: 1
        - backend/services/compliance/data_class_registry.v4.json
    - files with SAME PATH BUT DIFFERENT CONTENT: 2
        - backend/services/compliance/consequence_class.v0.json
        - backend/services/compliance/deletion_ledger.py
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `connect`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 4 | 530 | 2026-08-01T00:19:53+00:00 |
| Extraction-Akki | 4 | 530 | 2026-08-01T00:19:53+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (4 files)

- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-OS-V1, Akki-Executive-Core

## service: `data_source`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 16 | 35611 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 16 | 35611 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 16 | 35611 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (16 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `economics`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 1399 | 12033 | 2026-08-01T04:13:23+00:00 |
| Akki-OS-V1 | 1118 | 9776 | 2026-07-25T14:39:38+00:00 |
| Extraction-Akki | 1409 | 12113 | 2026-08-01T20:02:51+00:00 |

Anchor for comparison: **Extraction-Akki** (1409 files)

- **RMS-IQ-Core-2 vs Extraction-Akki**: SUBSET_OF_ANCHOR (missing 10 files)
    - files IN Extraction-Akki MISSING FROM RMS-IQ-Core-2: 10
        - backend/services/economics/tier_lock.v1387.json
        - backend/services/economics/tier_lock.v1388.json
        - backend/services/economics/tier_lock.v1389.json
        - backend/services/economics/tier_lock.v1390.json
        - backend/services/economics/tier_lock.v1391.json
        - ... +5 more
- **Akki-OS-V1 vs Extraction-Akki**: DIVERGED (missing_here=291, extra_here=0, content_diff=380)
    - files IN Extraction-Akki MISSING FROM Akki-OS-V1: 291
        - backend/services/economics/tier_lock.v1107.json
        - backend/services/economics/tier_lock.v1108.json
        - backend/services/economics/tier_lock.v1109.json
        - backend/services/economics/tier_lock.v1110.json
        - backend/services/economics/tier_lock.v1111.json
        - ... +286 more
    - files with SAME PATH BUT DIFFERENT CONTENT: 380
        - backend/services/economics/tier_lock.v1000.json
        - backend/services/economics/tier_lock.v1001.json
        - backend/services/economics/tier_lock.v1002.json
        - backend/services/economics/tier_lock.v1003.json
        - backend/services/economics/tier_lock.v1004.json
        - ... +375 more

Absent in: Akki-Executive-Core

## service: `g1_defensibility`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 10 | 616 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 10 | 616 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 10 | 616 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (10 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `health`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 2 | 72 | 2026-07-31T17:29:00+00:00 |
| Akki-OS-V1 | 2 | 62 | 2026-07-25T14:20:36+00:00 |
| Extraction-Akki | 2 | 72 | 2026-07-31T17:29:00+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (2 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: DIVERGED (missing_here=0, extra_here=0, content_diff=1)
    - files with SAME PATH BUT DIFFERENT CONTENT: 1
        - backend/services/health/parity_counter.py
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `layer_a`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 9 | 457 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 9 | 457 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 9 | 457 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (9 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `layer_b`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 10 | 505 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 10 | 505 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 10 | 505 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (10 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `layer_c`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 3 | 227 | 2026-07-02T02:38:29+00:00 |
| Akki-OS-V1 | 3 | 227 | 2026-07-02T02:38:29+00:00 |
| Extraction-Akki | 3 | 227 | 2026-07-02T02:38:29+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (3 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `master_admin`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 2 | 115 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 2 | 115 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 2 | 115 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (2 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `memory`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 12 | 1448 | 2026-07-31T02:52:17+00:00 |
| Extraction-Akki | 12 | 1448 | 2026-07-31T02:52:17+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (12 files)

- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-OS-V1, Akki-Executive-Core

## service: `mtafiti`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 12 | 946 | 2026-07-10T18:59:15+00:00 |
| Akki-OS-V1 | 12 | 946 | 2026-07-10T18:59:15+00:00 |
| Extraction-Akki | 12 | 946 | 2026-07-10T18:59:15+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (12 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `multi_instance`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 3 | 190 | 2026-07-16T04:17:17+00:00 |
| Akki-OS-V1 | 3 | 190 | 2026-07-16T04:17:17+00:00 |
| Extraction-Akki | 3 | 190 | 2026-07-16T04:17:17+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (3 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `northena`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 7 | 773 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 7 | 773 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 7 | 773 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (7 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `opportunity_briefs`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 9 | 637 | 2026-07-11T03:14:43+00:00 |
| Akki-OS-V1 | 9 | 637 | 2026-07-11T03:14:43+00:00 |
| Extraction-Akki | 9 | 637 | 2026-07-11T03:14:43+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (9 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `outer_gate`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 4 | 285 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 4 | 285 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 4 | 285 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (4 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `perception`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 30 | 2228 | 2026-07-23T20:14:21+00:00 |
| Akki-OS-V1 | 30 | 2228 | 2026-07-23T20:14:21+00:00 |
| Extraction-Akki | 30 | 2228 | 2026-07-23T20:14:21+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (30 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `registry`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 5 | 2134 | 2026-08-01T02:14:38+00:00 |
| Akki-OS-V1 | 4 | 1855 | 2026-07-25T14:20:36+00:00 |
| Extraction-Akki | 5 | 2134 | 2026-08-01T02:14:38+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (5 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: DIVERGED (missing_here=1, extra_here=0, content_diff=2)
    - files IN RMS-IQ-Core-2 MISSING FROM Akki-OS-V1: 1
        - backend/services/registry/sample_fixture_seeder.py
    - files with SAME PATH BUT DIFFERENT CONTENT: 2
        - backend/services/registry/parser.py
        - backend/services/registry/validator.py
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `retention`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 2 | 173 | 2026-07-07T20:11:33+00:00 |
| Akki-OS-V1 | 2 | 173 | 2026-07-07T20:11:33+00:00 |
| Extraction-Akki | 2 | 173 | 2026-07-07T20:11:33+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (2 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `service_1`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 25 | 4047 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 26 | 4274 | 2026-07-25T05:10:33+00:00 |
| Extraction-Akki | 25 | 4047 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **Akki-OS-V1** (26 files)

- **RMS-IQ-Core-2 vs Akki-OS-V1**: SUBSET_OF_ANCHOR (missing 1 files)
    - files IN Akki-OS-V1 MISSING FROM RMS-IQ-Core-2: 1
        - backend/services/service_1/batch_quarantine.py
- **Extraction-Akki vs Akki-OS-V1**: SUBSET_OF_ANCHOR (missing 1 files)
    - files IN Akki-OS-V1 MISSING FROM Extraction-Akki: 1
        - backend/services/service_1/batch_quarantine.py

Absent in: Akki-Executive-Core

## service: `solva_depth`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 15 | 692 | 2026-07-02T16:05:51+00:00 |
| Akki-OS-V1 | 15 | 692 | 2026-07-02T16:05:51+00:00 |
| Extraction-Akki | 15 | 692 | 2026-07-02T16:05:51+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (15 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `synisense`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 21 | 2928 | 2026-07-30T20:06:53+00:00 |
| Akki-OS-V1 | 16 | 2362 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 21 | 2928 | 2026-07-30T20:06:53+00:00 |
| Akki-Executive-Core | 34 | 6304 | 2026-07-04T19:05:20+00:00 |

Anchor for comparison: **Akki-Executive-Core** (34 files)

- **RMS-IQ-Core-2 vs Akki-Executive-Core**: DIVERGED (missing_here=24, extra_here=11, content_diff=6)
    - files IN Akki-Executive-Core MISSING FROM RMS-IQ-Core-2: 24
        - backend/services/synisense/adapter.py
        - backend/services/synisense/deck_signal_extraction.py
        - backend/services/synisense/encryption.py
        - backend/services/synisense/engine/__init__.py
        - backend/services/synisense/engine/derivation_scheduler.py
        - ... +19 more
    - files IN RMS-IQ-Core-2 MISSING FROM Akki-Executive-Core: 11
        - backend/services/synisense/shield/brief_prompt.v0.txt
        - backend/services/synisense/shield/brief_synthesizer.py
        - backend/services/synisense/shield/egress_firewall.py
        - backend/services/synisense/shield/fluency_prompt.v0.txt
        - backend/services/synisense/shield/fluency_synthesizer.py
        - ... +6 more
    - files with SAME PATH BUT DIFFERENT CONTENT: 6
        - backend/services/synisense/__init__.py
        - backend/services/synisense/config.py
        - backend/services/synisense/shield/__init__.py
        - backend/services/synisense/shield/llm_router.py
        - backend/services/synisense/shield/tenant_entities.py
        - ... +1 more
- **Akki-OS-V1 vs Akki-Executive-Core**: DIVERGED (missing_here=24, extra_here=6, content_diff=5)
    - files IN Akki-Executive-Core MISSING FROM Akki-OS-V1: 24
        - backend/services/synisense/adapter.py
        - backend/services/synisense/deck_signal_extraction.py
        - backend/services/synisense/encryption.py
        - backend/services/synisense/engine/__init__.py
        - backend/services/synisense/engine/derivation_scheduler.py
        - ... +19 more
    - files IN Akki-OS-V1 MISSING FROM Akki-Executive-Core: 6
        - backend/services/synisense/shield/brief_prompt.v0.txt
        - backend/services/synisense/shield/brief_synthesizer.py
        - backend/services/synisense/shield/fluency_prompt.v0.txt
        - backend/services/synisense/shield/fluency_synthesizer.py
        - backend/services/synisense/shield/perception_router.py
        - ... +1 more
    - files with SAME PATH BUT DIFFERENT CONTENT: 5
        - backend/services/synisense/__init__.py
        - backend/services/synisense/config.py
        - backend/services/synisense/shield/__init__.py
        - backend/services/synisense/shield/llm_router.py
        - backend/services/synisense/shield/tenant_entities.py
- **Extraction-Akki vs Akki-Executive-Core**: DIVERGED (missing_here=24, extra_here=11, content_diff=6)
    - files IN Akki-Executive-Core MISSING FROM Extraction-Akki: 24
        - backend/services/synisense/adapter.py
        - backend/services/synisense/deck_signal_extraction.py
        - backend/services/synisense/encryption.py
        - backend/services/synisense/engine/__init__.py
        - backend/services/synisense/engine/derivation_scheduler.py
        - ... +19 more
    - files IN Extraction-Akki MISSING FROM Akki-Executive-Core: 11
        - backend/services/synisense/shield/brief_prompt.v0.txt
        - backend/services/synisense/shield/brief_synthesizer.py
        - backend/services/synisense/shield/egress_firewall.py
        - backend/services/synisense/shield/fluency_prompt.v0.txt
        - backend/services/synisense/shield/fluency_synthesizer.py
        - ... +6 more
    - files with SAME PATH BUT DIFFERENT CONTENT: 6
        - backend/services/synisense/__init__.py
        - backend/services/synisense/config.py
        - backend/services/synisense/shield/__init__.py
        - backend/services/synisense/shield/llm_router.py
        - backend/services/synisense/shield/tenant_entities.py
        - ... +1 more

## service: `system_state.py`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 1 | 151 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 1 | 151 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 1 | 151 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (1 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `targeta`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 6 | 425 | 2026-07-14T10:10:52+00:00 |
| Akki-OS-V1 | 7 | 557 | 2026-07-25T05:10:33+00:00 |
| Extraction-Akki | 6 | 425 | 2026-07-14T10:10:52+00:00 |

Anchor for comparison: **Akki-OS-V1** (7 files)

- **RMS-IQ-Core-2 vs Akki-OS-V1**: SUBSET_OF_ANCHOR (missing 1 files)
    - files IN Akki-OS-V1 MISSING FROM RMS-IQ-Core-2: 1
        - backend/services/targeta/gap_candidate_filer.py
- **Extraction-Akki vs Akki-OS-V1**: SUBSET_OF_ANCHOR (missing 1 files)
    - files IN Akki-OS-V1 MISSING FROM Extraction-Akki: 1
        - backend/services/targeta/gap_candidate_filer.py

Absent in: Akki-Executive-Core

## service: `team`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 2 | 202 | 2026-08-01T03:38:15+00:00 |
| Extraction-Akki | 2 | 202 | 2026-08-01T03:38:15+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (2 files)

- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-OS-V1, Akki-Executive-Core

## service: `transform_forms`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 6 | 436 | 2026-07-10T14:51:58+00:00 |
| Akki-OS-V1 | 6 | 436 | 2026-07-10T14:51:58+00:00 |
| Extraction-Akki | 6 | 436 | 2026-07-10T14:51:58+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (6 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `use_data`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 4 | 757 | 2026-07-31T21:44:49+00:00 |
| Extraction-Akki | 4 | 757 | 2026-07-31T21:44:49+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (4 files)

- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-OS-V1, Akki-Executive-Core

## service: `v1_harness`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 3 | 223 | 2026-07-14T10:10:52+00:00 |
| Akki-OS-V1 | 3 | 223 | 2026-07-14T10:10:52+00:00 |
| Extraction-Akki | 3 | 223 | 2026-07-14T10:10:52+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (3 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `v2_gate`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 3 | 141 | 2026-07-14T15:09:04+00:00 |
| Akki-OS-V1 | 3 | 141 | 2026-07-14T15:09:04+00:00 |
| Extraction-Akki | 3 | 141 | 2026-07-14T15:09:04+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (3 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `v3_harness`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 2 | 138 | 2026-07-02T02:38:29+00:00 |
| Akki-OS-V1 | 2 | 138 | 2026-07-02T02:38:29+00:00 |
| Extraction-Akki | 2 | 138 | 2026-07-02T02:38:29+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (2 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: IDENTICAL to anchor
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core

## service: `wizard`

| Repo | files | lines | last commit date (this path) |
|---|---:|---:|---|
| RMS-IQ-Core-2 | 9 | 999 | 2026-07-31T01:52:38+00:00 |
| Akki-OS-V1 | 8 | 854 | 2026-07-06T10:48:30+00:00 |
| Extraction-Akki | 9 | 999 | 2026-07-31T01:52:38+00:00 |

Anchor for comparison: **RMS-IQ-Core-2** (9 files)

- **Akki-OS-V1 vs RMS-IQ-Core-2**: SUBSET_OF_ANCHOR (missing 1 files)
    - files IN RMS-IQ-Core-2 MISSING FROM Akki-OS-V1: 1
        - backend/services/wizard/milestones.py
- **Extraction-Akki vs RMS-IQ-Core-2**: IDENTICAL to anchor

Absent in: Akki-Executive-Core
