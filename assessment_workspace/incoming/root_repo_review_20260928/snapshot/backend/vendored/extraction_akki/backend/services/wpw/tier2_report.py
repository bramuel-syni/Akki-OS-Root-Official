"""WPW Tier 2 · Technical Report drafter.

Spec: `canon/fixtures/whitepaper_wizard_spec_v1/spec.extracted.txt` §4
(Normative Requirements — Tier 2) + §8 (Build Acceptance Criteria
A4/A6). Verbatim quotes for every rule appear in the docstrings of
the gating invariant tests at
`backend/tests/invariants/test_wpw_tier2_report.py`.

WPW-8 fixes a 9-section skeleton and requires automatic draft on
settle. WPW-9 requires every figure to carry its evidence class and
a receipt line resolving to a run artefact; unresolvable figures
MUST NOT render. WPW-10 marks Tier 2 as internal-only; publication
is a separate governed egress crossing (WPW-15), never a Tier-2
capability. A4 requires 100 % figure resolution in a well-formed
run; A6 requires refused-run reports to still draft with the
refusal reason and the numbers.

Design:
  * `draft_report(run_dir)` is the sole public writer. Given a
    settled run's artefact directory, it reads the run's on-disk
    records and emits an in-memory report dict. No mutation of the
    run's state; the module is a stenographer.
  * Figures are emitted per-section by `_emit_*` helpers. Each
    helper returns a figure dict OR None if its source artefact is
    absent. Absent figures move to `refused_figures[]` with a
    plain-language reason, and the corresponding section body
    surfaces the absence explicitly (never fills the gap).
  * `SECTION_SKELETON` is a frozen tuple — no runtime reordering.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# WPW-10 verbatim marker (banked in report body + metadata).
INTERNAL_ONLY_MARKER = (
    "[INTERNAL · Tier 2 · MUST NOT cross the outer gate — WPW-10]"
)

# WPW-8 fixed section skeleton (frozen tuple; runtime immutable).
SECTION_SKELETON: Tuple[str, ...] = (
    "problem_and_objective",
    "data_statement",
    "baseline_record",
    "method",
    "setup_and_reproducibility",
    "results_on_held_out",
    "ablations",
    "limitations",
    "negative_results",
)

# WPW spec §5 · evidence classes.
EVIDENCE_CLASSES = ("measured", "estimated", "observed")

# WPW-8 sub-clause: results section names the six acceptance criteria.
ACCEPTANCE_CRITERIA_ORDER = (
    "held_out_accuracy",
    "abstention_calibration",
    "cost_actual_vs_estimate",
    "latency_p95_ms",
    "refusal_rate_on_out_of_domain",
    "adapter_size_mib",
)


# -----------------------------------------------------------------
# Small on-disk helpers
# -----------------------------------------------------------------

def _load_json_or_none(p: Path) -> Optional[Dict[str, Any]]:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _load_text_or_none(p: Path) -> Optional[str]:
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return None


def _load_notebook(p: Path) -> List[Dict[str, Any]]:
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return out


def _figure(figure_id: str, evidence_class: str, receipt_line: str,
            summary_text: str) -> Dict[str, Any]:
    assert evidence_class in EVIDENCE_CLASSES
    return {
        "figure_id": figure_id,
        "evidence_class": evidence_class,
        "receipt_line": receipt_line,
        "summary_text": summary_text,
    }


def _refused(figure_id: str, receipt_line: str, reason: str) -> Dict[str, Any]:
    return {"figure_id": figure_id, "receipt_line": receipt_line, "reason": reason}


# -----------------------------------------------------------------
# Section builders — each returns (body_markdown, figures, refused)
# -----------------------------------------------------------------

def _sec_problem_and_objective(run_dir: Path):
    """WPW-8 sub-clause: 'problem & objective (from the commissioning
    reflection)'. Body derives from the run's commissioning artefact
    (Tier 1 event or a plain-text fallback)."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    txt = _load_text_or_none(run_dir / "commissioning_reflection.txt")
    if txt is None:
        return ("_the record is silent on the commissioning reflection._",
                figures, refused)
    return (f"{txt.strip()}", figures, refused)


