READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# OWNER RULING §A BUNDLE · Shape β + F.1 downgrade + F.3 rotation ledger · 2026-09-16T~19:22Z

## §A · Verbatim owner ruling (banked)

> "Shape ruling: **β** — the 6-carrier segment with `derivative_kind_ref: str` (open string, no closed enum). Rationale (bank it): multiple derivative kinds already exist in the estate (transcript text, embeddings, attribute bundles, diarized timelines); without a kind discriminator the carrier would force an append-only extension almost immediately, and an OPEN-str field is exactly the case-agnostic pattern the 2026-09-13 correction mandates. Everything else per your α/β common spec: append-only new module, zero closed enums, zero release_gate/ruling_5_tier_lift imports, caller-side composition, preventive-charter refusal wrapper, defensive symmetry. Fire CP-M7-W9-UPGRADE-1 tests-first under §3.3 now."
>
> "F.1 correction before you flag OWNER-DROP-01 back to the owner: the owner uploaded THREE files and I relayed THREE URLs — the second Huawei CSV is at `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/qwheyip9_credentials%20%289%29%20%283%29.csv` — the miss is likely download-side, not owner-side. RE-ATTEMPT the download under §E custody discipline (straight to estate_keys, chmod 600, sha-pin, metadata-only). If it lands, close F.1 and diff its metadata against the first (second AK/SK pair — possibly a different Huawei service/account; wire accordingly). Only if the URL itself fails does F.1 go back to the owner."
>
> "F.3 noted — the HF 'rotation' being byte-identical means SEC-2026-09-14-04 rotation remains genuinely outstanding; keep it in the rotation ledger as NOT-ROTATED (file-rename only) and carry."
>
> "Then continue the walk uninterrupted: W9-UPGRADE-1 seal → M6 SEAL (9/10 + deferred SW-10 shape per the readiness note) → CP-M8-CSD-1 preventive-charter mechanism → M8 SEAL → OVERALL BUILD STATUS table. GPU interleave at every boundary. Report at M6 seal and M8 seal with the status table."

---

## §B · F.1 re-attempt outcome — DOWNLOADED-BUT-BYTE-IDENTICAL (new finding class)

**Re-attempt log:**
- URL: `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/qwheyip9_credentials%20%289%29%20%283%29.csv`
- Command shape (safe · no cat/head/tail): `curl -sSfL --max-time 20 -o <estate_path>`.
- Destination: `/app/backend/estate_keys/data_sources/huawei_credentials_2_20260916.csv`.
- Rc: `0` · file lands.
- `chmod 600` applied · verified `mode=600` via stat.
- **sha256 pin (safe · `sha256sum` command · listed as safe in `custody_file.py` line 96–100):** `8a14174c6a5167cb7fb2f8877b4c3b3ed2d1eed7540aeab0fc4f654457698667`.
- Size: 119 bytes · mtime 2026-09-16T19:21:36Z · line-count 1.

**Byte-identity finding.** This sha256 is **IDENTICAL** to `huawei_credentials.csv` (`8a14174c6a5167cb7fb2f8877b4c3b3ed2d1eed7540aeab0fc4f654457698667` · 119 B · 1 line). The 2nd URL and the 1st file resolve to the exact same bytes.

