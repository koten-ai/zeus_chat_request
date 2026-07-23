#!/usr/bin/env python3
"""Rebuild root manifest.json from v2/min + CURRENT.json base_id if present."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MIN = ROOT / "v2" / "min"

def main() -> None:
    files = sorted(MIN.glob("chat_request_*_v2_min.json"))
    entries = []
    base_id = "base-1"
    cur = ROOT / "CURRENT.json"
    if cur.is_file():
        try:
            base_id = json.loads(cur.read_text()).get("base_id") or base_id
        except Exception:
            pass
    for p in files:
        data = json.loads(p.read_text())
        mode = p.name.replace("chat_request_", "").replace("_v2_min.json", "")
        raw = p.read_bytes()
        lin = data.get("_lineage") or {}
        entries.append({
            "file": str(p.relative_to(ROOT)).replace("\\", "/"),
            "mode": mode,
            "base_id": lin.get("base_id") or base_id,
            "custom_id": lin.get("custom_id"),
            "format": data.get("_format"),
            "version": data.get("_version"),
            "verb_count": len(data.get("verbs") or []),
            "contract": data.get("contract") or {},
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    manifest = {
        "schema_version": 2,
        "repo": "koten-ai/zeus_chat_request",
        "current_base_id": base_id,
        "profile": "v2_min",
        "description": "Zeus V2 chat_request catalogs — BASE sequence + latest min alias",
        "paths": {
            "latest_min": "v2/min",
            "current_base_min": f"v2/base/{base_id}/min",
        },
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "usage": {
            "stamp": "Always verify/stamp with your Zeus instance before production",
            "client_sync": "Prefer pin base_id; pull v2/base/<base_id>/min or v2/min",
            "compat": "See COMPAT.md",
        },
        "catalogs": entries,
    }
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {out} (current_base_id={base_id}, {len(entries)} catalogs)")

if __name__ == "__main__":
    main()
