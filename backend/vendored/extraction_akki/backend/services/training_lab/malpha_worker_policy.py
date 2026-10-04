"""Pure, independently testable worker rules. No provider, database or GPU dependency."""
import math

LANGUAGES = ('kik', 'kam', 'swa')


def story_score(ev):
    """Worst language first. Perplexity is a tie-break, never hides failed fidelity."""
    per = ev.get('per_language') or {}
    if any(l not in per for l in LANGUAGES): return None
    fidelity = [per[l].get('language_fidelity_rate') for l in LANGUAGES]
    ppl = [per[l].get('dev_perplexity') for l in LANGUAGES]
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in fidelity + ppl): return None
    if any(v <= 0 for v in ppl): return None
    bases = [per[l].get('base_perplexity') for l in LANGUAGES]
    below_base = all(type(b) in (int, float) and math.isfinite(b) and 0 < p < b for p, b in zip(ppl, bases))
    return (int(below_base), min(fidelity), sum(fidelity), -math.exp(sum(math.log(v) for v in ppl) / len(ppl)))


def rendered_identity_gate(cosines, *, prompts, rendered, comparators, threshold=0.40, comparator_coverage_complete=True):
    """A missing, short or nonfinite rendering cannot be averaged out of a pass."""
    complete = prompts > 0 and rendered == prompts and len(cosines) == prompts and comparators > 0 and comparator_coverage_complete
    finite = all(type(c) in (int, float) and math.isfinite(c) for c in cosines)
    maximum = max(cosines) if cosines and finite else None
    return {'comparators': comparators, 'threshold_cosine': threshold, 'prompts': prompts,
            'rendered': rendered, 'evaluated': len(cosines), 'coverage_complete': complete,
            'max_cosine_to_any_corpus_speaker': round(maximum, 4) if maximum is not None else None,
            'mean_max_cosine': round(sum(cosines) / len(cosines), 4) if cosines and finite else None,
            'passes': bool(complete and finite and 0 < threshold <= 0.40 and maximum < threshold),
            'scope': 'all available train/dev corpus groups across commissioned languages; sealed admission excluded; not global human uniqueness'}


def balanced_weights(rows, weights=None):
    """Equal total probability for each language; retain within-language curricula."""
    values = list(weights) if weights is not None else [1.0] * len(rows)
    totals = {l: sum(values[i] for i, r in enumerate(rows) if r['language'] == l) for l in LANGUAGES}
    if any(v <= 0 for v in totals.values()): raise ValueError('Missing qualified training language')
    return [values[i] / totals[r['language']] for i, r in enumerate(rows)]