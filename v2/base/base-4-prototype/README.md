**Start here:** [**BIBLE.md**](BIBLE.md) · **From base-1:** [BASE_1_TO_BASE_4_GUIDE.md](BASE_1_TO_BASE_4_GUIDE.md) · **Lessons:** [lessons-learned.md](lessons-learned.md) — complete base-4 requirements and examples.

# base-4-prototype

Indented **text** working copy for diet/edit iterations.

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **Files** | `text/chat_request_<mode>_base-4.txt` |
| **Later JSON** | `chat_request_<mode>_base-4.json` |
| **Customs** | `chat_request_<mode>_base-4_cus_<bucket>_<scope>-<rev>.json` |
| **Source** | `v2/base/base-4-prototype/min` |
| **Generator** | `scripts/export_base_text.py --base 4` |

## Regenerate / next base

```bash
# this pack again
python3 scripts/export_base_text.py --from v2/base/base-4-prototype/min --base 4

# next iteration (example)
python3 scripts/export_base_text.py --from v2/base/base-4-prototype/min --base 5
```

## Files

- [`text/chat_request_analytics_base-4.txt`](text/chat_request_analytics_base-4.txt) — mode `analytics`
- [`text/chat_request_auto_base-4.txt`](text/chat_request_auto_base-4.txt) — mode `auto`
- [`text/chat_request_code_base-4.txt`](text/chat_request_code_base-4.txt) — mode `code`
- [`text/chat_request_custom_base-4.txt`](text/chat_request_custom_base-4.txt) — mode `custom`
- [`text/chat_request_fraud_base-4.txt`](text/chat_request_fraud_base-4.txt) — mode `fraud`
- [`text/chat_request_open_base-4.txt`](text/chat_request_open_base-4.txt) — mode `open`
- [`text/chat_request_private_base-4.txt`](text/chat_request_private_base-4.txt) — mode `private`
- [`text/chat_request_regulated_base-4.txt`](text/chat_request_regulated_base-4.txt) — mode `regulated`
- [`text/chat_request_research_base-4.txt`](text/chat_request_research_base-4.txt) — mode `research`
- [`text/chat_request_tenant_base-4.txt`](text/chat_request_tenant_base-4.txt) — mode `tenant`

## Workflow

```text
JSON catalogs → export_base_text.py → base-N-prototype text
  → edit/diet
  → re-encode JSON (separate step)
  → stamp / Client
```
