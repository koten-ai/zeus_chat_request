# Optimization methods and pickable strategies

> **Doc status** · **WORK IN PROGRESS** · drafted **2026-09-01** · updated **2026-09-02** · **not** a BASE pack change · **not** hashed CORE · production pin **base-1** · candidate line **base-6.2** · version matrix: [COMPAT.md](../COMPAT.md)
>
> Do **not** stamp this into L0 `messages[]`. Do **not** flip `CURRENT.json`. Do **not** treat these enums as wire law until an assembler renders them and a book A/B proves them.
>
> **Citation (reserved):** `OPT:36` — problem class + pickable execution posture. Full card lives here until this graduates into [OPTIMIZATION.md](OPTIMIZATION.md).

**Audience:** catalog authors, Hub Workbench / Prompt Helper, zeus_client, operators choosing a `bucket.scope`  
**Related:** [OPTIMIZATION.md](OPTIMIZATION.md) (`OPT:0` Pachinko, `OPT:6` fast-pass vs multi-turn, `OPT:18` mode ≠ strategy) · [BEST_PRACTICES.md](BEST_PRACTICES.md) (`BP:1`–`BP:6`) · [HINTS.md](HINTS.md) · [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) · [MODE.md](MODE.md) · travel funnel (external) `USE_CASE_TRAVEL_BOOKING_STEP_BY_STEP_v2.md`

---

## 0. What optimization is (and is not)

Optimization here is **not “go faster.”** It is:

```text
Reach ORDER — the answer this question is allowed to cost —
by touching as little of the graph as possible,
in as few AI rounds as possible.
```

| Looks like a win | Usually is not |
| --- | --- |
| Same ORDER, fewer **AI rounds** | More sub-agents / more parallel Lists |
| Same ORDER, fewer **unbound** retrievals | Fewer tools that terminate empty |
| Same ORDER, work on Zeus (pipeline / rail) | Shallow 200 that forces another chat to do the real work |
| Hot-path rail for a **repeated known-goal** style | Teaching CORE a Mexico if-then, or a named_query for “why Rome fell” |

More processes over more rows is usually **anti-optimization**. A cheap blurry answer that still needs further processing is also anti-optimization unless the **SLA says** progressive disclosure.

**Hot-path** (original thought) is still valid as the *fleet* job: find common **styles** of question that miss SLA and freeze a plan. It does not invent a new meaning of optimize. It **remembers** a plan that already fit.

Two clocks:

| Clock | Job |
| --- | --- |
| **Per turn** | Intent (step 1) → verb plan (step 2) under a data budget |
| **Across traffic** | Cluster by style; if that style misses SLA, freeze the plan (rail or recipe) |

Before picking `thorough` / `fast_pass` / `scout`, name the **problem class**. There are two, and they want **different** optimization methods.

---

## 1. Two problem classes (frame this first)

These are not two temperatures of the same knob. They are **different products**.

### `known_goal` — size is designable; ORDER is a bind list

Canonical: travel booking step-by-step v2.

> *Vacation beach spot in Mexico that is fun in April, not more than $300 a night.*

The **goal is known**: collect the **correct inputs** for a prepared statement / `named_query` (ids, dates, guests, `max_nightly_usd`, …), then project a compact bag. You can **design** how much data to process (400 → 120 → 40 → 12 → 5). “Get close, then refine” means **narrow the same id bag** (`narrow_to` / `@step.ids`), then the hard rail.

```text
fuzzy phrase   → search (hybrid)
exact fact     → find (equality)
connected      → traverse / walk_path
hard filter    → named_query PREPARED   ← the actual ORDER machine
shape          → project
```

Success = the rail returns bookable (or otherwise SLA-complete) rows.  
Failure = List-per-entity fan-out, or `find` faking `nightly_usd <= 300`.

Hot-path here **shines**: repeated “place + vibe + date + budget” → freeze the shrink-plan into a pipeline template or SQL rail.

### `open_ended` — unknown size; ORDER is a grounded explanation

Canonical: *“Why did the Roman empire fall?”*

