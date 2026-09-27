# Workspace, repository and original Akki runtime — read-only comparison

## User request and boundary

Owner reports original Akki is live on `amazing-gates-8`, suggests connection is
pod-local rather than repository-owned, and asks to review newly pushed Git changes
and establish connectivity of both workspace and repo. Owner confirmed read-only
scope after clarification. No GPU/SSH/provider connection, workload, configuration,
credential or application change was authorised or performed in this review.
Read-only Git remote metadata requests were attempted; authentication/access failed.

## Observed current workspace

- Container hostname: `agent-env-8523a138-0b62-4004-aa52-eca60cb63a15`.
- Frontend configured app host: `pensive-goodall-6.preview.emergentagent.com`.
  Source: existing REACT_APP_BACKEND_URL; no preview URL inferred from old records.
- This is not evidence that the current runtime is `amazing-gates-8`.
- Selected configuration (`backend/.env` plus this inspection process overrides)
  contains two host profiles, `akki-vm` and `akki-vm-ii`. Each has endpoint/user/key
  path/identity receipt+pin configuration, and the referenced key/receipt/known-hosts
  files exist. No password is configured for these profiles in this inspected
  configuration. Contents of private keys were not read, fingerprints not derived,
  and identity validity/authentication was not tested. Presence does NOT establish
  equivalence to the original pod or successful access.
- No direct `amazing-gates-8` reference was found in selected AKKI_/CENSUS_/REACT_APP_
  environment values. This is a scoped check, not a claim that all possible bridges
  anywhere in the project were dynamically inspected.

## Git/code provenance

- Root checkout `/app`: branch `main`, inspected HEAD
  `b2ed3ef6625354b6ba5dcdbb8fd4a9e6b2c48697` (2026-09-27).
- Configured origin: `https://github.com/bramuel-syni/Akki-OS-Root.git`.
- Cached `origin/main`: `bd776f0e5f07c736016ea93ea6870b913596b6d3`, dated
  2026-09-24. Cached tracking data is NOT current remote evidence.
- `git ls-remote` could not authenticate/access origin with available configuration.
  **Owner's latest push was NOT fetched or verified.** No fetch/pull/reset/check-out,
  merge, push, remote modification or git write action was performed.
- `backend/server.py:19–58` selects a workspace Extraction-Akki backend if it exists,
  otherwise the vendored backend. `AKKI_FORCE_VENDORED` is not enabled in the inspected
  configuration; the workspace source backend directory is absent.
- `/app/assessment_workspace/repos/Extraction-Akki` exists as a directory but has
  neither its own `.git` nor a `backend`. Git invoked from there walks upward and
  reports `/app` as its repository root; it is NOT a second source checkout.
- Therefore the bootstrap rule selects
  `/app/backend/vendored/extraction_akki/backend`.
- Vendoring manifest records generation at `2026-09-24T03:54:05Z`,1070 files.
  There are subsequent local implementation changes; that timestamp does not mean
  every current file is identical to the original snapshot. This is a code copy,
  not a live process/connection link to the original Akki workspace.

## Why the environment distinction is real

`services/training_runner/ssh_seam.py:192–250` resolves host details and credential
paths from the executing process's environment. It does not use a Git identity.

`services/census_autonomy/remote_dispatch.py:16–27` loads the current configured
private key through the identity verifier, loads the current known-hosts file,
sets `allow_agent=False` and `look_for_keys=False`, and initiates its own connection.
No automatic reuse of an original pod's SSH agent/session is provided by this path.

`services/census_autonomy/execution_identity.py:28–50,55–95` verifies a local pinned
identity receipt and the key actually loaded from the local file before transport.
A copy of the receipt/public fingerprint is not the same thing as possession of the
right admitted private key and current remote authorisation.

Same repository/code/configured paths do not imply shared process state, private
key contents, environment, mounted custody, network source identity, grants or
existing connections. Different pods can nevertheless be separately admitted to
the same workers; the original connection does not inherently prohibit another.
This finding supports the owner's runtime-boundary explanation, but it is NOT yet
proof of the exact cause of earlier authentication rejection.

## What is known about the original workspace

Retained original-programme documents reference `job_amazing-gates-8` artifact
custody. In particular, `notes/ingest_20260907/manifest.md:54–67` reports real trainer
and dispatcher heartbeats on both Akki hosts at 2026-09-06T17:32Z, with actual step
progress. This is historical documentation supporting earlier real execution, not
a new observation that the original pod is connected now.

The owner's present report of live original connectivity remains distinguishable
from those historical records and from direct observation in this workspace.
No present process/session/keyring/network/worker health data from `amazing-gates-8`
was inspected. The earlier unbound/NOT LIVE-VERIFIED findings concern the traced
new activation composition in THIS workspace, not a proof that original Akki has
no live workers or that the GPU estate is down.

## Answers and next evidence

1. **Different workspace/runtime from the original?** Confirmed by current identity
   and source-resolution/configuration evidence; not a claim about physical CPU host.
2. **Repo linked by origin?** Configured, yes. Current authenticated remote access and
   latest-push equivalence are unverified/blocked by remote-read access failure.
3. **This workspace automatically inherits the original GPU connection?** No such
   mechanism in the traced connection path. It authenticates from local configuration.
4. **This workspace connected now?** Configuration present; no current successful
   connection verified. Neither current success nor current hardware failure asserted.
5. **Original workspace connected now?** User reports yes; retained historical real
   work supports past connectivity. Current original-pod health remains unobserved.

To complete the comparison, establish an accessible latest original source commit
and a timestamped non-secret runtime binding/health receipt from the original pod:
source commit, configured runtime/worker identities, public-key fingerprint and
custody reference identifiers, approved endpoint and current connection/heartbeat
status. Do not put private keys/passwords in Git or chat and do not replace keys as
a shortcut. Resolve whether the supported path is reuse of the existing admitted
worker/control interface or separately admitted caller access before any change.

Preserve the original working runtime. No competing controller, identity rotation,
fresh GPU retry or claimed restoration is justified by this read-only finding.