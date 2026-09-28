"""services.chat — the governed chat surface (W5 CP4).

POST /api/chat/ask · one Q / one A · every submit transits the LLM
chokepoint with purpose=chat.governed_answer, masking_tier=
llm_prompt_governed_text.

Refusals surface verbatim per A8-Q3 (owner sharpening §4).
"""
