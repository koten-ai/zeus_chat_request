#!/usr/bin/env python3
"""Verify a v2/base/base-<id> pack has required files and wire invariants.

Usage:
  python3 scripts/verify_base_pack.py --base 5
  python3 scripts/verify_base_pack.py --base 5.1
  python3 scripts/verify_base_pack.py --base 5.2

Rules (major >= 5, e.g. 5, 5.1, 5.2):
  - business_rules_triggers type object
  - app_output on schema + return tool
  - _lineage.base_id matches base-<id> on every min catalog
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def major_n(base: str) -> float:
    """5, 5.1, 5.2 → major 5 for wire checks."""
    m = re.match(r"^(\d+)", str(base))
    return float(m.group(1)) if m else 0.0


def check_pack(repo: Path, base: str) -> list[str]:
    errors: list[str] = []
    base_id = f"base-{base}" if not str(base).startswith("base-") else str(base)
    # normalize: base arg may be "5.1" or "base-5.1"
    if base_id.startswith("base-base-"):
        base_id = base_id.replace("base-base-", "base-", 1)
    bare = base_id.removeprefix("base-")
    pack = repo / "v2" / "base" / base_id

    if not pack.is_dir():
        return [f"missing pack directory: {pack}"]

    required = [
        pack / "MANIFEST.json",
        pack / "README.md",
        pack / "OVERVIEW.md",
        pack / "response_output_schema.json",
        pack / "response_output_example.json",
        pack / "min",
        pack / "text",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"missing required path: {p.relative_to(repo)}")

    min_dir = pack / "min"
    catalogs = sorted(min_dir.glob("chat_request*.json")) if min_dir.is_dir() else []
    if not catalogs:
        errors.append(f"no chat_request*.json under {min_dir.relative_to(repo)}")

    wire5 = major_n(bare) >= 5

    schema_path = pack / "response_output_schema.json"
    if schema_path.is_file():
        schema = load_json(schema_path)
        br = (schema.get("properties") or {}).get("business_rules_triggers") or {}
        if wire5:
            if br.get("type") != "object":
                errors.append(
                    f"schema business_rules_triggers.type must be object for {base_id}, got {br.get('type')!r}"
                )
            if "app_output" not in (schema.get("properties") or {}):
                errors.append(f"schema missing app_output for {base_id}")
        if bare.startswith("5.2") or bare == "5.2":
            if "data_gaps" not in (schema.get("properties") or {}):
                errors.append(f"schema missing data_gaps for {base_id} (base-5.2 train)")

        example_path = pack / "response_output_example.json"
        if example_path.is_file():
            example = load_json(example_path)
            for req in ("summary", "query_decomposition", "decomposition", "confidence"):
                if req not in example:
                    errors.append(f"example missing required field {req}")
            if wire5:
                tr = example.get("business_rules_triggers")
                if tr is not None and not isinstance(tr, dict):
                    errors.append(
                        f"example business_rules_triggers must be object for {base_id}, got {type(tr).__name__}"
                    )

    for path in catalogs:
        doc = load_json(path)
        lin = doc.get("_lineage") or {}
        if lin.get("base_id") != base_id:
            errors.append(f"{path.name}: _lineage.base_id={lin.get('base_id')!r} want {base_id}")
        if f"base-{bare}" not in path.name and base_id not in path.name:
            errors.append(f"{path.name}: filename does not contain {base_id}")

        for v in doc.get("verbs") or []:
            fn = v.get("function") if isinstance(v, dict) and "function" in v else v
            if not isinstance(fn, dict):
                continue
            props = ((fn.get("parameters") or {}).get("properties")) or {}
            name = fn.get("name")
            br = props.get("business_rules_triggers")
            if br is not None and wire5:
                if br.get("type") != "object":
                    errors.append(
                        f"{path.name} verb {name}: business_rules_triggers.type={br.get('type')!r} want object"
                    )
            if name == "return" and wire5:
                if "app_output" not in props:
                    errors.append(f"{path.name} return tool missing app_output property")
                for req in ("summary", "query_decomposition", "decomposition", "confidence"):
                    if req not in props:
                        errors.append(f"{path.name} return tool missing {req}")
                if bare.startswith("5.2") and "data_gaps" not in props:
                    errors.append(f"{path.name} return tool missing data_gaps (base-5.2)")

        text_path = pack / "text" / path.name.replace(".json", ".txt")
        alt = pack / "text" / f"{path.stem}.txt"
        if not text_path.is_file() and not alt.is_file():
            mode = (doc.get("_lineage") or {}).get("mode")
            if mode:
                t2 = pack / "text" / f"chat_request_{mode}_base-{bare}.txt"
                if not t2.is_file():
                    errors.append(f"missing text export for {path.name}")

    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--base",
        required=True,
        help="BASE id without 'base-' prefix (e.g. 5, 5.1, 5.2) or full base-5.1",
    )
    ap.add_argument("--repo-root", default=".", help="Repo root")
    ap.add_argument("--strict", action="store_true", help="unused; always exit 1 on fail")
    args = ap.parse_args(argv)
    repo = Path(args.repo_root).resolve()
    base = str(args.base).removeprefix("base-")
    errors = check_pack(repo, base)
    base_id = f"base-{base}"
    if not errors:
        print(f"OK {base_id} pack verification passed")
        return 0
    print(f"FAIL {base_id} ({len(errors)} issue(s)):", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
