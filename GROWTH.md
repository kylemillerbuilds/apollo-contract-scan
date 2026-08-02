# OLYMPUS GROWTH LEDGER — Apollo On-Chain Agent

The honest book. Real events only, each with its proof. No projections, ever.
(The record is the product.)

## Kill criteria (agreed 2026-07-22, immutable without a dated amendment below)
- Total real-money spend cap: **$50**.
- If publicly listed for **90 days** with **zero non-Kyle payments** → park the lane,
  keep the infrastructure, write the post-mortem here.
- Banned until a stranger pays: agent mainnet transactions, ServiceEscrow contracts,
  Aave/Uniswap treasury loops, any second service.
- No trading or market-making of any kind. Ruled out 2026-07-22 on its own evidence,
  before this lane began.

## Market reality, measured 2026-07-23 (read before setting expectations)
Researched because Kyle pushed back that "list it and wait" isn't self-sufficiency.
He was right, and the numbers are worse than we assumed:
- Whole x402 economy: **~$1.11M volume / 30d, down 77% since Nov 2025**; ~50% of
  transactions are self-dealing or wash; daily txs fell ~131k (Mar) → ~13k (Jul).
- Revenue leaderboard, 30d: #1 $3,120 · #2 $2,680 · #3 $1,420 · #4 $207 · #5 $152.
  **$400/month would make Apollo roughly the #4 x402 service on earth.**
- Structural mismatch: the winners sell high-frequency data and inference agents
  consume constantly. A contract scan is bought **once per contract** — bad fit
  for per-call micropayments.
- We are priced **5–50x under** every comp (AgentLISA $0.50–5, SmartSec $0.50–2),
  in a niche those two plus LoneStarOracle and SolidityScan already occupy.
- Only realistic path to $400/mo found: **Base Builder Rewards + Grants** — and
  those require human verification, so they pay Kyle, not Apollo.
→ Honest reframe: x402 revenue is a **portfolio credential**, not income.

## Milestones

### #1 — 2026-07-22 · First on-chain task ever settled
The agent detected TaskRequested(0) on Base Sepolia, computed SHA256 in code, and
settled `submitResult` on-chain. Before tonight the contract's task counter read 0 —
the loop had never fired once.
**Proof:** tx `0x07b3a15e27b723947e21f21e06f3bac378a5232f81e6687496921cb7bc28f91c`,
block 44502876 · hash independently verified (`shasum -a 256` match) · solver =
`0x9FC88702bb34e7890BEcd822e2D38d6CB37A4a62` · commit `65f32fe`.

### #2 — 2026-07-22 · Guardian becomes code, proves itself
The auditor's whitelist moved from prompt text to the signing layer (`guard.py`): whitelist,
zero-value rule, gas/fee caps, daily budget, killswitch. All six adversarial tests
pass; every rejection logged.
**Proof:** `test_guard.py` run in `activity_log.jsonl` (5 guardian_rejection entries) ·
commit `65f32fe`.

### #3 — 2026-07-22 · First paid API call, settled in USDC
The contract-scan service behind Coinbase's x402 paywall served its first paid call:
402 challenge → signed payment → facilitator settlement → 200 + report. Self-pay
(testnet USDC) — plumbing proof, not revenue.
**Proof:** settlement tx `0x7747c5d59da7bb5a8cbc9d8cfe032c3cd526d05dc97d09cc247793dd049040f6`,
block 44502993, asset = Base Sepolia USDC `0x036C...CF7e` · commit `1928906`.

### #4 — 2026-07-23 · Storefront live on the public internet, first paid call served
`apollo-contract-scan.vercel.app` (Vercel, receive-only, zero keys on host) served a
paid scan over the open internet: 402 challenge → signed testnet-USDC payment →
facilitator settlement → 200 + report. The promotion audit's one open item
(deployment protection) resolved — production domain was public by design.
**Proof:** settlement tx `0x03ed5a4de44e2912bab588d78d489...e313`
(full: `0x03ed5a4de44e2912bab588d48913c3b5bc02794d9fe36448d676c2598d78e313`),
block 44520026 · public `/health` 200, unpaid `/scan-testnet` 402 · commit `5c24584`.