You do **not** know how much graph, text, or hops are enough. There is no honest PREPARED statement whose binds are “the fall of Rome.” Success is a **grounded narrative** (or structured synthesis) with evidence, confidence, and `wish_i_knew` — not five hotel rows.

Optimization is **budgeted evidence gathering**:

- Bound first recall (do not ingest the whole corpus).
- Follow the strongest evidence links, not every entity type.
- Stop when SLA / confidence says stop, or admit gaps.
- Refine = *another bounded pass on the same evidence set*, not a new global List.

A named_query rail is the **wrong** end-state for most of this class. Hot-path here might remember a **recipe** (search primary sources → hop citations → project snippets), not a hotel availability PREPARED.

### Do not mix them on one endpoint / `bucket.scope`

| | `known_goal` | `open_ended` |
| --- | --- | --- |
| Typical scope | travel inventory, catalog, booking, BI facts | research KB, papers, investigations, “why / how come” |
| Typical mode bias | `analytics` / `custom` + rails | `research` / `open` (join/noise), still not “mode=open because paragraph” |
| Default think-budget | `fast_pass` (or `scout` then rail) | `thorough` (or `scout` then thorough) |
| ORDER | Compact bag / binds for PREPARED | Grounded explanation + refs |
| Hot-path output | `named_query` / frozen pipeline | Recipe + maybe partial rails (seed resolve only) |
| Gold book | Multi-axis funnel questions | Causal / synthesis / coverage questions |

A travel `bucket.scope` should not be asked why Rome fell. A history KB should not be asked to fill `hotels_under_price_with_availability_v3`. **Tune Zeus/Koten per class, per scope.** One catalog, one book, one rail set, one default strategy — not a mushy endpoint that “does both.”

If a company needs both, that is **two scopes** (or two products), two stamped `chat_request`s, two Helios funnels.

```text
question_class   = known_goal | open_ended     ← pick per bucket.scope (almost never per turn)
strategy         = thorough | fast_pass | scout  ← think-budget inside that class
mode             = analytics | research | …      ← join/noise/hop appetite
playbook BP:*    = verb class (always-on floor)
```

---

## 2. Guiding weights: SLA × complexity

| Weight | What it is | What it is not |
| --- | --- | --- |
| **SLA** | How complete / fresh / timely ORDER must be for **this surface** | p95 of a List dump |
| **Complexity** | How much data you must **process** to be allowed to stop | Word count, or “use more agents” |

Complexity is **catalog work**, not LLM difficulty:

| Cheap | Expensive |
| --- | --- |
| One entity, one equality | Several axes in one paragraph |
| Candidate set already small | First recall is 400 of 480k |
| Inject already names the tokens | Live values unknown (`scout`) |
| Answer is a count from BRIEF | Live price / availability **or** an unbounded “why” |

```text
data_budget ≈ f(question_class, SLA, complexity)

known_goal  + tight SLA  + known tokens     → fast_pass (rail)
known_goal  + unknown tokens                → scout once, then rail / short pipeline
open_ended  + loose SLA                     → thorough, stop on confidence
open_ended  + thin map                      → scout once, then thorough
open_ended  + tight SLA                     → bound evidence + clarify / wish — do not fake a rail
```

The travel funnel is **high complexity, known goal**. “Why Rome fell” is **unknown size, open-ended**. Same three think-budgets, **different** success tests.

---

## 3. Per turn: intent then verbs

**Step 1 — intent (already captured).**  
`query_decomposition`: intent, entity, parts, geo, price, … That says **what ORDER is**.

**Step 2 — compile a plan.**  
Given class + SLA + data-budget, which of the V2 verbs (and rails) **buy** that ORDER?

Treat the catalog as two layers (about **8 retrieve/control** + **the rest shape/rail**):

| Layer | Job | Examples |
| --- | --- | --- |
| **Retrieve / control** | Open or bound a bag; plan vs terminate | `describe`, `get`, `find`, `search`, `traverse`, `pipeline`, `analyze`, `return` |
| **Shape / rail** | Cheap work **on ids**, or skip planning | `set`, `order`, `enrich`, `project`, `named_query`, `walk_path`, … |

MASQ “find is cheap” is true **per call**. Ten unbound finds are expensive. One `pipeline` that shrinks an id bag is **one AI round**.

