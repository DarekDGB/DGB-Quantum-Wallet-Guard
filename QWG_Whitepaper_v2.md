# 🛡 DigiByte Quantum Wallet Guard (QWG) – Whitepaper v2

**Layer‑5: Quantum‑Era Wallet Behaviour Protection for DigiByte**

Author: **DarekDGB (@Darek_DGB)**  
AI Engineering Assistant: **Angel**  
Status: **v2 – Reference Implementation (Experimental)**  
License: **MIT**

---

## 1. Motivation

DigiByte was built with security in mind from day one: multi‑algorithm
mining, fast block times and a long history of honest work. But the
threat model for digital assets is evolving.

For years, security discussions focused almost exclusively on:

- consensus rules  
- hash algorithms  
- signature schemes  
- node‑level vulnerabilities  

In practice, **the wallet has become the new battlefield**:

- large custodial wallets protecting exchange funds  
- multi‑sig treasuries  
- long‑dormant cold wallets holding early coins  
- retail users interacting with dozens of apps and websites  

A future capable quantum adversary does not have to break the entire
network at once. It is enough to selectively target **high‑value keys**
and drain wallets in a way that looks “organic” to traditional tools.

QWG (Quantum Wallet Guard) is designed to protect DigiByte and other
UTXO‑based chains at this critical layer: **wallet behaviour over time**.

---

## 2. Role in the 5‑Layer Quantum Shield

QWG is part of a broader defensive architecture:

1. **Sentinel AI v2** – monitors node, mempool and chain health  
2. **DQSN v2** – aggregates and scores threat signals across many nodes  
3. **ADN v2** – local autonomous defense node; performs lock‑downs  
4. **Guardian Wallet v2** – user‑facing wallet guard & UX controls  
5. **Quantum Wallet Guard v2 (QWG)** – deep analysis of wallet flow
   patterns

Above these sits the **Adaptive Core**, which learns from all layers and
updates policies and thresholds over time.

Within this stack, QWG is the specialist focused on **patterns of fund
movement**, especially those that could indicate **quantum‑style
attacks**.

---

## 3. Threat Model

QWG is not designed to replace post‑quantum cryptography. Instead, it
assumes that the cryptographic layer will eventually be upgraded, but
that **behavioural early‑warning systems are needed today**.

### 3.1 Adversary Capabilities

We consider adversaries who may:

- Gain access to a subset of private keys (classical or quantum means)  
- Operate many compromised wallets in a coordinated fashion  
- Move funds slowly over time to avoid naive alerts  
- Split sweeps through intermediary addresses to blur visibility  
- Target long‑dormant or “forgotten” wallets in waves  

We also assume the attacker can:

- Automate withdrawals  
- Exploit weak monitoring at exchanges or custodians  
- Take advantage of fragmented logging or siloed systems  

### 3.2 Attack Patterns of Interest

QWG focuses on patterns such as:

- **Dormant Key Sweep** – many old, inactive wallets suddenly moving
  toward one or a few aggregation points.
- **Multi‑Wallet Drain** – coordinated withdrawals from many related
  addresses in a short window.
- **Escalating Probe** – small test transactions followed by
  increasingly larger sums if no protection triggers.
- **Entropy‑Weak Rhythm** – repeated signing with suspiciously regular
  timing or volume (indicative of scripted or automated control).

These patterns are subtle and often **span multiple transactions and
wallets**. They are not easily identified by checking one transaction in
isolation.

---

## 4. Design Goals

QWG is built around several guiding principles:

1. **Non‑invasive** – no changes to DigiByte consensus or crypto.  
2. **Composable** – works as a module in a larger security stack.  
3. **Observable & Explainable** – risk scores come with context and
   pattern labels.  
4. **Chain‑agnostic** – designed for DigiByte first, but other UTXO
   chains can reuse it.  
5. **Adaptive‑ready** – can feed into and receive updates from the
   Adaptive Core.

The goal is not to “stop every transaction”, but to make sure **high
risk flows cannot pass silently**.

---

## 5. Core Concepts

### 5.1 Quantum‑Style Risk Score (QRS)

QWG uses a **Quantum‑Style Risk Score (QRS)**:

- Integer range `0–100`  
- Aggregates multiple signals:
  - timing and rhythm of withdrawals  
  - number of wallets involved  
  - UTXO fragmentation and recombination patterns  
  - destination clustering (aggregation addresses)  
  - policy‑driven flags from DQSN / Sentinel / Guardian  
- Mapped to levels: `LOW`, `ELEVATED`, `HIGH`, `CRITICAL`

The QRS is not a claim that “quantum attack is happening”, but a
probabilistic indicator that **behaviour matches patterns we expect from
a powerful, automated adversary**.

### 5.2 RiskContext

`RiskContext` is a long‑lived object representing the **state of a
session, wallet, account or operator context**. It may track:

- history of incoming and outgoing flows  
- device or session identifiers (if provided)  
- links to Guardian Wallet signals (user behaviour)  
- external alerts from DQSN or Sentinel AI  

This allows QWG to reason not just about “one transaction”, but about
the *trajectory* of behaviour.

### 5.3 Engine and Policies

`QWGEngine` consumes structured events (e.g. “sweep from wallet A to X1,
10 UTXOs, 12,000 DGB”) and evaluates them under the current `RiskContext`
and `Policies`.

