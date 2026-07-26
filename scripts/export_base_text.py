#!/usr/bin/env python3
"""Export chat_request catalogs to indented text working copies (base-N diet packs).

Use this 4–10 times as you iterate:

  # From base-2-prototype JSON → base-3 text
  python3 scripts/export_base_text.py --from v2/base/base-2-prototype/min --base 3

  # Later: from edited text… (re-encode is separate)
  # From a JSON base-3 folder when you have one:
  python3 scripts/export_base_text.py --from v2/base/base-3/min --base 4

  # Dry run
  python3 scripts/export_base_text.py --from v2/base/base-2-prototype/min --base 5 --dry-run

What it does:
  - Reads chat_request*.json from --from
  - Writes v2/base/base-<N>-prototype/text/chat_request_<mode>_base-<N>.txt
  - Indented text only (not JSON)
  - Optionally rewrites _lineage.base_id / packaging fields to base-<N> (--set-base-id, default on)

What it does NOT do:
  - Diet/edit content for you
  - Hub stamp / contract hash validity
  - Custom cus_* naming (Workbench)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_mode(doc: dict, path: Path) -> str:
    mode = (doc.get("_lineage") or {}).get("mode")
    if mode:
        return str(mode)
    m = re.search(r"chat_request_(.+?)_(?:v2_min|base-[^.]+)\.json$", path.name)
    if m:
        return m.group(1)
    m = re.search(r"chat_request_(.+)\.json$", path.name)
    return m.group(1) if m else "unknown"


def emit_value(v, indent: int = 0) -> list[str]:
    sp = "  " * indent
    lines: list[str] = []
    if isinstance(v, dict):
        if not v:
            lines.append(f"{sp}{{}}")
            return lines
        for k, val in v.items():
            if isinstance(val, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.extend(emit_value(val, indent + 1))
            elif isinstance(val, str):
                if "\n" in val or len(val) > 100:
                    lines.append(f"{sp}{k}: |")
                    for line in val.splitlines() or [""]:
                        lines.append(f"{sp}  {line}")
                else:
                    lines.append(f"{sp}{k}: {val}")
            elif val is None:
                lines.append(f"{sp}{k}: null")
            elif isinstance(val, bool):
                lines.append(f"{sp}{k}: {str(val).lower()}")
            else:
                lines.append(f"{sp}{k}: {val}")
    elif isinstance(v, list):
        if not v:
            lines.append(f"{sp}[]")
            return lines
        for i, item in enumerate(v):
            if isinstance(item, dict):
                name = None
                fn = item.get("function")
                if isinstance(fn, dict):
                    name = fn.get("name")
                elif "name" in item:
                    name = item.get("name")
                label = f"- [{i}] {name}" if name else f"- [{i}]"
                lines.append(f"{sp}{label}")
                lines.extend(emit_value(item, indent + 1))
            elif isinstance(item, list):
                lines.append(f"{sp}- [{i}]")
                lines.extend(emit_value(item, indent + 1))
            else:
                lines.append(f"{sp}- {item}")
    else:
        lines.append(f"{sp}{v}")
    return lines


def apply_base_id(doc: dict, base_n: int, source_label: str) -> dict:
    """Shallow-copy and set packaging/lineage base id for the new text pack."""
    import copy

    d = copy.deepcopy(doc)
    base_id = f"base-{base_n}"
    lin = dict(d.get("_lineage") or {})
    parent = lin.get("base_id") or lin.get("parent_base_id")
    lin["base_id"] = base_id
    if parent and parent != base_id:
        lin["parent_base_id"] = parent
    lin["prototype"] = True
    lin["file_stem"] = None  # filled per mode later
    d["_lineage"] = lin

    if isinstance(d.get("_prototype"), dict):
        proto = dict(d["_prototype"])
        proto["base_id"] = base_id
        proto["packaging"] = f"base-{base_n}-prototype"
        proto["text_export_from"] = source_label
        proto["exported_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        d["_prototype"] = proto

    # contract stamp is prototype noise; leave hash values but mark builder if present
    if isinstance(d.get("contract"), dict):
        c = dict(d["contract"])
        c["prototype"] = True
        c["text_pack_base_id"] = base_id
        d["contract"] = c

    return d


def catalog_to_text(doc: dict, *, mode: str, base_n: int, source_label: str) -> str:
    base_id = f"base-{base_n}"
    lines = [
        "# chat_request catalog — indented text working copy",
        f"# file: chat_request_{mode}_{base_id}.txt",
        f"# packaging: base-{base_n}-prototype",
        f"# source: {source_label}",
        f"# base_id (lineage): {base_id}",
        "# NOT JSON. Indent = 2 spaces. Multiline: key: | then indented lines.",
        f"# Re-encode later → chat_request_{mode}_{base_id}.json for stamp/Client.",
        "# Customs (Hub): chat_request_<mode>_base-N_cus_<bucket>_<scope>-<rev>.json",
        "",
    ]

    order = [
        "_format",
        "_version",
        "_note",
        "_hash",
        "_hash_policy",
        "_lineage",
        "_prototype",
        "contract",
        "metadata",
        "messages",
        "instructions",
        "masq",
        "guidance",
        "verbs",
    ]
    keys = list(doc.keys())
    ordered = [k for k in order if k in doc] + [k for k in keys if k not in order]

    for k in ordered:
        val = doc[k]
        if isinstance(val, (dict, list)):
            lines.append(f"{k}:")
            lines.extend(emit_value(val, 1))
        elif isinstance(val, str) and ("\n" in val or len(val) > 100):
            lines.append(f"{k}: |")
            for line in val.splitlines() or [""]:
                lines.append(f"  {line}")
        elif val is None:
            lines.append(f"{k}: null")
        elif isinstance(val, bool):
            lines.append(f"{k}: {str(val).lower()}")
        else:
            lines.append(f"{k}: {val}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_pack_readme(dst: Path, base_n: int, files: list[dict], source: str) -> None:
    base_id = f"base-{base_n}"
    body = f"""# base-{base_n}-prototype