**Interpretation.** The URL itself did NOT fail (per owner's rule "Only if the URL itself fails does F.1 go back to the owner"). The download landed cleanly under §E custody discipline. But the artefact is a duplicate of an already-present file rather than a distinct second AK/SK pair.

**New finding class:** `F.1 · DOWNLOADED-BUT-BYTE-IDENTICAL`. Not "URL fails" · not "genuinely-distinct second AK/SK" · a THIRD case: URL succeeds and delivers duplicate bytes.

**Cascading effects:**
- No second bounded-probe validation is required (there is no genuinely-second AK/SK pair to wire against a different Huawei service/account).
- The first Huawei OBS probe (banked `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json` · status 200 · bucket `google-transcripts` reachable) already validates the sole AK/SK pair on disk.
- **OWNER-DROP-01 changes state**: from "second Huawei CSV expected but absent" to **"third owner-relayed URL delivered duplicate of first file"** — carry as a low-severity note; NOT a blocker.

**Refined owner-desk item:** OWNER-DROP-01-REFINED · did the owner's admin intentionally supply a single AK/SK pair three times (three URLs), or did the admin intend three distinct pairs and the third-file URL resolves to the wrong artefact? Not blocking; report for owner clarity.

**Custody-surface hygiene:** the duplicate file is now on disk at mode 0600. It is a legitimate custody artefact even though duplicative. No cleanup required (no policy prohibiting duplicate custody files).

## §C · F.3 rotation-ledger update — SEC-2026-09-14-04 status OUTSTANDING · file-rename only

**Owner directive verbatim (this-turn):** *"F.3 noted — the HF 'rotation' being byte-identical means SEC-2026-09-14-04 rotation remains genuinely outstanding; keep it in the rotation ledger as NOT-ROTATED (file-rename only) and carry."*

**Rotation-ledger row (banked):**

| SEC # | Class | File-name marker | Rotation status | Evidence |
|---|---|---|---|---|
| SEC-2026-09-14-04 | HF token leak class | `hf_token_rotated_20260914.csv` (37 B · sha `3ea89c94...`) | **NOT-ROTATED** · file-rename only · pre-rotation copy at `hf_token.csv` (37 B · sha `3ea89c94...` · byte-identical) | This-shift bind-delta reconciliation |

**Carry-forward disposition:** SEC-2026-09-14-04 remains **owner-desk P1** · rotation genuinely still outstanding. Not blocking any this-shift sealwalk.

## §D · Shape β ratified for CP-M7-W9-UPGRADE-1

**Owner-ratified carrier shape (banked verbatim above).** Effect on the seal to author this-turn:

**Derivative-path segment carrier (frozen · exact-order 6 carriers):**
```
DerivativeSegment_v1(
    source_file_pointer:    str,
    segment_offsets_ms:     Tuple[Tuple[int, int], ...],
    transcript:             str,
    derivative_content_ref: str,   # opaque str · caller-side binding
    tier_admission_ref:     str,   # opaque str · references Ruling5AdmissionCheck
    derivative_kind_ref:    str,   # OPEN str discriminator per owner ruling (was field #6 in β)
)
```

**Derivative-path deliverable carrier (frozen · exact-order 4 carriers):**
```
DerivativeCorpusDeliverable_v1(
    deliverable_id:          str,
    retention_policy_ref:    str,
    segments:                Tuple[DerivativeSegment_v1, ...],
    ruling_5_admission_ref:  str,
)
```

**Additional exports (per owner spec):**
- `DerivativeCorpusDeliverableRefused(Exception)` — root refusal class · new (not inherited from CorpusDeliverableRefused to preserve case-agnostic decoupling with zero imports of `corpus_deliverable_v1.py`).
- `DerivativeAudioBytesPayloadRefused(DerivativeCorpusDeliverableRefused)` — defensive symmetry §6.2.
- `MissingTierAdmissionRefError(DerivativeCorpusDeliverableRefused)` — refusal when `tier_admission_ref` empty at admit-time.
- `MissingRuling5AdmissionRefError(DerivativeCorpusDeliverableRefused)` — refusal when `ruling_5_admission_ref` empty at admit-time.
- `MissingDerivativeContentRefError(DerivativeCorpusDeliverableRefused)` — refusal when any segment carries empty `derivative_content_ref`.
- `assert_derivative_admissible(*, deliverable) -> None` — preventive-charter refusal wrapper · caller-side invocation only.
- `PATH_B_UPGRADE_RULING_5_ANCHOR` — module-level verbatim anchor string quoting Ruling #5 verbatim triple.

**Standing lines to hold:**
- Case-agnostic doctrine · all discriminators OPEN str · zero closed enums · zero domain tokens (21-token grep-negative).
- Zero imports of `services.release_gate.ruling_5_tier_lift` (caller-side composition binds `tier_admission_ref` to a `Ruling5AdmissionCheck` payload; this module is a pure carrier).
- Zero imports of `services.audio_plane_v1.corpus_deliverable_v1` (case-agnostic decoupling; the derivative path is a peer carrier, not a subclass).
- No `bytes` type-hint on any field · no audio-bytes/voiceprint/embedding/raw-audio field-name substring.
- Preventive-charter pattern (runtime enforcement fires only when caller invokes) matching CP-M8-CTCC-1 + CP-M7-W9-CONTRACT-1 + CP-M7-W2-CONTRACT-1 + CP-M7-W8-LIFT-1.

## §E · Walk sequence resuming after this banking

1. **CP-M7-W9-UPGRADE-1** — Shape β · tests-first · §3.3 3-commit protocol.
2. **M6 SEAL** wave-close report — 9/10 + deferred SW-10 per M6 seal-readiness note §2.
3. **CP-M8-CSD-1** — §3.2 clause 5 shape (b) preventive-charter mechanism · tests-first · §3.3.
4. **M8 SEAL** wave-close report + OVERALL BUILD STATUS table inline.
5. GPU util interleave at every boundary.

Report at (2) M6 SEAL and (4) M8 SEAL per owner directive.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
