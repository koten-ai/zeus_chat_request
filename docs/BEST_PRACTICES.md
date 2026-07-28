# Zeus chat_request — retrieval best practices

> **Doc status** · last reviewed **2026-07-27** · production pin **base-1** · candidate pack **base-6** (content; wire still base-5) · version matrix: [COMPAT.md](../COMPAT.md)  
> **Citation prefix:** `BP:N` (stable IDs for Prompt Helper / chat_request refs — e.g. `see BP:4`)  
> **Consumers:** humans (authors, operators) **and Zeus Hub Prompt Helper** — Helper may load this file, insert playbook cards into drafts/stamps, and cite **`BP:N`** in `chat_request` / Display Pad / CORE notes.

**Audience:** catalog authors, zeus_client / **Prompt Helper**, operators writing `company_context`  
**Pack surface today:** `v2/base/base-6/` (and prior content trains) CORE + verbs + runtime inject (SCOPE BRIEF / MINI-SCHEMA)  
**Related:** [MODE.md](MODE.md) · [ROADMAP.md](ROADMAP.md) · [OPTIMIZATION.md](OPTIMIZATION.md) (`OPT:N`) · [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) · [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) · [HINTS.md](HINTS.md)

This doc is the **policy of use** for Zeus verbs + mini-schema: day-one **wide-mouth** playbook. Design SoT for CORE **Playbook** excerpts — not a second BIBLE and not a pin flip.  
**Where a new law belongs (CORE vs BP vs OPT):** [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md).

---

## Stage map (how this doc is designed)

```text
STAGE DAY-ONE (this file)     First A/B spit tests · gold books · every new scope
  BP:0…BP:12                  Stable recipes + multi-part + short multi-turn

STAGE TRAFFIC (OPTIMIZATION)  Hundreds → 10k+ chats · Hot Path · Funnel
  OPT:N                       Sharpen CORE / hints / rails — cite OPT:4 for multi-turn CORE

PLACEMENT METHOD              docs/PROMPT_RULE_PLACEMENT.md
  CORE / MODE / BP / OPT      Classify every rule (old + new)
```

| Doc | Stage | Prompt Helper use |
| --- | --- | --- |
| **This file** | **Day-one / always floor** | Insert playbook cards; stamp `guidance` / CORE draft with `BP:N` refs |
| **[OPTIMIZATION.md](OPTIMIZATION.md)** | **After traffic** | Insert rails / sharpen notes with `OPT:N` refs |
| **[PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md)** | **Always (meta)** | Decide surface before drafting long text |

Best practices stay **general and stable**. Optimization **points the funnel** after rain — it does not replace this playbook.

### Citation index (Prompt Helper / chat_request)

Use **`BP:N`** in stamps, Display Pad, CORE notes, and Helper actions so inserts stay traceable.

| ID | Title | Stage |
| --- | --- | --- |
| **BP:0** | Three layers (world / instruments / playbook) | day-one |
| **BP:1** | Universal loop (every turn) | day-one |
| **BP:2** | Field class → first verb | day-one |
| **BP:3** | Always / never short law | day-one |
| **BP:4** | Multi-turn reuse — short law (Option B) | day-one |
| **BP:5** | Single-focus recipes A–H (index) | day-one |
| **BP:5A**…**BP:5H** | LOOKUP … STOP (per recipe) | day-one |
| **BP:6** | Multi-intent paragraphs | day-one |
| **BP:7** | Mode bias (open ≠ multi-ask) | day-one |
| **BP:8** | Joins / close / similar vocabulary | day-one |
| **BP:9** | Terminate hygiene | day-one |
| **BP:10** | What to put in the pack later | day-one → CORE |
| **BP:11** | Anti-patterns | day-one |
| **BP:12** | Quick reference card | day-one |
| **BP:13** | Empty / thin result recovery | day-one |
| **BP:14** | Virtual entity types (scalar_ent pivots) | day-one |

**ID rules:** never renumber existing `BP:N` (append new ids). Sub-recipes use `BP:5A`…`BP:5H`. Cross-doc: `OPT:4` = multi-turn CORE candidate under traffic; verbose traffic recipes **OPT:29+**.

---

