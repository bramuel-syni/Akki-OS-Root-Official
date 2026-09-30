# Playbook · ASR and spoken-register adaptation

**Metric.** Report WER and CER (CER for agglutinative languages such as Kiswahili, where a single morpheme error is a whole-word error in WER). "Accuracy" on the objective is 1 − WER unless the owner says otherwise. Coverage = share of utterances the model returns with confidence above the serving threshold.

**Error typing before any lever.** Substitution / insertion / deletion, then by cause: acoustic (noise, rate, mic), lexical (out-of-vocabulary register terms, Sheng, named entities), switch-point (errors clustered at code-switch boundaries), segmentation. The lever depends on which dominates; run the typing on the calibration errors per stratum.

**Levers in priority order (data-limited stratum).**
1. `aug.audio.speed_perturb` then `aug.audio.specaugment` — free data, literature-anchored effect, admissible (inherits lawful basis).
2. `data.target_label` on the sub-stratum the error typing exposed (a dialect region, one call-centre line).
3. More data — last, because it costs rights and time.

**Levers (method-limited / lexical).** `model.audio.lm_bias` with a register text corpus (Sheng lexicon, entity list) before touching the acoustic recipe; then `model.lora.rank` (raise rank / add encoder modules) and `model.schedule`; the optimizer comparison last.

**Levers (distribution-shifted).** `aug.audio.noise_rir` when production is a hall or phone line and calibration material is desk-mic; `data.restratify` if the real axis is capture condition, not register.

**Code-switched speech.** Treat switch-point errors as their own error type. Levers: LM bias with switch-aware text; targeted labelling of switch-heavy utterances; do not expect speed perturbation to help.

**Recipe defaults (Whisper-tiny class, CI fixture).** LoRA rank 8–16 on attention q/v and fc1; lr 1e-4–3e-4; warmup 5%; 2–3 epochs at calibration volumes. Class practice-anchored. Production base model is named after census (A17.11); do not tune for the fixture.

**Priors.** Exponent b 0.15–0.35; 150–400 examples per accuracy point from a 0.6–0.8 baseline; seed SD 0.4–1.0 points. Lexically driven registers sit at the low end of b: more audio helps less than a lexicon.

**Monitoring (industry lens).** Per stratum: coverage rate and confidence distribution weekly; register-classifier drift on incoming calls; retrain trigger = coverage below floor two weeks running or register mix shift > 10 points. Owner: the answering-service seat.

**Value (entrepreneur lens).** Calls served per point of coverage; the stratum with the largest unserved volume pays first, not the one with the largest gap.

**Known failure signatures.** Gain on small stratum with regression on large → augmentation mismatch. Insertions rising → LM bias too strong. Held-out far above train → leakage (dedup against the sealed set). Coverage up, accuracy down → confidence threshold moved, not the model.