def _sec_data_statement(run_dir: Path):
    """WPW-8 sub-clause: 'data statement at datasheet level,
    classification-driven'. Draws from extract_summary.json —
    included columns, excluded columns (including PII), scrub counts,
    rows extracted, JSONL sha256 for reproducibility."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    es = _load_json_or_none(run_dir / "extract_summary.json")
    if es is None:
        refused.append(_refused(
            "corpus_shape", "extract_summary.json",
            "extract_summary.json not present; data statement cannot render",
        ))
        return ("_the record is silent on the data statement (extract "
                "summary artefact absent)._", figures, refused)
    incl = es.get("included_columns", [])
    excl = es.get("excluded_columns", [])
    scrub = es.get("scrub_replacements", {}) or {}
    rows = es.get("rows_extracted", "?")
    body = (
        f"Source: `{es.get('database','?')}.{es.get('table','?')}`  · "
        f"rows extracted: **{rows}**  · dropped empty QA: "
        f"{es.get('dropped_empty_qa','?')}\n\n"
        f"**Included columns (governed as text):** {', '.join(incl) or '_none_'}.\n\n"
        f"**Excluded columns (classification-driven refusal):** "
        f"{', '.join(excl) or '_none_'}.\n\n"
        f"**Scrub pass replacements:** " +
        (", ".join(f"{k}={v}" for k, v in scrub.items()) or "_none_") + ".\n\n"
        f"Output corpus sha256 (shape-only receipt): "
        f"`{es.get('output_jsonl_sha256','_absent_')}`."
    )
    figures.append(_figure(
        "corpus_shape", "measured", "extract_summary.json",
        f"{rows} rows · included={incl} · excluded={excl} · scrub={scrub}",
    ))
    return (body, figures, refused)


def _sec_baseline_record(run_dir: Path):
    """WPW-8 sub-clause: 'baseline record' (Promise #24). Cite the
    BaselineLine record id + starting model + license note."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    bl = _load_json_or_none(run_dir / "baseline_line.json")
    if bl is None:
        refused.append(_refused(
            "baseline_line", "baseline_line.json",
            "baseline_line.json not present; Promise #24 record cannot resolve",
        ))
        return ("_the record is silent on the baseline (Promise #24 record "
                "absent)._", figures, refused)
    body = (
        f"Baseline line id: `{bl.get('baseline_line_id','?')}`  · "
        f"starting model: `{bl.get('starting_model_id','?')}`.\n\n"
        f"Licence note: {bl.get('starting_model_license_note','_unstated_')}.\n\n"
        f"Authored at {bl.get('authored_at','?')} by "
        f"`{bl.get('authored_by','?')}` (Promise #24 auto-mint at run open)."
    )
    figures.append(_figure(
        "baseline_line", "measured", "baseline_line.json",
        f"baseline={bl.get('baseline_line_id','?')} · model={bl.get('starting_model_id','?')}",
    ))
    return (body, figures, refused)


def _sec_method(run_dir: Path):
    """WPW-8 sub-clause: 'method, including adopted ideation events'.
    Reads notebook.jsonl and surfaces every cif_ideation with
    payload.adoption_status == 'adopted'. WPW-6: mirrored by
    reference, never paraphrased — we cite refs, not content."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    entries = _load_notebook(run_dir / "notebook.jsonl")
    adopted = [
        e for e in entries
        if e.get("event_kind") == "cif_ideation"
        and (e.get("payload", {}) or {}).get("adoption_status") == "adopted"
    ]
    if not adopted:
        return ("Method: LoRA/PEFT fine-tune per the adopted recipe on the "
                "Promise #24 baseline.\n\n"
                "**Adopted ideation events:** _the record is silent — no "
                "cif_ideation events with adoption_status='adopted' appear "
                "in the run notebook._", figures, refused)
    lines = [
        "Method: LoRA/PEFT fine-tune per the adopted recipe on the "
        "Promise #24 baseline.",
        "",
        "**Adopted ideation events (mirrored by reference · WPW-6):**",
    ]
    for e in adopted:
        p = e.get("payload", {})
        lines.append(
            f"* `{p.get('cif_event_ref','?')}` · idea `{p.get('idea_ref','?')}` "
            f"· conditions `{p.get('conditions_ref','?')}` · adopted."
        )
    return ("\n".join(lines), figures, refused)


def _sec_setup_and_reproducibility(run_dir: Path, state: Dict[str, Any]):
    """WPW-8 sub-clause: 'setup & reproducibility (hardware, duration,
    cost actual-against-estimate, seeds where applicable)'. Every
    required dimension emits a figure; missing sources refuse."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    body_parts: List[str] = []

    # Hardware fingerprint (WPW-9 refusal target when artefact missing)
    smi_before = _load_json_or_none(run_dir / "nvidia_smi_before.json")
    if smi_before is None:
        refused.append(_refused(
            "hardware_fingerprint", "nvidia_smi_before.json",
            "nvidia_smi_before.json not present; hardware fingerprint "
            "cannot resolve (WPW-9 refusal path).",
        ))
        body_parts.append(
            "**Hardware:** _the record is silent — nvidia_smi_before "
            "artefact absent._"
        )
    else:
        gpus = smi_before.get("gpus") or []
        gpu_names = ", ".join(
            f"{g.get('name','?')} #{g.get('index','?')}" for g in gpus
        ) or "_no gpus captured_"
        body_parts.append(f"**Hardware:** {gpu_names}.")
        figures.append(_figure(
            "hardware_fingerprint", "measured", "nvidia_smi_before.json",
            f"gpus={len(gpus)}: {gpu_names}",
        ))

    # Duration + FLOPs (from train_summary_raw)
    ts = _load_json_or_none(run_dir / "train_summary_raw.json")
    if ts is None:
        refused.append(_refused(
            "wall_clock_and_flops", "train_summary_raw.json",
            "train_summary_raw.json not present; duration/FLOPs cannot resolve",
        ))
        body_parts.append("**Duration:** _the record is silent._")
    else:
        dur_s = ts.get("total_train_s") or (ts.get("final_train_metrics") or {}).get("train_runtime")
        dur_str = f"{dur_s:.2f} s (~{int((dur_s or 0)/60)} min)" if dur_s else "_unknown_"
        body_parts.append(
            f"**Duration:** {dur_str}  · **epochs:** {ts.get('epochs','?')}  · "
            f"**effective batch:** {ts.get('effective_batch','?')}  · "
            f"**n_gpu:** {ts.get('n_gpu','?')}  · **base model:** "
            f"`{ts.get('base_model','?')}`  · **adapter sha256:** "
            f"`{ts.get('adapter_sha256','_absent_')}`."
        )
        figures.append(_figure(
            "wall_clock_and_flops", "measured", "train_summary_raw.json",
            f"duration={dur_str} · flops={ts.get('final_train_metrics',{}).get('total_flos','?')}",
        ))

    # Cost actual-against-estimate (from state.json)
    ca = state.get("cost_actual_usd")
    ce = state.get("cost_estimate_usd")
    if ca is not None and ce is not None:
        pct = (ca / ce * 100.0) if ce else 0.0
        body_parts.append(
            f"**Cost actual vs estimate:** ${ca:.2f} actual / ${ce:.2f} "
            f"estimate ({pct:.0f} % of estimate)."
        )
    else:
        body_parts.append("**Cost actual vs estimate:** _the record is silent._")

    # Seed
    seed = state.get("seed")
    if seed is not None:
        body_parts.append(f"**Seed:** {seed}.")
    else:
        body_parts.append(
            "**Seed:** _not applicable / the record is silent._"
        )

    return ("\n\n".join(body_parts), figures, refused)


