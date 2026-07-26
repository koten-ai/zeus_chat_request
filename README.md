# zeus_chat_request

**Published Zeus V2 chat_request catalogs** for clients, demos, and integrators.

## Helios (insights wishlist)

Helios Motions read terminating-turn facets from Analytics. Fields we want catalogs + Zeus to emit (geo_norm, price_norm, outcome quality, …) live in:

**→ [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)**  
Branch: `helios-beta` until merged. Not a committed schema change — design input for guidance / BASE bumps.

## Current pin

| Field | Value |
| --- | --- |
| **BASE** | `base-1` (see `CURRENT.json`) |
| **Profile** | `v2_min` |
| **Paths** | `v2/base/base-1/min/` (immutable) · `v2/min/` (latest alias) |

Each catalog JSON includes `_lineage.base_id`. Customs (Workbench) will set `custom_id` + parent BASE (ZE-223).

See **COMPAT.md** for Zeus version ↔ BASE ranges. Process: CR-1 / ZE-222.

### Diet pack — **base-4** (single Terminate table)

| Field | Value |
| --- | --- |
| **BASE id** | `base-4` |
| **Tree** | [`v2/base/base-4-prototype/`](v2/base/base-4-prototype/) |
| **JSON** | `min/chat_request_<mode>_base-4.json` |
| **Text** | `text/chat_request_<mode>_base-4.txt` |
| **Change** | One `## Terminate (Layer A)` table + example (removed duplicate Evidence-loop + Layer A essays) |
| **Bible** | [`BIBLE.md`](v2/base/base-4-prototype/BIBLE.md) — full step-by-step requirements |
| **base-1 → base-4** | [`BASE_1_TO_BASE_4_GUIDE.md`](v2/base/base-4-prototype/BASE_1_TO_BASE_4_GUIDE.md) |
| **Docs** | [`PROTOTYPE.md`](v2/base/base-4-prototype/PROTOTYPE.md) |

```bash
python3 scripts/export_base_text.py --from v2/base/base-4-prototype/min --base 4
```

### Text working copy — **base-3** (diet / edit)

| Field | Value |
| --- | --- |
| **BASE id** | `base-3` |
| **Tree** | [`v2/base/base-3-prototype/`](v2/base/base-3-prototype/) |
| **Files** | `text/chat_request_<mode>_base-3.txt` |
| **Inside** | `_lineage.base_id: base-3` (parent: base-2-prototype) |
| **Format** | Indented **text only** (not JSON) |
| **Use** | Human/LLM rework (“go on a diet”); re-encode → `chat_request_<mode>_base-3.json` before stamp |
| **Generator** | [`scripts/export_base_text.py`](scripts/export_base_text.py) |

```bash
# (re)build base-3 text pack from base-2-prototype JSON
python3 scripts/export_base_text.py --from v2/base/base-2-prototype/min --base 3

# later iterations
python3 scripts/export_base_text.py --from v2/base/base-2-prototype/min --base 4
```

### Prototype BASE (not production)

| Field | Value |
| --- | --- |
| **BASE** | `base-2-prototype` (fork of base-1) |
| **Path** | [`v2/base/base-2-prototype/min/`](v2/base/base-2-prototype/min/) · files `chat_request_<mode>_base-2-prototype.json` (not `*_v2_min.json`) |
| **Docs** | [`PROTOTYPE.md`](v2/base/base-2-prototype/PROTOTYPE.md) · Layer A terminate samples in [`samples/`](samples/) |
| **Status** | Feedback for **zeus_client** — may break engines expecting base-1-only `return` schema |
| **Pin** | Does **not** replace `CURRENT.json` / `v2/min` (still base-1) |

Layer A adds recommended: `policy_action`, `subject_confidence`, `jail_break_attempt` (0.0–1.0), `wish_i_knew`, `business_rules_triggers[]`. Layer B Detective envelope remains server-built.

---


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

### Docker Compose (port 3333)

```bash
docker compose up
# open http://localhost:3333/   (or /index.html)
```

On start, `scripts/scan_catalogs.py` rebuilds **`catalog-index.json`** from every
`v2/**/chat_request*.json` so the mode dropdown lists **all** folders (e.g. `min`
and `base/base-1/min`), not only the latest alias. Then a static server serves the
repo root on port **3333**.

Without Docker:

```bash
python3 scripts/scan_catalogs.py
python3 -m http.server 3333 --bind 127.0.0.1
```

