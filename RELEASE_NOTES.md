# Release notes — zeus_chat_request

Published **Zeus V2 min chat_request** catalogs for Zeus Client, Developer Helper MCP, demos, and coding agents.

| | |
| --- | --- |
| **Repo** | https://github.com/koten-ai/zeus_chat_request |
| **Profile** | `v2_min` |
| **Format** | `zeus.chat_request.v2` |
| **Index** | [`manifest.json`](manifest.json) |

---

## 0.1.0 — Initial public distribution

**Date:** 2026-07-16  
**Git:** `e342ebc` (`main`)

### Highlights

- First release of **integrator-facing** V2 **min** mode catalogs (no Zeus monorepo required).
- Sourced from Zeus engine generation path: `ai/V2/variants/min/` (`ai-snapshot --min`).
- Machine-readable **`manifest.json`** (mode, path, sha256, verb_count, template contract metadata).
- Scripts to refresh from a local Zeus checkout.

### Catalogs included (10 modes)

| Mode | File |
| --- | --- |
| analytics | `v2/min/chat_request_analytics_v2_min.json` |
| auto | `v2/min/chat_request_auto_v2_min.json` |
| code | `v2/min/chat_request_code_v2_min.json` |
| custom | `v2/min/chat_request_custom_v2_min.json` |
| fraud | `v2/min/chat_request_fraud_v2_min.json` |
| open | `v2/min/chat_request_open_v2_min.json` |
| private | `v2/min/chat_request_private_v2_min.json` |
| regulated | `v2/min/chat_request_regulated_v2_min.json` |
| research | `v2/min/chat_request_research_v2_min.json` |
| tenant | `v2/min/chat_request_tenant_v2_min.json` |

Typical payload size: ~13–15 KB per mode (min profile). Verb surface: **13** verbs per catalog in this snapshot set.

### Repo layout

```text
zeus_chat_request/
├── README.md
├── RELEASE_NOTES.md
├── manifest.json
├── scripts/
│   ├── sync-from-zeus.sh      # copy from Zeus/ai/V2/variants/min
│   └── refresh_manifest.py    # rebuild manifest.json
└── v2/min/
    └── chat_request_*_v2_min.json
```

### Intended consumers

| Consumer | How to use |
| --- | --- |
| **Zeus Client** (`kotenai-zeus-client`) | Demo/offline templates; production still **stamp + `sync_chat_requests`** |
| **Developer Helper MCP** | `list_catalog_modes` / `fetch_chat_request` ([zeus_dev_helper_mcp](https://github.com/koten-ai/zeus_dev_helper_mcp)) |
| **koten_docs** | Contracts / using-zeus-client point here as distribution home |
| **Coding agents** | Clone or fetch by mode; never invent `contract_hash` |

### Critical rules (unchanged for all releases)

1. **Templates ≠ production stamps.** Files may contain generation-time `contract` metadata; **your** Zeus Hub verify/stamp is authoritative.
2. Prefer live **`sync_chat_requests`** after ops stamps a scope.
3. Do **not** hand-edit hashes to clear drift (409) — resync and re-pin.
4. Engine full (non-min) snapshots remain under Zeus `ai/V2/chat_request_*_v2.json` for Hub A/B; integrators should start with **min**.

### Related tracking

| Item | Link |
| --- | --- |
| Docs story | [KD-8](https://kotenai.atlassian.net/browse/KD-8) |
| Helper catalog tools | [ZDH-14](https://kotenai.atlassian.net/browse/ZDH-14) |
| Platform docs | [docs.koten.ai](https://docs.koten.ai/) · [contracts](https://docs.koten.ai/zeus-client/contracts-and-catalog) |
| Generator | [koten-ai/Zeus](https://github.com/koten-ai/Zeus) `go run . ai-snapshot --mode=all --api-version=v2 --min` |

### Upgrade / refresh procedure

```bash
# 1. In Zeus engine repo — regenerate min catalogs
go run . ai-snapshot --mode=all --api-version=v2 --min

# 2. Publish into this repo
./scripts/sync-from-zeus.sh /path/to/Zeus
python3 scripts/refresh_manifest.py

# 3. Commit + tag
git add v2/min manifest.json
git commit -m "chore: refresh v2_min catalogs from Zeus"
git tag -a v0.1.1 -m "v0.1.1 catalog refresh"
git push origin main --tags
```

### Breaking changes

None (initial release).

### Known limitations

- No full (non-min) profile published yet — min only.
- No use-case-specific catalogs (e.g. travel_booking) in this tree yet.
- Private GitHub clones may require `GITHUB_TOKEN` or a local `ZEUS_CHAT_REQUEST_DIR` for Helper MCP.

---

## Unreleased

- Optional: full V2 profile mirror  
- Optional: use-case / vertical catalogs  
- Optional: signed release artifacts / CI sync from Zeus  
