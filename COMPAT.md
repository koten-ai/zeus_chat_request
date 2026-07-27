# Compatibility matrix — Zeus · chat_request BASE · zeus_client

**Last reviewed:** 2026-07-27  
**Status:** living matrix (CR-1). Warnings first; hard gates later (ZE-222 / ZE-223).  
**This file is the only place for three-product version compatibility.**

| Product | Identity | Machine source of truth |
| --- | --- | --- |
| **Zeus engine** | semver (`x.y.z`) | Zeus repo `main.go` → `const Version` |
| **chat_request BASE** | `base-N` | `CURRENT.json` (pin) · pack `_lineage.base_id` / `MANIFEST.json` |
| **zeus_client** | package semver | Python: `zeus_client_python/pyproject.toml` → `project.version` (`kotenai-zeus-client`) |

These three versions are **independent**. A BASE bump does not imply a Zeus minor bump; a Client bump does not change `contract_hash`.

---

## 1. Production pin (today)

| Field | Value |
| --- | --- |
| **Zeus engine 0.5.x line** | e.g. `0.5.107` — still **base-1** runtime for that train |
| **Zeus engine 0.6.x line** | **`0.6.15+`** — **vendors base-5.3** (`PIN.json` + embed `pin.json`; [ZE-273](https://kotenai.atlassian.net/browse/ZE-273)) — **breaking** vs 0.5 |
| **chat_request production pin (CURRENT)** | **`base-1`** — [`CURRENT.json`](CURRENT.json) · [`v2/min/`](v2/min/) until stamp + Client + Detective green on CURRENT flip |
| **chat_request Zeus 0.6 vendor pin** | **`base-5.3`** — pack [`v2/base/base-5.3/`](v2/base/base-5.3/) (content train; same base-5 wire as 5.2) |
| **chat_request candidates** | base-5 … **base-5.3** (Zeus vendor) · **base-6** (soft `hints.*` contract; Client inject residual) |
| **zeus_client (Python)** | **`0.1.0`** — object floor TBD until Client ships base-5 wire |
| **Helios** | **0.6.x** pairs Zeus **0.6.x** (HEL-17); do not run Helios 0.2 Analytics against base-5.2 report shapes |
| **Envelope** | `_format: "zeus.chat_request.v2"` |

Zeus operator matrix (surface checklist): Zeus repo [`docs/ops/COMPAT.md`](https://github.com/koten-ai/Zeus/blob/5TH/docs/ops/COMPAT.md).

---

## 2. Supported triples

| Zeus engine | chat_request BASE | zeus_client | Helios | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| **`0.6.15` – `0.6.x`** | **`base-5.3`** (vendor; ZE-273) | *TBD* object floor; no dual-read string wish / array triggers | **0.6.x** | **supported (Zeus 0.6 train)** | Same base-5 wire as 5.2; world-model CORE + verb clarity; not CURRENT |
| `0.6.0` – `0.6.14` | **`base-5.2`** (prior vendor) | same | **0.6.x** | **history** | Prefer upgrade to 0.6.15+ for order.asc / CORE fixes |
| `0.5.0` – `0.5.x` | **`base-1`** | `≥ 0.1.0` | 0.2.x | **supported (prior)** | Production CURRENT pin path |
| `0.5.x` / `0.6.x` trial | base-4 / base-5 / base-5.1 / base-5.2 / **base-5.3** / **base-6** packs | *TBD* | — | **candidate / history** | base-6 = additive soft hints contract; prefer base-5.3 until Client injects hints |
| `0.6.x` | base-1 | any | any | **unsupported** | Wrong wire for 0.6 Detective/report |
| *future* | **`base-6+`** live inject | base-5 floor + soft `hints.*` | matching | **additive only** | No rename/remove of base-5 wire without new major · ZC-WISH-040 |
| *future* | promoted pin (`CURRENT` → base-5.2+) | matching Client floor | matching | — | Only after stamp + Client + Detective green |

**Status legend**

| Status | Meaning |
| --- | --- |
| **supported** | Safe default for production integrators |
| **candidate / opt-in** | Use for trials; expect stamp + Client updates; not the pin |
| **design only** | Spec in `docs/`; catalogs/Client not required to implement yet |

### Prototypes (never in the production pin row)

| Id | Notes |
| --- | --- |
| `base-2-prototype` | Historical Layer A fork — Diff only |
| `base-3-prototype` | Text-export experiment — Diff only |

---

## 3. Feature capability by BASE (what Client must handle)

| Capability | base-1 (pin) | base-4 (history) | base-5 (candidate pack) |
| --- | --- | --- | --- |
| Required four: `summary`, `query_decomposition`, `decomposition`, `confidence` | **yes** | **yes** | **yes** |
| Filename `*_v2_min.json` | **yes** (legacy pin) | no | no |
| Filename `*_base-N.json` | lineage only | **yes** (`base-4`) | **yes** (`base-5`) |
| Recommended Layer A (`policy_action`, scores, `wish_i_knew`) | informal / absent | **recommended** | **recommended** + soft-require `policy_action` |
| `business_rules_triggers` | — | `boolean[]` | **`{ id: bool }` object only** (sparse) |
| Inject `rules` | free text / informal | array design | **named object only** + merge/freeze |
| `company_context` + jailbreak rule pack | no | score field only | **documented inject** |
| `output_request` → `app_output` | informal `structured` | informal | **schema + tool params** (`type` + `description`) |
| Settings bag | ad hoc config | ad hoc | **formal** ([PROMPT_SETTINGS](docs/PROMPT_SETTINGS.md)) |
| Client post-terminate policy table | app-defined | recommended | **normative** (Client implement) |

Detail: [docs/BIBLE.md](docs/BIBLE.md) · [docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md](docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [docs/PROMPT_SETTINGS.md](docs/PROMPT_SETTINGS.md).

---

## 4. Rules

1. **BASE** is `base-N` (monotonic). It is **not** Zeus semver and **not** the Client package version.  
2. **Customs** (`…_cus_<bucket>_<scope>-<rev>`) always set `parent_base_id = base-N`. Compat rows apply to the **parent BASE**.  
3. Runtime injects (SCOPE BRIEF, MINI-SCHEMA, `business_injection`, `output_request`) are **not** BASE identity (not in contract hash).  
4. Client / Workbench **should warn** (later **refuse**) when:
   - `base_id` is missing, or  
   - the triple (Zeus, BASE, Client) is outside this matrix for the deployment mode (prod vs trial).  
5. **Do not invent** production `contract_hash` values — Hub stamp is authoritative.  
6. When any product bumps a row that changes support, **update this file in the same change set** (or immediately after).

### File naming

| Kind | Pattern |
| --- | --- |
| BASE | `chat_request_<mode>_base-<N>.json` |
| BASE text | `chat_request_<mode>_base-<N>.txt` |
| Custom | `chat_request_<mode>_base-<N>_cus_<bucket>_<scope>-<rev>.json` |
| Legacy pin | `chat_request_<mode>_v2_min.json` (base-1 / `v2/min` only) |

Scaffold process: [docs/CREATE_BASE.md](docs/CREATE_BASE.md) · `scripts/new_base.py`.

---

## 5. How to bump each product

### chat_request BASE

1. Scaffold: `python3 scripts/new_base.py --from v2/base/base-N --base N+1`  
2. Diet catalogs + Layer A schemas; re-export text; refresh MANIFEST.  
3. Update this matrix (candidate row).  
4. Zeus: generator / snapshot / PIN when promoting.  
5. Hub stamp → Client sync → only then flip `CURRENT.json`.

### Zeus engine

1. Bump `main.go` `Version`.  
2. If catalog/generator contract changes, add/adjust BASE rows here.  
3. Ship stamp path for any new required Layer A / verb behavior.

### zeus_client

1. Bump package version in `pyproject.toml` (Python).  
2. Document which BASE features that version implements (array vs object triggers, `output_request`, settings bag).  
3. Update the **Supported triples** table (Client column / TBD floors).

---

## 6. Related docs

| Doc | Role |
| --- | --- |
| [AGENTS.md](AGENTS.md) | AI entry — hard rules |
| [docs/BASE_AGENT_PLAYBOOK.md](docs/BASE_AGENT_PLAYBOOK.md) | **Comply with base-X / upgrade X→Y** (checklists for catalog + Zeus + Client) |
| [docs/migration/README.md](docs/migration/README.md) | Hop archives `base-X_to_base-Y` |
| [docs/README.md](docs/README.md) | Doc hub + layout rules |
| [docs/BIBLE.md](docs/BIBLE.md) | Normative base-4-era requirements + ownership |
| [docs/ROADMAP.md](docs/ROADMAP.md) | base-5+ plan |
| [docs/CREATE_BASE.md](docs/CREATE_BASE.md) | New pack process |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | What shipped + breaking changes |
| [CURRENT.json](CURRENT.json) | Production BASE pin |

**Implementing a matrix row:** follow [BASE_AGENT_PLAYBOOK.md](docs/BASE_AGENT_PLAYBOOK.md), then record the hop under `docs/migration/base-X_to_base-Y/`.

---

*Draft CR-1. Fill TBD Client floors when `zeus_client_python` implements base-4/5 spikes — do not invent semver.*
