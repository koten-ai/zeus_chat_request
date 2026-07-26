# Lessons: base-4 → base-5 (first pack diet)

**Audience:** agents/humans doing the next BASE or Client implementation.  
**Related:** [GUIDE.md](GUIDE.md) · [ROADMAP.md](../../ROADMAP.md) · [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) · [verify_base_pack.py](../../../scripts/verify_base_pack.py)

**Shipped:** pack + docs on `main` via PR #5 (`release/base-5`). Production pin still **base-1**.

---

## 1. Break the wire once

Front-loading object triggers + `app_output` + inject contracts in **one** BASE avoids a second painful dual-read era. Do not plan multi-year array support. base-6+ must stay additive/optional.

## 2. Scaffold ≠ diet (P0)

`new_base.py` copies parent shapes. **Always** transform schema + `return`/`pipeline` props + Terminate prose after scaffold, or you ship base-4 arrays under a base-5 name.

**Gate:** before any pack PR:

```bash
python3 scripts/verify_base_pack.py --base N
```

For N≥5 this fails on array triggers / missing `app_output` if the diet was skipped.

## 3. System prompt table + tool schema must match

Updating only `response_output_schema.json` without tool parameters (or vice versa) creates Detective/Client drift. Bulk-edit both; re-export text after.

## 4. company_context is inject, not BASE prose

Do not paste multi-page brand into every mode’s system string. Point at Client inject and word caps (soft 150 / hard 250).

## 5. Helios stay off required Layer A

Pri-1 fields belong on Zeus reports / Client session — not new required terminate keys. Keeps catalogs lean and Analytics honest.

## 6. Checklist before PR (process)

Pack files alone are incomplete without RELEASE_NOTES breaking table, COMPAT row, migration GUIDE, and playbook jump update. Use **RELEASE_CHECKLIST.md** phases A→G.

## 7. What went well (base-5 train)

| Practice | Why keep |
| --- | --- |
| Docs-first layout (`docs/` + `docs/migration/base-X_to_base-Y/`) | Agents find hops without hunting pack folders |
| Break-once law written into ROADMAP + COMPAT before diet | No “we’ll break again in base-6” drift |
| Thin pack README/OVERVIEW | Design stays in `docs/`; pack stays ship unit |
| Separate PRs: process docs (#4) then pack (#5) | Reviewable diffs; matrix/playbook stable before catalogs |

## 8. What to change next time (process P0)

| Issue | Fix |
| --- | --- |
| Easy to forget diet after scaffold | Run **`verify_base_pack.py`** before PR; treat fail as blocker |
| Checklist was a flat list | Use **phases A–G** in [RELEASE_CHECKLIST_TEMPLATE](../RELEASE_CHECKLIST_TEMPLATE.md) |
| External work mixed into pack ticket | Open **separate CR tasks** for zeus_client + Zeus after pack lands |
| Playbook banners lagged pack status | Update COMPAT + playbook “candidate pack” language **same PR as pack** |
| Text export can stale after min edit | Re-export + verify in one shell block before commit |

## 9. Recommended shell block (every BASE bump)

```bash
# after diet edits under v2/base/base-N/
python3 scripts/export_base_text.py --from v2/base/base-N/min --base N --out v2/base/base-N --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base N
python3 scripts/scan_catalogs.py
python3 scripts/verify_base_pack.py --base N   # must print OK
```

## 10. Residual after pack (not pack PR)

These stay open until green — do **not** flip `CURRENT.json`:

1. **zeus_client** — object rules/triggers, settings bag, output_request type+description, policy table, app_output validate, dual-read ≤1 release.  
2. **Zeus** — loaders `*_base-5.json`, return/Detective allow object triggers + optional app_output, lineage stamp path.  
3. **Pin** — only after stamp + Client + Detective (see CR pin epic / checklist §8).
