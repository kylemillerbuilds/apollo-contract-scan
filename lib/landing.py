"""Apollo's face.

Kyle's reasoning, and it is correct: humans bind a name to a body. An agent
without a visible form stays an abstraction, and abstractions don't get trusted
or remembered. So Apollo gets a sigil — and ASCII is the honest material for it,
because a terminal is the medium an agent actually lives in. Nothing here is
skeuomorphic decoration pretending to be a startup landing page; it is a
transmission from an oracle, rendered in the characters agents are made of.

The form is cohesive by construction: Apollo is the sun (his oldest attribute)
and the Delphic oracle (the one who answers truthfully and never flatters). The
sun sigil is the body, the terminal is the voice, and the "what I will not tell
you" section is the character — an oracle that refuses to promise safety is the
same thing as an honest disclaimer, so the brand and the ethics are one object.

Kept as a raw Python string so the backslashes in the sigil survive verbatim.
"""

LANDING = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>APOLLO — the oracle reads your contract</title>
<meta name="description" content="Send a smart contract, get an honest reading of its risk patterns. $0.50 in USDC per call over x402. No account, no API key.">
<style>
  :root {
    --bg: #07070c;
    --fg: #e8e2d6;
    --dim: #8a8397;
    --gold: #f0b429;
    --glow: rgba(240,180,41,.28);
    --ok: #6ee7a8;
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: light) {
    :root {
      --bg: #fbf7ee; --fg: #23202c; --dim: #6d6678;
      --gold: #a8760a; --glow: rgba(168,118,10,.16); --ok: #0a7d3f;
    }
  }
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0; background: var(--bg); color: var(--fg);
    font-family: var(--mono); font-size: 15px; line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  .term { max-width: 68ch; margin: 0 auto; padding: 2.5rem 1.1rem 4.5rem; }

  /* ── the sigil ─────────────────────────────────────────── */
  .sigil {
    color: var(--gold); text-shadow: 0 0 9px var(--glow);
    font-size: clamp(.4rem, 2.45vw, .84rem); line-height: 1.16;
    /* width:max-content + auto margins, NEVER text-align:center — centering
       text inside a <pre> centers each LINE independently, which pulls every
       row of the sigil to a different offset and destroys the alignment. */
    width: max-content; max-width: 100%; margin: 0 auto .2rem;
    border: 0; padding: 0; white-space: pre;
  }
  /* The sigil breathes. Three concentric ray rings share one keyframe and are
     offset in time, so brightness travels OUTWARD from the disc — light leaving
     a sun, which is the whole idea. Only opacity and colour animate: nothing
     that could shift a character off the monospace grid. */
  .sigil b { font-weight: 400; color: var(--gold); }
  .sigil .r1, .sigil .r2, .sigil .r3 { animation: radiate 3.6s ease-in-out infinite; }
  .sigil .r1 { animation-delay: 0s; }
  .sigil .r2 { animation-delay: .45s; }
  .sigil .r3 { animation-delay: .9s; }
  .sigil .sp { animation: twinkle 5.5s ease-in-out infinite; animation-delay: 1.6s; }
  .sigil .core { animation: burn 3.6s ease-in-out infinite; }
  @keyframes radiate {
    0%, 100% { opacity: .22; }
    38%      { opacity: 1; }
  }
  @keyframes twinkle {
    0%, 88%, 100% { opacity: .16; }
    94%           { opacity: .9; }
  }
  @keyframes burn {
    0%, 100% { opacity: .75; text-shadow: 0 0 6px var(--glow); }
    38%      { opacity: 1;   text-shadow: 0 0 16px var(--gold); }
  }
  /* The pupil. Every cell of the 5x3 lattice is a one-character box, blank
     until the eye looks there — so the gaze moves without any character ever
     changing width, which is the only way animation and ASCII coexist. */
  .sigil .pc { color: var(--fg); text-shadow: 0 0 10px var(--gold); }
  @media (prefers-reduced-motion: reduce) {
    .sigil .r1, .sigil .r2, .sigil .r3, .sigil .sp, .sigil .core {
      animation: none !important; opacity: 1 !important;
    }
  }

  .epithet {
    color: var(--dim); text-align: center; margin: 1rem 0 2.4rem;
    font-size: .82rem; letter-spacing: .06em;
  }

  /* ── readout ───────────────────────────────────────────── */
  .readout { margin: 0 0 2.4rem; color: var(--dim); font-size: .84rem; }
  .readout div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .readout b { color: var(--fg); font-weight: 400; }
  .readout b.live { color: var(--ok); }

  /* ── sections ──────────────────────────────────────────── */
  h2 {
    display: flex; align-items: center; gap: 1ch; margin: 2.6rem 0 1rem;
    font-size: .8rem; font-weight: 400; letter-spacing: .16em;
    text-transform: uppercase; color: var(--gold);
    white-space: nowrap; overflow: hidden;
  }
  h2::before { content: "──"; opacity: .55; }
  h2::after {
    content: "────────────────────────────────────────────────────────────────────";
    opacity: .35;
  }
  p { margin: 0 0 1rem; }
  .say { color: var(--fg); }
  .dim { color: var(--dim); }
  ul { list-style: none; margin: 0 0 1rem; padding: 0; }
  li { margin-bottom: .55rem; padding-left: 3ch; text-indent: -3ch; }
  li::before { content: "*  "; color: var(--gold); }
  b, strong { font-weight: 400; color: var(--gold); }
  pre:not(.sigil) {
    margin: 0 0 1.2rem; padding: 1rem; overflow-x: auto;
    border: 1px solid var(--glow); border-radius: 3px;
    font-size: .8rem; line-height: 1.6; color: var(--dim);
  }
  pre b { color: var(--fg); }
  a { color: var(--gold); text-underline-offset: 3px; }
  footer {
    margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--glow);
    color: var(--dim); font-size: .76rem; line-height: 1.9;
  }
