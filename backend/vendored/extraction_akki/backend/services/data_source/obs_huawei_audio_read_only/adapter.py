"""CENSUS-3-F · OBS audio → GPU pipeline · read-only adapter shape (Commit-A).

Owner-authority anchors (verbatim; survive compaction):

1. CENSUS-SURFACE-A Commit-B autopilot line 2026-09-22T~03:45Z verbatim:

   "CENSUS-3-F OBS audio GPU pipeline on 15 readable OBS audio buckets
    against dual-host H200 (akki-vm + akki-vm-ii) with 1-process-per-GPU
    workaround + stream-and-unlink discipline"

2. SO §6.8 clause A verbatim (2026-09-21T~18:35Z):

   "S4 IS OPEN ... Begin the S4 Data-Ingest slices immediately per the
    standing plan: ingestion adapters under
    services/data_source/{source}_read_only/, RED-first invariants
    (LawfulBasisAdmit-before-first-byte, no-second-store),
    additive-only, BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green sweeps
    before every Commit-A, 3-commit local seals, no push/no fetch,
    ratchet only rises."

3. Owner Ruling 2 verbatim 2026-09-22T~04:14Z:

   "CENSUS-3-F GPU pipeline opens (RED-first invariants before first byte:
    LawfulBasisAdmit + no-second-store + all-reads-receipted +
    idempotent-restart-from-cursor; 15 readable OBS audio buckets; dual-host
    4xH200; 1-process-per-GPU; stream-and-unlink)"

4. LawfulBasisAdmit banked at
   `phase0/lawful_basis_admits/20260922T014000Z_LAWFUL_BASIS_ADMIT_CENSUS3.json`
   — CENSUS-3 wave-level lawful-basis-at-Admit receipt (Doc 5 B5.2 anchor).

5. 15-bucket target list banked in
   `phase0/census_v3/20260922T014400Z_CENSUS3_OBS_chapter.json` field
   `getobject_ok_audio_intersect_next_lane_targets` — intersection of
   GetObject-OK-32 and audio-top-10-by-object-count.

Canon anchors:
- Doc 5 B5.2 lawful-basis-at-Admit emitted before first byte
- Doc 5 B5.4 append-only writer as sole persistence path (no-second-store)
- Canon-9 §3 single-writer discipline (`record_external_read` routes to
  the sealed ledger writer; the adapter is READ-ONLY on OBS and never
  authors state outside the sealed ledger)
- Doc 5 ENT/CON no-second-store adapter has zero writes outside ledger
  writer surface
- SO §2.5 verbatim-docstring · §3 tests-first · §3.3 3-Commit Seal ·
  §3.8 additive-only · §3.10-α Final[tuple[str, ...]] closed-vocab
  landing pattern · §6.4 NOTHING-BEYOND · §6.7 seal-report-boundary ·
  §6.8 no-GO clause A

Structural shape at Commit-A (this-commit):
- `TARGET_BUCKETS: Final[tuple[str, ...]]` — 15 buckets · Final tuple ·
  paired test asserts equality with on-disk census chapter (§3.10-α).
- `LAWFUL_BASIS_ADMIT_REF: Final[str]` — path to banked admit receipt.
- `OBSAudioReadOnlyAdapter` — five public methods:
    - `emit_lawful_basis_admit()` — call once at wave open · before-first-byte
    - `stream_object(bucket, object_key)` — stream-and-unlink to GPU host
    - `record_external_read(bucket, object_key, sha256, byte_count)` —
      routes to sealed ledger single-writer path
    - `save_cursor(bucket, object_key)` — idempotent-restart discipline
    - `restore_cursor(bucket)` — pairs with save_cursor for resume

Runtime bindings NOT wired at this Commit-A (deferred to next sub-slice):
- OBS S3 client (AK/SK from custody via `services.secret_hygiene` shape-only)
- SSH bridge to `akki-vm` (41.173.184.244) + `akki-vm-ii` (41.173.184.247)
  via `AKKI_VM_HOST` / `AKKI_VM_II_HOST` env vars (banked in
  `/app/backend/.env`) using key at
  `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu`.
- `faster-whisper tiny int8` remote invocation with 1-process-per-GPU
  workaround per GPU-LANE-OPEN-20260922 findings.
- Ledger writer identity resolved at runtime binding time.

The Commit-A shape is TESTS-AUTHORITATIVE structurally — its method
signatures, docstrings, and closed-vocab constants gate the invariant
suite.  Runtime wiring lands in the next Commit-A sub-slice
(CENSUS-3-F.2 · live streaming) once this shape is banked.

Additive-only per SO §3.8: no sealed module touched.
"""

