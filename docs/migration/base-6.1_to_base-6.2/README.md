# Migration hop: base-6.1 → base-6.2

| | |
| --- | --- |
| **From** | `base-6.1` |
| **To** | `base-6.2` |
| **Breaking wire?** | **No** — content skinny on base-5 wire |
| **Pack** | [`v2/base/base-6.2/`](../../../v2/base/base-6.2/) |
| **Jira** | [CR-34](https://kotenai.atlassian.net/browse/CR-34) |
| **ROADMAP** | [§ base-6.2](../../ROADMAP.md) |

## Theme

End-of-base-6.x **catalog prefix diet**:

1. Compress CORE (world-model, efficiency, Terminate); Client stamp enum out of model prompt  
2. Thin `return` property essays; **single-source** terminating Layer A on `pipeline` (no deep G2 trees)  
3. Keep **all 13 verbs**, required four, dual gaps, progressive-empty one-liner  
4. Target: ≥20% smaller system+tools prefix vs base-6.1 analytics min (**measured ~−25%**)

## Commands

```bash
python3 scripts/new_base.py --from v2/base/base-6.1 --base 6.2
# edit work/mode_overlays/CORE.md + diet verbs in pack min/
python3 scripts/assemble_mode_prompts.py --base 6.2
python3 scripts/export_base_text.py --from v2/base/base-6.2/min --base 6.2 --out v2/base/base-6.2 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 6.2
python3 scripts/verify_base_pack.py --base 6.2
python3 scripts/diff_modes.py --base 6.2 --fail-if-clone
```

## Docs

| Doc | Role |
| --- | --- |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Ship gate phases |
| [lessons-learned.md](lessons-learned.md) | What we cut / kept |
| [OVERVIEW.md](../../../v2/base/base-6.2/OVERVIEW.md) | Pack delta |
| [PROMPT_RULE_PLACEMENT.md](../../PROMPT_RULE_PLACEMENT.md) | Where laws live while dieting |

## Pin / Client

- `CURRENT.json` may remain **base-1**.  
- Zeus vendor may stay on base-5.3 until a separate pin decision.  
- No Client API change required for this content train.
