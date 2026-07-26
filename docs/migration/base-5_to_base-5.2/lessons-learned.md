# Lessons: base-5 → base-5.2 + Zeus 0.6 / Helios 0.6 pin

**Audience:** agents/humans pinning Zeus (or Client) onto **base-5.2**; next BASE authors; Helios 0.6 Analytics.  
**Captured:** 2026-07-26 after Zeus **0.6.0 → 0.6.10** Beelink lab (Detective → chat → report → Vault → Contract → Wizard → Hot Paths → docs).  
**Related:** [README.md](README.md) · [WISH_I_KNEW_DUAL.md](../../WISH_I_KNEW_DUAL.md) · [base-4→5 lessons](../base-4_to_base-5/lessons-learned.md) · [COMPAT.md](../../../COMPAT.md)

This is **experience**, not a second BIBLE. Prefer pack schema + BIBLE for wire; use this to avoid re-breaking engines and Analytics.

---

## 0. Scope of this hop (what changed vs what broke)

| Layer | base-5 | base-5.1 | base-5.2 |
| --- | --- | --- | --- |
| Wire freeze | object `business_rules_triggers`, `app_output`, inject contracts | same | same |
| Content | diet + terminate table | **mode overlays** | **dual gaps** (`data_gaps` additive) + wish items |
| Zeus pin (this train) | candidate | candidate | **vendored on Zeus 0.6** (breaking vs 0.5 / base-1) |

**Policy that worked:** Zeus **0.6.x is not dual-compatible** with 0.5.x / base-1 Layer A shapes. Helios jumps **0.2.x → 0.6.x** in lockstep. Sparse optional fields still OK (missing ≠ error); **wrong shapes when present** are fail.

**Zeus ship record (lab):** `0.6.0` pin+Detective → `0.6.10` COMPAT/openapi. Residual surfaces landed in **order** (see §13); do not reshuffle for the next hop.

---

## 1. Three pins are not one pin

| Pin | Owner | Mistake |
| --- | --- | --- |
| `CURRENT.json` / `v2/min` | chat_request repo | Thinking Zeus pin requires CURRENT flip first |
| Zeus `PIN.json` + `pinned/min` | Zeus embed | Leaving stale `*_v2_min.json` beside `*_base-5.2.json` — loader preferred legacy names |
| Helios `VERSION` | Helios product | Keeping 0.2.x Analytics assumptions after Zeus emits base-5.2 fields |

**Lesson:** Document all three. Zeus can ship a **vendor pin** of base-5.2 while CURRENT remains base-1 for external consumers. Helios must not silently dual-read string `wish_i_knew` / array triggers.

---

## 2. Filename / mode parse is still the silent killer

Re-confirmed from base-1→4 lessons, worse with **dotted** ids:

| File | Bad mode parse | Good |
| --- | --- | --- |
| `chat_request_analytics_base-5.2.json` | `analytics_base-5.2` | `analytics` |
| `chat_request_analytics_v2_min.json` | `analytics` | (legacy only) |

**Engine checklist (same PR as first vendor):**

1. `modeFromFilename` strips `_base-<id>` **before** `_v2_min` (id may be `5.2`).  
2. `LoadMode` **prefers** pin `*_base-<PIN>.json` over leftover `*_v2_min.json`.  
3. After vendor, **delete** old min files from embed path or you will think you pinned 5.2 while serving base-1 bodies.  
4. `make chat-request-check` / structure scripts must **glob `*_base-*.json`**, not only `*_v2_min.json`.  
5. Unit test: `LoadMode("analytics")` against a MapFS that only has `*_base-5.2.json`.

---

## 3. Layer A required four vs synthetic terminate

Packs and Detective require:

```text
summary · query_decomposition · decomposition · confidence
```

**What first lab chat did:**

1. Tools ran (find → empty equality on FTS field; search FTS OK; get missing node ids).  
2. Model **finished without calling `return`**.  
3. Zeus stamped `return` with `status=synthetic` and **only**  
   `query_decomposition: {intent, entity, synthetic:true}`.  
4. Detective correctly **failed** Layer A (missing summary / decomposition / confidence).

**Lessons:**

| Do | Don't |
| --- | --- |
| Synthetic terminate fills **full required four** + `synthetic:true` (and optional `policy_action=error`) | Only inject QD “for Helios” |
| Use assistant prose as `summary` when present; honest placeholder if empty | Leave summary empty and expect checklist pass |
| Helios / Analytics: `WHERE t.report.synthetic IS MISSING` (or QD.synthetic) | Treat synthetic QD as real demand |
| Detective: note “terminate is synthetic” in diagnosis | Pretend `has_terminate=true` means model obeyed Layer A |
| Report root promotes `synthetic` + `layer_a_via` | Only bury synthetic on nested tool status |

