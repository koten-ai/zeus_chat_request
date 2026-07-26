# Migration hops (`base-X` → `base-Y`)

**Last reviewed:** 2026-07-26  
**Purpose:** One folder per BASE upgrade. Living design stays in `docs/` root; ship packs stay in `v2/base/base-N/`.

## Naming (normative)

| Item | Pattern |
| --- | --- |
| Hop folder | `docs/migration/base-<FROM>_to_base-<TO>/` |
| Guide | `GUIDE.md` — what stayed / moved / added |
| Lessons | `lessons-learned.md` — recommended |
| Optional | `CHECKLIST.md` — short agent delta bullets |
| Optional | hop `README.md` — status + links |

**AI playbook** always links hops as:

```text
docs/migration/base-X_to_base-Y/
```

See [BASE_AGENT_PLAYBOOK.md](../BASE_AGENT_PLAYBOOK.md) · root [AGENTS.md](../../AGENTS.md).

## Index of hops

| Jump | Path | Status |
| --- | --- | --- |
| base-1 → base-4 | [base-1_to_base-4/](base-1_to_base-4/) | Candidate pack on disk (`v2/base/base-4/`); pin still base-1 |
| base-4 → base-5 | [base-4_to_base-5/](base-4_to_base-5/) | **Design only** — no base-5 pack yet; see ROADMAP |

## When you finish a new hop

1. Create `docs/migration/base-X_to_base-Y/` with `GUIDE.md` (+ lessons).  
2. Add a row to this index.  
3. Update [BASE_AGENT_PLAYBOOK.md](../BASE_AGENT_PLAYBOOK.md) jump table + comply cards.  
4. Update [COMPAT.md](../../COMPAT.md).  
5. Scaffold pack via [CREATE_BASE.md](../CREATE_BASE.md) when Y is real catalogs.

## Not here

| Content | Where |
| --- | --- |
| Current requirements | [BIBLE.md](../BIBLE.md) |
| Future plan | [ROADMAP.md](../ROADMAP.md) |
| Version triples | [COMPAT.md](../../COMPAT.md) |
| Pack JSON/text | `v2/base/base-N/` |
