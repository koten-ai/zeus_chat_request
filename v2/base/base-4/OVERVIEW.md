# base-4 overview

Short pack changelog only. Full requirements: [docs/BIBLE.md](../../../docs/BIBLE.md).

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **JSON** | `min/chat_request_<mode>_base-4.json` |
| **Text** | `text/chat_request_<mode>_base-4.txt` |
| **Parent** | base-3 (text pack) / base-2-prototype (JSON source) |
| **Production pin** | Still base-1 until CURRENT.json promotes |
| **Bible** | [docs/BIBLE.md](../../../docs/BIBLE.md) |
| **base-1 → base-4 map** | [docs/migration/base-1_to_base-4/](../../../docs/migration/base-1_to_base-4/) |
| **Roadmap** | [docs/ROADMAP.md](../../../docs/ROADMAP.md) |
| **Multi-round** | [docs/MULTI_ROUND_CLIENT.md](../../../docs/MULTI_ROUND_CLIENT.md) |
| **Create next BASE** | [docs/CREATE_BASE.md](../../../docs/CREATE_BASE.md) |

## What changed

**Removed from system prompt:**

- `## Evidence loop / hot-path return contract (CRITICAL)`
- `## Layer A terminate contract (base-2-prototype)`

**Added:**

- `## Terminate (Layer A) — copy this shape`
- Field table: req | audience | type
- One-line distinctions (`query_decomposition` vs `wish_i_knew`, dual confidence)
- One full example `return` skeleton
- Shorter `return` / `pipeline` descriptions pointing at that section

## Unchanged

- 13 verbs + full parameter schemas
- Required: summary, query_decomposition, decomposition, confidence
- Recommended admin/client fields
- Execution style + efficiency + verb priority sections

## Naming

```text
chat_request_analytics_base-4.json
chat_request_analytics_base-4.txt
chat_request_analytics_base-4_cus_travel-sample_default-1.json
```

## Regenerate text

```bash
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 4 --out v2/base/base-4 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 4
```
