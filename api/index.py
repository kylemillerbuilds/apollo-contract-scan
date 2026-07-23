"""Apollo Contract Scan — public x402 storefront (receive-only by construction).

This deployment holds NO signing keys and NO wallet files. It can only receive:
x402 customers pay the facilitator-settled USDC straight to the pay-to address.

Routes:
  /              the oracle's front door (human landing page)
  /health        free — what is live and which facilitator is carrying payments
  /scan-testnet  $0.50 testnet USDC (Base Sepolia) — self-test rail
  /scan          $0.50 real USDC (Base mainnet) — dormant until a facilitator is chosen

Env (Vercel project settings):
  PAY_TO_TESTNET  optional, defaults to the agent's testnet address
  PAY_TO_MAINNET  optional, defaults to Kyle's verified Base wallet below
  CDP_API_KEY_ID / CDP_API_KEY_SECRET  use Coinbase's facilitator (Kyle's choice, 07-23)
  USE_OPEN_FACILITATOR=1               use the keyless OpenFacilitator instead
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from x402.fastapi.middleware import require_payment
from x402.facilitator import FacilitatorConfig

from auditor import fetch_source, scan
from landing import LANDING

PRICE = "$0.50"
PAY_TO_TESTNET = os.getenv("PAY_TO_TESTNET", "0x9FC88702bb34e7890BEcd822e2D38d6CB37A4a62")
# Kyle's own Base smart wallet (public receiving address, verified on Base mainnet
# 2026-07-23). Revenue lands here and nowhere else; nothing in this deployment can
# move it — the host holds no keys.
PAY_TO_MAINNET = os.getenv("PAY_TO_MAINNET", "0x8C491Ed88a02ecB0B3E33144fB52cc335b71ae27")

# Two mainnet facilitators, and the choice is made by what's configured.
# Coinbase's is the one we'd rather run on (named operator, official), but it
# needs API credentials. OpenFacilitator is keyless and verified to support Base
# mainnet, so the rail can be live TODAY and silently upgrade the moment CDP keys
# appear in the environment. A facilitator is non-custodial either way — it only
# broadcasts a payment the customer already signed to a destination the customer
# already saw, so neither one can redirect or hold Kyle's money.
CDP_FACILITATOR = "https://api.cdp.coinbase.com/platform/v2/x402"
OPEN_FACILITATOR = "https://pay.openfacilitator.io"




def _env_any(*names):
    """Coinbase has shipped two naming conventions for the same credential pair
    (ID/SECRET on the current portal, NAME/PRIVATE_KEY on the older one), so
    accept either rather than making a tired human guess which one we wanted."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


CDP_KEY_ID = _env_any("CDP_API_KEY_ID", "CDP_API_KEY_NAME")
CDP_KEY_SECRET = _env_any("CDP_API_KEY_SECRET", "CDP_API_KEY_PRIVATE_KEY")
CDP_ENV_NAMES = ("CDP_API_KEY_ID", "CDP_API_KEY_NAME",
                 "CDP_API_KEY_SECRET", "CDP_API_KEY_PRIVATE_KEY")

HAS_CDP = bool(CDP_KEY_ID and CDP_KEY_SECRET)
# Which facilitator processes real money is KYLE'S call, not a default I get to
# pick. Until he chooses, the mainnet rail stays dormant and /scan says so.
USE_OPEN_FACILITATOR = os.getenv("USE_OPEN_FACILITATOR") == "1"
FACILITATOR_NAME = ("coinbase-cdp" if HAS_CDP
                    else "openfacilitator (keyless)" if USE_OPEN_FACILITATOR else None)
MAINNET_READY = bool(PAY_TO_MAINNET and FACILITATOR_NAME)

app = FastAPI(title="Apollo Contract Scan", version="0.2.0")


async def _cdp_headers() -> dict:
    """Per-operation JWT headers for Coinbase's mainnet x402 facilitator.

    MUST be async: x402's FacilitatorClient does `await create_headers()`, so a
    plain function returns a dict into an await and raises TypeError — which
    surfaces only when a real payment is verified, i.e. it would have 500'd on
    the first paying customer and no earlier. Found by probing the live rail
    with a well-formed but unsigned payment.
    """
    from cdp.auth.utils.jwt import generate_jwt, JwtOptions
    headers = {}
    for op in ("verify", "settle", "list"):
        token = generate_jwt(JwtOptions(
            api_key_id=CDP_KEY_ID,
            api_key_secret=CDP_KEY_SECRET,
            request_method="POST" if op != "list" else "GET",
            request_host="api.cdp.coinbase.com",
            request_path=f"/platform/v2/x402/{op}" if op != "list" else "/platform/v2/x402/discovery/resources",
        ))
        headers[op] = {"Authorization": f"Bearer {token}"}
    return headers


DESCRIPTION = ("Heuristic Solidity risk scan: pattern-level red flags for a contract "
               "address (verified source via Sourcify) or raw source. Honest scoping: "
               "a fast pre-audit, not a formal security audit.")

app.middleware("http")(require_payment(
    price=PRICE, pay_to_address=PAY_TO_TESTNET, path="/scan-testnet",
    network="base-sepolia", description=DESCRIPTION + " (testnet rail)",
))

if MAINNET_READY:
    mainnet_facilitator = (FacilitatorConfig(url=CDP_FACILITATOR, create_headers=_cdp_headers)
                           if HAS_CDP else FacilitatorConfig(url=OPEN_FACILITATOR))
    app.middleware("http")(require_payment(
        price=PRICE, pay_to_address=PAY_TO_MAINNET, path="/scan",
        network="base", description=DESCRIPTION,
        facilitator_config=mainnet_facilitator,
    ))


class ScanRequest(BaseModel):
    address: str | None = None
    chain_id: int = 8453
    source: str | None = None


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(LANDING)


@app.get("/health")
def health():
    body = {"ok": True, "service": "apollo-contract-scan", "price": PRICE,
            "rails": {"testnet": bool(PAY_TO_TESTNET), "mainnet": MAINNET_READY},
            "mainnet_pay_to": PAY_TO_MAINNET,
            "mainnet_facilitator": FACILITATOR_NAME}
    if not MAINNET_READY:
        # Only while something is wrong: report WHICH credential names this
        # deployment can see. Names and presence only — never a value — so the
        # rail can be debugged without anyone pasting a secret into a chat.
        body["credential_names_visible"] = [n for n in CDP_ENV_NAMES if os.getenv(n)]
    return body


def _run_scan(req: ScanRequest):
    source, resolved_from = req.source, "provided source"
    if source is None and req.address:
        source = fetch_source(req.chain_id, req.address)
        resolved_from = f"sourcify {req.chain_id}/{req.address}"
        if source is None:
            return {"error": "Contract source not verified on Sourcify; "
                             "POST the source directly in the 'source' field."}
    if not source:
        return {"error": "Provide 'address' (verified contract) or 'source'."}
    report = scan(source)
    report["resolved_from"] = resolved_from
    return report


@app.post("/scan")
def scan_mainnet(req: ScanRequest):
    if not MAINNET_READY:
        return {"error": "Mainnet rail not yet configured — use /scan-testnet."}
    return _run_scan(req)


@app.post("/scan-testnet")
def scan_testnet(req: ScanRequest):
    return _run_scan(req)
