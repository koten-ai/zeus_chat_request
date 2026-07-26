# Release notes — zeus_chat_request

Published **Zeus V2 chat_request** catalogs for Zeus Client, Developer Helper MCP, demos, and coding agents.

| | |
| --- | --- |
| **Repo** | https://github.com/koten-ai/zeus_chat_request |
| **Format** | `zeus.chat_request.v2` |
| **Production pin** | **base-1** — `CURRENT.json` · `v2/min/` |
| **New BASE line** | **base-4** — `v2/base/base-4/` (not yet the production pin) |
| **Roadmap** | [ROADMAP.md](docs/ROADMAP.md) |
| **Helios emit wishlist** | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |

---

## Unreleased (toward next tag)

### Highlights

- **base-4** established as the **new chat_request BASE line** (`v2/base/base-4/`), with Bible, migration guide, multi-round Client docs, Layer A JSON Schema, lessons learned.
- Intermediate packs: **base-2-prototype** (Layer A design), **base-3-prototype** (text export).
- Authoring docs: prompt assembly, simple/base layout, root **ROADMAP** aligned with **Helios wishlist**.
- Inspector: one `index.html` lists multi-BASE catalogs; scanner understands `*_base-N.json` / `*_cus_*` names.

### Breaking changes

> **Pin is still base-1.** Breakage applies when you **opt in** to base-4 (or base-2-prototype) catalogs or assume only legacy filenames.

| Breaking change | Who is affected | Mitigation |
| --- | --- | --- |
| **Filename pattern** | Loaders that only glob `chat_request_*_v2_min.json` | Also accept `chat_request_<mode>_base-4.json` (and future `base-N`); prefer path from `manifest` / `catalog-index` / Hub sync |
| **`return` / terminating `pipeline` tool parameters grow** | Clients that reject unknown tool JSON Schema properties or freeze a base-1 schema | Treat extra properties as **optional**; keep validating required four; see `response_output_schema.json` |
| **System prompt Terminate contract rewritten (base-4)** | A/B or hash comparisons that assume base-1 system text | Expect new hash after stamp; Diff in inspector base-1 vs base-4 |
| **`_lineage.base_id` / packaging** | Code that assumes only `base-1` or ignores lineage | Read `_lineage.base_id`; customs use `…_cus_<bucket>_<scope>-<rev>` |
| **`_base_meta` replaces ad-hoc notes (base-4 JSON)** | Tools that required `_prototype` key from early prototypes | Prefer `_lineage` + docs; `_base_meta` is non-hashed design metadata |
| **Recommended Layer A fields** (`policy_action`, admin floats, `wish_i_knew`, `business_rules_triggers`) | Integrators who only implement user `summary` | Not required for Detective “core four,” but base-4 docs treat Client/admin paths as part of the product contract |
| **Prototype packs are not production stamps** | Anyone copying `contract.hash` from base-2/3/4 trees into prod | Hub verify/stamp only; never invent hashes |

**Non-breaking for base-1 pin consumers:**  
`v2/min/` and `CURRENT.json` remain base-1; existing `*_v2_min.json` paths and the **required four** terminate fields are unchanged on that pin.

### base-4 (`v2/base/base-4/`)

