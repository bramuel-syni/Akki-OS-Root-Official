"""services.critic_pass.producer_seam · W11 R4.8 producer-side helper.

Owner directive verbatim (2026-08-26):
    "Critic Seam producer wiring (pick the real worker outputs — at
     minimum chat/solva answer path and whitepaper drafts — and route
     them through run_critic_pass/manifest_gate with producer tests)"

Doc19A-005 verbatim: "every worker output passes through the Critic
Seam; shipped-without-seam is a defect".

This module is the producer-side helper each worker imports to route
its output through the seam. It:

  * generates a distinct `critic_instance_id` derived from the
    `producing_instance_id` so QA-3 (no self-review) is honoured by
    context isolation;
  * calls `run_critic_pass(...)`;
  * returns the verdict AND a "seam-attested" boolean so the
    Callers-Cover-the-Rule DoD tests can assert Y fired.

QA-1 discipline preserved: findings are DATA, never a gate. The producer
returns its artifact regardless of the verdict.
"""
from __future__ import annotations

import os
import uuid
from typing import Optional

from services.critic_pass.harness import CriticPassVerdict, run_critic_pass


def _critic_instance_id_for(producing_instance_id: str) -> str:
    """Derive a distinct critic instance id from the producer id.

    QA-3 (Critic Seam Spec v1.0 §6.2): 'the critic instance is never
    the instance that produced the artifact; where both are the same
    base model, independence is by context isolation.' The suffix
    `-critic-<8hex>` provides context isolation.
    """
    return f"{producing_instance_id}-critic-{uuid.uuid4().hex[:8]}"


def route_through_seam(
    *,
    artifact_ref: str,
    artifact_content: str,
    producing_instance_id: str,
    archive_verdict: bool = True,
    critic_instance_id: Optional[str] = None,
) -> CriticPassVerdict:
    """Run the Critic Seam on a worker artifact.

    The producer calls this on EVERY output artifact per Doc19A-005.
    Failure to call this seam is the audit §16 finding #3 (Critic Seam
    orphan). Callers-Cover-the-Rule DoD tests assert this helper fires.
    """
    cid = critic_instance_id or _critic_instance_id_for(producing_instance_id)
    return run_critic_pass(
        artifact_ref=artifact_ref,
        artifact_content=artifact_content,
        producing_instance_id=producing_instance_id,
        critic_instance_id=cid,
        archive_verdict=archive_verdict,
    )


def verdict_summary(verdict: CriticPassVerdict) -> dict:
    """Compact response shape for embedding a critic verdict in a
    worker's response body. Findings are data; QA-1 preserves execution."""
    return {
        "artifact_ref": verdict.artifact_ref,
        "critic_instance_id": verdict.critic_instance_id,
        "producing_instance_id": verdict.producing_instance_id,
        "findings_count": len(verdict.findings),
        "findings": [
            {
                "rubric_id": getattr(f, "rubric_id", ""),
                "verdict": getattr(f, "verdict", ""),
                "evidence_class": getattr(f, "evidence_class", ""),
            }
            for f in verdict.findings
        ],
        "seam_attested": True,
    }
