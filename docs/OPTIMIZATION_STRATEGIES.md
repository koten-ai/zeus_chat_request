# Pickable optimization strategies (`thorough` / `fast_pass` / `scout`)

> **Doc status** · **WORK IN PROGRESS** · drafted **2026-09-01** · **not** a BASE pack change · **not** hashed CORE · production pin **base-1** · candidate line **base-6.2** · version matrix: [COMPAT.md](../COMPAT.md)
>
> Do **not** stamp this into L0 `messages[]`. Do **not** flip `CURRENT.json`. Do **not** treat this enum as wire law until an assembler renders it and a book A/B proves it.
>
> **Citation (reserved):** `OPT:36` — pickable execution posture. Full card lives here until this graduates into [OPTIMIZATION.md](OPTIMIZATION.md).

**Audience:** catalog authors, Hub Workbench / Prompt Helper, zeus_client  
**Related:** [OPTIMIZATION.md](OPTIMIZATION.md) (`OPT:6` fast-pass vs multi-turn, `OPT:18` mode ≠ strategy, `OPT:19` confidence gates) · [BEST_PRACTICES.md](BEST_PRACTICES.md) (`BP:1`–`BP:6`) · [HINTS.md](HINTS.md) · [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) · [MODE.md](MODE.md)

---

## Why this exists

Operators need **2–3 execution postures** they can pick and insert into a `chat_request*.json` (or a Workbench draft / Client inject) without forking `mode` or republishing CORE:

| Strategy | Operator intent |
| --- | --- |
| **`thorough`** | Longer-running analytics. Wall time is secondary to a **detailed, grounded** bag. |
| **`fast_pass`** | As fast as possible. Prefer **one pipeline** and put repeatable logic on **Zeus** (`named_query` / frozen template). |
| **`scout`** | Mini-schema + SCOPE BRIEF are **not enough** to author a good pipeline (live tokens, ids, option space). Spend a **budgeted probe**, then commit. |

These are **how hard this turn may think**, not domain policy. `mode=analytics` vs `mode=open` stays join/noise/hop appetite ([OPT:18](OPTIMIZATION.md)). A multi-ask paragraph is still [BP:6](BEST_PRACTICES.md), not `mode=open`.

```text
mode            = domain posture (analytics / open / fraud / …)
playbook BP:*   = verb class + recipes (always-on floor)
strategy        = think budget this turn (WIP pick)
hints.*         = per-turn soft bias (path, hot_path, multipart)
named_query     = server rail when the fingerprint is hot
```

---

## What each strategy actually changes

| | **thorough** | **fast_pass** | **scout** |
| --- | --- | --- | --- |
| Goal | Rich, grounded bag | 1–2 hops; Zeus does the work | Learn **value space**, then one pipeline |
| AI rounds | 1, maybe 2 if hydrate | **1** | **1 probe + 1 commit** (hard cap) |
| Pipeline steps | Up to 8, bound `@step.ids` | Short; prefer named_query / frozen template | Probe is **not** the answer |
| Project | Richer fields; optional `get` `include:["body"]` | Compact fields | Probe: 1–3 rows / `return:count`; then compact |
| First move if inject is thin | Still a pipeline; larger candidate limits | Rail or fail-closed `wish_i_knew` | Budgeted sample / `find limit:1` / `describe` **values**, not stats |
| Failure mode to forbid | N independent `List`s | Empty terminate that “looks fast” | Probe that never commits (List-per-entity fan-out) |

CORE already says BRIEF is enough for **counts and type names**. Scout is still valid: brief does not name *which city tokens, FTS phrases, or FK ids actually exist*. Scout is **option discovery**, not recounting `nodes_total`.

---

## Catalog placement (hash boundary)

Keep the pick **out of the contract hash** so operators can A/B without republishing CORE.

```text
L0 hashed     messages + verbs + masq          ← playbook floor (unchanged)
L1 excluded   guidance.optimization            ← the pick (WIP)
L2 external   named_query rails                ← what fast_pass needs
wire          assembler copies L1 into messages[0]
              (or Workbench system_prompt_suffix)
```

**Runtime fact:** the chat path keeps `messages` + tools and **strips** `guidance` before the provider. A JSON-only `guidance.optimization` that is never rendered does nothing. Until an assembler exists, Workbench draft **suffix** / Client `hints.optimization` must carry the prose card.

Suggested closed enum (not free text):

```json
"guidance": {
  "optimization": {
    "strategy": "thorough",
    "max_ai_rounds": 2,
    "max_pipeline_steps": 8,
    "probe_budget": 0,
    "prefer_named_query": false,
    "project": "rich",
    "hydrate": "body_if_needed",
    "on_empty": "adjust_once_then_wish"
  },
  "strategy_boosts": {
    "thorough": 1
  }
}
```

`fast_pass` defaults:

```json
"strategy": "fast_pass",
"max_ai_rounds": 1,
"max_pipeline_steps": 4,
"probe_budget": 0,
"prefer_named_query": true,
"project": "compact",
"hydrate": "summary",
"on_empty": "wish_or_rail"
```

