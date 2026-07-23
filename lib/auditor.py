"""Heuristic Solidity risk scan — the sellable skill behind the x402 paywall.

Honest scoping: this is a fast heuristic PRE-audit (pattern-level red flags),
not a formal security audit, and its output says so. Reasoning-class analysis
(LLM-driven) is the extension point, same rule as the on-chain worker: the
model may reason, but code assembles and validates what the customer receives.
"""
import re

import httpx

SOURCIFY = "https://sourcify.dev/server/v2/contract/{chain_id}/{address}"

# (name, regex, severity, note)
CHECKS = [
    ("tx.origin auth", r"tx\.origin", "high",
     "tx.origin for auth is phishable; use msg.sender."),
    ("selfdestruct", r"selfdestruct\s*\(", "high",
     "selfdestruct can brick the contract and strand funds."),
    ("delegatecall", r"\.delegatecall\s*\(", "high",
     "delegatecall to untrusted targets hands over full control of storage."),
    ("low-level call with value", r"\.call\{value:", "medium",
     "External call transferring value — verify reentrancy protection and check the return value."),
    ("unchecked send/transfer", r"\.send\s*\(", "medium",
     ".send() returns bool that is easy to ignore; prefer checked patterns."),
    ("timestamp dependence", r"block\.timestamp", "low",
     "Miners can nudge block.timestamp; avoid using it for randomness or tight deadlines."),
    ("floating pragma", r"pragma\s+solidity\s*\^", "low",
     "Floating pragma compiles under future minor versions; pin for reproducible audits."),
    ("assembly block", r"\bassembly\s*\{", "low",
     "Inline assembly bypasses Solidity safety checks; review manually."),
]


def fetch_source(chain_id: int, address: str) -> str | None:
    """Pull verified source from Sourcify (keyless, public). None if unverified."""
    try:
        r = httpx.get(SOURCIFY.format(chain_id=chain_id, address=address),
                      params={"fields": "sources"}, timeout=15)
        if r.status_code != 200:
            return None
        sources = r.json().get("sources") or {}
        return "\n\n".join(v.get("content", "") for v in sources.values()) or None
    except httpx.HTTPError:
        return None


def scan(source: str) -> dict:
    findings = []
    for name, pattern, severity, note in CHECKS:
        hits = [m.start() for m in re.finditer(pattern, source)]
        if hits:
            lines = sorted({source.count("\n", 0, h) + 1 for h in hits})
            findings.append({"check": name, "severity": severity,
                             "lines": lines, "note": note})
    counts = {s: sum(1 for f in findings if f["severity"] == s)
              for s in ("high", "medium", "low")}
    return {
        "disclaimer": "Automated heuristic pre-audit — pattern-level red flags only. "
                      "Not a formal security audit.",
        "sloc": source.count("\n") + 1,
        "summary": counts,
        "findings": findings,
    }
