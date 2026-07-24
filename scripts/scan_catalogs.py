#!/usr/bin/env python3
"""Scan v2/**/chat_request*.json → catalog-index.json for the inspector dropdown.

The Hub-style map (index.html) loads this file so every catalog under v2/
appears in the mode dropdown, not only the latest v2/min alias in manifest.json.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
OUT = ROOT / "catalog-index.json"

# chat_request_auto_v2_min.json → auto
# chat_request_auto.json → auto
_MODE_RE = re.compile(r"^chat_request_(.+?)(?:_v\d+(?:_min)?)?\.json$", re.I)


def mode_from_name(name: str) -> str:
    m = _MODE_RE.match(name)
    return m.group(1) if m else Path(name).stem


def folder_label(rel: Path) -> str:
    """Short path for the dropdown (drop leading v2/)."""
    parts = rel.parts
    if parts and parts[0] == "v2":
        parts = parts[1:]
    return "/".join(parts) if parts else "."


def sort_key(entry: dict) -> tuple:
    """Prefer latest alias v2/min first, then BASE pins, then mode name."""
    folder = entry.get("folder") or ""
    mode = entry.get("mode") or ""
    if folder == "v2/min":
        group = 0
    elif "/base/" in folder:
        group = 1
    else:
        group = 2
    return (group, folder, mode)


def main() -> None:
    if not V2.is_dir():
        raise SystemExit(f"missing {V2}")

    catalogs: list[dict] = []
    for p in sorted(V2.rglob("chat_request*.json")):
        if not p.is_file():
            continue
        raw = p.read_bytes()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"skip {p}: {e}")
            continue
        rel = p.relative_to(ROOT).as_posix()
        lin = data.get("_lineage") if isinstance(data.get("_lineage"), dict) else {}
        mode = lin.get("mode") or mode_from_name(p.name)
        catalogs.append(
            {
                "file": rel,
                "mode": mode,
                "folder": str(p.parent.relative_to(ROOT)).replace("\\", "/"),
                "folder_label": folder_label(p.parent.relative_to(ROOT)),
                "base_id": lin.get("base_id"),
                "custom_id": lin.get("custom_id"),
                "profile": lin.get("profile") or data.get("_format"),
                "format": data.get("_format"),
                "version": data.get("_version"),
                "verb_count": len(data.get("verbs") or []),
                "contract": data.get("contract") or {},
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        )

    catalogs.sort(key=sort_key)
    payload = {
        "schema_version": 1,
        "description": "Auto-scanned chat_request*.json under v2/ for the inspector UI",
        "scan_glob": "v2/**/chat_request*.json",
        "count": len(catalogs),
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "catalogs": catalogs,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUT} ({len(catalogs)} catalogs)")


if __name__ == "__main__":
    main()
