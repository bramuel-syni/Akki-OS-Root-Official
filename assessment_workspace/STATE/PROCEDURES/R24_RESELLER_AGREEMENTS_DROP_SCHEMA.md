# R-24 · Reseller Agreements · Well-Formed Drop Schema

**Status:** OPEN · counsel brief on owner's desk · schema registered now so the eventual drop validates first-time.

**Owner disposition verbatim (2026-09-20T~21:24Z · this-session non-interrupting note):**

> "R-24 reseller agreements — register the WELL-FORMED DROP SCHEMA so the eventual drop validates first time. Required fields, all mandatory: provider · agreement reference and date · scope (models, regions, express permission for multi-tenant resale) · counsel's sign-off identity and date · sha256 of the executed document. 'Nothing flips to listed without every field.' Marketplace reseller programmes (Azure OpenAI, AWS Bedrock, Google Vertex) noted as the intended route under D-17. Counsel brief is on the owner's desk to commission — not your scope."

**Authority chain:** R-24 (owner-held pending reseller-frontier disclosure · banked at CP-ENTITLEMENT-BUILD-WAVE seal chain `c4bf7094/eff17295/7d1e66a9`) + D-17 marketplace-reseller-programme route.

**E1 scope boundary:** E1 registers the schema and validates drops against it. E1 does NOT commission counsel, does NOT sign documents, does NOT evaluate the reseller programme substance. Counsel brief is owner's scope.

---

## Well-formed drop schema (all fields MANDATORY · "nothing flips to listed without every field")

### Required top-level fields

| Field name (kebab-case)                | Type                                                    | Mandatory | Description |
|----------------------------------------|---------------------------------------------------------|-----------|-------------|
| `provider`                             | string                                                  | ✅ | Marketplace reseller programme identifier. Enumerated set per D-17 route: `azure_openai` · `aws_bedrock` · `google_vertex` · other requires ratification. |
| `agreement-reference`                  | string                                                  | ✅ | Executed-document reference (contract-number or similar unique identifier issued by the reseller programme). |
| `agreement-date`                       | string (ISO 8601 date · `YYYY-MM-DD`)                   | ✅ | Date the agreement was executed. Not signing-received date; execution date. |
| `scope.models`                         | tuple[str, ...]                                          | ✅ | Enumerated model identifiers covered by the agreement (matched against Master Requirements Registry v5 model dimension). Empty tuple is INVALID (agreement must cover ≥1 model). |
| `scope.regions`                        | tuple[str, ...]                                          | ✅ | Geographic/cloud regions covered by the agreement. Empty tuple is INVALID. |
| `scope.multi-tenant-resale-permitted`  | bool (must be explicitly `true` or `false`)              | ✅ | Express permission for multi-tenant resale. Owner disposition verbatim: "express permission for multi-tenant resale". Silence or ambiguity IS `false` by default (fail-closed FP-2). |
| `counsel.signoff-identity`             | string (counsel name/firm)                                | ✅ | Identity of counsel who signed off on the reseller agreement's legal fitness for Akki platform's D-17 route. |
| `counsel.signoff-date`                 | string (ISO 8601 date · `YYYY-MM-DD`)                    | ✅ | Date of counsel's sign-off. Must be ≥ `agreement-date` (counsel signs off after execution). |
| `document-sha256`                      | string (64 lowercase hex)                                 | ✅ | sha256 of the executed document (PDF or docx). |
| `document-path-relative-to-custody`    | string (relative path)                                    | ✅ | Path of the executed document relative to `custody/owner_drops/<drop-timestamp>/`. Document itself lives in custody per §4.1 §E discipline. |

**Additional non-mandatory metadata** (may be recorded but not required for "flip-to-listed" transition):

- `agreement-expiry-date`: ISO 8601 date. If absent, agreement is treated as indefinite until superseded.
- `renewal-notice-window-days`: integer. Advance notice window for non-renewal, if applicable.
- `notes`: free-text banked observations from counsel or owner.

### Schema-level validation rules (all MUST pass · fail-closed FP-2)

1. **All mandatory fields present.** Missing field → drop rejected · reseller stays UNLISTED.
2. **`document-sha256` is 64 lowercase hex.** Regex: `^[a-f0-9]{64}$`. Case-sensitive lowercase per §4.1 §F sha-pinning discipline.
3. **`document-sha256` matches** the actual sha256 of the file at `custody/owner_drops/<drop-timestamp>/<document-path-relative-to-custody>`. Verified by `sha256sum` at drop-ingest time by E1.
4. **`counsel.signoff-date >= agreement-date`.** Enforced structurally.
5. **`scope.models` and `scope.regions` are non-empty tuples.** Empty tuple → drop rejected.
6. **`scope.multi-tenant-resale-permitted` is explicit boolean.** Missing / null / string → treated as `false` per FP-2 fail-closed default. E1 records the observed value and any ambiguity in the drop-validation receipt.
7. **`provider` matches the D-17 enumerated set** OR requires owner-ratified extension banked separately.

