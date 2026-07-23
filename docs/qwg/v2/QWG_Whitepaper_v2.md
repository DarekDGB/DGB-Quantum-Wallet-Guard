# 🛡 DigiByte Quantum Wallet Guard (QWG) – Whitepaper v2

**Layer‑5: Quantum‑Era Wallet Behaviour Protection for DigiByte**

Author: **DarekDGB**
Status: **v2 – Historical design reference; non-authoritative**
License: **MIT**

> **Control notice:** This v2 document is historical and non-authoritative.
> The executable QWG-SIM-001 dormant-sweep prototype is formally retired and
> is not part of the current API. Neither this document nor QWG grants wallet
> action, execution, signing, broadcast or DigiByte consensus authority.

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

The historical QWG v2 design was intended to protect DigiByte and other
UTXO‑based chains at this critical layer: **wallet behaviour over time**. The
current runtime does not observe wallet behaviour over time; it evaluates one
caller-supplied, transaction-scoped `RiskContext` at a time.

---

## 2. Role in the 5‑Layer Quantum Shield

The historical design positioned QWG within a broader defensive architecture:

1. **Sentinel AI v2** – proposed node, mempool and chain-health monitoring
2. **DQSN v2** – proposed aggregation and scoring of multi-node threat signals
3. **ADN v2** – proposed local defensive signaling, without final execution
   authority
4. **Guardian Wallet v2** – proposed user-facing wallet guard and UX controls
5. **Quantum Wallet Guard v2 (QWG)** – proposed analysis of wallet-flow
   patterns

The design also described an **Adaptive Core** that could learn from those
layers and propose policy or threshold updates. That description does not grant
QWG, Adaptive Core or any upstream signal execution authority. AdamantineOS
remains the final fail-closed policy and execution boundary for Shield
evidence.

Within that historical design, QWG was the specialist for **patterns of fund
movement**, especially those that could indicate **quantum-style attacks**.
The current QWG runtime implements only the transaction-scoped decision
contract described in Sections 5 and 6.

---

## 3. Threat Model

The historical design did not propose replacing post-quantum cryptography. It
assumed that the cryptographic layer would eventually be upgraded while
behavioural early-warning concepts were explored separately.

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

The historical design considered patterns such as:

- **Dormant Key Sweep** – many old, inactive wallets suddenly moving
  toward one or a few aggregation points.
- **Multi‑Wallet Drain** – coordinated withdrawals from many related
  addresses in a short window.
- **Escalating Probe** – small test transactions followed by
  increasingly larger sums if no protection triggers.
- **Entropy‑Weak Rhythm** – repeated signing with suspiciously regular
  timing or volume (indicative of scripted or automated control).

These proposed patterns span multiple transactions and wallets. They are
retained here as historical threat-model context only; the current runtime does
not detect, correlate or label them.

---

## 4. Design Goals

QWG is built around several guiding principles:

1. **Non‑invasive** – no changes to DigiByte consensus or crypto.
2. **Composable** – works as a module in a larger security stack.
3. **Observable & Explainable** – decisions carry reasons and stable reason
   identifiers.
4. **Chain‑agnostic** – designed for DigiByte first, but other UTXO
   chains can reuse it.
5. **Adaptive‑ready** – can emit optional evidence to a caller-supplied
   integration sink.

The current implementation provides policy evidence to an integrating system.
It does not itself execute, sign, broadcast, freeze or reject a transaction.

---

## 5. Core Concepts

### 5.1 Quantum‑Style Risk Score (QRS)

The historical design proposed a **Quantum‑Style Risk Score (QRS)**:

- Integer range `0–100`
- Aggregates multiple signals:
  - timing and rhythm of withdrawals
  - number of wallets involved
  - UTXO fragmentation and recombination patterns
  - destination clustering (aggregation addresses)
  - policy‑driven flags from DQSN / Sentinel / Guardian
- Mapped to levels: `LOW`, `ELEVATED`, `HIGH`, `CRITICAL`

The current QWG decision engine does not implement this multi-wallet score,
its proposed feature aggregation or its pattern labels. The concept is
retained only as historical design context and cannot be cited as current API
behaviour or attack-detection evidence.

### 5.2 RiskContext

`RiskContext` is a transaction-scoped snapshot. It carries Sentinel and ADN
risk levels, a DQSN network score, wallet balance, transaction amount, address
age, behaviour score and device-trust data. It does not maintain multi-wallet
sweep history or destination-clustering state.

### 5.3 Engine and Policies

`DecisionEngine` evaluates a supplied `RiskContext` under `WalletPolicy` and
returns a `DecisionResult`. Current policy fields cover full-balance
protection, external-risk tolerance, transaction ratios, cooldowns,
behaviour/device checks and an extra-authentication amount.

