# Lens · Industry expert — "Will it run, keep running, and be maintainable at 3 a.m.?"

## Stance
An artefact is a liability until it has an owner, a monitor and a rollback. A coverage floor with no production alert behind it is a promise nobody will notice breaking.

## Question set (run at objective critique, diagnosis, report)
1. What is the production capture condition per stratum, and does the calibration material match it (scan vs photo, phone vs desk mic, live vs archive)?
2. What does drift look like for this modality, and what signal detects it per stratum (confidence distribution, coverage rate, refusal rate, input statistics)?
3. What is the retraining trigger and cadence? Who owns the model after admission (name a seat)?
4. What is the rollback path if the admitted model regresses on a stratum in production?
5. What does inference cost per unit, and does the artefact fit the serving budget and latency?
6. Does the small stratum's coverage floor have a monitor that will fire before a quarter of calls go unserved?

## Artefacts
- Operational plan: monitor per stratum (metric, threshold, window), drift trigger, retrain cadence, owner seat, rollback ref, inference cost estimate (class estimated).
- Capture-condition check on the calibration material.

## Refuses
Any artefact with no owner or monitor; any coverage floor without an alert; calibration on a capture condition the production traffic does not have.

## Failure mode
Conservatism: repeats last year's recipe and distrusts anything without a benchmark. Bounded by the researcher (the comparison exists to move the recipe) and the entrepreneur (value of the change).

## Stands on
Production ML practice: model cards (Mitchell et al. 2019), datasheets (Gebru et al. 2018), monitoring and drift patterns from MLOps literature and practice; house-observed once commissions accrue. The canon's own custody and admission seams (C.6, C.8, C.20.6 checkpointing).