Compiler:

1. Decompose (step 1).
2. **Size the bag** (known_goal: 400→120→12→5; open_ended: hard cap on first recall).
3. Pick retrieve vs shape — language → `search`; equality → `find`; hop → `traverse`; rank/shape → `order`/`project`; live $ / dates → **rail**.
4. **Bind** every step after the first to the previous ids / evidence set.
5. **Stop** when ORDER satisfies SLA, or `wish_i_knew`.

If the fingerprint is already a hot path **and** the class is `known_goal`, skip 2–4 and call the rail.

---

## 4. Think-budget strategies (`thorough` / `fast_pass` / `scout`)

These are **how hard this turn may think** *inside* a class. They are not domain policy (`mode`) and not a substitute for `question_class`.

| Strategy | Operator intent |
| --- | --- |
| **`thorough`** | Coverage > wall time. Detailed, grounded bag or explanation. |
| **`fast_pass`** | One AI round. Prefer Zeus (`named_query` / frozen template). Natural **default for `known_goal`**. |
| **`scout`** | MINI-SCHEMA names types; it does not name live values. One probe, then commit. |

`fast_pass` on `open_ended` is usually **wrong** (empty or shallow terminate).  
`named_query` as the default first tool on `open_ended` is usually **wrong**.  
`scout` that never commits is the Sessions `List · hotel` anti-pattern — on **both** classes.

```text
mode            = domain posture (analytics / open / fraud / …)
question_class  = known_goal | open_ended          ← per scope
strategy        = think budget this turn (WIP pick)
playbook BP:*   = verb class + recipes
hints.*         = per-turn soft bias
named_query     = server rail when class is known_goal and fingerprint is hot
```

### What each strategy changes

| | **thorough** | **fast_pass** | **scout** |
| --- | --- | --- | --- |
| Goal | Rich, grounded ORDER | 1–2 hops; Zeus does the work | Learn **value space**, then one pipeline |
| AI rounds | 1, maybe 2 if hydrate | **1** | **1 probe + 1 commit** (hard cap) |
| Pipeline steps | Up to 8, bound `@step.ids` | Short; prefer named_query / frozen template | Probe is **not** the answer |
| Project | Richer fields; optional `get` body | Compact fields | Probe: 1–3 rows / `return:count`; then compact |
| First move if inject is thin | Still a pipeline; larger candidate limits | Rail or fail-closed `wish_i_knew` | Budgeted sample / `find limit:1` / `describe` **values**, not stats |
| Failure mode to forbid | N independent `List`s | Empty terminate that “looks fast” | Probe that never commits |
| Fits `known_goal` | When SLA wants a rich bag after the rail | **Default** once binds are known | When tokens/ids for the rail are unknown |
| Fits `open_ended` | **Default** | Rare (tight SLA + already-bound evidence) | When the map does not say what to read first |

CORE already says BRIEF is enough for **counts and type names**. Scout is **option discovery**, not recounting `nodes_total`.

---

## 5. Catalog placement (hash boundary)

Keep class + strategy **out of the contract hash** so operators can A/B without republishing CORE.

```text
L0 hashed     messages + verbs + masq          ← playbook floor (unchanged)
L1 excluded   guidance.optimization            ← question_class + strategy (WIP)
L2 external   named_query rails                ← known_goal fast_pass
wire          assembler copies L1 into messages[0]
              (or Workbench system_prompt_suffix)
```

**Runtime fact:** the chat path keeps `messages` + tools and **strips** `guidance` before the provider. JSON-only `guidance.optimization` that is never rendered does nothing. Until an assembler exists, Workbench draft **suffix** / Client `hints.optimization` must carry the prose card.

Suggested closed enums (not free text):

```json
"guidance": {
  "optimization": {
    "question_class": "known_goal",
    "strategy": "fast_pass",
    "max_ai_rounds": 1,
    "max_pipeline_steps": 4,
    "probe_budget": 0,
    "prefer_named_query": true,
    "project": "compact",
    "hydrate": "summary",
    "on_empty": "wish_or_rail"
  },
  "strategy_boosts": {
    "fast_pass": 1
  }
}
```

