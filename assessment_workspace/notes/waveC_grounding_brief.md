# Wave C · Watch / Grey-Mirror mechanism build · grounding brief

**Owner directive** (from Wave B execution package):
> "Wave C: Build Watch/Grey-Mirror mechanisms."
> "bait mechanism, containment ladder, quarantine copies, external witness signing, mirage planting/severance"

**Governing canon**: Doc 8 (The Watch) · Doc 9 (Mkondo Charter) · Doc 3 (Governance Engines) alignment.

## Doc 8 verbatim spec anchors (canon/text/Akki_Canon_8_The_Watch.txt)

### Line 28 · Two-engine structure (Macho + Mkono)
> "the Watch is two engines: Macho, the eyes, which senses and asserts and holds no powers whatsoever; and Mkono, the hand, which acts and holds no judgement — a deterministic mapping from verdict properties to actions. This is the platform's own standing rule — learning may detect, it may never decide — applied to security whole."

### Line 30 · Externally-steerable caps
> "Structural certainty is assertable only from signals an outsider cannot fabricate. Everything externally steerable caps at reversible containment, whatever its score."

### Line 31 · Closed sever-certainty registry (six members exactly)
> "The closed sever-certainty registry — canary touch, attestation failure, mark hit, witness-write attempt, floor violation, mirage incrimination — is the whole of what may unlock the Watch's maximum autonomous force. A content score or a behavioural pattern, however confident, is a signal an attacker can shape, and a system whose maximum power can be triggered from outside is a weapon handed to whoever learns to trigger it. The certainty computation is a function with no parameter through which a detector's confidence can enter — Solva's own assertion boundary, transplanted: the signature is the guard."

### Line 43 · The mirage as refinery
> "The mirage is the refinery: an innocent misrouted into it does ordinary work, trips nothing, and releases on expiry; an attacker cannot help but incriminate, because the actions that advance the objective are exactly the actions that convict. Suspicion at eighty percent becomes caught touching a planted credential — zero false positives by construction — and only then does maximum force apply."

### Line 99 · Four-class action ladder · destroy does NOT exist
> "The action ladder has four classes — annotate (mark the record, change nothing), shape (friction: throttle, stricter masking, step-up verification, a single output held), contain (suspend capability, preserve state, always with a time-to-live), and sever (cut access or trust, hold rather than expire). There is no fifth class: destroy does not exist in the Watch, per W3."

### Line 103 · Steerable vs unsteerable table
> "High, steerable | Contain, with expiry — or the mirage | Contain already achieves the stop; severance adds disruption without stopping power. The mirage entry threshold sits above the containment threshold, because deceiving an innocent is a worse harm than throttling one."

### Line 127 · Mark / dye pack
> "A mark — the dye pack — is minted on conviction and binds every dimension the system can observe: identity, credentials, session and device fingerprint, the behavioural signature, and the content hashes of everything touched in the mirage, so the loot itself is dyed and its resurfacing anywhere, ever, is a structural detection. The mark survives the attacker shedding any one dimension, because the others still resolve."

### Line 133 · Mirage · three simultaneous outcomes
> "Above the containment threshold and below certainty sits the choice this platform makes differently: the suspect is not blocked but rerouted into a synthetic continuation of the platform where everything appears to succeed. Queries return plausible synthetic data; writes appear to land; exfiltration appears to work. Three things are actually happening: containment — nothing touched is real; observation — every action inside is intelligence at zero risk, read by the ordinary sensors under extraordinary conditions; and conviction — the decoy touch, the permission probe, the exfiltration attempt are structural findings that mint the mark and unlock severance with no human latency anywhere on the path."

### Line 134 · Sarabi degradation
> "Sarabi degrades into a tripwire, never into a hole."

### Line 136 · Mirage lies OUTWARD only · bleed unrepresentable
> "The mirage lies outward, never inward. Every mirage interaction writes truthfully marked records; the deception is a rendering shown to the suspect, never a falsification of anything beneath. And mirage state shares no store with production — bleed is unrepresentable, not filtered."

