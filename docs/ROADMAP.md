# BASE + Helios roadmap

**Status:** living plan after base-1 → base-4  
**Normative (base-4):** [BIBLE.md](BIBLE.md) · **Lessons:** [base-1_to_base-4/lessons-learned.md](base-1_to_base-4/lessons-learned.md)  
**Helios requests (source of truth for analytics emits):** [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)  
**base-5 inject / Layer A deltas:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) — **rules + triggers as objects**; Client **`output_request` → `app_output`** (each app field = **`type` + `description`**; type-only is not enough)  
**base-5 control plane:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) — **settings bag** · **rule pack merge/freeze** · **Client policy table** · cache zones · security · observability  
**Ownership (set/unset/change):** [BIBLE.md §2](BIBLE.md)  
**Production pin:** still **base-1** (`CURRENT.json` / `v2/min`) until an explicit promote  

This is **what we want next and why**, not a commitment schedule. Prefer small, testable BASE bumps over big-bang rewrites.

---

## North star

```text
1. Model reliably emits complete Layer A (required + useful recommended)
2. Client multi-round state without prompt explosion
3. Humans/AIs can diet a BASE in text, re-encode JSON, Diff in one inspector
4. Helios gets typed, queryable scalars — prefer Zeus/Client over AI emit tax
5. Production pin only when stamp + Client + Detective are green
6. Clear control plane: settings ≠ prompt essays; triggers = signals; Client policy = law
7. Named rules + merge/freeze so multi-tenant packs stay auditable
```

---

## Cost law (Helios-aligned — every BASE)

From [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) §0:

| Provider | Cost | Role |
| --- | --- | --- |
| **AI / Layer A** | Expensive | Meaning only the model knows |
| **Zeus Client** | Cheap | tz, language, channel, market, deployment |
| **Zeus** | Cheap | tools, outcome, path, precomputed counts/sums |

**Rules:** Prefer cheap providers · AI only for meaning in the ask · piggyback before expand · `optional_when` over always-on · JSON numbers as numbers · sparse AI is normal · exception flags **true-only**.

Helios Motions read Analytics over **scalars** first; nested arrays are for drill-down.

---

## Where we are (base-4)

| Done | Why it mattered |
| --- | --- |
| Layer A G1/G2/G3 design | User / admin / client without Detective pollution |
| Single Terminate table + example | Clarity > second essay |
| base-N naming + customs pattern | Lineage on disk |
| Text export + `export_base_text.py` | Repeatable diet loops |
| Bible, mapping, lessons, multi-round docs | Onboarding |
| One `index.html` multi-BASE Diff | Migration without forking UI |

| Still open | Risk |
| --- | --- |
| Required four often incomplete in the wild | Detective fail · weak Helios QD |
| Recommended Layer A easy to drop | No Client control / admin telemetry |
| **No formal `company_context` or jailbreak `rules[]` in the prompt** | Score without policy ([JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)) |
| Most HEL-WISH items not in Layer A (by design) | Helios still on proxies until Zeus/Client emit |
| Production stamp path for base-4 | Can’t pin safely |
| Text → JSON re-encode | Manual drift |

