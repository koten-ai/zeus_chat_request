#!/usr/bin/env python3
"""Assemble CORE + mode overlay into chat_request system prompts (base-5.1).

Usage:
  python3 scripts/assemble_mode_prompts.py --base 5.1
  python3 scripts/assemble_mode_prompts.py --base 5.1 --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODES = [
    "analytics",
    "auto",
    "code",
    "custom",
    "fraud",
    "open",
    "private",
    "regulated",
    "research",
    "tenant",
]


def assemble(core: str, overlay: str, mode: str) -> str:
    body = core.replace("{{mode}}", mode).rstrip() + "\n\n" + overlay.strip() + "\n"
    return body


def fix_analytics_job_blurbs(doc: dict, mode: str) -> int:
    """Replace leftover '[exp] analytics job' style blurbs with mode name."""
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "description" and isinstance(v, str) and "analytics job" in v:
                    o[k] = v.replace("analytics job", f"{mode} job")
                    n += 1
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--base",
        default="5.1",
        help="Pack id without base- prefix (e.g. 5.1). Writes into v2/base/base-<id>/ only.",
    )
    ap.add_argument("--repo-root", default=".")
    ap.add_argument(
        "--overlays",
        default="work/mode_overlays",
        help="Directory with CORE.md and <mode>.md",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.repo_root).resolve()
    bare = str(args.base).removeprefix("base-")
    base_id = f"base-{bare}"
    ov_dir = root / args.overlays
    core_path = ov_dir / "CORE.md"
    if not core_path.is_file():
        print(f"error: missing {core_path}", file=sys.stderr)
        return 1
    core = core_path.read_text()

    pack_min = root / "v2" / "base" / base_id / "min"
    if not pack_min.is_dir():
        print(f"error: missing {pack_min}", file=sys.stderr)
        return 1

    for mode in MODES:
        ov_path = ov_dir / f"{mode}.md"
        if not ov_path.is_file():
            print(f"error: missing overlay {ov_path}", file=sys.stderr)
            return 1
        content = assemble(core, ov_path.read_text(), mode)
        path = pack_min / f"chat_request_{mode}_base-{bare}.json"
        if not path.is_file():
            print(f"error: missing pack {path}", file=sys.stderr)
            return 1
        doc = json.loads(path.read_text())
        msgs = doc.get("messages")
        if not isinstance(msgs, list) or not msgs:
            print(f"error: {path.name}: no messages[]", file=sys.stderr)
            return 1
        if not isinstance(msgs[0], dict) or msgs[0].get("role") != "system":
            print(f"error: {path.name}: messages[0] is not system", file=sys.stderr)
            return 1
        old_len = len(str(msgs[0].get("content", "")))
        msgs[0]["content"] = content
        fixed = fix_analytics_job_blurbs(doc, mode)
        meta = doc.get("_base_meta")
        if isinstance(meta, dict):
            meta.pop("content_train", None)
            meta["mode_overlay"] = True
            meta["base_id"] = base_id
        lin = doc.get("_lineage") or {}
        lin["base_id"] = base_id
        lin["file_stem"] = path.name
        doc["_lineage"] = lin
        print(
            f"{mode:12} system {old_len} → {len(content)} chars"
            + (f" (fixed {fixed} analytics-job blurb(s))" if fixed else "")
        )
        if not args.dry_run:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    if args.dry_run:
        print("dry-run — no files written")
    else:
        print(f"ok — wrote system prompts under {pack_min.relative_to(root)}")
        print("note: pack folder is the snapshot SoT — never set content_train only on parent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