`known_goal` + `thorough` (rich bag after a funnel):

```json
"question_class": "known_goal",
"strategy": "thorough",
"max_ai_rounds": 2,
"max_pipeline_steps": 8,
"probe_budget": 0,
"prefer_named_query": true,
"project": "rich",
"hydrate": "body_if_needed",
"on_empty": "adjust_once_then_wish"
```

`open_ended` + `thorough`:

```json
"question_class": "open_ended",
"strategy": "thorough",
"max_ai_rounds": 2,
"max_pipeline_steps": 8,
"probe_budget": 0,
"prefer_named_query": false,
"project": "rich",
"hydrate": "body_if_needed",
"on_empty": "adjust_once_then_wish"
```

`scout` (either class; probe then commit):

```json
"strategy": "scout",
"max_ai_rounds": 2,
"max_pipeline_steps": 8,
"probe_budget": 1,
"prefer_named_query": false,
"project": "compact",
"hydrate": "summary",
"on_empty": "probe_then_pipeline"
```

### When to pick

| When | Mechanism (target) |
| --- | --- |
| **Scope / endpoint** | Set `question_class` once for that `bucket.scope`. Do not A/B Rome vs hotels on the same catalog. |
| Default think-budget | Stamp customs (`…:c-M_fast` / `_thorough` / `_scout`) **or** one stamp + `strategy` |
| Per session | Client `hints.optimization` (same keys) — extends [ZC-WISH-040](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) |
| Lab | Workbench-2 draft suffix / A/B pane B — **within one class** |

A/B compares **strategy cards on the same class**, not “fast hotel rail vs why-Rome essay.”

---

## 6. Prose cards (insert into `messages` / suffix)

Helper can paste these as `guidance_markdown` today. Prefix with the class. Later the assembler fills them from `guidance.optimization`.

### Class banners

```text
## Question class: known_goal
The user wants a compact answer bag (ids/rows) whose fields can bind a named_query or frozen pipeline.
Shrink one id bag. Hard filters (price, dates, availability) are rails, not find.where ranges.
Stop when the rail/project satisfies SLA.

## Question class: open_ended
The user wants a grounded explanation. Evidence size is unknown. There is no PREPARED whose binds are the whole question.
Bound first recall. Follow evidence; do not List every entity type. Stop on confidence/SLA or wish_i_knew.
Do not invent a named_query for a causal essay.
```

### thorough — detail over speed

```text
## Optimization: thorough
Coverage > wall time. One terminating pipeline (cap 8). Bind @step.ids.
Use search for language, find for [gsi], hops for relations, order+project for top-N.
Hydrate (get include body / richer project) when the user needs attributes, not just ids.
Do not spend rounds on List-per-entity. Extra AI round only if the first bag is too thin to project.
Empty: one bound adjust, then wish_i_knew. Never invent rows.
```

### fast_pass — speed; logic on Zeus (`known_goal` default)

```text
## Optimization: fast_pass
Minimize AI rounds (exactly one). Prefer named_query / frozen pipeline template over planning.
If a rail matches, call it and project compact fields. Do not scout.
If no rail and the ask is multi-step, emit ONE short pipeline (search/find → bind → project).
Do not terminate empty to look fast. Missing rail → wish_i_knew (kind:tool|data), not N List calls.
If question_class is open_ended, do not use this card as the default.
```

### scout — inject is not enough; then commit

```text
## Optimization: scout
MINI-SCHEMA names types/indexes; it does not name live values. If predicates are underspecified
(unknown tokens, empty where, no id bag), spend AT MOST one probe round:
  describe (inventory only if brief missing) OR find limit 1–3 OR search limit 5
  OR find return:count|selectivity on a real [gsi] path.
Probe is not the answer. Next round: ONE pipeline that uses the observed values (@ids, tokens).
Never rediscover nodes_total / entity type lists from the brief.
Never chain List hotel, List airport, List landmark as “exploration.”
```

---

## 7. CORE conflict (scout vs “never rediscover”)

CORE: *never rediscover stats when BRIEF is present.* Scout must **not** call `get_stats` / `list_entity_types`. It **may**:

