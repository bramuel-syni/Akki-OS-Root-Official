# M1 Registry — complete source-row routing for this readiness take

28 September 2026. Coverage is not closure. Original source statuses/wording
remain immutable in `REQUIREMENT_GAPS_648.csv`; the dispositions below are current
integration findings. No row is marked product-complete from code presence.

Source-text references under `notes/full_requirements_gap_20260926/source_text/`:
`09_Estate_Registry_Part_1_Connection_and_Census_2de58fd1.txt` and
`10_Estate_Registry_Part_2_Comprehensive_Registry_44307b9a.txt`, read in full.
Existing delivery IDs are preserved. No new milestone gate or policy is created.

## Docs 9 and 10 — all 22 rows

| Review ID / source clause | Current disposition, reuse and exact remaining integration | Existing acceptance |
|---|---|---|
| REQ-094 Doc 9 A5.1 | PARTIAL: NormalizedUnit/candidate contracts and connector variants exist; bind all admitted source types to the same intake, not raw worker-specific public records. | M1-T1/T2/T4 |
| REQ-095 Doc 9 A5.2 | OPEN: RDS/OBS read in E1; NAS/external GPU-worker custody still unqualified. Local subprocess not off-E1. | M1-T2 |
| REQ-096 Doc 9 A5.3 | PARTIAL: scoped commission/refusal evidence exists; Connect drawer and genuine connection→record effects not end-to-end. | M1-T2/T4/T5 |
| REQ-097 Doc 9 A5.4 | PARTIAL: source and connection details exist; public denominator and honest adapter-gap coverage still incomplete. Preserve PROPOSED source marking; owner roadmap already requires honest coverage. | M1-T1/T3 |
| REQ-098 Doc 9 B5.1 | PARTIAL: objective-blind enumerator exists; currently selected aggregate sources do not establish complete accessible-estate walk. | M1-T1/T3 |
| REQ-099 Doc 9 B5.2 | PARTIAL with narrow correction retained: Measurement/Unmeasured union and explicit current limitations exist; all designed dimensions/rows and no-zero inference still require integration. | M1-T1/T3/T4 |
| REQ-100 Doc 9 B5.3 | PARTIAL: six-carrier Measurement exists; per-field lineage/units/population and source/run detail need end-to-end wiring. | M1-T3/T4 |
| REQ-101 Doc 9 B5.4 | PARTIAL: declaration, measure, overlay-admission and runtime-mode mechanisms exist; connect actual feed/source baseline without per-item invention. | M1-T1/T3 |
| REQ-102 Doc 9 B5.5 | PARTIAL: opaque matrix/verdict and import separation exist; persist actual regime/rule/inputs for re-derivation. No model-authored classes. | M1-T3 |
| REQ-103 Doc 9 B5.6 | PARTIAL: stale detector exists; actual structure/retraction producer, scoped remeasurement and failed-refresh consumer state remain open. | M1-T5 |
| REQ-104 Doc 9 B5.7 | PARTIAL: deterministic feed classifier exists; same source attribute must reach entitlement and all readers. | M1-T2/T3/T4 |
| REQ-105 Doc 10 A5.1 | PARTIAL: run receipts and primitive methods exist; complete 13-row report plus per-source figures must retain their own method/date/population, not only report hash. | M1-T3/T4 |
| REQ-106 Doc 10 A5.2 | PARTIAL: advisory marker, selector, generator, quantitative grounding and brief registry exist; real census/precedent inputs, tenant scope and refresh not live-proven. | M1-T1/T3/T4 |
| REQ-107 Doc 10 A5.3 | OPEN operational proof: duplicate detection/report artifacts and scaffolds exist; bind real evidence/grades, flags only and human confirmation; never merge during census. Ruling already settled. | M1-T1/T2/T3 |
| REQ-108 Doc 10 A5.4 | OPEN operational proof: FK-name scaffold is not all four evidence-backed shared-key/derivation/overlap/reference linkages. Read remaining candidates then extend; keep descriptive, never entitlement or verdict authority. Ruling already settled. | M1-T1/T2/T3/T4 |
| REQ-109 Doc 10 A5.5 | PARTIAL: shared scoped receipt projection works; source writer, asset writer and Mongo consumer roles not fully reconciled. Qualify durable one-source account across manager/Targeta/convergence/entitlement. | M1-T4/T5 |
| REQ-110 Doc 9 C5.1 | PARTIAL/SHARED: same NormalizedUnit/perception architecture exists. M1 enumerates modalities and uses qualified available reading; new perception capability acceptance M9, not a new intake. | M1-T1/T2; M9-T1 |
| REQ-111 Doc 9 C5.2 | PARTIAL/SHARED: frozen perception job/result contracts exist; actual runtime/model/corpus binding and measured outputs require proof. | M1-T3 if activated; M9-T1 |
| REQ-112 Doc 9 C5.3 | PARTIAL/SHARED: re-extraction/grounding carriers exist; genuine source-position resolution needs real modality evidence. Not closed by file-level inventory. | M1-T3 if activated; M9-T1 |
| REQ-113 Doc 9 C5.4 | PARTIAL/SHARED: model registry/licence/hash paths exist; display actual records in M1, qualify any executed model before use; new candidates M9. | M1-T2/T4; M9-T1/T2 |
| REQ-114 Doc 9 C5.5 | PARTIAL/SHARED: boundary-governor perception path exists; no live bypass/receipt proof from metadata census. No external model source export invented. | M1-T2 if invoked; M9-T1 |
| REQ-115 Doc 9 C5.6 | PARTIAL/SHARED: recorded execution-mode seam exists; both worker classes must preserve contract and actual attribution. GPU-hosted CPU execution is not acceleration proof. | M1-T1/T3; M9-T1 |

