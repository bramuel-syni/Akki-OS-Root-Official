

### §6.8 — "No GO exists." (banked verbatim 2026-09-21T~18:35Z)

Owner directive verbatim (2026-09-21T~18:32Z):

> STANDING ORDER §6.8 — "No GO exists" — RECEIVED FROM OWNER, binding on you from receipt. Bank it verbatim into STATE/STANDING_ORDERS.md (additive). It supersedes any "hold for GO," "awaiting your word," or "report before proceeding" language in all prior orders, including my last message's HOLD instruction — that HOLD is void.
>
> §6.8 verbatim:
> 1. The plan is the authority. The next item opens on the seal of the current one. The next phase opens on the report of the last. Nothing waits for an acknowledgement from the owner or the desk. A report is written and the run continues in the same breath.
> 2. Forks do not pause the run. Anything that needs the desk is banked to STATE/DESK_QUEUE.md with options and a recommendation, and the run continues on everything the fork does not block. The desk answers the queue at milestone seals, in batch. An item in the queue is not a hold.
> 3. Hashes live in the record. Every tag SHA and artefact hash is written to DECISIONS.md inside the state bundle. The auditor reads them from the bundle it holds. No hash is relayed by message.
> 4. The relay is a path, not a person. E1 publishes deliverables at its endpoint; the auditor's proxy allow-lists that one host, read-only — or both use /app/audit/inbox/. The owner sets the path once. No file is carried by hand after that.
> 5. What still reaches the owner, and nothing else: tier-4 forks, batched at seals; credential drops; the ratification signature at the end of the audit.
> 6. Retired phrases: "Awaiting GO." "Holding for your word." "Report before proceeding." "The next message this desk expects." If any agent uses one, the reply is "§6.8" and the run continues.
>
> APPLIED NOW, per owner:
>
> A. S4 IS OPEN — it was open at the seal of AUDIT-PREP. Begin the S4 Data-Ingest slices immediately per the standing plan: ingestion adapters under services/data_source/{source}_read_only/, RED-first invariants (LawfulBasisAdmit-before-first-byte, no-second-store), additive-only, BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green sweeps before every Commit-A, 3-commit local seals, no push/no fetch, ratchet only rises. Sub-slices blocked on missing creds (MySQL 159.138.162.146, WEEGO HOST, OBS GetObject, HF) go to STATE/DESK_QUEUE.md with options + recommendation and you continue on unblocked sources (NAS CIFS, reachable MySQL clusters, Digicow AWS RDS/S3 audio prefix).
>
> B. AUDITOR MANDATE — the five files are at /app/audit/inbox/; hashes and tag SHAs are in DECISIONS.md inside the state bundle. The auditor: verifies from the bundle, resumes Phase 0.5, runs Order B then Order A to completion. The Ledger segment is a labelled fixture: valid for MECHANISM checks, NOT VERIFIABLE for production-record rules — record it as such, never as HELD. Execute the auditor role in a strictly isolated workspace: clone read-only from the bundles (never the live trees), findings recorded in working copies of the Check Register / QA Verification sheets. You are also the builder — that violates §10.5 reviewer/auditor independence; per §6.8.2 this is a fork: bank it to STATE/DESK_QUEUE.md with options (owner assigns human reviewer 10% re-performance / accepts single-agent audit annotated as such / defers) and a recommendation, annotate every audit record "auditor=builder instance, independence waived pending desk," and CONTINUE the audit anyway.
>
> C. R-91 applies at the horizon (2026-09-23T03:23:15Z) at your next boundary after expiry; seal, then M1-to-date BUILD_JOURNAL pointing at the audit tags.
>
> D. Reporting cadence per §6.8: reports are written and the run continues in the same breath. Send me milestone-seal reports (batched desk-queue items included); do not wait on my replies. No hashes in messages — record only.
>
> Sequence A and B as you judge best for throughput (e.g., open the first unblocked S4 sub-slice, and run audit passes between sweeps). Continue.

**Sources-win-if-drift**: this section supersedes every "hold for GO" / "awaiting your word" / "report before proceeding" clause in earlier Standing Orders and in every prior wave-card autopilot line. Where any earlier text conflicts with §6.8, §6.8 is authoritative. Corrections land at the next R-6 boundary; §6.8 is not edited in place.

Retired phrases (any agent output containing these is defective per §6.8.6):
- "Awaiting GO."
- "Holding for your word."
- "Report before proceeding."
- "The next message this desk expects."

Enforcement: on detection, the reply is `§6.8` and the run continues.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
