# zeus_chat_request

**Published Zeus V2 chat_request catalogs** for Zeus Client, Developer Helper MCP, demos, and coding agents.

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · candidate pack **base-5** · **[COMPAT.md](COMPAT.md)** = Zeus × BASE × zeus_client matrix

![Assembled prompt flow](images/assembled_prompt.svg)

*One model round: **PROMPT** = rules **+** client inject **+** messages (one request) → LLM ↔ Zeus → **OUTPUT** = Layer A terminate (G1/G2/G3). See [docs/PROMPT_ASSEMBLY.md](docs/PROMPT_ASSEMBLY.md).*

---

## Documentation

| Doc | Topic |
| --- | --- |
| **[AGENTS.md](AGENTS.md)** | **AI entry** — hard rules + BASE comply/upgrade |
| [docs/BASE_AGENT_PLAYBOOK.md](docs/BASE_AGENT_PLAYBOOK.md) | Comply with base-X · upgrade X→Y |
| [docs/migration/](docs/migration/) | Hop archives (`base-X_to_base-Y`) |
| **[docs/README.md](docs/README.md)** | **Doc hub** — layout rules + full index |
| [COMPAT.md](COMPAT.md) | **Zeus × chat_request BASE × zeus_client** versions |
| [docs/BIBLE.md](docs/BIBLE.md) | Requirements + ownership (set/unset/change) |
| [docs/ROADMAP.md](docs/ROADMAP.md) | base-5+ plan |
| [docs/CREATE_BASE.md](docs/CREATE_BASE.md) | Scaffold a new `base-N` pack |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | Releases + breaking changes |

---

## Current pin

| Field | Value |
| --- | --- |
| **Production BASE** | **base-1** (`CURRENT.json` · [`v2/min/`](v2/min/)) |
| **Candidate pack** | **base-5** ([`v2/base/base-5/`](v2/base/base-5/)) — last breaking freeze; not the pin |
| **Prior candidate** | **base-4** ([`v2/base/base-4/`](v2/base/base-4/)) — Diff / history |
| **Zeus engine (example)** | `0.5.x` (e.g. `0.5.107`) — see [COMPAT.md](COMPAT.md) |
| **zeus_client (Python)** | `0.1.0` (`kotenai-zeus-client`) — see [COMPAT.md](COMPAT.md) |
| **Profile** | `v2_min` |
| **Format** | `zeus.chat_request.v2` |

Each catalog JSON includes `_lineage.base_id`. Customs (Workbench):  
`chat_request_<mode>_base-<N>_cus_<bucket>_<scope>-<rev>.json`.

See [COMPAT.md](COMPAT.md) · process CR-1 / board [CR](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48).

### base-4 (new chat_request line)

| | |
| --- | --- |
| **JSON** | `v2/base/base-4/min/chat_request_<mode>_base-4.json` |
| **Text** | `v2/base/base-4/text/chat_request_<mode>_base-4.txt` |
| **Bible** | [BIBLE.md](docs/BIBLE.md) |
| **base-1 → base-4** | [BASE_1_TO_BASE_4_GUIDE.md](docs/migration/base-1_to_base-4/GUIDE.md) |
| **Multi-round Client** | [MULTI_ROUND_CLIENT.md](docs/MULTI_ROUND_CLIENT.md) |
| **Inspector notes** | [INSPECTOR.md](docs/INSPECTOR.md) |

```bash
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 4 --out v2/base/base-4 --no-set-base-id
```

### Other packs

| Pack | Role |
| --- | --- |
| `v2/base/base-1/` + `v2/min/` | Production pin (legacy `*_v2_min.json`) |
| `v2/base/base-2-prototype/` | Earlier Layer A design fork (history / Diff) |
| `v2/base/base-3-prototype/` | Text-export experiment |

---

## Catalog inspector (`index.html`)

Raw chat_request JSON is large and easy to get lost in. **[index.html](index.html)** is a local web UI that maps one catalog into **colored parts** so you can see what ships in the BASE, what the Client injects at runtime, and how terminate / output is shaped — without scrolling a 15KB+ blob.

Open it after a catalog scan (static site; no backend):

```bash
docker compose up
# http://localhost:3333/

# or without Docker:
python3 scripts/scan_catalogs.py          # builds catalog-index.json
python3 -m http.server 3333 --bind 127.0.0.1
# http://127.0.0.1:3333/
```

### What it shows

