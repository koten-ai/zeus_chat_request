# Documentation

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · design line **base-4** (base-5 = design only) · version matrix: [COMPAT.md](../COMPAT.md)


Educational and design docs for **zeus_chat_request**.  
Catalog **JSON packs** live under `v2/base/base-N/` (not here). Production pin is still **base-1** until promote.

## Layout (where things go)

| Location | Put here | Do **not** put here |
| --- | --- | --- |
| **`docs/`** | Cross-BASE product design: Bible, assembly, rules, settings, jailbreak, roadmap, multi-round, inspector notes | Per-mode catalog JSON |
| **`docs/base-1_to_base-4/`** | Migration-only narrative for **this** bump (guide + lessons) | Living design that still evolves for base-5+ |
| **`docs/CREATE_BASE.md`** | Process to cut a new `base-N` pack | — |
| **`v2/base/base-N/`** | **Ship pack:** `min/`, `text/`, `MANIFEST.json`, `response_output_*.json`, short `README.md` / `OVERVIEW.md` | Long design essays (those stay in `docs/`) |
| **`samples/`** | Generic terminate samples (not pack-specific) | BASE diet docs |

```text
docs/                          ← humans + agents (design)
  BIBLE.md                     ← current design-line requirements (base-4 era)
  MULTI_ROUND_CLIENT.md
  multi_round_example.json
  PROMPT_ASSEMBLY.md
  PROMPT_SETTINGS.md
  RULES_OBJECT_AND_OUTPUT_REQUEST.md
  JAILBREAK_POLICY.md
  ROADMAP.md
  CHAT_REQUEST.md
  HELIOS_WISHLIST_FOR_CHAT_REQUEST.md
  INSPECTOR.md
  CREATE_BASE.md               ← how to make base-N
  base-1_to_base-4/            ← migration archive for 1→4
  simple_layout.txt · base_layout.txt

v2/base/base-4/                ← pack (what Client/stamp load)
  min/*.json
  text/*.txt
  MANIFEST.json
  response_output_schema.json
  response_output_example.json
  README.md · OVERVIEW.md
```

## Start here

| Doc | Topic |
| --- | --- |
| [BIBLE.md](BIBLE.md) | Full requirements + ownership matrix (set/unset/change) |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Assembled prompt wire order |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings bag · rule merge · Client policy · security |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules + `output_request` (type + description) |
| [ROADMAP.md](ROADMAP.md) | base-5 / base-6+ + Helios |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold a new `base-N` pack |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + named rules + hooks |
| [CHAT_REQUEST.md](CHAT_REQUEST.md) | What a catalog is, contracts, Client vs Hub |
| [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) | Middleman multi-round |
| [INSPECTOR.md](INSPECTOR.md) | One `index.html` for multi-BASE |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Helios emit requests (cost-aware) |
| [../images/assembled_prompt.svg](../images/assembled_prompt.svg) | Diagram |

## Migration (base-1 → base-4)

| Doc | Topic |
| --- | --- |
| [base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md](base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md) | Field / behavior map |
| [base-1_to_base-4/lessons-learned.md](base-1_to_base-4/lessons-learned.md) | What went wrong / right |

## Pack on disk (base-4 catalogs)

| Path | Topic |
| --- | --- |
| [../v2/base/base-4/README.md](../v2/base/base-4/README.md) | Pack entry |
| [../v2/base/base-4/OVERVIEW.md](../v2/base/base-4/OVERVIEW.md) | Diet changelog only |
| [../v2/base/base-4/response_output_schema.json](../v2/base/base-4/response_output_schema.json) | Layer A JSON Schema |
| [../v2/base/base-4/response_output_example.json](../v2/base/base-4/response_output_example.json) | Terminate example |

## Version matrix

| Doc | Role |
| --- | --- |
| [../COMPAT.md](../COMPAT.md) | **SoT** — Zeus engine × chat_request BASE × zeus_client |

## Root (not under docs/)

| Doc | Why at root |
| --- | --- |
| [../README.md](../README.md) | Project entry + diagram |
| [../RELEASE_NOTES.md](../RELEASE_NOTES.md) | Releases + breaking changes |
| [../COMPAT.md](../COMPAT.md) | Version matrix (three products) |