**base-4 Layer A already useful for Helios (when emitted):**  
`query_decomposition` (intent/entity/geo/price strings), `decomposition`, `confidence`, plus recommended `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `policy_action`, `business_rules_triggers`.

**base-4 does *not* yet put in the prompt:** tenant **company/service content** or a default **jailbreak rule pack**. That is **base-5**.

---

## Helios wishlist → BASE / emit owner

Canonical detail: [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) §3–§5.  
**Do not** shove Pri-1 cheap items into AI Layer A.

### Priority 1 (cheap — ship first, almost never AI)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **003** | Outcome quality beyond `status=ok` | **Zeus** report | No catalog growth — Zeus emit |
| **008** | Path / rail / evidence counts | **Zeus** | No |
| **013** | User text preview (privacy-safe) | **Zeus** | No |
| **014** | Funnel / path stage enum | **Zeus** | No |
| **007** | Locale / language / timezone | **Client** → Zeus | Client inject / session headers |
| **009** | Channel & tenant-safe identity | **Client + Zeus** | Client session |

→ Track under **base-5 “emit spine”** (Zeus/Client workstreams), not “more return fields.”

### Priority 2 (cheap / mixed — next)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **002** | Session market geo | **Client** | Inject / config |
| **001** | `geo_norm` | AI `geo` string **piggyback** → **Zeus geocode** | Guidance: keep free-text `geo` on QD; Zeus fills norm |
| **012** | `multi_part` true-only + sparse AI | **Zeus** normalize; AI may propose parts | Guidance in Terminate / QD docs (not always-on) |
| **016** | Deployment / ruleset / mode slice | **Client + Zeus** | Session config (ties to base-id pin) |
| **017** | Context dump metrics | **Zeus** | No |
| **018** | Compare score parts | **Zeus** when ranking | No |
| **019** | Refine offer / recovery | **Zeus / Client UI** | No |

→ **base-5/6:** document QD optional facets (`geo`, `parts`) + sparse rules; implement norms on Zeus/Client.

### Priority 3 (scheduled — optional_when / map first)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **004** | `price_norm` numeric | Client slider preferred; AI last | Guidance types; not required every turn |
| **005** | `intent_norm` enum | Zeus synonym map preferred | Optional closed set in guidance |
| **011** | Demand rollups | Zeus jobs | No Layer A |
| **020** | chat_id recovery link | Zeus | No |
| **021** | Tool sequence fingerprint | Zeus from `tool_usage` | No |

### Priority 4–5 (defer AI-heavy)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **006** | Constraints / party size | Client forms preferred | Avoid AI-required bags |
| **010** | JTBD / sentiment | AI only | **Do not** put on hot-path terminate |

### Helios Motions → BASE alignment (quick)

| Motion | Wishlist unlocks | Prefer |
| --- | --- | --- |
| Explore | 013, 001, 017 | Zeus scalars + geo_norm |
| Compare | 018, 005, 013 | Zeus scores; intent_norm map |
| Refine | 019, 006, 004 | Product events; forms not AI |
| Funnel | 014, 016, 003 | Zeus stage + outcome.kind |

### Build order (from Helios §3 — unchanged)

```text
1. Zeus: outcome.kind + user_visible_count (003)
2. Zeus: path/funnel stage + evidence counts (008, 014)
3. Zeus: user_text_preview; context.chars (013, 017)
4. Client: language, tz, channel, tenant, market, deployment_id
5. Zeus: multi_part true-only; geocode geo_norm
6. Product: compare scores (018); refine (019)
7. AI only if needed: intent_norm / price_norm (optional_when)
8. Defer: soft AI JTBD/sentiment (010)
```

---

## base-5 — “Company + named rules + output_request + control plane + hooks”

**Theme:** Policy **in the prompt** (company + hard named rules); Layer A **objects** + **`app_output`**; and a full **Client control plane** (settings bag, rule merge/freeze, post-terminate policy table, cache zones, inject security, multi-turn flags, cheap observability). Start Helios Pri-1 on Zeus/Client (not more AI fields).

**Design detail:**

| Doc | Covers |
| --- | --- |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers · `output_request` → `app_output` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security · multi-turn · observability |
| [BIBLE.md §2](BIBLE.md) | Who may set / unset / change |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + hard rules + hooks |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |

### Headline deliverables (must ship in base-5)

| Deliverable | Where | Notes |
| --- | --- | --- |
| **`company_context` / service brief** | Prompt inject | After MINI-SCHEMA, before `rules` · ≤150 soft / 250 hard words · hash-excluded |
| **Jailbreak + hard `rules` as object** | Prompt inject | `{ rule_id: "one sentence" }` · [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) |
| **`business_rules_triggers` as object** | Terminate G3 | `{ rule_id: bool }` · missing = false · sparse |
| **`output_request` → `app_output`** | Inject + Terminate | See **§ base-5 output_request (type + description)** below — not type-only |
| **`message_jailbreak_soft`** (+ `message_*`) | Boilerplate | User-facing refuse; never show score |
| **`policy_action` soft-required** | Terminate G3 | Client maps → `message_*` |
| **Settings bag** | Client config (not essays) | `max_rounds`, model, verb deny, locale/channel/tz, redaction, debug, `output_request` · [PROMPT_SETTINGS §1](PROMPT_SETTINGS.md) |
| **Rule pack merge + freeze** | Client logic | SDK defaults ∪ tenant ∪ request · `override_defaults` · append-only keys mid-session · [§2](PROMPT_SETTINGS.md) |
| **Hard vs soft separation** | Docs + Client | Hard = `rules{}`; soft = hints later; brand = `message_*` |
| **Client post-terminate policy table** | After every `return` | Triggers = signals; Client (+ hooks) = law · chrome · flags · metrics · [§3](PROMPT_SETTINGS.md) |
| **Dual jailbreak scores** | Metrics | Model `jail_break_attempt` + Client `hooks_jailbreak_score` (do not overwrite) |
| **Session prefix vs refresh zones** | Assembly | Stable catalog+company+rules; dirty brief/schema; prune tool bodies · [§4](PROMPT_SETTINGS.md) |
| **Terminate reliability levers** | Client | Soft-require from `output_request.layer_a`; optional force final `return` when budget low |
| **Inject security** | Client | Schema caps; strip secrets; tool JSON = untrusted data; safe log defaults · [§8](PROMPT_SETTINGS.md) |
| **Multi-turn semantics** | Client | Sticky OR flags for business keys; clarify loop keeps `output_request`; mode switch = new session · [§6](PROMPT_SETTINGS.md) |
| **Cheap observability** | Client/Zeus | `ruleset_id`, inject-present bools, zone size estimates, trigger key rates · [§9](PROMPT_SETTINGS.md) |
| **AgentHooks baseline** | Client code | Prompt-dump / secrets / denied verbs even if model cooperates |

**Why base-5 (not base-4, not base-6):**  
base-4 has the **thermometer** and Terminate table (triggers still **arrays**). Real products need **policy in the prompt**, **named control-plane**, **settings not essays**, and **post-model law** — before soft HINTS/A-B (**base-6**) or Hub UI (**base-7**).

### Breaking vs base-4 (document in RELEASE_NOTES when shipping)

| base-4 | base-5 |
| --- | --- |
| `rules: string[]` (index `0` often empty) | `rules: { [id]: string }` |
| `business_rules_triggers: boolean[]` | `business_rules_triggers: { [id]: boolean }` |
| No first-class app bag | Optional `app_output` when Client sends `output_request.app.fields` |
| Type-only app maps (e.g. `sum_favorites: "INT"`) | **Rejected** — each field needs **`type` + `description`** |
| Informal Client behavior | Normative settings bag + merge + policy table |

Client **dual-read** arrays for one transition release if needed; objects are canonical.

### base-5 `output_request` — type + description (App → prompt → AI → validate)

**Problem:** If the App only sets a type map, the model has no idea *what* to compute.

```text
# BAD — type only (not enough)
{ "sum_favorites": "INT" }
```

**Rule:** each app field is **type** (machine) + **description** (model instruction). Client **renders descriptions into the prompt**; validates **types** on terminate.

```text
# GOOD
output_request.app.fields = {
  sum_favorites: {
    type: "integer",   # or INT → normalize
    description: "Sum of favorites across rows returned by Zeus this turn for the asked subject. Use 0 if none. Integer only — not in summary."
  },
  booking_ready: {
    type: "boolean",
    description: "True only if city, check-in, and check-out are known and a search could run; else false."
  }
}
required: ["sum_favorites", "booking_ready"]
```

**Flow:**

```text
App sets:   field → { type, description }
Client:     injects short "Output request" block into prompt (from descriptions)
            keeps types for post-return validation
