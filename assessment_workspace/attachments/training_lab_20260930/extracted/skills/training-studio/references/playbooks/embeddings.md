# Playbook · Embeddings and retrieval fine-tuning

**Metric.** Recall@k and MRR on a sealed, judged query set per stratum (`eval.embed.sealed_queries`); without judged relevance there is no evaluation. Coverage = share of queries with a result above the score threshold.

**Levers in priority order.**
1. `model.embed.hard_negatives` — the lever that moves retrieval most; mine with a cross-encoder filter to avoid false negatives.
2. Domain-adaptive pretraining on the corpus (unsupervised) when the vocabulary is far from the base's.
3. `data.target_label` — more judged pairs for the weakest query type.
4. Rank/schedule; optimizer last.

**Evaluation cautions.** Judged sets are small; MDE is large; report intervals. Never evaluate on queries used to mine negatives (leakage).

**Priors.** b 0.2–0.4; pair-limited; seed SD 0.5–1.5 points recall@10.

**Monitoring.** Query distribution drift; zero-result rate; click/feedback signals where lawful. Retrain trigger: corpus growth > 20% or zero-result rate above threshold. Owner: the memory-layer seat.

**Value.** Queries answered correctly × cost of a miss (a wrong retrieval that feeds an answer is worse than no retrieval).

**Failure signatures.** Recall up on judged set, worse in use → judged set not representative. Training loss falls, recall flat → false negatives in mining.