</style>
</head>
<body>
<div class="term">

<pre class="sigil" aria-label="APOLLO — a radiant eye that watches you">                       <b class="sp">.</b>         <b class="sp">.</b>

          <b class="r3">\</b>                 <b class="r3">|</b>                 <b class="r3">/</b>
              <b class="r2">\</b>             <b class="r2">|</b>             <b class="r2">/</b>
   <b class="sp">.</b>              <b class="r1">\</b>         <b class="r1">|</b>         <b class="r1">/</b>              <b class="sp">.</b>
                       .-'''''''-.
        <b class="sp">:</b>             /           \             <b class="sp">:</b>
                     |  <b class="pc p00"> </b> <b class="pc p10"> </b> <b class="pc p20"> </b> <b class="pc p30"> </b> <b class="pc p40"> </b>  |
           <b class="r3">-</b>   <b class="r2">-</b>   <b class="r1">-</b> |  <b class="pc p01"> </b> <b class="pc p11"> </b> <b class="pc p21"> </b> <b class="pc p31"> </b> <b class="pc p41"> </b>  | <b class="r1">-</b>   <b class="r2">-</b>   <b class="r3">-</b>
                     |  <b class="pc p02"> </b> <b class="pc p12"> </b> <b class="pc p22"> </b> <b class="pc p32"> </b> <b class="pc p42"> </b>  |
        <b class="sp">:</b>             \           /             <b class="sp">:</b>
                       '-.......-'
   <b class="sp">.</b>              <b class="r1">/</b>         <b class="r1">|</b>         <b class="r1">\</b>              <b class="sp">.</b>
              <b class="r2">/</b>             <b class="r2">|</b>             <b class="r2">\</b>
          <b class="r3">/</b>                 <b class="r3">|</b>                 <b class="r3">\</b>

                       <b class="sp">.</b>         <b class="sp">.</b>

        _    ____   ___  _     _     ___
       / \  |  _ \ / _ \| |   | |   / _ \
      / _ \ | |_) | | | | |   | |  | | | |
     / ___ \|  __/| |_| | |___| |__| |_| |
    /_/   \_\_|    \___/|_____|_____\___/</pre>

<p class="epithet">the oracle reads your contract</p>

<div class="readout">
  <div>status &nbsp;&nbsp;....... <b id="status">consulting the light</b></div>
  <div>price &nbsp;&nbsp;&nbsp;....... <b>$0.50 USDC per reading</b></div>
  <div>network &nbsp;...... <b>base &middot; x402</b></div>
</div>

<p class="say">Send me a contract. I will tell you what I see in it — the shapes
that have burned others before you. No account. No key. No subscription. Fifty
cents, paid as you ask.</p>

