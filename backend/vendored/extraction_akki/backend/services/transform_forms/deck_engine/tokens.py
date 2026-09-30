"""DR-R8 token sets: versioned artefacts extracted from the frontend file of record (frontend/src/App.css) — every style
constant lives here and nowhere else in the engine. Registers are token themes + density parameters; plates read tokens only."""

TOKEN_SETS = {
    "v1": {
        "source": "frontend/src/App.css",
        "source_sha256_at_extraction": "see frontend/src/App.css :root block — values copied verbatim 2026-09-30",
        "colour": {"paper": "#f5f2ea", "surface": "#f0ece1", "surface2": "#ede8da", "line": "#e4dfd3", "ink": "#1b1f27", "ink2": "#3d4350",
                   "ink3": "#5b6270", "sage": "#1d7a6e", "brass": "#b08d2e", "oxblood": "#b8395b", "blue": "#16274a", "white": "#ffffff"},
        "font": {"head": "'Iowan Old Style', Georgia, serif", "body": "'Söhne', 'Helvetica Neue', Arial, sans-serif", "mono": "ui-monospace, Menlo, Consolas, monospace"},
        "status": {"measured": "sage", "estimated": "brass", "sample": "oxblood", "unmeasured": "ink3"},
        "ramp": ["#1d7a6e", "#16274a", "#b08d2e", "#5b6270", "#b8395b", "#3d4350"],
        "divider": "1px solid #e4dfd3",
        "hatch": {"stroke": "#b8b0a0", "gap": 6},
    }
}

# Register = density parameters over one token set (DR-R8). Values are engine constants, versioned with ENGINE_VERSION.
REGISTERS = {
    "R1": {"name": "Board brief", "slide_w": 1280, "slide_h": 720, "title_px": 40, "body_px": 20, "kicker_px": 13, "max_body_slides": 8, "title_chars_per_line": 46},
    "R2": {"name": "Compliance export", "slide_w": 1280, "slide_h": 720, "title_px": 32, "body_px": 17, "kicker_px": 12, "max_body_slides": 20, "title_chars_per_line": 58},
    "R3": {"name": "Working deck", "slide_w": 1280, "slide_h": 720, "title_px": 34, "body_px": 18, "kicker_px": 12, "max_body_slides": 14, "title_chars_per_line": 54},
    "R4": {"name": "Commission close", "slide_w": 1280, "slide_h": 720, "title_px": 36, "body_px": 18, "kicker_px": 12, "max_body_slides": 12, "title_chars_per_line": 50},
    "R5": {"name": "Run status", "slide_w": 1280, "slide_h": 720, "title_px": 30, "body_px": 16, "kicker_px": 11, "max_body_slides": 6, "title_chars_per_line": 62},
}

DEFAULT_REGISTER = "R3"  # owner slot O-D1 default (DISCLOSED, not ratified)
LIVE_MOTION = False  # owner slot O-D2 default: off in v1