AI:         reads instruction → tools/work → emits app_output values only
Client:     validates type/required → App UI / flags
            descriptions are NOT re-emitted on terminate
```

**What the model should see (Client-rendered, not a raw schema dump):**

```text
## Output request (this turn) — fill app_output on terminate
Always also emit required Layer A: summary, query_decomposition, decomposition, confidence.

app_output fields (follow the instruction; types are for the JSON value):
- sum_favorites (integer, required): Sum of favorites across rows returned by Zeus
  this turn for the asked subject. Use 0 if none. Integer only — not in summary.
- booking_ready (boolean, required): True only if city, check-in, and check-out
  are known and a search could run; else false.

Emit: app_output: { "sum_favorites": <int>, "booking_ready": <bool>, ... }
Only these keys. Ground numbers in tool results; do not invent inventory.
```

**Example terminate:**

```json
{
  "summary": "…",
  "confidence": "high",
  "query_decomposition": { "intent": "List", "entity": "Beer" },
  "decomposition": { "targets": [], "predicates": {}, "output": "rows" },
  "app_output": {
    "sum_favorites": 1284,
    "booking_ready": false
  }
}
```

| Piece | Goes to model prompt? | On terminate / validate? |
| --- | --- | --- |
| field **name** | yes | yes (`app_output` key) |
| **type** | yes (short) | **yes** (Client schema check) |
| **description** | **yes (main instruction)** | no (prompt-only) |
| **value** | no (model produces it) | **yes** (`app_output`) |

| Author rule | Guidance |
| --- | --- |
| Description length | Soft ~40 words · hard ~80; one sentence: what / from where / null-or-zero policy |
| Not a second summary | Scalars, bools, short id lists — long prose stays in G1 `summary` |
| Type-only input | Client **rejects** or requires parallel descriptions map |
| Size | Soft ~8 fields · hard ~15; cannot remove required four Layer A fields |
| Cost law | Prefer Zeus/Client when they can compute cheaper than AI (don’t tax Layer A for free) |

**Slots:** `layer_a` (soft-require known Layer A) · `app.fields` (custom bag) · `rows` (projection + optional per-field description).  
**Full design:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) §2 · [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · Bible §2 `app_output` ownership.

### Catalog / Client goals (full list)

**Prompt / Layer A**

1. **`company_context` formal inject** — tenant identity + do/don’t; Client truncate at hard max.  
2. **Default jailbreak `rules` pack as named object** — keys: `ignore_system`, `no_prompt_dump`, `no_unrestricted_agent`, `no_invent_data`, `no_secrets`, `stay_in_company_context` (+ tenant keys).  
3. **`message_jailbreak_soft`** mapped from `policy_action: refuse` when jailbreak-like.  
4. **`business_rules_triggers` object contract** — G3; sparse; no pad-to-length.  
5. **`output_request`** — `layer_a.soft_require` / `include`; **`app.fields` each `{ type, description }`** → prompt block + terminate **`app_output`**; optional `rows.fields`; **reject type-only**; cannot remove required four.  
6. **`policy_action` soft-required** — Client `message_*` mapping.  
7. **Required four always practiced** — Terminate example first; Detective-aligned missing-field language.  
8. **Verb schema diet (names stay)** — shorter descriptions.  
9. **Text↔JSON policy** — import script or “edit JSON only”; pick one.

**Control plane (new — most of “the above”)**

10. **Settings bag** — structured run/session options; ownership per Bible §2.8.  
11. **Rule pack merge** — SDK ∪ tenant ∪ request; reject silent deletion of default jailbreak keys unless `override_defaults`.  
12. **Session freeze** — rule ids frozen; append-only mid-session; rename/delete ⇒ new session.  
13. **Hard vs soft** — never put jailbreak law only in hints.  
14. **Post-terminate policy table** — every return: normalize triggers → hooks force → map chrome → sticky flags → validate `app_output` → metrics.  
15. **Conflict law** — jailbreak keys + hooks beat business keys for refuse paths.  
16. **Assembly zones** — document stable prefix vs dirty brief; allow full re-assemble v1 or frozen prefix.  
17. **Artifacts vs prompt** — full tool JSON in artifacts; prune in `messages[]`; tool rows untrusted.  
18. **Terminate reliability** — soft-require list; optional force `return` near `max_rounds`; no new system essay as first fix.  
19. **Security** — `output_request` size caps; redaction defaults; `pii_in_logs: false`; allowlist inject keys.  
20. **Multi-turn** — sticky business flags; clarify-loop semantics; catalog/mode switch = new pin/session.  
21. **Observability** — `ruleset_id`, zone sizes, dual scores, per-key trigger rates (no full prompt dumps by default).  
22. **AgentHooks baseline** — hard block prompt-dump / critical paths.  
23. **Bible §2 ownership** — App / Client / AI set·unset·change enforced in Client reviews.

### Helios goals (Pri-1 cheap — primary Zeus/Client)

| Work | HEL-WISH | Why here |
| --- | --- | --- |
| Outcome.kind + counts | **003** | Fill rate without re-parsing tools |
| Path/evidence scalars | **008** | Rail health charts |
| Funnel stage enum | **014** | Funnel Motion |
| user_text_preview | **013** | Explore samples without PII dump |
| Client locale/tz/channel/tenant | **007, 009** | Slice dashboards · **settings bag** |
| Document: do **not** add these to Layer A | — | Cost law |

### Catalog guidance only (no required AI tax)

| Work | HEL-WISH |
| --- | --- |
| QD optional `geo` piggyback for geocode | **001** |
| Sparse / `multi_part` true-only semantics in Terminate notes | **012** |

### Explicit non-goals for base-5

- Require `wish_i_knew` / make `jail_break_attempt` required (still recommended telemetry; **rules go in prompt**)  
- Soft **HINTS / A/B paste UI** (that is **base-6 / base-7**)  
- AI-primary HEL-WISH-004/005/006/010  
- TOON as SoT · separate index HTML · pin CURRENT to base-4 without Client proof  
- Multi-page company manifesto in the inject (hard-cap 250 words)  
- Giant `app` JSON Schema / OpenAPI dumps (soft max ~8 properties; hard ~15)  
- Replacing required four with app schema alone  
- Keeping index-aligned `rules[]` as the long-term contract (arrays only for dual-read)  
- Provider prompt-cache **product** as a hard dependency (document zones only; productize later)  
- Auto-summarize tool history via a second LLM (truncate first)  
- Workbench full key/value editor (design ok; UI is **base-7**)

### Success signals

- [ ] Diff base-4 → base-5 documents **array→object rules/triggers** + **`app_output`** + **control plane**  
- [ ] Client injects **company_context** + **merged frozen jailbreak `rules` object** on every turn  
- [ ] Client spike: `triggers.get("coupon_presented")` + sticky flags + `policy_action` + `message_jailbreak_soft`  
- [ ] Client spike: **settings bag** + **policy table** runs on every terminate  
- [ ] Client spike: `output_request.app.fields` with **type + description** → prompt “Output request” block + validated **`app_output`**  
- [ ] Client **rejects** type-only fields (e.g. `sum_favorites: "INT"` without description)  
- [ ] Description rendered for model; types used only for validate; values-only on terminate  

- [ ] Merge rejects deleting default jailbreak keys without `override_defaults`  
- [ ] Mid-session rule rename rejected or requires session reset  
- [ ] Tool JSON treated as untrusted; G2 never in chat UI  
- [ ] Cheap emit: `ruleset_id` and/or zone size estimates on a demo path  
- [ ] Refuse path works on freebie/prompt-dump examples in [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)  
- [ ] At least one Pri-1 Helios field path demoed on **Zeus report** (003 or 014 preferred)  
- [ ] Inspector: base-1 + base-5 Diff  
- [ ] Catalog bytes ≤ base-4 or justified  
- [ ] Bible §2 + PROMPT_SETTINGS + this section stay aligned  

### Why this order

**Policy in the prompt + named control-plane + post-model law** before soft A/B hints or more admin fields. Helios Pri-1 remains **report/session emit**, not “grow return schema for every dashboard.”

---

## base-6 — “G2 telemetry + prompt budget + soft hints + Helios norms”

**Theme:** Admin Layer A discipline; **measured** prompt size zones; formal **soft hints** (not hard policy); **typed norms** Helios can GROUP BY.  
**Depends on base-5:** company_context + named `rules` + settings/policy table already work.

### Catalog / Client goals

1. **`wish_i_knew` optional-but-shaped** (max 3, kinds enum) — Workbench gaps, not UI.  
2. **`subject_confidence` / `jail_break_attempt` metrics hygiene** — never `summary`; **require dual path** for `hooks_jailbreak_score` in ops docs.  
3. **Assembled prompt budget zones (enforced)** — drop order; size map tags; company_context / hints caps; build on base-5 zone *estimates*.  
4. **`hints` / Hot-Path / A/B paste slots (formal)** — **after** hard `rules`  
   - Workbench **Prompt Helper** whole-block copy-paste (`hot_path`, `ab_paste`, `ab_arm`).  
   - **Hash-excluded** so A/B does not thrash contract pins.  
   - Same word discipline: soft max ~150 / hard max ~250 **per block**.  
   - **Must not strip or replace base-5 jailbreak rules** by default.  
   - Why base-6 (not base-5): needs stable company_context + frozen hard rules first; soft ≠ hard.  
5. **Optional terminate retry** — one “required four only” repair pass after incomplete Layer A.  
6. **De-demo efficiency prose** — generic entity examples.  
7. **Customs filename smoke** — `…_cus_<bucket>_<scope>-N` in scan + Client.  
8. **Settings `ab_arm` / experiment slice** on report (cheap Client).

### Helios goals (Pri-2/3 norms)

| Work | HEL-WISH | AI load |
| --- | --- | --- |
| `geo_norm` via Zeus geocode from QD `geo` | **001** | piggyback only |
| Client market geo | **002** | none |
| deployment / ruleset / mode / base_id slice | **016** | none |
| context dump metrics | **017** | none |
| multi_part normalize on Zeus | **012** | flag cheap |
| intent_norm map (Zeus first) | **005** | light if AI |
| price_norm (Client slider preferred) | **004** | light if AI |
| Tool fingerprint / chat recovery | **021, 020** | none |

### Explicit non-goals for base-6

- Full wishlist as always-on Layer A  
- HEL-WISH-010 on hot path  
- Auto-ban on jailbreak float  

### Success signals

- [ ] G2 metrics without UI leak  
- [ ] System prompt flat/down after de-demo  
- [ ] At least one `*_norm` path live (001 or 005) without new required AI fields  
- [ ] lessons-learned updated  

---

## base-7 — “Workbench + stamp + product events”

**Theme:** Productize base-N authoring; Helios product-path events; Detective soft fail.

| Goal | Why | Helios / control plane |
| --- | --- | --- |
| Hub load/save base-N + custom rev | Customs lifecycle | **016** ruleset identity |
| **Rules key/value editor** + company_context word meter | Authors don’t freehand JSON only | base-5 packs become operable |
| **Lint** (rule length, dup keys, default-key delete, inject caps) | Catch bad packs early | PROMPT_SETTINGS §10 |
| **Preview assembled prompt** with zone sizes | Debug budget before prod | base-6 zones |
| **Prompt Helper UI for HINTS + A/B arms** | Whole-block paste, arm label, Diff arms | **016** + experiment slice |
| Stamp/verify for base-N | Real hashes before pin | Contract slice |
| Detective: optional Layer A = **warn** not fail | Don’t block on wish_i_knew | Terminate reliability |
| Compat: Zeus semver ↔ base-N | `COMPAT.md` | — |
| Compare score parts when ranking | Product | **018** |
| Refine recovery events | Product | **019** |
| Demand rollups jobs | Batch | **011** |

---

## base-8+ — “Pin, compression, cache product, optional AI-heavy”

| Idea | Why | Gate |
| --- | --- | --- |
| Promote base-N to `CURRENT` / `v2/min` | Users get diet | Stamp + Client + Helios Pri-1 green |
| Provider **prompt-cache** productization | Cost on stable prefix | Measured savings; base-5 zones already documented |
| Structured-output / JSON-schema constrained `return` | Layer A reliability | AI API support |
| Tool-history auto-summarize | Long sessions | Quality evals; truncate first |
| TOON view for Workbench | Editor tokens | JSON remains SoT |
| Per-mode default rule packs (fraud stricter) | Mode matrix | After merge algorithm stable |
| Soft AI insights (JTBD/sentiment) | **HEL-WISH-010** | Off by default; offline/batch only |
| Constraints AI (006) only if forms insufficient | Cost | Client forms first |
| Multimodal user parts | Product | Same inject model |
| Require more Layer A fields | Quality | Measured emit rates |

---

## Suggested sequencing (summary)

```text
base-4  Terminate table + Layer A score fields (jail_break_attempt telemetry only)
        triggers still boolean[] (index-aligned) in schema
           │