from __future__ import annotations

from typing import Final


# ---------------------------------------------------------------------------
#  Closed-vocab constants (SO §3.10-α · Final[tuple[str, ...]])
# ---------------------------------------------------------------------------

TARGET_BUCKETS: Final[tuple[str, ...]] = (
    "news-vault",
    "rmsbroadcast",
    "music-bucket-rms",
    "skizaaudio",
    "google-transcripts",
    "chamgei-backup",
    "citizen-vod",
    "instore-radio-items",
    "hot96backup",
    "edailynew",
    "inoorotv",
    "citizentv",
    "razuna.royalmedia",
    "razuna-ireland-replication-7sep2017",
    "royalmedia",
)
"""The 15 CENSUS-3-F target buckets · verbatim from CENSUS-3-OBS chapter
field `getobject_ok_audio_intersect_next_lane_targets` banked at
`phase0/census_v3/20260922T014400Z_CENSUS3_OBS_chapter.json`."""


LAWFUL_BASIS_ADMIT_REF: Final[str] = (
    "phase0/lawful_basis_admits/20260922T014000Z_LAWFUL_BASIS_ADMIT_CENSUS3.json"
)
"""Reference to the CENSUS-3 LawfulBasisAdmit banked receipt (Doc 5 B5.2
lawful basis at Admit · emitted before first byte of the wave)."""


# ---------------------------------------------------------------------------
#  Adapter class shape (Commit-A · signatures + docstrings)
# ---------------------------------------------------------------------------


