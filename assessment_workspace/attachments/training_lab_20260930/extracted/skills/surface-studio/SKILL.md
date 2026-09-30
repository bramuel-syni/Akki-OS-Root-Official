---
name: surface-studio
description: The expert + production-manager skill for page-aware interface content in Akki's applications and workspace (layer 5, read-only over layers 1–4). Use whenever a page needs the sentences a person reads on it — Board 360, Exco 360, Registry, Watch State, Manage Rules, Model Admission, Training Run, Spend Requests, Documents, ThinkLab, Estate Intelligence — or when someone asks for the page to "explain", "summarise what changed", "show what's waiting on me", "make this page useful for the board", or to write role-aware copy for a dashboard. The expert chooses the move (interpret, report, trigger) and authors blocks by reference; the manager assembles the frozen content record per page state and role, caches it by key, and keeps every figure receipted and every silence visible. It never nudges, never decides, never states a cause without a causal receipt. Not for documents people carry away (doc-studio) or for run reporting (training-studio).
---

# surface-studio

Template: akki-skill 1.0. Self-contained; imports nothing from other skills.

## What this skill is for
Making Akki's pages helpful, insightful and prompting without inventing anything: every sentence on a page comes from the page state by reference, is fitted to the reader's role, and says what waits on them only when a mechanism says something is waiting. Freshness comes from the page state changing, not from regenerating copy.

## The six stages
1. **Brief** — `references/brief.md`. Purpose is `surface`; audience is a role from the policy; setting names the page.
2. **Model** — `page-state.json`: facts, deltas (prior → current since), pending (three kinds only: decision_pending with seat/mechanism/due; advisory with brief_ref; anomaly with watch_ref), silence (unmeasured territory), receipts (with `causal: true` where a cause is recorded), `source` (live | snapshot | stub), `unavailable_sources`. Every figure classed and receipted. Grammar in `references/model.md`.
3. **Direction** — `verdict.json`: 2–4 assemblies (lead move, order, voice, density) from `references/directions.md`; one adopted under the page's standing frame; manifest cites brief fields (role, aggregate-only) and the pending set.
4. **Specification** — `spec.json`: authored blocks with tokens (`{F003}`, `{D001.current}`, `{P001.phrasing}`, `{S001.closes_with}`); a literal number in authored text is a blocker; a trigger block names its pending item and kind; a causal marker needs a `causal_ref`; a silence block is mandatory when the page state records silence.
5. **Production** — `scripts/build.py <fixture> <build> [--prove]`. Resolve (tokens, page brief, voice, cache key) → validate → assemble (content record + preview) → freeze → qa. Figures from an unavailable source render as `[not available]` and the block is marked degraded; a wholly unavailable block degrades to silence. A stub page state produces a record with `servable: false`.
6. **Gates and delivery** — outcome set `pass | finding-not-blocking | blocked`. Delivery: `content-record.json` (frozen copy per block with classes, receipts and walk targets, keyed by cache key), `preview.html`, `build-manifest.json`. Revision: `scripts/revise.py` bumps the page-state version, re-keys the cache, detects manifest strikes (role change, aggregate-only change), rebuilds.

## The three moves, and when each leads
Page policy sets the lead move per page (`policies/page-policy.json`): interpret leads Board 360, Exco 360, Registry, ThinkLab, Estate Intelligence; report leads Watch State, Manage Rules, Training Run, Documents; trigger leads Model Admission and Spend Requests. A direction may override with a recorded reason (review item, not blocker).

## What the expert half must demonstrate
`references/capabilities.md`: role fitting, move selection, delta narration without causal drift, trigger discipline, silence surfacing, editorial economy under the role's word cap.

## Discretion
`references/discretion.md`. Permitted: block order within the adopted direction; wording within the role cap; which deltas to narrate; which receipts to walk to first. Reserved: any directive ("you should", "approve this"); any cause without a causal receipt; any trigger not backed by a pending decision, an advisory brief or a Watch record; any individual-level field on an aggregate-only page; serving a stub page state.

## Non-negotiables
- Every figure by reference, classed, with a walkable receipt. Unmeasured reads as unmeasured, never blank, never zero.
- Findings, not directives. A trigger says what is waiting and on whom; it never says what to do.
- Correlation only, unless the receipt is marked causal (WPW-5).
- Same cache key → same bytes. Copy regenerates only when the page state, role, voice, spec or policy version changes.
- Aggregate-only pages carry no individual-level field.

## Layout
```
surface-studio/
├── SKILL.md · template.json
├── references/   brief · model · directions · capabilities · discretion · reproducibility · gates
├── schemas/      page-state · brief · verdict · spec
├── policies/     page-policy.json — pages, roles, moves, trigger kinds, language rules, cache key
├── scripts/      studio (resolve) · validate · assemble (produce) · freeze · qa · build · revise
├── fixtures/     board360-rms (board, aggregate-only) · spend-requests-secops (security officer, itemised)
└── evals/        evals.json · run_evals.py
```
