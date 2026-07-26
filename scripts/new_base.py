#!/usr/bin/env python3
"""Scaffold a full base-N pack (min JSON + text + MANIFEST + Layer A schemas + README).

Reference layout: v2/base/base-4/

  python3 scripts/new_base.py --from v2/base/base-4 --base 5
  python3 scripts/new_base.py --from v2/base/base-4 --base 5 --dry-run
  python3 scripts/new_base.py --refresh-manifest --base 4

Also see docs/CREATE_BASE.md.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse text export helpers
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from export_base_text import (  # noqa: E402
    apply_base_id,
    catalog_to_text,
    find_mode,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_min_dir(src: Path) -> Path:
    """Accept pack root (…/base-4) or min dir (…/base-4/min)."""
    if (src / "min").is_dir() and list((src / "min").glob("chat_request*.json")):
        return src / "min"
    if src.is_dir() and list(src.glob("chat_request*.json")):
        return src
    raise FileNotFoundError(f"no chat_request*.json under {src} or {src / 'min'}")


def resolve_pack_root(src: Path) -> Path:
    if src.name == "min" and src.parent.name.startswith("base-"):
        return src.parent
    return src


def rewrite_doc_note(doc: dict, base_n: int) -> None:
    """Point packaging meta at docs/ (not pack-local essays)."""

    def fix_str(s: str) -> str:
        s = re.sub(r"v2/base/base-\d+/BIBLE\.md", "docs/BIBLE.md", s)
        s = re.sub(
            r"v2/base/base-\d+/BASE_1_TO_BASE_4_GUIDE\.md",
            "docs/base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md",
            s,
        )
        s = re.sub(
            r"v2/base/base-\d+/MULTI_ROUND_CLIENT\.md",
            "docs/MULTI_ROUND_CLIENT.md",
            s,
        )
        s = re.sub(
            r"v2/base/base-\d+/lessons-learned\.md",
            "docs/base-1_to_base-4/lessons-learned.md",
            s,
        )
        s = re.sub(r"v2/base/base-\d+/INSPECTOR\.md", "docs/INSPECTOR.md", s)
        s = re.sub(r"See v2/base/base-\d+/BIBLE\.md\.?", "See docs/BIBLE.md.", s)
        return s

    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        if isinstance(o, str):
            return fix_str(o)
        return o

    # mutate in place
    fixed = walk(doc)
    doc.clear()
    doc.update(fixed)



def copy_min_catalogs(
    min_src: Path,
    min_dst: Path,
    base_n: int,
    source_label: str,
    *,
    prototype: bool,
    dry_run: bool,
) -> list[dict]:
    paths = sorted(min_src.glob("chat_request*.json"))
    if not paths:
        raise FileNotFoundError(f"no catalogs in {min_src}")
    if not dry_run:
        min_dst.mkdir(parents=True, exist_ok=True)
    written: list[dict] = []
    for path in paths:
        doc = json.loads(path.read_text())
        mode = find_mode(doc, path)
        doc = apply_base_id(doc, base_n, source_label, prototype=prototype)
        lin = doc.setdefault("_lineage", {})
        lin["mode"] = mode
        lin["file_stem"] = f"chat_request_{mode}_base-{base_n}.json"
        lin["kind"] = lin.get("kind") or "base"
        rewrite_doc_note(doc, base_n)
        out_name = f"chat_request_{mode}_base-{base_n}.json"
        out_path = min_dst / out_name
        body = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        print(f"  min/{path.name} → min/{out_name} ({len(body)} bytes)")
        if not dry_run:
            out_path.write_text(body)
        written.append(
            {
                "file": f"v2/base/base-{base_n}/min/{out_name}",
                "mode": mode,
                "base_id": f"base-{base_n}",
                "prototype": bool(prototype),
                "bytes": len(body.encode("utf-8")),
            }
        )
    return written


def export_text(
    min_dir: Path,
    pack_dst: Path,
    base_n: int,
    source_label: str,
    *,
    prototype: bool,
    set_base_id: bool,
    dry_run: bool,
) -> list[dict]:
    text_dir = pack_dst / "text"
    if not dry_run:
        text_dir.mkdir(parents=True, exist_ok=True)
    written: list[dict] = []
    for path in sorted(min_dir.glob("chat_request*.json")):
        doc = json.loads(path.read_text())
        mode = find_mode(doc, path)
        if set_base_id:
            doc = apply_base_id(doc, base_n, source_label, prototype=prototype)
            doc["_lineage"]["mode"] = mode
            doc["_lineage"]["file_stem"] = f"chat_request_{mode}_base-{base_n}.txt"
        body = catalog_to_text(doc, mode=mode, base_n=base_n, source_label=source_label)
        out_name = f"chat_request_{mode}_base-{base_n}.txt"
        print(f"  text/{out_name} ({len(body)} chars)")
        if not dry_run:
            (text_dir / out_name).write_text(body)
        written.append({"file": f"text/{out_name}", "mode": mode, "chars": len(body)})
    return written


def copy_layer_a_schemas(pack_src: Path, pack_dst: Path, *, dry_run: bool) -> list[str]:
    root = resolve_pack_root(pack_src)
    copied: list[str] = []
    for name in ("response_output_schema.json", "response_output_example.json"):
        src_file = root / name
        if not src_file.is_file():
            print(f"  warn: missing {name} under {root} — skip")
            continue
        print(f"  copy {name}")
        if not dry_run:
            shutil.copy2(src_file, pack_dst / name)
        copied.append(name)
    return copied


def write_manifest(
    pack_dst: Path,
    base_n: int,
    catalogs: list[dict],
    *,
    prototype: bool,
    parent_label: str,
    dry_run: bool,
) -> dict:
    base_id = f"base-{base_n}"
    pack = f"base-{base_n}-prototype" if prototype else f"base-{base_n}"
    rel_pack = f"v2/base/{pack}"
    manifest = {
        "schema_version": 2,
        "base_id": base_id,
        "kind": "base",
        "status": "scaffold" if not prototype else "prototype_scaffold",
        "note": (
            f"{base_id} scaffolded from {parent_label}. "
            "Edit catalogs + Layer A schemas; do not invent production contract hashes. "
            "Design docs live under docs/ (see docs/BIBLE.md, docs/CREATE_BASE.md)."
        ),
        "paths": {
            "min": f"{rel_pack}/min",
            "text": f"{rel_pack}/text",
            "bible": "docs/BIBLE.md",
            "roadmap": "docs/ROADMAP.md",
            "create_base": "docs/CREATE_BASE.md",
            "response_output_schema": f"{rel_pack}/response_output_schema.json",
            "response_output_example": f"{rel_pack}/response_output_example.json",
        },
        "parent_source": parent_label,
        "updated_at": utc_now(),
        "generator": "scripts/new_base.py",
        "catalogs": catalogs,
    }
    if not dry_run:
        (pack_dst / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"wrote {pack_dst / 'MANIFEST.json'}")
    return manifest


def write_pack_docs(pack_dst: Path, base_n: int, parent_label: str, *, dry_run: bool) -> None:
    base_id = f"base-{base_n}"
    readme = f"""# {base_id}

