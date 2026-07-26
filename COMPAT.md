# Compatibility matrix — Zeus · chat_request BASE · zeus_client

**Last reviewed:** 2026-07-26  
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
| **Zeus engine (example latest)** | `0.5.107` (line `0.5.x`) |
| **chat_request production pin** | **`base-1`** — [`CURRENT.json`](CURRENT.json) · [`v2/min/`](v2/min/) |
| **chat_request design / candidate pack** | **`base-4`** — [`v2/base/base-4/`](v2/base/base-4/) (opt-in, **not** pin) |
| **chat_request next design (docs only)** | **base-5** — see [`docs/ROADMAP.md`](docs/ROADMAP.md) (no pack until scaffold) |
| **zeus_client (Python)** | **`0.1.0`** — package `kotenai-zeus-client` |
| **Envelope** | `_format: "zeus.chat_request.v2"` |

---

## 2. Supported triples

| Zeus engine | chat_request BASE | zeus_client | Status | Notes |
| --- | --- | --- | --- | --- |
| `0.5.0` – `0.5.x` | **`base-1`** | `≥ 0.1.0` | **supported** | Production pin; required four Layer A |
| `0.5.x` (current line) | **`base-4`** | `≥ 0.1.0` + optional Layer A G2/G3 | **candidate / opt-in** | Pack on disk; not `CURRENT`; Client should accept extra terminate fields |
| *future* | **`base-5`** | *TBD* (settings bag, object rules, `output_request`) | **design only** | Docs in [`docs/ROADMAP.md`](docs/ROADMAP.md); no pin |
| *future* | `base-2`+ promoted pin | *TBD* | — | Only after stamp + Client + Detective green |

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

| Capability | base-1 (pin) | base-4 (candidate) | base-5 (design) |
| --- | --- | --- | --- |
| Required four: `summary`, `query_decomposition`, `decomposition`, `confidence` | **yes** | **yes** | **yes** |
| Filename `*_v2_min.json` | **yes** (legacy pin) | no (uses `*_base-4.json`) | `*_base-5.json` |
| Filename `*_base-N.json` | lineage only | **yes** | **yes** |
| Recommended Layer A (`policy_action`, scores, `wish_i_knew`) | informal / absent | **recommended** | **recommended** + soft-require paths |
| `business_rules_triggers` | — | `boolean[]` (index-aligned) | **`{ id: bool }` object** (sparse) |
| Inject `rules` | free text / informal | design: array | **named object** + merge/freeze |
| `company_context` + jailbreak rule pack in prompt | no | score field only | **yes** (design) |
| `output_request` → `app_output` | informal `structured` | informal | **`type` + `description` per field** |
| Settings bag (max_rounds, locale, redaction, …) | ad hoc config | ad hoc | **formal** ([PROMPT_SETTINGS](docs/PROMPT_SETTINGS.md)) |
| Client post-terminate policy table | app-defined | recommended | **normative** |

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
| [docs/README.md](docs/README.md) | Doc hub + layout rules |
| [docs/BIBLE.md](docs/BIBLE.md) | Normative base-4-era requirements + ownership |
| [docs/ROADMAP.md](docs/ROADMAP.md) | base-5+ plan |
| [docs/CREATE_BASE.md](docs/CREATE_BASE.md) | New pack process |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | What shipped + breaking changes |
| [CURRENT.json](CURRENT.json) | Production BASE pin |

---

*Draft CR-1. Fill TBD Client floors when `zeus_client_python` implements base-4/5 spikes — do not invent semver.*
