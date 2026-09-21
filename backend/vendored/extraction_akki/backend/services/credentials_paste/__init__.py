"""services.credentials_paste — deterministic-only paste → fields parser.

Owner Simplification Ruling 2026-08-14 (DECISIONS.md · lines 492-508):
  Connect collapses to ONE paste panel. Parsing is pattern-only, in-process.
  Pasted credential text NEVER transits an LLM, external API, or synisense.
  Password is env-grade only inside the seven-stage pipeline call; the parse
  endpoint's response NEVER carries the password back — only a boolean
  `password_captured` signal (Owner Q2 addendum, this cycle).
"""
