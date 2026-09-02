# Optimization theory — staples `fast_pass` · `scout` · `thorough`

> **Doc status** · **WORK IN PROGRESS** · drafted **2026-09-01** · updated **2026-09-02** · **not** a BASE pack change · **not** hashed CORE · production pin **base-1** · candidate line **base-6.2** · version matrix: [COMPAT.md](../COMPAT.md)
>
> Do **not** stamp this into L0 `messages[]`. Do **not** flip `CURRENT.json`. Cards must be **rendered** into `messages` / Workbench suffix or the model never sees them (`guidance` is stripped on the wire).
>
> **Citation (reserved):** `OPT:36` — optimization theory + staples. Verbose card lives here until a short form graduates into [OPTIMIZATION.md](OPTIMIZATION.md).

**Audience:** catalog authors, Hub Workbench / Prompt Helper, zeus_client, operators  
**Related:** [OPTIMIZATION.md](OPTIMIZATION.md) (`OPT:0` Pachinko, `OPT:6`, `OPT:18`) · [BEST_PRACTICES.md](BEST_PRACTICES.md) · [HINTS.md](HINTS.md) · [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) · [MODE.md](MODE.md) · travel funnel (external) `USE_CASE_TRAVEL_BOOKING_STEP_BY_STEP_v2.md`

---

## 0. One-sentence theory

```text
Optimization = reach ORDER (the answer this turn is allowed to cost)
               by shrinking the right evidence set,
               using one of three staples: fast_pass | scout | thorough.
```

Not: more sub-agents, more rows, more Lists, or a faster empty 200.  
Not: hop-count as the reward.  
Not: “always named_query” on day one (that tool is **not** in the current chat_request verb list).

The staples are the **theory**. Problem class, SLA, and complexity only **pick which staple** and how hard it may spend.

```text
fast_pass   one planned trip to Zeus; summary is a bet
scout       pay one look at live values, then commit
thorough    same bound plan, richer evidence / hydrate; still not more Lists
```

---

## 1. What ORDER is

| Product default | ORDER |
| --- | --- |
| Cheap Client (`ai_process_result: false`) | Zeus **rows/ids** in UI — a table can *be* the answer |
| Essay / insight turn (`ai_process_result: true`) | Grounded **summary** from those rows |
| Funnel bottom (later) | Compact bag **or** governed action (book / dispatch) |

A shallow table that the **SLA asked for** is a win. A shallow table that still needs another chat to become the real answer is a miss — unless SLA says progressive disclosure.

---

## 2. The three staples (optimization theory)

These are closed names. Do not invent a fourth until a staple is proven insufficient.

### `fast_pass` — one planned call

**Law:** exactly **one** AI round. Emit **one terminating `pipeline`** (or one rail **when that tool exists**). Write Layer A **before** results (CORE tradeoff). Bind `@step.ids` / `narrow_to`. Compact `project`.

**Use when:** the plan is already known — tokens, entity types, and funnel steps can be authored without peeking.

**Forbidden:** empty terminate “to look fast”; N unbound Lists; a second pipeline “just to see.”

**Today on the pin:** “logic on Zeus” = **pipeline + transforms** (`set` / `order` / `enrich` / `project`).  
**Later:** graduate a hot fingerprint to a **callable** `named_query` (HTTP `POST /v1/.../named_queries/{name}/execute` exists; it is **not** a catalog verb until Client/Hub wires it). Do not make `fast_pass` mean “call named_query” until that wire exists.

### `scout` — one look, then commit

**Law:** at most **one probe round**, then **one** commit pipeline. Probe is not ORDER.

Probe **may:** `find` `limit:1`–`3` or `return:selectivity` on a MINI-SCHEMA path; tiny `search`; `describe` only if BRIEF/MINI-SCHEMA is missing.  
Probe **must not:** `get_stats` / `list_entity_types` / recount `nodes_total` (CORE); chain `List hotel`, `List airport`, `List landmark`.

