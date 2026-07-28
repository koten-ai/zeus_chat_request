# base-6.2 overview

Short pack changelog only. Full requirements: [docs/BIBLE.md](../../../docs/BIBLE.md) · [ROADMAP § base-6.2](../../../docs/ROADMAP.md).

| | |
| --- | --- |
| **BASE id** | `base-6.2` |
| **Scaffolded from** | `v2/base/base-6.1` |
| **Breaking wire?** | **No** — content skinny |
| **Jira** | [CR-34](https://kotenai.atlassian.net/browse/CR-34) |
| **JSON** | `min/chat_request_<mode>_base-6.2.json` |
| **Status** | Candidate content train |

## What changed

- **CORE diet:** shorter world-model, efficiency, Terminate; Client `user`/`ip` enum out of model prompt; one-line `hints.*` + insight turn.
- **Tools diet:** thinner `return` property descriptions; `pipeline` terminating Layer A **thin-refs** return (no deep G2 item trees).
- **Measured (analytics min):** catalog prefix system+tools ~**6.4k → ~4.8k tokens (~−25%)**.
- **Unchanged:** 13 verbs · required four · dual gaps · progressive-empty one-liner · report_sink / `ai_process_result` contracts from base-6.1.

## Regenerate

```bash
python3 scripts/assemble_mode_prompts.py --base 6.2
python3 scripts/export_base_text.py --from v2/base/base-6.2/min --base 6.2 --out v2/base/base-6.2 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 6.2
python3 scripts/verify_base_pack.py --base 6.2
```
