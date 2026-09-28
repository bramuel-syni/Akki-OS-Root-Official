"""Census source router — routes each admitted source to its execution driver.

Different estates use different admitted runtimes:
  rms_mysql   -> jump server (or local non-GPU worker) — env AKKI_CENSUS_EXECUTION_MODE
  digicow_rds -> AWS RDS Data API
  rms_obs     -> Huawei OBS inventory
Anything else falls back to the GPU remote_dispatch (default).
The pod never opens a raw source socket for rms_mysql (that runs on the jump);
managed-API sources (rds_data, obs) are read via their HTTPS endpoints.
"""
import os


def _rms_mysql():
    mode = os.environ.get("AKKI_CENSUS_EXECUTION_MODE")
    if mode == "non_gpu_jump":
        from services.census_autonomy.jump_dispatch import execute_source
    elif mode == "non_gpu_worker":
        from services.census_autonomy.non_gpu_dispatch import execute_source
    else:
        from services.census_autonomy.remote_dispatch import execute_source
    return execute_source


def _driver_for(source):
    if source == "rms_mysql":
        return _rms_mysql()
    if source == "digicow_rds":
        from services.census_autonomy.rds_data_dispatch import execute_source
        return execute_source
    if source == "rms_obs":
        from services.census_autonomy.obs_dispatch import execute_source
        return execute_source
    from services.census_autonomy.remote_dispatch import execute_source
    return execute_source


def execute_source(run_id, tenant, source, lawful_hash, deadline):
    # Every source, including managed HTTPS APIs, executes outside this pod.
    from services.census_autonomy.deep_dispatch import execute_source as external_execute
    return external_execute(run_id, tenant, source, lawful_hash, deadline)