`scout` defaults:

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
| Default for a product | Stamp three customs (`…:c-M_thorough` / `_fast` / `_scout`) **or** one stamp + this block |
| Per session | Client `hints.optimization` (same keys; CORE already says prefer `hints.*`) — extends [ZC-WISH-040](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) |
| Lab | Workbench-2 draft suffix / A/B pane B |

A/B should compare **strategy cards**, not only models.

---

## Prose cards (insert into `messages` / suffix)

Helper can paste these as `guidance_markdown` today. Later the assembler fills them from `guidance.optimization`.

### thorough — detail over speed

```text
## Optimization: thorough
Coverage > wall time. One terminating pipeline (cap 8). Bind @step.ids.
Use search for language, find for [gsi], hops for relations, order+project for top-N.
Hydrate (get include body / richer project) when the user needs attributes, not just ids.
Do not spend rounds on List-per-entity. Extra AI round only if the first bag is too thin to project.
Empty: one bound adjust, then wish_i_knew. Never invent rows.
```

### fast_pass — speed; logic on Zeus

```text
## Optimization: fast_pass
Minimize AI rounds (exactly one). Prefer named_query / frozen pipeline template over planning.
If a rail matches, call it and project compact fields. Do not scout.
If no rail and the ask is multi-step, emit ONE short pipeline (search/find → bind → project).
Do not terminate empty to look fast. Missing rail → wish_i_knew (kind:tool|data), not N List calls.
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

## CORE conflict (scout vs “never rediscover”)

CORE: *never rediscover stats when BRIEF is present.* Scout must **not** call `get_stats` / `list_entity_types`. It **may**:

- `find` `limit:1` or `return:selectivity` on a **schema path**
- tiny `search` to see if a phrase hits
- `describe` only when inject is actually missing (already allowed)

Value-space ≠ inventory. Encode that sentence in the scout card or Helper will regenerate the waste CORE was written to stop.

**fast_pass** without L2 rails is just “terminate sooner.” Hard filters (price, dates, availability) stay `named_query`, not a prompt adjective.

**thorough** still needs bind ratio. Longer is not “more Lists.”

---

## Scoring / promotion (do not invent a fourth system)

Reuse Zeus closed-loop profiles; add **hygiene** so B cannot win by dumping lists faster.

| Strategy | Promotion profile | Hygiene extra |
| --- | --- | --- |
| thorough | `balanced` (quality first; ignore small latency) | parts coverage; hydrate when asked |
| fast_pass | `latency_first` / `cost_first` | rail hit **or** 1-round pipeline; empty = fail |
| scout | `balanced` | `probe_budget` ≤ 1, then bind ratio on the commit turn |

Pathshape **S2 waste** should mean **unbound** retrievals / extra **AI rounds** / find↔search divergence — **not** `len(pipeline steps) > 1`. A bound 5-step pipeline is a rail candidate, not waste.

Gold books should **label** which strategy they test. A “List hotel” book will always elect `fast_pass` and hide the other two.

Product reward remains Pachinko **ORDER** (compact evidence bag, later book/dispatch) — not “pretty tools.” Do not RLHF “use pipeline”; the model will wrap a single `find` in a 1-step pipeline.

---

## What this is not

| Temptation | Better home |
| --- | --- |
| Fork `mode=open` for scout | [MODE.md](MODE.md) · [OPT:18](OPTIMIZATION.md) |
| Hash strategy into L0 CORE | This file stays L1 / hints until proven |
| Free-text “be faster” with no caps | Closed enum + `max_ai_rounds` / `probe_budget` |
| Per-question auto-pick | Operator/client choice until the enum is stable |
| Reward pipeline step count | Reward unbound retrievals + extra LLM rounds |
| Mexico / Tulum in CORE | Book questions; strategy is motion-shaped |

---

## Open work (this is WIP)

- [ ] Assembler renders `guidance.optimization` into `messages[0]` (or Workbench always copies the card into suffix).
- [ ] Hub Workbench-2 strategy picker → suffix + Export `guidance.optimization`.
- [ ] Client `hints.optimization.strategy` (extend [ZC-WISH-040](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md); do not mint a new wish until this graduates).
- [ ] A/B hygiene: `expected_route` + bind ratio; stop classifying KindPipeline as S2.
- [ ] Three labeled books (thorough / fast_pass / scout) on one multi-part paragraph.
- [ ] Graduate a short `OPT:36` card into [OPTIMIZATION.md](OPTIMIZATION.md) when the enum is stable; keep this file as the verbose design.
- [ ] No pack JSON change until the above is proven.

---

## Checklist (paste into a later PR)

```text
Rule: pickable execution posture thorough | fast_pass | scout
Placement: HINTS / guidance (L1) — not CORE, not MODE
Modes: all (orthogonal to mode overlay)
Day-one?: no (operator pick; default thorough or fast_pass per product)
Hashed?: no
Enforced by: model (card) until Client/assembler exists
Citation: OPT:36 (reserved)
Anti-pattern if misplaced: scout becomes List fan-out; fast_pass becomes empty terminate; mode=open used as “explore”
```
