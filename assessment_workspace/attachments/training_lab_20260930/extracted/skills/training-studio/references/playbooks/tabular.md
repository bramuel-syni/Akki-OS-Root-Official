# Playbook · Tabular prediction and forecasting

**Metric.** AUC / PR-AUC for classification (PR-AUC when positives are rare); RMSE / MAPE for regression; per-stratum where the objective names strata (region, product line).

**Baseline first.** `model.tabular.gbdt_first`: gradient-boosted trees are the baseline to beat below ~1M rows (literature-anchored, Grinsztajn et al. 2022). A neural model that does not beat it at equal effort is not adopted.

**Leakage before everything.** `data.tabular.leakage_time`: time-aware splits; target leakage audit (features computed after the label event); group leakage (same customer in train and test). A leaked number is the commonest "great result" in tabular work.

**Levers (data-limited).** Feature engineering from domain knowledge beats more rows; `data.target_label` rarely applies (labels come from the process); more history (longer window) is the "more data" lever and shifts distribution — check.

**Levers (method-limited).** Hyperparameter search on the GBDT (depth, learning rate, regularisation) with a time-aware validation; monotone constraints where the domain demands them; only then a neural model with a with-vs-without comparison.

**Priors.** b 0.2–0.5; feature-limited more often than row-limited; seed SD small (0.2–0.6 points AUC).

**Monitoring.** Feature drift (PSI per feature), calibration drift (reliability curve), performance on delayed labels. Retrain cadence: monthly or on PSI trigger. Owner: the analytics seat.

**Value.** Decisions improved × value per decision; state the counterfactual (what the current rule does) explicitly.

**Failure signatures.** AUC 0.99 → leakage until proven otherwise. Great validation, poor production → split not time-aware. Calibration off → threshold policy, not model.
