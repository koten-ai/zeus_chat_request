# RELEASE_CHECKLIST — base-6.1 → base-6.2

**Train:** content skinny · **Jira:** CR-34 · **Breaking wire:** No

## Pack

- [x] `v2/base/base-6.2/` snapshot from base-6.1
- [x] CORE + assemble all 10 modes
- [x] `return` / `pipeline` schema diet
- [x] report_sink + settings companions copied (unchanged contracts)
- [x] `verify_base_pack.py --base 6.2` OK
- [x] `diff_modes.py --fail-if-clone` OK
- [x] text export + MANIFEST refresh
- [x] Prefix ≥20% vs base-6.1 analytics min (measured ~−25%)

## Docs

- [x] Hop README + lessons
- [x] ROADMAP § base-6.2 + board map CR-34
- [x] COMPAT candidate row
- [x] RELEASE_NOTES unreleased highlight
- [x] Pack OVERVIEW / README

## Residual (not blocking pack candidate)

- [ ] A/B or gold books 6.1 vs 6.2 (quality_pass / hops)
- [ ] Zeus vendor pin (optional follow-up ZE)
- [ ] CURRENT pin (CR-18 — still blocked Client/Zeus floors)
