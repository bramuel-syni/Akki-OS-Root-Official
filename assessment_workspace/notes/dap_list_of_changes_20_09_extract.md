# DAP List of Changes · 20 Sep 2026 · citation extract

**Source manifest**: `phase0/credential_drop_manifests/20260920T1140Z_owner_drops_manifest.json` (drop_id `20260920T1140Z`)
**Custody**: `custody/owner_drops/20260920T1140Z/DAP_List_of_Changes_20260920.docx` (sha256 `4eabe4d55d795dba147ce4b77d645aa3ec5d95cb24c17e36c678bed6bc38a826` · 16,645 bytes)
**Role**: change-log companion · design-side delta since prior banked prototype
**Citation form**: `DAP List of Changes 20.09 · <section-header>`

## Row inventory (bullet-list · verbatim descriptions)

| # | Section/area | Description verbatim |
|---|---|---|
| 1 | Data Estate Module | `[ Build a skill on it ]` and `[ Download the raw data ]` CTA buttons on What You Can Do With It Section |
| 2 | Data Estate Module | Fixed the navigation such that when the CTA is clicked it opens the respective page at the top |
| 3 | Extract Module | Moved How It Works to be above Assistance and made the section collapsible |
| 4 | Extract Module | Added the persistent marker "Assistance" on the chat compose area at the footer to tie it to the assistance section on the middle of the page |
| 5 | Extract Module | Moved `[Start another request]` button to the rail and always visible |
| 6 | Rail | On the rail created By status section that changes per Extraction type eg. Get Intelligence showing count of requests per status |
| 7 | Request Status Cards and Drawers | Request → In Approval (sign off by data owner where applicable) → Executing → Ready → Retrieved. A request can also be blocked, refused and Expired as per DAP specs |
| 8 | In Approval Card and Drawer | Designed and created the In Approval Card and Drawer |
| 9 | Executing Card and Drawer | Designed and created the Executing Card and Drawer — when request has been approved and the requesting is been carried out by the system |
| 10 | Ready Card | Designed and created the Ready Card — when execution has been concluded successful |
| 11 | Retrieved Card | Designed and created the Retrieved Card. Here models and raw data are sent to the requester environment that is provided during onboarding |
| 12 | Refused Card and Drawer | Designed and created the Refused Card and Drawer |
| 13 | Blocked Card and Drawer | Designed and created the Blocked Card and Drawer |
| 14 | Expired Card and Drawer | Designed and created the Expired Card and Drawer |
| 15 | Toast Notifications | Incorporated toast notifications |
| 16 | Email Notifications | Incorporated email notifications to Requester accounts |
| 17 | Request Assistance History (Drawers) | Incorporated assistant history in drawers where assistance was used to formulate the request |

## Touch surface index (backend-relevant)

- **Rows 7–14**: Request lifecycle states + card/drawer set — matches journey doc §11 and rail §9 (8 stat cards + Total aggregate). Backend contract: state machine `Compose→Submitted→Routing→In Approval→Executing→Ready→Retrieved`; terminals `Refused/Blocked/Expired`.
- **Row 15**: Toast notifications — event-emission surface at submission + retrieval per journey L48, L225, L397.
- **Row 16**: Email notifications to Requester accounts — **CONFLICT-FLAG**: journey doc treats email as `deliberately_deferred` per drop manifest ("Org-admin status emails — submitter-only remains the current rule per owner directive verbatim · product decision · nothing blocked"). Bank as DEFAULT-class stub behind flag OFF pending owner ratification of email surface granularity.
- **Row 17**: Assistant history in drawers — surfaces new drawer content (assistant conversation binding). Not lifecycle-state-changing; deferred to specialist wave.

## Absence findings vs. journey doc

- **DAP-15 14-day timer**: NOT explicitly cited in the changelog. Journey doc L27/L219 is the binding source.
- **Blocked kinds (request / check / estate)**: changelog says "blocked" flat; journey doc L30/L201 defines 3 kinds.
- **Approver identity discipline**: changelog says "sign off by data owner where applicable"; journey doc L25/L212 forbids approver-name surface to party.
- **Retry, standing approval, partial release, spend ceiling, suspension-from-Ready, wait-line, non-gate fault, destination removal**: changelog does NOT touch any of these — consistent with DAP-LIFECYCLE-Q1..Q8 being open.

## Standing bounds preserved

Additive-only per SO §3.8 · citation-only note · does not itself bind any behaviour.
