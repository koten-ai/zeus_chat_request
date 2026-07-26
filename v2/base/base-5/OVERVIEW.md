# base-5 overview

Short pack changelog. Full plan: [docs/ROADMAP.md](../../../docs/ROADMAP.md). Release checklist: [docs/migration/base-4_to_base-5/RELEASE_CHECKLIST.md](../../../docs/migration/base-4_to_base-5/RELEASE_CHECKLIST.md).

| | |
| --- | --- |
| **BASE id** | `base-5` |
| **Parent** | base-4 |
| **Status** | Candidate pack (not pin) |
| **Production pin** | base-1 until promote |

## What changed (vs base-4)

**Wire / Layer A**

- `business_rules_triggers`: **object** `{ rule_id: bool }` (sparse; missing = false) — not `boolean[]`
- Optional **`app_output`** when Client sends `output_request.app.fields` (each field **type + description**)
- Terminate table prose: object triggers; soft-require `policy_action`; Client inject notes (company_context, rules{}, output_request)

**Unchanged**

- Required four: `summary`, `query_decomposition`, `decomposition`, `confidence`
- 13 verb names
- Envelope `_format: "zeus.chat_request.v2"`
- G1/G2/G3 audience split

**Client contracts (documented; implement in zeus_client)**

- Settings bag, rule pack merge/freeze, post-terminate policy table
- Dual-read of base-4 arrays: ≤1 Client release then remove

**Not in this pack body**

- Full company manifesto (inject only, word-capped)
- Soft hints / A/B (base-6 additive)
- Helios Pri-1 as required AI fields (Zeus/Client report emits)

## Regenerate

```bash
python3 scripts/export_base_text.py --from v2/base/base-5/min --base 5 --out v2/base/base-5 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 5
```