## Stage: Day-one playbook

## BP:0 — Three layers (do not collapse)

| Layer | What it is | Where it lives |
| --- | --- | --- |
| **World model** | AI-Ready overlay: entities, attributes, relations (map of the world, not a form to invent into) | CORE blurb + inject brief/schema |
| **Instruments** | 13 verbs, costs, WHEN/KEY on tool schemas | `verbs[]` in pack |
| **Playbook (this doc)** | Sequences + decision rules for common ask shapes | Here → later short CORE excerpt |

You already ship map + instruments in base-5.3. Playbook turns them into **reliable first moves**.

```text
Capability (verbs, schema)  +  Policy of use (recipes, multi-part law)  →  good pipelines
```

---

## BP:1 — Universal loop (every mode, every turn)

```text
1. Name entity_type(s) from MINI-SCHEMA (do not invent).
2. Classify field paths: [gsi] equality · text_fts language · display result-only · entity_fk link.
3. Choose ONE primary access path (or N paths if multi-part — §3).
4. Prefer one terminating pipeline (or one decisive tool) over rediscovery rounds.
5. Terminate Layer A from evidence only (summary must not invent tool results).
```

### BP:2 — Field class → first verb (non-negotiable)

| MINI-SCHEMA mark | First move | Never |
| --- | --- | --- |
| `[gsi]` / scalar / entity_fk equality | `find` (`where` equality only) | free text in `where` |
| `text_fts` | `search` (`strategy:fts` / short `query_text`) | `find where` on that path |
| `display` | only in `project` / result rows | filter on it |
| exact public id known | `get` (`include:["body"]` if full node needed) | re-find by name when id works |
| “related / from / of” across entities | seed `find`/`search` → hop (traverse / walk_path / inverse `find`) | invent edge types |

Cost tags (`[cheap]` / `[mod]` / `[exp]`) matter **after** correct class. Wrong class is more expensive than a slightly costlier correct verb.

### BP:3 — Always / never (short law)

| Always | Never |
| --- | --- |
| Prefer inject BRIEF + MINI-SCHEMA over `describe` when present | Rediscover stats/entity lists when inject is green |
| One pipeline for multi-step | Same pipeline thrice hoping for different data |
| Bind `@step.ids` (not bare `@step`) | Invent counts / field values into `summary` |
| Empty result OK → adjust path, clarify, or `wish_i_knew` / `data_gaps`; **≥2 same-topic empties → inventory + MUST wish** | Fake rows / title-only terminate on empty streak |
| `order` with `by: "field:<name>"` and `asc: false` for top-N | `direction: "desc"` on order (not the Zeus API) |
| Prefer reusing prior Zeus tool evidence when the user points at it (**BP:4**) | Unconstrained global rediscovery for “those / listed / above” follow-ups |

**Contract note:** under enforcement, **do not strip tools[] mid-session** (e.g. drop `describe` because mini-schema arrived). Teach skip-in-prose; membership changes only via a **new stamped pack** ([ROADMAP § Getting skinny](ROADMAP.md)).

### BP:4 — Multi-turn reuse (prior Zeus results) — short law

**Within a pipeline** you already bind prior step ids (`@step.ids`).  
**Across user turns**, the model often has only chat history + prior tool rows still in `messages` (Client) — not the Hub “Zeus results” lightbox (UI-only).

**House style (Option B — pack CORE / Prompt Helper card; cite `BP:4`):**

```text
Multi-turn: when the user points at a prior Zeus result ("those / listed / above"),
reuse that evidence (ids, cities, fields) and constrain new tools to it.
Do not re-run the same broad discovery if prior tool rows already answer the restrictor.
If prior rows are missing from context, re-query narrowly or clarify — never invent them.
```

| Prefer | Avoid |
| --- | --- |
| Intersect new filter (e.g. pizza / FTS category) with **prior set** when evidence is in context | Global `search "pizza"` while talking as if prior cities were applied |
| One search/find + **filter to prior set** | N equality `find`s (fan-out / step caps) for large prior sets |
| Re-fetch **smallest** set if history lost the rows | Invent city/id lists into `summary` |
| QD / summary that names the **restrictor** | Prose that claims multi-turn while tools ignore it |

