"""services.campaign_infra — 3-day unattended GPU campaign machinery.

Public surface:
    manifest.load_manifest, manifest.validate_manifest, manifest.iter_runs,
        manifest.ManifestInvalid
    checkpoint.write_checkpoint_marker, checkpoint.read_checkpoint_marker,
        checkpoint.latest_checkpoint_step
    on_host_logging.write_host_heartbeat, write_host_poll_receipt,
        write_run_summary, host_journal_root
    run_queue.execute_campaign, run_queue.next_pending_run,
        run_queue.CampaignRunAlreadyActive, run_queue.CampaignPriorRunNotSealed
    reconcile.adoptability_of_campaign_run, reconcile.list_host_runs

Zero-influence classes carried this wave:
    (1) observer-only (r1/r2 inherited),
    (2) recovery-not-interference (this wave):
        restart-from-checkpoint fires only against DEAD processes,
        resumes from LAST CHECKPOINT (never fresh-start),
        NEVER touches a live run,
        writes a journal entry per restart.
"""
