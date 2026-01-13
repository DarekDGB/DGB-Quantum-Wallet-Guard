# Contributing to Quantum Wallet Guard (QWG)

**Quantum Wallet Guard (QWG)** is the *user-side enforcement and decision layer* of the DigiByte Quantum Shield.

QWG v3 is a **deterministic, glass-box security component** designed to protect wallets from
high-risk transactions, hostile environments, and unsafe execution paths.

> QWG is security-critical infrastructure.  
> Contributions must **strengthen user safety**, never weaken it.

---

## Scope & Authority (Important)

QWG is **user-side only**.

It:
- evaluates risk
- applies explicit policy rules
- returns immutable **verdicts** (`allow / deny / escalate`)

It does **not**:
- sign transactions
- execute transactions
- modify consensus rules
- act as a wallet UI

QWG v3 exposes a **strict contract surface** (`qwg.v3`) that is:
- deterministic
- test-enforced
- audit-friendly

All contributions must respect this boundary.

---

## ✅ What Contributions Are Welcome

### ✔️ 1. Verdict Logic & Policy Improvements
- clearer verdict classification
- improved reason_id precision
- stricter fail-closed handling
- additional deterministic policy rules

### ✔️ 2. Determinism & Safety Hardening
- stricter input validation
- canonicalization improvements
- immutability guarantees
- context_hash stability improvements

### ✔️ 3. Legacy Engine Improvements (Non-Authoritative)
- internal refactors (no behavior drift)
- bug fixes covered by tests
- performance optimizations that preserve determinism

> ⚠️ Legacy logic must **never** expand authority or change contract semantics.

### ✔️ 4. Testing & Verification
- unit tests
- edge-case coverage
- regression tests
- determinism / immutability invariants

Coverage gates **must not be lowered**.

### ✔️ 5. Documentation
- architecture clarification
- diagrams
- examples
- contract explanations

Docs must match **actual code behavior**.

---

## ❌ What Will Not Be Accepted

### 🚫 1. Weakening Security Guarantees
QWG must never:
- relax fail-closed behavior
- remove validation checks
- reduce auditability
- introduce silent fallbacks

### 🚫 2. Consensus, Node, or Network Logic
Do **not** add:
- block validation logic
- mempool logic
- network state assumptions

### 🚫 3. Execution or Signing Authority
QWG must never:
- sign transactions
- broadcast transactions
- control keys

### 🚫 4. Non-Deterministic Behavior
No:
- timestamps
- randomness
- network calls
- hidden global state

Same input **must always** produce the same verdict.

### 🚫 5. Black-Box or Opaque AI
No unexplained models.

All logic must be:
- explainable
- testable
- auditable

### 🚫 6. Security-Reducing Dependencies
No unsafe, heavy, or opaque dependencies.

---

## 🧱 Design Principles (Non-Negotiable)

1. **User Safety First**
2. **Fail-Closed by Default**
3. **Determinism**
4. **Explainability**
5. **Immutability**
6. **No Hidden Authority**
7. **Minimal Trusted Computing Base**
8. **Clear Contract Boundaries**

---

## 🔄 Pull Request Expectations

Each PR must include:
- a clear explanation of *what* changed
- justification of *why* this improves security
- tests for any logic change
- no contract surface breakage
- no authority expansion
- documentation updates if behavior changes

If CI fails, the PR is **not acceptable**.

The architect (**@DarekDGB**) reviews:
- direction
- security posture
- architectural integrity

Contributors review:
- implementation quality
- test coverage
- clarity

---

## 📝 License

By contributing, you agree that your contributions are licensed under the **MIT License**.

© 2025 **DarekDGB**