**Use when:** inject names **types**, not **live values** (which city tokens, which FTS phrase hits, which ids exist).

**This is the only staple that sees intermediate data** before the terminating plan. CORE “don’t repeat the pipeline” still applies after commit.

### `thorough` — bound plan, richer ORDER

**Law:** still **one** (maybe two if hydrate) AI round. Still **one** bound pipeline, cap 8, `@step.ids`. Richer `project` / optional `get` `include:["body"]`. Coverage > wall time.

**Use when:** SLA wants attributes, snippets, parts[] coverage — not a faster List dump.

**Forbidden:** longer = more independent Lists. Thorough without bind ratio is the Sessions anti-pattern with extra latency.

### How they compose

```text
unknown live values?     scout → then fast_pass or thorough
plan already writable?   fast_pass
SLA wants a rich bag?    thorough  (or scout → thorough)
tight SLA + known plan?  fast_pass
```

Never: scout that never commits. Never: thorough as “try every entity type.” Never: fast_pass as empty-fast when the plan is not known (use scout).

---

## 3. Two clocks (do not mix)

| Clock | Job | Staple role |
| --- | --- | --- |
| **Per turn** | Intent (QD) → pick a staple → verb plan | Model + catalog card |
| **Across traffic (hot-path)** | Repeated **styles** that miss SLA → freeze the winning staple’s plan | Operator: pipeline template, then rail |

Hot-path does not invent a fourth meaning of optimize. It **remembers** a staple that already fit.

**Honest pin:** pathshape Phase 1 scores `hops > 1` / KindPipeline as **S2 waste**, and `fail_rate` is `nil`. That **punishes** a good `fast_pass` funnel. Until the scorer uses **unbound retrievals** and **AI rounds** (not step count), hot-path cannot implement “optimize slow common styles.” Fix the scorer before trusting backlog → named_query.

---

## 4. Problem class (picks a **default staple**, not a different theory)

Two classes. Same three staples. Different ORDER tests and default staple.

### `known_goal` — sized bag (travel step-by-step v2)

Goal can be designed: shrink an id bag until SLA is met. Canonical: *beach / Mexico / fun / April / ≤ $300*.

```text
fuzzy phrase  → search
exact fact    → find (equality only)
connected     → traverse
hard filter   → rail **when wired** (not find.where ranges)
shape         → project
```

**Default staple:** `fast_pass` once the funnel is writable; `scout` if binds/tokens are unknown.  
**Success:** compact rows (and later, binds for a PREPARED).  
**Not every known-goal is a named_query.** Lookups and “top N hotels in Paris” are `find`/`search`→`project`. Rails are how a **hot** fingerprint **graduates**.

The travel **narrative** is six HTTP looks (model sees each bag). The travel **efficient** form is **one planned pipeline** (`fast_pass` / `thorough`) **or** `scout` + pipeline. Do not document those as the same thing.

### `open_ended` — unknown evidence size, **in this graph**

Canonical *in-graph:* *“Why is Tulum busy in April?”* with season/review evidence on the overlay.  
Not canonical: *“Why did the Roman empire fall?”* on `travel-sample.inventory` — **out of corpus**. That is `wish_i_knew` / clarify, not `thorough`.

**Default staple:** `thorough` (or `scout` → `thorough`).  
**Success:** grounded synthesis **from this scope’s data**, refs, confidence, gaps.  
**`fast_pass` is usually wrong** (empty/shallow). A PREPARED whose binds are “the whole why” is usually wrong. Partial seed rails are OK later.

### Class is a **scope default + optional turn label**

Do **not** treat “one class per `bucket.scope` forever” as a physical law. Real inventory chat mixes “book me X” and “why is X popular.” Split **stamps / rails / books** when that mix is chronic. Don’t A/B Rome-essays against hotel funnels on one gold book.

