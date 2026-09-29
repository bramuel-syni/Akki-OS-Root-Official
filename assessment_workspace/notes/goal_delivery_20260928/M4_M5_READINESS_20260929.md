# M4 / M5 joint readiness — context preservation and rapid-access memory

**Date:** 2026-09-29. **Scope:** requirements/repository readiness review, not M4/M5 implementation or acceptance. The four previously proposed journey items remain deferred at the owner's request.

## Executive reading

The owner is correct: heavy shrinkage with preserved meaning and rapid-access memory are explicit adopted product concerns, not new features to invent. They sit across Docs 7/8, the Memory Compaction specification and the Context and Capability amendment. M4 needs the shared memory/retrieval foundation before it can demonstrate answers; M5 extends that foundation across closed runs, applications and organisational work. **Ready for a reuse-first integration sprint; not ready for G4/G5 acceptance.**

The repository has meaningful mechanisms. It does not yet prove the complete short-inquiry → warm qualified-unit answer → durable scoped memory → restart/reuse journey. Passing synthetic receipt/model-shape tests is not proof of semantic preservation or estate-scale serving economics.

## 1. Requirements recovered

| Concern | Governing requirement | What acceptance must show |
|---|---|---|
| Estate shrinkage | Doc 7, promise #19, A5.1–A5.6 | Five-ring units preserve content, provenance, relational edges, context and defensibility; a live source-position re-extraction handle; executed judgement trace, not a post-hoc story; degraded material stays unqualified. |
| Small memory | Doc 8, promise #20, A5.1–A5.4 | The answerer reads stored, relevant qualified units, not raw estate dumps or a running mining tail. One asset-building write path; objective-serving does not invent a second extraction path. |
| Traffic controller | Doc 8, promise #21, B5.1–B5.5 | Decide warm/fresh/refused once against frozen scope and convergence. Warm is synchronous/full. Fresh invokes the existing builder for the specific missing slice, returns acknowledgement/estimate, and keeps retrieval authenticated. |
| Severe window reduction | CC-4/5/6 | Deterministic load-bearing → class → relational proximity → source-position recency → unit-ID ordering; whole units; excluded counts by class and top ten re-extraction handles; loss statement travels to trace AND answer; no learned reranking after assembly. |
| Cross-run compaction | MEM-1–MEM-11, S-30; CC-15 | Compact working context, never evidence/receipts/Ledger/audit. Rules decide retention. Facts remain anchored by hash/handle, never paraphrased into new facts. New artifact/version; ledger-before-read; deterministic hash-verified reload; explicit loss/class cap; erasure reaches descendants. |
| Serving economics | CC-8/9, M4-T4 | Governed latency by request class, warm-serve ratio, fresh-ack latency and actual resource consumption. A short query's work must scale with the missing slice, not the whole estate. |
| Independent demonstration | CC-16, M4-T3/M5-T2 | Shrink and regenerate the same content ring, reject degraded evidence, demonstrate warm/full serving, and exercise controlled-entity meaning/custody routing. |
| Application continuity | M5-T1/T2/T5 | Preserve objective/session/work identity, source versions, class/loss, rights and per-app boundaries across save/reopen/handoff/revocation. |

Sources: `source_text/07_Context_Preservation_Part_1_Shrinkage_98dd23e5.txt` B18–B43; `source_text/08_Context_Preservation_Part_2_Memory_and_Retrieval_2a0c89d6.txt` B18–B67; `source_text/Memory_Compaction_Spec_v1_a0ab271c.txt` MEM-1–11; `notes/enhancement_specs_20260926/supplement_18/Context_and_Capability_v1.md` CC-4–9/15/16. All source_text paths are beneath `notes/full_requirements_gap_20260926/`.

**Important distinction:** rapid-access memory here means a bounded, scoped working set over durable qualified intelligence—not a promise to keep the entire estate in hardware RAM. There are three distinct reductions: raw estate → qualified units; qualified units → one model window; historical run context → compacted lineage. They must compose without inventing parallel representations.

## 2. Repository readiness (current effective code)

Backend paths below are relative to `backend/vendored/extraction_akki/backend/`.

