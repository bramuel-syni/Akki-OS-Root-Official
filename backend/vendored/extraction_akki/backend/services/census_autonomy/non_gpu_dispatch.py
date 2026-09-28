"""Compatibility entry point; a local subprocess is not an external worker.

Uses the same admitted-source dispatcher and existing durable commission.
"""
from services.census_autonomy.deep_dispatch import execute_source

__all__ = ['execute_source']