| Item | Detail |
| --- | --- |
| Files | `min/chat_request_<mode>_base-4.json` · `text/chat_request_<mode>_base-4.txt` |
| Diet | Single `## Terminate (Layer A)` table + example (merged old Evidence-loop + Layer A essays) |
| Layer A required | `summary`, `query_decomposition`, `decomposition`, `confidence` |
| Layer A recommended | `policy_action`, `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `business_rules_triggers`, refs |
| Docs | [BIBLE.md](v2/base/base-4/BIBLE.md) · [BASE_1_TO_BASE_4_GUIDE.md](v2/base/base-4/BASE_1_TO_BASE_4_GUIDE.md) · [lessons-learned.md](v2/base/base-4/lessons-learned.md) · [MULTI_ROUND_CLIENT.md](v2/base/base-4/MULTI_ROUND_CLIENT.md) · [JAILBREAK_POLICY.md](docs/JAILBREAK_POLICY.md) |
| Schema | [response_output_schema.json](v2/base/base-4/response_output_schema.json) |
| Helios | Aligns with wishlist **cost law**; does **not** add Pri-1 Helios fields as always-on AI emits (see ROADMAP) |

### base-3-prototype

- Indented text packs for diet/edit; generator [`scripts/export_base_text.py`](scripts/export_base_text.py).

### base-2-prototype

- Design fork introducing extended Layer A fields and base-N naming (historical / Diff).

### Inspector / tooling

- [`scripts/scan_catalogs.py`](scripts/scan_catalogs.py) — mode parse for `*_base-N.json` and `*_cus_*`.
- [`index.html`](index.html) — multi-BASE dropdown labels; Help for base-1 vs base-4; **one page** (no `index-base-4.html`).

### Docs

- [ROADMAP.md](docs/ROADMAP.md) — base-5+ **and** Helios HEL-WISH sequencing  
- [PROMPT_ASSEMBLY.md](docs/PROMPT_ASSEMBLY.md), [simple_layout.txt](docs/simple_layout.txt), [base_layout.txt](docs/base_layout.txt)  
- [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) — structured Requests (HEL-WISH-001–021)

### Helios (roadmap alignment — not all shipped in catalogs)

| Horizon | Helios focus (see ROADMAP) |
| --- | --- |
| base-5 | Pri-1 cheap spine on **Zeus/Client** (003, 008, 013, 014, 007, 009) + Layer A reliability |
| base-6 | Norms / geo_norm / multi_part / deployment slice (001, 002, 012, 016, …) + G2 Layer A discipline |
| base-7+ | Product events 018/019, stamp/Workbench, pin promote; AI-heavy 010 off hot path |

### Upgrade notes (opt-in base-4)

```bash
# Inspector
python3 scripts/scan_catalogs.py
docker compose up   # http://localhost:3333/index.html — Diff base-1 vs base-4

# Client (sketch)
# 1. Load v2/base/base-4/min/chat_request_<mode>_base-4.json
# 2. Accept extra return properties; validate required four
# 3. Map policy_action / business_rules_triggers when present
# 4. Stamp on Hub before production — do not use prototype/candidate hashes as prod
```

### Known limitations (unreleased)

- Production pin still base-1.  
- base-4 not Hub-stamped by default.  
- Helios Pri-1 report fields are **roadmap**, not all present in catalog JSON.  
- Text packs are not a substitute for stamped JSON in production.

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

### Repo layout (at 0.1.0)

```text
zeus_chat_request/
├── README.md
├── RELEASE_NOTES.md
├── manifest.json
├── scripts/
│   ├── sync-from-zeus.sh
│   └── refresh_manifest.py
└── v2/min/
    └── chat_request_*_v2_min.json
```

### Intended consumers

| Consumer | How to use |
| --- | --- |
| **Zeus Client** (`kotenai-zeus-client`) | Demo/offline templates; production still **stamp + `sync_chat_requests`** |
| **Developer Helper MCP** | `list_catalog_modes` / `fetch_chat_request` |
| **koten_docs** | Contracts / using-zeus-client |
| **Coding agents** | Clone or fetch by mode; never invent `contract_hash` |

### Critical rules (unchanged for all releases)

1. **Templates ≠ production stamps.** Your Hub verify/stamp is authoritative.  
2. Prefer live **`sync_chat_requests`** after ops stamps a scope.  
3. Do **not** hand-edit hashes to clear drift (409) — resync and re-pin.  
4. Engine full (non-min) snapshots remain under Zeus `ai/V2/` for Hub A/B; integrators start with **min** / base-N min trees.

### Related tracking

| Item | Link |
| --- | --- |
| Docs story | [KD-8](https://kotenai.atlassian.net/browse/KD-8) |
| Helper catalog tools | [ZDH-14](https://kotenai.atlassian.net/browse/ZDH-14) |
| Platform docs | [docs.koten.ai](https://docs.koten.ai/) |
| Generator | [koten-ai/Zeus](https://github.com/koten-ai/Zeus) `ai-snapshot --min` |
| Helios wishlist | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |
| Roadmap | [ROADMAP.md](docs/ROADMAP.md) |

### Upgrade / refresh procedure (base-1 pin)

```bash
go run . ai-snapshot --mode=all --api-version=v2 --min   # in Zeus
./scripts/sync-from-zeus.sh /path/to/Zeus
python3 scripts/refresh_manifest.py
python3 scripts/scan_catalogs.py   # inspector index
```

### Breaking changes (0.1.0)

None (initial release).

### Known limitations (0.1.0)

- No full (non-min) profile published yet — min only.  
- No use-case-specific catalogs in this tree yet.  
- Private clones may need `GITHUB_TOKEN` / `ZEUS_CHAT_REQUEST_DIR` for Helper MCP.  
