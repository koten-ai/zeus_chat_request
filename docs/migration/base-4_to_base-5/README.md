# Hop: base-4 → base-5

| | |
| --- | --- |
| **From** | base-4 (candidate pack) |
| **To** | base-5 (**design only** — no pack yet) |
| **Kind** | **BREAKING** — last wire/control-plane break before prod on this line |
| **Pack** | _not scaffolded_ — use `scripts/new_base.py --from v2/base/base-4 --base 5` when ready |
| **Pin after hop?** | No until stamp + Client + Detective green |

## Status

base-5 is the **intentional big-bang break** (objects, settings, output_request, policy table) while **no one is production on base-4/5**.  
**base-6+ must stay additive/optional** ([ROADMAP.md](../../ROADMAP.md) BASE change law).

base-5 is specified in design docs, not as `v2/base/base-5/` catalogs yet.

| Topic | Read |
| --- | --- |
| Full base-5 plan | [../../ROADMAP.md](../../ROADMAP.md) § base-5 |
| Named rules + `output_request` | [../../RULES_OBJECT_AND_OUTPUT_REQUEST.md](../../RULES_OBJECT_AND_OUTPUT_REQUEST.md) |
| Settings / Client policy | [../../PROMPT_SETTINGS.md](../../PROMPT_SETTINGS.md) |
| Comply / upgrade steps | [../../BASE_AGENT_PLAYBOOK.md](../../BASE_AGENT_PLAYBOOK.md) |
| Versions | [../../../COMPAT.md](../../../COMPAT.md) |

## Release checklist (double-check before / while scaffolding)

**[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** — pack + docs + scripts + RELEASE_NOTES + COMPAT + Zeus/Client + base-5 content rules.

Template for other hops: [../RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md).

## When the pack exists

Also add:

- `GUIDE.md` — wire deltas vs base-4  
- `lessons-learned.md`  

Until pack exists, treat [ROADMAP.md](../../ROADMAP.md) as the delta source and work the RELEASE_CHECKLIST in design mode.
