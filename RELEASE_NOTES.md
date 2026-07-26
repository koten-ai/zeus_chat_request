# Release notes — zeus_chat_request

Published **Zeus V2 chat_request** catalogs for Zeus Client, Developer Helper MCP, demos, and coding agents.

| | |
| --- | --- |
| **Repo** | https://github.com/koten-ai/zeus_chat_request |
| **Format** | `zeus.chat_request.v2` |
| **Production pin** | **base-1** — `CURRENT.json` · `v2/min/` |
| **Candidate pack** | **base-5** — `v2/base/base-5/` (last breaking freeze; not pin) |
| **Content train** | **base-5.1** — mode overlays in system prompt (same pack path; not a wire break) |
| **Prior candidate** | **base-4** — `v2/base/base-4/` |
| **Roadmap** | [ROADMAP.md](docs/ROADMAP.md) |
| **Modes** | [MODE.md](docs/MODE.md) · [work/RECREATE_MODE.md](work/RECREATE_MODE.md) |
| **Helios emit wishlist** | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |

---

## Unreleased (toward next tag)

### Highlights

- **base-5.1 (content on base-5 wire):** system prompts are **CORE + MODE_OVERLAY** per mode (DESIGN §14 personas). Packs no longer “analytics × rename.” Author under `work/mode_overlays/`; assemble with `scripts/assemble_mode_prompts.py`. Clone gate: `scripts/diff_modes.py --fail-if-clone`. Jira **CR-23**.
- **base-5 candidate pack** on disk: [`v2/base/base-5/`](v2/base/base-5/) — **last breaking wire/control-plane freeze** (objects, `app_output`, inject contracts). Pin remains **base-1**.
- Hop docs: [docs/migration/base-4_to_base-5/](docs/migration/base-4_to_base-5/) (GUIDE, lessons, RELEASE_CHECKLIST).
- **base-4** remains available for Diff/history (`v2/base/base-4/`).
- Docs/process: AI playbook, COMPAT, RELEASE_CHECKLIST, `verify_base_pack.py`, `new_base.py`.

### Breaking changes (opt-in **base-5**)

> **Pin is still base-1.** These apply when you **opt in** to base-5 catalogs.

| Breaking change | Who is affected | Mitigation |
| --- | --- | --- |
| **`business_rules_triggers` is an object** `{ rule_id: bool }` (not `boolean[]`) | Clients/parsers assuming array indexes | Parse object; missing key = false; dual-read arrays ≤1 Client release |
| **Inject `rules` is an object** `{ id: text }` | Clients building parallel arrays | Use named keys; merge/freeze per PROMPT_SETTINGS |
| **Optional `app_output`** on terminate | Strict tool schema rejecting unknown props | Allow optional object; validate against Client `output_request` |
| **`output_request` fields need type + description** | Type-only maps | Client renders descriptions into prompt; reject type-only |
| **Filename `*_base-5.json`** | Loaders only knowing `v2_min` or base-4 | Accept `base-N` pattern from COMPAT / manifest |
| **New stamp required** for any production use of base-5 | Anyone copying scaffold hashes | Hub verify/stamp only |

### Breaking changes (opt-in **base-4** / prototypes — still valid)

> Breakage when opting into base-4 (or base-2-prototype) vs base-1 pin only.

| Breaking change | Who is affected | Mitigation |
| --- | --- | --- |
| **Filename pattern** | Loaders that only glob `*_v2_min.json` | Accept `*_base-N.json` |
| **`return` / pipeline params grow** (recommended Layer A) | Strict unknown-property clients | Treat extra props optional; required four unchanged |
| **Terminate contract rewritten (base-4)** | Hash comparisons to base-1 system text | New stamp after opt-in |
| **Prototype packs are not production stamps** | Copying `contract.hash` from trees | Hub stamp only |

**Non-breaking for base-1 pin consumers:**  
`v2/min/` and `CURRENT.json` remain base-1; existing `*_v2_min.json` paths and the **required four** terminate fields are unchanged on that pin.

### base-4 (`v2/base/base-4/`)

| Item | Detail |
| --- | --- |
| Files | `min/chat_request_<mode>_base-4.json` · `text/chat_request_<mode>_base-4.txt` |
| Diet | Single `## Terminate (Layer A)` table + example (merged old Evidence-loop + Layer A essays) |
| Layer A required | `summary`, `query_decomposition`, `decomposition`, `confidence` |
| Layer A recommended | `policy_action`, `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `business_rules_triggers`, refs |
| Docs | [BIBLE.md](docs/BIBLE.md) · [BASE_1_TO_BASE_4_GUIDE.md](docs/migration/base-1_to_base-4/GUIDE.md) · [lessons-learned.md](docs/migration/base-1_to_base-4/lessons-learned.md) · [MULTI_ROUND_CLIENT.md](docs/MULTI_ROUND_CLIENT.md) · [JAILBREAK_POLICY.md](docs/JAILBREAK_POLICY.md) |
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