base-5  ★ company_context IN PROMPT (≤150 / 250 words)
        ★ hard rules as OBJECT { id → text } + triggers OBJECT (sparse)
        ★ output_request → app_output (type + description per field; type-only rejected)
        ★ Client renders field descriptions into prompt; validates types on return
        ★ settings bag (caps, verbs, locale, redaction, …)
        ★ rule pack merge + freeze + override_defaults
        ★ Client post-terminate policy table (signals → law)
        ★ assembly zones + inject security + sticky flags
        ★ cheap observability (ruleset_id, zone sizes, dual scores)
        ★ message_jailbreak_soft + policy_action + hooks baseline
        + Layer A reliability levers (soft-require, force return)
        + Helios Pri-1 cheap spine (Zeus/Client)  HEL 003,008,013,014,007,009
           │
base-6  G2 hygiene + enforced budget zones + soft hints/A-B slots
        + optional Layer A retry · ab_arm on report
        + HEL 001,002,012,016,017,004/005 optional
           │
base-7  Workbench: rules KV editor, lint, prompt preview, A/B UI
        + stamp/compat + Detective warn + product events
        + HEL 018,019,011,020,021
           │
base-8+ pin promote · prompt-cache product · structured return
        · optional TOON · AI-heavy 010 only off-path
```

```text
Helios cost filter (every proposal):
  Can Zeus/Client emit it?  → do that (BASE guidance only if needed)
  Needs AI meaning?         → optional_when · never always-on hot path
  Needs dashboard GROUP BY? → precomputed scalar on report, not only arrays
