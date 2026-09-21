"""services.documents_registry · documents-registry package.

M15-W3 · Documents-registry Mongo collections per-tenant persistence.
Binds the sealed W1/W2 document contracts (`WhitepaperDraft_v0` +
`SkillFileProvenanceV0`) to per-tenant Mongo databases (`t_<tenant_id>`)
via the sealed M11-W1 `services.data.repository.Repository` primitive
(sole Motor importer for the data plane).

Canon anchors:
- Canon 3 §B.7 (per-tenant provisioning).
- Canon 3 §9.3 (append-only writer discipline).
- M11-W1 sealed (Repository sole Motor importer · AKKI-DATA-001).
- Doc 14 §33 (WhitepaperDraft citation invariant · sealed W1 shape).
- Doc 18 A18.7 (buyer-facing provenance chain · sealed W2 shape).
- SO §3.8 (thin-kernel additive-only · new package surface consuming
  sealed pre-M15 surfaces without editing them).
"""