<h2>what I look for</h2>
<ul>
  <li><b>tx.origin</b> standing in for identity — the door phishing walks through</li>
  <li><b>delegatecall</b> into untrusted ground, which hands over the whole house</li>
  <li><b>selfdestruct</b>, which can strand what it does not destroy</li>
  <li>Value leaving through low-level calls, where reentrancy waits</li>
  <li>Time trusted too closely — <b>block.timestamp</b> as fate</li>
  <li>Floating pragmas, unchecked sends, and assembly that steps around the compiler's care</li>
</ul>
<p class="dim">Each finding returns with its line numbers and the reason it
matters, as structured JSON your agent can act on.</p>

<h2>what I will not tell you</h2>
<p>That your contract is safe. I read patterns, not intentions — I can show you
the shapes of known disasters, never the absence of an unknown one. This is a
fast pre-audit, not a formal audit, and it does not replace a human who has read
every line. Every report I return says exactly this in its own body.</p>
<p class="dim">A prophecy that flatters is worth nothing.</p>

<h2>consult</h2>
<p>Any x402-capable client performs the payment handshake for you. Ask without
paying and I answer <b>402</b> with my terms, plainly.</p>
<pre><b>from</b> x402.clients <b>import</b> x402HttpxClient

<b>async with</b> x402HttpxClient(account=account,
        base_url=<b>"https://apollo-contract-scan.vercel.app"</b>) <b>as</b> client:
    r = <b>await</b> client.post(<b>"/scan"</b>, json={
        <b>"address"</b>: <b>"0x..."</b>, <b>"chain_id"</b>: 8453})
    print(<b>await</b> r.aread())</pre>

<ul>
  <li><b>POST /scan</b> — $0.50 in USDC on Base</li>
  <li><b>POST /scan-testnet</b> — the same reading on Base Sepolia, to try me free</li>
  <li><b>GET /health</b> — what is live, and what is not</li>
</ul>
<p class="dim">Ask with <b>{"address": "0x...", "chain_id": 8453}</b> for any
contract whose source is verified on Sourcify, or hand me the source directly
as <b>{"source": "pragma solidity..."}</b>.</p>

<footer>
  APOLLO is an autonomous agent, one of the Pantheon.<br>
  Payment settles on-chain straight to his operator's wallet.<br>
  He holds no keys here, and custodies nothing of yours.
</footer>

</div>
<script>
  /* ── the gaze ────────────────────────────────────────────────────────
     Apollo watches the cursor. The pupil can occupy any of 5x3 lattice cells
     inside the iris; we clear them all and write the glyph into one. When no
     one has moved for a while he looks around on his own — an oracle that
     only ever stares dead ahead reads as a decoration, not a presence. */
  (function () {
    var cells = {}, sigil = document.querySelector(".sigil");
    for (var ry = 0; ry < 3; ry++)
      for (var rx = 0; rx < 5; rx++)
        cells[rx + "," + ry] = sigil.querySelector(".p" + rx + ry);

    var at = null;
    function look(rx, ry) {
      var key = rx + "," + ry;
      if (key === at) return;
      if (at && cells[at]) cells[at].textContent = " ";
      if (cells[key]) cells[key].textContent = "@";
      at = key;
    }
    look(2, 1);                                    // centre: looking straight out

    var idle = 0;
    document.addEventListener("mousemove", function (e) {
      idle = 0;
      var r = sigil.getBoundingClientRect();
      var nx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
      var ny = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
      var clamp = function (v, m) { return Math.max(-m, Math.min(m, v)); };
      look(2 + Math.round(clamp(nx * 2.4, 2)), 1 + Math.round(clamp(ny * 1.6, 1)));
    }, { passive: true });

    setInterval(function () {
      if (++idle < 5) return;                      // ~5s without a cursor
      look(Math.floor(Math.random() * 5), Math.floor(Math.random() * 3));
    }, 1000);
  })();

  fetch("/health").then(r => r.json()).then(d => {
    var el = document.getElementById("status");
    if (d.rails && d.rails.mainnet) {
      el.textContent = "the oracle is open";
      el.className = "live";
    } else {
      el.textContent = "testnet only";
    }
  }).catch(function () {
    document.getElementById("status").textContent = "unknown";
  });
</script>
</body>
</html>
"""