- `find` `limit:1` or `return:selectivity` on a **schema path**
- tiny `search` to see if a phrase hits
- `describe` only when inject is actually missing (already allowed)

Value-space ≠ inventory.

**fast_pass** without L2 rails (on `known_goal`) is just “terminate sooner.” Hard filters stay `named_query`.

**thorough** still needs bind ratio. Longer is not “more Lists.”

---

## 8. Scoring / promotion (do not invent a fourth system)

Reuse Zeus closed-loop profiles; add **hygiene** so B cannot win by dumping lists faster. **Books and A/B stay inside one `question_class`.**

| Strategy | Promotion profile | Hygiene extra |
| --- | --- | --- |
| thorough | `balanced` (quality first; ignore small latency) | parts coverage; hydrate when asked; open_ended: evidence refs, not empty-fast |
| fast_pass | `latency_first` / `cost_first` | rail hit **or** 1-round pipeline; empty = fail; only default on `known_goal` |
| scout | `balanced` | `probe_budget` ≤ 1, then bind ratio on the commit turn |

Pathshape **S2 waste** should mean **unbound** retrievals / extra **AI rounds** / find↔search divergence — **not** `len(pipeline steps) > 1`. A bound 5-step funnel is a **known_goal rail candidate**, not waste.

Gold books: label **class + strategy**. A “List hotel” book will always elect `fast_pass` and hide thorough/scout. A “why Rome” book must not share a catalog with the hotel funnel.

Product reward:

| Class | ORDER (center slot) |
| --- | --- |
| `known_goal` | Compact evidence bag, or later book/dispatch (Pachinko) |
| `open_ended` | Grounded explanation + refs; confidence; gaps named |

Do not RLHF “use pipeline”; the model will wrap a single `find` in a 1-step pipeline.

---

## 9. What this is not

| Temptation | Better home |
| --- | --- |
| Fork `mode=open` for scout or for “why” questions | [MODE.md](MODE.md) · `question_class: open_ended` |
| One `bucket.scope` / one endpoint for hotels **and** Rome | Two scopes, two stamps, two books |
| Hash strategy into L0 CORE | This file stays L1 / hints until proven |
| Free-text “be faster” with no caps | Closed enums + `max_ai_rounds` / `probe_budget` |
| Per-question auto-pick of class | Operator sets class on the scope |
| Reward pipeline step count | Reward unbound retrievals + extra LLM rounds |
| Mexico / Tulum / “Rome” in CORE | Book questions; class is per scope; strategy is motion-shaped |
| named_query as the optimization for open-ended “why” | Recipe + evidence budget; maybe partial seed rails only |

---

## 10. Open work (this is WIP)

- [ ] Assembler renders `guidance.optimization` (class + strategy) into `messages[0]` (or Workbench always copies the cards into suffix).
- [ ] Hub Workbench-2: **class is a scope fact**; strategy picker → suffix + Export.
- [ ] Client `hints.optimization.question_class` / `strategy` (extend [ZC-WISH-040](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md); do not mint a new wish until this graduates).
- [ ] A/B hygiene: `expected_route` + bind ratio; stop classifying KindPipeline as S2; **do not A/B across classes**.
- [ ] Two example books: known_goal funnel (travel-style) vs open_ended synthesis — **different scopes**.
- [ ] Graduate a short `OPT:36` card into [OPTIMIZATION.md](OPTIMIZATION.md) when the enums are stable; keep this file as the verbose design.
- [ ] No pack JSON change until the above is proven.

---

## Checklist (paste into a later PR)

```text
Rule: question_class known_goal|open_ended (per scope) + think-budget thorough|fast_pass|scout
Placement: HINTS / guidance (L1) — not CORE, not MODE
Modes: all (orthogonal to mode overlay; research/open bias often rides open_ended scopes)
Day-one?: class yes (pick when you create the scope); strategy no (operator pick)
Hashed?: no
Enforced by: model (card) until Client/assembler exists
Citation: OPT:36 (reserved)
Anti-pattern if misplaced: mix Rome and hotels on one endpoint; scout becomes List fan-out;
  fast_pass becomes empty terminate; named_query used as the “why” machine; mode=open used as “explore”
```