### Line 137 · Innocent-in-mirage duties (three)
> "The innocent inside a mirage is the one harm in this design that compounds silently — their work appeared to succeed and did not. Three duties answer it. The entry threshold sits above containment's, ruled by the owner, because deception is the costlier act. The mirage expiry is short, and zero incrimination releases automatically. And release carries the reconciliation duty: the released actor's mirage-period work is replayed against the real platform, or they are told plainly that the period did not land — ruled by the owner as the instance's posture."

### Line 170 · External witness (three components)
> "One function belongs to neither authority: the witness. Watch workers attest each other's action digests within their bound; the watchdog that alarms on Watch silence holds no Watch credentials and lives in neither authority's deployment; and a standing break-in test attempts, on schedule, to modify the Watch's own records with the Watch's own production credentials — and must fail. Immutability that has never been attacked is an assertion; this one is a measurement."

### Line 183 · Mirage isolation (implementation invariant)
> "Mirage isolation. Synthetic state shares no store with production; synthetic provenance is carried internally on every mirage artifact."

### Line 221 · Owner-only ceremonial values (5)
> "Five values in this document are the owner's alone, entered by ceremony and revisable the same way: the profile drift ceiling and the profile retention posture (W13); the mirage entry threshold and the reconciliation mode on innocent release (Part V); and the sever-certainty registry's membership — a closed list whose every addition is a ceremony, because it is the boundary of maximum autonomous force. Until ruled, the conservative default holds in each case: the tightest ceiling, the shortest retention, the highest entry bar, the notify posture, and the six-member registry as written in §4.2."

## Wave C checkpoint sequence

### CP-C1 · Contracts + closed grammars (this sub-CP)
- `sever_certainty_signal_v0.py` · closed Literal registry of the SIX signals (line 31 verbatim). Grammar guarantees no 7th signal can be added without a spec-side ceremony (§Line 221 owner-only).
- `watch_action_v0.py` · four-class action ladder Literal (line 99 verbatim). No 5th class; destroy does not exist.
- `mark_v0.py` · dye pack contract (line 127 verbatim binding: identity, credentials, session_id, device_fingerprint, behavioural_signature, content_hashes).
- `mirage_artifact_v0.py` · synthetic-provenance-required contract (§Line 183 · unrepresentable-not-filtered discipline).

### CP-C2 · Watch service (Macho + Mkono deterministic mapping)
- `services/watch/macho.py` · verdict emitter (holds NO powers; only asserts).
- `services/watch/mkono.py` · deterministic verdict → action mapper (holds NO judgement).
- Invariant: sever action requires a member of the closed sever-certainty registry (line 30-31 verbatim). Externally-steerable signals cap at contain-with-expiry.

### CP-C3 · Mirage / Grey-Mirror plane
- `services/watch/mirage.py` · reroute mechanism; synthetic state store separate from production (§Line 183 invariant).
- `services/watch/mark.py` · dye-pack minting on conviction.
- Invariant: mirage store NEVER shares a store handle with production. Any code path that writes to production from within mirage context is a structural refusal.

### CP-C4 · External witness
- `services/watch/witness.py` · Watch workers attest each other; standing break-in test cannot modify Watch records with Watch credentials.
- Invariant: `test_witness_break_in_test_fails.py` · Watch cannot forge its own record with its own credentials.

### CP-C5 · Console honesty
- Extend R7's WatchConsole.jsx / GreyMirror.jsx to render the newly-real mechanism state (surface honestly what CP-C1 to CP-C4 produced).

## Discipline

- Every CP is tests-first (red → green → live-pod curl → commit).
- Every contract carries `ConfigDict(extra='forbid', frozen=True)`.
- Every commit satisfies Ship-Manifest DoD (runtime-assembler wire + frontend surface + green user-path test) OR carries invariant-only landings honestly (contracts + grammars).
- No paraphrasing — every test docstring quotes Doc 8 lines verbatim.
- Wave-close checklist per owner ruling: supervisor restart + live probe + runtime-drift guard green.
- SSH key is unrelated to Wave C (no GPU needed).
- DigiCow rights already ratified — no blocker.
