# DB filename × sweep basename cross-check
- DB samples: **60** unique names (30 from `company.image_url`, 30 from `user_group_trainings.file_url`, 0 from `user_group_trainings.pend_action_file` sample)
- Match rule: exact basename match (case-insensitive) against any path enumerated in the sweep on each host

## akki-vm
- Enumerated basenames on this host: **26891** unique
- DB samples matched: **0** / 60
## akki-vm-ii
- Enumerated basenames on this host: **24407** unique
- DB samples matched: **0** / 60
## Verdict
**Zero DB-sampled filenames match any file on either GPU host.** The DigiCow file backend is definitively NOT on `akki-vm` or `akki-vm-ii`. This confirms the earlier prior probe finding at higher rigor: the block-device-up sweep saw every mounted filesystem, and the content-level classification saw every file's magic bytes on the reachable estate.
