# Reuse Audit — PARKED at Cat 6 (in-progress) per owner ruling 2026-08-28T~06:35Z ("Complete G")

## Cats 1-5 findings (banked; ready for closure post-Wave-G):

### Cat 1: DECKS TRACK
Executive-Core donor: MASSIVE. deck_*.py routers (4 files, 713 LOC) + services/deck_* (5 files, 883 LOC) + solva_v2/pptx_exporter.py (940 LOC) + work_studio/pptx_generator.py (368 LOC) + sandbox_templates.py (596 LOC) + services/synisense/deck_signal_extraction.py (230 LOC). Plus Executive-Final adds pdf_generator.py (215), docx_generator.py (221), work_studio/enhance.py (548), work_studio/brief.py (382), work_studio/persistence.py (301), routers/work_studio_export.py (2354). **Total ~8000 LOC of deck/render code available for LIFT-clean or ADAPT.** Master Plan currently frames Decks as "post-plan build-scheduled" — this audit says most of it is BUILD-ALREADY-DONE in donors.

### Cat 2: DOC 17 EXPANSION
RMS-IQ-Core-2 backend/services/perception (29 files) is **byte-identical to Extraction-Akki backend/services/perception (29 files)** — perception stack ALREADY FULLY LIFTED. VAD (140), ASR (248), diarization (197), model_loader (45), audio_batching (32), cuda_runtime (51), model_registry (114), execution_mode_telemetry (43), gpu_execution/*. No additional Doc-17 codec/tokenized/character-register code found in the perception donor beyond what's lifted. Character register, clustering, calibration, wizard-compile, invention: found in Executive-Core (sandbox_v2_strategic.py, sandbox_v2_corpus.py, studio_sensitivity.py, solva_v2 stack) — REFERENCE-pattern level, not clean-lift.

### Cat 3: DOC 14 BUILD ROWS
Extraction-Akki already has contracts/knowledge_artifact_v0.py, training_run_v0.py, model_acceptance_card.py, optimizer_comparison_v0.py, sever_certainty_signal_v0.py, evidence_register_row_v0.py, skill_file_provenance_v0.py, continuity_attestation.py — most Doc 14 contract surfaces already home. No named `contents_attestation`, `quality_card`, `moac_drift_detection` module in any donor with those exact names — BUILD or ADAPT-from-Doc-14-inline scope remains.

### Cat 4: WALK-THIS / EVIDENCE RECORDS
Extraction-Akki has services/audit_trail + services/trace + services/watch + services/grey_mirror. Executive-Core has services/solva_voice_audit. No Doc-10 evidence-record traversal named directly — v8 prototype embeds WALKS constant + walk types (bait/crossing/rule/broken) as data. LIFT-clean is v8 template constant; BUILD-thin is the traversal-side API to serve it. Small.

### Cat 5: WATCH MECHANISM (Doc 15-014)
Extraction-Akki backend/services/watch exists. Executive-Core has services/monitor + routers/monitor_strategic_items.py (591) + routers/monitor_status_assessment.py (401). ADAPT-viable for Watch tab expansions.

### Cat 6: 16 v8 APP DOMAINS — **IN PROGRESS at park time** — top-line findings so far:
**Executive-Core / Executive-Final are the GOLDMINE** — they contain built surfaces + backends for essentially every v8 domain I audited before the park:

- **Documents**: services/documents (935 LOC × 4 files) + routers/documents.py (2863 LOC) + frontend/components/documents (2929 LOC × 11 files) + pages/DocumentsPage.jsx (566) + pages/WorkStudioDocumentPage.jsx (88). **LIFT-CLEAN candidate ~6500 LOC**.
- **Task Manager**: services/tasks (1590 LOC × 5) + services/tasks_initiatives (550 × 3) + routers/tasks.py (1573) + routers/tasks_initiatives.py (539) + pages/TaskManager.jsx (248) + pages/TaskManagerActivity.jsx (111) + components/tasks (2796 × 5). **LIFT-CLEAN candidate ~7400 LOC**.
- **Collab (mentions/emails/projects/HR)**: services/inbox_routing (2356 × 11) + routers/inbound_email.py (1687) + routers/inbound_queue.py (368) + routers/admin_inbox.py (525). **ADAPT candidate ~5000 LOC** (Collab isn't quite the same as inbox but pattern-adjacent).
- **Data Suite / Analyze**: services/workbook_analyzer (2116 × 10) + services/analyze_workspace (569 × 3) + pages/AnalyzeJournal.jsx (423) + pages/WorkStudioAnalyze.jsx (438) + routers/workbook_analysis.py (1698). **LIFT/ADAPT ~5500 LOC**.
- **WorkStudio**: pages/WorkStudio.jsx (1578) + pages/WorkStudioActivity.jsx (133) + Cycle.jsx (1512) + Manage.jsx (508) + routers/cycle.py (1832) + routers/studio.py (915) + routers/studio_blocks.py (1226) + routers/cycle_manager.py (1344). **ADAPT ~9000 LOC**.
- **ThinkLab**: pages/ThinkLabApp.jsx (95) + ThinkLabSession.jsx (555) + ThinkLabSessions.jsx (462) + ThinkLabPhaseDSession.jsx. **ADAPT ~1500 LOC**.
- **Exco/Board 360**: components/marketing/Exco360Voice.jsx + components/home/ExcoTeamsCard.jsx + routers/exco_teams.py (355) + routers/monitor_strategic_items.py (591) + routers/monitor_status_assessment.py (401) + routers/strategic_goals.py (386) + routers/strategic_goal_assessment.py (393) + routers/briefings.py (1506) + routers/pulse.py (857) + routers/portfolio_data.py (372) + routers/company_home.py (603) + routers/ned/* (multiple NED-committee/meeting/inbox pages) + pages/CompanyHome.jsx. **ADAPT-heavy candidate ~7000 LOC — the "board briefings" grammar is Executive-Core's core competence.**
- **Trust Center**: routers/trust_center.py (897 LOC). LIFT-CLEAN candidate.

## Still to audit (Cat 6 remainder):
- Agent Builder + Your Agents domain
- Extract Data domain
- 3rd-Party Apps domain
- Full frontend component audit for the above
- LOC estimates → LIFT/ADAPT/BUILD split
- Top 5 highest-value lifts
- Recommended wave-order changes

## Boundary note
Audit is READ-ONLY. Zero code changes made. Findings compact-cached here for post-Wave-G resumption.