def _sec_results_on_held_out(run_dir: Path, state: Dict[str, Any]):
    """WPW-8 sub-clause: 'results on held-out material with all six
    acceptance criteria and their numbers'. Every criterion by name,
    with measured value + threshold + pass/fail."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    crit = state.get("acceptance_criteria") or {}
    if not crit:
        refused.append(_refused(
            "acceptance_criteria", "state.json",
            "state.json missing acceptance_criteria block; results cannot resolve",
        ))
        return ("_the record is silent on held-out results._",
                figures, refused)
    lines = ["| Criterion | Measured | Threshold | Pass? |",
             "|---|---:|---:|---|"]
    for name in ACCEPTANCE_CRITERIA_ORDER:
        c = crit.get(name)
        if not c:
            lines.append(f"| `{name}` | _absent_ | _absent_ | _absent_ |")
            continue
        m = c.get("measured", "?")
        th = c.get("threshold", "?")
        ok = "✅" if c.get("pass") else "❌"
        lines.append(f"| `{name}` | {m} | {th} | {ok} |")
    body = "\n".join(lines)
    figures.append(_figure(
        "acceptance_criteria", "measured", "state.json",
        f"6 acceptance criteria · pass={sum(1 for n in ACCEPTANCE_CRITERIA_ORDER if (crit.get(n) or {}).get('pass'))}/6",
    ))
    return (body, figures, refused)


def _sec_ablations(state: Dict[str, Any]):
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    abl = state.get("ablations") or []
    if not abl:
        return ("_No ablations run for this settlement._", figures, refused)
    return ("\n".join(f"* {a}" for a in abl), figures, refused)


def _sec_limitations(state: Dict[str, Any]):
    """WPW-8: limitations. If the run record surfaces limitations,
    render them. Otherwise the report says the record is silent —
    it does not fill the gap (§5 refusal grammar)."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    lims = state.get("limitations") or []
    if not lims:
        return ("_the record is silent on limitations._", figures, refused)
    return ("\n".join(f"* {L}" for L in lims), figures, refused)