| Area | Existing implementation worth reusing | Readiness finding |
|---|---|---|
| Window selection | `services/non_gpu_governance/context.py:15–74` | Reconstructs whole-unit order, token-budget fit and excluded-class/top-handle metadata. **Built metadata verifier**, not an observed native tokenizer/content assembly. `units` capped at 500; full-estate candidate retrieval must remain bounded and explicit, not silently truncated before this population check. |
| Context/memory/rights checks | `services/non_gpu_governance/gate.py:57–118` | Checks signed context population/hash/policy joins and memory principal, class, source versions, closed run, publication ordering and current rights. Strong reusable gates; real producer/model-consumer integration still needs proof. |
| Warm/fresh routing | `services/northena/gate.py:18–68`; `services/service_1/dispatch.py:366–405,419+` | Real exact-membership routing and existing warm qualified-data/composed-conclusion branches plus fresh acknowledgement exist. Some legacy output/work-order branches remain placeholders. No end-to-end evidence yet that short questions read the smallest sufficient qualified set and fresh work fetches only the gap. **Do not call every dispatch branch a stub.** |
| Existing answer path | `services/service_1/composed_conclusion.py:315–445` | Already connects class/trace to fluent synthesis and per-sentence grounding, with a labelled mechanical fallback path. Reuse after checking the active provider/tokenizer and current native custody route; an old synthesis path is not current M4 acceptance. |
| Existing chat | `services/chat/router.py:23–59`; root `backend/server.py:322`; `frontend/src/components/Chat.jsx:34–50` | `/api/chat/ask` DOES exist and is mounted. It sends a single question into the existing model chokepoint; no session ID, retrieved qualified set or CC-window proof enters this request shape. The active `/os/work/chat` route still mounts the separate honest-gap `WorkChat` page (`App.js:1292`). No complete governed, memory-backed multi-turn journey. **Do not claim the backend route is absent.** |
| Rapid working set | `services/memory/working_set.py:33–85`; `scoped_accessor.py:178–210` | Mongo-backed reference use counters and bounded decay/eviction implementation exist. No production call sites for record-use/evict were found. No hot-set hit/miss/eviction benchmark or real short-query warm-ratio measurement. Eviction implementation currently enumerates a whole plane before trimming; scaling/index/uniqueness must be checked under a real workload. |
| Memory contribution/write-back | `services/memory/write_back.py:136–220`; `routers/memory.py` | Plane-scoped contribution storage and class/rights-at-birth checks exist. Its legacy five-ring stamp is a loose dict with a key-presence test, not full canonical ring validation (`write_back.py:106–128`, `contracts/memory_write_back_v0.py:51`). It does not explicitly require the relational-edges ring. Reconcile at the existing frozen-unit seam, not by creating another unit format. |
| Publication | `services/memory/publication.py:34–58,124–151`; `constants.py:51–61` | Publication threshold is unset by default and no environment setting was found in this preview; refusal is correct, not a bypass to remove. On pass, existing code marks a contribution registry-visible and records a `registry:memory:...` reference, but the examined path does not materialise a servable canonical Registry unit. Join that ceremony to the one asset writer/native proof path. |
| Compaction behaviour | `services/memory/compaction_v1/retention.py:62–79`; `operations.py:45–88,121–209` | v1 retains ALL claims; facts/receipts become pointers and other text stays verbatim. This can reduce fact text, but **does not demonstrate severe mixed-context reduction** or semantic preservation at high reduction ratios. No active trigger→compact→consumer flow found. A drafting interface exists but is intentionally unused. |
| Compaction durability | `services/memory/compaction_v1/chain_integration.py:170–238,246–327` | Reuses the one ledger and structurally gates reads on append receipt. Reader receipt/byte maps remain in-process dicts; no production caller or restart-reconstruction binding found. Ledger ordering is not equivalent to durable payload storage or restart recovery. |
| My Work/M5 | `frontend/src/App.js:1295–1297`; `components/prototype/osWorkModel.js:5–28`; `nexusWork.js:47–59` | Current My Work routes use `AdminEstate` and real operational request/history projections—not the obsolete static `WorkTasks.jsx`. Team/goals/board feeds and task-workspace documents/team/questions remain largely empty/unconnected in the active model. Connect those later against the owner's journeys, without replacing the established design. |

### Policy/reference reconciliation