**Open product risk:** force-`return` round (tools-only instruction) is still weaker than a real model terminate. Synthetic bag is a **safety net for observability**, not a substitute for teaching the model to call `return`.

---

## 4. Checklist / structure gates vs base-5.2 wording

| Gate | Old assumption | base-5.2 reality |
| --- | --- | --- |
| Evidence-loop string | System must contain `"Evidence loop"` | Min packs use **evidence rules** / terminate field tables |
| Structure `EVIDENCE_MARKERS` | Heading-oriented | Accept `evidence` + `query_decomposition` |
| Output diagnosis | Missing confidence = note only | Align with required four: decomp + confidence are **missing**, not soft notes only |

**Lesson:** When pack diet renames prose, **update Zeus Detective + check_structure in the same train** — or every green pin chat fails “INPUT NOT OK” for cosmetic wording.

---

## 5. Shape changes engines must not half-implement

From base-5 wire + base-5.2 dual gaps:

| Field | Wrong (0.5 / base-1 era) | Right (base-5.2) |
| --- | --- | --- |
| `wish_i_knew` | `string` | **array of objects** `{what, kind, why?, severity?}` max 3 |
| `business_rules_triggers` | `boolean[]` parallel to rules list | **object** `{ rule_id: bool }` sparse |
| `data_gaps` | absent | optional array (G2/Helios acquisition) |
| `app_output` | informal / dropped | optional object when Client sent `output_request` |
| `policy_action` | informal | enum; soft-require on Client |

**Half-implement traps:**

- Tool handler only copies `wish_i_knew` if `string` → **drops** array emits.  
- Pipeline struct tags `WishIKnew string` → JSON decode fails silently / empties.  
- Detective `String(args.wish_i_knew)` on array → useless UI.  
- Report rollup `WishIKnew []string` only — fine as **flattened** display, but keep **items** (or raw) for Helios if you query structure.  
- `if len(triggers) > 0` only → **drops explicit `{}`** (“no rules fired” vs “not emitted”).

**Lesson:** Passthrough Layer A as `any` / map first; strict validate later. Prefer **pass-through** on day-one pin; fail closed on **known wrong shapes** (string wish / array triggers) in Detective. On report root, emit **presence flags** (`business_rules_triggers_present`, `data_gaps_present`) when JSON `omitempty` would hide empty bags.

---

## 6. G1 / G2 / G3 still confuse first-debug (and chat UI)

| Audience | Fields | UI |
| --- | --- | --- |
| G1 user | `summary` only | Chat bubble |
| G2 admin | wish, data_gaps, scores | Detective only |
| G3 client | policy_action, triggers, app_output | Client control plane |
| G2 **light** (ops) | confidence, policy, intent·entity chips | Optional under bubble (ZE-260) — **not** full G2 dump |

**Lesson:** Detective must **render** full G2/G3; chat must **not** dump wish/triggers/scores into user bubbles. Zeus 0.6 order that worked:

1. **Detective + pin** (ZE-259) — see the bag  
2. **Chat G1 + light chips** (ZE-260) — summary fills empty bubble; chips only  
3. **Report rollup** (ZE-265) — Helios root fields  
4. Then Prompt Vault / Contract / Wizard / Hot Paths / docs

Do **not** start with Vault or Ingress polish before Detective can show a real `return`.

---

## 7. Lab data lies look like catalog bugs

First fruit-beer chat SCOPE BRIEF:

```text
nodes_total: 0 · entities_total: 0 · edges_total: 250
```

FTS returned doc keys; `get` returned **all missing_node_ids**. Detective graded Layer A fail on synthetic return — correct — but operators may blame base-5.2 catalogs.

**Lesson:** Before blaming pin/catalog:

1. Confirm inject **scope match** + mini entity types.  
2. Confirm **nodes/entities non-zero** for that scope (Enable / EntityMap / ingest).  
3. Equality `where` on `text_fts` fields is a **model** miss; FTS recovery is expected.

Catalog pin green ≠ graph healthy.

---

## 8. Hub freezes and “hung chat” are often client-side

0.6.2 lab: Debug chat “Live streaming…” forever was **browser graph seed density** (hundreds of labeled nodes), not a stuck LLM.

| Symptom | Real cause | Fix pattern |
| --- | --- | --- |
| Tab freezes after answer | Force-graph labels + unbounded seeds | Cap seeds, hide labels above N nodes, bound deep-walk |
| Spinner forever | Nested backticks broke `app.js` parse (ZE-80) | `make check-admin-js` before ship |
| Stream never ends | No AbortController | 3 min timeout on Debug fetch |

