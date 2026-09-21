"""Observability subpackage · M13-W3 · OTel wrapper surface.

Additive-only per SO §3.8: this package exposes a `traced_call`
context-manager surface for callers to adopt at their thin-adapter
layer. It does NOT edit any sealed module (chokepoint, ledger_writer,
watch.input_seat, watch.verdict_interface). Actual OTel span emission
attaches at each caller's adapter layer at a subsequent CP.
"""
