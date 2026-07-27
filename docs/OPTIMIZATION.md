# Fine-tuning & end-goal optimization (Pachinko → named rails)

> **Doc status** · last reviewed **2026-07-27** · production pin **base-1** · candidate pack **base-6** (content; wire still base-5) · version matrix: [COMPAT.md](../COMPAT.md)  
> **Citation prefix:** `OPT:N` (stable IDs for Prompt Helper / chat_request refs — e.g. `see OPT:4`, `see OPT:14`)  
> **Consumers:** humans (product, Hot Path, Funnel) **and Zeus Hub Prompt Helper** — Helper may load this file, attach verbose cards by fingerprint, insert into drafts/stamps, and cite **`OPT:N`** in `chat_request` / Display Pad / board-release notes. Prefer **OPT:29+** only when the pattern matches (not every turn).

**Audience:** product, catalog authors, Workbench / Hot Path operators, Helios Funnel, **Prompt Helper**  
**Not:** day-one general retrieval playbook — that is [BEST_PRACTICES.md](BEST_PRACTICES.md) (`BP:N`)  
**Companion diagram:** [../images/zeus-pachinko-shaping.svg](../images/zeus-pachinko-shaping.svg)  
**Related:** [ROADMAP.md](ROADMAP.md) · [HELIOS_WISHLIST](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) · [HINTS.md](HINTS.md) · [ZE-267](https://kotenai.atlassian.net/browse/ZE-267)

---

## Stage map (how this doc is designed)

```text
STAGE DAY-ONE     BEST_PRACTICES.md   BP:0…BP:12   spit tests · gold · every new scope
STAGE TRAFFIC     THIS FILE           OPT:N        hundreds→10k · Hot Path · Funnel · rails
```

| | [BEST_PRACTICES.md](BEST_PRACTICES.md) | **This doc** |
| --- | --- | --- |
| **Traffic** | First A/B spit tests, gold books | **Hundreds → 10k+ chats**, Hot Path, Funnel |
| **Role** | Stable playbook floor (`BP:N`) | **Sharpen** CORE / `hints.*` / **rails** (`OPT:N`) |
| **Mouth** | Keep wide | Keep wide — add **rails**, don’t shrink questions |

```text
Best practices  =  how every ball should bounce on day one
Optimization    =  after rain, angle the pins + bolt rails for the busy paths
```

### Citation index (Prompt Helper / chat_request)

Use **`OPT:N`** in stamps, Display Pad, Helper actions, and contracted notes. **Never renumber** existing ids (append only).

| ID | Title | Stage |
| --- | --- | --- |
| **OPT:0** | Thesis — wide mouth → rails | traffic |
| **OPT:1** | Pachinko picture + stages | traffic |
| **OPT:2** | What is a `named_query` | traffic |
| **OPT:3** | Relationship to best practices | traffic |
| **OPT:4** | Multi-turn reuse — CORE Option A | traffic / CORE |
| **OPT:5** | Lifecycle rain → mine → rail → order | traffic |
| **OPT:6** | Fast-pass vs multi-turn AI cost | traffic |
| **OPT:7** | Optimization portfolio ladder | traffic |
| **OPT:8** | Priority if you only build a few | traffic |
| **OPT:9** | Rail types (SQL / pipeline / hybrid / …) | traffic |
| **OPT:10** | Intent → rail router | traffic |
| **OPT:11** | Board release (contract packaging) | traffic |
| **OPT:12** | Rail SLOs + demote | traffic |
| **OPT:13** | Multi-intent compiler | traffic |
| **OPT:14** | Partial rails / mid-board chutes | traffic |
| **OPT:15** | Parameter dictionaries / normalization | traffic |
| **OPT:16** | Seasonal / campaign rail packs | traffic |
| **OPT:17** | Result + prompt-prefix cache | traffic |
| **OPT:18** | Mode-specific board density | traffic |
| **OPT:19** | Confidence-gated ORDER + HITL | traffic |
| **OPT:20** | Action rails two-phase ORDER | traffic |
| **OPT:21** | Negative rails | traffic |
| **OPT:22** | Cross-scope rail patterns | traffic |
| **OPT:23** | Skinny stamped tool sets | traffic |
| **OPT:24** | Helios Funnel alignment | traffic |
| **OPT:25** | What this is *not* | traffic |
| **OPT:26** | Operator checklist | traffic |
| **OPT:27** | Implementation horizons / ZE-267 | traffic |
| **OPT:28** | One-pager for talks | traffic |
| **OPT:29** | Follow-up ∩ prior set (verbose recipe) | traffic · high-value rare |
| **OPT:30** | Dual-bag without intersect (anti-pattern) | traffic · high-value rare |
| **OPT:31** | Virtual entity types under traffic | traffic · high-value rare |
| **OPT:32** | Project fields vs missing stubs | traffic · high-value rare |
| **OPT:33** | Detective “pass” ≠ multi-turn success | traffic · measure |
| **OPT:34** | Soft `hints.multipart` pastes (verbose) | traffic · Client inject |
| **OPT:35** | Why verbose OPT cards are worth tokens | traffic · meta |

**Cross-doc:** day-one multi-turn short law = **BP:4**; longer CORE under traffic = **OPT:4**; worked multi-turn recipe = **OPT:29**.

### Why OPT cards can be longer than BP cards

Best-practice text is in **every** system prompt / gold path — keep it short.  
Optimization text is for **Hot Path / Helper / custom stamps** that apply on a **two-digit %** (or less) of turns — but when the user’s ask matches that pattern, the chance the long recipe helps is often **~1 in 3–10**. Paying more tokens on those paths is rational:

| Surface | Length | When loaded |
| --- | --- | --- |
| **BP:*** | Short law | Always / day-one CORE |
| **OPT:0–28** | Medium | Operator + Helper portfolio |
| **OPT:29+** | **Verbose, specific** | Only when Helper/Hot Path selects the card (or custom stamp for that pattern) |

---

## Stage: Traffic → sharpen → rails

## OPT:0 — One-sentence thesis

Zeus starts as a **wide-mouth** natural-language board (many pins = many tool hops).  
Over time you **shape the pins into rails**: the top question patterns become **`named_query`** rails — Couchbase **SQL++ PREPARED** statements (and related governed paths) so traffic reaches **order / action** in **1–2 hops**, not 8–12 LLM↔Zeus rounds.

This is an **end-goal optimization**, not the default day-one best practice for every ad-hoc ask.

```text
Day one:     rain of questions → multi-hop AI + Zeus verbs (pachinko pins)
Mature:      rain of questions → few named rails → ORDER / book / dispatch
Seasonal:    new traffic → mine misses → new rails (green in the diagram)
```

---

## OPT:1 — The Pachinko picture

![Shaping the Pachinko pins over time](../images/zeus-pachinko-shaping.svg)

| Metaphor | Meaning |
| --- | --- |
| **Ball** | A question / intent dropped across a **wide mouth** (typos, synonyms, angles) |
| **Pin** | A tool hop / chat round (find, search, traverse, pipeline step, …) |
| **Rail** | A **named_query** (prepared path) that channels traffic |
| **ORDER (center slot)** | Goal completion: answer bag ready **or** governed action (book car, place order, …) |
| **Fell out** | No answer / refuse / timeout / permission / capability gap — next to mine |

### Stages (from the diagram)

| Stage | Board | Hops (illustrative) | What you do |
| --- | --- | --- | --- |
| **1 · Day one** | Full pin grid, no rails | 8–12 · many miss center | World model + verbs + BEST_PRACTICES playbook; observe traffic |
| **2 · After traffic** | First angled rails | 4–6 · busy paths land | Mine Hot Paths → first `named_query` rails |
| **3 · Shaped funnel** | Rails from front/middle/sides | **1–2** · rare miss | Top 5–10 patterns are fast-pass; seasonal green rails for new demand |

**Shape the funnel — don’t shrink the box.**  
That is the opposite of Path B2 (restrict chat so only form-shaped questions remain). See [ENTITY foundation](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) Path B2 and Zeus Funnel motion docs.

---

## OPT:2 — What is a `named_query`?

**A:** In Zeus, a **named query** is an operator-defined, versioned, **Couchbase SQL++ PREPARED** statement stored per scope (e.g. `zeus_config::named_query:<name>`), invocable as a **governed tool/path** without writing new Go for every pattern.

| Property | Why it matters |
| --- | --- |
| **PREPARED** | Plan reuse, stable shape, predictable cost vs ad-hoc multi-hop AI planning |
| **Named** | Stable id for Hot Path, Helios Funnel (`path.named_query` / `rail_id`), A/B, audit |
| **Scoped** | Same tenancy / mode boundaries as the rest of Zeus |
| **Versioned / archive** | Safe evolve rails; rollback |
| **Parameterized** | User/entity slots (`$brewery_id`, `$limit`) — not free SQL from the model |

**Not the same as:**

| Concept | Difference |
| --- | --- |
| Ad-hoc `find` / `search` / `pipeline` | Flexible day-one exploration; more hops |
| Soft `hints.hot_path` | Prose bias toward a verb sequence — still multi-tool unless a rail exists |
| Hard `rules{}` | Policy law, not data path |
| Path B2 canned FAQ only | Shrinks the mouth; Zeus keeps the **wide mouth** and adds **rails** |

Mental model: **Candy Land chute / shoots-and-ladders / wormhole / fast-pass lane** from “I know this ask” → prepared execution → order/action.

---

## OPT:3 — Relationship to general best practices

| Layer | Doc | Role |
| --- | --- | --- |
| **General playbook** | [BEST_PRACTICES.md](BEST_PRACTICES.md) `BP:N` | Day one: field→verb, **BP:5A–H**, multi-intent **BP:6**, multi-turn **BP:4** |
| **Soft steer** | [HINTS.md](HINTS.md) · ROADMAP § HINTS | Per-turn bias without re-stamp |
| **Sharpen under traffic** | **This doc** **OPT:4+** | CORE / hints / books from hundreds–10k chats |
| **End-goal rails** | **OPT:2**, **OPT:5–OPT:23** | Top patterns → **named_query** / pipeline rails |

```text
BEST_PRACTICES (BP:*)  →  how to play the pin grid safely (day one + forever floor)
HINTS / Hot Path       →  which paths are getting hot (sharpen)
named_query (OPT:2+)   →  turn a hot path into a rail (few hops)
Funnel motion          →  measure and operate the board (Helios)
```

Do **not** replace day-one playbook with “only call named_query.”  
Do **promote** repeated winning multi-hop shapes into rails over time.

---

## OPT:4 — Multi-turn reuse (prior Zeus evidence) {#opt4--multi-turn-reuse-prior-zeus-evidence}

Day-one short law: **[BP:4](BEST_PRACTICES.md)** (Option B).  
Under real traffic, multi-turn *restrictors* (“those cities,” “from the list above”) show up as **repeat waste** in Detective: global rediscovery, parallel re-find + search without intersection, prose that claims a filter tools never applied.

**Prompt Helper:** when inserting multi-turn CORE under traffic, cite **`OPT:4`** (and still link day-one **`BP:4`**).

### Why this is an optimization concern

| Signal (Hot Path / Detective) | Cost |
| --- | --- |
| Follow-up re-runs full `find Business limit N` after cities already projected | Extra GSI + project; often **wrong set** vs prior turn |
| Global `search "pizza"` while summary says “among listed cities” | Wrong answer shape; low trust |
| N× `find where city=` for large prior sets | Fan-out / step caps; slow wall |

**Mine** these as path fingerprints (e.g. `followup_prior_set+fts_category`) and **sharpen** CORE / soft `hints.multipart` / books — then, if stable, a **rail**.

### CORE candidate (Option A — longer house style) · cite `OPT:4`

Promote into a **content train** CORE block (or stamped custom) when Hot Path shows multi-turn waste — not as jailbreak law:

```text
5) Multi-turn reuse (when evidence is in context)
- If the user refers to prior answers ("those", "the cities listed", "above", "from the last result"),
  prefer reusing cities / ids / fields already returned by Zeus tools in this conversation
  over rediscovering the same set with a new broad find/search.
- Intersect new filters (e.g. pizza / category) with that prior set when possible;
  do not answer a restricted follow-up with an unconstrained global search.
- Within a pipeline, keep binding prior step ids as @step.ids.
- If prior rows are not available in context, re-fetch the smallest set needed or clarify —
  do not invent the prior list.
```

| Prefer under traffic | Avoid |
| --- | --- |
| Prior set ∩ new predicate (one FTS/find + filter) | Parallel “all businesses” + “global pizza” with no join |
| Soft `hints.multipart` / last-result inject (ZC-WISH-040) | Hoping the model remembers 50 cities from summary prose alone |
| Book / gold: “cities then pizza among them” | Gold that only tests single-turn pizza |

**Hub note:** Zeus results lightbox is **operator UI**; the model only reuses what is still in **messages / tool results**. Client multi-round memory or `hints.prior_result` is required for reliable binding — [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) · [HINTS.md](HINTS.md).

### Ladder placement

```text
BP:4 short multi-turn  →  OPT:4 CORE Option A
  →  soft hints / prior_result inject  →  Hot Path book
  →  named_query or pipeline template (OPT:2 / OPT:9) if the pattern dominates
```

---

## OPT:5 — Lifecycle: rain → mine → rail → order

### Observe (wide mouth stays open)

- Chat + Detective: rounds, tool sequences, zero-rows, timeouts.  
- Helios **Funnel** motion: drop-off, stages, conversion (see HEL-WISH-014 path stage).  
- Workbench **Hot Paths / Path Finder**: multi-hop shapes for the scope.

Balls still drop across the **whole mouth** — natural language is not reduced to five form fields.

### Mine (top 5–10 ideas / question patterns)

Cluster traffic into **intents / path shapes**, not raw user strings:

| Signal | Example pattern id |
| --- | --- |
| QD intent + entity_type | `List/Beer+fts_description` |
| Tool fingerprint | `search→order→project` |
| Join shape | `Brewery→Beer inverse_fk` |
| Terminal action | `book_vehicle`, `place_order` |

Target **5–10 rails per mature scope** first — enough coverage without catalog explosion. Seasonal demand adds rails (green path in the diagram), it does not require rewriting CORE every week.

### Shape (publish a rail)

1. Author SQL++ (or promote a proven pipeline shape) as **`named_query:<name>`** with parameters + validation.  
2. Expose to the agent as a **callable verb/path** (catalog / mode allow-list / Workbench draft rail).  
3. Teach the model **when** to prefer the rail:
   - soft: `hints.hot_path` / `hints.path` (“prefer named_query fruit_beers when …”)  
   - harder product: Client router or tool_choice bias when classifier confidence high  
4. Keep general verbs for **misses** and novel asks (side bins → next to mine).

### Prove (A/B the board)

- A/B Bench: rounds-to-order, success rate, named_query hit rate, fall-out class.  
- Promote rails that reduce hops **without** raising wrong-answer rate.  
- Retire or version rails that go cold.

### Act (order is not only “rows”)

Center slot **ORDER** can mean:

| Outcome | Example |
| --- | --- |
| **Answer** | Ranked rows + Layer A terminate |
| **Governed side-effect** | Book a car, place order, open claim, dispatch tech |
| **Publish rail** | Operator action: ship a new named_query |

Action rails need the same discipline as SQL rails: parameters, authz, audit, idempotency — not free agent invention of mutations.

---

## OPT:6 — Fast-pass vs multi-turn AI (cost picture)

| Path | Typical cost | When |
| --- | --- | --- |
| Full pin grid (many tool rounds) | High AI ms + planning risk | Novel, multi-intent, exploratory |
| Soft hot_path hint only | Still multi-tool, better first guess | Early shaping |
| **named_query rail** | Low planning; PREPARED exec | Top patterns, stable schema |
| Action rail | Lowest UX friction if intent clear | Funnel bottom (book / order / …) |

End state for a mature deployment:

```text
most traffic  →  rail (1–2 hops)  →  order/action
tail traffic  →  general playbook (pins)  →  mine or fall-out
```

Helios Funnel metrics should eventually show **% traffic on named rails** and **avg hops** falling as the board shapes (not only “fewer user questions allowed”).

---

## OPT:7 — Optimization portfolio (ladder)

`named_query` rails are the **headline**, but they sit on a **ladder** of optimizations that all “shape the board” without shrinking the mouth. Day-one docs cover **BP:*** + ladder steps 1–2. [ZE-267](https://kotenai.atlassian.net/browse/ZE-267) is mostly **3→6→contract**. The rest is product/engine portfolio.

```text
cheapest / always-on
  1  Inject quality (brief, mini-schema, ex: samples)
  2  Playbook + verb clarity (day-one pins)     ← BP:* / base-5.3+
  2b Multi-turn reuse (prior Zeus set)         ← BP:4 short · OPT:4 CORE
  3  Soft hints / hot_path (bias, no re-stamp) ← HINTS · ZC-WISH-040
  4  Contracted catalog delta (custom stamp / mode pack)
  5  Named pipeline templates (multi-verb rail)  ← OPT:9
  6  named_query PREPARED (SQL++ fast-pass)      ← OPT:2
  7  Intent→rail router (pre-LLM or light classifier) ← OPT:10
  8  Action rails (book / order / dispatch)      ← OPT:20
  9  Materialized edges / walk_path / indexes (engine)
 10  Cache / prompt-cache / result cache         ← OPT:17
 11  Skinny stamped tool sets (empiric A/B)      ← OPT:23
expensive / later
```

**Filter for any new idea:** does it **add a rail**, **shorten pins**, or **measure shaping** — while keeping the **wide mouth**?  
If it only **forbids questions**, it is Path B2, not Zeus optimization.

### OPT:8 — Priority if you only build a few

| Pri | Idea | Why |
| --- | --- | --- |
| **P0** | SQL `named_query` rails (§§1–5) | Real hop reduction; PREPARED cost |
| **P0** | Pipeline / composite rails (§6.2) | Many hot paths aren’t one SELECT |
| **P0** | Intent→rail router (§6.3) | Skip planning, not only speed SQL |
| **P1** | Board release: stamp + rails + hints (§6.4) | “Contracted in” packaging |
| **P1** | Rail SLOs + demote (§6.5) | Fast-pass must not become fast-wrong |
| **P2** | Multi-intent compiler (§6.6) | Paragraph traffic |
| **P2** | Partial rails + value normalization (§6.7–6.8) | Mid-board chutes; zero-row loops |
| **P2** | Seasonal rail packs (§6.9) | Green rails in the diagram |
| **P3** | Result / prompt cache (§6.10) | Orthogonal speed |
| **P3** | Mode board density (§6.11) | open vs analytics rail policy |
| **P3** | HITL approve queue + action two-phase ORDER (§6.12–6.13) | Operator time; book-car Funnel |

---

## OPT:9 — Rail types (not only SQL++)

Some hot paths are `search→order→project` with no single SQL that feels natural. Treat **rail** as a product type:

| Rail type | What it is | Example |
| --- | --- | --- |
| **SQL rail** | `named_query` PREPARED | `named_query:top_abv_beer` |
| **Pipeline / composite rail** | Frozen multi-verb steps + param slots; one agent invocation | `search→order field:abv→project` template |
| **Hybrid rail** | NQ for ids → fixed project / enrich | PREPARED seeds + cheap shape |
| **Partial rail** | Only the expensive middle or seed resolution | “resolve Pliny → brewery_id” then playbook |
| **Action rail** | Governed side-effect after answer | book / order / dispatch (§4.5, §6.13) |

Same Pachinko diagram; different **rail material**. ZE-267 should draft SQL rails first, then composite rails when Hot Paths are multi-verb.

---

## OPT:10 — Intent → rail router (pre- or co-LLM)

Before a full 13-verb think, a **cheap** step:

```text
user / embedding / small classifier
  → high confidence: call named_query | force tool_choice on rail
  → low confidence: full pin grid (playbook)
```

That is the real **wormhole**: not only a faster query, but **skipping planning**.

| Metric | Meaning |
| --- | --- |
| `% first-tool = named_query` | Router + teach working |
| Avg AI rounds when rail hit vs miss | Board shaping |
| Wrong-rail rate | Router / rail quality |

Client or Zeus can own the router; Prompt Helper proposes **when** strings and confidence thresholds for contract.

---

## OPT:11 — Board release (contract as packaging)

Helper output is eventually **contracted in**. A **board release** is one deployable unit:

| Artifact | What it binds |
| --- | --- |
| Custom / stamped chat_request | Playbook bias, soft teach for rails, optional skinny verbs |
| `named_query` set (versioned) | PREPARED + params |
| Default `hints.hot_path` / `hints.path` | Tenant hot list without re-stamp thrash on every experiment |
| Optional deployment_id / ruleset | Helios A/B of “shaped board” vs day-one grid |

A/B compares **board releases**, not only model temperature.  
Does **not** invent production `contract_hash` inside Helper — stamp/publish stays Hub workflow.

---

## OPT:12 — Rail quality SLOs + demote

Treat each rail like a product API:

| SLO | Example |
| --- | --- |
| p95 latency | PREPARED exec budget |
| Empty rate | Param / data drift |
| Error rate | Statement / authz |
| Wrong-answer samples | Spot books / human review |

**Auto demote** (or archive) if SLO breaks → balls return to pin grid for that pattern.  
Keeps “fast-pass” from becoming “fast wrong.” Helios / admin should show rail health next to hit rate.

---

## OPT:13 — Multi-intent compiler

Paragraph multi-ask is playbook ([BEST_PRACTICES §3](BEST_PRACTICES.md)); **optimization** is a compiler:

```text
paragraph → parts[]
  → independent parts: parallel NQs / recipes
  → dependent parts: ordered pipeline
  → combine: set union/intersect when two bags
  → budget: if >N parts → clarify or Client multi-round
```

Output can be a **single multi-rail plan** the model only fills parameters for — fewer free-form tool invents.

Optional soft inject: `hints.multipart` (ROADMAP § HINTS).

---

## OPT:14 — Partial rails / mid-board chutes

Not every pattern needs mouth→ORDER in one shot:

| Partial rail | Effect |
| --- | --- |
| Seed resolution only | “resolve entity X → id” then general playbook |
| Expensive middle only | Big FTS/hybrid as NQ; AI only terminates |
| Rank tail only | Candidate bag in → `order`/`project` template |

Reduces average hops without requiring a full funnel win on day two.

---

## OPT:15 — Parameter dictionaries / value normalization

`ex:` trailers teach conventions; optimization is **automatic normalize**:

- user “UK” → `United Kingdom` via map or NQ param coercion  
- style / city synonyms  
- **Fail closed**: unknown → fall back to FTS pin path (not invent)

Cuts zero-row loops that look like “bad AI” but are **value shape** problems.

---

## OPT:16 — Seasonal / campaign rail packs

Diagram **green rail** = seasonal demand:

- versioned **pack of rails** per season/campaign  
- auto-expire or archive  
- Helios `deployment_id` / ruleset = which rail pack is live  

Optimization is not only “more rails forever” — it is **lifecycle** of rails (promote, expire, replace).

---

## OPT:17 — Result cache + prompt-prefix cache

Even without a new NQ:

| Cache | Effect |
| --- | --- |
| Brief / mini-schema inject | Already “free orientation” vs `describe` |
| NQ result by param hash (TTL) | Identical balls → zero re-exec |
| Multi-turn same NQ params | Don’t re-run |
| Provider prompt-prefix cache | Stable catalog+company+rules+rail list; dirty user/brief only (ROADMAP base-8) |

Orthogonal to named_query but same goal: less wall time and less AI ms.

---

## OPT:18 — Mode-specific board density

Same Pachinko; different **rail density** and fall-out policy (see DESIGN §14.7):

| Mode | Optimization flavor |
| --- | --- |
| **analytics** | NQ for top BI patterns; tight joins; multi-intent OK |
| **open** | More exploratory pins early; fewer premature NQs; sample-then-expand; accept noise |
| **fraud** | NQ for known typologies + keep weak-signal hops open |
| **code** | NQ for “callers of X”, “impls of Y”; deeper hops when pins remain |
| **research** | Citation / backlink rails + semantic when needed |
| **tenant / regulated** | Fewer speculative pins; NQ must be audit-friendly; scope wall hard |
| **private** | Local graph rails; no fake corpus stats |
| **auto** | Almost no permanent rails until named mode commits |

Do **not** switch to `open` only because the user wrote a multi-ask paragraph — that is multi-intent compiler / playbook, not mode.

---

## OPT:19 — Confidence-gated ORDER + human-in-the-loop

| Gate | Behavior |
| --- | --- |
| High intent + rail hit | Terminate faster; lighter soft Layer A |
| Low confidence | More pins, or `policy_action: clarify` |
| Operator HITL | Helper proposes rail → **one-click approve** → PREPARE + optional stamp candidate |

Optimizes **when to stop thinking** and **operator time**, not only fetch latency. Fits ZE-267 Slice A/B.

---

## OPT:20 — Action rails as two-phase ORDER

“Book a car” is rarely one free agent hop:

```text
1) Answer rail  — candidates (availability, price, constraints)
2) Action rail  — book with idempotency key, policy table, optional human confirm
```

Funnel bottom can still be **fewer hops than free planning** even if it is two governed steps.  
Authz, audit, idempotency required — same discipline as SQL rails.

---

## OPT:21 — Negative rails / “do not go there”

Mine **fall-out** and **bad paths**:

| Source | Publish as |
| --- | --- |
| Always-empty FTS shapes | `hints.avoid_patterns` or books |
| Timeout patterns | budget / timeout_ms defaults |
| Mode / permission denials | capability gap ticket, not a rail |

Side bins feed the **next green rail** *or* a blocked chute (schema/index/product gap). Negative teach is soft unless stamped policy.

---

## OPT:22 — Cross-scope rail patterns (careful)

Tenant-safe **templates**: same NQ shape, different scope binding (portability / D2P spirit).  
Only where boundary model allows — never one global PREPARE that crosses tenant walls.

---

## OPT:23 — Skinny stamped tool sets (empiric)

After Hot Path shows 3 of 13 verbs unused:

- **New stamp / A/B arm** with fewer tools on the wire (not mid-session strip under enforcement)  
- General pin grid remains for admin / workbench / full packs  

Complements rails: fewer pins **and** more rails on the product board.

---

## OPT:24 — Helios Funnel alignment

| Helios concern | Optimization story |
| --- | --- |
| Funnel motion | Goal-directed path to action; wide mouth in, bounded outcome out |
| `path.stage` / rail_id / named_query (HEL-WISH-014, path scalars) | Report which balls rode which rail |
| Drop-off | Side bins: no answer, refuse, error, permission |
| Deployment / ruleset | A/B “shaped board” vs day-one pin grid; seasonal rail packs |
| Tool fingerprint (HEL-WISH-021) | Mine candidates for the next rail |
| Named-query hit rate / avg hops | Board maturity KPIs (§5, §6.5) |

Cheap Zeus/Client path metrics beat forcing the model to emit funnel stages every turn ([HELIOS cost law](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)).

---

## OPT:25 — What this is *not*

| Anti-goal | Why |
| --- | --- |
| Day-one “only named_query” | No rails yet; mouth would empty into fall-out |
| Path B2: shrink chat to five canned questions | Destroys wide mouth; freezes product |
| Unbounded agent SQL | PREPARED + validate + scope RBAC only |
| Replacing mini-schema / world model | Rails sit **on top of** overlay data, not instead of it |
| Runtime strip of general verbs under same stamp | Novel balls still need pins; skinny catalogs are separate stamps |
| Soft hints as only policy | Jailbreak / tenancy stay hard rules + engine mode |
| Forever-growing rail list without SLOs | Stale rails → fast wrong; demote/archive (§6.5) |
| Switch mode to `open` for multi-paragraph asks | Multi-intent compiler / playbook — not exploration bias |

---

## OPT:26 — Operator checklist (close the loop)

0. **Multi-turn:** gold/book **OPT:29**; measure **OPT:33** metrics (restrictor miss, dual-bag, virtual empty, stub-heavy).  
0b. **Helper:** attach verbose cards **OPT:29–34** by fingerprint only — not into every CORE (**OPT:35**).

1. **Observe** Funnel + Hot Paths + Detective slow/error packs.  
2. **Triage** each fall-out: prompt fix vs new rail vs capability/schema gap.  
3. **Draft rail** (Workbench Hot Paths → named_query and/or pipeline template).  
4. **Wire teach** (`hints.hot_path` and/or catalog verb entry; optional router rule).  
5. **A/B** board release (rounds, conversion, rail hit rate, wrong-rail rate).  
6. **Publish** versioned named_query; archive losers; enforce rail SLOs.  
7. **Season** — new product season ⇒ new green rails, not a full BASE rewrite.  
8. **Contract** — stamp custom / pin path so Helper output is durable (ZE-267 Slice B).

---

## OPT:27 — Implementation horizons (where work lives)

| Horizon | Work | Owner |
| --- | --- | --- |
| **Now** | BEST_PRACTICES + verb clarity + world model (pin grid skills) | chat_request packs |
| **Near** | Hot Path mine → draft rail → hints.hot_path | Workbench / CR-26 residual / base-6 hints |
| **Product (ZE-267)** | Prompt Helper propose → draft NQ → **contract** path; Pachinko framing in Display Pad | Hub Prompt Helper |
| **Product** | named_query admin + execute + metrics (OpenAPI exists) | Zeus targets + Hub |
| **Router / composite rails** | Intent→rail; pipeline templates | Zeus + Client + Helper |
| **Funnel ops** | path.stage, rail_id, hit rate, rail SLOs on report | Zeus + Helios |
| **Action rails** | book/order/dispatch two-phase ORDER | Product + Client policy |
| **Cache / prompt-cache** | Result TTL; stable prefix zones | Zeus / Client / provider |

ROADMAP home: **named rails + portfolio** under Funnel / Hot Path / base-6 hints / base-7 Workbench / [ZE-267](https://kotenai.atlassian.net/browse/ZE-267) — not a base-5.3 day-one pack requirement.

### ZE-267 slice mapping (Helper)

| ZE-267 slice | Portfolio items |
| --- | --- |
| **A Propose** | Hot Path rank, rail candidates, Pachinko framing |
| **B Contract** | Board release (stamp + rails + hints); no invented contract_hash |
| **C Prove** | A/B hops, hit rate, fall-out; rail SLOs |
| **D Action** | Two-phase ORDER / book-car style rails |

---

## OPT:28 — One-pager for talks

> Questions fall into Zeus like balls in a Pachinko machine. Day one, every pin is a tool hop — slow, messy, but the mouth is wide. Watch the traffic, mine the top paths, and bolt on **named_query rails** (SQL++ PREPARED fast lanes) — plus pipeline rails, routers, and seasonal packs as the board matures. Most balls reach **order** in one or two hops — including real actions like booking a car — while rare misses still use the open playbook and become the next rail. **Shape the funnel; don’t shrink the box.**

---

## Stage: High-value rare patterns (verbose cards)

These cards are intentionally **long**. Load them when Hot Path / Helper / books match the fingerprint — not into every BASE CORE.

---

## OPT:29 — Follow-up ∩ prior set (verbose recipe)

**Fingerprint (mine this):**  
User turn 1 lists a **set** (cities, ids, names) via Zeus tools.  
User turn 2 uses **restrictor language**: *those / the ones you listed / among them / out of the cities above / from that list* **plus** a new predicate (pizza, open now, top by stars, category FTS).

**Day-one cite:** **BP:4**. **CORE long form under traffic:** **OPT:4**. **This card:** full plan the model should execute.

### Intent translation

| User said | Logical plan |
| --- | --- |
| “Which of those cities have pizza?” | `cities_prior ∩ cities(pizza_businesses)` |
| “Pizza places in the cities you listed” | `pizza_businesses` filtered to `city ∈ cities_prior` |
| “Top rated among those” | prior bag → order → project (no global rediscovery) |

### Preferred tool plan (one pipeline when possible)

```text
// 1) PRIOR SET — reuse if still in messages/tool results; else re-fetch SMALL
//    Prefer prior project rows (city values / ids). Do NOT re-find limit 200 “all businesses”
//    unless prior evidence is gone from context.

// 2) NEW PREDICATE — class the field (BP:2)
//    pizza / cuisine language → search Business strategy:fts query_text:"pizza"
//    (categories is text_fts — never find where categories=…)

// 3) SHAPE
//    project name, city, state, categories, stars, …

// 4) INTERSECT (model-side or set if you have two id bags of the SAME entity_type)
//    Keep only rows where city ∈ cities_prior (string normalize: trim, case)
//    If prior was City ids and Business.city is scalar surface form, match surface strings
//    from prior project — not invent City entity hosts.

// 5) TERMINATE
//    summary: which prior cities hit / miss; list pizza places with city
//    query_decomposition.parts[]: (List prior set) + (Find pizza) + (Intersect)
//    confidence: med if prior set incomplete or many missing stubs
//    Do NOT claim “among listed cities” unless step 4 ran.
```

### Worked sketch (Yelp-style)

```text
Turn 1: “What cities have listings?”
  → find/project Business fields [city] (or whatever produced the Zeus results table)
  → prior_cities = distinct city strings in tool results / history

Turn 2: “Out of the cities listed, which have pizza?”
  GOOD:
    search Business fts "pizza" limit 50–100
    → project city, name, categories, stars
    → filter rows to city ∈ prior_cities
    → summary names only cities that appear in both

  BAD (seen in Detective):
    search pizza global only → pretend multi-turn
    OR parallel find all Business + search pizza with no join (OPT:30)
    OR 50× find where city= each city (fan-out / step caps)
```

### When prior rows are NOT in context

Hub “Zeus results” lightbox is **not** in the model prompt. If history only has a one-line summary:

1. Re-run the **smallest** prior harvest (e.g. project city again with modest limit), **or**  
2. `policy_action: clarify` / ask which cities, **or**  
3. Client inject `hints.prior_result` / keep tool JSON in multi-round messages (**OPT:34**, MULTI_ROUND_CLIENT).

Never invent the prior city list into `summary`.

### Success metrics (Hot Path)

| Metric | Goal |
| --- | --- |
| Follow-ups with restrictor language that run **global** search/find only | ↓ |
| Summaries claiming “among listed” without city filter / intersect | ↓ |
| Avg extra tool calls vs one search+project+filter | ↓ |

**Promote to rail when:** same fingerprint dominates a scope’s Hot Path (e.g. `followup_prior_geo+fts_category`).

---

## OPT:30 — Dual-bag without intersect (anti-pattern)

**Fingerprint:** one pipeline with **two independent harvests** on level 0:

```text
pizza_biz = search … "pizza"
all_biz   = find Business limit N   // “re-list cities”
// projects both bags
// NO set / NO city filter / NO join
```

**Why models do it:** QD says “filter cities for pizza” so they fetch **cities** and **pizza** in parallel and hope to reason over both bags. Prose sounds multi-turn; tools never bind the prior set.

**Cost / quality**

| Issue | Effect |
| --- | --- |
| `all_biz` ≠ turn-1 city set | Wrong restrictor (limit/order/filter differ) |
| No intersection | Pizza may be outside “listed” cities; cities bag may have no pizza signal |
| Double project | Extra ms and tokens; still fails the user ask |

**Fix:** collapse to **OPT:29** (one new predicate + intersect prior set). If you need two bags of the **same** entity_type for boolean logic, use **`set`** (BP:5F) — not narrative join.

**Helper teach string (paste-ready):**

```text
If you load two bags (e.g. all businesses + pizza hits), you MUST intersect or filter
explicitly (set on ids, or keep rows whose city/field ∈ prior set). Parallel project
without intersect is not a multi-turn answer.
```

---

## OPT:31 — Virtual entity types under traffic

**Day-one:** **BP:14**.  
**Under traffic:** operators map `Business.city → entity City` with **City fields: 0**. MINI-SCHEMA shows City + `inverse_fks`, so models love `find entity_type:City` and get **0 rows**, then invent or pivot poorly.

### Teach block (verbose — custom stamp / mode book)

```text
VIRTUAL / PIVOT TYPES (this scope may have them):
- City, State, (sometimes) category labels exist as scalar_ent on a HOST (Business).
- Host has the filterable field: Business.city [gsi] scalar_ent → City.
- City document body may be empty (fields: 0). find City often returns [] even when
  many Business.city values exist.

TO LIST CITIES WITH LISTINGS:
  find Business (return ids, broad limit) → project fields [city] (and state if needed)
  → distinct city strings in summary / next-turn memory
NOT: find City limit 100 → project name   // empty inventory common

TO FILTER BY CITY:
  find Business where { city: "<surface form from project/ex:>" }
  Normalize user "NYC" to stored surface (MINI-SCHEMA ex: samples) before equality.

TO ASK “pizza in those cities”:
  search pizza → project city → keep city ∈ prior_cities   (OPT:29)
  Optional: for a SMALL prior set (≤5), equality where.city per city is OK;
  for large sets prefer one FTS + filter, not N finds.
```

### Hot Path signals

| Signal | Likely virtual-type miss |
| --- | --- |
| `find City` / `find State` result_size 0 then global Business search | Inventory via wrong entity_type |
| Mini-schema City present + inverse_fks only | Pivot type |
| project city works; find City fails | Confirm BP:14 / OPT:31 teach |

---

## OPT:32 — Project fields vs missing stubs

**Fingerprint:** `project` with `fields: [name, city, state, …]` returns many rows with only:

```json
{ "doc_key": "file::…", "id": "file::…", "missing": true, "node_id": "file::…" }
```

mixed with rich rows that have `city` / `name`.

**Causes (engine / projection):** partial v2 hosts, wrong id kind (`file::` vs `biz:…`), not-yet-reprojected docs after entity_map change.

**Model law (when this appears in tool results):**

```text
1. Prefer rich rows for summary / next-turn prior set (city, name present).
2. Do not treat missing:true stubs as equal evidence.
3. confidence: med/low if a large fraction are stubs.
4. wish_i_knew / data_gaps when inventory is mostly unresolved hosts
   (kind: data or schema — “host not fully projected”).
5. Do not re-project the same missing ids hoping for different data without
   changing path (get include body only if id is known good).
```

**Operator path:** re-ingest / DCP zero after entity_map `re_project` (Zeus Lifecycle) — not a chat_request pin flip.

**Helper / stamp:** if Hot Path shows high `missing:true` rate on project, add a **book** case and optional CORE note pointing at re-project; UI may hide stubs (Hub Zeus results) but the **model still sees tool JSON**.

---

## OPT:33 — Detective “pass” ≠ multi-turn success

Detective **output_grade=pass** means Layer A required four + tools OK — **not**:

| Check | Who owns it |
| --- | --- |
| Honored “those / listed” restrictor | Plan quality · **OPT:29** |
| Intersected prior set | Plan · **OPT:30** |
| Used virtual type correctly | Plan · **OPT:31** |
| Summary matches tool evidence | Layer A honesty · **BP:9** |

**Measure in Hot Path / books (not only Detective pass rate):**

```text
multi_turn_restrictor_miss  = follow-up with restrictor language
                              AND no prior-set filter AND global harvest
virtual_type_empty_inventory = find pivot type → 0 AND host project would work
stub_heavy_project           = project rows missing:true > 50%
```

Gold books should include at least one **OPT:29** scenario per mature scope.

---

## OPT:34 — Soft `hints.multipart` pastes (verbose)

Hash-excluded Client inject ([HINTS.md](HINTS.md) · ZC-WISH-040). Use when CORE is full and this turn needs a **recipe**, not a new stamp.

### Example: prior city set + category FTS

```json
{
  "hints": {
    "multipart": {
      "when": "user refers to prior Zeus result set (those/listed/above) + new category/language filter",
      "prefer": "Reuse prior city/id/field values from conversation tool results. Run one search/find for the new predicate; project city (and name); keep only rows in the prior set. Do not re-find all Business just to re-list cities. Do not answer with unconstrained global search while claiming multi-turn.",
      "recipe": "prior_set → search|find(new_filter) → project → filter to prior_set → terminate with parts[]"
    },
    "path": {
      "avoid": [
        "parallel all_biz find + pizza search without intersect",
        "find City for inventory when City is scalar_ent pivot with 0 fields",
        "N equality finds for large prior city sets"
      ]
    }
  }
}
```

### Example: last-fail negative (after Detective)

```json
{
  "hints": {
    "avoid_patterns": [
      "find where on text_fts categories — use search fts",
      "order.direction — use asc boolean + by field:name",
      "repeat same pipeline after empty — change path or clarify"
    ]
  }
}
```

Keep inject size soft-capped (~1–2 KB). Jailbreak law stays in hard `rules{}`, never only here.

---

## OPT:35 — Why verbose OPT cards are worth tokens

| | BP cards | OPT:29+ cards |
| --- | --- | --- |
| **How often loaded** | Most chats / base CORE | Pattern match only |
| **Length** | Short | Specific + worked examples |
| **ROI** | Always-on correctness | When the rare ask hits, long recipe prevents a wrong global path |

**Operator rule of thumb:** if Hot Path shows a pattern on **~5–20%** of sessions, and when present the long teach would help **~1/3–1/10** of those, the **expected value** of a verbose Helper insert still beats a one-line “reuse prior results” that models ignore.

**Do not** dump OPT:29–34 into every mode CORE (token tax on the other 80–95%).  
**Do** wire Prompt Helper to attach **`OPT:N`** by fingerprint (restrictor language, virtual type, stub-heavy project, dual-bag).

---

## Doc ownership

| Doc | Role |
| --- | --- |
| **This file** | End-goal fine-tuning / Pachinko / named rails / **optimization portfolio** / **verbose rare cards OPT:29+** |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | Day-one playbook (pins) · `BP:N` |
| [ROADMAP.md](ROADMAP.md) § HINTS · sequencing | Soft hot_path inject; when rails enter product trains |
| [ZE-267](https://kotenai.atlassian.net/browse/ZE-267) | Prompt Helper → rails → contract |
| Zeus Funnel motion + OpenAPI named queries | Engine rails + admin lifecycle |
| HELIOS wishlist Funnel / path | Analytics of shaping |
| DESIGN §14.7 | Mode bias + retrieval optimizations |