Open-ended on Zeus = **unbounded evidence budget on this overlay**, not a general encyclopedia.

---

## 5. Weights that pick a staple: SLA × complexity

Neither is a first-class engine input today. Treat them as **operator / profile inputs** (Workbench, Client hints, promotion profile).

| Weight | Meaning | Not |
| --- | --- | --- |
| **SLA** | How complete / fresh / timely ORDER must be | p95 of a List dump |
| **Complexity** | How much **catalog work** you must do to be allowed to stop | Word count; “more agents” |

Complexity is more than row count: join fan-out, FTS quality, freshness, RBAC, empty index, unknown tokens.

```text
data_budget ≈ f(class default, SLA, complexity)  →  staple

known_goal  + plan writable + tight SLA     → fast_pass
known_goal  + unknown tokens                → scout → fast_pass | thorough
open_ended  + in-graph + loose SLA          → thorough
open_ended  + thin map                      → scout → thorough
open_ended  + out of corpus                 → wish / clarify (not a staple spend)
open_ended  + tight SLA                     → bound thorough + wish — do not fake a rail
```

---

## 6. Per turn: intent, then verbs (retrieve vs shape)

**Step 1 — intent.** `query_decomposition` is the right field. It is **not** “done”: live QD is often `List` + one entity. Weak QD makes every staple look like brute force. Gold books need **expected_route** and expected QD, not only suffix prose.

**Step 2 — compile under the chosen staple.**

Pin `verb_order` is **12** (not “8+7”):  
`find`, `get`, `pipeline`, `describe`, `set`, `order`, `enrich`, `project`, `traverse`, `search`, `analyze`, `return`.

Useful split:

| Layer | Job | Examples |
| --- | --- | --- |
| **Retrieve / control** | Open or bound a bag; terminate | `describe`, `get`, `find`, `search`, `traverse`, `pipeline`, `analyze`, `return` |
| **Shape** | Cheap work **on ids** | `set`, `order`, `enrich`, `project` |
| **Other surfaces** | Not in the 12 until wired | `named_query` HTTP, `walk_path`, … |

MASQ “find cheap, search expensive” is **per call**. Ten unbound finds are expensive. One `pipeline` that shrinks a bag is one AI round.

Independent **parts in one pipeline** (`set` union, BP:6) can be the right spend. Ban **unbound rediscovery**, not all parallelism.

Compiler:

1. Decompose (and don’t trust a bare `List`).
2. Pick staple (`fast_pass` / `scout` / `thorough`).
3. Size the bag (known_goal: e.g. 400→120→12→5; open_ended: hard cap first recall).
4. Retrieve vs shape; hard $ / dates → rail **when it exists**.
5. Bind after the first step.
6. Stop when ORDER meets SLA, or `wish_i_knew`.

---

## 7. Three execution shapes (do not collapse)

CORE: a **terminating** pipeline writes `summary` + `query_decomposition` **before** seeing rows.

| Shape | Staple | Sees intermediate data? |
| --- | --- | --- |
| One terminating pipeline | `fast_pass` or `thorough` | **No** — summary is a bet |
| Probe + terminating pipeline | `scout` then `fast_pass` / `thorough` | **Yes**, once |
| Client multi-round | Product (`ai_process_result`, user pick) | Yes, by setting |

“Get close then refine” is the **funnel shape** (narrow the same ids). Adaptive refine (author step 2 after seeing step 1) **is scout or multi-round**, and costs an AI round. Selling 1-round speed and evidence-adaptive refine as one strategy is false.

---

## 8. Catalog placement (hash boundary)

```text
L0 hashed     messages + verbs + masq
L1 excluded   guidance.optimization   ← class default + staple (must be rendered)
L2 external   named_query docs        ← graduate known_goal hot paths (HTTP today)
wire          assembler → messages[0]  or Workbench system_prompt_suffix
```

