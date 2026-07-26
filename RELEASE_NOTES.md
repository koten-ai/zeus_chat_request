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

### base-4-prototype (terminate diet)

- [`v2/base/base-4-prototype/`](v2/base/base-4-prototype/) — JSON + text
- **Diet:** single `## Terminate (Layer A) — copy this shape` (field table + one example return)
- Removed duplicate Evidence-loop + Layer A prototype essays from system prompt
- Files: `chat_request_<mode>_base-4.json` / `.txt`
- Parent lineage: base-3 / base-2-prototype
- Migration guide: [`BASE_1_TO_BASE_4_GUIDE.md`](v2/base/base-4-prototype/BASE_1_TO_BASE_4_GUIDE.md)
- Full requirements bible: [`BIBLE.md`](v2/base/base-4-prototype/BIBLE.md)

### base-3-prototype (text export for diet)

- [`v2/base/base-3-prototype/`](v2/base/base-3-prototype/) — indented **text** packs (`chat_request_<mode>_base-3.txt`, lineage `base_id: base-3`)
- Generator: [`scripts/export_base_text.py`](scripts/export_base_text.py) for base-4/5/6… iterations
- Not stampable until re-encoded to `chat_request_<mode>_base-N.json`

### base-2-prototype (design / feedback)

- New tree [`v2/base/base-2-prototype/`](v2/base/base-2-prototype/) forked from `base-1` min catalogs  
- **Filename convention (BASE):** `chat_request_<mode>_base-2-prototype.json` (not `*_v2_min.json` / `*_v2.json`)  
- **Filename convention (customs):** `chat_request_<mode>_base-2_cus_<bucket>_<scope>-<rev>.json` (Hub Workbench / Prompt Helper; rev increments on save)  
  e.g. `…_base-2_cus_travel-sample_default-1.json` → `…-2.json`  
- Extended **Layer A** `return` / terminating `pipeline` schema: `policy_action`, `subject_confidence`, `jail_break_attempt` (0.0–1.0), `wish_i_knew` (max 3), `business_rules_triggers[]`, refs  
- System prompt addendum + `_prototype` metadata + [PROTOTYPE.md](v2/base/base-2-prototype/PROTOTYPE.md)  
- Samples: [`samples/terminate_response*.json`](samples/)  
- **Does not** change `CURRENT.json` or `v2/min` alias (still base-1)  
- **May break** consumers that assume base-1-only tool parameters — intentional for zeus_client feedback  

### Docs — assembled prompt mental model (authoring)

- **[PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md)** — Zeus rules → Client inject → user → terminate (G1/G2/G3); token budget guidance  
- **[simple_layout.txt](simple_layout.txt)** — field map: Contract vs `zeus_client` pass-in, `business_injection.rules[]` / `business_rules_triggers[]`, admin scores (`wish_i_knew`, `jail_break_attempt` 0.0..1.0), brand boilerplate  
- **[base_layout.txt](base_layout.txt)** — bridge + original sketch corrections  
- Cross-links from [CHAT_REQUEST.md](CHAT_REQUEST.md) and [README.md](README.md)  

These are **design / authoring** docs. They do not change published `v2/min` JSON hashes by themselves. Wire fields for Client inject/triggers land with zeus_client + engine work.

### Catalog (still optional backlog)

- Optional: full V2 profile mirror  
- Optional: use-case / vertical catalogs  
- Optional: signed release artifacts / CI sync from Zeus  
