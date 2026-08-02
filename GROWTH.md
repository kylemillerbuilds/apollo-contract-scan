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

### #7 — 2026-08-02 · Listed, with the receipt written late — and an audit that got it backwards first

This entry exists because the ledger was missing one, and because the first
attempt to write it was wrong. Both halves belong in an honest book.

**The listing is real.** The service appears in Coinbase's CDP x402 discovery
index ("the Bazaar"): resource `https://apollo-contract-scan.vercel.app/scan`,
network `base`, `maxAmountRequired` 500000 (that is $0.50 USDC at 6 decimals),
`discoverable: true`, entry `lastUpdated` 2026-07-30T16:46:21Z. No milestone was
recorded when it happened, so for three days this ledger and the world disagreed.
**The gap was the bookkeeping, not the deployment.**

**The audit that nearly wrote the opposite.** On 2026-08-02 a review concluded the
service had *never* been listed and drafted this entry as a post-mortem. That
conclusion came from querying the discovery endpoint and reading the first page of
results — 100 entries out of **14,810**. The index is paginated; page one is 0.7%
of it. A complete sweep of all 14,810 listings found the entry immediately.

**Why the mistake is worth publishing.** The review was auditing a *different*
document for making claims nobody could check. It then made a claim of exactly
that kind: a negative — "it is not there" — established by searching a fraction of
the space without stating that it was a fraction. **A negative result is only as
good as the completeness of the search behind it, and completeness is the part you
have to prove.** The tell was visible the whole time and went unread: the response
carried `pagination: {limit: 100, total: 14810}`. The number that falsified the
conclusion was sitting inside the evidence used to reach it.

**What is still open, and is not being guessed at.** The index reports
`l30DaysTotalCalls: 4` and `l30DaysUniquePayers: 1` for this resource, last called
2026-07-30T16:46:21Z. Whether that single payer is the operator's own test traffic
or a third party is **not yet established on-chain** — an attempt to settle it
against public Base RPC endpoints failed on rate limits, and a positive control
confirmed the queries were being rejected rather than returning a true zero. Until
that is read properly, the payer is unknown, and "unknown" is what this book says.

**Proof:** complete sweep of the CDP discovery index 2026-08-02 — all 14,810
listings retrieved across 15 pages, one match, payload retained · `/health` 200
with `mainnet: true` on the same date · index entry `lastUpdated` 2026-07-30.

**Lesson for the ledger:** *a clean scan over the wrong subset reports clean.* This
book already carried that lesson from a secret scan that matched no files. It came
back in a new costume — page one of a paginated index — and was caught only
because the payload was kept and re-read. Keep the payload.
