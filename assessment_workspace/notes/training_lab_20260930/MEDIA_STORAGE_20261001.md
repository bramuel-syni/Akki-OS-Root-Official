# File & media storage — 1 October 2026

## Owner scope
Request: "Add the File & media storage integration to my app."
User replied "yes" to recommended music/audio + transcripts/label manifests; batch upload → private library → rights/label checks → training-lab assessment. Google Drive connection is a separate future integration. No retraining, media export to LLMs or model admission was authorized.

## Implemented
- WorkStudio **Media Library** at `/os/work/media`; accessible from WorkStudio launcher and Documents. Existing editorial visual language preserved; file titles, not internal IDs, appear in the interface.
- Real managed object storage via server-only integration credentials. Browser calls tenant-authenticated Akki endpoints; no storage keys, object paths, public file links or bearer tokens in download URLs.
- Two-stage idempotent upload reservation/content transfer; bounded temporary spool closes after relay. Server verifies declared size, SHA256 and basic container signatures/UTF-8/JSON/CSV structure before publishing an available record. No audio decoding or quality inference here.
- Operator writes / admitted-tenant reads; analysts cannot mutate and DIGICOW cannot access RMS files by ID. Optimistic metadata revision checks, archived/withdrawn download refusal, Watch mutation receipts, original-name attachment downloads and no-store/nosniff headers.
- Names, language, speech/music/mixed declarations, human-review checkbox, rights basis/reference and explicit training-permission declaration. Declaration is not independent rights verification.
- Selected-file assessments are atomically banked in the existing training lab, `kind=dataset_readiness`, metadata-only, always held before retraining. These never enter the GPU/model-review queue. Changing rights/details or archiving makes prior reports stale on both the media and training-lab APIs.
- Batch queue, progress/retry, filter/search, metadata and archive dialogs, readiness reports/history. User-facing retained bytes warning at upload, footer and archive confirmation.

## Provider constraints and application limits
- **No hard-delete API.** Archive revokes future app access; it does not physically erase provider bytes or downloaded copies. Do not call Archive "Delete" or claim compliance retention/immutability.
- No presigned/direct/resumable upload API in the verified provider contract. Transfers are bounded authenticated backend relays.
- Current app-configured limits: **25,000,000 bytes per audio file; 2,000,000 bytes per transcript/label file; 20 files per browser batch; 1,000,000,000 bytes per tenant reservations including archived files**. These are configured application limits, not asserted provider maximums. Incomplete reservations conservatively retain their allowance.
- Audio: WAV, MP3, FLAC, OGG, M4A. Transcripts: TXT, VTT, SRT. Label manifests: JSON, CSV. Archives/ZIP import and Google Drive are not supported by this upload flow.
- Format checks are not full media decoding, music detection, antivirus scanning or legal clearance. Uploaded files are served as attachments, not executed.

## Architecture
`services/media_library/{storage,formats,contracts,store,assessment}.py`, `routers/media_library.py`; existing server startup initializes managed storage once. Metadata/audit/quota collections: `media_files`, `media_events`, `media_quota` using unchanged MONGO_URL/DB_NAME. `services/training_lab/store.py` adds atomically complete dataset reports and dynamic stale checks. No login/JWT/password changes.

Frontend: `pages/os/WorkMedia.jsx`, `components/media/*`; navigation additions in `App.js`, `components/prototype/evidence.js`, `WorkDocuments.jsx`.

Config: `INTEGRATION_PROXY_URL`, existing server integration credential; `MEDIA_STORAGE_APP`, `MEDIA_MAX_FILE_BYTES`, `MEDIA_MAX_TEXT_BYTES`, `MEDIA_MAX_BATCH_FILES`, `MEDIA_TENANT_MAX_BYTES`. Credentials never appear in this note or the browser bundle.

## Verification
- `/app/test_reports/iteration_71.json`; final retest `/app/test_reports/pytest/iteration_71_media_retest.xml`: **10/10 media tests passed** after separating idempotency 409 from invalid-format 422.
- Existing lab/M8/M9 regressions: **24/24 passed**. Real provider uploads exercised for five formats, authenticated download bytes/hash checked, permissions/withdrawal/archive/staleness verified.
- UI desktop 1920×800 and mobile 390×844, plus DOM width checks at 320/768/1024/1440: no horizontal overflow. Upload retry negative path injected one **MOCKED failure only**. Test file contents are **SYNTHETIC**; no real music or model-quality claim. All test file records archived; metadata retained and provider objects not deleted. Test assessments remain explicitly named verification records.
- Existing frontend lacks an ESLint configuration; CLI lint could not run. Live frontend compilation/browser workflows passed. Screenshot paths: `test_reports/screenshots/iteration_71_ui/`.

## Next
User uploads authorized music, records rights/labels, selects a metadata readiness assessment. Actual worker-side music/quality evaluation, dataset annotation agreement, independent sealed evaluation and any GPU retraining still require the separately approved plan. Google Drive import and larger/resumable transfers remain backlog.