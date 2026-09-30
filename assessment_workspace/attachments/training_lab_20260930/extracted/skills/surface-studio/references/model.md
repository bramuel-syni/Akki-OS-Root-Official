# Page state — the model
| Block | ID | Required | Notes |
|---|---|---|---|
| receipts | `Rnn` | resolves_to; optional `causal: true` | Ledger, Cost Ledger, Spend Requests, Watch, MOAC, census, Opportunity Brief |
| facts | `Fnnn` | label, value, unit (`pct`, `GBP`, `count`), class, receipt | |
| deltas | `Dnnn` | label, prior, current, unit, since, class, receipt | Narrated as prior → current since date; no cause unless the receipt is causal |
| pending | `Pnnn` | kind, what, receipt + kind fields | `decision_pending`: seat, mechanism, due; `advisory`: brief_ref; `anomaly`: watch_ref. Nothing else may trigger. |
| silence | `Snnn` | label, reason, closes_with, receipt | Mandatory block when present |
| source | — | live \| snapshot \| stub | stub → servable false |
| unavailable_sources | — | receipt ids | figures render `[not available]`; blocks degrade |
| aggregate_only_check | — | individual_fields_present | blocks aggregate-only pages |

## Tokens
`{F003}` fact · `{D001.prior}` `{D001.current}` `{D001.since}` · `{P001.what}` `{P001.seat}` `{P001.due}` `{P001.mechanism}` `{P001.phrasing}` · `{S001.label}` `{S001.reason}` `{S001.closes_with}`.
Classes: measured / estimated / sample / observed; a block's chips are the union of its refs' classes.