**Lesson:** After pin, **soak Debug chat + graph** once. Ship freeze fixes in the same train as pin if lab is unusable.

---

## 9. Report rollup is the Helios contract (do it early)

Analytics must **not** UNNEST `detail.ai.calls[].args` for every chart. Zeus **0.6.5 / ZE-265** promotes terminate bag onto `session.traces.report` root:

| Report root | Source |
| --- | --- |
| `query_decomposition`, `decomposition`, `intent` | terminate args / AI |
| `confidence`, `policy_action` | terminate |
| `wish_i_knew` (flat strings), `wish_i_knew_items` (objects) | wish array / legacy string |
| `business_rules_triggers` + `business_rules_triggers_present` | object (incl. empty `{}`) |
| `data_gaps` + `data_gaps_present` | array (incl. empty) |
| `app_output`, `subject_confidence`, `jail_break_attempt` | when emitted |
| `synthetic`, `layer_a_via` | bag + tool status |

**Terminate tool names to scan (last wins):** `return` · `return_result` · `pipeline` (with summary/QD/turn_complete) · `classic.return`.

**Unit test requirement for next pin:** `TestBuildReportLayerAG2FromReturn` style — marshal report JSON and assert Helios keys exist at **root**, not only under `detail`.

**Lesson:** Open **ZE report rollup + HEL epic the same day** as pin. Hub UI can lag a few patches; Helios blocked on missing report fields cannot.

---

## 10. Helios is a second product, not a SQL footnote

| Mistake | Fix |
| --- | --- |
| “Helios will tolerate anything sparse” | Sparse ≠ wrong type forever |
| No HEL tickets until Zeus ships | Open **HEL epic 0.6** with Zeus epic same day |
| Query only `report.query_decomposition` | Plan `data_gaps`, structured wish, object triggers, `synthetic` on report root |
| Same Helios VERSION as 0.2 motions train | Jump **0.6** with Zeus to signal break |
| Unbounded Analytics scans | **Always** filter `t.ts` + `t.scope` (see §11) |

---

## 11. Helios Analytics — always WHERE `ts` and `scope` (index law)

Lab index (Analytics secondary, **not** GSI):

```sql
CREATE ANALYTICS INDEX idx_traces_ts_scope
ON `zeus_sessions`.`session`.`traces` (
  ts: STRING,
  scope: STRING
)
EXCLUDE UNKNOWN KEY;
```

Helios Motions top-bar is **Time + Scope**. The index key order is **`ts` first, `scope` second**. Analytics only uses a secondary index when predicates form a **prefix** of that key with equality/range ops.

### Non-negotiable predicates on every board / pack / probe query

```sql
FROM `zeus_sessions`.`session`.`traces` AS t
WHERE 1 = 1
  {{TIME_FILTER}}     -- AND t.ts >= DATE_ADD_STR(NOW_STR(), -N, "day"|"hour")
                      -- or absolute: AND t.ts >= "ISO" AND t.ts <= "ISO"
  {{SCOPE_FILTER}}    -- empty when All scopes; else AND t.scope = "bucket/_default"
  AND t.scope IS NOT MISSING   -- product scopes only (drop orphan rows)
  -- then feature filters (report.*, synthetic, …)
```

| Rule | Why |
| --- | --- |
| **Always** `t.ts` range (or absolute bounds) | Index **prefix**; without it full scan |
| **Always** touch `t.scope` | Equality when Scope set; `IS NOT MISSING` when All (hygiene + second key ready) |
| Never wrap `t.ts` in a function in **WHERE** | `DATE_TRUNC_STR(t.ts, …)` belongs in GROUP BY, not the window predicate |
| Never query `scope = …` alone | Wrong prefix — index unused |
| Prefer BFF `exploreTimeScopeFilters` | One helper; every motion reuses it |

### Placeholder contract (SQL packs + Go)

| Placeholder | Expands to |
| --- | --- |
| `{{TIME_FILTER}}` | `AND t.ts >= DATE_ADD_STR(NOW_STR(), -N, "unit")` (or absolute range) |
| `{{SCOPE_FILTER}}` | `AND t.scope = "…"` or empty |

**Smoke / STARTER queries** must include the same predicates — not only live Motions SQL. Lab “COUNT(*) with no WHERE” is fine for connectivity once; **do not** copy it into boards, probes, or HEL-20 packs.

### Helios Layer A filters (on top of ts/scope)

