"""services.shield_train — governed masking pipeline for row-bearing
training runs (W-Shield-Train).

Charter (owner directive 2026-09-06T~11:20Z, verbatim):
  "W-Shield-Train BUILD PHASE. ... Definition of done: pipeline fully
   built and fixture-proven, RED receipts banked, double-green from
   floor 2786, admission request drafted. If TxtTrain-v2's go lands
   mid-wave, note that v2 should RUN THROUGH this new pipeline if it's
   close to done — coordinate the timing at a clean boundary rather
   than running v2 on the old ad-hoc path while the governed one is
   nearly ready."

Modules:
  * `authoring`     — masking-policy authoring surface (Doc 02 §A5.2)
  * `row_executor`  — row-bearing SQL executor through the chokepoint
  * `pipeline`      — masked-file transport + cleanup + governed LoRA run
"""
from . import authoring, row_executor, pipeline

__all__ = ["authoring", "row_executor", "pipeline"]
