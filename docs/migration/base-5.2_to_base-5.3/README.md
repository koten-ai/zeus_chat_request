# Migration hop: base-5.2 → base-5.3

| | |
| --- | --- |
| **From** | `base-5.2` |
| **To** | `base-5.3` |
| **Breaking wire?** | **No** — content train on base-5 wire |
| **Pack** | [`v2/base/base-5.3/`](../../../v2/base/base-5.3/) |
| **ROADMAP** | [§ base-5.3](../../ROADMAP.md) · CR-26 |

## Theme

1. World-model CORE blurb (DESIGN: AI-Ready overlay · mini-schema shape · access class)  
2. Verb catalog clarity vs Zeus `docs/API/V2` (WHEN/KEY; order `asc` + `field:`)  
3. Skinny habits (no rediscovery when inject present; evidence-only Layer A)  

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-5.2 --base 5.3   # already done for ship
# after diet:
python3 scripts/assemble_mode_prompts.py --base 5.3
python3 scripts/export_base_text.py --from v2/base/base-5.3/min --base 5.3 --out v2/base/base-5.3 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 5.3
python3 scripts/verify_base_pack.py --base 5.3
```

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate phases |
| [lessons-learned.md](lessons-learned.md) | Order direction bug + contract-safe tools[] |
| [OVERVIEW.md](../../../v2/base/base-5.3/OVERVIEW.md) | Pack delta |

## Pin

`CURRENT.json` may remain **base-1**. Zeus may still **vendor base-5.2** until a separate engine pin. This hop is **candidate pack on disk**.
