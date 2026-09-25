"""Composition entry point for the already owner-required persistent supervisor worker."""
import os
from dotenv import load_dotenv

load_dotenv(os.environ["AKKI_CONFIG_ENV_FILE"])

from services.census_autonomy.scheduler_program import main

if __name__ == "__main__":
    raise SystemExit(main())