class OBSAudioReadOnlyAdapter:
    """CENSUS-3-F OBS audio → GPU pipeline read-only adapter.

    Per SO §6.8 clause A verbatim: adapter under
    `services/data_source/obs_huawei_audio_read_only/`.  This class holds
    the four RED-first invariants (LawfulBasisAdmit-before-first-byte ·
    no-second-store · all-reads-receipted · idempotent-restart-from-cursor)
    as method contracts.

    At Commit-A this class exposes shape only.  Live runtime bindings —
    OBS S3 client, SSH bridge to GPU hosts, faster-whisper invocation,
    ledger writer resolution — land in the next Commit-A sub-slice
    (CENSUS-3-F.2 live streaming) once this shape is sealed.

    Public surface (5 methods · no writer verbs outside ledger routing):

    - `emit_lawful_basis_admit()` — call once at wave open before any
      OBS byte crosses.  Idempotent.  Doc 5 B5.2.

    - `stream_object(bucket, object_key)` — pull a single OBS object,
      pipe it to the remote GPU host, and unlink the local copy before
      returning.  No persistent local storage · no-second-store · Doc 5 B5.4.

    - `record_external_read(bucket, object_key, sha256, byte_count)` —
      register an ExternalRead ledger event via the sealed single-writer
      path.  Every OBS GetObject routes through this method.

    - `save_cursor(bucket, object_key)` — persist the last-successfully-
      streamed object key for `bucket` so restart resumes at the next
      key · idempotent-restart-from-cursor.

    - `restore_cursor(bucket)` — return the last saved cursor key for
      `bucket`, or the empty string if no cursor is banked yet.
    """

    def emit_lawful_basis_admit(self) -> str:
        """Emit the wave-level LawfulBasisAdmit receipt before the first
        OBS byte crosses.

        Doc 5 B5.2 verbatim: 'lawful basis is emitted at Admit before the
        first byte'.  This method is the before-first-byte gate for the
        entire CENSUS-3-F wave: no `stream_object()` call may proceed
        until `emit_lawful_basis_admit()` has returned a receipt id
        (either the banked wave-level admit id at
        `LAWFUL_BASIS_ADMIT_REF`, or a fresh admit for a re-open).

        Returns:
            The admit receipt id string.  At Commit-A this is a stub
            that returns the banked wave-level admit id
            `LAWFUL-BASIS-ADMIT-CENSUS3-20260922T014000Z` (the same id
            written into the CENSUS-3 admit receipt at
            `LAWFUL_BASIS_ADMIT_REF`).  Live runtime binding to the
            sealed admit writer lands in CENSUS-3-F.2.
        """
        return "LAWFUL-BASIS-ADMIT-CENSUS3-20260922T014000Z"

    def stream_object(self, bucket: str, object_key: str) -> None:
        """Stream a single OBS object to the remote GPU host and unlink
        the local copy before returning.

        Doc 5 B5.4 verbatim: 'append-only writer as sole persistence
        path' — this method must not create a persistent local copy of
        the OBS bytes.  The stream-and-unlink discipline is enforced by
        construction: open a NamedTemporaryFile, write the OBS
        GetObject stream into it, scp it to the GPU host, unlink the
        local file in a `finally` block, then invoke `faster-whisper`
        remotely on the GPU-side copy · the GPU-side copy is itself
        unlinked after the language-ID result is returned.  No OBS byte
        outlives the ExternalRead event that receipted it.

        Commit-A: not yet implemented (NotImplementedError).  Runtime
        binding lands in CENSUS-3-F.2 live sub-slice.

        Args:
            bucket: OBS bucket name · must be in `TARGET_BUCKETS`.
            object_key: OBS object key within `bucket`.
        """
        raise NotImplementedError(
            "CENSUS-3-F.2 live streaming not yet wired; Commit-A ships "
            "shape only."
        )

    def record_external_read(
        self,
        bucket: str,
        object_key: str,
        sha256: str,
        byte_count: int,
    ) -> str:
        """Register an ExternalRead ledger event for an OBS GetObject.

        Canon-9 §3 verbatim: 'single writer; second writer is a defect
        on sight.'  This method routes to the sealed ledger
        single-writer path.  Every OBS GetObject — whether via
        `stream_object` or via any admin probe path — must emit an
        ExternalRead event through this method.

        The event payload carries: (bucket, object_key, sha256,
        byte_count, wave_id=`CENSUS-3-F`, lawful_basis_admit_ref).

        Commit-A: returns a synthetic receipt id.  Runtime binding to
        the sealed ledger writer lands in CENSUS-3-F.2 alongside live
        streaming.

        Args:
            bucket: OBS bucket name.
            object_key: OBS object key.
            sha256: Content sha256 (hex, lowercase).
            byte_count: Object byte count.

        Returns:
            The ExternalRead ledger event receipt id string.
        """
        return f"EXTERNAL-READ-CENSUS3F-STUB-{bucket}-{object_key}"

    def save_cursor(self, bucket: str, object_key: str) -> None:
        """Persist the last-successfully-streamed object key for `bucket`.

        Together with `restore_cursor` this method makes the pipeline
        idempotent-across-restart: on restart the streaming loop calls
        `restore_cursor(bucket)`, seeks to the next-after-cursor object
        key, and resumes.  Partial progress is preserved · no re-reads
        · no double-billing on the ledger.

        Commit-A: no-op stub (in-memory only).  Runtime binding to a
        sealed cursor-writer surface lands in CENSUS-3-F.2.

        Args:
            bucket: OBS bucket name.
            object_key: Last-successfully-streamed key.
        """
        return None

    def restore_cursor(self, bucket: str) -> str:
        """Return the last saved cursor key for `bucket`, or the empty
        string if no cursor is banked yet (fresh start).

        Commit-A: returns empty string (fresh-start stub).  Runtime
        binding to the sealed cursor reader lands in CENSUS-3-F.2.

        Args:
            bucket: OBS bucket name.

        Returns:
            Last-saved object key, or empty string if no cursor exists.
        """
        return ""
