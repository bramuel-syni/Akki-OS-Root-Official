# Playbook · Text classification, NER and LLM instruction fine-tuning

**Metric.** Classification: macro-F1 (small classes count), coverage above threshold. NER: entity-level F1 per type. LLM fine-tune: task metric on the sealed set plus a held-out win-rate against the base with a fixed judge protocol (EP-4 dual-judge before terminal test).

**Contamination first.** `model.text.contamination_check`: n-gram overlap between training text and the sealed set; blocker above threshold. LLM pretraining contamination is unknowable for closed bases; say so.

**Levers in priority order (classification, data-limited).**
1. Better labels over more labels: `data.clean.confident_learning` if agreement is below floor.
2. `data.target_label` on the confusable classes.
3. Class reweighting for macro-F1.
4. More data.

**Levers (LLM instruction fine-tune).** `data.text.instruction_quality`: 1k curated examples routinely beat 50k noisy (LIMA-class finding, literature-anchored); curate before scaling. Then `model.lora.rank` (16–64 on a 7B class) and `model.schedule`; optimizer last. Keep a with-vs-without-curation comparison as the recipe-seat comparison when the cause is label-noise-limited.

**Evaluation.** Judged evaluations need a fixed rubric, two judges, agreement reported; a single LLM judge is a single annotator. Bootstrap intervals over test items; MDE per class.

**Recipe defaults (7B class).** LoRA rank 16–64; lr 1e-4–2e-4; warmup 3%; 2–3 epochs; practice-anchored.

**Priors.** Classification b 0.25–0.5, 30–120 examples per macro-F1 point; LLM fine-tune quality-dominated, seed SD 1–3 points (higher than classification: say "single-seed" loudly).

**Monitoring.** Class distribution drift on inputs; refusal and low-confidence rates; for LLMs, a weekly judged sample against the sealed rubric. Retrain trigger: input distribution shift or a rubric change. Owner: the answering-service or extraction seat as applicable.

**Value.** Documents routed correctly × cost of a misroute; for LLM fine-tunes, minutes saved per interaction × volume; be explicit when the value is a hypothesis.

**Failure signatures.** Macro-F1 up, accuracy down → reweighting overshot. LLM win-rate up, task metric flat → judge preference, not capability. Held-out far above train → contamination.
