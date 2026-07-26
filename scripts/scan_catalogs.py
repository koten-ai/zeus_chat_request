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

# Filename → mode when _lineage.mode is absent:
#   chat_request_auto_v2_min.json              → auto
#   chat_request_analytics_base-4.json         → analytics
#   chat_request_analytics_base-2-prototype.json → analytics
#   chat_request_analytics_base-4_cus_travel-sample_default-1.json → analytics
# Prefer data["_lineage"]["mode"] when present (see main()).


def mode_from_name(name: str) -> str:
    stem = Path(name).stem
    if not stem.startswith("chat_request_"):
        return stem
    rest = stem[len("chat_request_") :]
    # strip custom + base suffixes first (…_base-4_cus_bucket_scope-1)
    rest = re.sub(r"_cus_.*$", "", rest, flags=re.I)
    rest = re.sub(r"_base-[\d.]+(?:-prototype)?$", "", rest, flags=re.I)
    rest = re.sub(r"_v\d+(?:_min)?$", "", rest, flags=re.I)
    return rest or stem


def folder_label(rel: Path) -> str:
    """Short path for the dropdown (drop leading v2/)."""
    parts = rel.parts
    if parts and parts[0] == "v2":
        parts = parts[1:]
    return "/".join(parts) if parts else "."


def sort_key(entry: dict) -> tuple:
    """Newest / highest BASE first (base-4 → base-1 → v2/min pin), then mode.

    Inspector dropdown + Matrix both rely on this order.
    """
    folder = (entry.get("folder") or "").replace("\\", "/")
    mode = entry.get("mode") or ""
    base_id = str(entry.get("base_id") or "")
    hay = f"{base_id} {folder}"
    m = re.search(r"base-(\d+(?:\.\d+)*)", hay, flags=re.I)
    if m:
        parts = [int(x) for x in m.group(1).split(".")]
        # pad for sort: (major, minor, patch…)
        while len(parts) < 3:
            parts.append(0)
        n_key = tuple(-p for p in parts)
    else:
        n_key = (0, 0, 0)
    proto = 1 if re.search(r"prototype", hay, flags=re.I) else 0
    # Production pin last within the same generation
    is_v2_min = 1 if folder == "v2/min" else 0
    # Higher base first: negate parts. Formal pack before prototype.
    return (*n_key, proto, is_v2_min, folder, mode)


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
                "prototype": bool(lin.get("prototype")),
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
