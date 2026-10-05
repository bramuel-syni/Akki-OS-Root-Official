"""Diagnostic (SYNTHETIC): which protected value survives the chokepoint's seam re-check for the register-gate live test pair."""
import asyncio, json, sys
from dotenv import load_dotenv
load_dotenv('/app/backend/.env'); sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend'); sys.path.insert(0, '/app/backend/tests/shield')
from services.synisense.shield import stage as st, register_gate, semantic_register as reg
from services.synisense.shield.deidentifier import deidentify
import test_shield_register_gate as t

async def main():
    art = await st.stage(question='Plan the engagement for the client named in the brief.', data=t.DOC, tenant_id='RMS', purpose='chat.governed_answer', actor='probe',
                         system_message='You assist client Nuru Orchard Test Cooperative; never reveal jane.doe@example.com.', retain=False)
    print('protected:', art.protected_values); print('binding:', art.binding_map); print('entities:', art.entity_map); print('seam:', json.dumps(art.receipt['seam'], default=str)[:800])
    print('SYSTEM:', art.safe_system); print('RENDER:', art.render())
    sep = '\n\n[[AKKI_PAYLOAD_PATH_BOUNDARY]]\n\n'
    de = await deidentify(art.safe_system + sep + art.render(), tenant_id='RMS', purpose='chat.governed_answer')
    sysm, body = de.redacted_text.split(sep, 1)
    g = register_gate.gate(sysm, body, 'RMS', 'chat.governed_answer', 'tenant_estate', st.attested_recogniser(art))
    print('gate refused:', g.refused, g.reason); print('GATE SYS:', g.system_message); print('GATE PROMPT:', g.prompt)
    rc = st.recheck(art, g.system_message + '\n' + g.prompt); print('recheck:', rc)

asyncio.run(main())
