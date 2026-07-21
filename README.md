# zeus_chat_request

**Published Zeus V2 chat_request catalogs** for:

- [Zeus Client](https://github.com/koten-ai/zeus_client_python) (`kotenai-zeus-client`)
- Developer Helper MCP ([ZDH](https://kotenai.atlassian.net/jira/software/projects/ZDH/boards/45))
- Demos and coding agents

These are the **min** profile snapshots (`*_v2_min.json`) — currently the best default for integrators (smaller wire payload, full verb surface).

| | |
| --- | --- |
| **Profile** | `v2_min` |
| **Format** | `zeus.chat_request.v2` |
| **Layout** | [`v2/min/`](v2/min/) |
| **Index** | [`manifest.json`](manifest.json) |

## Catalog structure map (Hub-style)

**[index.html](index.html)** — visual AI Catalog layout for published `v2/min` files:

- **Don’t edit (Rules)** vs **Editable (guidance)** vs **On the wire**
- What min is **missing** vs full engine profile
- Evidence-loop terminate contract checklist
- **JSON only** view + org plan

```bash
python3 -m http.server 8766 --bind 127.0.0.1
# open http://127.0.0.1:8766/index.html
```

## Learn the format

**[CHAT_REQUEST.md](CHAT_REQUEST.md)** — what a `chat_request*.json` is for, section-by-section, what a **contract** is, what you can change (Client vs Hub Workbench), and why these files are **baselines** you refine for your dataset.

## Why this repo exists

Historically catalogs lived only inside the Zeus engine tree (`Zeus/ai/V2/…`). Clients and helpers should **not** need a full Zeus source checkout to obtain mode templates.

| Role | Location |
| --- | --- |
| **Generator / engine embed** | [koten-ai/Zeus](https://github.com/koten-ai/Zeus) `ai/V2/` (prompts + `ai-snapshot`) |
| **Distribution (this repo)** | `v2/min/*.json` for Client / MCP / docs |
| **Live / production** | **Stamp on your Zeus** (Hub verify/stamp) then sync to the client |

## Catalogs (modes)

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

Machine index: `manifest.json` (`mode`, `sha256`, `verb_count`, embedded `contract` metadata from generation).

## Critical rules

1. **Do not invent production `contract_hash` values.** Templates here may include a generation-time hash; **your** Zeus stamp is authoritative after verify/stamp.
2. Prefer **`sync_chat_requests`** from a live Zeus after ops stamps for that scope.
3. Use this repo for **bootstrapping demos**, offline scaffolds, Dev Helper MCP `fetch_chat_request` fallbacks, and docs examples.
4. Full (non-min) engine snapshots still regenerate inside Zeus (`ai/V2/chat_request_*_v2.json`) for Hub A/B; integrators should start with **min**.

## Use with Zeus Client (Python)

```bash
git clone https://github.com/koten-ai/zeus_chat_request.git
export ZEUS_CLIENT_CONFIG_DIR=~/.config/zeus_client
mkdir -p "$ZEUS_CLIENT_CONFIG_DIR/chat_requests"
# After stamping on your Zeus (recommended), place stamped files under
# chat_requests/{bucket}__{scope}/ — or copy a template mode for local demos:
cp zeus_chat_request/v2/min/chat_request_analytics_v2_min.json \
  "$ZEUS_CLIENT_CONFIG_DIR/chat_requests/analytics.json"
```

Better production path:

```python
from zeus_client import ZeusClient, load_config, sync_chat_requests

async with ZeusClient():
    cfg = await load_config()
    await sync_chat_requests(cfg)  # pulls stamped catalogs from live Zeus
```

**Published docs:** [docs.koten.ai](https://docs.koten.ai/) · [Using Zeus Client](https://docs.koten.ai/zeus-client/using-zeus-client) · [Contracts & catalog](https://docs.koten.ai/zeus-client/contracts-and-catalog)

## Use with Developer Helper MCP

Helper tools should:

1. Prefer **live** Zeus: bootstrap + stamped catalog endpoints.
2. Fall back to **this repo** for mode templates / offline scaffold (`fetch_chat_request` / `use_sample`).
3. Read `manifest.json` for mode list + file paths.
4. Never tell the coding agent to hand-edit hashes.

See [docs.koten.ai](https://docs.koten.ai/) · [Dev Helper MCP](https://docs.koten.ai/zeus-client/dev-helper-mcp) · machine index in source repo `agent-index.yaml`.

## Refresh from a Zeus checkout

```bash
# In Zeus engine:
go run . ai-snapshot --mode=all --api-version=v2 --min

# Publish into this repo:
./scripts/sync-from-zeus.sh /path/to/Zeus
python3 scripts/refresh_manifest.py
git add v2/min manifest.json && git commit -m "chore: refresh v2_min catalogs from Zeus"
```

## Related repos

| Repo | Role |
| --- | --- |
| [Zeus](https://github.com/koten-ai/Zeus) | Engine; generates catalogs |
| [zeus_client_python](https://github.com/koten-ai/zeus_client_python) | Client library |
| [**docs.koten.ai**](https://docs.koten.ai/) | **Published platform docs** (GitBook; source: [koten_docs](https://github.com/koten-ai/koten_docs)) |
| ZDH board | Developer Helper MCP |

## License

Same product family as Zeus / Koten unless otherwise noted.

## Release notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for version history and refresh procedure.