```sql
AND (t.report.synthetic IS MISSING OR t.report.synthetic = false)
-- dual gaps / structured Layer A (Zeus ≥ 0.6.5 report root):
-- t.report.data_gaps, t.report.data_gaps_present
-- t.report.wish_i_knew_items, t.report.wish_i_knew
-- t.report.business_rules_triggers, t.report.business_rules_triggers_present
-- t.report.policy_action, t.report.confidence
```

**Docs:** Helios `docs/analytics/INDEXES.md` · `SCHEMA_AND_SPARSE_DATA.md` · H6 schema (HEL-19).

---

## 12. Residual surfaces after report (what actually shipped)

After ZE-265 report root, the rest of ZE-258 residual was **not** optional fluff — but none of it unblocks Helios SQL the way report does. Actual Zeus train:

| Ver | Ticket | Surface | Lesson for next hop |
| --- | --- | --- | --- |
| 0.6.0–0.6.3 | ZE-259 | Pin + Detective + synthetic bag + evidence wording | Pin day 1 |
| 0.6.4 | ZE-260 | Chat G1 summary + G2 light chips | No full G2 in bubble |
| 0.6.5 | ZE-265 | Report root Layer A G2 | **Helios contract** |
| 0.6.6 | ZE-261 | Prompt Vault BASE lineage | Catalog UX after report |
| 0.6.7 | ZE-262 | Contract Verify pin + hash_policy | Empty verify = pin catalog |
| 0.6.8 | ZE-263 | Wizard dry-run pin + Layer A teach | Ingress polish late |
| 0.6.9 | ZE-266 | Hot Paths / Path Finder Layer A | Skip synthetic; hash-excluded paths |
| 0.6.10 | ZE-264 | COMPAT + openapi pin notes | Cut docs last |

**Anti-pattern reconfirmed:** Vault / Wizard / Hot Paths before report root → Helios still blocked.

**Hub JS:** Nested backticks inside template literals still break `:9091/hub` (ZE-80). After any `app.js` change: `make check-admin-js`.

**Catalog vs Contract:** Contract Verify must use pin catalog / `CatalogForContract` (or equivalent), not a generator that diverges from Detective.

**Deploy:** Compose image pin (`zeus:X.Y.Z`) must match tar; only push branch **`5TH`** (ticket branches stay local).

---

## 13. Recommended Zeus pin shell block

```bash
# From Zeus repo; sibling clone of this repo recommended
export ZEUS_CHAT_REQUEST_ROOT=../zeus_chat_request

# 1) Flip PIN
# ai/chat_request/PIN.json + internal/chatrequest/pin.json → base_id base-5.2

# 2) Vendor (overwrite embed path)
make chat-request-vendor ZEUS_CHAT_REQUEST_ROOT=$ZEUS_CHAT_REQUEST_ROOT

# 3) Remove leftover legacy names under pinned/min if still present
# rm -f ai/chat_request/pinned/min/*_v2_min.json

# 4) Structure gate + unit tests
make chat-request-check
go test ./internal/chatrequest/ ./internal/admin/ ./internal/tracebundle/ -count=1

# 5) Rebuild / deploy lab; open Detective after one terminate chat
# Expect: chat_request_base_id=base-5.2 on /admin/api/status
```

### Lab deploy gotchas (Beelink / Dockhand)

| Gotcha | Fix |
| --- | --- |
| Image load OK but assert fails | Local `docker-compose.frontend.yml` must pin `zeus:X.Y.Z` before deploy script |
| Tar served from Mac | `python3 -m http.server 8765` in `__dev_only/env`; Dockhand pulls Mac IP not localhost |
| Only push `5TH` | Ticket branches stay local (`Agents.md`); never open PR ticket → main |
| Double `base-` in filenames | Vendor/export scripts; mode parse strips one `_base-<id>` only |

---

## 14. Detective soak definition of done (first pin)

Do **not** mark engine pin green until:

1. `/admin/api/status` → `chat_request_base_id: base-5.2`  
2. Real model **`return`** (not only synthetic) on a healthy scope  
3. Checklist: Layer A required four **pass** (or fail for real missing fields, not wording noise)  
4. Structured wish / object triggers / data_gaps render when model emits them  
5. **Report rollup** carries G2 fields at root for Helios (unit + one lab trace)  
6. One known-bad chat (synthetic or empty graph) still **explains** itself in diagnosis  
7. Chat bubble shows **summary** when content empty; chips optional; no full G2 dump  

Helios 0.6 green is separate: SQL packs + BFF parsers on report root with **ts/scope** predicates (HEL-17…HEL-23).

---

## 15. Ordered Zeus residual (ZE-258) — do not reshuffle casually

