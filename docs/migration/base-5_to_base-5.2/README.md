# Hop: base-5 → base-5.2 (engine adoption)

| | |
| --- | --- |
| **From** | base-5 wire freeze + base-5.1 mode overlays |
| **To** | **base-5.2** candidate (dual gaps: `wish_i_knew` + `data_gaps`) |
| **Kind** | Additive pack fields on frozen base-5 wire; **breaking engine pin** for Zeus 0.6 / Helios 0.6 |
| **Pack** | [`v2/base/base-5.2/`](../../../v2/base/base-5.2/) |
| **Dual-gap design** | [WISH_I_KNEW_DUAL.md](../../WISH_I_KNEW_DUAL.md) |
| **Lessons** | [lessons-learned.md](lessons-learned.md) — **required reading before Zeus pin / Detective / Helios** |

Production pin (`CURRENT.json`) may still be base-1 while engines **vendor** base-5.2 independently. Do not confuse pack candidate with `CURRENT` flip.

**Zeus lab:** **0.6.0–0.6.10** residual complete (Detective → report → Vault → Contract → Wizard → Hot Paths → COMPAT). **Helios lab:** **0.6.0** H6 cut (Layer A / dual gaps) — always WHERE **`t.ts` + `t.scope`** on Analytics (`idx_traces_ts_scope`).

## Docs

| Doc | Role |
| --- | --- |
| [lessons-learned.md](lessons-learned.md) | Full Zeus **0.6** train + Helios index law + next-migration checklist |
| [../base-4_to_base-5/GUIDE.md](../base-4_to_base-5/GUIDE.md) | Breaking wire (object triggers, app_output) still applies |
| [COMPAT.md](../../../COMPAT.md) | Triple matrix Zeus · BASE · Client |
| Helios sibling | `../Helios/docs/analytics/LAYER_A_REPORT.md` · `LAYER_A_QUERIES.sql` (H6) |
