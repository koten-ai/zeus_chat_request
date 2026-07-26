# base-4

Ship pack for chat_request catalogs. **Design docs** live under [`docs/`](../../../docs/) (not duplicated here).

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **JSON** | [`min/chat_request_<mode>_base-4.json`](min/) |
| **Text** | [`text/chat_request_<mode>_base-4.txt`](text/) |
| **Layer A schema** | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| **Manifest** | [`MANIFEST.json`](MANIFEST.json) |
| **Overview / diet notes** | [OVERVIEW.md](OVERVIEW.md) |
| **Requirements (docs)** | [BIBLE.md](../../../docs/BIBLE.md) — ownership §2 |
| **Control plane** | [PROMPT_SETTINGS.md](../../../docs/PROMPT_SETTINGS.md) · [ROADMAP.md](../../../docs/ROADMAP.md) |
| **base-1 → base-4 map** | [BASE_1_TO_BASE_4_GUIDE.md](../../../docs/base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md) |
| **Lessons** | [lessons-learned.md](../../../docs/base-1_to_base-4/lessons-learned.md) |
| **Multi-round** | [MULTI_ROUND_CLIENT.md](../../../docs/MULTI_ROUND_CLIENT.md) |
| **Inspector** | [INSPECTOR.md](../../../docs/INSPECTOR.md) |
| **Create next BASE** | [CREATE_BASE.md](../../../docs/CREATE_BASE.md) · `scripts/new_base.py` |
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
python3 scripts/new_base.py --refresh-manifest --base 4
python3 scripts/scan_catalogs.py
```

## Scaffold base-5 from this pack

```bash
python3 scripts/new_base.py --from v2/base/base-4 --base 5
```

## Related packs

| Pack | Role |
| --- | --- |
| `base-1` | Production pin (legacy `*_v2_min.json`) |
| `base-2-prototype` | Earlier design fork (history / Diff) |
| `base-3-prototype` | Text-export experiment |
| **`base-4`** | **Current new chat_request line** |
