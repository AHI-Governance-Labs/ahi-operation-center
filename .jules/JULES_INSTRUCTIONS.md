# 🤖 Jules Agent Instructions

**Generated:** 2026-01-29  
**Source:** Pre-Release Audit by Antigravity Agent  
**Priority:** Execute in order listed

---

## Overview

This document contains 11 prioritized tasks for the Jules agent to execute. Each task is a standalone prompt that can be executed independently, though the recommended order is top to bottom.

---

## PROMPT 1: Update Deploy Workflow for ethic-check

> **Priority:** HIGH  
> **Files:** `.github/workflows/deploy.yml`

```
Update the `.github/workflows/deploy.yml` file to also deploy the ethic-check site.

Current state: Only deploys ahigovernance and sovereignsymbiosis
Required: Add deployment for ethic-check

Add this line after line 41:
firebase deploy --only hosting:ethic-check --project cs-poc-aguy0wkzgf55jarewtxljk9 --token "${{ steps.auth.outputs.access_token }}"

Also update the workflow triggers in the 'paths' section to include:
- 'sitios-web/ethic-check/**'

Commit with message: "ci: add ethic-check to firebase deploy workflow"
```

---

## PROMPT 2: Clean Up Duplicate Documentation Folders

> **Priority:** MEDIUM  
> **Files:** `ahi-governance-docs/`, `documentos-de-gobernanza/`

```
The repository has duplicate documentation:
- `ahi-governance-docs/` (legacy, 8 items)
- `documentos-de-gobernanza/` (current, organized in 6 categories)

Task:
1. Verify all content from `ahi-governance-docs/` exists in `documentos-de-gobernanza/`
2. If yes, delete the `ahi-governance-docs/` folder entirely
3. Update any references in README.md or other files that point to the old folder
4. Commit with message "chore: consolidate documentation folders"
```

---

## PROMPT 3: Archive or Remove ahi-operation-center-v2 Folder

> **Priority:** MEDIUM  
> **Files:** `ahi-operation-center-v2/`

```
The folder `ahi-operation-center-v2/` contains 68 legacy files that appear to be from a previous iteration.

Task:
1. Review the contents and determine if any code is still actively used
2. If any code is needed, move it to the appropriate location in the main structure
3. Delete the entire `ahi-operation-center-v2/` folder
4. Commit with message "chore: remove v2 legacy folder"
```

---

## PROMPT 4: Consolidate Firebase Functions

> **Priority:** MEDIUM  
> **Files:** `functions/`, `alpha-core/`

```
There are two Firebase functions directories:
- `functions/` (8 files, older structure)
- `alpha-core/` (7 files, current per firebase.json)

Task:
1. Verify `firebase.json` only references `alpha-core` (it does, line 94-102)
2. Check if any code in `functions/` is unique and needed
3. If `functions/` is truly legacy with no unique code, delete it
4. Commit with message "chore: remove legacy functions folder"
```

---

## PROMPT 5: Update Pricing Model on ahigovernance.com

> **Priority:** HIGH  
> **Files:** `sitios-web/ahigovernance.com/index.html`

```
The current website mentions "3 auditorías de sistemas de IA gratis" which is not a sustainable business model.

Task:
1. Open `sitios-web/ahigovernance.com/index.html`
2. Find and replace any "3 auditorías gratis" or similar free tier messaging
3. Replace with a tiered pricing structure using these tiers:
   - Free: Documentation access, VIE Calculator (limited to 5 calculations/day)
   - Developer ($49/mo): API access, 1,000 ECP-1 verifications
   - Business ($299/mo): Unlimited verifications, monthly audit report
   - Enterprise: Contact for custom pricing, includes CRI™ certification
4. Ensure pricing cards maintain the current gold (#c9a227) and jade (#2d8a6e) color scheme
5. Commit with message "feat: update pricing model for sustainability"
```

---

## PROMPT 6: Add ethic-check Integration Banner to ahigovernance.com

> **Priority:** MEDIUM  
> **Files:** `sitios-web/ahigovernance.com/index.html`

