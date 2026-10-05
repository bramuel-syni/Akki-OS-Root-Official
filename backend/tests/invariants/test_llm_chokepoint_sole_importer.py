"""AST negative scan: `services/chokepoint/llm.py` is the sole importer of any LLM SDK and the sole constructor of an external client.
Restored on 2026-10-05 (WP-A5) — the W5 scan this module's docstring cites was no longer on disk."""
import ast
import sys
from pathlib import Path

ROOT = Path('/app/backend/vendored/extraction_akki/backend')
CHOKEPOINT = ROOT / 'services' / 'chokepoint' / 'llm.py'
SDK_ROOTS = ('emergentintegrations', 'openai', 'anthropic', 'google.genai', 'google.generativeai', 'litellm')
SKIP_PARTS = {'tests', 'tools', '__pycache__', 'node_modules', '.venv'}


def _imports(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names: yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module


def sdk_importers():
    """Every backend module (outside tests/tools) that imports an LLM SDK, except the chokepoint itself."""
    offenders = []
    for path in ROOT.rglob('*.py'):
        if SKIP_PARTS & set(path.parts) or path == CHOKEPOINT: continue
        try: tree = ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as exc: offenders.append((str(path.relative_to(ROOT)), f'unparseable: {exc}')); continue
        for mod in _imports(tree):
            if any(mod == r or mod.startswith(r + '.') for r in SDK_ROOTS): offenders.append((str(path.relative_to(ROOT)), mod))
    return offenders


def test_only_chokepoint_llm_may_import_llm_sdks():
    assert CHOKEPOINT.exists()
    assert sdk_importers() == []


def test_chokepoint_itself_imports_an_sdk_so_the_scan_is_not_vacuous():
    mods = set(_imports(ast.parse(CHOKEPOINT.read_text())))
    assert any(any(m == r or m.startswith(r + '.') for r in SDK_ROOTS) for m in mods), sorted(mods)


def test_scan_detects_a_planted_offender(tmp_path, monkeypatch):
    planted = ROOT / 'services' / '_sole_importer_probe_SYNTHETIC.py'
    planted.write_text('import openai\n')
    try: assert ('services/_sole_importer_probe_SYNTHETIC.py', 'openai') in sdk_importers()
    finally: planted.unlink()


if __name__ == '__main__':
    bad = sdk_importers(); print(bad or 'sole importer green'); sys.exit(1 if bad else 0)
