# base-6.1 overview

| | |
| --- | --- |
| **Parent** | `base-6` |
| **Wire** | base-5 freeze (objects / required four / `app_output`) — **no break** |
| **Theme** | Client emit **`user`** + **`ip_address`** + settings **`ai_process_result`** (cheap default) |
| **SoT** | [docs/ROADMAP.md § base-6.1](../../../docs/ROADMAP.md) · [MULTI_ROUND_CLIENT.md](../../../docs/MULTI_ROUND_CLIENT.md) · [PROMPT_SETTINGS.md](../../../docs/PROMPT_SETTINGS.md) |

## What changed vs base-6

1. **CORE** — short Client-loop note:
   - Default path after Zeus tools is **cheap** (UI/tables without a required second AI essay).
   - When Client sets **`ai_process_result: true`**, expect another turn with tool JSON already in the transcript; analyze from evidence only; do not re-run a successful pipeline.
   - Report sinks stamp root **`user`**: `zeus_client` | `zeus` | `helios` | `admin` (product Client always `zeus_client`) and optional **`ip_address`** (IPv4 or IPv6 string when known).
2. **Machine JSON for report sink (not Layer A):**
   - [`report_sink_schema.json`](report_sink_schema.json) · [`report_sink_example.json`](report_sink_example.json)
   - Settings companion: [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json)
3. Retains base-6 soft **`hints.*`** contract + base-5.3 world-model / verb clarity / dual gaps.

## What did **not** change

- **Layer A** (`response_output_schema.json` / `response_output_example.json`) — still model terminate only; **no** `user` / `ip_address` / `ai_process_result` (model must never invent stamps).
- Verb set (still 13 platform verbs in stamp).
- Production pin (`CURRENT` may remain base-1).
- Invented production `contract_hash`.

## Pack files (SoT)

| File | Audience |
| --- | --- |
| `response_output_*.json` | **Layer A** — model `return` |
| `report_sink_*.json` | **Client/engine sink** — Analytics/session root stamps |
| `settings_ai_process_result.example.json` | **Client settings** bag key (loop policy) |
| `min/` · `text/` | Assembled catalogs (CORE note included) |

## Implement residual (not this pack)

| ID | Owner |
| --- | --- |
| **ZC-WISH-035** | zeus_client stamps `user` + optional `ip_address` on sinks |
| **ZC-WISH-044** | zeus_client honors `ai_process_result` |
| **HEL-WISH-022** | Helios filters `user = "zeus_client"` |

## Verify

```bash
python3 scripts/verify_base_pack.py --base 6.1
```
