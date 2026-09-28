"""RDS compatibility entry point; estate SDK execution lives on external workers."""
from services.census_autonomy.deep_dispatch import execute_source

__all__ = ['execute_source']