```json
"guidance": {
  "optimization": {
    "question_class": "known_goal",
    "strategy": "fast_pass",
    "max_ai_rounds": 1,
    "max_pipeline_steps": 4,
    "probe_budget": 0,
    "prefer_named_query": false,
    "project": "compact",
    "hydrate": "summary",
    "on_empty": "wish_or_rail"
  },
  "strategy_boosts": {
    "fast_pass": 1
  }
}
```

`prefer_named_query: true` only when the model **has** that tool. Default **false** on current pin.

Other staple defaults:

```json
"strategy": "thorough",
"max_ai_rounds": 2,
"max_pipeline_steps": 8,
"probe_budget": 0,
"prefer_named_query": false,
"project": "rich",
"hydrate": "body_if_needed",
"on_empty": "adjust_once_then_wish"

"strategy": "scout",
"max_ai_rounds": 2,
"max_pipeline_steps": 8,
"probe_budget": 1,
"prefer_named_query": false,
"project": "compact",
"hydrate": "summary",
"on_empty": "probe_then_pipeline"
```

| When | Mechanism |
| --- | --- |
| Scope default class | Operator sets `question_class` on the catalog; turn may override |
| Default staple | Stamp `…:c-M_fast` / `_scout` / `_thorough` or one stamp + `strategy` |
| Per session | `hints.optimization.strategy` (extends ZC-WISH-040; not live until Client injects) |
| Lab | Workbench-2 suffix / A/B **within one book class** |

---

## 9. Prose cards (suffix / messages)

Prefix with class default, then **exactly one** staple card.

```text
## Question class: known_goal
ORDER is a sized bag (ids/rows) for this overlay. Shrink one id bag.
Hard filters (price, dates) are rails when wired — never find.where ranges.
Default staple: fast_pass when the funnel is writable; else scout then commit.

## Question class: open_ended
ORDER is grounded synthesis from THIS scope. Evidence size is unknown.
Out-of-corpus questions → wish_i_knew / clarify, not a bigger search.
Default staple: thorough (or scout → thorough). Do not default fast_pass.
```

### Staple: fast_pass

```text
## Optimization: fast_pass
Exactly one AI round. One terminating pipeline (cap short). Bind @step.ids.
Plan the funnel up front; summary is written before results.
Shape with set/order/enrich/project. Compact project.
Do not terminate empty. Do not scout. Do not List-per-entity.
If live tokens are unknown, this is the wrong staple — use scout.
named_query only if that tool is actually on the catalog.
```

### Staple: scout

```text
## Optimization: scout
MINI-SCHEMA names types; it does not name live values.
At most one probe: find limit 1–3 or selectivity on a [gsi] path, or search limit 5,
or describe if brief is missing.
Probe is not ORDER. Next round: one terminating pipeline using observed @ids / tokens.
Never rediscover nodes_total / entity type lists. Never List every entity type.
```

### Staple: thorough

```text
## Optimization: thorough
Coverage > wall time, still one bound pipeline (cap 8), still @step.ids.
Richer project / get include body when attributes are the SLA.
Do not spend rounds on List-per-entity. Extra AI round only to hydrate a thin bag.
Empty: one bound adjust, then wish_i_knew. Never invent rows.
```

---

## 10. Scoring (do not invent a fourth system)

Reuse closed-loop profiles. Add **hygiene**. Books stay **inside one class** as much as possible; mixed product traffic is OK, mixed **gold books** are not.

| Staple | Promotion profile | Hygiene |
| --- | --- | --- |
| fast_pass | `latency_first` / `cost_first` | 1 AI round; bound steps; empty = fail |
| scout | `balanced` | `probe_budget` ≤ 1, then bind ratio on commit |
| thorough | `balanced` | parts coverage; hydrate when asked; still bound |

S2 waste = **unbound** retrievals / extra **AI rounds** / find-on-text_fts — **not** `len(pipeline steps) > 1`.

Do not RLHF “use pipeline”; models will wrap a single `find`.

