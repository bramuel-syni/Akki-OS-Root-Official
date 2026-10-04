"""Iter 84 — CaaS client-side (X-CaaS-Key) backend checks."""
import json, requests

BE = "https://pensive-goodall-6.preview.emergentagent.com"
state = json.load(open("/tmp/caas_state.json"))
SECRET = state["secret"]
H = {"X-CaaS-Key": SECRET}

def _p(label, r):
    try:
        body = r.json()
    except Exception:
        body = r.text[:200]
    print(f"{label}: {r.status_code} :: {str(body)[:400]}")
    return body

r = requests.get(f"{BE}/api/caas/client/licence", headers=H)
lic = _p("GET /api/caas/client/licence", r)
assert r.status_code == 200
assert "SYNTHETIC" in lic.get("client",{}).get("name","")
prods = lic.get("licence",{}).get("terms",{}).get("products",[])
assert "brand.mention_inventory" in prods and "estate.language_inventory" in prods

r = requests.post(f"{BE}/api/caas/client/deliver", headers=H, json={"product":"brand.mention_inventory"})
dj = _p("POST deliver brand.mention_inventory", r)
assert r.status_code == 201
assert dj.get("accepted") is True
assert dj.get("delivery_id","").startswith("dlv-")
assert dj.get("raw_estate_exported") is False
m = dj.get("meter") or {}
assert m.get("quantity") == 1
assert m.get("rate_usd") in (None,)
by_lang = (dj.get("result") or {}).get("by_language")
assert by_lang is not None
print("by_language keys:", list(by_lang)[:3] if isinstance(by_lang, dict) else "list len "+str(len(by_lang)))
dlv_id = dj["delivery_id"]
state["dlv_id"] = dlv_id
json.dump(state, open("/tmp/caas_state.json","w"))

r = requests.get(f"{BE}/api/caas/client/deliveries", headers=H)
dls = _p("GET /api/caas/client/deliveries", r)
assert r.status_code == 200
ds = dls.get("deliveries") if isinstance(dls, dict) else dls
ids = [d.get("id") or d.get("delivery_id") for d in ds]
assert dlv_id in ids, f"dlv not found in {ids}"

r = requests.post(f"{BE}/api/caas/client/deliver", headers=H, json={"product":"domain.media_plan"})
_p("deliver domain.media_plan (not licensed)", r)
assert r.status_code == 403

r = requests.get(f"{BE}/api/caas/client/licence", headers={"X-CaaS-Key":"caas_badbadbad"})
_p("wrong key", r)
assert r.status_code == 401

r = requests.get(f"{BE}/api/caas/client/licence")
_p("no key", r)
assert r.status_code == 401

print("\nALL CLIENT-SIDE ASSERTS PASSED")
