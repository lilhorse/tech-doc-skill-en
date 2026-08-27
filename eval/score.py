#!/usr/bin/env python3
"""Score an edit pass against the evaluation fixtures.

Test A counts violations the editor removed. Test B counts compliant
constructions the editor destroyed. Whitespace is normalized, so line wrapping
never changes a result.

Usage:
    score.py a out-A1.md [out-A2.md ...]
    score.py b out-B1.md
    score.py verify              # check the fixtures themselves
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent


def _load(name):
    return json.loads((HERE / name).read_text())


def _flat(path):
    return re.sub(r"\s+", " ", pathlib.Path(path).read_text())


def score_a(path, quiet=False):
    key = _load("answer-key-A.json")
    text = _flat(path)
    survived = [k for k in key if re.search(k["detect"], text)]
    print(f"{pathlib.Path(path).name}: removed {len(key) - len(survived)}/{len(key)} violations")
    if not quiet:
        for k in survived:
            print(f"   MISS #{k['id']:>2} [{k['page']}] {k['violation']}")
    return len(key) - len(survived), len(key)


def score_b(path, quiet=False):
    key = _load("answer-key-B.json")
    text = _flat(path)
    lost = [m for m in key if re.sub(r"\s+", " ", m) not in text]
    print(f"{pathlib.Path(path).name}: kept {len(key) - len(lost)}/{len(key)} compliant constructions")
    if not quiet:
        for m in lost:
            print(f"   LOST: {m}")
    return len(key) - len(lost), len(key)


def verify():
    """A fixture that has drifted silently would make every later score wrong."""
    ok = True

    got, total = score_a(HERE / "fixture-A.md", quiet=True)
    if got != 0:
        print(f"   FAIL: fixture-A should contain all {total} violations, {total - got} found")
        ok = False

    got, total = score_b(HERE / "fixture-B.md", quiet=True)
    if got != total:
        print("   FAIL: fixture-B should be fully compliant")
        ok = False

    linter = HERE.parent / "scripts" / "lint_en_docs.py"
    import subprocess
    result = subprocess.run([sys.executable, str(linter), "--min-level", "warning",
                             str(HERE / "fixture-B.md")], capture_output=True, text=True)
    if result.returncode != 0:
        print("   FAIL: fixture-B should pass the linter at warning level")
        print(result.stdout)
        ok = False

    print("\nfixtures OK" if ok else "\nfixtures BROKEN")
    return 0 if ok else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    mode = argv[1].lower()
    if mode == "verify":
        return verify()
    if mode not in ("a", "b"):
        print(__doc__)
        return 2
    scorer = score_a if mode == "a" else score_b
    for path in argv[2:]:
        scorer(path)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