---

## 11. Assumptions — keep vs change

### Keep

- Optimization ≠ more agents / more unbound Lists.
- Intent field first; then a verb plan.
- Bind the same id bag.
- `find` equality; language → `search`.
- Cards must be rendered; `guidance` JSON alone is a no-op.
- MASQ cheap-find steers List today.
- Pathshape hop-waste fights a good funnel (must change the **scorer**, not the staple names).
- Travel-sample inventory ≠ OTA funnel catalog.

### Change (this revision)

| Old assumption | Now |
| --- | --- |
| known_goal = fill a named_query | ORDER = sized bag; rail is a **graduation** |
| named_query is how the model puts logic on Zeus | **Pipeline + transforms** on current pin |
| Terminating pipeline = see-then-refine | Summary is a **bet**; adaptive refine = scout / multi-round |
| One class per bucket forever | Scope **default** + turn label; mixed inventory chat is normal |
| “Why Rome fell” is Zeus open-ended | Open-ended = **in-graph** unknown budget; out-of-corpus = wish |
| SLA × complexity already drive the engine | Operator inputs to **invent**; A/B still HTTP OK − empty |
| Step 1 intent is done | QD exists; quality is often `List` — fix the **book** |
| 8 action + 7 other APIs | **12** pin verbs; retrieve vs shape; named_query is another surface |
| More parallelism never faster | Unbound Lists no; BP:6 parallel **parts in one pipeline** yes |
| Shallow then another chat always bad | Cheap table can **be** ORDER (`ai_process_result: false`) |
| Mini-schema never enough | Often enough for lookups; scout is **value-space** gaps |
| fast_pass default for all known_goal | Only when the plan (or a wired rail) exists; else scout |

---

## 12. What this is not

| Temptation | Better home |
| --- | --- |
| Fourth staple | Prove the three insufficient first |
| Fork `mode=open` for scout or “why” | Class default + staple; [MODE.md](MODE.md) is join/noise |
| Hash staples into L0 CORE | L1 / hints until proven |
| Free-text “be faster” | Closed staple + caps |
| named_query as the “why” machine | thorough + evidence budget |
| Mexico / Tulum / Rome in CORE | Books; staples are motion-shaped |
| Reward pipeline step count | Unbound retrievals + extra LLM rounds |
| Trust hot-path → rail on current scorer | Fix S2 = unbound / AI rounds first |

---

## 13. Open work (WIP)

- [ ] Assembler renders `guidance.optimization` (class default + **staple**) into `messages[0]`.
- [ ] Workbench-2 staple picker → suffix + Export; class is a default, not a second product unless books diverge.
- [ ] Client `hints.optimization.strategy` = `fast_pass` \| `scout` \| `thorough` (ZC-WISH-040; not live until inject).
- [ ] A/B hygiene: `expected_route` + bind ratio; **do not** classify KindPipeline as S2.
- [ ] Gold books labeled **class + staple** (funnel vs in-graph why vs List-only — List-only books lie).
- [ ] Wire named_query as a tool **before** `prefer_named_query: true`.
- [ ] Short `OPT:36` staple card in [OPTIMIZATION.md](OPTIMIZATION.md) when stable.
- [ ] No pack JSON change until cards are rendered and one book A/B exists.

---

## Checklist (later PR)

```text
Rule: staples fast_pass | scout | thorough; class known_goal|open_ended is a default
Placement: HINTS / guidance (L1) — not CORE, not MODE
Modes: all (orthogonal)
Day-one?: staple pick per product/book; class default on scope
Hashed?: no
Enforced by: rendered card until Client/assembler exists
Citation: OPT:36 (reserved)
Anti-pattern: mix gold books; scout never commits; fast_pass empty-fast;
  named_query claimed as a verb on current pin; terminating pipeline sold as see-then-refine;
  out-of-corpus why treated as thorough; hop-count as waste
```
