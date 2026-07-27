# RELEASE_CHECKLIST — base-5.3 → base-6

| Field | Value |
| --- | --- |
| **From** | `base-5.3` |
| **To** | `base-6` |
| **Breaking?** | **no** (additive content on base-5 wire) |
| **Owner** | catalog train |
| **Date** | 2026-07-27 |

Template: [RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md)

## 0. Pre-flight (Phase A)

- [x] Read COMPAT — pin vs candidate  
- [x] Read ROADMAP base-6 theme (soft hints.*)  
- [x] Confirm **not breaking**  
- [x] Production pin still base-1 — do not flip  
- [x] CR-4 theme linked  

## 1. Pack on disk (Phases B–C)

- [x] New folder `v2/base/base-6/`  
- [x] Scaffolded from base-5.3  
- [x] `_lineage.base_id` = base-6; parent base-5.3  
- [x] CORE soft-hints blurb; dual gaps + verb clarity retained  
- [x] 10 min + 10 text catalogs  
- [x] MANIFEST + response_output_* + README + OVERVIEW  
- [x] No invented production contract_hash  
- [x] Layer A required four unchanged  

## 2. Scripts / regenerate (Phase D)

- [x] assemble_mode_prompts.py --base 6  
- [x] export_base_text.py  
- [x] refresh-manifest  
- [x] verify_base_pack.py --base 6 → OK  

## 3. Docs (Phase E)

- [x] migration hop README + lessons + this checklist  
- [x] migration/README.md index row  
- [x] docs/HINTS.md SoT  
- [x] ROADMAP / COMPAT / RELEASE_NOTES  
- [x] No BIBLE wire break (content only)  

## 4–5. Content correctness

- [x] Soft-hints CORE note in all 10 modes  
- [x] World-model + order asc + dual gaps still present  
- [x] No new required Layer A Helios tax  

## 6. External (Phase F — residual)

- [ ] Client injects `hints.*` after rules{} (ZC-WISH-040 / CR-13)  
- [ ] Zeus vendor pin base-6 (optional separate)  
- [ ] Hot Path → hints.hot_path product (ZE-267)  

## 7–8. Pin (Phase G)

- [ ] CURRENT flip — **not this PR**  
