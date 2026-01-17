# AHI Governance Labs — Contribution Guidelines

---

## 1. Purpose

AHI Governance Labs maintains open technical tooling to support **event-level governance**, **auditing**, and **certification** of AI systems.

> **Contributions are welcome only if they preserve the following principles:**
> - Deterministic behavior
> - Auditability
> - Reproducibility
> - Zero-knowledge processing (no semantic content)

### Important Notice

**This is not a general-purpose AI project.**  
It is an auditing and governance infrastructure.

---

## 2. Scope of Contributions

### Accepted Contributions

We accept contributions related to:

| Category | Description |
|----------|-------------|
| **Code improvements** | Performance, clarity, robustness for SAP tooling |
| **Bug fixes** | Resolution of identified issues |
| **Test coverage** | Enhancements to test suites |
| **Documentation** | Technical accuracy corrections only |
| **Reproducibility** | Improvements to deterministic execution |

> All contributions must be **technically justified**.

### Explicitly Out of Scope

The following will **not** be accepted:

- Content moderation logic
- Ethical or moral filters
- Semantic analysis of prompts or outputs
- Alignment heuristics
- Opinionated governance proposals not grounded in metrics
- Marketing content

```
We govern entropy and structure, not meaning or intent.
```

---

## 3. Core Principles (Non-Negotiable)

All contributions must comply with these principles:

### 3.1 Event-Centric Governance

- Governance applies to **execution events**, not persistent entities
- No assumptions of identity, intent, or consciousness are allowed

### 3.2 Determinism and Falsifiability

- State transitions must be **deterministic**
- Any metric must be **reproducible** by an independent auditor
- Non-falsifiable logic will be **rejected**

### 3.3 Zero-Knowledge by Design

- **No** prompts, outputs, or semantic payloads may be read, logged, stored, or inferred
- Contributions introducing content access will be **rejected immediately**

### 3.4 Fail-Safe Bias

- Fast failure is preferred over graceful degradation
- Recovery must be slower and more expensive than failure

---

## 4. Repository-Specific Rules

### 4.1 Code Repositories `[MIT Licensed]`

**Applies to repositories such as:**
- `sap-protocol-core`
- `meba-core`

**Requirements:**

```
→ Clear function boundaries
→ Explicit state machines
→ No hidden side effects
→ Unit tests for any new logic
```

**By contributing code, you agree that:**
1. Your contribution is licensed under the **MIT License**
2. You grant AHI Governance Labs the right to use it without additional restrictions

---

### 4.2 Standards and Certification Repositories `[CC BY-NC-SA 4.0]`

**Applies to repositories such as:**
- `ahi-governance-standards`
- `ahi-certification-kit`
- `sap-training-program`

**Requirements:**

| Requirement | Description |
|-------------|-------------|
| **Precise language** | No ambiguity allowed |
| **No speculative claims** | Evidence-based only |
| **No commercial reuse** | Non-commercial license |
| **Versioned changes** | With clear rationale |

> Contributions here are **normative**, not experimental.

---

## 5. Contribution Process

```mermaid
Fork → Branch → Changes → Tests → PR → Review
```

**Step-by-step:**

1. **Fork** the repository
2. **Create** a feature branch with a descriptive name
3. **Make changes** with clear commit messages
4. **Add or update** tests if applicable
5. **Submit** a Pull Request (PR)

### Each PR must include:

- [ ] Clear description of the change
- [ ] Technical rationale
- [ ] Impact assessment on auditability or determinism

---

## 6. Review and Acceptance Criteria

Pull Requests are evaluated on:

| Criterion | Weight |
|-----------|--------|
| Technical correctness | **CRITICAL** |
| Alignment with SAP principles | **CRITICAL** |
| Impact on reproducibility | **HIGH** |
| Risk to audit integrity | **HIGH** |

### Possible outcomes:

- **Accepted** — Merged into codebase
- **Rejected** — Not aligned with principles
- **Revision Requested** — Changes needed

> Rejection does not require consensus or debate.

---

## 7. Authority and Final Decision

**Final authority on all contributions rests with AHI Governance Labs.**

This includes the right to:

```
→ Reject contributions without justification
→ Modify accepted contributions
→ Revoke contributor access in case of violations
```

> This project prioritizes **system integrity** over openness for its own sake.

---

## 8. Reporting Issues and Vulnerabilities

Security or integrity issues must be reported **privately**.

### Do NOT open public issues for:

- Vulnerabilities
- Bypass techniques
- Exploit vectors

### Contact:

```
enterprise@ahigovernance.com
```

---

## 9. Code of Conduct (Minimal)

| Principle | Meaning |
|-----------|---------|
| **Be precise** | Technical accuracy required |
| **Be technical** | Focus on implementation |
| **Be respectful** | Professional communication |
| **Do not anthropomorphize** | Systems are not entities |
| **Do not introduce ideology** | Metrics-based only |

**Violations result in removal.**

---

## 10. Legal Notice

Contributing does **not** grant rights to:

- Offer certification services
- Use SAP branding
- Represent AHI Governance Labs

```
Certification authority is not open-source.
```

---

## Status

This `CONTRIBUTING.md` is **normative**.

By submitting a contribution, you acknowledge and accept these terms.

---

**Document Version:** 1.0  
**Last Updated:** 2025-01  
**Authority:** AHI Governance Labs
