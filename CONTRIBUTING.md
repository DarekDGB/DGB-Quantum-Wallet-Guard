# Contributing to Quantum Wallet Guard (QWG)

**Quantum Wallet Guard (QWG)** is the *user-side protection layer* of the DigiByte Quantum Shield.  
It provides behavioural analysis, PQC-ready transaction verification, rule-based defence,  
and integrates with ADN v2 and Guardian Wallet.

QWG is a **reference architecture**.  
Contributions must **strengthen user safety**, never weaken it.

---

## ✅ What Contributions Are Welcome

### ✔️ 1. Behavioural & Heuristic Improvements
- new anomaly detectors  
- transaction pattern classifiers  
- better fee sanity logic  
- expanded rule sets  

### ✔️ 2. PQC Extensions
- improvements to signature adapters  
- support for new PQC schemes (Falcon / Dilithium variants)  
- performance and verification refinements  

### ✔️ 3. Defence Logic & Runtime Enhancements
- smarter guard_runtime strategies  
- additional defence conditions  
- improved integration with ADNv2 playbooks  

### ✔️ 4. Guardian Wallet Integration
- better warnings or UX signals  
- improved prompt structures  
- new classification categories  

### ✔️ 5. Testing & Simulation
- unit tests  
- behavioural simulations  
- fuzz tests  
- mock ADN scenarios  

### ✔️ 6. Documentation Improvements
Clarity, architecture diagrams, examples, explanations.

---

## ❌ What Will Not Be Accepted

### 🚫 1. Removing or Weakening Defence Logic
QWG **must never**:

- remove critical checks  
- weaken behavioural analysis  
- silence warnings  
- reduce rule coverage  

Any removal of core protections will be **rejected immediately**.

### 🚫 2. Adding Consensus or Node Logic
QWG is *user-side only*.  
It must not:

- change network rules  
- modify block or mempool logic  
- become a validator or signing authority  

### 🚫 3. Turning QWG Into a Wallet UI  
QWG **feeds Guardian Wallet**, but is not a UI itself.  
Do NOT add:

- screens  
- UX components  
- app logic  

### 🚫 4. Black-Box or Unexplained AI
All defence decisions must be:

- explainable  
- auditable  
- deterministic  

No opaque models will be accepted.

### 🚫 5. Security-reducing dependencies
No unsafe libraries or frameworks.

---

## 🧱 Design Principles

1. **User First** — protect users by default.  
2. **Fail-Safe** — on uncertainty → warn or block.  
3. **Explainability** — every action has a reason.  
4. **Determinism** — same input → same output.  
5. **Zero-Trust** — environment is treated as potentially hostile.  
6. **Modularity** — each defence lives in its own module.  
7. **Interoperability** — works cleanly with ADN, Guardian Wallet, and Adamantine.

---

## 🔄 Pull Request Expectations

Your PR should include:

- a clear explanation of your change  
- motivation: why this improves QWG  
- tests when adding or modifying logic  
- no breaking of folder structure  
- no removal of architectural components  
- updated documentation if needed  

The architect (@DarekDGB) reviews **direction**.  
Developers review **technical implementation**.

---

## 📝 License

By contributing, you agree that your contributions are licensed under the MIT License.

© 2025 **DarekDGB**