| View | Use it for |
| --- | --- |
| **Structure** | Five tabs (full width): **Overview** · **Assembly** (wire order) · **Catalog** (tiles/JSON) · **Wire** · **Output**. |
| **Size map** | Byte/token-ish weight of sections — **Full catalog** vs **Wire payload** (what tends to hit the model). |
| **Diff** | Side-by-side two catalogs (e.g. base-1 pin vs base-4 same mode). |
| **Matrix** | Fingerprints across every `v2/**/chat_request*.json` — click a row to open it in Structure. |
| **Export brief** | Download a Markdown integrator brief for the selected file. |

**Mode dropdown** lists every scanned file as `folder · mode · base_id` (and prototype flags when present). The badge shows `_lineage.base_id`.

### Color legend (same palette as the diagram above)

These chips match the Structure map and [images/assembled_prompt.svg](images/assembled_prompt.svg):

| Color | Meaning |
| --- | --- |
| **RED · Rules** | In the catalog / Contract — changing it changes the **hashed** stamp. |
| **GREEN · Editable / transcript** | Messages and output-shaped areas the Client grows over rounds. |
| **BLUE · Inject** | Client / Zeus runtime inject (scope brief, business rules, session) — **not** hashed with the BASE. |
| **PURPLE · Meta** | Lineage, envelope, Layer A–related meta. |

In-app **Help** explains the chapters in more detail. Deeper notes: [docs/INSPECTOR.md](docs/INSPECTOR.md).

### Deep links

```text
#view=diff&a=v2/min/chat_request_analytics_v2_min.json&b=v2/base/base-4/min/chat_request_analytics_base-4.json
#view=matrix
#view=size
#struct=assembly
#struct=catalog
#struct=output
```

Tip: first migration check is **Diff** the same mode from `v2/min` (base-1) against `v2/base/base-4/min` (base-4).

---

## Why this repo exists

Historically catalogs lived only inside the Zeus engine tree. Clients should **not** need a full Zeus checkout for mode templates.

| Role | Location |
| --- | --- |
| Generator / engine | [koten-ai/Zeus](https://github.com/koten-ai/Zeus) `ai/V2/` |
| Distribution (this repo) | `v2/min/` (pin) · `v2/base/base-N/` |
| Production | **Stamp on your Zeus** then Client sync |

---

## Catalogs (production pin — base-1)

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

Machine index: `manifest.json`. Full scan: `catalog-index.json` (`scripts/scan_catalogs.py`).

---

## File naming

| Kind | Pattern | Example |
| --- | --- | --- |
| **BASE** | `chat_request_<mode>_base-<N>.json` | `chat_request_analytics_base-4.json` |
| **Custom** | `…_base-<N>_cus_<bucket>_<scope>-<rev>.json` | `…_cus_travel-sample_default-1.json` |
| **Legacy pin** | `chat_request_<mode>_v2_min.json` | base-1 / `v2/min` |

`_format: "zeus.chat_request.v2"` is the **envelope**, not the file stem.

---

## Critical rules

1. **Do not invent production `contract_hash` values.** Hub stamp is authoritative.  
2. Prefer **`sync_chat_requests`** from live Zeus after stamp.  
3. Use this repo for demos, scaffolds, MCP fallbacks, docs.  
4. Full (non-min) engine snapshots stay under Zeus `ai/V2/` for Hub A/B.  
5. **Do not over-stuff prompts** — short named `rules` (base-5 objects); company_context ≤150/250 words; see PROMPT_ASSEMBLY budget.  
6. Opt-in **base-4** has **breaking** filename/schema deltas — see [RELEASE_NOTES.md](RELEASE_NOTES.md).  
7. **base-5 design:** named **rules/triggers objects**; **`output_request` → `app_output`**; **settings bag** + rule merge + Client policy table — [docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md](docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [docs/PROMPT_SETTINGS.md](docs/PROMPT_SETTINGS.md) · [docs/ROADMAP.md](docs/ROADMAP.md).

---

## Use with Zeus Client (Python)

```bash
git clone https://github.com/koten-ai/zeus_chat_request.git
export ZEUS_CLIENT_CONFIG_DIR=~/.config/zeus_client
mkdir -p "$ZEUS_CLIENT_CONFIG_DIR/chat_requests"
# After stamping on your Zeus (recommended):
# or for local demo of base-1 pin:
cp zeus_chat_request/v2/min/chat_request_analytics_v2_min.json \
  "$ZEUS_CLIENT_CONFIG_DIR/chat_requests/analytics.json"
```

Production path: `sync_chat_requests(cfg)` after Hub stamp.

---

## Refresh from Zeus (base-1 pin)

```bash
go run . ai-snapshot --mode=all --api-version=v2 --min   # in Zeus
./scripts/sync-from-zeus.sh /path/to/Zeus
python3 scripts/refresh_manifest.py
python3 scripts/scan_catalogs.py
```

## License

Same product family as Zeus / Koten unless otherwise noted.

## Release notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md).
