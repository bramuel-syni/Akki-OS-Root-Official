# STATE/DESK_QUEUE.md

Batched fork queue per Standing Order §6.8.2. The desk answers at milestone seals; an item in this queue is **NOT** a hold — the run continues on everything the fork does not block.

Each entry carries: **fork id · surfaced-at seal · options · recommendation · what it blocks · what it does NOT block (i.e., what continues)**.

---

## DQ-01 · Auditor–Builder independence violation (§10.5 vs §6.8.2)

- **Surfaced at**: AUDIT-PREP-20260921 seal (state Commit-A `433748dc…`).
- **Fact**: Standards v2 §10.5 requires reviewer/auditor independence from the builder (10% re-performance by an independent reviewer). This E1 instance is both builder (Extraction-Akki backend) and auditor (Order A + Order B execution).
- **Options**:
  - **(a)** Owner assigns human reviewer for the 10% re-performance sample.
  - **(b)** Owner accepts single-agent audit annotated at every finding as `auditor=builder instance, independence waived pending desk`.
  - **(c)** Defer audit findings ratification until an independent reviewer is available; keep audit running to produce evidence for later re-performance.
- **Recommendation**: **(b)**. The owner directed §6.8 to open the audit self-running, so independence is knowingly waived; annotating every record is the cheapest reversible option and preserves optional (a) later.
- **Blocks**: audit ratification signature (per §6.8.5, that reaches the owner at completion).
- **Continues**: all audit passes (Order B Q-1..Q-11, Order A Part 0/I). Findings will land annotated per (b) throughout.

## DQ-02 · Deliverable count mismatch (five hashes vs owner-asked four)

- **Surfaced at**: AUDIT-PREP-20260921 seal.
- **Fact**: `programme/track-a` and `master` live in two different repos, so one `git bundle create` cannot cover both. Two bundles produced. Owner's Step 4 language ("owner asked for four hashes; with two bundles you will report five — flag the count and why") already anticipated this; flagging here for completeness.
- **Options**: **(a)** Accept as delivered · **(b)** Adjust protocol to require single-repo consolidation (breaks assessment_workspace / Extraction-Akki topology).
- **Recommendation**: **(a)**. The five hashes are recorded in DECISIONS.md and PINS.md inside the state bundle per §6.8.3.
- **Blocks**: nothing.
- **Continues**: everything.

## DQ-03 · S4 sub-slice blocked · MySQL `159.138.162.146` credentials

- **Surfaced at**: CP-ESTATE-INGESTION wave-card AUTHOR (2026-09-21T13:15Z); confirmed still blocked at AUDIT-PREP seal.
- **Fact**: Fresh RMS creds sheet (2026-09-21) omitted this host. All other MySQL hosts in the ingestion scope authenticate.
- **Options**: **(a)** Owner supplies working creds for `159.138.162.146:3306` in next credential drop · **(b)** Owner explicitly de-scopes this host from S4 · **(c)** Owner supplies IP allowlist relaxation on the host so JUMP can reach a re-issued admin cred.
- **Recommendation**: **(a)** — the "MICROSERVICES-primary" DB is a named scope target; option (b) loses a scope target; (c) still needs a cred drop.
- **Blocks**: S4 sub-slice for host `159.138.162.146` only.
- **Continues**: all other MySQL sub-slices (8 of 9 hosts proven authable), NAS CIFS, Digicow AWS RDS/S3.

## DQ-04 · S4 sub-slice blocked · MySQL `HOST` placeholder (WEEGO)

- **Surfaced at**: CP-ESTATE-INGESTION wave-card AUTHOR; confirmed still blocked at AUDIT-PREP seal.
- **Fact**: The fresh creds sheet has valid credentials for WEEGO but the host cell contains the literal string `HOST` (placeholder), not an IP.
- **Options**: **(a)** Owner supplies IP · **(b)** De-scope WEEGO.
- **Recommendation**: **(a)**.
- **Blocks**: WEEGO ingestion sub-slice only.
- **Continues**: everything else.

## DQ-05 · S4 sub-slice blocked · Huawei OBS `obs:object:GetObject` scope missing

- **Surfaced at**: HUAWEI-OBS-ACCESS-DRILL seal (part of `18b4d85…`).
- **Fact**: Current rotated AK/SK (`HPUA…`) authorises `ListBuckets` and `ListObjects` (verified 200 OK against multiple buckets across regions), but `GetObject` returns 403 across all tested buckets. Region-routing bug already ruled out.
- **Options**: **(a)** RMS admin extends IAM policy to include `obs:object:GetObject` on the audit-scope buckets · **(b)** Owner supplies a second AK/SK pair with wider scope for read ingestion · **(c)** De-scope object-body reads from S4 (keep bucket/object metadata only).
- **Recommendation**: **(a)**. GetObject is required to satisfy "read every byte through a ledgered ExternalRead event" — metadata-only is a scope regression per Doc 5 B5.4.
- **Blocks**: OBS object-body ingestion sub-slice (any surface that requires reading object bytes).
- **Continues**: OBS metadata-level manifest work (ListObjects → manifest → LawfulBasisAdmit rows can still be prepared and emitted).

## DQ-06 · HuggingFace ingestion credentials

- **Surfaced at**: HF-HOLD SEC-2026-09-12-01 (still standing).
- **Fact**: HF hold is still active per §4.1 §E; no HF token supplied.
- **Options**: **(a)** Owner drops HF read token · **(b)** HF hold remains in force → no HF ingestion this milestone.
- **Recommendation**: **(b)** unless a corpus is specifically needed by an in-flight card. HF-HOLD is standing; no card in flight requires it.
- **Blocks**: any HF-sourced ingestion sub-slice.
- **Continues**: everything else.

---

## Standing rules for this file

- Additive-only. An entry is closed by an owner desk-answer at the next milestone seal; **closed entries are struck-through, not deleted**, so the queue keeps its history.
- Items are ordered by surface-at-seal timestamp, oldest first. New items append.
- Every entry cites the seal at which it was surfaced.
- Every entry states **what continues** — not just what blocks — so the run's non-blocked breadth is visible at a glance.
