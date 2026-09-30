# Creative direction — the CIF stage

Creativity enters the studio in exactly one place: the choice of direction
for a commission. That choice is a CIF verdict: candidate ideas, a verdict
against a stated goal, a manifest of the load-bearing assumptions, and a
confirmer. Everything below it is curated and rule-driven.

## The verdict record (`verdict.json`)

| Field | Meaning |
|---|---|
| `goal` | What the direction must achieve, in the brief's terms |
| `frame_ref` | The standing frame this commission runs under (e.g. `FR-strategy-decide-v1`). A confirmed frame covers many verdicts, so routine classes do not need the coach on every commission. |
| `candidates[]` | 2–4 directions. Each has an `assembly` (narrative, compositions, treatment, density, imagery) drawn from the libraries in `taxonomy.md`, and a `verdict`: adopt / reject / rank / defer. Deferred and rejected directions keep their `conditions` or `rationale`; they persist and re-enter when conditions arrive. |
| `adopted` | The idea_id with verdict adopt |
| `manifest[]` | The assumptions the adopted direction depends on. Each: `assumption`, `class` (fact / recalled / inferred, by the counterfactual probe: what, if false, flips this?), `source` (the brief field it rests on), `flips` (the design decisions that would have to be re-verdicted). |
| `confirmed_by`, `confirmed_at` | The coach seat. Required. |

## Bounds

1. Direction-level only. Three to six verdicts per commission. Per-slide
   choices come from the voice and the seed; they do not get manifests.
2. Routine work runs under a frame. A new frame, a novel brief, or a strike
   reaches the coach; ordinary commissions do not.
3. The adopted verdict and manifest are part of the frozen specification. A
   rebuild reads them. It never re-ideates.

## Strikes and flips

`scripts/revise.py` compares each change to the manifest sources. A change to
a brief field a manifest entry names is a strike: the report lists the
manifest entry and its flips, and marks release *blocked pending re-verdict*.
Content changes (a new capex figure) are not strikes; they flow through the
references and the design holds by construction. This is the revision policy:
"update the assumptions and preserve the design" is guaranteed when nothing
in the manifest is touched, and explicitly re-decided when something is.

## Previewing for major commissions

Show three pages, not three covers: the cover, the densest analytical page,
and one diagram or table page. Covers are the easiest page to make look good
and reveal nothing about how the direction handles hard content. Record the
pick in the verdict; that is the choice made once and then frozen.

## Corrections retire the class

When the coach corrects a design outcome ("never that serif with that
accent", "too dense for a board"), the correction becomes a `veto` entry or a
structural limit in the voice, so the error class cannot recur. Corrections
are the only way compatibility rules are authored.
