# Portal Registry landing · DATA CONNECTED tab · UI spec (BANKED FOR POST-R-91)

- **Wave**: CENSUS-SURFACE-A · Commit-A" · Registry landing extension.
- **Design source**: RMS AI Prototype Ver 2.0 Sep 2026 · owner-shared
  3-page addendum (2026-09-22T~03:2XZ · "TWO OWNER DELIVERIES · Part 1").
- **Status**: BANKED · not implemented in App.js this seal.
- **Blocker**: R-91 horizon `2026-09-23T03:23:15Z` (owner NO-EXPEDITE
  ruling 2026-09-21T~06:15Z · unchanged).
- **Post-R-91 ε-apply gate**: ε-apply mirrors `/app/frontend/src/App.js`
  byte-identically to `pod_shell/frontend/src/App.js` FIRST; this
  Registry landing UI lands in the SAME horizon-boundary seal along
  with the census journey UI spec after ε-apply completes.
- **Backend endpoint**: `GET /api/portal/census/registry-landing`
  (JWT-gated · additive under §3.8 · lands this-Commit-A").

---

## 1. Page shape (owner design pixel-for-layout)

```
Registry (MANAGE ESTATE)                                    ┌───────────────────┐
├── [Shield report]  [+ Connect]                            │                   │
│                                                            │  CENSUS RUN       │
├── ┌ Tabs ────────────────────────────────────────────┐    │  STATUS           │
│   │  ▸ DATA CONNECTED     COMPUTE      LLMS &        │    │                   │
│   │                       CONNECTED    TRAINED       │    │  ── idle ─────    │
│   │                                    MODELS        │    │  Next census:     │
│   └───────────────────────────────────────────────────┘    │  Sep 29, 2026    │
│                                                            │  (in 7 days)      │
├── DATA CONNECTED — CENSUS #3                             │                   │
│   See what your estate holds, as last counted on           │  [Run census]    │
│   Sep 22, 2026 by owner. Every figure here was measured,   │  View past       │
│   not estimated.                                           │  censuses →      │
│                                                            │                   │
├── ┌─────────────┬─────────────┬─────────────┬───────────┐  │  ── running ──   │
│   │ HELD IN     │ SOURCES     │ DATA TYPES  │ LANGUAGES │  │  Started 18s ago │
│   │ TOTAL       │ CONNECTED   │ PRESENT     │ OBSERVED  │  │  ~58s left       │
│   │             │             │             │           │  │  Running…        │
│   │ 161.8 TB    │ 6           │ 5           │ 15        │  │  🔴 1 response   │
│   │ across 6    │ each        │ audio, doc, │ Swahili & │  │  required        │
│   │ connected   │ recorded at │ image, db,  │ English   │  │                   │
│   │ sources     │ connection  │ pdf         │ dominant  │  ├───────────────────┤
│   └─────────────┴─────────────┴─────────────┴───────────┘  │  WHAT CENSUS      │
│                                                            │  FOUND            │
├── HOW FAR IT HAS BEEN READ ▸ (collapsible)                 │                   │
│                                                            │  Almost half of   │
├── WHAT NEEDS CARE ▸                                        │  everything held  │
│                                                            │  in the readable  │
├── THE MIX, IN THREE VIEWS ▾ (expanded)                     │  32 buckets is    │
│                                                            │  audio — chiefly  │
│   ┌ CONDITION OF THE ESTATE ────┐                          │  Swahili customer │
│   │  4 censuses since May 12    │                          │  service calls.   │
│   │  ▓▓▓░░░░░░░░░░░░░░░░░░░     │                          │                   │
│   │  Read verified 5%           │                          ├───────────────────┤
│   │  Read not verified 12%      │                          │  CENSUS DID       │
│   │  Problems found 3%          │                          │  NOT TOUCH        │
│   │  Never read 80%             │                          │                   │
│   └─────────────────────────────┘                          │  74 buckets       │
│                                                            │  never read (74   │
│   ┌ HOW FAR WE HAVE GOT WITH IT ┐                          │  na7p4* + cold-   │
│   │  Read verified 8.1 TB       │                          │  tier), 5 mirror  │
│   │  Read not verified 19.4 TB  │                          │  pairs confirmed. │
│   │  Problems found 4.9 TB      │                          │  Their volume is  │
│   │  Never read 129.4 TB        │                          │  held out of      │
│   └─────────────────────────────┘                          │  every verified   │
│                                                            │  figure until     │
│   ┌ IN WHICH LANGUAGE ──────────┐                          │  the next census  │
│   │  15 languages observed      │                          │  reaches them.    │
│   │  Swahili (sw)  90%          │                          │                   │
│   │  English (en)  5%           │                          ├───────────────────┤
│   │  Not yet measured (74       │                          │  WHAT YOUR DATA   │
│   │  blocked buckets)  80%      │                          │  CAN DO           │
│   └─────────────────────────────┘                          │                   │
│                                                            │  → Product cards  │
│   ┌ HELD PER CENSUS ────────────┐                          │  based on         │
│   │  #1 · 0 TB   (first read)   │                          │  verified data    │
│   │  #2 · 3 GB   (+3 GB)        │                          │  only             │
│   │  #3 · 161.8 TB  (+161.8 TB) │                          │                   │
│   └─────────────────────────────┘                          └───────────────────┘
│
│   ┌ WHAT IT IS MADE OF ─────────┐
│   │  Audio archive   ~29 TB     │
│   │  Video/binary    ~104 TB    │
│   │  Documents       ~15 TB     │
│   │  Database         ~3 GB     │
│   │  Images/PDFs     ~13 TB     │
│   └─────────────────────────────┘
│
│   ┌ WHERE IT FALLS SHORT ───────┐
│   │  32 of 106 OBS buckets read │
│   │  5871 cross-bucket clusters │
│   │  Never read: 74 OBS buckets │
│   └─────────────────────────────┘
│
│   ┌ WHAT YOU CAN DO WITH IT ────┐
│   │  (Rights class is declared  │
│   │   at Connect, not measured) │
│   │  Internal only  63.9 TB 74% │
│   └─────────────────────────────┘
│
├── HOW THE ESTATE IS MEASURED ▸
│
└── ── HONEST-ACCOUNTING LAW ─────────────────────────────────┐
    │ Unverified volume is excluded from every verified       │
    │ figure until the next census reaches it.                │
    │                                                         │
    │ Verified volume:   30.32 TB (32 GetObject-OK buckets +  │
    │                    Digicow S3 audio + RDS content)      │
    │ Unverified volume: 131.44 TB (74 IAM-blocked +          │
    │                    unreached surfaces)                  │
    │ Total measured:    161.76 TB                            │
    └─────────────────────────────────────────────────────────┘
```

---

## 2. Read model contract (GET /api/portal/census/registry-landing)

Response is a nested dict with the following top-level shape:

```json
{
  "tabs": ["DATA CONNECTED", "COMPUTE CONNECTED", "LLMS & TRAINED MODELS"],
  "active_tab": "DATA CONNECTED",
  "manage_estate_buttons": [
    {"label": "Shield report", "kind": "secondary"},
    {"label": "+ Connect", "kind": "primary"}
  ],
  "data_connected": {
    "header": {
      "census_number": 3,
      "last_counted_on_utc": "2026-09-22T01:36:48Z",
      "last_counted_by": "owner",
      "measurement_pledge_copy": "Every figure here was measured, not estimated."
    },
    "stat_cards": {
      "held_in_total": {
        "value": 161.76, "unit": "TB",
        "caption": "across 6 connected sources"
      },
      "sources_connected": {
        "value": 6,
        "caption": "each recorded at connection"
      },
      "data_types_present": {
        "value": 5,
        "type_names": ["audio/*", "video/*", "image/*", "application/pdf", "text/*"],
        "caption": "audio, video, image, pdf, text"
      },
      "languages_observed": {
        "value": 15,
        "language_codes": ["sw", "en", "ar", "es", "mi", "la", "ro",
                            "ko", "de", "nn", "el", "nl", "cy", "gu", "pt"],
        "dominant_language_codes": ["sw", "en"],
        "caption": "Swahili & English dominant"
      }
    },
    "collapsibles": {
      "how_far_it_has_been_read": {
        "headline_copy": "HOW FAR IT HAS BEEN READ",
        "sub_copy": "See how much of the estate the census reached, and how much of that has been checked back against its source.",
        "body": {...}
      },
      "what_needs_care": {
        "headline_copy": "WHAT NEEDS CARE",
        "sub_copy": "See where the estate carries risk, restriction or damage. These four figures decide what can be used, and how.",
        "body": {...}
      },
      "the_mix_three_views": {
        "headline_copy": "THE MIX, IN THREE VIEWS",
        "sub_copy": "See what the estate is made of, how far we have got with it, and what you are allowed to do with it.",
        "body": {
          "condition_of_the_estate": {
            "read_and_verified": 5.0,
            "read_not_verified": 12.0,
            "problems_found": 3.0,
            "never_read": 80.0,
            "censuses_since_first": 4,
            "first_census_date_utc": "2026-08-28T15:48:38Z"
          },
          "how_far_we_have_got_with_it": {
            "read_and_verified_tb":  8.09,
            "read_not_verified_tb": 19.41,
            "problems_found_tb":     4.85,
            "never_read_tb":       129.41
          },
          "in_which_language": {
            "entries": [
              {"code": "sw", "name": "Swahili", "size_tb":  … , "share_pct": …},
              {"code": "en", "name": "English", "size_tb":  … , "share_pct": …},
              …
            ],
            "dominance_note": "Swahili and English dominant.",
            "not_yet_measured_share_pct": 80.0
          },
          "held_per_census": {
            "entries": [
              {"census_number": 1, "size_tb": 0.0, "delta_vs_previous_tb": null,   "delta_chip_copy": "first read"},
              {"census_number": 2, "size_tb": 0.003, "delta_vs_previous_tb": 0.003, "delta_chip_copy": "+ 3 GB"},
              {"census_number": 3, "size_tb": 161.76, "delta_vs_previous_tb": 161.76, "delta_chip_copy": "+161.76 TB"}
            ]
          },
          "what_it_is_made_of": {
            "entries": [
              {"type_name": "audio",     "size_tb":  29.12, "share_pct": 18.0},
              {"type_name": "video",     "size_tb": 104.14, "share_pct": 64.4},
              …
            ]
          },
          "where_it_falls_short": {
            "sources_swept_last_census": 32,
            "sources_total": 106,
            "duplicate_pairs_flagged": 87684,
            "never_read_note": "74 OBS buckets IAM-blocked (dominated by na7p4* series)."
          },
          "what_you_can_do_with_it": {
            "axis_note": "Rights class is declared at Connect, not measured.",
            "declared_at_connect_entries": [
              {"class_name": "Internal only", "size_tb": 119.7, "share_pct": 74.0},
              …
            ]
          }
        }
      },
      "how_the_estate_is_measured": {
        "headline_copy": "HOW THE ESTATE IS MEASURED",
        "sub_copy": "See what stands behind every figure above, including the one figure nobody has measured yet.",
        "body": {...}
      }
    },
    "right_rail": {
      "census_run_status": {
        "state": "idle",
        "next_census_utc": "2026-09-29T05:52:00Z",
        "days_until_next": 7,
        "actions": [
          {"label": "Run census",         "endpoint": null},
          {"label": "View past censuses", "endpoint": "/api/portal/census/records"}
        ],
        "responses_required": 0
      },
      "narrative": {
        "what_census_found": "Almost half of everything held in the readable 32 buckets is audio — chiefly Swahili customer service calls.",
        "census_did_not_touch": {
          "counts": {
            "never_read": 74,
            "read_but_not_verified": 0,
            "read_with_problems_found": 0,
            "flagged_as_possible_duplicates": 87684
          },
          "prose_copy": "74 buckets never read (74 na7p4* + cold-tier), 5871 cross-bucket clusters flagged as possible duplicates. Their volume is held out of every verified figure until the next census reaches them."
        },
        "what_your_data_can_do": {
          "prose_copy": "Six things could be built from what is already verified …",
          "product_cards": [
            {"name": "Complaints intelligence product",  "verified_only": true},
            {"name": "Swahili-first ASR fine-tune corpus", "verified_only": true}
          ]
        }
      }
    },
    "honest_accounting_law": {
      "law_copy": "Unverified volume is excluded from every verified figure until the next census reaches it.",
      "total_volume_tb":     161.76,
      "verified_volume_tb":   30.32,
      "unverified_volume_tb": 131.44
    }
  }
}
```

---

## 3. Real-data mapping (owner directive: "Map our real data into this model")

| Read-model field                             | Source receipt                                                                              |
|----------------------------------------------|---------------------------------------------------------------------------------------------|
| `stat_cards.held_in_total.value`             | `phase0/census_v3/20260922T014400Z_CENSUS3_OBS_chapter.json` · `estate_rollup.total_bytes_scanned_across_buckets_capped_TB` |
| `stat_cards.sources_connected.value`         | Length of `_SURFACE_DESCRIPTORS` in the hydrator (currently 6)                              |
| `stat_cards.data_types_present.type_names`   | Union of every surface's `media_types` tuple                                                |
| `stat_cards.languages_observed.language_codes` | Keys of `lang_by_prior_label.speech + speech_probable` in `DIGICOW_LANGID_AGGREGATE.json` |
| `condition_of_the_estate.*`                  | Derived from OBS chapter access reassessment + duplication chapter V2 verification counts   |
| `in_which_language.entries[]`                | LID aggregate `lang_by_prior_label` counts weighted by `total_manifest`                     |
| `held_per_census.entries[]`                  | `phase0/census/census_000N/manifest.json` × 3 + OBS chapter for #3                          |
| `where_it_falls_short.duplicate_pairs_flagged` | Duplication chapter V2 `tier_1_obs_catalogue.cross_bucket_clusters`                       |
| `honest_accounting_law.verified_volume_tb`   | OBS bytes on the 32 GetObject-OK buckets + Digicow S3 verified content + RDS content        |
| `honest_accounting_law.unverified_volume_tb` | Total volume − verified                                                                     |

---

## 4. Honest-accounting law · owner-embedded rule

Owner directive verbatim: *"Note the honest-accounting law embedded there:
unverified volume is EXCLUDED from every verified figure until the next
census reaches it — carry that rule into the read model."*

This is not just copy. Any figure that the FE renders as "verified" MUST
be derived from `honest_accounting_law.verified_volume_tb` (or narrower
subsets) — NEVER from `total_volume_tb`. The read model separates the
two so the FE cannot conflate. Invariant test
`test_registry_landing_verified_figures_exclude_unverified_volume`
enforces `verified + unverified ≈ total` and `unverified > verified` at
the CENSUS-3 boundary (74 of 106 OBS buckets IAM-blocked).

---

## 5. Compute Connected + LLMs & Trained Models tabs

Named for tab-nav parity only this-seal. Body payloads for those two
tabs land in later waves (out of §6.4 scope for Commit-A"). Read model
returns them as `{"placeholder": true, "reason": "landed in later wave"}`
so the FE renders a "coming soon" state without breaking the tab shell.

---

## 6. Post-R-91 landing checklist

After ε-apply mirrors `App.js` byte-identically to `pod_shell/App.js`:

1. Author `RegistryLandingPage.jsx` component under `frontend/src/`
   binding `data-testid="registry-landing-*"` per §data-testid rule.
2. Wire tab navigation (three tabs) with `data-testid="tab-data-connected"`
   etc.; DATA CONNECTED is default active.
3. Render stat cards from `body.data_connected.stat_cards.*` with
   `data-testid="stat-card-held-in-total"` etc.
4. Render collapsibles from `body.data_connected.collapsibles.*` with
   headline_copy + sub_copy sourced from the payload verbatim.
5. THE MIX (expanded) five sub-cards each with own `data-testid`.
6. Right rail census-run-status idle/running variants + narrative
   sections with `data-testid="right-rail-*"`.
7. Honest-accounting law rendered as a persistent footer band with
   `data-testid="honest-accounting-law"` — always visible on DATA
   CONNECTED, not collapsed.
8. Compute + LLMs tabs render "coming soon" state from placeholder.

## 7. Sources-win-if-drift

If any line above disagrees with owner-shared design surface (RMS AI
Prototype Ver 2.0 Sep 2026 3-page addendum), owner design wins. Update
this spec with `SUPERSEDED-BY` annotation; do not edit in place.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
