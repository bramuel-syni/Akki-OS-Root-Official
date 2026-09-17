# PLATFORM_LAYER_REQUIREMENTS_v0_2.md

**Source of truth:** "Akki OS Pilot — Platform Reference v0.2" (17 September 2026 · Status: reference for development). Full doc fetched this turn from customer-assets URL under the STANDING_ORDERS §1 SESSION BOOT PROTOCOL discipline. Local mirror-of-record for future sessions.

**Owner directive banking (2026-09-17):** treat this document as a milestone-level requirements pack for a new build stream, and drive the walk under all standing disciplines (tests-first RED → GREEN → GREEN byte-match, `BASELINE_GUARD=1`, monotonic ratchet, §3.3 3-commit, LOCAL-ONLY, no `testing_agent`, thin-kernel no-refactor, JSON persistence, reference-not-copy, POST-2 placement, GPU check-in at every seal boundary).

**Milestone banner:** **M9 · Akki OS pilot platform layer** (multi-tenant control plane). Home for new mechanisms: `services/platform_control_plane/` (new home selected per POST-2 · no peer existed prior to this ingest; naming mirrors the doc's own §4.1 "Control plane" language).

---

## §1 · Verbatim scope (§1.2 of the source doc)

Covers:
- Tenancy model and hosting architecture
- Data-estate integration
- Compute integration, allocation and isolation
- Access management
- Account setup and personalisation wizard
- App catalogue and per-tenant enablement
- Control-plane data model
- Pilot tenant register and acceptance criteria

Does NOT cover (record as requirements, do NOT build): individual app behaviour · model pipelines · commercial terms · cross-tenant users · custom roles · per-user personalisation · custom domains · typography/layout theming · tenant self-service provisioning · billing · data residency beyond region · third-party/marketplace apps · tenant-initiated allocation changes. (§13.)

## §2 · Definitions extracted verbatim (§2)

- **Tenant** — one company (RMS, Trinity, DigiCow, BDO each one tenant). Owns its users, data estates, compute allocations, apps, theme and audit trail.
- **Data estate** — named collection of data sources belonging to a tenant, integrated through connectors.
- **Connector** — configured link from the tenant's data plane to one data source inside an estate, with a declared scope and access mode.
- **Compute integration** — source of compute available to a tenant: tenant-provided OR central-pool allocation.
- **Central pool** — GPU + CPU capacity owned and operated by the Akki OS pilot environment, partitioned into per-tenant allocations.
- **Allocation** — a tenant's reserved share of the central pool: GPU count/fraction · class · hours-per-period · concurrency limit.
- **Control plane** — shared, Syni-operated services managing tenants, identity, catalogue, scheduling, metering, audit. **Metadata only.**
- **Data plane** — per-tenant services connecting to estates, running workloads, and storing derived artefacts.
- **Workspace** — division inside a tenant used to scope users and outputs. Every tenant has at least one.
- **Task** — unit of approved work with objective, MOU reference, and explicit list of connectors and modes it may use. Every job runs under a task.
- **MOU task reference** — identifier of the task as defined in the tenant's MOU. Required on every connector and task.

## §3 · Verbatim mandates (become invariants)

### Tenancy (§3)
- M-T-1 (§3.1). *"A tenant maps one-to-one to a legal entity."*
- M-T-2 (§3.1). *"All resources are owned by exactly one tenant and carry its tenant_id."*
- M-T-3 (§3.1). *"There are no shared resources between tenants other than the control plane itself and the physical hardware of the central pool, both of which are partitioned by tenant_id at every layer."*
- M-T-4 (§3.3). *"A tenant's work never runs on, is visible from, or is queued alongside another tenant's integration."*

### Hosting & tenant-context enforcement (§4)
- M-H-1 (§4.3). *"The API gateway resolves tenant_id from the authenticated session and injects it into every request. Clients cannot supply it."*
- M-H-2 (§4.3). *"Every data-plane service validates tenant_id on every call against its own provisioned identity and rejects mismatches."*
- M-H-3 (§4.3). *"Storage is namespaced by tenant_id at bucket, prefix or schema level. Row-level filtering is never the sole isolation mechanism."*
- M-H-4 (§4.3). *"Job queues are partitioned per tenant. A runner is bound to one tenant_id and cannot dequeue another tenant's work."*
- M-H-5 (§4.3). *"Metrics, logs and traces carry tenant_id and are filtered by it at the query layer."*
- M-H-6 (§4.3). *"A cross-tenant access test suite runs on every deploy. Release is blocked on failure."*
- M-H-7 (§4.7). Tenant lifecycle: `provisioning → sandbox_active → production_active → suspended → offboarded`.
  - suspended = sessions revoked · jobs halted · allocations released · data retained.
  - offboarded = control-plane metadata + Syni-hosted derived artefacts deleted within 30 days · data-plane certs revoked · allocation returned to pool.
- M-H-8 (§4.4). Sandbox attaches only to `sandbox_safe=true` connectors + sandbox allocation. Promotion to production requires **tenant_owner + platform_operator** joint approval.
- M-H-9 (§4.5). Per-tenant secret store with envelope encryption under per-tenant key. Break-glass required to read plaintext.

### Connector modes & access (§5)
- M-C-1 (§5.2). Every connector carries: `type`, `location`, `credential_ref`, `scope`, `mode`, `mou_task_ref`, `status`. Empty scope is invalid.
- M-C-2 (§5.3). Modes: `discovery` (list/metadata/count/sample-headers; no content) · `read` (discovery + content extraction) · `write` (read + derived-output write within designated path).
- M-C-3 (§5.3). *"Mode is enforced in the connector runtime, not in the calling app."*
- M-C-4 (§5.3). *"Raising a connector's mode requires approval by a `data_steward` or `tenant_admin`, is logged, and invalidates any task that referenced the connector until the task is re-approved."*
- M-C-5 (§5.4). *"Every connector passes a connection test before it can be attached to a task. The test verifies reachability, authentication and scope resolution. It does not read content."*

### Compute (§6)
- M-Cp-1 (§6.4). *"Every job names a compute_integration_id (an allocation or tenant-provided compute). Jobs without one are rejected at submission."*
- M-Cp-2 (§6.4). *"The scheduler admits a job only if the named integration belongs to the job's tenant, has the class the job requires, and has capacity within its reservation, burst ceiling, hour budget and concurrency limit. Rejections state the reason."*
- M-Cp-3 (§6.4). *"Central-pool jobs run in tenant-dedicated execution contexts: separate Kubernetes namespaces (or equivalent) per tenant, per-tenant node taints or MIG partitions for GPU, network policies that deny all cross-namespace traffic, and per-tenant storage mounts. No two tenants' processes share a namespace, a GPU partition, or a mount."* — CONTRACT-MODELED (verify-on-real-infra).
- M-Cp-4 (§6.4). *"Reserved-capacity jobs are never pre-empted. Burst jobs are pre-emptible by another tenant's reserved-capacity jobs within SLA."* — CONTRACT-MODELED (verify-on-real-infra).
- M-Cp-5 (§6.4). *"Queue position, job metadata, logs and metrics are visible only to the owning tenant."*
- M-Cp-6 (§6.5). Metering records GPU-seconds + CPU-seconds + RAM-seconds + bytes-read + bytes-written per `tenant_id + compute_integration_id`. Reconciliation invariant: `sum(job_gpu_seconds per tenant per period) == allocation_ledger`.
- M-Cp-7 (§6.6). Enabling an app for a tenant requires the tenant hold at least one healthy integration of each required compute class.

### Access management (§7)
- M-A-1 (§7.3). 7 roles ONLY: `platform_operator`, `tenant_owner`, `tenant_admin`, `data_steward`, `analyst`, `viewer`, `service`. *"Custom roles are recorded as requirements, not built."*
- M-A-2 (§7.4). *"Permissions are evaluated as action × resource_type × scope, deny-by-default. Evaluation happens at the API gateway and again inside the data plane."*
- M-A-3 (§7.5). *"A job cannot read a connector not listed on its task."*
- M-A-4 (§7.5). *"A job cannot use a connector at a higher mode than the task specifies or the connector permits."*
- M-A-5 (§7.5). *"Any change to a task's connectors, modes or compute invalidates its approval; the task returns to pending_approval."*
- M-A-6 (§7.2). Sessions: 12h absolute lifetime · 1h idle timeout · revocable by tenant admin. Data-plane agents auth via short-lived certs bound to `tenant_id`.
- M-A-7 (§7.7). Audit: append-only per tenant + one platform log. Retention = pilot + 12 months. Every event type in §7.7 must be emitted.
- M-A-8 (§7.8). Break-glass: stated reason · 2nd-operator approval · ≤4h · auto owner notification at open + close · flagged in both audit logs.

### Wizard (§8)
- M-W-1 (§8.1). Wizard produces a provisioned **sandbox** tenant and a **provisioning report**. Drafts saveable + resumable for 30 days.
- M-W-2 (§8.2). 9-step ordered wizard: Company → Identity → Estates → Connectors → Compute → Apps → Theme → Workspaces/Users → Review/Provision.
- M-W-3 (§8.3). Theme tokens fixed set: `logo_primary`, `logo_mark`, `colour_primary`, `colour_accent`, `mode ∈ {light, dark, user_choice}`, `display_name (≤40 chars)`, `login_message (≤200 chars)`, `email_sender_name`. Typography + layout + component geometry + iconography FIXED across tenants.

### App catalogue (§9)
- M-Ac-1 (§9). App fields: `app_id`, `name`, `version`, `required_connector_types` (with min-mode per type), `required_compute_classes`, `run_roles`, `view_roles`, `availability`.
- M-Ac-2 (§9). *"Enablement is validated against the tenant's connectors and compute integrations at enable time and re-validated when a connector is disabled or an integration goes offline; apps whose requirements lapse are marked degraded with the missing requirement named."*

## §4 · Control-plane data model — 16 entities (§10 verbatim)

```
tenant              (id, legal_name, short_name, jurisdiction, status, mou_ref, created_at)
workspace           (id, tenant_id, name, is_default)
user                (id, tenant_id, email, status, auth_method, mfa_enrolled, created_at)
role_assignment     (id, user_id, role, scope_type, scope_id, granted_by, granted_at)
service_account    (id, tenant_id, name, cert_fingerprint, expires_at)
estate              (id, tenant_id, name, tier, location_summary, estate_contact, agent_id, sandbox_safe)
connector           (id, tenant_id, estate_id, type, location, credential_ref, scope, mode, mou_task_ref, status)
compute_integration (id, tenant_id, kind, estate_id, class, capacity, agent_id, status)
allocation          (id, tenant_id, compute_integration_id, class, reserved, burst_ceiling,
                     hours_per_period, max_concurrent_jobs, environment, granted_by, granted_at, expires_at)
app                 (id, name, version, required_connector_types, required_compute_classes,
                     run_roles, view_roles, availability)
app_enablement      (id, tenant_id, app_id, status, enabled_by, enabled_at)
task                (id, tenant_id, workspace_id, mou_task_ref, objective, connector_modes,
                     compute_integration_id, status, approved_by, approved_at)
job                 (id, task_id, tenant_id, compute_integration_id, environment,
                     submitted_at, started_at, ended_at, status, metrics)
theme               (id, tenant_id, tokens, updated_by, updated_at)
audit_event         (id, tenant_id, actor_id, actor_type, action, resource_type, resource_id,
                     at, break_glass_session_id)
break_glass_session (id, tenant_id, operator_id, approver_id, reason, opened_at, expires_at, closed_at)
```

Note: `compute_integration.kind ∈ {central_allocation, tenant_provided}` per §10. For central allocations, `allocation` holds the terms; for tenant-provided, `capacity` + `agent_id` are populated on `compute_integration`.

## §5 · Pilot tenant register (§11)

| Tenant | Estates | Tier | Compute | Identity | Initial apps |
|---|---|---|---|---|---|
| **RMS** | Radio recordings (NAS); Broadcast systems (CAL, RMS Huawei) | Connected | Central `gpu_inference` for ASR + diarisation; tenant-provided compute registered if supplied | Native (SSO configurable) | Data census (discovery); Extraction (read · separate task) |
| **DigiCow** | Clinical/breeding records; app + USSD logs; training registers | Hosted | Central `cpu_general`; `gpu_inference` if audio workloads scoped | Native | Structured-data intelligence apps |
| **BDO** | Professional-services doc systems (M365 / SharePoint) | Connected | Central `cpu_general` | SSO via Entra ID | *capture at provisioning* |
| **Trinity** | *capture at provisioning* | *capture at provisioning* | *capture at provisioning* | *capture at provisioning* | *capture at provisioning* |

## §6 · Acceptance criteria (§12) — become CP-level acceptance tests

1. Each pilot tenant provisioned to sandbox through wizard with NO manual DB changes.
2. Cross-tenant access suite passes — no request/job/queue/storage/log/metric can reach another tenant.
3. Tenant with central allocation cannot list/observe/infer any other tenant's jobs/queue/utilisation/logs.
4. Job w/o compute_integration_id (or against one tenant doesn't hold, or against class it lacks) → rejected at submission with stated reason.
5. Discovery-mode connector returns no content; raising to read → logged approval + invalidates dependent tasks.
6. Job cannot use connector outside task list or above task mode.
7. Reserved never pre-empted; burst pre-empted by another tenant's reserved within SLA. — CONTRACT-MODELED.
8. Metering reconciles: `sum(gpu_seconds per tenant per period) == allocation ledger`.
9. Each tenant's users see only their own logo/colours/display-name/app-set.
10. Every audit event type in §7.7 emitted + visible to correct tenant admin.
11. Break-glass produces owner notification open+close + flagged trail in both audit logs.
12. Sandbox offboarding: metadata + Syni-hosted artefacts deleted · certs revoked · allocation returned.
13. Provisioning report lists estates/connectors+modes/compute+allocations/apps/workspaces/users; reconciles to MOU task refs.

---

## §7 · Proposed CP breakdown (M9 milestone)

Phase-to-CP mapping, thin-kernel disciplined, matching CP-M8-CSD-1's one-module / one-mechanism / ~7-invariants shape.

### P1 · Foundation: control-plane data model + tenancy core + isolation invariants
| CP | Module | Mechanism | Invariants |
|---|---|---|--:|
| **P1-CP1 · TENANT-CONTEXT-ENFORCEMENT** *(this-turn build)* | `services/platform_control_plane/tenant_context.py` | Preventive-charter refusal on client-supplied tenant_id / missing tenant_id / cross-tenant resource. Foundation isolation invariant for every downstream CP. | 7 |
| P1-CP2 · TENANT-ENTITY | `services/platform_control_plane/tenant_entity.py` | Frozen carrier for `tenant` record; owner-ratified lifecycle enum values as OPEN str refs. | ~7 |
| P1-CP3 · TENANT-LIFECYCLE-FSM | `services/platform_control_plane/tenant_lifecycle.py` | Refusal on illegal state transitions (provisioning→sandbox_active→production_active→suspended→offboarded); irreversible offboarded state; effects (sessions revoked, jobs halted, allocations released) recorded as effect refs, not enforced runtime. | ~7 |
| P1-CP4 · WORKSPACE-ENTITY | `services/platform_control_plane/workspace_entity.py` | Frozen `workspace` carrier + refusal when tenant has zero workspaces on provision. | ~5 |
| P1-CP5 · CONTROL-PLANE-PERSISTENCE-CONTRACT | `services/platform_control_plane/persistence_contract.py` | Atomic JSON write refusal wrapper reusing `services/artifact_store/atomic_write.py`; contract is metadata-only per §4.1. | ~6 |

### P2 · RBAC (deny-by-default) + session + break-glass
| CP | Module | Mechanism |
|---|---|---|
| P2-CP1 · ROLE-ENUM-REGISTRY | `services/platform_control_plane/role_registry.py` | Fixed 7-role registry as OPEN str refs; refusal on unknown role. |
| P2-CP2 · ROLE-ASSIGNMENT | `services/platform_control_plane/role_assignment.py` | Frozen carrier + granter/grantee refusal semantics. |
| P2-CP3 · PERMISSION-EVALUATION | `services/platform_control_plane/permission_evaluation.py` | `assess_permission_grant(action, resource_type, scope, assignments) → allow_ref | deny_ref` deny-by-default. |
| P2-CP4 · SESSION-BINDER | `services/platform_control_plane/session_binder.py` | Session→tenant_id binding contract; refusal on unbound/expired. Absolute 12h · idle 1h. |
| P2-CP5 · BREAK-GLASS-SESSION | `services/platform_control_plane/break_glass_session.py` | Frozen `break_glass_session` carrier + refusal on missing reason / 2nd-approver / >4h duration / missing owner-notification-refs. |

### P3 · Estate + connector modes + connection test + mode-change approval
| CP | Module | Mechanism |
|---|---|---|
| P3-CP1 · ESTATE-ENTITY | `services/platform_control_plane/estate_entity.py` | Frozen carrier; refusal on unknown tier (connected/hosted); sandbox_safe rule. |
| P3-CP2 · CONNECTOR-ENTITY | `services/platform_control_plane/connector_entity.py` | Frozen carrier with 10 fields; empty-scope refusal; mou_task_ref required. |
| P3-CP3 · CONNECTOR-MODE-LATTICE | `services/platform_control_plane/connector_mode_lattice.py` | 3-mode partial order (discovery < read < write); refusal on downgrade-only-permitted invariants. |
| P3-CP4 · CONNECTOR-MODE-CHANGE-APPROVAL | `services/platform_control_plane/mode_change_approval.py` | Refusal on missing approver-with-role + missing log-ref + missing dependent-task-invalidation set. |
| P3-CP5 · CONNECTION-TEST-CONTRACT | `services/platform_control_plane/connection_test.py` | Refusal on any content-read attempt during test; positive outcome refuses when reachability/auth/scope-resolution missing. |

### P4 · Task-scoped access + compute integration + allocation + scheduler admission + metering
| CP | Module | Mechanism |
|---|---|---|
| P4-CP1 · COMPUTE-INTEGRATION-ENTITY | `services/platform_control_plane/compute_integration.py` | Frozen carrier; kind ∈ {central_allocation, tenant_provided} as OPEN str. |
| P4-CP2 · ALLOCATION-ENTITY | `services/platform_control_plane/allocation_entity.py` | Frozen carrier w/ 12 fields; env ∈ {sandbox, production} OPEN str. |
| P4-CP3 · TASK-ENTITY | `services/platform_control_plane/task_entity.py` | Frozen carrier + connector_modes as tuple of `(connector_id, mode)` OPEN pairs. |
| P4-CP4 · TASK-SCOPE-ENFORCEMENT | `services/platform_control_plane/task_scope_enforcement.py` | Refusal when job requests connector not on task or mode above task's spec. |
| P4-CP5 · TASK-APPROVAL-INVALIDATION | `services/platform_control_plane/task_invalidation.py` | Refusal on task-approved-state when connectors/modes/compute change without re-approval. |
| P4-CP6 · SCHEDULER-ADMISSION | `services/platform_control_plane/scheduler_admission.py` | Refusal on: no compute_integration_id · wrong tenant · wrong class · exceeds reservation/burst/hours/concurrency. |
| P4-CP7 · METERING-LEDGER | `services/platform_control_plane/metering_ledger.py` | Reconciliation invariant `sum(gpu_seconds per tenant per period) == allocation_ledger`. |
| P4-CP8 · PREEMPTION-CONTRACT | `services/platform_control_plane/preemption_contract.py` | CONTRACT-MODELED · refusal on preempting a reserved job; permits preempting burst with reserved. |

### P5 · App catalogue + enablement + onboarding wizard + provisioning report + theme
| CP | Module | Mechanism |
|---|---|---|
| P5-CP1 · APP-ENTITY | `services/platform_control_plane/app_entity.py` | Frozen carrier w/ 8 fields. |
| P5-CP2 · APP-ENABLEMENT | `services/platform_control_plane/app_enablement.py` | Frozen carrier + refusal when required connector types/modes/classes not held. |
| P5-CP3 · APP-REQUIREMENT-REVALIDATION | `services/platform_control_plane/app_revalidation.py` | Marks enabled apps degraded when connector disabled or integration offline. |
| P5-CP4 · WIZARD-STATE-MACHINE | `services/platform_control_plane/wizard_state_machine.py` | 9-step ordered progression; save/resume-30d contract; sandbox-only output. |
| P5-CP5 · PROVISIONING-REPORT | `services/platform_control_plane/provisioning_report.py` | Refusal on missing sub-list (estates/connectors/compute/apps/workspaces/users) or missing mou_task_ref reconciliation. |
| P5-CP6 · THEME-ENTITY | `services/platform_control_plane/theme_entity.py` | Fixed 8-token set; refusal on unknown token / oversized-logo (>512KB) / >40-char display_name / >200-char login_message. WCAG-AA-refusal CONTRACT-MODELED. |

### P6 · Audit + cross-tenant access acceptance suite + pilot tenant register + sandbox offboarding
| CP | Module | Mechanism |
|---|---|---|
| P6-CP1 · AUDIT-EVENT-ENTITY | `services/platform_control_plane/audit_event.py` | Frozen carrier + append-only refusal on mutate/delete. |
| P6-CP2 · AUDIT-EVENT-TYPES | `services/platform_control_plane/audit_event_types.py` | Refusal when the emitted-event-types set is not a superset of the §7.7 required set. |
| P6-CP3 · CROSS-TENANT-ACCESS-SUITE | `services/platform_control_plane/cross_tenant_access_suite.py` | Refusal aggregator: joins tenant_context, task_scope, permission_evaluation, scheduler_admission, metering, audit visibility. |
| P6-CP4 · PILOT-TENANT-REGISTER | `services/platform_control_plane/pilot_tenant_register.py` | RMS · DigiCow · BDO · Trinity records; refusal on missing capture-at-provisioning where marked. |
| P6-CP5 · SANDBOX-OFFBOARDING | `services/platform_control_plane/sandbox_offboarding.py` | 30-day irreversible-delete contract; refusal on missing cert-revocation / allocation-return / artefact-delete evidence refs. |
| P6-CP6 · M9-SEAL | wave-close report `notes/M9_SEAL_YYYYMMDD.md` | Inline OVERALL BUILD STATUS table per owner directive. |

**Estimated ratchet growth for M9:** 5+5+5+8+6+6 ≈ **35 CPs × ~6 invariants = ~210 new passing invariants** across the milestone. Ratchet floor is expected to move from **4433 → ~4640** over the M9 walk.

---

## §8 · CONTRACT-MODELED vs REAL infra items

For every acceptance-criterion / mandate that depends on infrastructure **not present in this pod**, the SOFTWARE CONTRACT + invariant is built, but real-infra verification is DEFERRED. Every such item labelled **CONTRACT-MODELED (verify-on-real-infra)** in the seal note. **Do NOT silently mock.**

| # | Item | Depends on infra | Software contract this session | Real-infra verify path |
|--:|---|---|---|---|
| 1 | Per-tenant Kubernetes namespace isolation (§6.4 M-Cp-3) | K8s cluster with namespace-scoped RBAC + NetworkPolicy | `scheduler_admission.py` refuses when execution-context ref does not carry tenant-scoped namespace ref | Deploy to K8s cluster with per-tenant `Namespace` + `NetworkPolicy default-deny` + verify with cross-namespace-traffic test |
| 2 | Per-tenant GPU MIG partition / taints (§6.4 M-Cp-3) | Nvidia GPU + MIG-enabled node + Kubernetes device-plugin | `scheduler_admission.py` refuses when GPU partition ref does not carry tenant scope | Configure MIG on real GPU + assert isolation via `nvidia-smi mig list` per-tenant |
| 3 | Network policy default-deny cross-namespace (§6.4 M-Cp-3) | K8s NetworkPolicy CNI (Calico/Cilium) | `scheduler_admission.py` refuses on missing network_policy_ref | Apply `NetworkPolicy` object; verify cross-namespace `curl` blocked |
| 4 | Reserved-never-preempted / burst-preemptible-within-SLA (§6.4 M-Cp-4) | Scheduler runtime (K8s + custom controller) | `preemption_contract.py` (P4-CP8) — refusal on invalid transitions | Live scheduler pre-emption test with two tenants |
| 5 | Live OIDC / SAML SSO per tenant (§7.2 M-A-6) | Real IdP (Entra ID / Google Workspace / Okta) | `session_binder.py` refuses on unsigned session claim; auth_method OPEN str | Wire real IdP + verify JIT session-to-tenant_id resolution |
| 6 | Data-plane agent cert issuance (§7.2, §4.5) | Real PKI + certificate authority | `service_account` frozen carrier + expiration refusal | Real cert issuance + tenant_id binding via SAN/CN validation |
| 7 | Real 12-hour absolute / 1-hour idle session lifecycle (§7.2) | Session store (Redis/DB) | `session_binder.py` refusal on ttl > 12h / idle > 1h | Wire real session store + wall-clock test |
| 8 | Break-glass owner notification via email/webhook (§7.8 M-A-8) | Email / webhook service | `break_glass_session.py` refusal on missing notification refs at open+close | Real webhook + delivery-receipt test |
| 9 | WCAG-AA contrast check for `colour_primary` (§8.3) | Colour-contrast library / real render | `theme_entity.py` refusal on missing contrast_verify_ref | Real render + WCAG-AA measurement library |
| 10 | Envelope-encryption per-tenant secret store (§4.5) | KMS / HSM | `service_account` refuses on missing envelope_key_ref | Real KMS + envelope-encryption round-trip |
| 11 | Audit log append-only durability (§7.7) | Append-only store (S3-object-lock / immutable DB) | `audit_event.py` frozen carrier + `audit_event_types.py` refusal | Real append-only store + attempt-mutate test |
| 12 | 30-day irreversible offboarding delete (§4.7) | Real storage + wall-clock scheduler | `sandbox_offboarding.py` refusal on missing evidence refs | Wall-clock verification + storage-object-list-after-delete assertion |
| 13 | Cross-tenant access suite runs on every deploy (§4.3 M-H-6) | CI/CD pipeline | `cross_tenant_access_suite.py` aggregator can be run in-CI locally | Wire into deploy pipeline · block release on failure |
| 14 | Real connector runtime enforcing mode (§5.3 M-C-3) | Data-plane connector agents | `connector_mode_lattice.py` + `mode_change_approval.py` refusal contracts | Wire into real connector runtime (data-plane); verify write-attempt on read-mode connector refuses |
| 15 | Storage namespaced by tenant_id at bucket/prefix/schema (§4.3 M-H-3) | Real object store + DB schema | `tenant_context.py` (P1-CP1) refusal on storage_path_ref not tenant-prefixed | Real bucket + prefix / schema policy verification |

**Discipline:** every module built under this milestone that touches a CONTRACT-MODELED item MUST expose the invariant such that real-infra wiring becomes a bind-only change (no refactor). The `_ref: str` (OPEN str) pattern from CP-M8-CSD-1 is exactly the correct shape.

---

## §9 · Provenance

- Source doc: fetched 2026-09-17 from `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/fs5op6ny_Akki%20OS%20Pilot%20-%20Platform%20Reference%20v0.2.docx` — parsed successfully.
- Ingest turn: 2026-09-17.
- New home under services: `services/platform_control_plane/` (created by CP-P1-CP1 this turn · POST-2 discipline: home selected where no peer exists — new-home permitted since the doc's own §4.1 language is *"Control plane"* and no existing services/ sub-tree owns platform-control semantics).
- All standing disciplines from `STATE/STANDING_ORDERS.md` apply unchanged.

*End of requirements pack.*
