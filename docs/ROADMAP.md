# BASE + Helios roadmap

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · **candidate pack base-5** (`v2/base/base-5/`) · last breaking train · version matrix: [COMPAT.md](../COMPAT.md)


**Status:** living plan after base-1 → base-4 → **base-5 candidate pack**  
**Normative (base-4 era docs, base-5 wire freeze):** [BIBLE.md](BIBLE.md) · **Lessons:** [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) · [migration/base-4_to_base-5/lessons-learned.md](migration/base-4_to_base-5/lessons-learned.md)  
**Helios requests (analytics emits):** [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)  
**zeus_client backlog (implement floor):** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) (`ZC-WISH-*`)  
**base-5 inject / Layer A deltas:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) — **rules + triggers as objects**; Client **`output_request` → `app_output`** (each app field = **`type` + `description`**; type-only is not enough)  
**base-5 control plane:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) — **settings bag** · **rule pack merge/freeze** · **Client policy table** · cache zones · security · observability  
**Ownership (set/unset/change):** [BIBLE.md §2](BIBLE.md)  
**Production pin:** still **base-1** (`CURRENT.json` / `v2/min`) until an explicit promote  
**Agent procedure:** [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) · hop [migration/base-4_to_base-5/](migration/base-4_to_base-5/)  
**Jira board:** [CR board 48](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48) · tracking table **§ CR board map** below

This is **what we want next and why**, not a commitment calendar.  
**Exception to “small bumps”:** **base-5 is intentionally the big wire/control-plane break** while nothing is in production on this line — then **base-6+ stay additive/optional**.

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
8. Break once in base-5; additive/optional forever after (until a new major is justified)
```

---

## BASE change law (post base-4)

No production traffic on the **base-4/5 line** yet. Use that:

| BASE | Allowed change type | Examples |
| --- | --- | --- |
| **base-5** | **BREAKING OK** — freeze the contract | Object rules/triggers · settings bag · policy table · `output_request` · company+jailbreak in prompt |
| **base-5.1** | **Content patch on base-5 wire** — **not** a new wire break | Restore **mode overlays** in system prompt (`messages[].content`); core+overlay; no Layer A rename |
| **base-6+** | **ADDITIVE / OPTIONAL only** | Soft hints/A/B · optional_when fields · Workbench UX · Helios norms as cheap emits · pin when green |
| **Helios wishlist** | **Nice-to-have** (cheap provider first) | Pri-1 Zeus/Client report scalars — **never** required AI Layer A tax |

```text
base-5    = last wire/control-plane break before real adoption of this line
            Prefer one clean object contract over dual-read forever.

base-5.1  = content/diet train ON the base-5 wire (mode personas in prompts)
            Same schema objects / required four / app_output — packs stop being
            “analytics × rename”. See docs/MODE.md · work/RECREATE_MODE.md

base-6+   = additive / optional_when / hash-excluded soft injects / productization
            No rename/remove of base-5 wire keys without a new major BASE + migration hop.

Helios    = analytics spine on Zeus/Client; optional_when if AI ever needed
            Never block pin on Pri-2/3/4/5 AI fields
