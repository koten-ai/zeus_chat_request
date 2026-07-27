# Migration hop: base-5.3 → base-6

| | |
| --- | --- |
| **From** | `base-5.3` |
| **To** | `base-6` |
| **Breaking wire?** | **No** — additive on base-5 wire |
| **Pack** | [`v2/base/base-6/`](../../../v2/base/base-6/) |
| **ROADMAP** | [§ base-6](../../ROADMAP.md) · [HINTS.md](../../HINTS.md) · **CR-4** |

## Theme

1. Soft **`hints.*`** inject contract (hash-excluded, after hard `rules{}`)  
2. Thin CORE note: path/recipe / field / multipart bias never replaces jailbreak or MINI-SCHEMA  
3. Keep base-5.3 world-model + verb clarity + dual gaps  

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-5.3 --base 6
# after CORE diet:
python3 scripts/assemble_mode_prompts.py --base 6
python3 scripts/export_base_text.py --from v2/base/base-6/min --base 6 --out v2/base/base-6 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 6
python3 scripts/verify_base_pack.py --base 6
```

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate phases |
| [lessons-learned.md](lessons-learned.md) | Hints vs rules; multi-intent ≠ open |
| [HINTS.md](../../HINTS.md) | Inject contract SoT |
| [OVERVIEW.md](../../../v2/base/base-6/OVERVIEW.md) | Pack delta |

## Pin / Client

- `CURRENT.json` may remain **base-1**.  
- Zeus may still **vendor base-5.3** until a separate engine pin.  
- Client runtime inject of `hints.*` is **ZC-WISH-040** residual (not required for candidate pack ship).
