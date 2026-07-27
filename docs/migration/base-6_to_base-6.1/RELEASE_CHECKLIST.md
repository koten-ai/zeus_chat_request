# RELEASE_CHECKLIST — base-6 → base-6.1

| Field | Value |
| --- | --- |
| **From** | `base-6` |
| **To** | `base-6.1` |
| **Breaking?** | **no** (additive on base-5 wire) |
| **Owner** | catalog + docs train |
| **Date** | 2026-07-27 |

**Template:** [RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md)

## 0. Pre-flight (Phase A)

- [x] ROADMAP theme: `user` + `ai_process_result` (readable enums)  
- [x] Additive only (no Layer A rename)  
- [x] Helios bulk stays out of Client wishlist  

## 1. Pack on disk (Phases B–C)

- [x] `v2/base/base-6.1/` from `new_base.py --from v2/base/base-6 --base 6.1`  
- [x] `_lineage.base_id` = `base-6.1`, parent `base-6`  
- [x] CORE section 5 (Client loop + `user` stamp) via `assemble_mode_prompts.py --base 6.1`  
- [x] text re-export + MANIFEST refresh  
- [x] OVERVIEW.md + README.md  

## 2. Verify (Phase D)

- [x] `python3 scripts/verify_base_pack.py --base 6.1` **OK**  

## 3. Docs ship (Phase E)

- [x] Hop README + lessons-learned + this checklist  
- [x] ROADMAP § base-6.1  
- [x] COMPAT candidate row  
- [x] RELEASE_NOTES unreleased  
- [x] Client wishlist: strip HEL-WISH Pri-3 bulk; keep ZC-035/044  

## 4. External residual (Phase F — not this PR)

- [ ] zeus_client: ZC-WISH-035 / ZC-WISH-044  
- [ ] Helios Motions: HEL-WISH-022 filters  
- [ ] Zeus Hub Debug default for `ai_process_result` (optional product choice)  

## 5. Pin (Phase G)

- [ ] Do **not** flip `CURRENT.json` until stamp + Client + Detective green  
