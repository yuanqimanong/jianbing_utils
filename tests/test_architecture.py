"""验证通用工具库可脱离应用与第三方运行时使用。"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"


def test_public_utility_imports_work_without_site_packages() -> None:
    script = f"""
import sys
sys.path.insert(0, {str(_SRC)!r})
from jianbing_utils import crypto, text
from jianbing_utils.retry import BackoffPolicy, retry_async
from jianbing_utils.s3.planning import count_parts
assert crypto.sha256('abc')
assert text.snake_case('helloWorld') == 'hello_world'
assert BackoffPolicy().delay(10000) == 30.0
assert count_parts(11, 5) == 3
assert not any(name in sys.modules for name in ('boto3', 'botocore', 'payipa', 'pyp_server'))
"""
    subprocess.run([sys.executable, "-S", "-c", script], check=True, timeout=15, capture_output=True)


def test_policy_layers_do_not_import_adapters_or_applications() -> None:
    allowed = {
        "retry/policy.py": set(),
        "s3/planning.py": {"jianbing_utils.s3.constants"},
    }
    for relative, utility_imports in allowed.items():
        tree = ast.parse((_SRC / "jianbing_utils" / relative).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
        for name in imports:
            if name.startswith("jianbing_utils"):
                assert name in utility_imports, (relative, name)
            else:
                assert name.split(".")[0] in sys.stdlib_module_names, (relative, name)
