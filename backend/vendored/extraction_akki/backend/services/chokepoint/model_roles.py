"""Task-strength model assignment (owner order 2026-10-02): every LLM-shaped role names the model family best measured for its
job, planners and reviewers come from different families, and the writer keeps the model whose evidence-grounded prose has
passed the content manager. Configuration is environment-only; the chokepoint reads the role from the purpose. No fallback."""
import os

ROLES = {
    'assistant': {'env': 'TRAINING_LAB', 'job': 'planning collaborator in Train Models: reads the run record, plans the next bounded step, proposes one action',
                  'strength': 'long-horizon planning and orchestration; strict JSON; grounded figures'},
    'planner': {'env': 'PLANNER', 'job': 'plans and orchestrates multi-step work (document story, measurement order, task decomposition)',
                'strength': 'planning and orchestration across tools and steps'},
    'reviewer': {'env': 'REVIEWER', 'job': 'independent review of complex outputs against source evidence and acceptance criteria; a different family from the planner',
                 'strength': 'complex-task reasoning, error detection, disagreement stated plainly'},
    'writer': {'env': 'REPORT_AUTHOR', 'job': 'writes every sentence the reader sees from evidence tokens under the content-manager gate',
               'strength': 'evidence-grounded British-English prose that passes the figure-by-reference gate'},
}
ROLE_BY_PURPOSE = {'training_lab.conversation': 'assistant', 'training_lab.advisory_review': 'reviewer', 'doc_studio.author': 'writer',
                   'doc_studio.review': 'reviewer', 'doc_studio.plan': 'planner', 'census.estate_intelligence_dossier': 'writer'}
EVALUATION = {'date': '2026-10-02', 'basis': 'integration model catalogue plus published task benchmarks reviewed on the day; planner/reviewer families kept distinct so the review does not share the planner\'s blind spots',
              'not_claimed': 'no independent head-to-head benchmark was run on owner data; assignments are disclosed configuration, re-evaluated when a role under-performs on its own gate'}


def resolve(role):
    spec = ROLES[role]
    return {'role': role, 'connection': os.environ[f"{spec['env']}_CONNECTION"], 'sdk_provider': os.environ[f"{spec['env']}_MODEL_PROVIDER"], 'model': os.environ[f"{spec['env']}_MODEL"],
            'job': spec['job'], 'strength': spec['strength']}


def for_purpose(purpose):
    role = ROLE_BY_PURPOSE.get(purpose)
    return resolve(role) if role else None


def assignments():
    """The published assignment table: role, model, family, job description, strength and evaluation disclosure."""
    rows = [resolve(role) for role in ROLES]
    families = {r['role']: r['sdk_provider'] for r in rows}
    return {'roles': rows, 'planner_reviewer_distinct_families': families['planner'] != families['reviewer'] and families['assistant'] != families['reviewer'],
            'evaluation': EVALUATION, 'shield': 'every call crosses the sole chokepoint: purpose gate, credential scrub, masking tier, allowlisted endpoint, de-identification, Watch input seat, crossing receipt'}
