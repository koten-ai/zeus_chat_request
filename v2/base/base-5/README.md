# base-5

Ship pack for chat_request catalogs — **last breaking wire/control-plane freeze** on this line ([docs/ROADMAP.md](../../../docs/ROADMAP.md)).

**Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-5` |
| **Status** | **Candidate pack** — not production pin |
| **Production pin** | Still **base-1** (`CURRENT.json` / `v2/min`) |
| **JSON** | [`min/chat_request_<mode>_base-5.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-5.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Overview** | [OVERVIEW.md](OVERVIEW.md) |
| **Roadmap / breaking law** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **Rules + output_request** | [RULES_OBJECT…](../../../docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md) |
| **Control plane** | [PROMPT_SETTINGS.md](../../../docs/PROMPT_SETTINGS.md) |
| **Hop base-4 → base-5** | [migration/base-4_to_base-5/](../../../docs/migration/base-4_to_base-5/) |
| **Release checklist** | [RELEASE_CHECKLIST.md](../../../docs/migration/base-4_to_base-5/RELEASE_CHECKLIST.md) |
| **AI playbook** | [BASE_AGENT_PLAYBOOK.md](../../../docs/BASE_AGENT_PLAYBOOK.md) · [AGENTS.md](../../../AGENTS.md) |
| **Versions** | [COMPAT.md](../../../COMPAT.md) |

## Breaking vs base-4 (summary)

| base-4 | base-5 |
| --- | --- |
| `business_rules_triggers: boolean[]` | **`{ rule_id: bool }` object** (sparse) |
| inject `rules[]` (design) | inject **`rules{}`** object |
| no first-class app bag | optional **`app_output`** (Client `output_request` type+description) |
| informal Client control plane | settings bag + policy table (documented for Client) |

## Naming

```text
chat_request_analytics_base-5.json
chat_request_analytics_base-5.txt
chat_request_analytics_base-5_cus_<bucket>_<scope>-1.json
```

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-5/min --base 5 --out v2/base/base-5 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 5
python3 scripts/scan_catalogs.py
```
