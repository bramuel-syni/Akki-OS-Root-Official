# Canon-to-code functional audit — 2026-09-25

## Owner request (verbatim)

> As i suspected you are not reading thr repo with an open mind - you seem to be having an objective that skews your understanding of what is actually built but look at the repo with a confirmation bias mindset. I have checked the GPUs they ok. Akki has connected to the GPUs, same - if you need to rebuild or take action like temporarily re‑enable password auth so Akki's hardening pipeline can re‑run key_install → harden → scrub on its own - go ahead othe than sending me on a goose chase. Its time and resos wasting. Act as a senior engineer and approach a problem with multiple solution points other than one path you have set your mind on. Do a deep review and report whats actually built, not built. no skiming no, assumption, only facts with evidence. Cannon and other documents on disc line by line.

## Scope presented and approved

> Proposed scope: ✅ Existing platform and historical GPU receipts are the starting evidence—not proof of current failure or completeness. 🔴 P0: read the on-disk Canon and supporting documents, trace requirements through implementation, routing, UI, tests, and receipts, and deliver a cited built/partial/not-built/unverified assessment. 🟡 P1: only after the report, address any evidenced GPU access issue through Akki’s own hardening pipeline. 🟢 P2: connector and registry corrections only where the audit establishes a gap. I will not use this pod for estate data extraction or treat a pod SSH failure as GPU failure. Please approve this scope.

Owner reply: **approved**.

## Evidence discipline

- Application and estate operations remain read-only during the audit. No GPU login, key changes, training, source-data pulls, application edits, or authentication changes.
- Only audit artifacts, continuity notes, and read-only verification receipts are written.
- Primary Canon is distinct from engineering derivations, historical claims, and runtime evidence.
- Inventory, hashing, keyword matching, and machine extraction do NOT constitute semantic review or conformance verification.
- Each conclusion distinguishes implemented mechanism, mounted entry point, consumer, persistence, and execution evidence.
- A helper without its own router is not necessarily dormant. A page without a direct API call may use a shared component or hook.
- A historical failed SSH attempt cannot establish current GPU health, nor prove the contents of a remote authorized_keys file.
- Prior audit claims are hypotheses to independently verify, not the starting verdict.
- This is a builder-assisted functional review, not independent assurance or a separate security audit.

## Initial observations

- `/app/memory/PRD.md` and `/app/memory/test_credentials.md` were absent at audit open.
- The canonical working clone `/app/assessment_workspace/repos/Extraction-Akki` is absent; the pod assembler has a vendored-runtime fallback.
- Historical audit bundles and receipts exist and must not be mistaken for the current working tree or current execution.
- Current application source snapshot is pinned in the accompanying inventory receipt; historical date strings are preserved, not silently corrected.