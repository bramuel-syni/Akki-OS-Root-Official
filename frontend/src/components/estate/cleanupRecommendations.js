// These are review instructions, not executable plans or claims of safe deletion.
export const cleanupGuidance = {
  obs_duplicate_objects: { title: 'Verify duplicate objects', next: 'Compare full object hashes, confirm retention rights, then choose the copy to keep. Check every reference before retiring another copy.', destination: 'Not selected. Bucket names are recorded; exact object paths and a verified keep-copy are not in this report.' },
  obs_cold_buckets: { title: 'Review older buckets for cheaper storage', next: 'Check read frequency and retrieval costs before changing the storage tier. A last-write date does not prove a file is unused.', destination: 'Proposed: archive tier in the same bucket, keeping object names. No new folder or move has been approved.' },
  archive_stale: { title: 'Review older tables for archiving', next: 'Confirm application dependencies and retention requirements; test a restorable snapshot before archiving.', destination: 'An approved archive location is still required. Keep the current table until restore is verified.' },
  redundant_indexes: { title: 'Review redundant indexes', next: 'Check query plans and index hints with the database owner before removing a covered index.', destination: 'No file move. Data stays in its current table; review the named indexes only.' },
  within_table_dedup: { title: 'Prevent repeated database rows', next: 'Confirm which repeated rows are intentional. Agree a uniqueness rule and preserve a recoverable copy before merging.', destination: 'Keep valid rows in the source table. An archive destination for removed rows has not been selected.' },
  cross_table_consolidation: { title: 'Compare overlapping table copies', next: 'Compare the complete rows and dependencies, then agree the authoritative table. Partial overlap is not grounds to delete either table.', destination: 'Choose the system of record from the two listed locations; neither is verified as the keep-copy.' },
  drop_empty: { title: 'Review empty tables', next: 'Confirm the table is unused and not temporarily empty before approving removal.', destination: 'No move proposed. A recoverable schema backup is required before removal.' },
  orphan_repair: { title: 'Check broken-reference candidates', next: 'Confirm the intended relationship before repairing references. Inferred targets can be wrong.', destination: 'Repair in the source table after confirming the target. No purge is approved.' },
  pii_minimisation: { title: 'Reduce unnecessary personal data', next: 'Ask the data owner which personal fields are required; remove or mask only approved fields in analytics copies.', destination: 'Keep authorised originals in the agreed system of record. The report does not select a new destination.' },
};

export const reviewOrder = items => [...items].sort((a, b) => {
  const rank = { obs_duplicate_objects: 0, obs_cold_buckets: 1, redundant_indexes: 2 };
  return (rank[a.key] ?? 3) - (rank[b.key] ?? 3);
});