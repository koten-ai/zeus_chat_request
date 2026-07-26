# Documentation

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · candidate pack **base-5** · prior candidate **base-4** · version matrix: [COMPAT.md](../COMPAT.md)


Educational and design docs for **zeus_chat_request**.  
Catalog **JSON packs** live under `v2/base/base-N/` (not here). Production pin is still **base-1** until promote.

## Layout (where things go)

| Location | Put here | Do **not** put here |
| --- | --- | --- |
| **`docs/`** | Cross-BASE product design: Bible, assembly, rules, settings, jailbreak, roadmap, multi-round, inspector, **AI playbook** | Per-mode catalog JSON |
| **`docs/migration/base-X_to_base-Y/`** | **Hop archives** (GUIDE + lessons) for each upgrade | Living design that still evolves |
| **`docs/CREATE_BASE.md`** | Process to cut a new `base-N` pack | — |
| **`v2/base/base-N/`** | **Ship pack:** `min/`, `text/`, `MANIFEST.json`, `response_output_*.json`, short `README.md` / `OVERVIEW.md` | Long design essays (those stay in `docs/`) |
| **`samples/`** | Generic terminate samples (not pack-specific) | BASE diet docs |
| **Root `AGENTS.md`** | Short AI entry | Full checklists (those live in the playbook) |

```text
docs/
  BASE_AGENT_PLAYBOOK.md       ← AI: comply with base-X / upgrade X→Y
  BIBLE.md · PROMPT_* · RULES_* · ROADMAP · …
  CREATE_BASE.md
  migration/
    README.md
    base-1_to_base-4/          ← GUIDE.md + lessons
    base-4_to_base-5/          ← stub (design only)

v2/base/base-N/                ← pack only (min, text, MANIFEST, Layer A schemas)
AGENTS.md                      ← repo root: agent start here
COMPAT.md                      ← Zeus × BASE × zeus_client
```

## Start here

| Doc | Topic |
| --- | --- |
| [../AGENTS.md](../AGENTS.md) | **AI entry** — hard rules + where to go |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | Comply with base-X · upgrade X→Y (checklists) |
| [BIBLE.md](BIBLE.md) | Full requirements + ownership matrix (set/unset/change) |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Assembled prompt wire order |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings bag · rule merge · Client policy · security |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules + `output_request` (type + description) |
| [ROADMAP.md](ROADMAP.md) | base-5 / base-6+ + Helios |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold a new `base-N` pack |
| [migration/README.md](migration/README.md) | All BASE upgrade hops |
| [migration/RELEASE_CHECKLIST_TEMPLATE.md](migration/RELEASE_CHECKLIST_TEMPLATE.md) | **BASE bump release checklist** (copy per hop) |
| [migration/base-4_to_base-5/RELEASE_CHECKLIST.md](migration/base-4_to_base-5/RELEASE_CHECKLIST.md) | Filled checklist for base-5 |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + named rules + hooks |
| [CHAT_REQUEST.md](CHAT_REQUEST.md) | What a catalog is, contracts, Client vs Hub |
| [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) | Middleman multi-round |
| [INSPECTOR.md](INSPECTOR.md) | One `index.html` for multi-BASE |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Helios emit requests (cost-aware) |
| [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) | **zeus_client** backlog (base-5 floor → base-6+) |
| [MODE.md](MODE.md) | **Modes** — engine vs catalog; why packs converged; overlay model |
| [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) | **base-5.2** — classic `wish_i_knew` + `data_gaps` for Helios |
| [../work/RECREATE_MODE.md](../work/RECREATE_MODE.md) | **Plan** — restore mode overlays into system prompt (`messages[].content`) |
| [../images/assembled_prompt.svg](../images/assembled_prompt.svg) | Diagram |

## Migration hops

| Hop | Path |
| --- | --- |
| Index | [migration/README.md](migration/README.md) |
| base-1 → base-4 | [migration/base-1_to_base-4/](migration/base-1_to_base-4/) |
| base-4 → base-5 | [migration/base-4_to_base-5/](migration/base-4_to_base-5/) (candidate pack on disk; pin still base-1) |

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
