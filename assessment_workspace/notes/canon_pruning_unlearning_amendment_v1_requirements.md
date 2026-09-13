READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_pruning_unlearning_amendment_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Pruning_Unlearning_Amendment_v1.docx` sha256 `14bbd73760…` · 13,543 B. Extracted text `canon/drops/20260909/extracted/text/Pruning_Unlearning_Amendment_v1.txt`.
**Standing.** CHANGE REGISTER · SECURITY · 9 OF 9. 2 amendments · 1 new promise · 1 ruling · 9 September 2026.
**Applies to (verbatim, Table 0 R0).** *"`dap_backend_spec_v1` (new DAP-37, DAP-38) · Security Assurance Promise Set (S-26)"*.

---

## §A · T-3 — Artefact Pruning Before Egress

**TARGET.** `dap_backend_spec_v1` — new **DAP-37**, extending DAP-31 and DAP-36.

- **DAP-37** (verbatim): *"A fine-tuned artefact MAY be pruned — magnitude pruning or an equivalent structural reduction — between MOAC acceptance and DAP-31's distance gate, as a ruled optional step. Pruning is a second, empirical reduction in memorisation surface on top of DAP-36's differentially private training; it is never a substitute for it, and this document does not present it as one. A pruned artefact MUST re-pass MOAC's acceptance criteria — pruning can degrade performance below the accepted bar, and acceptance is re-evaluated, not assumed to survive the change. A pruned artefact's hash differs from its pre-pruning hash; it is a new artefact for every purpose DAP-10 and DAP-31 govern, including a fresh pass through the distance gate at the ruled threshold. Pruning ratio and method are ruled values, ratified alongside DAP-31's own probe parameters."*
- **MECHANISM** (verbatim): *"Magnitude pruning removes the weights contributing least to model output, which empirically also reduces the model's capacity to have memorised specific training examples … DAP-31's probe, re-run on the pruned artefact, is what actually confirms the result."*
- **DERIVATION**: Han/Mao/Dally (2015) Deep Compression + DAP-31 + DAP-36.
- **PRINCIPLE** (verbatim): *"A smaller artefact is not a safer artefact by assertion. It is a candidate for re-testing, and DAP-31 is what turns the candidacy into a fact."*

## §B · T-4 — Unlearning on Rights Withdrawal

**TARGET.** `dap_backend_spec_v1` — new **DAP-38**. Rules Service (registry query, RBM-20).

- **DAP-38** (verbatim): *"When a unit's rights status changes to withdrawn — consent revoked, licence expired, or an equivalent event — every artefact whose training manifest cites that unit is identified via the registry (a query, per RBM-20's design, not a search) and is either re-derived without the unit or recalled. Re-derivation trains a replacement artefact excluding the withdrawn unit, using the same run configuration recorded in the original training manifest, and passes it through DAP-31 and MOAC as a new artefact before it replaces the original in the registry. Recall withdraws the original artefact's registry entry and, where the artefact was already delivered under DAP-10, notifies the receiving party that the artefact's rights basis has changed. A unit's contribution to the estate release budget (DAP-35) is NOT refunded on unlearning — the privacy loss from the original release already occurred; unlearning restores the artefact's cleanliness going forward, not the budget already spent."*
- **MECHANISM** (verbatim): SISA (Bourtoule et al. 2021) sharded isolated training + DP-SGD per-shard accountant. Where sharding not used, re-derivation = full retrain; **R-12 rules whether mandatory**.
- **DERIVATION**: SISA + Certified Data Removal (Guo et al. 2020) + Kenya DPA 2019 s.40 + GDPR Art.17 + CA1-N3.
- **PRINCIPLE** (verbatim): *"The erasure right does not stop at the database. A model that carries a unit's influence is still carrying it, whatever the registry says about the source record."*

## §C · New Promise (§3, Table 1 verbatim)

**S-26**: *"The system will remove a unit's influence from every artefact that carried it when the right to that unit ends — by re-derivation or recall, findable by registry query, with the release budget's prior consumption left unrefunded."* — Rests on T-3, T-4 (DAP-37, DAP-38), CA1-N3, SISA, certified removal, DPA s.40, GDPR Art.17.

## §D · Ruling (§4)

- **R-12** (verbatim): *"When the original training run was not sharded for isolated retraining, is re-derivation mandatory regardless of cost, or does recall alone satisfy DAP-38 where re-derivation is uneconomic? Neither this document nor CA1-N3 answers this; it is a genuine owner decision, not a technical one."*
- **Non-blocking (verbatim)**: *"Where sharding was used, re-derivation is the norm and inexpensive enough that the question doesn't arise. R-12 matters only for the harder case, and DAP-38's recall path is fully specified either way."*

## §E · Post-C3-batch-ratification status

Per owner C3 batch 2026-09-13 (see `notes/RATIFICATION_C3_BATCH_20260913.md`), **R-12 recommended default (re-derivation) is now RATIFIED** — recall alone requires owner sign-off case-by-case.

## §F · Milestone binding

- **M3** — W-PRUNING-UNLEARNING landing DAP-37 + DAP-38 + S-26 discharge + RBM-20 registry query.
- **M1** — DAP-37 is optional between DAP-16 approval and DAP-31 egress gate; landing tests-first with `PRUNING_RATIO=DEFAULT-PENDING-OVERRIDE` (pruning-ratio ratified alongside DAP-31 probe params).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
