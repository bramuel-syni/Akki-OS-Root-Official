# Direction library — assemblies the expert chooses from

A direction is one item from each axis. The model chooses the assembly for the brief; it does not invent items. Each item carries a worked example and a failure example; the worked examples are the two fixtures, produced by this pipeline.

## Axis 1 · Stage plan
| Item | Use when | Worked example | Failure example |
|---|---|---|---|
| calibration-3-volumes-then-full | Default. Calibration is mandatory (A17.20); three volumes fit a log-linear curve per stratum | Both fixtures: 250/500/1000 per stratum, curve, quote, full stage conditional on the Owner verdict | Skipping calibration and quoting the full run from the baseline alone: a point estimate with no curve behind it (A17.20 forbids) |
| four-independent-calibrations | A uniform adapter has already shown a split result: large strata clear, small strata fail | Deferred in both fixtures with a re-entry condition | Choosing it first: quadruples admission cost (four artefacts through C.6) with no evidence the split exists |
| pseudo-label-then-calibrate | Never in the current canon: pseudo-labelled examples have no receipt and no lawful basis of their own | — | Rejected in asr-register-adapter (T3): the manifest requirement cannot be met |
| warm-start-from-prior-adapter | Same modality, same task family, lineage recorded (A17.3) | — | Rejected in dairy-record-classifier (T4): audio adapter into a document task; no lineage argument survives |

## Axis 2 · Sampling
| Item | Use when | Worked | Failure |
|---|---|---|---|
| proportional-to-share-with-small-stratum-floor | Default when share is skewed; the floor (policy.calibration.small_stratum_floor_examples) keeps the small strata's curves fittable | Both fixtures | Pure proportional sampling gives a 9%-share stratum 22 examples at the first volume; the curve is noise |
| per-stratum | With four-independent-calibrations only | — | Per-stratum sampling under a uniform adapter double-counts small strata and hides the regression on the large ones |
| uniform | Strata of similar size and similar gap | — | Uniform sampling with a 52/10 share split over-trains the large stratum relative to its gap |
| augmented | Only with material that carries its own lawful basis (augmentation of admitted examples is admissible; synthesis is not) | — | Augmentation used to manufacture a "reachable" verdict on a stratum whose real material is short |

## Axis 3 · Comparison
| Item | Use when | Worked | Failure |
|---|---|---|---|
| two-arm-optimizer-on-smallest-valid-stratum | Default; exactly one comparison fills the recipe seat (A17.5); identical data/base/eval/cap | Both fixtures; note dairy-record-classifier picks ST3 because ST4's test set is below the validity floor | Running the comparison on the largest stratum because "it's more stable": violates A17.5 and hides the small-stratum behaviour the recipe must serve |
| two-arm-with-vs-without-X | Testing one recipe component (a scheduler, an adapter rank) after the optimizer is settled | — | Testing two components in one comparison; the delta cannot be attributed |
| none | A recorded Owner verdict already fills the recipe seat for this task family and modality | — | "None" because the last run's numbers looked fine: an unevidenced revision is a defect (A17.4) |

## Axis 4 · Evaluation
| Item | Use when | Worked | Failure |
|---|---|---|---|
| sealed-test-set-per-stratum | Always; uncurated held-out (#22) | Both fixtures | Evaluating on a curated subset "because the raw set has bad audio": the floor is the floor |
| sealed-plus-counterfactual-path | When a novelty claim will be made (WPW-12 needs a measured delta against the counterfactual) | — | Claiming a methods contribution with no counterfactual arm |

## Choosing between candidates
Two to four candidates for a new task family or modality; one candidate under the standing frame for a routine re-run. Reject on lawful basis, lineage or evaluation validity before anything else. Defer with a named re-entry condition rather than reject when the only objection is "not yet evidenced".
