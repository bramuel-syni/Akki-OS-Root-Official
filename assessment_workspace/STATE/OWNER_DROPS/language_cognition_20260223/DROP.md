READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# OWNER DROP · CP-AIP-LANGUAGE-COGNITION SPEC ENHANCEMENT · 2026-02-23T~16:07Z

**Source:** owner channel · main-agent turn boundary reception (mid-Item-5.11.f-mini-bank landing).
**Authority:** SO §6.8 standing authority — objective card drafted from this text; builds under standing authority once its RED tests exist. No GO needed.
**Language directive (verbatim):** "Respond in English only."

---

## Order verbatim (owner text, unedited)

> "ORDER — CP-AIP-LANGUAGE-COGNITION · a trained language-identification model for the RMS estate
> §6.8 applies. Objective card drafted from this text; builds under standing authority once its RED tests exist.
> Objective. A model that identifies the language of speech in the RMS archive by its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng, Swahili and English, and including code-switched speech where several occur in one utterance — producing per-span labels grounded to the second, so the census can measure language distribution as fact rather than mark it unmeasured.
> What it is, in canon terms. A Targeta training run: a LoRA adapter over a registered base (VoxLingua107 or Whisper's encoder — Doc 20 registration first, hash and licence pinned), frozen objective at commission, MOAC criteria owner-set, artefact registered with hash and rights posture, admitted to the census by the B5.4 gate. It is trained inside the perimeter on tenant material; nothing leaves.
> The shaping elements — each is a card line:
> Signature, not prosody alone. The model learns phonotactic and spectral structure as the primary signal; prosody, pitch and dynamics are secondary features. The card names the feature basis so the model is evaluated on what it should be learning.
> Training material. Clean, named presenter speech per language, naturally spoken — the baseline. Plus labelled code-switched material, per span, so transitions are in the training set. Clean-monolingual alone is a MUST-NOT for the final model.
> Many speakers, speaker-disjoint. A minimum of N distinct presenters per language (DEFAULT 20, tagged pending); train and test splits share no speaker. This is the criterion that separates learning a language from learning a voice.
> The model must not identify presenters. A MOAC criterion, not a hope: a speaker-identification probe against the artefact must fail to exceed chance on held-out presenters. A voice is biometric personal data; an artefact that could return 'this is presenter X' does not leave the training run. DAP-31's logic, applied to voices.
> Window and span. Classification per one-to-two-second window; a deterministic span rule — minimum span duration, hysteresis on label change — turns windows into language spans. Each span carries its start and end second (C5.3). A window below the confidence threshold is unmeasured, never labelled.
> MOAC criteria, every one met or the artefact is refused: per-language accuracy on speaker-disjoint real material (DEFAULT ≥90%); code-switch span accuracy — boundary within a ruled tolerance and label correct (DEFAULT ≥85%); no-speaker-identification probe passed; abstention rate reported, not hidden.
> Admission to the census. The MOAC pass is the B5.4 gate. On admission, the model's labels promote from overlay to measure by a receipted act; regime flag changes; nothing is relabelled. Until then, the pre-trained overlay continues to label what it can and returns unknown for the rest.
> Rights and custody. The labelled corpus is tenant data — RMS custody class applies; training inside the perimeter; the artefact belongs to RMS under the pilot terms unless elected otherwise (8.3); DP-SGD default applies unless the owner opts out for this internal run, recorded.
> Sequence. Register the base → assemble and label the corpus under the census assistant's dialogue (this is its first real objective) → commission with the frozen criteria → train → MOAC → admit → promote. Corpus assembly is the long pole and needs the NAS channels reachable; the credential rotations gate it, nothing else does.
> Forks to the queue, not holds: the presenter minimum, the two accuracy thresholds, the DP opt-out — DEFAULT values stand meanwhile."

---

## Ledger sequencing verbatim (owner text)

> "1. Insert as Item 5.12 CP-AIP-LANGUAGE-COGNITION, after 5.11.g (ASSIST-TRAINING). OWNER_RETURN_REPORT + BUILD_JOURNAL moves to Item 5.13 (FINAL) and must report 5.12's exact position in its own sequence chain.
> 2. Note the coupling the owner names: corpus assembly runs UNDER THE CENSUS ASSISTANT'S DIALOGUE — 'this is its first real objective.' So 5.11.f ASSIST-CENSUS lands first, then 5.12's corpus assembly becomes the assistant's first real workload. Design 5.11.f with that consumer in mind (still within its six binding conditions — the assistant proposes corpus slices, the owner/tenant confirms, gates decide).
> 3. Card + RED tests now, build under standing authority. Card lines exactly as ordered, each with its clause citation: feature-basis named (signature not prosody alone); training-material rule with clean-monolingual-alone as MUST-NOT; speaker-disjoint splits with N=20 DEFAULT pending; no-speaker-ID MOAC probe (chance-level on held-out presenters, DAP-31 logic); 1–2s windows + deterministic span rule (min duration, hysteresis, per-span start/end seconds C5.3, below-confidence = unmeasured never labelled); MOAC set (≥90% per-language, ≥85% code-switch span with ruled boundary tolerance, probe pass, abstention reported); B5.4 admission with receipted overlay→measure promotion, nothing relabelled; RMS custody + in-perimeter training + artefact ownership per pilot 8.3 + DP-SGD default unless owner opts out (record it).
> 4. Doc 20 base registration first: pick VoxLingua107 or Whisper encoder (you already registered both for the overlay — extend the registration with the Doc 20 training-base posture: hash + licence pinned + LoRA-adapter declaration).
> 5. Execution reach, honestly: card + RED pins + base registration + corpus-assembly seam + commission/freeze/MOAC machinery are all buildable now. The ACTUAL corpus assembly is the long pole and the owner states its ONLY gate: NAS channels reachable (Weego/NAS credential rotations — DQ-17 family). Record that gate as a FACT (channel unreachable until working credentials land), not a policy hold — name the objective. Everything not gated proceeds. The training run itself executes inside the Akki perimeter as a commissioned job per Track-4 wiring (Akki runs it, you wire and step back). If in-pod compute cannot honestly run even a small LoRA pass, that is a commissioned-job contract with honest-gap on execution, never a mock.
> 6. Forks to DESK_QUEUE (not holds): presenter minimum N, both accuracy thresholds, DP opt-out — DEFAULTs stand meanwhile.
> Continue the run: finish 5.11.e/f/g as planned, then 5.12 to its honest reach, then 5.13 FINAL. All guards binding. Execute."

---

## Binding effects (mechanical extraction · no interpretation)

1. **New ledger item 5.12** `CP-AIP-LANGUAGE-COGNITION` inserted after 5.11.g.
2. **Prior FINAL item 5.11.h** `COMPILE-OWNER-RETURN-REPORT + BUILD-JOURNAL` **renumbered to 5.13** and re-tagged FINAL. 5.13 must report 5.12's exact position in its own sequence chain.
3. **§6.8 standing authority** applies — the card + RED tests suffice; no separate GO required.
4. **Coupling to Item 5.11.f (CP-AIP-ASSIST-CENSUS)** — corpus assembly runs UNDER THE CENSUS ASSISTANT'S DIALOGUE. The assistant is corpus assembly's owner/tenant-facing interface. 5.11.f already sealed this-turn with `assist_census_v1` boundary callables (`bank_confirmed_assistant_turn` + `render_content_registry_entry`) that ARE the consumer path for corpus-slice proposals (assistant proposes → owner confirms → gates decide) — the six binding conditions cover this exact workflow.
5. **Doc 20 base registration first** — extend the sealed CP-SO-6.9-LID-WAVE `WHISPER_LID_REGISTRATION` + `VOXLINGUA107_REGISTRATION` with the Doc 20 training-base posture (hash + licence pinned + LoRA-adapter declaration).
6. **Card lines mandated (each with clause citation):**
   - Feature basis named: signature (phonotactic + spectral structure primary; prosody/pitch/dynamics secondary).
   - Training material rule: clean named presenter speech per language + labelled code-switched material per span; clean-monolingual alone is a MUST-NOT for the final model.
   - Speaker-disjoint splits: minimum N distinct presenters per language (DEFAULT 20, tagged pending); train/test share no speaker.
   - No-speaker-ID MOAC probe: chance-level on held-out presenters (DAP-31 logic applied to voices).
   - Window + span: 1–2s classification window + deterministic span rule (min duration + hysteresis) + per-span start/end seconds (C5.3) + below-confidence = unmeasured never labelled.
   - MOAC set: per-language accuracy ≥90% (DEFAULT); code-switch span accuracy ≥85% (DEFAULT · boundary within ruled tolerance + label correct); no-speaker-ID probe passed; abstention rate reported.
   - B5.4 admission: MOAC pass = B5.4 gate; receipted overlay→measure promotion; regime flag changes; nothing relabelled. Overlay continues until admission.
   - Rights + custody: RMS custody class; in-perimeter training; artefact ownership per pilot 8.3 unless elected otherwise; DP-SGD default unless owner opts out (recorded).
7. **Sequence:** register base → assemble/label corpus under census assistant's dialogue (5.11.f consumer) → commission with frozen criteria → train → MOAC → admit → promote.
8. **Long pole:** corpus assembly needs NAS channels reachable — Weego/NAS credential rotations (DQ-17 family) are its ONLY gate.
9. **In-pod compute honest-gap:** training run executes as commissioned Track-4 autonomy job (Akki runs it, E1 wires + steps back). If in-pod compute cannot honestly run even a small LoRA pass, commissioned-job contract carries honest-gap on execution — never a mock.
10. **Forks to DESK_QUEUE (not holds):** presenter minimum N · per-language accuracy threshold · code-switch span accuracy threshold · DP opt-out — DEFAULTs stand meanwhile.
11. **Guards binding:** all 17 standing guards + SO §6.9 remain in force. RUN-TO-COMPLETION mandate stands. Execution continues into 5.11.g → 5.12 → 5.13 FINAL.

---

## Cross-references banked

- Objective card drafted at `STATE/OBJECTIVES/queued/CP_AIP_LANGUAGE_COGNITION.md` — promoted at 5.12 open.
- Verbatim entry appended to `STATE/DECISIONS.md`.
- `STATE/EXECUTION_ORDER.md` updated: Item 5.12 inserted; former 5.11.h renumbered to 5.13 with FINAL tag.
- `STATE/DESK_QUEUE.md` updated: 4 forks banked (presenter minimum N · per-language accuracy · code-switch span accuracy · DP opt-out).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