```

---

## Why not dump Helios into base-5 Layer A

| Temptation | Why not |
| --- | --- |
| AI emits outcome.kind / path.stage | Zeus already knows — cheaper and exact |
| AI lat/lon | Geocode from free-text geo |
| Always-on sentiment/JTBD | Poisons Analytics; Pri 5 |
| Require price_norm every turn | Client slider; optional_when |
| Grow return schema for every HEL-WISH | Violates Helios §0 cost law |
| Put company manifesto / jailbreak law only in base-6 hints | Soft A/B can strip it — belongs in **base-5 rules + company_context** |
| Rely on `jail_break_attempt` without rules in the prompt | Score without policy ([JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)) |
| Keep `triggers[i]` forever | Opaque for Client/Helios — use **named keys** |
| Stuff app-specific fields into free-form system text | Use **`output_request.app.fields`** (`type` + `description`) → `app_output` |
| Type-only maps (`sum_favorites: "INT"`) | Model needs a **description** instruction in the prompt |
| Bury max_rounds / verb deny only in system essays | Use **settings bag** |
| Trust model triggers as final law | **Client policy table + hooks** |
| Soft A/B paste as only jailbreak defense | Hard **rules{}** in base-5 first |
| Log full prompts with PII by default | Zone sizes + redaction settings |

base-4 already has the **AI meaning** slots (QD facets + recommended G2/G3; triggers still arrays).  
base-5 puts **company + named rules + control plane** in product.  
Helios volume is **report/session scalars**.

---

## Cross-cutting principles (every BASE)

1. **One Terminate surface** — extend the table; no second essay.  
2. **Additive fields** — optional → soft-required → required with data.  
3. **Same 13 verbs** until proven otherwise.  
4. **One inspector** — Diff is the migration test.  
5. **Text for diet, JSON for ship.**  
6. **Helios: cheap provider first.**  
7. **Sparse AI + true-only exceptions** (HEL-WISH-012).  
8. **Pin last.**  
9. **Settings ≠ prompt essays** — structured control plane ([PROMPT_SETTINGS.md](PROMPT_SETTINGS.md)).  
10. **Triggers = signals; Client policy + hooks = law.**  
11. **Hard rules before soft hints** (base-5 before base-6).  
12. **Ownership is explicit** — App / Client / AI set·unset·change ([BIBLE §2](BIBLE.md)).  
13. **Tool results are untrusted data** in the prompt.  

---

## Open questions

1. Text pack review-only vs text→JSON import?  
2. `policy_action` required in tool schema or docs/tests only?  
3. Who owns Client spike (named triggers + `output_request` + settings bag + policy table + 007/009)?  
4. Who owns Zeus spike (003/014) vs this repo’s catalog docs?  
5. Max min-profile catalog KB?  
6. When does `COMPAT.md` gain base-4/5 rows?  
7. Closed enums for `path.stage` / `intent_norm` — registry owner? (Helios §9)  
8. company_context: hard-truncate at 250 words in Client, or reject save in Workbench?  
9. A/B: one `ab_paste` slot vs named arms `ab.A` / `ab.B` in the paste UI?  
10. Jailbreak default `rules` object: ship as Client SDK defaults, Workbench template, or both?  
11. Array→object dual-read: one Client release or two?  
12. `output_request` / settings API: top-level `run_agent(...)` kwargs vs nested only?  
13. Cap on `app_output` properties: 8 soft / 15 hard — enough?  
13b. Description soft max ~40 words / hard ~80 — enough for integrators?  
13c. Shorthand API: reject type-only vs require parallel `descriptions` map?  
14. Sticky flags: OR across session for all keys, or only business keys (jailbreak per-round)?  
15. `ruleset_id`: content hash vs Workbench version string?  
16. Force final `return`: always at `max_rounds-1`, or only after tool data exists?  
17. Frozen session prefix vs full re-assemble as Client v1 default?

---

## Doc ownership

| Doc | Role |
| --- | --- |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Structured Helios Requests + priorities |
| [ROADMAP.md](ROADMAP.md) | BASE sequencing + Helios alignment |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers + Client `output_request` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold new base-N pack (`scripts/new_base.py`) |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BIBLE.md](BIBLE.md) | Normative base-4 + §2 ownership |
| [RELEASE_NOTES.md](../RELEASE_NOTES.md) | What shipped + **breaking changes** |
| [base-1_to_base-4/lessons-learned.md](base-1_to_base-4/lessons-learned.md) | Experience |

---

*Align with Helios wishlist when HEL-WISH IDs change; revise BASE section when base-5 starts. Control-plane detail lives in PROMPT_SETTINGS.md.*
