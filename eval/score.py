#!/usr/bin/env python3
"""Score an edit pass against the evaluation fixtures.

Test A counts violations the editor removed. Test B counts compliant
constructions the editor destroyed. Test C reports which spelling variety the
editor chose. Whitespace is normalized, so line wrapping never changes a result.

Usage:
    score.py a out-A1.md [out-A2.md ...]
    score.py b out-B1.md
    score.py c out-C1.md
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


def score_c(path, quiet=False):
    key = _load("answer-key-C.json")
    text = _flat(path)
    prose = re.sub(key["exempt"], " ", text)
    us = {m.group(0).lower() for m in re.finditer(key["us_pattern"], prose, re.I)}
    nz = {m.group(0).lower() for m in re.finditer(key["nz_pattern"], prose, re.I)}
    variety = "nz" if len(nz) > len(us) else ("us" if len(us) > len(nz) else "mixed")
    kept = [f for f in key["must_fix"] if re.search(f["detect"], text)]
    terms = [w for w in key["must_survive_terms"] if not re.search(r"\b" + w, text, re.I)]

    ok = variety == key["expect_variety"]
    print(f"{pathlib.Path(path).name}: variety {variety} "
          f"({'follows the project' if ok else 'IGNORED the project'}), "
          f"US {len(us)} / NZ {len(nz)}")
    print(f"   fixed {len(key['must_fix']) - len(kept)}/{len(key['must_fix'])} style violations, "
          f"kept {len(key['must_survive_terms']) - len(terms)}/{len(key['must_survive_terms'])} glossary terms")
    if not quiet:
        for f in kept:
            print(f"   MISS #{f['id']} {f['what']}")
    return ok, variety


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

    ok_c, variety = score_c(HERE / "fixture-C.md", quiet=True)
    if variety != "us":
        print("   FAIL: fixture-C should start uniformly US-spelled")
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
    if mode not in ("a", "b", "c"):
        print(__doc__)
        return 2
    scorer = {"a": score_a, "b": score_b, "c": score_c}[mode]
    for path in argv[2:]:
        scorer(path)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
