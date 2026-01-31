# Sentinel's Journal

## 2026-01-22 - Static Site Reverse Tabnabbing
**Vulnerability:** Multiple `target="_blank"` links in static HTML files lacked `rel="noopener noreferrer"`.
**Learning:** Static sites often bypass security scanning pipelines focused on backend code (Python/JS). Developers copy-paste links without security attributes.
**Prevention:** Use a linter (like `HTMLHint` or `eslint-plugin-html`) or a pre-commit hook to scan for `target="_blank"` without `rel="noopener"`.
