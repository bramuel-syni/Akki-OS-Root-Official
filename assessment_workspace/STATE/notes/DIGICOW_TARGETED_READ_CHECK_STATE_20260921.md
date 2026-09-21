# DIGICOW targeted read-capability check — state note (2026-09-21T14:55Z)

**Trigger**: Owner directive this-session 2026-09-21T~14:35Z verbatim: "OWNER GO → targeted read-capability check on 'DIGICOW'".
**R-91 hold**: unchanged (~38h to `2026-09-23T03:23:15Z`).
**Ratchet floor**: 5858 (untouched).
**Discipline**: read-only, value-blind for credentials, receipted, hard-stopped after location + proof passes. No downloads. No writes. No `testing_agent`. No seal.

## Receipts banked

- `phase0/connectivity_receipts/20260921T145515Z_DIGICOW_targeted_read_check_owner_authorized_20260921.json` — the four-surface search + proof-of-read plan.
- `phase0/connectivity_receipts/20260921T150223Z_DIGICOW_cifs_deeper_search_20260921.json` — CIFS follow-up: honest `find` rc + tree-width fingerprint.
- Tools: `tools/digicow_targeted_read_check_20260921.py` + `tools/digicow_cifs_deeper_20260921.py`.

## Step 1 · Locate (value-blind) — where the token was searched

| # | surface | scope of search | hits |
|---|---|---|---|
| a | Fresh RMS CREDS sheet (`Sheet1`, sha `3311dae2…`) | every cell across every sheet, case-insensitive; USER/PASSWORD cells never emit values — only shape (len + sha8) is banked if matched | **0** |
| b | Last full-estate sweep receipt (`20260921T142146Z`) | every `show_databases`, `user_databases`, `representative_table`, `expected_schemas_in_sheet` string across all 8 authenticated MySQL clusters | **0** |
| c | OBS bucket inventory | (i) all 106 buckets in banked receipt `20260921T130729Z`; (ii) fresh `listBuckets` cross-check against `obs.ap-southeast-1.myhuaweicloud.com` with the rotated AK/SK | **0 + 0** |
| d | CIFS mount `/mnt/nfs-share` on JUMP (i.e. `//10.10.55.55/OFFAIRRECS/Record`) | top-level `ls -1` (all 16 channel dirs) + three progressively-broader `find -iname '*digicow*'` passes at depth 3 and depth 4 | **0 top-level; 0 in walked portion of depth 3-4** |

**Cross-run consistency**: every surface returned zero hits.

## Step 1d · Honest disclosure on CIFS

The initial CIFS pass used `find … | head` and reported rc=0 in 26.3s, but the pipeline masked `find`'s real exit. A follow-up (`20260921T150223Z_DIGICOW_cifs_deeper_search_20260921.json`) preserved `find`'s rc and extended the window to 90s. All three follow-up passes returned `rc=124 (TIMEOUT)` — meaning `find` did NOT complete the full depth-3/4 walk within 90 seconds. Tree width fingerprint (also captured):

| channel | depth-1 subdir count |
|---|---|
| channel01 | 324 |
| channel02 | 356 |
| channel03 | 356 |
| channel04 | 357 |
| channel05 | 356 |
| channel06 | 356 |
| channel07 | 356 |
| channel08 | 355 |
| channel09 | 355 |
| channel10 | 355 |
| channel11 | 356 |
| channel12 | 356 |
| channel13 | 170 |
| channel14 | **0** (empty channel) |
| channel15 | 356 |
| channel16 | **0** (empty channel) |

~4,860 date-subdirs total at depth 1. At depth 3 (`channelXX/YYYYMMDD/HH-MM-SS/…`), the walk is on the order of 10⁵ to 10⁶ paths over 47 TB via CIFS — 90s was not enough. **The CIFS search's negative is therefore not exhaustive.** However — see structural argument below.

## Structural argument for the NOT-PRESENT verdict, despite the CIFS-timeout caveat

The CIFS mount `/mnt/nfs-share` is the `OFFAIRRECS/Record` **broadcast-content archive**, organized as `channel{01..16}/YYYYMMDD/HH-MM-SS.mp4` (per the readable channel01 + channel04 samples captured on 2026-09-21T14:21Z, extension histogram = 2995-2996 `.mp4` per channel-tree, mtimes 2025-04-15…2026-09-21). A discrete application/service called "digicow" — a livestock-management platform for smallholder dairy farmers, in the wider Kenyan tech ecosystem — would not manifest as a subdirectory INSIDE a broadcast recording archive. If it existed within RMS estate, it would surface as:

- a distinct **top-level directory** on the CIFS mount → **not present** (top-level is exactly the 16 broadcast channel dirs, bounded).
- a distinct **CIFS/NFS share** on the NAS → **no such share visible** to the current mount + no other CIFS mounts on JUMP (`mount | grep -iE '(cifs|nfs)'` returns only `/mnt/nfs-share`).
- a distinct **MySQL schema** on any credentialed cluster → **not present** across all 8 clusters (VIUSASA/USSD/MICROSERVICES×5 including new/`159.138.173.58` Razuna+Newsvault).
- a distinct **MySQL cluster** in the RMS CREDS sheet → **not present** in the sheet (0 cell hits).
- an **OBS bucket name** → **not present** in the 106-bucket inventory nor in a fresh `listBuckets` call.

The CIFS timeout only leaves open the (highly implausible) case of "digicow" being nested somewhere inside `channelXX/YYYYMMDD/` — which would be an off-air recording file whose name happens to contain "digicow". That's a content-search question, not an estate-presence question.

## Step 2 · Proof-of-read

**Zero proof-of-read attempts made** — no location produced a hit that would warrant one.

## Verdict (binary + failure layer)

**Binary answer**: **NO** (with the CIFS-depth caveat above; structurally the answer is definitive across all named estate surfaces).

**Reason**: `SURFACE_NOT_PRESENT_IN_BANKED_ESTATE`. Digicow is a candidate owner-drop: the owner would need to provide a host/DB-name/API-endpoint/S3-bucket/mount-path plus credentials before we can prove read. No endpoint guessed.

**Content-readable**: **N/A — surface does not exist in the banked estate.**

## Standing bounds (unchanged)

- R-91 hold intact (~38h remaining to `2026-09-23T03:23:15Z` — do NOT execute early).
- Ratchet floor 5858 unchanged (survey-only).
- §3.8 additive-only intact.
- No `testing_agent`, no seal.
- S4 bulk ingestion still gated.

## Hygiene tally

- Read-only across every touch. Zero downloads. Zero writes.
- USER/PASSWORD cell values never emitted (shape-only path in the sheet search was designed but never triggered — no cell matched anyway).
- CIFS proof used `find` metadata only — no file byte reads. Top-level `ls -1` produced only structural directory names (`channel01..channel16`), safe to emit.
- OBS `listBuckets` returned bucket names only (public-to-account); no object bytes.
- JUMP host key un-drifted.

## Standing admin asks (unchanged from prior state note; digicow adds no new ones)

1. MySQL `159.138.162.146` creds — still missing.
2. MySQL `HOST` placeholder (WEEGO) — needs IP substitution.
3. Huawei OBS `obs:object:GetObject` scope on rotated AK/SK.
4. (nice-to-have) NAS DSM/SMB direct creds — CIFS mount still working via cached session.
5. **(new) digicow surface location + credentials** — if the owner expects to read digicow content, they need to supply the endpoint.

— end of state note.
