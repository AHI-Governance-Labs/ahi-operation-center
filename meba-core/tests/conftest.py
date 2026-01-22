import os
import sys

# Get the absolute path to the src directory of the current package
# This assumes conftest.py is in tests/ and the package is in src/
# We go up one level from tests/ to the root of the package (e.g. meba-core/)
# and then add src/ to the path.
package_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(package_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)
