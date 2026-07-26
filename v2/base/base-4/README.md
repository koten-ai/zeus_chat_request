# base-4

**The new chat_request BASE line** (directory `v2/base/base-4`, not `base-4-prototype`).

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **JSON** | [`min/chat_request_<mode>_base-4.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-4.txt`](text/) |
| **Start here** | [**BIBLE.md**](BIBLE.md) |
| **From base-1** | [BASE_1_TO_BASE_4_GUIDE.md](BASE_1_TO_BASE_4_GUIDE.md) |
| **Lessons** | [lessons-learned.md](lessons-learned.md) |
| **Roadmap** | [ROADMAP.md](../../../docs/ROADMAP.md) |
| **Overview / diet notes** | [OVERVIEW.md](OVERVIEW.md) |
| **Inspector** | [INSPECTOR.md](INSPECTOR.md) — one `index.html` for base-1 + base-4 |
| **Jailbreak policy** | [JAILBREAK_POLICY.md](../../../docs/JAILBREAK_POLICY.md) |
| **Prompt assembly** | [PROMPT_ASSEMBLY.md](../../../docs/PROMPT_ASSEMBLY.md) · [diagram](../../../images/assembled_prompt.svg) |
| **Production pin** | Still **base-1** in `CURRENT.json` / `v2/min` until you promote |

## Naming

```text
chat_request_analytics_base-4.json
chat_request_analytics_base-4.txt
chat_request_analytics_base-4_cus_travel-sample_default-1.json
```

## Regenerate text from JSON

```bash
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 4 --out v2/base/base-4 --no-set-base-id
```

## Related packs

| Pack | Role |
| --- | --- |
| `base-1` | Production pin (legacy `*_v2_min.json`) |
| `base-2-prototype` | Earlier design fork (history / Diff) |
| `base-3-prototype` | Text-export experiment |
| **`base-4`** | **Current new chat_request line** |