Ship pack for chat_request catalogs. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `{base_id}` |
| **JSON** | [`min/chat_request_<mode>_{base_id}.json`](min/) |
| **Text** | [`text/chat_request_<mode>_{base_id}.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Parent scaffold** | `{parent_label}` |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) |
| **Roadmap** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **How this pack was created** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min` until you promote |

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/{base_id}/min --base {base_n} --out v2/base/{base_id} --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base {base_n}
python3 scripts/scan_catalogs.py
```

## Scaffold next BASE

```bash
python3 scripts/new_base.py --from v2/base/{base_id} --base {base_n + 1}
```
"""
    overview = f"""# {base_id} overview

Short pack changelog only. Full requirements: [docs/BIBLE.md](../../../docs/BIBLE.md).

| | |
| --- | --- |
| **BASE id** | `{base_id}` |
| **Scaffolded from** | `{parent_label}` |
| **JSON** | `min/chat_request_<mode>_{base_id}.json` |
| **Text** | `text/chat_request_<mode>_{base_id}.txt` |
| **Status** | Scaffold — edit before Client trial / stamp |

## What to change in this BASE

_Replace this section with the diet / feature theme for {base_id} (see docs/ROADMAP.md)._

## Unchanged until you edit

- 13 verbs (unless this BASE deliberately changes them)
- Required Layer A four: summary, query_decomposition, decomposition, confidence
- Envelope `_format: "zeus.chat_request.v2"`

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/{base_id}/min --base {base_n} --out v2/base/{base_id} --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base {base_n}
```
"""
    if not dry_run:
        (pack_dst / "README.md").write_text(readme)
        (pack_dst / "OVERVIEW.md").write_text(overview)
        print(f"wrote {pack_dst / 'README.md'}")
        print(f"wrote {pack_dst / 'OVERVIEW.md'}")


def refresh_manifest_only(repo: Path, base_n: int, *, prototype: bool, dry_run: bool) -> int:
    pack = f"base-{base_n}-prototype" if prototype else f"base-{base_n}"
    pack_dst = repo / "v2" / "base" / pack
    min_dir = pack_dst / "min"
    if not min_dir.is_dir():
        print(f"error: missing {min_dir}", file=sys.stderr)
        return 2
    catalogs = []
    for path in sorted(min_dir.glob("chat_request*.json")):
        doc = json.loads(path.read_text())
        mode = find_mode(doc, path)
        catalogs.append(
            {
                "file": f"v2/base/{pack}/min/{path.name}",
                "mode": mode,
                "base_id": f"base-{base_n}",
                "prototype": prototype,
                "bytes": path.stat().st_size,
            }
        )
    write_manifest(
        pack_dst,
        base_n,
        catalogs,
        prototype=prototype,
        parent_label=f"(refresh) v2/base/{pack}",
        dry_run=dry_run,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="src", default=None, help="Parent pack or min dir (e.g. v2/base/base-4)")
    ap.add_argument("--base", type=int, required=True, help="New BASE number N")
    ap.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    ap.add_argument("--out", default=None, help="Output pack dir (default: v2/base/base-N)")
    ap.add_argument("--prototype-pack", action="store_true", help="Name pack base-N-prototype")
    ap.add_argument("--force", action="store_true", help="Allow non-empty destination")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--refresh-manifest",
        action="store_true",
        help="Only rebuild MANIFEST.json for existing base-N min/",
    )
    ap.add_argument(
        "--no-copy-json",
        action="store_true",
        help="Do not copy min JSON (text+manifest only; rare)",
    )
    args = ap.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    base_n = args.base
    if base_n < 1:
        print("error: --base must be >= 1", file=sys.stderr)
        return 2

    if args.refresh_manifest:
        return refresh_manifest_only(repo, base_n, prototype=args.prototype_pack, dry_run=args.dry_run)

    if not args.src:
        print("error: --from is required unless --refresh-manifest", file=sys.stderr)
        return 2

    src = Path(args.src)
    if not src.is_absolute():
        src = (repo / src).resolve()
    try:
        min_src = resolve_min_dir(src)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    pack_src = resolve_pack_root(src if src.name != "min" else src)

    pack_name = f"base-{base_n}-prototype" if args.prototype_pack else f"base-{base_n}"
    pack_dst = Path(args.out) if args.out else repo / "v2" / "base" / pack_name
    if not pack_dst.is_absolute():
        pack_dst = (repo / pack_dst).resolve()

    if pack_dst.exists() and any(pack_dst.iterdir()) and not args.force and not args.dry_run:
        print(f"error: destination not empty: {pack_dst} (use --force)", file=sys.stderr)
        return 2

    source_label = str(min_src.relative_to(repo)) if str(min_src).startswith(str(repo)) else str(min_src)
    parent_label = str(pack_src.relative_to(repo)) if str(pack_src).startswith(str(repo)) else str(pack_src)

    print(f"parent:  {pack_src}")
    print(f"min src: {min_src}")
    print(f"out:     {pack_dst}")
    print(f"base:    base-{base_n}")

    if not args.dry_run:
        pack_dst.mkdir(parents=True, exist_ok=True)

    catalogs: list[dict] = []
    if not args.no_copy_json:
        catalogs = copy_min_catalogs(
            min_src,
            pack_dst / "min",
            base_n,
            source_label,
            prototype=args.prototype_pack,
            dry_run=args.dry_run,
        )
    else:
        # text-only from existing min
        if (pack_dst / "min").is_dir():
            for path in sorted((pack_dst / "min").glob("chat_request*.json")):
                doc = json.loads(path.read_text())
                catalogs.append(
                    {
                        "file": f"v2/base/{pack_name}/min/{path.name}",
                        "mode": find_mode(doc, path),
                        "base_id": f"base-{base_n}",
                        "prototype": args.prototype_pack,
                        "bytes": path.stat().st_size,
                    }
                )

    min_for_text = pack_dst / "min" if not args.dry_run and (pack_dst / "min").is_dir() else min_src
    if args.dry_run:
        min_for_text = min_src

    copy_layer_a_schemas(pack_src if pack_src.is_dir() else pack_src.parent, pack_dst, dry_run=args.dry_run)

    export_text(
        min_for_text if not args.no_copy_json and not args.dry_run else min_src,
        pack_dst,
        base_n,
        source_label,
        prototype=args.prototype_pack,
        set_base_id=True,
        dry_run=args.dry_run,
    )

    # Rebuild catalog byte sizes from written min if present
    if not args.dry_run and (pack_dst / "min").is_dir():
        catalogs = []
        for path in sorted((pack_dst / "min").glob("chat_request*.json")):
            doc = json.loads(path.read_text())
            catalogs.append(
                {
                    "file": f"v2/base/{pack_name}/min/{path.name}",
                    "mode": find_mode(doc, path),
                    "base_id": f"base-{base_n}",
                    "prototype": args.prototype_pack,
                    "bytes": path.stat().st_size,
                }
            )

    write_manifest(
        pack_dst,
        base_n,
        catalogs,
        prototype=args.prototype_pack,
        parent_label=parent_label,
        dry_run=args.dry_run,
    )
    write_pack_docs(pack_dst, base_n, parent_label, dry_run=args.dry_run)

    if args.dry_run:
        print("(dry-run — no files written)")
    print("ok — next:")
    print("  1. DIET catalogs / Layer A schema under", pack_dst)
    print("     (scaffold copies parent wire — not ship-ready)")
    print("  2. re-export text + refresh MANIFEST + scan_catalogs")
    print("  3. python3 scripts/verify_base_pack.py --base", base_n, "  # must OK before PR")
    print("  4. fill docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md")
    print("     (template: docs/migration/RELEASE_CHECKLIST_TEMPLATE.md — phases A–G)")
    print("  5. see docs/CREATE_BASE.md + docs/BASE_AGENT_PLAYBOOK.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
