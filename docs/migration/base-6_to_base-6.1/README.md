# Migration hop: base-6 → base-6.1

| | |
| --- | --- |
| **From** | `base-6` |
| **To** | `base-6.1` |
| **Breaking wire?** | **No** — additive on base-5 wire |
| **Pack** | [`v2/base/base-6.1/`](../../../v2/base/base-6.1/) |
| **ROADMAP** | [§ base-6.1](../../ROADMAP.md) · [§ Emit `user` + `ai_process_result`](../../ROADMAP.md) |

## Theme

1. Root report field **`user`**: `zeus_client` | `zeus` | `helios` | `admin` (product Client stamps **`zeus_client`**)  
2. Client setting **`ai_process_result`** (bool, **default `false`**) — optional post-Zeus AI insight turn  
3. Thin CORE note so the model expects re-call only when Client enables insight  
4. Keep base-6 soft **`hints.*`** + base-5.3 world-model / verb clarity  

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-6 --base 6.1
# CORE diet (work/mode_overlays/CORE.md) then:
python3 scripts/assemble_mode_prompts.py --base 6.1
python3 scripts/export_base_text.py --from v2/base/base-6.1/min --base 6.1 --out v2/base/base-6.1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 6.1
python3 scripts/verify_base_pack.py --base 6.1
```

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate phases |
| [lessons-learned.md](lessons-learned.md) | Cheap default; Client stamps user; Helios filters |
| [OVERVIEW.md](../../../v2/base/base-6.1/OVERVIEW.md) | Pack delta |
| [PROMPT_SETTINGS.md](../../PROMPT_SETTINGS.md) | `ai_process_result` + ownership |
| [MULTI_ROUND_CLIENT.md](../../MULTI_ROUND_CLIENT.md) | Loop branch after tools |
| [ZEUS_CLIENT_WISHLIST…](../../ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) | **ZC-WISH-035**, **ZC-WISH-044** |
| [HELIOS_WISHLIST…](../../HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | **HEL-WISH-022** only (not Client wishlist bulk) |

## Pin / Client

- `CURRENT.json` may remain **base-1**.  
- Zeus may stay on current vendor pin until a separate engine bump.  
- Runtime stamp + loop are Client residual (**ZC-WISH-035 / 044**). Pack documents the contract; do not claim product insight-turn is live until Client lands.
