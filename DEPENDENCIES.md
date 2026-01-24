# Dependency Audit Report

## Current Versions and Constraints

### Root (`.`)
*   **numpy**: `>=1.21.0, <3.0.0` (Pinned to allow v1 and v2, preventing v3)
*   **Dev Dependencies**:
    *   `pytest`: `>=7.0.0, <10.0.0`
    *   `pytest-cov`: `>=4.0.0, <8.0.0`
    *   `flake8`: `>=6.0.0, <8.0.0`

### MEBA Core (`meba-core`)
*   **Dependencies**: None. (Removed unused `numpy` dependency).

### SAP Pilot Kit (`sap-pilot-kit`)
*   **numpy**: `>=1.21.0, <3.0.0`

## Security Notes
*   **Audit Date**: 2024-05-22 (Simulated)
*   **Tool**: `pip-audit`
*   **Findings**: No known vulnerabilities found in installed packages.
*   **Note on `greenlet`**: Found outdated version (3.3.0 vs 3.3.1) in environment, likely a transitive dependency. Not a direct dependency of project.

## Upgrade Recommendations
1.  **Numpy**: The project is compatible with both NumPy 1.x (tested 1.26.4) and 2.x (tested 2.4.1). Constraints have been updated to `<3.0.0` to ensure stability while allowing current versions.
2.  **MEBA Core**: `numpy` was removed as it was unused in the source code.
3.  **Future Upgrades**: Monitor for `numpy` 3.0.0 release.
4.  **Root Build**: The root directory lacks a `src` layout, causing `pip install -e .` to fail with setuptools discovery errors. Consider refactoring root into a proper package structure or using a workspace tool if intended as a monorepo root.
