# base-4-prototype

> **Start here for full requirements:** [**BIBLE.md**](BIBLE.md) — step-by-step rules, naming, Layer A, multi-round Client, examples, checklists.

**Diet release:** one **Terminate (Layer A)** table + one example (replaces two long essays).

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **JSON** | `min/chat_request_<mode>_base-4.json` |
| **Text** | `text/chat_request_<mode>_base-4.txt` |
| **Parent** | base-3 (text pack) / base-2-prototype (JSON source) |
| **Production** | No |
| **Bible (full requirements)** | [**BIBLE.md**](BIBLE.md) |
| **base-1 → base-4 map** | [BASE_1_TO_BASE_4_GUIDE.md](BASE_1_TO_BASE_4_GUIDE.md) |
| **Lessons learned** | [lessons-learned.md](lessons-learned.md) |
| **Multi-round Client** | [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) · [multi_round_example.json](multi_round_example.json) |

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
python3 scripts/export_base_text.py --from v2/base/base-4-prototype/min --base 4
```
