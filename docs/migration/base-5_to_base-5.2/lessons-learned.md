# Lessons: base-5 → base-5.2 + first Zeus 0.6 / Helios 0.6 pin

**Audience:** agents/humans pinning Zeus (or Client) onto **base-5.2**; next BASE authors.  
**Captured:** 2026-07-26 after Zeus **0.6.0 → 0.6.1** Beelink lab + Detective first chat (`req` sample: fruit beers / beer-sample).  
**Related:** [README.md](README.md) · [WISH_I_KNEW_DUAL.md](../../WISH_I_KNEW_DUAL.md) · [base-4→5 lessons](../base-4_to_base-5/lessons-learned.md) · [COMPAT.md](../../../COMPAT.md)

This is **experience**, not a second BIBLE. Prefer pack schema + BIBLE for wire; use this to avoid re-breaking engines.

---

## 0. Scope of this hop (what changed vs what broke)

| Layer | base-5 | base-5.1 | base-5.2 |
| --- | --- | --- | --- |
| Wire freeze | object `business_rules_triggers`, `app_output`, inject contracts | same | same |
| Content | diet + terminate table | **mode overlays** | **dual gaps** (`data_gaps` additive) + wish items |
| Zeus pin (this train) | candidate | candidate | **vendored on Zeus 0.6** (breaking vs 0.5 / base-1) |

**Policy that worked:** Zeus **0.6.x is not dual-compatible** with 0.5.x / base-1 Layer A shapes. Helios jumps **0.2.x → 0.6.x** in lockstep. Sparse optional fields still OK (missing ≠ error); **wrong shapes when present** are fail.

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
| Helios / Analytics: `WHERE query_decomposition.synthetic IS MISSING` | Treat synthetic QD as real demand |
| Detective: note “terminate is synthetic” in diagnosis | Pretend `has_terminate=true` means model obeyed Layer A |

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

**Lesson:** Passthrough Layer A as `any` / map first; strict validate later. Prefer **pass-through** on day-one pin; fail closed on **known wrong shapes** (string wish / array triggers) in Detective.

---

## 6. G1 / G2 / G3 still confuse first-debug

| Audience | Fields | UI |
| --- | --- | --- |
| G1 user | `summary` only | Chat bubble |
| G2 admin | wish, data_gaps, scores | Detective only |
| G3 client | policy_action, triggers, app_output | Client control plane |

**Lesson:** Detective must **render** G2/G3; chat must **not** dump them into user bubbles. First 0.6 work correctly prioritized Detective over Workbench chat polish.

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

## 8. Helios is a second product, not a SQL footnote

| Mistake | Fix |
| --- | --- |
| “Helios will tolerate anything sparse” | Sparse ≠ wrong type forever |
| No HEL tickets until Zeus ships | Open **HEL epic 0.6** with Zeus epic same day |
| Query only `report.query_decomposition` | Plan `data_gaps`, structured wish, object triggers on report root |
| Same Helios VERSION as 0.2 motions train | Jump **0.6** with Zeus to signal break |

Zeus should promote Layer A G2 fields onto **report** (cheap code path) so Analytics does not UNNEST tool args every chart.

---

## 9. Recommended Zeus pin shell block

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
go test ./internal/chatrequest/ ./internal/admin/ -count=1

# 5) Rebuild / deploy lab; open Detective after one terminate chat
# Expect: chat_request_base_id=base-5.2 on /admin/api/status
```

---

## 10. Detective soak definition of done (first pin)

Do **not** mark engine pin green until:

1. `/admin/api/status` → `chat_request_base_id: base-5.2`  
2. Real model **`return`** (not only synthetic) on a healthy scope  
3. Checklist: Layer A required four **pass** (or fail for real missing fields, not wording noise)  
4. Structured wish / object triggers / data_gaps render when model emits them  
5. Report rollup carries G2 fields for Helios  
6. One known-bad chat (synthetic or empty graph) still **explains** itself in diagnosis

---

## 11. Jira pairing (what worked)

| Project | Epic (example) | First story |
| --- | --- | --- |
| ZE | 0.6 base-5.2 adoption | Detective + pin |
| HEL | 0.6 Layer A / dual gaps | ROADMAP train docs, then SQL |

Open Helios tickets when Zeus residual is named — not after SQL breaks in production charts.

---

## 12. One-line takeaways

| Topic | Takeaway |
| --- | --- |
| Pins | CURRENT ≠ Zeus PIN ≠ Helios VERSION |
| Files | Strip `_base-5.2`; never leave v2_min beside pin |
| Synthetic | Full required four + synthetic flags |
| Wording | “evidence rules” counts as evidence guidance |
| Shapes | Object triggers + wish **array**; no half string handlers |
| Lab | Empty graph ≠ bad catalog |
| Helios | Same minor jump; report fields cheap on Zeus |
| Done | Real return on healthy scope, not only green CI |

---

## 13. Pointers

| Doc | Use |
| --- | --- |
| [WISH_I_KNEW_DUAL.md](../../WISH_I_KNEW_DUAL.md) | wish vs data_gaps |
| [base-4_to_base-5/GUIDE.md](../base-4_to_base-5/GUIDE.md) | Breaking wire still in force |
| [base-4_to_base-5/lessons-learned.md](../base-4_to_base-5/lessons-learned.md) | Pack diet + residual #10.1 |
| [COMPAT.md](../../../COMPAT.md) | Supported triples |
| Pack | `v2/base/base-5.2/response_output_schema.json` + `min/` |

---

*Update this file when CURRENT flips to base-5.2, Client ships object floor, or Helios 0.6 SQL lands.*