```

**Naming note:** `base-5.1` is a **roadmap train id** (content patch). On disk the pack may still live under `v2/base/base-5/` with `_lineage.base_id=base-5` until an explicit pack folder/lineage policy is chosen in the work plan (D1). It is **not** a semver of Zeus or zeus_client.

**Dual-read** of base-4 `rules[]` / `boolean[]` triggers: **≤ one Client release** while migrating, then **drop**. base-5 catalogs and docs are **object-only**. Prefer **zero** dual-read if no external consumers.

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

## Where we are

| Done | Why it mattered | CR |
| --- | --- | --- |
| base-4 pack + Terminate table + Layer A G1/G2/G3 | Candidate foundation | **CR-2** Done |
| Multi-BASE inspector (`index.html`) | Diff packs | **CR-7** Done |
| Policy docs + RELEASE_NOTES + ROADMAP on main | Train language | **CR-8** Done |
| Multi-round Client **docs** | Bags A–D | **CR-17** Done |
| **base-5 pack on disk** (`v2/base/base-5/`) | **Last breaking freeze**: object triggers, `app_output`, inject contracts | **CR-3** / **CR-22** |
| Docs: playbook, migration hops, RELEASE_CHECKLIST, COMPAT | Agent-friendly BASE bumps | PR #4–#5 |
| Process: `verify_base_pack.py` + phased checklist + Jira §9 | Scaffold ≠ ship | **CR-19** (PR #6) |
| `scripts/new_base.py` | Repeatable pack scaffold | — |
| zeus_client **wishlist** (`ZC-WISH-*`) | Prioritized Client backlog | [ZEUS_CLIENT_WISHLIST…](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) |

| Still open | Risk | CR |
| --- | --- | --- |
| zeus_client implements object triggers + settings/policy/`output_request` | Catalogs ready; Client floor TBD | **CR-20** (+ CR-9/10/11) |
| Zeus loaders / return schema / Detective for base-5 | Can’t pin | **CR-21** |
| **base-5.1 mode overlays** — catalogs ≈ analytics×rename | LLM ignores DESIGN mode intent | **CR-23** (plan) |
| Helios Pri-1 report emits (cheap spine) | Not catalog tax | **CR-12** |
| Required four incomplete in the wild | Detective / soft-require levers | CR-21 + Client |
| CURRENT still base-1 | Expected until green | **CR-18** (blocked by CR-20/21) |
| base-6 soft injects | After Client floor | **CR-4** |
| base-7 Workbench / stamp product | Later | **CR-5** |

**Pack SoT for new work:** **base-5** wire ([v2/base/base-5/](../v2/base/base-5/)) · next **content** train **base-5.1** (modes).  
**Production pin:** **base-1**.  
**Hop:** [migration/base-4_to_base-5/](migration/base-4_to_base-5/).  
**Modes:** [MODE.md](MODE.md) · plan [work/RECREATE_MODE.md](../work/RECREATE_MODE.md).  
**Client implement order:** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) §4.

---

## CR board map (project CR)

Board: https://kotenai.atlassian.net/jira/software/projects/CR/boards/48  
Last status pass: **2026-07-26**.

| Key | Role | Board status (intent) | ROADMAP home |
| --- | --- | --- | --- |
| **CR-1** | Epic — repo SoT / BASE sequence / COMPAT | In Progress | This repo strategy (ongoing) |
| **CR-2** | Epic — base-4 ship | **Done** | § Where we are (base-4) |
| **CR-3** | Epic — base-5 pack + residual | In Progress | § base-5 |
| **CR-4** | Epic — base-6 additive | To Do | § base-6 |
| **CR-5** | Epic — base-7 Workbench | To Do | § base-7 |
| **CR-6…8, CR-17** | base-4 stories | **Done** | base-4 train |
| **CR-9** | company_context inject (Client) | In Progress (spec/pack done) | base-5 · ZC-WISH-006 |
| **CR-10** | jailbreak rules{} + hooks | In Progress (spec/pack done) | base-5 · ZC-WISH-002/013 |
| **CR-11** | object triggers + policy table | In Progress (pack done) | base-5 · ZC-WISH-004/010 |
| **CR-12** | Helios Pri-1 cheap spine | To Do | Helios Pri-1 · ZC-WISH-030… |
| **CR-13…14** | base-6 stories | To Do | § base-6 |
| **CR-15…16** | base-7 stories | To Do | § base-7 |
| **CR-18** | Pin promote CURRENT | To Do (blocked) | § base-8+ |
| **CR-19** | Process verify + checklist | In Review (PR #6) | Process / CREATE_BASE |
| **CR-20** | zeus_client base-5 floor | To Do | § base-5 · full wishlist |
| **CR-21** | Zeus base-5 loaders/Detective | To Do | § base-5 external |
| **CR-22** | Pack docs completion tracker | In Review | § base-5 pack |
| **CR-23** | **base-5.1** mode overlays in system prompt | To Do | § base-5.1 · [MODE.md](MODE.md) · [RECREATE_MODE.md](../work/RECREATE_MODE.md) |

When a train lands: update epic + create residual stories (checklist [§9](migration/RELEASE_CHECKLIST_TEMPLATE.md)).

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

→ **base-5:** document QD optional facets (`geo`, `parts`) in Terminate notes (guidance only).  
→ **base-6+:** implement norms on Zeus/Client as **optional / additive** (nice-to-have; not wire breaks).

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

## base-5 — “Last breaking freeze + company + control plane”

**Theme:** Take **all remaining wire/control-plane breaks now** (nothing prod on this line yet). Freeze a clean contract: company + hard named rules; Layer A **objects** + **`app_output`**; Client **settings + policy table + merge/freeze**. Helios Pri-1 stays **Zeus/Client report emits** (nice spine, not Layer A tax).

**Design detail:**

| Doc | Covers |
| --- | --- |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers · `output_request` → `app_output` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security · multi-turn · observability |
| [BIBLE.md §2](BIBLE.md) | Who may set / unset / change |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + hard rules + hooks |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | Agent comply/upgrade checklists |
| [migration/base-4_to_base-5/](migration/base-4_to_base-5/) | Hop + GUIDE + RELEASE_CHECKLIST |
| Pack | [`v2/base/base-5/`](../v2/base/base-5/) | Candidate on disk |

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
base-4 has the **thermometer** and Terminate table (triggers still **arrays**). Real products need **policy in the prompt**, **named control-plane**, **settings not essays**, and **post-model law**. Soft HINTS/A-B and Helios norms are **additive later** — they must **not** re-open the wire.

### Breaking vs base-4 (take **all** of this now — document in RELEASE_NOTES)

| base-4 | base-5 (**canonical; no multi-BASE dual-read plan**) |
| --- | --- |
| `rules: string[]` (index `0` often empty) | `rules: { [id]: string }` **only** |
| `business_rules_triggers: boolean[]` | `business_rules_triggers: { [id]: boolean }` **only** (sparse) |
| No first-class app bag | `app_output` when Client sends `output_request.app.fields` |
| Type-only app maps (e.g. `sum_favorites: "INT"`) | **Rejected** — each field needs **`type` + `description`** |
| Informal Client behavior | Normative settings bag + merge + policy table + hooks dual score |
| Array triggers forever / dual-read lifestyle | **Migrate once** · Client dual-read **≤ 1 release** then **remove** |

### Frozen after base-5 (do not break without a new major BASE + migration hop)

| Surface | Frozen shape |
| --- | --- |
| `rules` / `business_rules_triggers` | **Objects** keyed by stable `rule_id` |
| `app_output` | Optional G3/app bag; field map is type+description on inject |
| Settings bag | Structured keys (max_rounds, locale, redaction, verb deny, …) — extend additively |
| G1 / G2 / G3 audiences | User / admin / client split on Layer A |
| Required four | Unchanged forever unless major BASE |
| Soft inject slot names | Reserve hash-excluded `hints.*` for base-6+ (**additive**; implement later) |

After base-5 ships as candidate: **prefer only additive optional fields and soft injects** until pin.

### base-5 `output_request` — type + description (summary)

**Rule:** each app field is **`type` (validate) + `description` (model instruction in the prompt)**. Type-only maps like `{ "sum_favorites": "INT" }` are **rejected**.

```text
App:  fields.sum_favorites = { type: integer, description: "Sum favorites…; 0 if none" }
Client → prompt "Output request" block from descriptions
AI → app_output: { "sum_favorites": 1284 }
Client → type-check values (descriptions not re-emitted)
```

**Canonical detail + full examples:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) §2  
**Ownership:** [BIBLE.md](BIBLE.md) §2 · **Version floors:** [COMPAT.md](../COMPAT.md)

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
- Soft **HINTS / A/B paste UI** (**base-6+ additive** — not a second wire break)  
- AI-primary HEL-WISH-004/005/006/010 (nice-to-have / off-path)  
- Multi-year dual-read of array triggers (objects only after ≤1 Client release)  
- TOON as SoT · separate index HTML · pin CURRENT without Client proof  
- Multi-page company manifesto in the inject (hard-cap 250 words)  
- Giant `app` JSON Schema dumps (soft max ~8 properties; hard ~15)  
- Replacing required four with app schema alone  
- Provider prompt-cache **product** as a hard dependency  
- Auto-summarize tool history via a second LLM (truncate first)  
- Workbench full key/value editor (additive **base-7** product)  
- Blocking base-5 on Helios Pri-2+ dashboard norms  

### Success signals

**Pack / docs (this repo) — largely green after PR #5:**

- [x] Diff base-4 → base-5 documents **all breaking wire** (array→object, app_output, control plane) — RELEASE_NOTES + hop GUIDE  
- [x] base-5 catalogs: **object rules/triggers only** (no array as SoT)  
- [x] COMPAT: base-5 **candidate** row (object-only Client floor noted; package TBD)  
- [x] Playbook + migration hop describe base-5 as **last breaking** train  
- [x] Pack verified: `python3 scripts/verify_base_pack.py --base 5`  

**Client / Zeus residual — still open (CR-20 / CR-21):**

- [ ] Client: object triggers; dual-read arrays **≤1 release** then removed  
- [ ] Client injects **company_context** + **merged frozen jailbreak `rules` object**  
- [ ] Client spike: `triggers.get("coupon_presented")` + sticky flags + `policy_action` + `message_jailbreak_soft`  
- [ ] Client spike: **settings bag** + **policy table** every terminate  
- [ ] Client spike: `output_request.app.fields` type+description → prompt + validated **`app_output`**  
- [ ] Client **rejects** type-only fields  
- [ ] Merge rejects deleting default jailbreak keys without `override_defaults`  
- [ ] Tool JSON untrusted; G2 never in chat UI  
- [ ] Cheap emit: `ruleset_id` / zone sizes (ops, not Layer A tax)  
- [ ] Refuse path works on [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) examples  
- [ ] Helios Pri-1 path on **Zeus report** (003 or 014) — not new required AI fields (**CR-12**)  
- [ ] COMPAT: Client package version row when floor ships  
- [ ] Catalog bytes ≤ base-4 or justified  

**Track Client work as `ZC-WISH-*`:** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) · umbrella **CR-20**.

### Why this order

**Break the wire once (base-5)** while no one is prod on this line, then **content patches (base-5.1)** and **only additive/optional** (base-6+) changes. Soft A/B and Helios norms must not force a second contract rewrite. Helios Pri-1 remains **report/session emit**.

---

## base-5.1 — “Mode overlays restored” (content on base-5 wire)

**Jira:** **[CR-23](https://kotenai.atlassian.net/browse/CR-23)** · parent epic **CR-3** · status To Do  
**SoT:** [MODE.md](MODE.md) · **Plan:** [work/RECREATE_MODE.md](../work/RECREATE_MODE.md)  
**Design:** [zeus_design_docs DESIGN.md §14](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) · Zeus `internal/modes/`

**Theme:** base-5 **froze the wire** but left **10 mode packs nearly identical** (analytics system essay × rename; only `auto` shorter). **base-5.1** restores DESIGN mode intent into the **stamped system prompt** (`messages[].content` = shared CORE + per-mode **MODE_OVERLAY**). **Not** a Layer A / object break.

| | |
| --- | --- |
| **Wire** | Unchanged base-5 (object triggers, `app_output`, required four, settings/policy contracts) |
| **Content** | Mode personas: entities, join/noise posture, edges, don’ts, example pipelines |
| **On disk** | Prefer keep `v2/base/base-5/` + document train as **5.1** until D1 says otherwise |
| **Generator** | Fill Zeus `ai/V2/prompt/core/modes/<mode>.md` (hook already exists, empty today) |

### Goals

1. Core + thin overlay architecture (not 10 full forked essays).  
2. Overlays for all 10 modes (priority: analytics → fraud → research → code → regulated → tenant/private/open → auto → custom).  
3. Clean clone leftovers (`[exp] analytics job`, etc.).  
4. `diff_modes` / clone gate so `new_base` cannot re-ship analytics×rename.  
5. Port overlays into Zeus snapshot path.  
6. Inspector Diff analytics vs fraud/research/code is human-meaningful.

### Explicit non-goals for base-5.1

- Rename/remove base-5 wire keys or required four  
- Soft HINTS/A/B (**base-6**)  
- Pin promote (**CR-18**)  
- Client policy-table implement (**CR-20**) — orthogonal; can parallel  
- Full Zeus `AppliesTo` tool matrix rewrite (optional later)

### Success signals

- [ ] [MODE.md](MODE.md) + [RECREATE_MODE.md](../work/RECREATE_MODE.md) on main  
- [ ] CORE extracted; analytics rebuild from CORE + overlay  
- [ ] fraud / research / code / regulated overlays land in packs  
- [ ] All 10 modes pass §6.1 keyword/entity smoke in MODE.md  
- [ ] Neutralize-mode Diff ≠ empty vs analytics (except intentional shared CORE)  
- [ ] `verify_base_pack.py --base 5` OK  
- [ ] Zeus `modes/<mode>.md` ported or dual-home documented  
- [ ] RELEASE_NOTES notes base-5.1 content train  
- [ ] CR-23 Done  

### Sequencing vs other work

```text
base-5 pack (wire)     ──done──►  base-5.1 (mode prompts)  ──►  base-6 soft injects
        │                              │
        └── Client CR-20 / Zeus CR-21 ─┴── can parallel; pin still last
