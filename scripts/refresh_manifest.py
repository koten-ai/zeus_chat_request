#!/usr/bin/env python3
"""Rebuild manifest.json from v2/min/*.json"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN = ROOT / "v2" / "min"

def main() -> None:
    files = sorted(MIN.glob("chat_request_*_v2_min.json"))
    entries = []
    for p in files:
        data = json.loads(p.read_text())
        mode = p.name.replace("chat_request_", "").replace("_v2_min.json", "")
        raw = p.read_bytes()
        entries.append({
            "file": str(p.relative_to(ROOT)).replace("\\", "/"),
            "mode": mode,
            "format": data.get("_format"),
            "version": data.get("_version"),
            "verb_count": len(data.get("verbs") or []),
            "contract": data.get("contract") or {},
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    manifest = {
        "schema_version": 1,
        "repo": "koten-ai/zeus_chat_request",
        "profile": "v2_min",
        "description": "Minified Zeus V2 chat_request catalogs for clients, demos, and Dev Helper MCP",
        "source_engine": {
            "generated_from": "koten-ai/Zeus",
            "path_in_engine": "ai/V2/variants/min/",
            "regenerate": "go run . ai-snapshot --mode=all --api-version=v2 --min",
        },
        "usage": {
            "stamp": "Always verify/stamp with your Zeus instance before production; do not invent contract hashes",
            "client_sync": "Copy or sync into ZEUS_CLIENT_CONFIG_DIR/chat_requests/ after stamp, or use sync_chat_requests from live Zeus",
        },
        "catalogs": entries,
    }
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {out} ({len(entries)} catalogs)")

if __name__ == "__main__":
    main()