### #5 — 2026-07-23 · Apollo gets a face, and a voice
The storefront stopped reading as raw JSON. `/` now speaks as Apollo the Delphic
oracle — solar emblem, gold-on-night and bronze-on-parchment, first-person copy
whose honest-scoping section ("a prophecy that flatters is worth nothing") IS the
character rather than fine print. Kyle's call: agents with real personality draw
people; sterile API docs don't.
**Proof:** commit `f0cfb00` · verified in both color schemes · live at
apollo-contract-scan.vercel.app.

### #6 — 2026-07-23 · The real-money rail is open and PROVEN
Mainnet USDC payments live on Base via Coinbase's CDP facilitator, paying to
Kyle's own Base wallet. Not merely "configured" — probed with a well-formed but
unsigned payment, which Coinbase's facilitator authenticated and rejected with
`invalid_exact_evm_payload_signature`. That round trip proves credentials,
connectivity, and verification all work; only a genuine signature is missing.
**The probe also caught a real bug:** `_cdp_headers` was a plain function while
x402 does `await create_headers()` — every genuine paying customer would have hit
a 500 while `/health` stayed green. Fixed in `6842cfe`.
**Proof:** `/health` reports `mainnet: true`, `facilitator: coinbase-cdp` ·
payTo `0x8C49…ae27` · asset = Base mainnet USDC `0x8335…2913`.
**Lesson for the ledger:** a green status page is not a working system. Probe the
failure path, not the happy one.

### #7 — 2026-08-02 · PARKED. The listing that was never made, and the record that said it was.

This lane is closed. It never took a customer, and the honest reason is worth more
than the service was.

**What happened.** A research pass on 2026-08-02 reported the storefront "verified
LISTED in the Bazaar (external fetch)" and recommended a price cut to remove a
pricing confound from the 90-day kill test. An audit the same day fetched the same
public index — Coinbase's CDP x402 discovery endpoint, the one the claim cited —
and found **no entry for this service**: no matching URL, no matching payTo
address, no matching description, at any page size. The service was live and
answering. It had never been listed anywhere.

**Why that mattered more than the price.** The kill criterion below reads "publicly
listed for 90 days with zero non-Kyle payments." An unlisted service cannot fail
that test, and it cannot pass it. Ninety days of silence would have measured only
that unfindable things are not found. The experiment had a clock that was never
started, a confound that did not exist, and a fix aimed at both.

**The decision.** Park, on evidence rather than on the clock. The category was
already measured: contract-scanning-over-x402 is sellers selling to sellers —
30+ listed competitors, none appearing in any earnings ranking, while the real
buyers of contract security (wallets, exchanges, screeners) buy B2B subscriptions
from vendors whose free tier covers 150K calls a month. A per-contract purchase is
structurally wrong for per-call micropayments, and no listing repairs that.

**What was actually built, and stands:** a receive-only x402 service where the
internet-reachable limb holds no signing keys and cannot move funds — machine-
checked with negative controls, not asserted; a proven mainnet USDC rail; a
deterministic scanner with no model in the critical path. That pattern is the
asset. The scanner was its demonstration, not its product.

**The lesson, which is the reason this entry exists:** the research pass that
reported the listing imposed a "no claim without a fetched artifact" rule on
everyone else, and carried no artifacts of its own. Its cited workflow ID appears
in exactly one file — itself. **A verification standard you apply only outward is
not a standard.** The failure was not believing a wrong number; it was believing a
number that no one could have checked, in the one lane whose entire product is a
record you can check.

**Proof:** CDP discovery endpoint queried 2026-08-02 (incl. `?limit=1000`), zero
matches for this service · `/health` 200 with `mainnet: true` on the same date
(the service was live, simply unlisted) · council ruling 057, 2026-07-30, which
had already made listing conditional and was never satisfied.

**Standing:** infrastructure kept, service left running, no further spend. Total
real-money spend over the life of the lane: $0 against a $50 cap. Reopening
requires a named buyer, not a better listing.