```

Prefer **base-5.1 before or in parallel with Client spike** so trials exercise real mode personas, not 10 analytics clones.

---

## base-6 — “Additive soft inject + optional Helios norms”

**Jira:** epic **[CR-4](https://kotenai.atlassian.net/browse/CR-4)** · stories **CR-13**, **CR-14** · status To Do (correct until base-5 Client residual prefers green).

**Theme:** **No breaking wire changes vs base-5.** Soft hints/A/B (hash-excluded); optional budget metrics; optional Helios norms as **cheap Zeus/Client** work — same spirit as Helios “nice to have.”  
**Depends on base-5:** frozen objects + company_context + settings/policy already ship (pack done; Client CR-20).

### Catalog / Client goals (all additive or optional)

1. **`wish_i_knew` hygiene** — already optional; shape/docs polish only.  
2. **G2 metrics hygiene** — never `summary`; dual path docs for `hooks_jailbreak_score` (base-5 already has dual scores).  
3. **Budget zone metrics (enforced reporting)** — size tags; caps already in base-5 design.  
4. **`hints` / Hot-Path / A/B paste** — **after** hard `rules`; hash-excluded; must not strip jailbreak rules.  
5. **Optional** terminate retry (“required four only”).  
6. **De-demo** efficiency prose.  
7. Customs filename smoke in scan + Client.  
8. **`ab_arm`** on report (cheap Client scalar).

### Helios goals (Pri-2/3 — optional / nice-to-have)

| Work | HEL-WISH | AI load |
| --- | --- | --- |
| `geo_norm` via Zeus geocode from QD `geo` | **001** | piggyback only |
| Client market geo | **002** | none |
| deployment / ruleset / mode / base_id slice | **016** | none |
| context dump metrics | **017** | none |
| multi_part normalize on Zeus | **012** | flag cheap |
| intent_norm map (Zeus first) | **005** | light if AI · optional_when |
| price_norm (Client slider preferred) | **004** | light if AI · optional_when |
| Tool fingerprint / chat recovery | **021, 020** | none |

### Explicit non-goals for base-6

- **Any breaking rename/remove** of base-5 wire keys  
- Full wishlist as always-on Layer A  
- HEL-WISH-010 on hot path  
- Auto-ban on jailbreak float  
- “Must wait for base-6 to have company_context” (already base-5)  

### Success signals

- [ ] Diff base-5 → base-6 shows **additive-only** (hints slots, metrics)  
- [ ] G2 metrics without UI leak  
- [ ] At least one `*_norm` path live without new **required** AI fields  
- [ ] lessons-learned / migration note if any optional fields added  

---

## base-7 — “Workbench + stamp + product events” (additive product)

**Jira:** epic **[CR-5](https://kotenai.atlassian.net/browse/CR-5)** · stories **CR-15**, **CR-16** · status To Do (future).

**Theme:** Productize authoring and ops; **no Layer A wire break** vs base-5. Helios product-path events remain optional/nice.

| Goal | Why | Breaking? |
| --- | --- | --- |
| Hub load/save base-N + custom rev | Customs lifecycle | No |
| Rules key/value editor + company_context word meter | Authors | No |
| Lint (rule length, dup keys, caps) | Catch bad packs | No |
| Preview assembled prompt + zone sizes | Debug | No |
| Prompt Helper A/B UI | Experiments | No |
| Stamp/verify for base-N | Real hashes | No |
| Detective: optional Layer A = **warn** not fail | Soften | No (softer) |
| COMPAT rows kept current | Versions | No |
| Compare / refine / demand events | HEL 018, 019, 011 | No (product) |

---

## base-8+ — “Pin + optional compression / AI-heavy”

**Jira:** epic **[CR-18](https://kotenai.atlassian.net/browse/CR-18)** — pin promote · **blocked by CR-20 + CR-21** · do not start until green.

| Idea | Why | Breaking wire? |
| --- | --- | --- |
| Promote base-N to `CURRENT` / `v2/min` | Users get diet | Pin gate only |
| Provider prompt-cache productization | Cost | No |
| Structured-output constrained `return` | Reliability | Optional path |
| Tool-history auto-summarize | Long sessions | No |
| TOON view for Workbench | Editor tokens | No (JSON SoT) |
| Per-mode default rule packs | Mode matrix | Additive packs |
| Soft AI JTBD/sentiment (**010**) | Insights | Off-path only |
| Constraints AI (006) if forms fail | Cost | Optional |
| Multimodal user parts | Product | Additive message parts |
| Require more Layer A fields | Quality | **Only with measured rates + new major if required** |

---

## Suggested sequencing (summary)

```text
base-4  Terminate table + Layer A scores (triggers still boolean[])
           │
