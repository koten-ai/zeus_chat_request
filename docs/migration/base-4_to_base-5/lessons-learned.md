# Lessons: base-4 → base-5 (first pack diet)

**Audience:** agents/humans doing the next BASE or Client implementation.  
**Related:** [GUIDE.md](GUIDE.md) · [ROADMAP.md](../../ROADMAP.md) · [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

---

## 1. Break the wire once

Front-loading object triggers + `app_output` + inject contracts in **one** BASE avoids a second painful dual-read era. Do not plan multi-year array support.

## 2. Scaffold ≠ diet

`new_base.py` copies parent shapes. **Always** transform schema + `return`/`pipeline` props + Terminate prose after scaffold, or you ship base-4 arrays under a base-5 name.

## 3. System prompt table + tool schema must match

Updating only `response_output_schema.json` without tool parameters (or vice versa) creates Detective/Client drift. Bulk-edit both; re-export text after.

## 4. company_context is inject, not BASE prose

Do not paste multi-page brand into every mode’s system string. Point at Client inject and word caps.

## 5. Helios stay off required Layer A

Pri-1 fields belong on Zeus reports / Client session — not new required terminate keys. Keeps catalogs lean and Analytics honest.

## 6. Checklist before PR

Pack files alone are incomplete without RELEASE_NOTES breaking table, COMPAT row, migration GUIDE, and playbook jump update. Use **RELEASE_CHECKLIST.md**.
