# Apollo Contract Scan — a receive-only agent that sells a service on Base

Live: **https://apollo-contract-scan.vercel.app**

A pay-per-call Solidity risk scan for AI agents. No account, no API key, no
subscription. An agent calls the endpoint, gets `402 Payment Required` with the
terms, pays **$0.50 USDC on Base** over [x402](https://www.x402.org/), and
receives a structured report of pattern-level risks with line numbers.

```bash
curl -s https://apollo-contract-scan.vercel.app/health
```

## The point: the agent holds no keys

This deployment contains **no signing keys and no wallet files**, and that is the
part worth copying. It cannot custody, move, or redirect funds. x402 payments
settle directly from the customer's wallet to the operator's; the service's only
capability is to *receive*.

That constraint is deliberate. 2026 has produced a $45M AI-trading-agent breach,
and the Grok-Bankr exploit in which hidden instructions were decoded by one agent
and handed to another that held wallet permissions. The prevailing pattern gives
agents keys and then tries to constrain them with prompts. A prompt is not a lock.

This is the other shape: a commercially useful agent whose deployment is
structurally incapable of losing your money, because it never holds any.

Where the boundary actually lives:

- **Credentials** are Vercel environment variables, never in source.
- **The payout address** is a plain constant. Changing it changes where money
  goes and shows up in a diff — it is not hidden in config.
- **The facilitator** (Coinbase CDP, or a keyless alternative) is non-custodial
  either way: it can only relay a payment the customer already signed, to the
  exact destination and amount the customer already saw.

## Endpoints

| Route | Cost | Notes |
|---|---|---|
| `GET /` | free | the oracle's front door |
| `GET /health` | free | which rails are live, and which facilitator carries them |
| `POST /scan` | $0.50 USDC (Base) | the real rail |
| `POST /scan-testnet` | $0.50 testnet USDC (Base Sepolia) | try it for nothing |

Body takes either a verified contract address or raw source:

```json
{"address": "0x...", "chain_id": 8453}
{"source": "pragma solidity ^0.8.20; ..."}
```

Any x402-capable client handles the payment handshake:

```python
from x402.clients import x402HttpxClient

async with x402HttpxClient(account=account,
        base_url="https://apollo-contract-scan.vercel.app") as client:
    r = await client.post("/scan", json={"source": src})
    print(await r.aread())
```

## What it will not tell you

That your contract is safe. This is a fast heuristic **pre-audit** — it finds the
shapes of known disasters (`tx.origin` as identity, `delegatecall` into untrusted
ground, `selfdestruct`, value leaving through low-level calls, timestamp
dependence, floating pragmas, inline assembly). It cannot show the absence of an
unknown one, it is not a formal audit, and it does not replace a human who has
read every line. Every report says so in its own body.

## Two engineering notes worth stealing

**A green status page is not a working system.** After the mainnet rail went live
— health green, payment terms correct — we probed it with a well-formed but
deliberately unsigned payment. It returned HTTP 500. The credential function was
a plain `def` where x402's client does `await create_headers()`, and that code
path runs *only* when a real payment is verified. It would have failed for every
paying customer and no one else. Probe the failure path, not the happy one.

**Gitignore key material by pattern, never by exact name.** A pre-commit scan
caught `wallet_data 2.txt` — an iCloud duplicate of a private key file that the
exact-name rule sailed straight past.

## Layout

```
api/index.py     the service: routes, x402 paywall, facilitator selection
lib/auditor.py   the scan itself — deterministic, no LLM in the critical path
lib/landing.py   the human front door (ASCII sigil, generated not hand-spaced)
```

Deploys to Vercel as a Python function. Set `PAY_TO_MAINNET` to your own address
and the CDP credentials as env vars; with no facilitator configured the mainnet
route stays dormant and says so rather than failing at payment time.

## License

MIT.