```
Add a "Coming Soon" or "New Service" banner for the ECP-1 Ethical Captcha service on the ahigovernance.com homepage.

Task:
1. Open `sitios-web/ahigovernance.com/index.html`
2. Add a new section after the hero section (around line 350) with:
   - Section label: "NUEVO SERVICIO"
   - Title: "ECP-1 Captcha Ético"
   - Description: "Proteja sus sistemas contra automatizaciones de IA con verificación ética basada en dilemas constitucionales"
   - CTA button linking to the ethic-check site
   - Use the existing gold-dim/jade-dim styling classes
3. Commit with message "feat: add ECP-1 ethical captcha promotion banner"
```

---

## PROMPT 7: Add ELIZA Translator Research Announcement

> **Priority:** LOW  
> **Files:** `sitios-web/sovereignsymbiosis.com/index.html`

```
Add a research announcement for the ELIZA Translator project on sovereignsymbiosis.com.

Task:
1. Open `sitios-web/sovereignsymbiosis.com/index.html`
2. Find the publications/timeline section
3. Add a new timeline item with:
   - Status badge: "En Desarrollo" with purple background
   - Title: "ELIZA Translator: Protocolo de Intermediación Ética"
   - Description: "Bridge de comunicación cross-model con filtrado ético integrado"
   - Date: Current month/year
   - Use the existing timeline-item styling with the sigma class
4. Commit with message "feat: add ELIZA translator research announcement"
```

---

## PROMPT 8: Clean Empty Figures Folder

> **Priority:** LOW  
> **Files:** `figures/`

```
The `figures/` folder exists but appears to be empty or near-empty.

Task:
1. Check if the folder contains any files
2. If empty, delete the folder entirely
3. If it has contents, verify they are needed and add a README.md explaining what should be there
4. Note: The .gitignore line 89 mentions figures/*.png - this is fine to leave
5. Commit with message "chore: clean up figures directory"
```

---

## PROMPT 9: Fix Sovereign Symbiosis Footer Copyright in ethic-check

> **Priority:** LOW  
> **Files:** `sitios-web/ethic-check/index.html`

```
The ethic-check site footer references "Sovereign Symbiosis Research Foundation" but the main organization branding should be consistent.

Task:
1. Open `sitios-web/ethic-check/index.html`
2. Find the footer section (around line 723-729)
3. Update the copyright to: "© 2026 AHI Governance Labs • Powered by Sovereign Symbiosis Research"
4. Keep the link to sovereignsymbiosis.com for documentation
5. Ensure consistent branding pattern across all three sites
6. Commit with message "fix: unify footer branding across sites"
```

---

## PROMPT 10: Update Technical Debt Document Date

> **Priority:** LOW  
> **Files:** `TECHNICAL_DEBT.md`

```
The `TECHNICAL_DEBT.md` file shows "Date: October 26, 2023" which is outdated.

Task:
1. Update the date to "January 29, 2026"
2. At the end of the findings table, add this new row:
   | `.env` | - | Security | Critical | Was tracked in git with placeholder credentials | [FIXED] Removed from git tracking |
3. Commit with message "docs: update technical debt report date and add .env fix"
```

---

## PROMPT 11: Create ELIZA Translator Teaser Page

> **Priority:** LOW  
> **Files:** NEW: `sitios-web/sovereignsymbiosis.com/eliza.html`

```
Create a teaser landing page for the ELIZA Translator at sovereignsymbiosis.com/eliza.html

Task:
1. Create new file `sitios-web/sovereignsymbiosis.com/eliza.html`
2. Copy the basic structure from `index.html` (head, styles, header, footer)
3. Create a simple hero section with:
   - Badge: "Investigación en Progreso"
   - Title: "ELIZA Translator Protocol"
   - Subtitle: "Comunicación ética cross-model con preservación de intención"
   - Description paragraph explaining the concept
   - Email signup form placeholder (just UI, no backend)
   - "Volver a Sovereign Symbiosis" link
4. Use the existing purple accent color for this page
5. Commit with message "feat: add ELIZA translator teaser page"
```

---

## Execution Notes for Jules

1. **Test after each change** - Run `firebase serve` locally if possible
2. **Preserve styling** - The gold/jade color scheme is intentional, maintain it
3. **Spanish content** - Main content is in Spanish, keep it that way
4. **No breaking changes** - These are additive/cleanup changes only

---

*Generated by Antigravity Agent - 2026-01-29*
