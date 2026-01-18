# Security Policy — AHI Operation Center

---

## 1. Scope

This security policy applies to all components in the AHI Operation Center repository:

| Component | Scope |
|-----------|-------|
| **meba-core/** | MEBA Calculator implementation |
| **sap-pilot-kit/** | SAP Protocol implementation and tooling |
| **sitios-web/** | Web platforms |
| **ahi-gov/** | API Gateway configuration |

For component-specific security details, see:
- [SAP Pilot Kit SECURITY.md](./sap-pilot-kit/SECURITY.md)

---

## 2. Reporting Vulnerabilities

### Private Disclosure Required

All security vulnerabilities **MUST** be reported privately.

**Do NOT:**
- Open public GitHub issues
- Publish proof-of-concept exploits
- Share vulnerability details publicly

### Contact

| Method | Details |
|--------|---------|
| **Email** | enterprise@ahigovernance.com |
| **Subject** | `[SECURITY] Vulnerability Disclosure` |

### Required Information

A valid security report must include:

1. **Description** — Clear explanation of the vulnerability
2. **Component** — Affected repository component and version
3. **Reproduction** — Steps to reproduce (keep confidential)
4. **Impact** — Assessment of potential impact

---

## 3. Security Considerations

### Python Components (meba-core, sap-pilot-kit)

- No external network calls
- No persistent storage of sensitive data
- Deterministic, reproducible execution

### Web Components (sitios-web)

- Static HTML/CSS only
- No server-side processing
- No user data collection

### API Configuration (ahi-gov)

- Cloud Build configuration only
- No credentials stored in repository

---

## 4. Response Timeline

| Phase | Timeline |
|-------|----------|
| Acknowledgment | Within 72 hours |
| Initial Assessment | Within 7 days |
| Resolution | Dependent on severity |

---

## 5. Dependencies

This project uses minimal dependencies:

| Dependency | Purpose | Security Notes |
|------------|---------|----------------|
| **numpy** | Numerical computations | Well-maintained, secure |
| **pytest** | Testing (dev only) | Not in production |

---

## 6. Supported Versions

| Version | Supported |
|---------|-----------|
| main branch | ✅ Yes |
| Other branches | ❌ No |

---

## Legal Notice

This policy does **not** grant permission to:

- Perform unauthorized testing on production systems
- Access customer environments
- Disclose vulnerabilities without coordination

---

**Document Version:** 1.0  
**Authority:** AHI Governance Labs