## Data cleanliness — all 15 rows

`non_gpu_governance/quality.py` is a reusable pack/bitmap/reconciliation consumer,
not execution of these checks. `quality_profiler.py` and relationship/PII helpers
are partial producers, not evidence that the full DQ register exists. Preserve
earlier owner ruling statuses and recover confirmed pack/threshold inputs; do not
invent them. The five-category UI does not replace the four-stratum register.

| Review ID / clause | Current remaining work and reuse | Ownership |
|---|---|---|
| REQ-618 DQ-1 | PARTIAL: extend existing field profiling to type/format/encoding and actual candidate-FK resolution; record results. | M1.3/T1/T3 |
| REQ-619 DQ-2 | OPEN execution: cardinality supports candidates; bind existing owner-confirmed sentinel list, never silently null. | M1.3/T1/T3 |
| REQ-620 DQ-3 | OPEN execution: recover confirmed source cross-field rules; learned suggestions are not authoritative rules. | M1.3/T1/T3 |
| REQ-621 DQ-4 | PARTIAL: reuse duplicate paths and extend exact/key/fuzzy evidence at adopted tolerance; no merge. | M1.3/T1/T2/T3 |
| REQ-622 DQ-5 | OPEN operational integration: pair shared natural keys/fields and retain disagreements; don't decide truth. | M1.3/T1/T3 |
| REQ-623 DQ-6 | PARTIAL: profiling statistics are inputs; distinguish impossible-value failures from outlier/shift flags. | M1.3/T1/T3/T5 |
| REQ-624 DQ-7 | PARTIAL: provenance consumer/stratum cap exists; bind actual source/pipeline/write-time, retain provenance unknown. | M1.3/T3 |
| REQ-625 DQ-8 | OPEN active execution: reuse media probe/inventory; decodability, duration, rate, clipping/silence and fingerprint checks on external workers. Deterministic media checks are not automatically deferred to GPU/model milestone. | M1.2/M1.3/T1/T2/T3 |
| REQ-626 DQ-9 | PARTIAL consumer; repair must be pack-named, deterministic and original-preserving under a separately permitted action. Read-only census must not repair the source. | M1 read/flag boundary; downstream repair M3/M9 as applicable |
| REQ-627 DQ-10 | PARTIAL: pure bitmap classifier exists; bind real bitmaps/versioned pack and receipted re-stratification. | M1.3/T3/T5 |
| REQ-628 DQ-11 | OPEN full artifact: existing QualityRegister lacks proof of complete estate sentinel/match/disagreement/repair lists and scale integration. Bind existing producers/retained detail, not another quality engine. | M1.3/T1/T3/T4 |
| REQ-629 DQ-12 | PARTIAL with existing reconciliation reused: exact pinned population/count validator exists; prove complete per-source/pack publication and failure handling. | M1.3/T3/T5 |
| REQ-630 DQ-13 | PARTIAL with existing honesty protection reused: accuracy not_measured is enforced in metadata consumer. Ground-truth accuracy, if measured, needs its named method; quality is not truth. | M1.3/T3/T4 |
| REQ-631 DQ-14 | SHARED: M1 supplies valid quality/version evidence; actual training commission eligibility/exception enforcement belongs M9 (with existing execution gates). | M1-T3/T4; M9-T2 |
| REQ-632 DQ-15 | SHARED: M1 supplies quality/lineage; actual fact-anchor eligibility/inference behaviour belongs M4, not claimed from census. | M1-T3/T4; M4-T2/T3 |

## Trust domains — all 3 rows

| Review ID / clause | M1-relevant disposition | Acceptance |
|---|---|---|
| REQ-458 TD-1 | UNVERIFIED physical appliance boundary; M1 must establish actual admitted runtime placement. A pod receipt label does not prove sealed appliance/network properties. | M1-T2; broader M8/M10 |
| REQ-459 TD-2 | OPEN estate-route proof: execute source work in appropriate external tenant domain, not E1. Do not claim physical one-tenant appliance isolation from scoped UI tests. | M1-T2 |
| REQ-460 TD-3 | PARTIAL: scoped operator/read rules tested; all external-party credential/store/identifier separation remains broader shared integration proof. | M1-T2/T4; M3/M7 |

**Reporting discipline:** keep verified narrow corrections closed with evidence;
open integration stays open. One row's shared ownership does not make it waived.
Readiness coverage: 22 + 15 + 3 = **40 mapped rows, not forty delivered clauses**.
All M1 live acceptance packs remain NOT RUN. New scope starts as an explicit
delta; do not reopen accepted work without a concrete reason.