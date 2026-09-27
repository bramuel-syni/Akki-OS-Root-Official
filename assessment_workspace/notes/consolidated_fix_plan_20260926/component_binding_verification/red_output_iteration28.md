# Component binding verification — RED output (iteration 28)

- Scope: architecture-first RED suite only (no runtime/API/UI execution).
- Command:

```bash
pytest /app/backend/tests/execution_components -v --tb=short --junitxml=/app/test_reports/pytest/pytest_execution_components_red_iteration28.xml
```

- Result: **11 failed / 11 total** (expected RED state).

## Failure summary

1. Missing module: `services.northena.execution_component_models`
2. Missing module: `services.northena.execution_authority`
3. Missing module: `services.mtafiti.execution_record_models`
4. Missing module: `services.mtafiti.execution_registry`
5. Missing module: `services.northena.execution_usage`
6. Missing module: `services.northena.execution_bindings`
7. `services.northena.execution_coordinator.Coordinator.__init__` missing `usage_publisher` extension parameter

## Evidence

- JUnit XML: `/app/test_reports/pytest/pytest_execution_components_red_iteration28.xml`