`Policies` encode:

- thresholds for QRS levels  
- combinations of signals that qualify as `DORMANT_KEY_SWEEP` or other
  pattern tags  
- escalation rules (e.g. repeated suspicious events → CRITICAL)  

The separation between `Engine` and `Policies` is intentional so that
the **Adaptive Core** or human operators can refine policies without
rewriting engine internals.

---

## 6. Architecture Overview

At code level (see README for file listing), the main components are:

- `engine.py` – implements `QWGEngine`, the central entry point.  
- `risk_context.py` – tracks state needed across multiple events.  
- `policies.py` – declarative rules for thresholds and pattern logic.  
- `decisions.py` – result objects, risk levels, and helper structures.  
- `adaptive_bridge.py` – hooks for communication with Adaptive Core.  
- `examples/` – concrete scenarios, including a dormant key sweep.  
- `tests/` – unit tests and scenario tests for QWG behaviour.

Integration is done by instantiating a `RiskContext` and `QWGEngine`,
then feeding events into the engine as they occur.

---

## 7. Dormant Key Sweep Scenario (QWG‑SIM‑001)

To make the system concrete, QWG ships with a documented simulation:

- Specified in `QWG-QuantumAttackScenario-1.md`  
- Implemented in `examples/dormant_key_sweep_scenario.py`  
- Tested via `tests/test_dormant_key_sweep.py`

The scenario simulates multiple wallets (`A`, `B`, `C`) moving UTXOs in a
coordinated sequence to aggregation addresses (`X1`, `X2`). Although the
numbers are synthetic, the pattern is intended to mirror what a
real‑world quantum adversary might do when draining long‑dormant keys.

The example demonstrates:

- how QRS climbs with each step  
- at which point risk escalates to `HIGH` or `CRITICAL`  
- how the engine labels the pattern (e.g. `DORMANT_KEY_SWEEP`)  

This gives DigiByte developers and integrators a **tangible feel** for
how QWG reacts to structured attack patterns.

---

## 8. Integration Paths

QWG is designed to be embedded into a variety of DigiByte‑aligned
systems:

### 8.1 Exchanges and Custodians

- Wrap withdrawal flows with QWG checks.  
- Require extra approval, cooling‑off time or multi‑factor verification
  on `HIGH` / `CRITICAL` events.  
- Feed anonymised statistics back into Adaptive Core for improved
  learning.

### 8.2 DigiDollar Infrastructure

DigiDollar stability and oracle components can integrate QWG to monitor:

- large rebalancing transactions  
- cross‑chain bridge movements  
- multi‑wallet sweeps when oracle keys or treasury wallets move funds.

### 8.3 High‑Value Personal or Institutional Wallets

Advanced users or institutions holding large long‑term positions can
run QWG as part of a **local security stack**:

- QWG scores outgoing flows before they are broadcast.  
- Guardian Wallet UX reflects the QRS (e.g. warnings, delay, friction).  
- ADN v2 can receive alerts to restrict RPC or node behaviour if
  something looks catastrophic.

---

## 9. Relationship to Post‑Quantum Cryptography

QWG does **not** attempt to implement or replace post‑quantum
signatures. Instead, it acknowledges that:

- PQC migration will take time.  
- There may be multiple candidate schemes and transition phases.  
- Even after PQC adoption, **behavioural anomalies remain valuable
  indicators of compromise**.

Thus QWG is designed to work **before, during and after** PQC migration:

- **Before** – as a proactive detector of high‑risk patterns.  
- **During** – to monitor legacy vs PQC address interactions and sweeps.  
- **After** – as an additional line of defense for any future class of
  automated or AI‑assisted attacks.

---

## 10. Limitations

QWG is intentionally scoped:

- It does not claim mathematical proof of quantum attack.  
- It depends on integrators supplying correct event data.  
- It can generate false positives if policies are too aggressive.  
- It does not see off‑chain social engineering or phishing on its own
  (this is where Guardian Wallet v2 contributes).

For these reasons, QWG is best deployed in environments where **humans
or higher‑level systems remain in the loop** to interpret alerts.

---

## 11. Roadmap

The current v2 release is a **reference implementation** suitable for:

- code review  
- testnet experimentation  
- integration trials in staging environments  

Planned future directions include:

- more scenario libraries (multi‑bridge attacks, flash sweeps, etc.)  
- deeper integration with Sentinel AI v2 and DQSN v2 signals  
- optional cryptographic hooks to distinguish legacy vs PQC addresses  
- policy sets tuned for different risk profiles (retail vs custodial vs
  treasury)

As the Adaptive Core matures, we expect QWG policies to evolve based on
real‑world data and red‑team exercise results.

---

## 12. Conclusion

DigiByte has always been about **security, speed and forward thinking**.
Quantum Wallet Guard (QWG) extends that philosophy into the wallet
layer, where human behaviour, automation and future quantum threats all
intersect.

By analysing how funds move — not just which algorithm signs them — QWG
provides DigiByte and its ecosystem with an additional line of defense
that is:

- chain‑agnostic  
- explainable  
- adaptable  
- ready for testnet today  

This whitepaper describes the reference v2 design. The implementation in
this repository is open under MIT license so that the DigiByte community
and other projects can review, extend and deploy it in the way that best
protects their users.

For questions, experimentation or collaboration, please contact:

**@Darek_DGB** on X.