Indented **text** working copy for diet/edit iterations.

| | |
| --- | --- |
| **BASE id** | `{base_id}` |
| **Files** | `text/chat_request_<mode>_{base_id}.txt` |
| **Later JSON** | `chat_request_<mode>_{base_id}.json` |
| **Customs** | `chat_request_<mode>_{base_id}_cus_<bucket>_<scope>-<rev>.json` |
| **Source** | `{source}` |
| **Generator** | `scripts/export_base_text.py --base {base_n}` |

## Regenerate / next base

```bash
# this pack again
python3 scripts/export_base_text.py --from {source} --base {base_n}

# next iteration (example)
python3 scripts/export_base_text.py --from {source} --base {base_n + 1}
```

## Files

"""
    for f in files:
        body += f"- [`{f['file']}`]({f['file']}) — mode `{f['mode']}`\n"
    body += """
## Workflow

```text
JSON catalogs → export_base_text.py → base-N-prototype text
  → edit/diet
  → re-encode JSON (separate step)
  → stamp / Client
```
"""
    (dst / "README.md").write_text(body)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--from",
        dest="src",
        required=True,
        help="Directory of chat_request*.json (e.g. v2/base/base-2-prototype/min)",
    )
    ap.add_argument(
        "--base",
        type=int,
        required=True,
        help="BASE number N → base-N-prototype + chat_request_*_base-N.txt",
    )
    ap.add_argument(
        "--repo-root",
        default=".",
        help="Repo root (default: .)",
    )
    ap.add_argument(
        "--out",
        default=None,
        help="Output dir (default: <repo>/v2/base/base-<N>-prototype)",
    )
    ap.add_argument(
        "--set-base-id",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Rewrite _lineage.base_id (and related) to base-N inside the text (default: true)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    src = Path(args.src)
    if not src.is_absolute():
        src = (repo / src).resolve()
    if not src.is_dir():
        print(f"error: source not a directory: {src}", file=sys.stderr)
        return 2

    base_n = args.base
    if base_n < 1:
        print("error: --base must be >= 1", file=sys.stderr)
        return 2

    dst = Path(args.out) if args.out else repo / "v2" / "base" / f"base-{base_n}-prototype"
    if not dst.is_absolute():
        dst = (repo / dst).resolve()
    text_dir = dst / "text"

    paths = sorted(src.glob("chat_request*.json"))
    if not paths:
        print(f"error: no chat_request*.json under {src}", file=sys.stderr)
        return 2

    source_label = str(src.relative_to(repo)) if str(src).startswith(str(repo)) else str(src)
    written: list[dict] = []

    print(f"source:  {src}")
    print(f"out:     {dst}")
    print(f"base:    base-{base_n}")
    print(f"set-id:  {args.set_base_id}")
    print(f"files:   {len(paths)}")

    if not args.dry_run:
        text_dir.mkdir(parents=True, exist_ok=True)

    for path in paths:
        doc = json.loads(path.read_text())
        mode = find_mode(doc, path)
        if args.set_base_id:
            doc = apply_base_id(doc, base_n, source_label)
            doc["_lineage"]["mode"] = mode
            doc["_lineage"]["file_stem"] = f"chat_request_{mode}_base-{base_n}.txt"

        body = catalog_to_text(doc, mode=mode, base_n=base_n, source_label=source_label)
        out_name = f"chat_request_{mode}_base-{base_n}.txt"
        out_path = text_dir / out_name
        print(f"  {path.name} → text/{out_name} ({len(body)} chars)")
        if not args.dry_run:
            out_path.write_text(body)
        written.append(
            {
                "file": f"text/{out_name}",
                "mode": mode,
                "chars": len(body),
                "source_json": path.name,
            }
        )

    manifest = {
        "base_id": f"base-{base_n}",
        "packaging": f"base-{base_n}-prototype",
        "kind": "text_export",
        "source": source_label,
        "content_policy": "text_export; lineage base_id set to base-N"
        if args.set_base_id
        else "text_export; lineage preserved from source",
        "format": "indented_text",
        "file_pattern_text": f"chat_request_<mode>_base-{base_n}.txt",
        "file_pattern_json_later": f"chat_request_<mode>_base-{base_n}.json",
        "custom_pattern": f"chat_request_<mode>_base-{base_n}_cus_<bucket>_<scope>-<rev>.json",
        "generator": "scripts/export_base_text.py",
        "files": written,
    }

    if not args.dry_run:
        (dst / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
        write_pack_readme(dst, base_n, written, source_label)
        print(f"wrote {dst / 'README.md'}")
        print(f"wrote {dst / 'MANIFEST.json'}")
    else:
        print("(dry-run — no files written)")

    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