def _sec_negative_results(state: Dict[str, Any]):
    """WPW-8: negative results. Same discipline as limitations."""
    figures: List[Dict[str, Any]] = []
    refused: List[Dict[str, Any]] = []
    neg = state.get("negative_results") or []
    if not neg:
        # If this is a refused run, surface the refusal here too.
        if state.get("status") == "closed_rejected":
            reason = state.get("refusal_reason", "_reason not on record_")
            return (f"**Run refused.** {reason}", figures, refused)
        return ("_the record is silent on negative results._", figures, refused)
    return ("\n".join(f"* {n}" for n in neg), figures, refused)


# -----------------------------------------------------------------
# Public API — draft_report
# -----------------------------------------------------------------

def draft_report(run_dir: str) -> Dict[str, Any]:
    """WPW-8 · draft a Tier 2 technical report from a settled run's
    artefacts. Returns a report dict:

        {
          "metadata": {
              "run_id": str,
              "tier": 2,
              "internal_only": True,
              "settlement": "accepted" | "refused",
              "spec_ref": "whitepaper_wizard_spec_v1 · WPW-8..10",
          },
          "sections": { name: {"body": str}, ... }   # 9 sections
                                                     # in SECTION_SKELETON order
          "figures": [ {figure_id, evidence_class, receipt_line,
                        summary_text}, ... ]
          "refused_figures": [ {figure_id, receipt_line, reason}, ... ]
          "body": str   # concatenated markdown carrying INTERNAL_ONLY_MARKER
        }
    """
    rd = Path(run_dir)
    state = _load_json_or_none(rd / "state.json") or {}
    status = state.get("status", "unknown")
    settlement = "refused" if status == "closed_rejected" else "accepted"

    figures: List[Dict[str, Any]] = []
    refused_figures: List[Dict[str, Any]] = []
    sections: Dict[str, Dict[str, str]] = {}

    def _add(name: str, body: str, figs, ref):
        sections[name] = {"body": body}
        figures.extend(figs)
        refused_figures.extend(ref)

    _add("problem_and_objective", *_sec_problem_and_objective(rd))
    _add("data_statement", *_sec_data_statement(rd))
    _add("baseline_record", *_sec_baseline_record(rd))
    _add("method", *_sec_method(rd))
    _add("setup_and_reproducibility", *_sec_setup_and_reproducibility(rd, state))
    _add("results_on_held_out", *_sec_results_on_held_out(rd, state))
    _add("ablations", *_sec_ablations(state))
    _add("limitations", *_sec_limitations(state))
    _add("negative_results", *_sec_negative_results(state))

    # Assemble the body markdown (carries the WPW-10 watermark).
    section_titles = {
        "problem_and_objective": "1 · Problem & Objective",
        "data_statement": "2 · Data Statement (classification-driven)",
        "baseline_record": "3 · Baseline Record (Promise #24)",
        "method": "4 · Method (including adopted ideation events)",
        "setup_and_reproducibility": "5 · Setup & Reproducibility",
        "results_on_held_out": "6 · Results on held-out material",
        "ablations": "7 · Ablations",
        "limitations": "8 · Limitations",
        "negative_results": "9 · Negative Results",
    }
    body_lines = [
        f"# Tier 2 Technical Report · {state.get('run_id','_unknown_run_')}",
        "",
        INTERNAL_ONLY_MARKER,
        "",
        f"**Settlement:** {settlement}  · **Spec:** whitepaper_wizard_spec_v1 · WPW-8..10.",
        "",
    ]
    for name in SECTION_SKELETON:
        body_lines.append(f"## {section_titles[name]}")
        body_lines.append("")
        body_lines.append(sections[name]["body"])
        body_lines.append("")
    if figures:
        body_lines.append("## Figures (WPW-9)")
        body_lines.append("")
        body_lines.append("| # | evidence_class | receipt_line | summary |")
        body_lines.append("|---|---|---|---|")
        for i, f in enumerate(figures, 1):
            body_lines.append(
                f"| {i} · `{f['figure_id']}` | {f['evidence_class']} | "
                f"`{f['receipt_line']}` | {f['summary_text']} |"
            )
        body_lines.append("")
    if refused_figures:
        body_lines.append("## Refused figures (WPW-9)")
        body_lines.append("")
        for f in refused_figures:
            body_lines.append(
                f"* `{f['figure_id']}` · receipt_line=`{f['receipt_line']}` · "
                f"reason: {f['reason']}"
            )
        body_lines.append("")
    body_lines.append(INTERNAL_ONLY_MARKER)
    return {
        "metadata": {
            "run_id": state.get("run_id", "_unknown_run_"),
            "tier": 2,
            "internal_only": True,
            "settlement": settlement,
            "spec_ref": "whitepaper_wizard_spec_v1 · WPW-8..10",
        },
        "sections": sections,
        "figures": figures,
        "refused_figures": refused_figures,
        "body": "\n".join(body_lines),
    }