base-5  ★ LAST BREAKING WIRE / CONTROL-PLANE FREEZE
        ★ rules{} + triggers{} (object-only; dual-read ≤1 Client release)
        ★ company_context + jailbreak pack + message_*
        ★ output_request (type+description) → app_output
        ★ settings bag + merge/freeze + policy table + hooks
        ★ inject security + multi-turn flags + cheap ops metrics
        ★ Helios Pri-1 = Zeus/Client emits only (nice spine, not Layer A tax)
           │
base-5.1 CONTENT on base-5 wire (not a wire break)
         ★ mode overlays in messages[].content (CORE + MODE_OVERLAY)
         ★ stop analytics×rename packs · DESIGN §14 personas
         ★ diff_modes / clone gate · Zeus modes/*.md port
           │
base-6+ ADDITIVE / OPTIONAL only
        soft hints/A/B · optional norms · Workbench · pin when green
        Helios nice-to-haves stay cheap providers · never re-break base-5 wire
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
2. **base-5 = last break; base-6+ = additive/optional only** — until a new major is justified.  
3. **Same 13 verbs** until proven otherwise.  
4. **One inspector** — Diff is the migration test.  
5. **Text for diet, JSON for ship.**  
6. **Helios: cheap provider first; nice-to-have never blocks pin.**  
7. **Sparse AI + true-only exceptions** (HEL-WISH-012).  
8. **Pin last.**  
9. **Settings ≠ prompt essays** — structured control plane ([PROMPT_SETTINGS.md](PROMPT_SETTINGS.md)).  
10. **Triggers = signals; Client policy + hooks = law.**  
11. **Hard rules before soft hints** (base-5 freeze; base-6+ soft only).  
12. **Ownership is explicit** — App / Client / AI set·unset·change ([BIBLE §2](BIBLE.md)).  
13. **Tool results are untrusted data** in the prompt.  
14. **Any base-6+ wire break** needs a new major BASE + `docs/migration/base-X_to_base-Y/` — **default is no**.  

---

## Open questions

1. Text pack review-only vs text→JSON import?  
2. `policy_action` required in tool schema or docs/tests only?  
3. Who owns Client spike (named triggers + `output_request` + settings bag + policy table + 007/009)?  
4. Who owns Zeus spike (003/014) vs this repo’s catalog docs?  
5. Max min-profile catalog KB?  
6. ~~When does `COMPAT.md` gain base-4/5 rows?~~ → **Done** (see [COMPAT.md](../COMPAT.md)); keep Client TBD floors updated  

7. Closed enums for `path.stage` / `intent_norm` — registry owner? (Helios §9)  
8. company_context: hard-truncate at 250 words in Client, or reject save in Workbench?  
9. A/B: one `ab_paste` slot vs named arms `ab.A` / `ab.B` in the paste UI?  
10. Jailbreak default `rules` object: ship as Client SDK defaults, Workbench template, or both?  
11. ~~Array→object dual-read: one release or two?~~ → **≤1 Client release, prefer 0**; objects only after  
12. `output_request` / settings API: top-level `run_agent(...)` kwargs vs nested only?  
13. Cap on `app_output` properties: 8 soft / 15 hard — enough?  
13b. Description soft max ~40 words / hard ~80 — enough for integrators?  
13c. Shorthand API: reject type-only vs require parallel `descriptions` map?  
14. Sticky flags: OR across session for all keys, or only business keys (jailbreak per-round)?  
15. `ruleset_id`: content hash vs Workbench version string?  
16. Force final `return`: always at `max_rounds-1`, or only after tool data exists?  
17. Frozen session prefix vs full re-assemble as Client v1 default?  
18. Any proposed base-6+ **breaking** change — force new major BASE? (**default yes**)

---

## Doc ownership

| Doc | Role |
| --- | --- |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Structured Helios Requests + priorities |
| [ROADMAP.md](ROADMAP.md) | BASE sequencing + Helios alignment |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers + Client `output_request` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold new base-N pack (`scripts/new_base.py`) |
| [COMPAT.md](../COMPAT.md) | Zeus × chat_request BASE × zeus_client matrix |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BIBLE.md](BIBLE.md) | Normative base-4 + §2 ownership |
| [RELEASE_NOTES.md](../RELEASE_NOTES.md) | What shipped + **breaking changes** |
| [migration/README.md](migration/README.md) | All BASE hops `base-X_to_base-Y` |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | AI comply / upgrade procedures |
| [../AGENTS.md](../AGENTS.md) | Repo AI entry |
| [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) | Experience (1→4 hop) |

---

*Align with Helios wishlist when HEL-WISH IDs change; revise BASE section when base-5 starts. Control-plane detail lives in PROMPT_SETTINGS.md.*
