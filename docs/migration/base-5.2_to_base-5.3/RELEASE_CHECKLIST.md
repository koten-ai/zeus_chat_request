# RELEASE_CHECKLIST — base-5.2 → base-5.3

| Field | Value |
| --- | --- |
| **From** | `base-5.2` |
| **To** | `base-5.3` |
| **Breaking?** | **no** (content on base-5 wire) |
| **Owner** | catalog train |
| **Date** | 2026-07-26 |

Template: [RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md)

## 0. Pre-flight (Phase A)

- [x] Read COMPAT — pin vs candidate  
- [x] Read ROADMAP base-5.3 theme (skinny + world-model + verb clarity)  
- [x] Confirm **not breaking**  
- [x] Production pin still base-1 — do not flip  
- [x] CR-26 theme linked in ROADMAP  

## 1. Pack on disk (Phases B–C)

- [x] New folder `v2/base/base-5.3/`  
- [x] Scaffolded from base-5.2  
- [x] `_lineage.base_id` = base-5.3; parent base-5.2  
- [x] Dieted: CORE world-model + verb clarity P0–P2  
- [x] 10 min + 10 text catalogs  
- [x] MANIFEST + response_output_* + README + OVERVIEW  
- [x] No invented production contract_hash  
- [x] Layer A required four unchanged  

## 2. Scripts / regenerate (Phase D)

- [x] assemble_mode_prompts.py --base 5.3  
- [x] export_base_text.py  
- [x] refresh-manifest  
- [x] verify_base_pack.py --base 5.3 → OK  
- [ ] scan_catalogs.py (optional in PR if catalog-index regenerated)  

## 3. Docs (Phase E)

- [x] migration hop README + lessons + this checklist  
- [x] migration/README.md index row  
- [x] ROADMAP success signals (pack-owned)  
- [x] RELEASE_NOTES  
- [x] COMPAT candidate row  
- [ ] BASE_AGENT_PLAYBOOK jump row (if present — add if quick)  
- [x] No BIBLE wire break (content only)  

## 4–5. Content correctness

- [x] World-model blurb in all 10 system prompts  
- [x] order: `field:` + `asc` (no order `direction: desc`)  
- [x] find/search KEY constraints  
- [x] describe/get/traverse/pipeline improved  
- [x] Dual gaps retained  
- [x] No new required Layer A Helios tax  

## 6. External (Phase F — residual)

- [ ] Zeus pin/vendors base-5.3 (separate)  
- [ ] zeus_client load base-5.3 filenames (separate)  
- [ ] Hot Path empirics / A/B skinny stamps (separate)  

## 7–8. Pin (Phase G)

- [ ] CURRENT flip — **not this PR**  