- Personal user-memory **R-21 remains OFF**; rapid qualified-unit serving and per-app memory do not require silently enabling it.
- The decision log has numbering collisions and stale repeated summaries. It contains an explicit owner statement **“R-19, R-20: ratified, unaffected. R-21: stays off”** at `STATE/DECISIONS.md:20601–20602`, but other entries continue to label compaction R-19/R-20 pending and some use the same numbers for unrelated decisions. Bind activation to document-qualified ruling identity/version; do not invent new policy values or declare a new consent model from a bare R-number. This review does not re-ratify policy.
- Working-set cap/decay and publication threshold are configuration/benchmark slots, not measurements. No fabricated memory latency, compression ratio or hit rate is accepted.

## 3. Shared M4/M5 integration order

1. **One qualified-memory spine (M4 prerequisite, M5 reuse):** persistent canonical units + current rights + relational/source-position indexes → scoped bounded working set. Record hits/misses/use/eviction and keep application/user-memory boundaries distinct.
2. **One query decision:** frozen objective/session → warm qualified selection OR the specifically unconverged source slice through the existing M3 worker. No new estate walker in the answer service and no whole-estate refresh for a short question.
3. **Preservation at the model boundary:** native tokenizer measures whole-unit packing; model reads exactly the pinned window; trace/answer carry exclusions, class and limitations. Test contradictions and relevant low-frequency evidence, not only easy summaries.
4. **Durable compaction and reuse:** connect ruled triggers/retention to the existing single ledger and durable artifact custody, restart reload, source-specific regeneration and withdrawal. M4 depends on this when consuming compacted context; M5 owns continuity across runs/applications.
5. **M5 journeys after shared spine:** saved work, scoped handoffs, team contributions, goal evidence and versioned board decisions, using the journeys the owner will share. No need to defer all memory work until M5 or invent two memory services.

## 4. Required acceptance additions made explicit (not new numeric quality bars)

- **Heavy shrink test:** controlled stress cases with large reductions (e.g. 95%/99% working-context volume reduction as test inputs, NOT newly ratified targets). Preserve frozen objective/frame/floor, source truth and load-bearing relationships; disclose loss. If sufficient support cannot fit, answer narrowly or refuse rather than pretending completeness. Regenerate selected units from exact source positions and compare content-ring hashes.
- **No-estate-rerun test:** after building relevant units once, make multiple short and paraphrased/follow-up inquiries. Warm answers must produce **zero new source-extraction dispatches/reads**. A genuine gap creates one bounded slice, not a full census/extraction pass. Measure source rows/bytes touched, candidate counts, included tokens, hit/warm ratio, p95 latency and actual cost per tenant. No fixed latency claim before measurement.
- **Window determinism:** same objective/model/tokenizer/rule/population → identical selected order/exclusions; no downstream reranking. Exercise an oversized load-bearing unit and heavy exclusions, not just single-unit happy paths.
- **Restart/withdrawal seam:** publish/compact → restart → scope-checked reload → answer; withdraw one source and ensure stale hot references, compacted descendants, answers and artifacts cannot be reused outside valid rights. Eviction is not evidence deletion.
- **Multi-turn/cross-app seam:** preserve session/run/objective IDs, source versions and loss statements while moving answer → task/document → reopened answer; no duplicate chargeable job or audience widening.

These strengthen the explicit reading of existing M4-T1/T3/T4 and M5-T1/T2/T5. They do not add milestones, relax G3/G4/G5 or count parked journey work as complete.

## 5. Evidence and limits of this review

- Requirements and implementation/call-site review completed; a second read-only review was reconciled against actual route/dispatch code. Its over-broad “no chat backend” / “all dispatch is placeholder” statements are corrected above.
- Targeted regressions: 36 passed, 1 skipped; includes SYNTHETIC native context/memory metadata tests. Separate corrective-training tests: 4 passed; external authenticated training metadata checks: 2 passed (`test_reports/iteration_65.json`). These are **not** M4/M5 live semantic/latency acceptance.
- Preview smoke loads. No M4/M5 UI or production memory policy was changed. No entity/source query was sent to a model and no RMS estate extraction was run.
- M9 corrective campaign is separately commissioned in `notes/m9_corrective_training/`; successful training is not M9 acceptance.