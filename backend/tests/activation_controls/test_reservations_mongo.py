"""Real Mongo CAS on a unique SYNTHETIC test tenant, NOT live owner permission.

No accounts/credentials/keys installed, no sources/SSH. Append-only evidence is
retained; the generated test resolver exists only within this pytest process.
"""
import asyncio
from uuid import uuid4
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from test_native_control_ledger import Keys, scope, prepare, request
from services.activation.receipts import NativeReceipts
from services.activation.reservations import Reservations
from services.watch.signature_primitive import watch_sign
from services.northena.execution_models import Held


def test_real_mongo_cross_client_reservations_do_not_oversubscribe():
    async def run():
        env=dotenv_values('/app/backend/.env')
        first_client=AsyncIOMotorClient(env['MONGO_URL'])
        second_client=AsyncIOMotorClient(env['MONGO_URL'])
        tenant='TEST-SYNTHETIC-activation-'+uuid4().hex
        class TestKeys(Keys):
            def receipt(self,*args,**kwargs):
                original=super().receipt(*args,**kwargs).model_copy(update={'tenant_id':tenant})
                return original.model_copy(update={'signature_hex':watch_sign(self.private,original.signing_bytes()).hex()})
        keys=TestKeys()
        r1=NativeReceipts(first_client[env['DB_NAME']],keys,timeout_seconds=5,clock=lambda:keys.now)
        r2=NativeReceipts(second_client[env['DB_NAME']],keys,timeout_seconds=5,clock=lambda:keys.now)
        try:
            with scope(tenant=tenant):
                a,ar,_=await prepare((keys,r1,None),request('one').model_copy(update={'tenant_id':tenant}))
                b,br,_=await prepare((keys,r1,None),request('two').model_copy(update={'tenant_id':tenant}),allocation_ref=a.allocation_ref)
                results=await asyncio.gather(Reservations(r1).reserve(a,ar),Reservations(r2).reserve(b,br),return_exceptions=True)
                assert sum(isinstance(v,str) for v in results)==1,results
                assert sum(isinstance(v,Held) and v.reason_code=='ALLOCATION_CAPACITY_EXCEEDED' for v in results)==1,results
                rows=await r2.events()
                assert sum(e['row']['event_type']=='activation.reserved' for e in rows)==1
                print('SYNTHETIC_TEST_TENANT',tenant,'REAL_MONGO_EVENTS',len(rows))
        finally:
            first_client.close();second_client.close()
    asyncio.run(run())