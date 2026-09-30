# Brief — six dimensions for a surface commission
| Dimension | What it decides | Field |
|---|---|---|
| Purpose | Always `surface`; the statement names the page and what a reader should leave knowing | `purpose` |
| Audience | The role (board, exco, security_officer, operator, depot_lead) → voice, priorities, word cap | `audience.role`, `audience.priorities` |
| Setting | The page (→ lead move, aggregate-only, max blocks), device, unattended or live | `setting.page`, `setting.device` |
| Content | Which record kinds are present: records, deltas, pending, advisories | `content` |
| Brand/tone | House voice; expressiveness is always restrained on a page | `brand` |
| Outputs | content-record, preview-html | `outputs` |
| Constraints | aggregate_only, max_blocks | `constraints` |
A role change or an aggregate-only change strikes the manifest; the page state changing does not (it re-keys the cache).