### Inspector views (`index.html`)

| View | Purpose |
| --- | --- |
| **Structure** | Anatomy, stamp health, assembly storyboard, prompt outline, tiles / full JSON, wire vs inject, output scheme |
| **Size map** | One treemap: Full catalog vs Wire payload · Zeus API base % |
| **Diff** | Compare two catalogs (mode/BASE dropdowns, paste, or upload) · section + prompt line diff · API impact notes |
| **Matrix** | Fingerprint table across all scanned files (hash, prompt σ, terminate, sizes) |
| **Export brief** | Download a Markdown integrator brief for the selected catalog |

Deep links (examples):

```text
#view=diff&a=v2/min/chat_request_auto_v2_min.json&b=v2/min/chat_request_analytics_v2_min.json
#view=matrix
#view=size&sizeMode=wire&file=v2/min/chat_request_auto_v2_min.json
```

## Learn the format

| Doc | Contents |
| --- | --- |
| **[PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md)** | Assembled prompt: **Zeus rules → Client inject → user → terminate**; token budget (avoid 10KB→60KB stuffing) |
| **[simple_layout.txt](simple_layout.txt)** | Working field map: Contract vs Client, business rules/triggers, admin-only output |
| **[base_layout.txt](base_layout.txt)** | Short bridge + original sketch right/wrong |
| **[CHAT_REQUEST.md](CHAT_REQUEST.md)** | What a catalog is, stamp/contract, Client vs Hub, anatomy of V2 JSON |
| **[HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)** | Analytics emit wishlist (cost-aware; not all fields belong in every prompt) |

### Assembled prompt (one line)

```text
ZEUS RULES (catalog/contract) → ZEUS_CLIENT inject (brand, rules[], brief/schema, round)
  → USER message → LLM ↔ tools → terminate (user | admin | client triggers)
```

**Size:** prefer **min** catalogs (~13–17KB). Keep Client `business_injection.rules[]` short and indexed; do not paste policy novels into Base or inject until the wire prompt balloons toward tens of KB of rules alone.

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

## File naming

| Kind | Pattern | Example |
| --- | --- | --- |
| **BASE (start here)** | `chat_request_<mode>_base-<N>.json` | `chat_request_analytics_base-2.json` |
| **base-2-prototype (this repo)** | `chat_request_<mode>_base-2-prototype.json` | `chat_request_analytics_base-2-prototype.json` |
| **Custom (Hub → Workbench → Prompt Helper)** | `chat_request_<mode>_base-<N>_cus_<bucket>_<scope>-<rev>.json` | `chat_request_analytics_base-2_cus_travel-sample_default-1.json` |
| **Custom next save** | bump `<rev>` | `…_default-2.json` |
| **Legacy base-1 pin** | `chat_request_<mode>_v2_min.json` | under `v2/min/` and `v2/base/base-1/min/` |

```text
chat_request_analytics_base-2.json
  → Workbench save
chat_request_analytics_base-2_cus_travel-sample_default-1.json
  → change & save
chat_request_analytics_base-2_cus_travel-sample_default-2.json
```

- Normalize scope: `_default` → `default` in filenames (no `/`).
- `_format: "zeus.chat_request.v2"` is the **JSON envelope** id, not the file stem.
- Customs are produced on Hub, not required in this repo’s BASE tree.
- Full naming + lineage: [v2/base/base-2-prototype/PROTOTYPE.md](v2/base/base-2-prototype/PROTOTYPE.md#file-naming-base-vs-workbench-customs)


## Critical rules

1. **Do not invent production `contract_hash` values.** Templates here may include a generation-time hash; **your** Zeus stamp is authoritative after verify/stamp.
2. Prefer **`sync_chat_requests`** from a live Zeus after ops stamps for that scope.
3. Use this repo for **bootstrapping demos**, offline scaffolds, Dev Helper MCP `fetch_chat_request` fallbacks, and docs examples.
4. Full (non-min) engine snapshots still regenerate inside Zeus (`ai/V2/chat_request_*_v2.json`) for Hub A/B; integrators should start with **min**.
5. **Do not over-stuff prompts.** Catalog min is intentionally small; Client injects (brief, schema, business rules) must stay bounded or assembled size jumps from ~10KB toward 60KB+. Prefer short indexed rules + terminate triggers over long free-form policy.

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