### Structural placement

- Drop lives at `custody/owner_drops/<YYYYMMDDTHHMM>Z_reseller_agreement_<provider>/` (owner-timestamped custody directory · per §4.1 §E).
- Manifest JSON at `custody/owner_drops/<YYYYMMDDTHHMM>Z_reseller_agreement_<provider>/manifest.json` with the schema above.
- Executed document PDF/docx at `custody/owner_drops/<YYYYMMDDTHHMM>Z_reseller_agreement_<provider>/<document-filename>`.
- E1 ingest procedure: verify manifest → compute sha256 of document → compare to `document-sha256` → validate all mandatory fields → bank drop-ingest receipt.

### Drop-ingest validation procedure (E1 mechanical process at drop-land time)

1. Verify `manifest.json` exists at the expected custody path.
2. Load manifest JSON (E1 may open the manifest · manifest is metadata, not credential material).
3. Verify all mandatory fields present. If any missing: **REJECT** · reseller stays UNLISTED · bank rejection receipt with the missing-field list.
4. Verify `document-sha256` regex conformance (`^[a-f0-9]{64}$`). If not: **REJECT**.
5. Compute `sha256sum <custody-path>/<document-path-relative-to-custody>` → compare to `document-sha256`. If mismatch: **REJECT**.
6. Verify `counsel.signoff-date >= agreement-date` (ISO 8601 parse and compare). If not: **REJECT**.
7. Verify `scope.models` and `scope.regions` are non-empty. If either empty: **REJECT**.
8. Verify `scope.multi-tenant-resale-permitted` is explicit boolean. If not: FP-2 default to `false` + bank the observation.
9. Verify `provider` is in enumerated set. If not: HOLD + bank fork for owner ratification (not automatic reject; owner may ratify extension).
10. If all checks pass: **ACCEPT** · reseller flips to LISTED at this-ingest. Bank drop-ingest receipt with all field values + all-checks-pass evidence + reseller-listed disposition.

**No wave opens on partial validation.** Owner directive: "Nothing flips to listed without every field."

### Sample manifest.json (empty template · to be filled by owner-side counsel at drop time)

```json
{
  "provider": "<enum: azure_openai | aws_bedrock | google_vertex>",
  "agreement-reference": "<contract-number-or-unique-id>",
  "agreement-date": "<YYYY-MM-DD>",
  "scope": {
    "models": ["<model-id-1>", "<model-id-2>"],
    "regions": ["<region-1>", "<region-2>"],
    "multi-tenant-resale-permitted": true
  },
  "counsel": {
    "signoff-identity": "<counsel-name-or-firm>",
    "signoff-date": "<YYYY-MM-DD>"
  },
  "document-sha256": "<64-lowercase-hex>",
  "document-path-relative-to-custody": "<filename.pdf-or-docx>",
  "agreement-expiry-date": null,
  "renewal-notice-window-days": null,
  "notes": null
}
```

---

## D-17 marketplace-reseller-programme route (owner-noted intended route)

Owner disposition verbatim: *"Marketplace reseller programmes (Azure OpenAI, AWS Bedrock, Google Vertex) noted as the intended route under D-17."*

- **azure_openai:** Microsoft's Azure OpenAI Service reseller programme. Contract terms per Azure marketplace agreement.
- **aws_bedrock:** Amazon Bedrock reseller programme. Contract terms per AWS marketplace agreement.
- **google_vertex:** Google Cloud Vertex AI reseller programme. Contract terms per Google Cloud marketplace agreement.

E1 does NOT evaluate the reseller-programme substance. E1's role: validate the drop against the schema above and enforce the flip-to-listed only on complete validation.

---

## Standing bounds unchanged

- E1 does NOT commission counsel · does NOT evaluate reseller-programme substance · does NOT sign documents.
- E1 validates drops mechanically against the schema.
- FP-2 fail-closed default: silence or ambiguity IS `false` for multi-tenant resale.
- No wave opens on partial validation.
- Zero push · zero remote configured · terminal-only operations.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law. Consult R-24 owner ruling banking at CP-ENTITLEMENT-BUILD-WAVE `c4bf7094/eff17295/7d1e66a9` for authority-chain context.