| Order | Surface | Ticket (this train) | Why |
| --- | --- | --- | --- |
| 1 | Detective + pin | ZE-259 | Fast feedback on real terminate |
| 2 | Chat Layer A (G1 + light chips) | ZE-260 | Operator-visible without Helios |
| 3 | **Report rollup** | ZE-265 | Unblocks Helios SQL/BFF |
| 4 | Prompt Vault / Vault+ | ZE-261 | Catalog UX; not on critical Helios path |
| 5 | Contract hash + Verify | ZE-262 | Stamp authority vs new `_hash_policy` |
| 6 | Wizard + Ingress | ZE-263 | Optimize paths / app_output |
| 7 | Hot Paths / Path Finder | ZE-266 | Layer A on workbench paths |
| 8 | Docs COMPAT / openapi | ZE-264 | End of train cut |

**Anti-pattern:** polish Prompt Vault or Wizard before report root fields exist — Helios sits idle while Hub chrome moves.

---

## 16. Jira pairing (what worked)

| Project | Epic (example) | First stories |
| --- | --- | --- |
| ZE | 0.6 base-5.2 adoption (ZE-258) | Detective + pin → chat chips → **report rollup** → residual Hub → docs |
| HEL | 0.6 Layer A / dual gaps (HEL-17) | ROADMAP → schema → SQL on report root (**ts+scope**) → BFF → boards → cut 0.6.0 |

Open Helios tickets when Zeus residual is named — not after SQL breaks in production charts. Helios **does not** dual-compat 0.2.x field assumptions with 0.6 report shapes.

---

## 17. One-line takeaways

| Topic | Takeaway |
| --- | --- |
| Pins | CURRENT ≠ Zeus PIN ≠ Helios VERSION |
| Files | Strip `_base-5.2`; never leave v2_min beside pin |
| Synthetic | Full required four + synthetic flags on bag **and** report |
| Wording | “evidence rules” counts as evidence guidance |
| Shapes | Object triggers + wish **array**; no half string handlers |
| Empty bags | Presence flags when `omitempty` would hide `{}` / `[]` |
| Lab | Empty graph ≠ bad catalog; freezes often graph UI |
| Helios | Same minor jump; **report root** is the contract |
| **Analytics** | **Every query: WHERE `t.ts` + `t.scope` for `idx_traces_ts_scope`** |
| UI order | Detective → chat G1 → report → Vault/Contract/Wizard/Hot Paths → docs |
| Done (Zeus) | Real return + report JSON keys + residual Hub + COMPAT + green CI |
| Done (Helios) | Packs/BFF on Layer A root fields; no dual-read; index-safe SQL |

---

## 18. Pointers

| Doc | Use |
| --- | --- |
| [WISH_I_KNEW_DUAL.md](../../WISH_I_KNEW_DUAL.md) | wish vs data_gaps |
| [base-4_to_base-5/GUIDE.md](../base-4_to_base-5/GUIDE.md) | Breaking wire still in force |
| [base-4_to_base-5/lessons-learned.md](../base-4_to_base-5/lessons-learned.md) | Pack diet + residual #10.1 |
| [COMPAT.md](../../../COMPAT.md) | Supported triples |
| Pack | `v2/base/base-5.2/response_output_schema.json` + `min/` |
| Zeus | `internal/tracebundle/report.go` (`BuildReport` / Layer A extract) |
| Zeus | `web/static/admin/app.js` (`extractLayerATerminate` / chips) |
| Zeus | `docs/ops/COMPAT.md` — 0.6.x surface table |
| Helios | `docs/analytics/INDEXES.md` — `idx_traces_ts_scope` |
| Helios | H6 tickets HEL-17…HEL-23 · Zeus pair ZE-258 / ZE-265 |

---

## 19. For the *next* migration (base-5.2 → N)

Carry these forward as default law:

1. **Three pins** named in the migration README before any code.  
2. **Filename / mode strip** unit-tested on day 0 of the engine pin.  
3. **Synthetic terminate** fills full required Layer A + flags report root.  
4. **Report rollup ticket** opened same day as pin; Helios epic same day.  
5. **UI residual order** fixed: Detective → chat G1 → report → everything else.  
6. **Helios SQL:** never ship a board or pack query without `t.ts` + `t.scope` predicates.  
7. **No dual-read** of obsolete shapes once the engine minor jumps.  
8. **Hub JS syntax gate** after every admin UI change.  
9. **Only integration branch** pushed remote (Zeus: `5TH`).  
10. Update **this** lessons file before starting Helios / Client residual on the next hop.

---

*Update this file when CURRENT flips to base-5.2, Client ships object floor, Helios 0.6 SQL lands, or the next BASE hop starts.*
