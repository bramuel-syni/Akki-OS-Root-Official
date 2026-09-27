# Component binding verification — RED output (iteration 29)

- Scope: corrected RED harness only (no runtime/API/UI implementation edits).
- Command:

```bash
pytest /app/backend/tests/execution_components -v --tb=short --junitxml=/app/test_reports/pytest/pytest_execution_components_red_iteration29.xml
```

- Result: **13 failed / 1 passed (14 total)**.

## Harness corrections landed before implementation

1. Authority RED fixtures now require bound `principal_context` + `bind_control_scope` for positive prepare paths.
2. Authority resolved view fixture now includes realistic `LicenceAllowanceState` with `period_iso`.
3. Added explicit missing-context negative test for authority prepare.
4. Registry worker result now binds `request_sha256=request.digest()` and operation key consistently.
5. Registry isolated fault fixture now uses synthetic valid typed authority context (`PrincipalV1`, `LicencePortalView`) to avoid pre-commit false-pass paths.
6. Registry commit-failure test asserts specific `registry commit failure` and confirms zero writer calls before any registry slot persistence.
7. Fake journal semantics now enforce idempotent replay and `CommandConflict` on same-slot changed payload.

## Remaining RED blockers (implementation)

1. Missing module: `services.northena.execution_component_models`
2. Missing module: `services.northena.execution_authority`
3. Missing module: `services.mtafiti.execution_record_models`
4. Missing module: `services.mtafiti.execution_registry`
5. Missing module: `services.northena.execution_usage`
6. Missing module: `services.northena.execution_bindings`
7. `services.northena.execution_coordinator.Coordinator.__init__` missing `usage_publisher` parameter

## Evidence

- JUnit XML: `/app/test_reports/pytest/pytest_execution_components_red_iteration29.xml`
- Iteration report: `/app/test_reports/iteration_29.json`