The separation between engine and policy keeps thresholds explicit. Any policy
change remains subject to validation by the integrating system.

---

## 6. Architecture Overview

At code level (see README for file listing), the main components are:

- `engine.py` – implements `DecisionEngine`, the transaction-policy entry
  point.
- `risk_context.py` – defines the transaction-scoped security snapshot.
- `policies.py` – defines `WalletPolicy`.
- `decisions.py` – defines decision values and structured results.
- `adaptive_bridge.py` – provides optional best-effort evidence emission.
- `examples/` – contains maintained transaction-policy examples.
- `tests/` – covers current engine, policy, decision and bridge behaviour.

Integration constructs a validated `RiskContext`, evaluates it with
`DecisionEngine`, and interprets the result under the integrator's own final
policy.

---

## 7. Dormant Key Sweep Scenario (QWG‑SIM‑001)

`QWG-QuantumAttackScenario-1.md` is retained as a historical,
documentation-only threat scenario. It describes a synthetic sequence in
which wallets `A`, `B` and `C` move UTXOs toward aggregation addresses `X1`
and `X2`.

The executable prototype and its associated test are formally retired because
the proposed multi-event analytics contract is not part of the current
runtime. The illustrative scores and labels in the scenario were not produced
by current QWG code and must not be used as implementation, coverage or attack
detection evidence.

---

## 8. Integration Paths

The current decision component can be evaluated for possible use by
DigiByte-aligned systems. Every integration must validate its inputs and retain
its own final policy and execution boundary.

### 8.1 Exchanges and Custodians

- Evaluate transaction-scoped context before a withdrawal.
- Interpret warnings, delays, blocks or extra-authentication requests under
  independently controlled policy.
- A separate integration could emit anonymised evidence to a caller-supplied
  sink; any later use remains outside QWG authority.

### 8.2 DigiDollar Infrastructure

DigiDollar stability and oracle components could supply transaction and
external-risk context for local evaluation of:

- large rebalancing transactions
- cross‑chain bridge movements
- transaction-scoped treasury or oracle operations.

### 8.3 High‑Value Personal or Institutional Wallets

Advanced users or institutions holding large long‑term positions can
run QWG as part of a **local security stack**:

- An application can evaluate a transaction context before broadcast.
- Wallet UX can present the returned decision and reason.
- A separate, authoritative component decides whether any restriction is
  appropriate.

---

## 9. Relationship to Post‑Quantum Cryptography

QWG does **not** attempt to implement or replace post‑quantum
signatures. Instead, it acknowledges that:

- PQC migration will take time.
- There may be multiple candidate schemes and transition phases.
- Even after PQC adoption, **behavioural anomalies remain valuable
  indicators of compromise**.

Behavioural policy evidence may remain useful **before, during and after** PQC
migration:

- **Before** – to evaluate current transaction and external-risk signals.
- **During** – to complement, but never replace, cryptographic migration
  controls.
- **After** – as one input to independently controlled wallet policy.

---

## 10. Limitations

QWG is intentionally scoped:

- It does not claim mathematical proof of quantum attack.
- It depends on integrators supplying correct context data.
- It can generate false positives if policies are too aggressive.
- It does not implement the retired multi-wallet dormant-sweep analytics
  design.
- It does not sign, broadcast, freeze funds or change consensus.
- It does not see off‑chain social engineering or phishing on its own
  (this is where Guardian Wallet v2 contributes).

For these reasons, QWG is best deployed in environments where **humans
or higher‑level systems remain in the loop** to interpret alerts.

---

## 11. Roadmap

This historical v2 whitepaper is not deployment authorization. The current
implementation, tests and controlled release evidence must be evaluated
directly before any staging or integration decision.

Planned future directions include:

- separately specified and implemented behavioural analytics
- deeper integration with Sentinel AI v2 and DQSN v2 signals
- optional cryptographic hooks to distinguish legacy vs PQC addresses
- policy sets tuned for different risk profiles (retail vs custodial vs
  treasury)

Roadmap items are proposals, not current capabilities.

---

## 12. Conclusion

DigiByte has always been about **security, speed and forward thinking**.
Quantum Wallet Guard (QWG) extends that philosophy into the wallet
layer, where human behaviour, automation and future quantum threats all
intersect.

This whitepaper records the historical v2 motivation and design. Current QWG
code provides explainable transaction-policy decisions, while the retired
dormant-sweep concept remains documentation only. Capability claims must come
from implemented code, tests and controlled evidence, not from this paper.

The repository is open under the MIT license for review and development.

For questions, experimentation or collaboration, please contact:

**DarekDGB**.