**Client / multi-round:** keep prior tool bodies (or a compact city/id bag) in `messages` when product cares about follow-ups — see [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md). Soft long recipes / last-result inject → [HINTS.md](HINTS.md) · ZC-WISH-040.  
**Sharpening under traffic:** longer multi-turn CORE excerpt + Hot Path → **OPT:4** in [OPTIMIZATION.md](OPTIMIZATION.md#opt4--multi-turn-reuse-prior-zeus-evidence).

---

## BP:5 — Single-focus recipes (high coverage)

Most product turns collapse to a few pipelines. Teach these in CORE; mode overlays only bias which recipe is “default.”  
**Cite:** `BP:5` for the set; `BP:5A`…`BP:5H` for one recipe.

| ID | Legacy | Name | Pattern | Use when |
| --- | --- | --- | --- | --- |
| **BP:5A** | A | **LOOKUP** | `find` (`return:ids`, equality `where`) → `project` | “list / filter X where field = value” |
| **BP:5B** | B | **TEXT** | `search` (`fts`/`hybrid`, short `query_text`) → `project` | language, description, fuzzy name |
| **BP:5C** | C | **TOP_N** | broad `find`/`search` → `order` `by:"field:X"` `asc:false` → `project` `limit:N` | highest / top / ranked |
| **BP:5D** | D | **HOP** | seed `find`/`search` → `traverse` \| walk_path \| inverse `find` → `project` | related-to, multi-entity |
| **BP:5E** | E | **HYDRATE** | …ids → `get` `include:["body"]` | need full node after id bag |
| **BP:5F** | F | **COMPOSE** | two+ id bags → `set` (intersect/union/…) → `project` | “in A and B”, close/similar sets |
| **BP:5G** | G | **STATS** | use SCOPE BRIEF; optional cheap `find` limit 1 | “how many / what types” when brief answers |
| **BP:5H** | H | **STOP** | terminating `pipeline` or `return` | always after evidence |

### 2.1 Minimal examples (copy shape, not domain)

**LOOKUP**

```json
{
  "steps": [
    {"as": "cands", "verb": "find", "entity_type": "Beer", "where": {"brewery_id": "…"}, "return": "ids", "limit": 50},
    {"as": "out", "verb": "project", "ids": "@cands.ids", "fields": ["name", "abv"], "limit": 20}
  ]
}
```

**TEXT**

```json
{
  "steps": [
    {"as": "hits", "verb": "search", "entity_type": "Beer", "strategy": "fts", "query_text": "fruit", "limit": 30, "timeout_ms": 5000},
    {"as": "out", "verb": "project", "ids": "@hits.ids", "fields": ["name", "description"], "limit": 10}
  ]
}
```

**TOP_N**

```json
{
  "steps": [
    {"as": "cands", "verb": "find", "entity_type": "Beer", "return": "ids", "limit": 100},
    {"as": "ord", "verb": "order", "ids": "@cands.ids", "by": "field:abv", "asc": false},
    {"as": "out", "verb": "project", "ids": "@ord.ids", "fields": ["name", "abv"], "limit": 5}
  ]
}
```

**HOP (inverse FK style — common when edges_total is low)**

```text
1) find Brewery where name equality / search name
2) find Beer where brewery_id = <that id>   // inverse_fks on MINI-SCHEMA
3) project
```

Or `traverse` / `walk_path` when ## WALK_PATHS / real edges support it.

**COMPOSE (close / similar / both)**

```text
1) search or find → bag A (@a.ids)
2) search or find → bag B (@b.ids)
3) set op:intersect|union inputs:[[@a.ids],[@b.ids]]
4) project
```

---

## BP:6 — Multi-intent paragraphs (multiple things in one message)

Users often paste a **paragraph**: several asks, compares, filters, and joins. That is **not** a different Zeus API — it is a different **planning problem**.

### 3.1 Is that “open” mode?

**Mostly no.** Modes and multi-intent are orthogonal:

| Concern | What it is | Mode role |
| --- | --- | --- |
| **Multi-intent / multi-part** | User text has **several goals** in one turn | All modes; playbook + `query_decomposition.parts[]` + pipeline/`set` |
| **`open` mode** | Product bias: **serendipity, liberal joins, low confidence floor (~0.20), link maps** | Explore / crawl / public data — *not* “the multi-part mode” |
| **`analytics` mode** | Safe default: structural+semantic edges, ~0.50 floor, evidence before claim | Still handles multi-part, but **tighter join noise** |
| **`fraud` mode** | Weak-signal hops are the product | Multi-hop heavy, not multi-sentence parsing |

So: **paragraph multi-ask** → multi-part playbook (§3.2–3.4).  
**“Show me the whole linky world / sample then expand”** → `open` mode bias (§4).

Using only `open` for multi-intent would:

- raise noise and false joins on BI-like scopes  
- not teach `set` / dual find / QD `parts[]`  
- conflate **exploration policy** with **task decomposition**

### 3.2 Decompose first (Layer A + plan)

Before tools:

1. Split the paragraph into **atomic goals** (list, filter, compare, hop, rank, count).  
2. Emit structure in terminate (and plan against it):
   - `query_decomposition`: core intent + entity; optional **`parts[]`** for distinct sub-goals  
   - `decomposition`: targets / predicates / output grounded in MINI-SCHEMA  
3. Decide: **one pipeline** (shared scope, joinable) vs **sequential rounds** (Client multi-round — [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md)).

```text
Paragraph
  → parts: [P1, P2, P3]
  → each part → recipe A–G
  → join parts with set / hop / shared entity_type
  → one terminating answer (or clarify if under-specified)
```

### 3.3 Patterns for multi-thing turns

| Pattern | User shape | Tool shape |
| --- | --- | --- |
| **Parallel filters (same type)** | “IPAs under 6% and also stouts with fruit in the description” | Two branches → `set` union or two result sections in summary |
| **Close / similar** | “like this beer / near this set / same style as …” | seed resolve → `search` hybrid/vector or GSI style → optional `set` intersect |
| **Combine (AND)** | “in California **and** abv > …” | Prefer one `find` with multiple equality `where` when all GSI; else bag ∩ bag via `set` intersect |
| **Combine (OR)** | “IPA **or** Pale Ale” | two finds/searches → `set` union → project |
| **Join across types** | “breweries in X and their beers” | HOP / inverse FK / walk_path — not one flat `where` across types |
| **Rank after filter** | “top 5 of those” | candidate bag → TOP_N recipe |
| **Compare** | “A vs B” | two lookups → project both → summary compares; optional `set` only if shared-id logic needed |
| **Mixed count + list** | “how many … and show examples” | BRIEF for count when possible; else `find return:count` + limited `project` — do not double full scans |
| **Follow-up on prior Zeus set** | “out of those cities…”, “which of the ones you listed…” | Reuse prior rows/ids/fields in context (**BP:4**); new predicate ∩ prior set — not unconstrained rediscovery |
| **Under-specified paragraph** | many goals, no entities | `policy_action: clarify` or answer partial + `wish_i_knew` — do not invent schema |

### 3.4 One pipeline vs multi-round

| Prefer **one pipeline** when | Prefer **multi-round Client** when |
| --- | --- |
| All parts share one scope and known entity types | User must pick among ambiguous entities mid-flight |
| Joins are FK / id-bag (`set`) expressible | Tool result must be shown before next branch (UX) |
| Budget allows ≤ 8 steps | Plan exceeds step/timeout caps |
| No clarify needed | `policy_action: clarify` then continue |

Hard cap: **8 steps** per pipeline (CORE). Multi-part does not raise the engine cap — **split or sequence**.

### 3.5 Worked multi-intent sketch

User:

> Find fruit-forward beers, also anything over 8% ABV, and show me which of those come from the same brewery as Pliny if you can.

Plan:

```text
parts:
  P1 TEXT fruit  → search Beer fts "fruit" → @fruit.ids
  P2 LOOKUP high abv → find Beer (if abv GSI) or order field:abv → @strong.ids
       (if only rank available: broad find → order field:abv asc:false limit …)
  P3 COMPOSE → set union @fruit @strong → @pool.ids
  P4 resolve Pliny → find/search name → brewery_id
  P5 HOP/inverse → find Beer where brewery_id = that (or filter @pool)
  project names + abv + brewery_id; terminate with parts in query_decomposition
```

Summary states what was found vs what failed (e.g. Pliny not in scope) — no invented Pliny row.

---

## BP:7 — Mode bias (playbook stays shared)

Modes change **join noise, hop appetite, confidence honesty** — not the existence of recipes A–H.

| Mode | Playbook bias |
| --- | --- |
| **analytics** (default) | A–D primary; HOP only on real links; noise floor ~0.50; multi-part OK with tight joins |
| **open** | Same recipes, but **HOP / sample-then-expand** more often; low floor (~0.20); serendipity; **not** the multi-part parser |
| **fraud** | HOP-heavy; weak signals kept; multi-hop bags; careful terminate honesty |
| **code** | HOP on calls/imports; deeper hops; structure before FTS |
| **research** | citation/backlink-ish HOP + semantic search when present |
| **tenant / regulated** | same recipes; **scope wall**; higher confidence bar; less speculative join |
| **private** | local graph + backlinks; no fake corpus stats |
| **auto** | discover/propose mode; don’t over-commit long traversals |
| **custom** | follow injects; conservative joins |

### 4.1 When to actually use **open**

Use **open** when the product goal is:

- public / crawl / link-map exploration  
- “what’s connected / interesting nearby” over BI precision  
- operator accepts **noise** and lower `confidence`

Do **not** switch to open only because the user wrote a long multi-ask paragraph — stay on analytics (or the scope’s bound mode) and apply **§3 multi-intent**.

---

## BP:8 — Joins, “close”, and “similar” (vocabulary)

| User language | Zeus move |
| --- | --- |
| **Join** (relational) | FK `where` / `inverse_fks` / `walk_path` / `traverse` — entity–transaction–entity |
| **Combine** (boolean) | `set` union / intersect / difference on id bags |
| **Close / near** (graph) | traverse limited depth from seed; cap fan-out |
| **Similar** (language/vector) | `search` hybrid/vector/semantic; optional seed |
| **Same as** (identity) | resolve to id first, then equality / FK — not fuzzy forever |

Never implement “join” by inventing a SQL-shaped `where` across unrelated entity types in one `find`.

---

## BP:9 — Terminate hygiene (multi-part included)

| Field | Single-focus | Multi-intent paragraph |
| --- | --- | --- |
| `query_decomposition` | one intent + entity | core + **`parts[]`** for sub-goals when distinct |
| `decomposition` | one plan | targets/predicates covering parts; honest if partial |
| `summary` | answer | cover each part or say what was skipped |
| `confidence` | overall | lower if any part thin or join weak |
| `policy_action` | usually `answer` | `clarify` if under-specified; not silent invent |
| `wish_i_knew` / `data_gaps` | optional | use when a part failed for schema/data/index |

---

## BP:10 — What to put in the pack later (implementation note)

| Surface | Content | Size discipline |
| --- | --- | --- |
| **CORE Playbook** (~150–250 words) | field→verb + recipes A–D + multi-part 5-line law | Prefer this over longer verb essays |
| **Mode overlay** | 3–5 prefer/don’t bullets | open: sample-then-expand; analytics: tight joins |
| **Verb KEY lines** | keep short; recipes live once in Playbook | base-5.3 already heavy — diet when Playbook lands |
| **company_context** | tenant people/places/things + default recipe | inject, not CORE |
| **Hot Path / books** | empiric winning pipelines per scope | not contract hash |

Suggested next content train: **Playbook in CORE + light verb description diet** (clarity without another +8 KB surprise).

---

## BP:11 — Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Treat multi-paragraph as “must use open mode” | Conflates exploration bias with task decomposition |
| One giant `find` with invented cross-type `where` | Not how overlay FKs work |
| FTS field in `find where` | Empty results; use `search` |
| Rank with `direction` | Wrong API; use `asc` + `field:` |
| Rediscover via `describe` when inject green | Waste round; inject is authoritative |
| Multi-round thrash of the same pipeline | Adjust path or clarify |
| Summary invents the join | Evidence-only Layer A |
| Unbounded traverse on open “because exploration” | Sample then expand; hard step caps still apply |
| “Those cities” follow-up answered with global search only | Multi-turn restrictor ignored (**BP:4**) |
| N× `find where city=` for large prior sets | Prefer one new filter + intersect; respect fan-out / step caps |

---

## BP:12 — Quick reference card

```text
SINGLE:  class field → verb → recipe BP:5A–H → terminate     (BP:1–BP:3)
MULTI:   split parts[] → each part a recipe → set/hop → one summary  (BP:6)
FOLLOW:  prior Zeus set ("those/listed") → reuse → constrain      (BP:4)
OPEN:    same recipes, looser HOP — not “multi-ask mode”          (BP:7)
JOIN:    FK / walk_path / traverse                                (BP:8)
COMBINE: set on id bags
SIMILAR: search hybrid/vector
RANK:    order by field:X asc:false                               (BP:5C)
STOP:    evidence-only Layer A                                    (BP:5H, BP:9)
EMPTY:   adjust class → verb → path; clarify / wish_i_knew        (BP:13)
STREAK:  ≥2 same-topic empties → inventory facet + MUST wish_i_knew (BP:13)
VIRTUAL: list via host fields (Business.city) not find City only  (BP:14)
```

---

## BP:13 — Empty / thin result recovery

When a step returns **0 rows** (or only `missing: true` stubs):

```text
1. Re-check field class (BP:2) — was this text_fts in find.where?
2. One alternate path (search vs find; drop one where key; broaden limit once).
3. Do not invent rows; summary may say none found; confidence down.
4. wish_i_knew / data_gaps when schema/data/index is the gap.
5. Do not thrash the same pipeline (BP:3).
```

### Progressive same-topic empty (ops signal)

When the **user stays on one theme** (same entity family + facet: amenity, market, …) and you get **≥2 tool-backed empties** — especially if they **relax constraints** (“anyplace”, “any X”) — that is **not** three quiet zeros. Something is missing (vocabulary, path, or data).

```text
SAME_TOPIC_EMPTY_STREAK (≥2):
  G1: 0 + keys tried; sample host fields for known facet values when possible
      (e.g. Listing.amenities[*] — not only empty find on Amenity)
  G2: MUST emit wish_i_knew (≥1 item, max 3) — inventory/path/samples *I* lacked
  If inventory truly empty → data_gaps kind:data|schema (+ blocked_answer)
  NEVER high confidence + title-only summary with empty G2 on streak
```

Single under-specified clarify stays `kind: message`. Different topic resets the streak. One honest 0 that already returns a full facet list in summary may leave `wish_i_knew: []`.

See [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) §3.3.1.

Keep this short in CORE; traffic-specific “missing host projection” mining → **OPT:32**.

---

## BP:14 — Virtual entity types (scalar_ent pivots)

Some MINI-SCHEMA types exist only as **pivots** on a host (e.g. `Business.city → City` with **City fields: 0**).  
**Day-one rule:** list values via the **host** (`find/project Business` fields `city` / `state`), not only `find entity_type:City` (often empty until entities materialize).

| Prefer | Avoid |
| --- | --- |
| `find Business` → `project city` (distinct in summary) | Assume `find City` always inventories cities |
| Filter `where.city` on Business | Treat City as a full document type with body fields |

Verbose inventory / Hot Path for virtual types → **OPT:31**.

---

## Doc ownership

| Doc | Role |
| --- | --- |
| **This file** | Day-one playbook SoT · cite **`BP:N`** |
| [OPTIMIZATION.md](OPTIMIZATION.md) | Traffic sharpen · cite **`OPT:N`** · multi-turn CORE **OPT:4** · verbose recipes **OPT:29+** |
| [MODE.md](MODE.md) | What each mode is for |
| [ROADMAP.md](ROADMAP.md) | When Playbook / multi-turn enters a BASE pack |
| [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) | Client bags when one pipeline is not enough |
| Pack CORE | Short LLM-facing excerpt of **BP:1–BP:5** (+ thin **BP:4**, **BP:6**) |

*When Playbook is copied into CORE, keep this doc as the long form; cite `BP:N` in stamps (`guidance.playbook_refs: ["BP:4","BP:5A"]`). Do not grow system prompt to full BEST_PRACTICES length.*
