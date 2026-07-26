#!/usr/bin/env python3
"""Verify a v2/base/base-N pack has required files and base-N wire invariants.

Usage:
  python3 scripts/verify_base_pack.py --base 5
  python3 scripts/verify_base_pack.py --base 5 --strict   # exit 1 on any failure

Rules (N >= 5):
  - business_rules_triggers in response_output_schema and return tools must be type object
  - app_output present on return tool parameters
  - _lineage.base_id matches base-N on every min catalog
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def check_pack(repo: Path, base_n: int) -> list[str]:
    errors: list[str] = []
    pack = repo / "v2" / "base" / f"base-{base_n}"
    base_id = f"base-{base_n}"

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

    schema_path = pack / "response_output_schema.json"
    if schema_path.is_file():
        schema = load_json(schema_path)
        br = (schema.get("properties") or {}).get("business_rules_triggers") or {}
        if base_n >= 5:
            if br.get("type") != "object":
                errors.append(
                    f"schema business_rules_triggers.type must be object for {base_id}, got {br.get('type')!r}"
                )
            if "app_output" not in (schema.get("properties") or {}):
                errors.append(f"schema missing app_output for {base_id}")

        example_path = pack / "response_output_example.json"
        if example_path.is_file():
            example = load_json(example_path)
            # structural: required four
            for req in ("summary", "query_decomposition", "decomposition", "confidence"):
                if req not in example:
                    errors.append(f"example missing required field {req}")
            if base_n >= 5:
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
        if not path.name.endswith(f"_{base_id}.json") and f"_base-{base_n}." not in path.name:
            # allow chat_request_MODE_base-N.json
            if f"base-{base_n}" not in path.name:
                errors.append(f"{path.name}: filename does not contain base-{base_n}")

        for v in doc.get("verbs") or []:
            fn = v.get("function") if isinstance(v, dict) and "function" in v else v
            if not isinstance(fn, dict):
                continue
            props = ((fn.get("parameters") or {}).get("properties")) or {}
            name = fn.get("name")
            br = props.get("business_rules_triggers")
            if br is not None and base_n >= 5:
                if br.get("type") != "object":
                    errors.append(
                        f"{path.name} verb {name}: business_rules_triggers.type={br.get('type')!r} want object"
                    )
            if name == "return" and base_n >= 5:
                if "app_output" not in props:
                    errors.append(f"{path.name} return tool missing app_output property")
                for req in ("summary", "query_decomposition", "decomposition", "confidence"):
                    if req not in props:
                        errors.append(f"{path.name} return tool missing {req}")

        text_path = pack / "text" / path.name.replace(".json", ".txt")
        # text stem uses base-N
        alt = pack / "text" / f"{path.stem}.txt"
        if not text_path.is_file() and not alt.is_file():
            # try mode pattern
            mode = (doc.get("_lineage") or {}).get("mode")
            if mode:
                t2 = pack / "text" / f"chat_request_{mode}_base-{base_n}.txt"
                if not t2.is_file():
                    errors.append(f"missing text export for {path.name}")

    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", type=int, required=True, help="BASE number N")
    ap.add_argument("--repo-root", default=".", help="Repo root")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any check fails (default: exit 1 on fail always)",
    )
    args = ap.parse_args(argv)
    repo = Path(args.repo_root).resolve()
    errors = check_pack(repo, args.base)
    base_id = f"base-{args.base}"
    if not errors:
        print(f"OK {base_id} pack verification passed")
        return 0
    print(f"FAIL {base_id} ({len(errors)} issue(s)):", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
