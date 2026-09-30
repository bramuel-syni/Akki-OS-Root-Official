# Playbook · Document image classification and extraction

**Metric.** Accuracy and per-class recall (the small form type's recall is the number that matters); coverage = share classified above threshold. For extraction: field-level F1.

**Hidden axes.** Capture condition (scan vs photo), device, skew, lighting. Re-stratify if per-capture breakdown diverges from per-form-type (`data.restratify`); otherwise a "form-type" objective is really a "photo" objective.

**Levers in priority order (data-limited small class).**
1. `data.class_imbalance` (balanced sampling or loss reweighting) — free.
2. `aug.image.geometric_photometric` — free; keep ranges within production capture.
3. `data.target_label` on the confusable pair (breeding record vs vet visit).
4. More images — last.

**Levers (method-limited).** `model.document.layout_vs_ocrfree`: if form types differ by layout, a layout-aware model; if photos are noisy, OCR-free (Donut-class) avoids OCR error propagation. Then `model.lora.rank`, `model.schedule`, optimizer last.

**Labels.** One annotator with a 10% second-annotator audit; agreement floor 0.80; `data.clean.confident_learning` if below. Fields under a PII ruling (the occupation boolean, R07) are never transcribed; the collection schema says so.

**Recipe defaults (document-encoder class).** LoRA rank 8–32; lr 5e-5–2e-4; warmup 5%; input long edge ≥ 1200 px. Practice-anchored.

**Priors.** b 0.25–0.5; 40–150 examples per accuracy point from 0.6–0.9; seed SD 0.3–0.8 points. Document classification is usually cheaper per point than ASR.

**Monitoring.** Per form type: recall on a weekly audited sample; capture-condition mix; refusal rate. Retrain trigger: a new form version in the field (census signal) or recall below floor on the audit sample. Owner: the census classification seat.

**Value.** Forms auto-classified × downstream cost per manual classification; the high-volume form type usually pays first even at a small gap.

**Failure signatures.** Scan recall drops when photo augmentation added → ranges too wide. Confusion concentrated on one pair → targeted labelling, not more data. Accuracy high, coverage low → threshold, not model.
