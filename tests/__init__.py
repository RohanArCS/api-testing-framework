"""Ensure that the `src` directory is importable in tests.

Pytest collects tests as modules, and sometimes the package under test is not
installed into the Python environment.  To allow `import src.api_client` to
work without installing the package, we append the project's `src` directory to
`sys.path` at test discovery time.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
src_path = project_root / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))