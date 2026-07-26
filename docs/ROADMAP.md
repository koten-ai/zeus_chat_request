# BASE + Helios roadmap

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · **candidate line base-5.2** (`v2/base/base-5.2/`) · last wire break **base-5** · next content train **base-5.3 skinny + world-model + verb clarity** (planned) · version matrix: [COMPAT.md](../COMPAT.md)


**Status:** living plan after base-1 → base-4 → **base-5 / 5.1 / 5.2 candidate line**  
**Normative (base-4 era docs, base-5 wire freeze):** [BIBLE.md](BIBLE.md) · **Lessons:** [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) · [migration/base-4_to_base-5/lessons-learned.md](migration/base-4_to_base-5/lessons-learned.md) · [migration/base-5_to_base-5.2/lessons-learned.md](migration/base-5_to_base-5.2/lessons-learned.md)  
**Helios requests (analytics emits):** [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)  
**zeus_client backlog (implement floor):** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) (`ZC-WISH-*`)  
**base-5 inject / Layer A deltas:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) — **rules + triggers as objects**; Client **`output_request` → `app_output`** (each app field = **`type` + `description`**; type-only is not enough)  
**base-5 control plane:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) — **settings bag** · **rule pack merge/freeze** · **Client policy table** · cache zones · security · observability  
**Latency / skinny plan:** **§ Getting skinny** below — contract-safe tools[] · Hot Path empirics · stamped A/B · schema diet · measure AI floor  
**World-model language for packs:** **§ World model language for chat_request** — DESIGN vocabulary (AI-Ready overlay · mini-schema shape · access class · modes) · not form-fill  
**Verb catalog clarity:** **§ Verb catalog clarity** — base-5.2 13-API review vs Zeus `docs/API/V2/*.md` · description/schema gaps · P0 fixes  
**Ownership (set/unset/change):** [BIBLE.md §2](BIBLE.md)  
**Production pin:** still **base-1** (`CURRENT.json` / `v2/min`) until an explicit promote  
**Agent procedure:** [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) · hop [migration/base-4_to_base-5/](migration/base-4_to_base-5/)  
**Jira board:** [CR board 48](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48) · tracking table **§ CR board map** below

This is **what we want next and why**, not a commitment calendar.  
**Exception to “small bumps”:** **base-5 is intentionally the big wire/control-plane break** while nothing is in production on this line — then **base-5.x content / skinny** and **base-6+ additive/optional**.

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
9. Skinny path: full 13-verb platform stays; fewer tools only via stamped packs/A/B from Hot Path empirics
10. Measure AI floor honestly — catalog/control-plane trains ≠ automatic wall-ms wins; never unhash tools[] mid-chat
11. Chat_request teaches **world model + verbs** (DESIGN: AI-Ready overlay · mini-schema shape · access class) — not form-fill / slot extraction over raw tables
12. Each of the 13 tools teaches **when / when-not / KEY constraint** (aligned to Zeus V2 API docs) — not cost-tags alone
```

---

## BASE change law (post base-4)

No production traffic on the **base-4/5 line** yet. Use that:

| BASE | Allowed change type | Examples |
| --- | --- | --- |
| **base-5** | **BREAKING OK** — freeze the contract | Object rules/triggers · settings bag · policy table · `output_request` · company+jailbreak in prompt |
| **base-5.1** | **Content patch on base-5 wire** — **not** a new wire break | Restore **mode overlays** in system prompt (`messages[].content`); core+overlay; no Layer A rename |
| **base-5.2** | **Additive G2 design on base-5 wire** | Keep classic **`wish_i_knew`** + append **`data_gaps`** for Helios acquisition ([WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md)) |
| **base-5.3** | **Content skinny train on base-5 wire** — **not** a wire break | Prose no-rediscovery · **verb clarity** (desc + params vs V2 API) · schema diet · **usage-driven** skinny packs (stamped A/B) · world-model CORE blurb · **no** runtime strip of hashed verbs · **no** Layer A rename |
| **base-6+** | **ADDITIVE / OPTIONAL only** | Soft hints/A/B · optional_when fields · Workbench UX · Helios norms as cheap emits · pin when green |
| **Helios wishlist** | **Nice-to-have** (cheap provider first) | Pri-1 Zeus/Client report scalars — **never** required AI Layer A tax |

```text
base-5    = last wire/control-plane break before real adoption of this line
            Prefer one clean object contract over dual-read forever.

base-5.1  = content/diet train ON the base-5 wire (mode personas in prompts)
            Same schema objects / required four / app_output — packs stop being
            “analytics × rename”. See docs/MODE.md · work/RECREATE_MODE.md

base-5.2  = additive G2: classic wish_i_knew (ops) + data_gaps (Helios acquisition)
            Optional fields only; not a wire break of required four. See WISH_I_KNEW_DUAL.md

base-5.3  = SKINNY + WORLD-MODEL + VERB CLARITY on the base-5 wire
            Platform keeps 13 verbs; production wire = stamped contract verbs[]
            (do NOT strip tools mid-session when enforcement is on).
            Diet via prose + schema bytes + empirics → new stamped packs / A/B.
            Plus short DESIGN-aligned worldview in CORE + rewrite tool
            descriptions/params so they teach use (aligned to docs/API/V2).
            See § Getting skinny · § World model language · § Verb catalog clarity.

base-6+   = additive / optional_when / hash-excluded soft injects / productization
            No rename/remove of base-5 wire keys without a new major BASE + migration hop.

Helios    = analytics spine on Zeus/Client; optional_when if AI ever needed
            Never block pin on Pri-2/3/4/5 AI fields
```

**Naming note (normative):** train id **= pack folder = `_lineage.base_id`**.  
Examples: `v2/base/base-5/`, `v2/base/base-5.1/`, `v2/base/base-5.2/`.  
**Never** apply a train only via `content_train` on a parent pack — that blocks pull-by-path and simple JSON Diff.  
BASE ids are **not** Zeus or zeus_client semver.

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

## Latency law (chat wall time — every BASE + Client)

Detective-shaped truth (beer-sample / base-5.2 example, 2026-07-26):

| Slice | Typical share on a healthy 1-round turn |
| --- | --- |
| **`ai.chat.round.N` (LLM)** | **~95–99%** of wall |
| Zeus tool / pipeline execution | often **&lt;1–5%** when path is correct |
| Dispatch / inject / encode | noise unless broken |

**Implications:**

1. **base-5 / 5.1 / 5.2 were not latency trains.** They grew catalog quality (modes, dual gaps, control plane). System + verbs JSON on disk **increased** base-1 → base-5.2 — do not expect wall-ms to drop from pin alone.
2. **Structural wins** = fewer rounds + no rediscovery (`describe` / `get_stats` when inject is green) + one terminating `pipeline`. Measure **rounds**, `tool_calls_total`, **per-verb use rates**, and rediscovery rate — not only wall ms on already-1-round chats.
3. **Token wins** = shorter verb schemas (especially `return` / `pipeline`), smaller **completion**, stable prefix + prompt cache for multi-turn, and — only via a **new stamped pack/custom** — fewer tools in the hashed catalog.  
4. **Model floor** remains real: ~3s for one rich tool call on a “fast” model can still be `speed_grade=pass`. Skinny cannot invent a sub-second LLM if generation stays ~1k completion tokens.
5. **Fix inject before teaching discovery.** If `describe()` “because mini-schema wasn’t sent,” that is a **Client/Zeus inject** bug or a **missing inject** path — fix inject reliability; do **not** silently mutate the hashed tools list mid-chat.
6. **Contract enforcement law:** `verbs[]` participate in **`contract_hash`**. When enforcement is on, **do not strip tools from the wire at runtime** (e.g. “mini-schema present ⇒ drop `describe`”) — Zeus/Client will refuse or fail the turn as a contract mismatch. Skinny verb sets are **new stamps / A/B packs**, not per-turn list surgery.

Full plan: **§ Getting skinny**.

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
| **base-5.1 mode overlays** pack + CORE/overlay | Stop analytics×rename | **CR-23** |
| **base-5.2 dual gaps** design + pack path | `wish_i_knew` + `data_gaps` | **CR-24** |
| Latency diagnosis + skinny plan in ROADMAP | Honest AI-floor + verb surface | **CR-26** (this section) |
| base-5.2 13-verb review vs Zeus `docs/API/V2` in ROADMAP | Findings + P0/P1 clarity backlog | **CR-26** · § Verb catalog clarity |

| Still open | Risk | CR |
| --- | --- | --- |
| zeus_client implements object triggers + settings/policy/`output_request` | Catalogs ready; Client floor TBD | **CR-20** (+ CR-9/10/11) |
| Zeus loaders / return schema / Detective for base-5+ | Can’t pin | **CR-21** |
| **base-5.3 skinny** — schema diet + prose + **usage empirics → stamped A/B packs** | Catalog always-13 without evidence; AI floor stuck | **CR-26** |
| **base-5.3 world-model blurb** — DESIGN vocabulary in CORE (overlay / shape / access class) | Packs read as form-fill + tool list; join blindness | **CR-26** · § World model language |
| **base-5.3 verb clarity** — rewrite 13 tool desc/params; fix order/search schema mismatches | Model taught wrong knobs; empty `where` / wrong sort | **CR-26** · § Verb catalog clarity |
| Hot Path / Prompt Helper: per-verb use over last N runs | Guessing which verbs to diet | Workbench / Detective (CR-26 Phase 0–1) |
| Inject reliability (brief + mini-schema always on product path) | Model rediscovers when inject missing | Client + Zeus CR-20/21 |
| Helios Pri-1 report emits (cheap spine) | Not catalog tax | **CR-12** |
| Required four incomplete in the wild | Detective / soft-require levers | CR-21 + Client |
| CURRENT still base-1 | Expected until green | **CR-18** (blocked by CR-20/21) |
| base-6 soft injects | After Client floor + skinny prefer | **CR-4** |
| base-7 Workbench / stamp product | Later | **CR-5** |

**Pack SoT for new work:** **base-5 wire** · live candidate packs **base-5.1 / base-5.2** · next content train **base-5.3 skinny** (§ Getting skinny).  
**Production pin:** **base-1**.  
**Hop:** [migration/base-4_to_base-5/](migration/base-4_to_base-5/).  
**Modes:** [MODE.md](MODE.md) · plan [work/RECREATE_MODE.md](../work/RECREATE_MODE.md).  
**Client implement order:** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) §4 · add skinny settings to wishlist when CR-26 lands.

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
| **CR-23** | **base-5.1** mode overlays in system prompt | In Review / merge | § base-5.1 · [MODE.md](MODE.md) |
| **CR-24** | **base-5.2** dual `wish_i_knew` + `data_gaps` design | In Review / merge | § base-5.2 · [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) |
| **CR-25** | **Snapshot folders** base-5 / 5.1 / 5.2 + process | In Progress | This PR · process P0 |
| **CR-26** | **base-5.3 skinny + world-model + verb clarity** — schema diet · Hot Path empirics · stamped A/B · DESIGN CORE blurb · 13-verb desc/params vs V2 API | To Do (create if missing) | § Getting skinny · § World model language · § Verb catalog clarity · § base-5.3 |

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
8. **Verb schema diet (names stay)** — shorter descriptions · **deferred implement to base-5.3 skinny** (§ Getting skinny) while base-5 freezes wire.  
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
| **Wire** | Same as base-5 objects / app_output / required four (content on that wire) |
| **Content** | Mode personas: entities, join/noise posture, edges, don’ts, example pipelines |
| **On disk** | **`v2/base/base-5.1/`** full snapshot · parent `base-5` · Diff vs `base-5/` |
| **Generator** | Fill Zeus `ai/V2/prompt/core/modes/<mode>.md` (optional follow-up) |

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

- [x] [MODE.md](MODE.md) + [RECREATE_MODE.md](../work/RECREATE_MODE.md) authored  
- [x] CORE extracted; all 10 modes assembled CORE + overlay  
- [x] fraud / research / code / regulated (+ tenant/private/open/auto/custom) overlays in packs  
- [x] Keyword/entity smoke via `diff_modes.py --fail-if-clone`  
- [x] Neutralize-mode signatures unique per mode  
- [x] `verify_base_pack.py --base 5` OK  
- [ ] Zeus `modes/<mode>.md` ported (follow-up; dual-home = `work/mode_overlays/`)  
- [x] RELEASE_NOTES notes base-5.1 content train  
- [ ] CR-23 Done (after PR merge)  

### Sequencing vs other work

```text
base-5 pack (wire)  ──done──►  base-5.1 (mode prompts)  ──►  base-5.2 (dual gaps)
        │                            │                              │
        │                            │                              ▼
        │                            │                       base-5.3 (skinny)
        │                            │                              │
        └── Client CR-20 / Zeus CR-21 ┴──────────────────────────────┴── pin last
                                                                         │
                                                                    base-6 soft injects
```

Prefer **base-5.1 before or in parallel with Client spike** so trials exercise real mode personas, not 10 analytics clones.  
Prefer **base-5.3 skinny before pin** so production surface is not “always 13 + rediscover.”

---

## base-5.2 — “Dual gap channels: wish_i_knew + data_gaps”

**Jira:** **[CR-24](https://kotenai.atlassian.net/browse/CR-24)** · parent epic **CR-3**  
**SoT:** [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md)  
**Related:** [BIBLE.md](BIBLE.md) §5 · [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)

**Theme:** Keep the **classic** operator feedback channel (`wish_i_knew`) and **append** a Helios-oriented acquisition channel (`data_gaps`) when the model cannot fully answer because **schema / data / index** is missing. Both G2, optional, never chat UI. **Additive** on base-5 wire — not a required-four break.

| Stream | Field | Consumer |
| --- | --- | --- |
| **A classic** | `wish_i_knew[]` (keep) | Detective, Workbench, prompt ops |
| **B acquisition** | `data_gaps[]` (new) | Helios backlog / Motions (+ precomputed counts) |

### Goals

1. Design doc with A vs B rules and examples.  
2. Additive wire: keep array `wish_i_knew`; add optional `data_gaps` with machine keys.  
3. Document Zeus string dual-read for A; Helios cost law for B.  
4. Implement PR later: schema + terminate table + Client/Zeus parse + report rollups.

### Explicit non-goals

- Require A or B every turn  
- Nest-break `wish_i_knew` into `{feedback, acquisition}` without dual-read  
- Soft HINTS/A/B (**base-6**)  
- Pin promote  

### Success signals

- [x] [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) design authored  
- [x] ROADMAP § base-5.2  
- [x] CR-24 created  
- [ ] Design PR merged to main  
- [ ] Schema + pack terminate table implement (follow-up)  
- [ ] Client/Zeus parse + Helios precomputed counters  

---

## Getting skinny — latency + verb surface plan

**Jira:** **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** (create if missing) · parent epic **CR-3**  
**Train:** **base-5.3** (content on base-5 wire — **not** a Layer A / object break)  
**Related:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · Zeus `docs/API/V2/describe.md` · Detective / Hot Path / Prompt Helper · stamp + `contract_hash`  

**Why now:** base-5 → 5.2 improved contracts, modes, and dual gaps. Live Detective packs show wall time still dominated by **`ai.chat.round.*`**. Catalog bytes grew. Operators still see wasteful **`describe()`** (sometimes because inject was missing — a different bug). We need an explicit **skinny** train — and we must **not** “optimize” by mutating the hashed tool list mid-session.

### North star (skinny)

```text
1. Platform keeps all 13 Zeus verbs (names + HTTP stay)
2. Production tools[] = stamped contract verbs[] when enforcement is on
3. Prefer inject + data plane over rediscovery; teach via prose, not runtime strip
4. Prefer one terminating pipeline over multi-round orientation
5. Measure: rounds, per-verb use rates, rediscovery, tokens, ai_ms — not vibes
6. Drop verbs only after empirics → new stamped pack / A/B arm (re-hash)
7. Never grow always-on Layer A for Helios or “maybe useful” fields
```

### Law: hashed contract owns tools[] (critical)

`verbs[]` (OpenAI-style tools) participate in **`contract_hash`** when a pack is stamped. With **contract enforcement on**:

| Do | Don't |
| --- | --- |
| Ship the **full stamped** tools list for that pin | **Strip** `describe` (or any verb) from tools[] mid-chat because mini-schema arrived |
| Re-pin / re-stamp a **new** pack/custom that omits unused verbs | Mutate tools[] after bind and expect Zeus to execute happily |
| Use **prompt prose** + inject reliability so the model *doesn't call* escape verbs | Assume “deny after the model already planned the call” is free |
| Use **Prompt Helper / Hot Path / A/B** to *decide* which verbs to drop next stamp | Guess a subset without run data |

**Why strip-at-runtime fails:** Client/Zeus bind a pin to a hash of catalog body including tool schemas. If tools[] on the wire no longer match the stamped contract, **enforcement refuses the chat or tool path** — the “optimization” becomes a hard failure.

**Hooks `denied_verbs`:** fine for **safety** (refuse a call the model still *could* name) — that is not the same as removing the tool from the LLM tools list under a stamped hash. Safety deny after a wasted tool_call is still a wasted round. Prefer not listing a verb only in a **new stamped** skinny pack used by A/B or a deliberate pin.

### How to actually drop APIs (right venues)

| Venue | Role in skinny |
| --- | --- |
| **Hot Path / Detective analytics** | Over last **N hundreds of runs** (scope/mode/pin): count uses of each of the 13 verbs. Output: never / rare / common. |
| **Prompt Helper** | Operator co-pilot: surface the use histogram, propose “drop candidates,” draft a skinny custom or guidance, run books. |
| **A/B testing** | Arm A = current full stamp; Arm B = **re-stamped** pack with candidate verbs removed (or thinner schemas). Promote B only if quality + latency win. |
| **base-5.3 content pack** | Prose + schema **byte** diet on the full-13 baseline (still hashable); optional **documented** skinny customs once empirics exist. |
| **Production pin** | Change verb membership only by **promoting a stamped** skinny pin — never by Client list surgery. |

#### Empirical report shape (target)

```text
window: last 500 runs · scope=beer-sample/_default · mode=analytics · pin=base-5.2
verb          calls   runs_with≥1   share_of_tool_calls
return          …         …              …
pipeline        …         …              …
search          …         …              …
find            …         …              …
…
describe        …         …              …   ← rediscovery rate vs inject_green
explain         …         …              …
```

**Decision rule (sketch):**

```text
never used in window     → strong A/B drop candidate (keep on platform)
hardly used (< threshold)→ drop candidate or workbench-only pack
often used + wasteful    → prose / inject fix first (e.g. describe + inject green)
always needed            → keep; diet schema text only
```

Pair with **inject_green** × **describe_called** so “describe because schema missing” is separated from “describe despite schema present.”

### Verb tiers (planning / A/B design — not runtime mutation)

Use as a **hypothesis** for Hot Path reports and skinny stamps; do **not** apply as per-turn tools[] surgery under enforcement.

| Tier | Verbs | Role |
| --- | --- | --- |
| **Usually hot** | `find`, `search`, `get`, `order`, `project`, `set`, `enrich`, `pipeline`, `return` | Data + shape + terminate on healthy packs |
| **Conditional** | `traverse` | Graph / walk_path scopes |
| **Job / heavy** | `analyze` | Analytics jobs / Motions |
| **Escape / debug** | **`describe`**, **`explain`** | Orientation + planner — valuable when inject missing or admin; costly as default habit |

#### `describe` — normative guidance (still true)

From Zeus (`docs/API/V2/describe.md`): `describe` is the **callable companion** to the brief/schema — **never a replacement**.

| Inject state | **Correct** response | **Wrong** response under enforcement |
| --- | --- | --- |
| BRIEF + MINI-SCHEMA **present** | Prose: do not rediscover; model should skip `describe`. Metrics if it still calls. | Strip `describe` from tools[] for this turn only |
| Inject **missing / bad** | **Fix inject** (or use a pack/session that includes `describe` by stamp); treat as reliability incident | Leave broken inject and hope discovery saves quality every time |
| User asks fresh inventory / indexes | Model may call `describe` (tool still on stamped list) | — |
| Workbench / Prompt Helper | Full 13 or experiment arms | — |

```text
Inject OK?  → use brief/schema; call data-plane verbs (still all listed if stamp says so)
Inject bad? → fix inject / re-assemble; do not “unhash” the catalog
Want fewer tools? → new stamp / A/B arm from Hot Path empirics
```

### What actually moves the AI floor

| Lever | Owner | Effect | Contract-safe? |
| --- | --- | --- | --- |
| **Prose no-rediscovery** | catalog base-5.3 | Fewer wasteful first calls | Yes (same tools[]) |
| **Verb schema diet** (names stay) | catalog base-5.3 | Less prompt tokens | Yes |
| **Verb clarity** (desc + params vs V2) | catalog base-5.3 | Fewer wrong tools / empty results | Yes — same 13 names |
| **Soft Layer A diet** | Client `output_request.layer_a` | Less completion | Yes (settings, not hash body if excluded) |
| **Inject reliability** | Client + Zeus | Stops “describe because no schema” | Yes |
| **Hot Path verb histogram** | Workbench / Detective | Evidence for what to drop | Yes (observe only) |
| **A/B skinny stamped pack** | Hub stamp + Prompt Helper | Real tools[] reduction | Yes — **new hash** |
| **Runtime strip tools when inject green** | — | Breaks enforcement | **No** |
| **Tool-history truncate** | Client multi-round | Round 2+ size | Yes |
| **Inject text diet** | Zeus Client | Moderate | Yes |
| **Model SKU** | App settings | Large | Yes |
| **One terminating pipeline** | catalog prose | Structural | Yes |

### Explicit non-goals (skinny)

- Removing verbs from Zeus / OpenAPI platform  
- **Runtime** remove/rewrite of stamped `tools[]` under contract enforcement  
- Renaming or dropping required four Layer A fields  
- Replacing inject with `describe` as the schema channel  
- Expecting base-5.3 prose alone to turn a 3s LLM call into &lt;1s if completion stays large  
- Stuffing more Helios fields into terminate “while we’re dieting”  
- Soft A/B *hints* as the only latency control without **stamped** tool-set A/B when dropping verbs  

### Phased plan

#### Phase 0 — Measure (now)

| Action | Owner | Success |
| --- | --- | --- |
| Gold set: same questions on base-1 vs base-5.2, same model | Ops / Prompt Helper | wall, ai_ms, rounds, tokens, rediscovery |
| **Per-verb use histogram** over last N runs (mode/scope/pin) | Hot Path / Detective | never / rare / common table |
| Cross-tab: `describe` × inject present | Detective | split “schema missing” vs “ignored schema” |
| Zone sizes: system / tools JSON / inject | inject_inspect | which zone dominates |

#### Phase 1 — Prompt Helper + Hot Path product (primary “drop API” path)

| Action | Owner | Success |
| --- | --- | --- |
| UI/report: “of 13 verbs, last N runs: unused / rare / hot” | Workbench Prompt Helper | Operators see candidates without guessing |
| Propose skinny **custom** or A/B arm from histogram | Prompt Helper | Draft pack with fewer verbs **for stamp** |
| A/B run full-13 stamp vs skinny stamp | Workbench A/B | promote only if quality holds |
| Document: **never** strip tools mid-session when enforcement on | docs / Hub | Operators don’t ship the anti-pattern |

#### Phase 2 — base-5.3 pack content (this repo)

| Action | Owner | Success |
| --- | --- | --- |
| **CORE world-model blurb** (DESIGN vocab — § World model language) | catalog | ≤ ~180 words; all modes via CORE + overlay |
| **Verb clarity P0–P1** (order/find/search/describe/get/traverse/pipeline — § Verb catalog clarity) | catalog | Schema matches Zeus V2; system example uses `asc` + `field:` |
| Pack prose: no rediscovery when inject present; `describe` = fallback, not default habit | catalog | Diff vs base-5.2 |
| Verb schema diet: drop duplicate Terminate text in params; keep KEY constraints | catalog | Clearer, not necessarily longer overall |
| Terminate one-liner: Layer A from evidence only | catalog | No field rename |
| Document empiric → stamp workflow (Hot Path → A/B → pin) | ROADMAP + playbook | Agents don’t invent runtime strip |
| Optional: **example** skinny custom in samples/ (not production pin) | pack | Template for A/B |
| `verify_base_pack.py` + Diff | process | Green |

Production default pin may **keep all 13** until Hot Path evidence says a skinny stamp is safe.

#### Phase 3 — Inject + multi-turn polish

| Action | Owner | Success |
| --- | --- | --- |
| Inject reliability: product path always sends brief + mini-schema | Client + Zeus | describe-for-missing-schema rate → 0 |
| Scope-aware inject diet (no empty noise; keep zero-row guards) | Zeus | Smaller inject |
| Multi-round tool body prune | Client | Round N doesn’t explode |
| Prompt-cache stable zones | Client + provider | Multi-turn savings |

#### Phase 4 — Optional later (base-6 / base-8+)

| Action | When |
| --- | --- |
| Soft hints that reduce bad paths without growing Layer A | base-6 |
| Productized prompt-cache | base-8+ |
| Structured-output constrained `return` | provider-proven |
| Promote skinny stamp to CURRENT only after gold + Hot Path green | pin gate |

### Success signals (skinny overall)

- [x] Latency law + skinny plan written in ROADMAP  
- [x] **Contract law:** no runtime strip of hashed tools under enforcement (documented)  
- [x] base-5.2 13-verb review vs V2 API findings in ROADMAP (§ Verb catalog clarity)  
- [ ] CR-26 on board (create if missing)  
- [ ] Phase 0 gold + **per-verb histogram** baseline  
- [ ] Prompt Helper / Hot Path surfaces never/rare/common verbs  
- [ ] At least one A/B: full stamp vs skinny stamp (re-hashed)  
- [ ] base-5.3 pack: prose + **verb clarity P0** + schema diet; Diff content-only  
- [ ] Rediscovery rate down **without** breaking enforcement chats  
- [ ] Inject-missing rate down (root cause for many `describe` calls)  
- [ ] COMPAT / RELEASE_NOTES note base-5.3 skinny train  
- [ ] ZC-WISH / Workbench notes: empirics → stamp, not mid-turn tools[] edit  

### Sequencing vs other work

```text
base-5.2 (dual gaps) ──► base-5.3 skinny + world-model + verb clarity
        │                      │
        │                      ├── CORE blurb (DESIGN overlay / shape / access class)
        │                      ├── Verb clarity P0–P1 (order/find/search/… vs V2 API)
        │                      ├── Hot Path / Prompt Helper (Phase 1) can lead
        │                      ├── A/B skinny stamps before production pin change
        │                      └── do NOT “fix inject ⇒ drop describe” under enforcement
        │
        └── Helios Pri-1 stays Zeus/Client report emits
```

Prefer **measure → A/B stamp → pin**, not **strip tools because inject looked green**.  
Prefer **short DESIGN worldview in CORE** over pasting foundation essays.  
Prefer **verb clarity before aggressive tool-count diet**.

---

## World model language for chat_request (DESIGN vocabulary)

**Jira:** folds into **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** (base-5.3 content)  
**Upstream SoT (Zeus product design):**

| Doc | Use for |
| --- | --- |
| [zeus_design_docs DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) §1 | **AI-Ready overlay** — source targets vs Zeus store; never mutate source bodies |
| DESIGN.md §7 (tool classes) + §7.8 | **Access class** (discovery / kv / lookup / vector / traversal / …) · **MINI-SCHEMA = shape** (legal `where`, FTS vs GSI, FK / inverse_fks, walk_paths) |
| DESIGN.md §14 | **Modes** — persona + limits (hop caps, confidence floors); analytics = safe default |
| [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) | E–T–E ancestry · **schema-as-world-model** vs form · “predicates as verbs for discovery” |

**Gap today (base-5.2):** packs already *have* tools, brief, mini-schema, and mode overlays, but they read like **efficiency + Layer A form**. The DESIGN / foundation thesis — *overlay world map + instruments, not form-fill* — is **implicit**, not taught. Layer A terminate is intentionally form-shaped (emit contract); the **data path** must not be taught the same way.

### Prefer / avoid (catalog copy)

| Prefer (DESIGN-aligned) | Avoid (as the main story) |
| --- | --- |
| **AI-Ready overlay** — project identity/relations from operator data; source of record stays owner’s docs | “Dump the table / fill the spreadsheet” |
| **World map** — entity types, attributes, edges/FKs, samples in SCOPE BRIEF + MINI-SCHEMA | Schema as **slots to invent values into** |
| **MINI-SCHEMA = shape** — legal `where` keys, index kind (`gsi` / `fts` / `display`), `fk_to`, `inverse_fks`, walk_paths | Treating every field as equality-filterable |
| **Access class / lens** — pick verb by how the fact is stored (id → get, equality → find, language → search, hop → traverse) | One giant “answer from context” or invent joins |
| **Navigator** — plan, call tools, answer from evidence | **Clerk** — invent nulls / SKUs / counts into a form |
| **Predicates for discovery** (tool args grounded in map) | Predicates as **field slots for invention** |
| **Mode** bounds hops, join noise, confidence floor | Unbounded multi-hop “explore everything” |
| Layer A terminate = **emit contract from evidence** | Layer A = invent analytics facets when tools found nothing |

### Two contracts (must stay distinct in prose)

```text
1) DATA contract  — world model in front of the model
   SCOPE BRIEF + MINI-SCHEMA + verbs → retrieve / hop / filter → evidence

2) EMIT contract  — Layer A terminate (required four + recommended)
   summary / QD / decomposition / confidence … filled FROM evidence
   (Helios/Client shape — not a substitute for retrieval)
```

base-5.2 already has (2) strong and (1) mechanical. base-5.3 must **name (1)** in ~one short CORE block so the model does not collapse both into form-fill.

### Canonical short blurb (draft for CORE — ship in base-5.3)

Keep **≤ ~120–180 words** in shared CORE (all modes). Mode overlays stay thin (DESIGN §14 persona). Do **not** paste DESIGN.md or the foundation essay.

```text
## How Zeus data works (read this once)

Zeus is an AI-Ready overlay over operator-owned documents: it projects
entities, attributes, and relations you can navigate — it does not replace
the system of record, and you must not invent facts into empty fields.

1) World map (already in this message when present)
   - SCOPE BRIEF = scale + vocabulary for this scope/mode
   - MINI-SCHEMA = shape: legal where keys, index kind (gsi|fts|display),
     entity_fk / inverse_fks, samples (ex:). Absence ≠ invent.
   - WALK_PATHS (if present) = pre-validated FK chains

2) Access path → verb (prefer cheapest that answers)
   - id / exact key     → get
   - equality / GSI     → find  (where only on [gsi] / scalar paths)
   - language / text_fts → search (never put text_fts paths in find where)
   - multi-hop / graph  → traverse (respect mode hop caps; real links > noise)
   - multi-step         → pipeline; terminate with return (or terminating pipeline)

3) Answer from evidence only
   - Layer A fields are an emit contract: fill from tool results / brief.
   - Missing data → clarify, empty rows, or wish_i_knew / data_gaps — do not invent.
```

**Company / tenant texture** stays in **`company_context`** (hash-excluded inject), not CORE:

```text
# company_context pattern (App/Client — ≤150 soft / 250 hard words)
- Durable things: people / places / things (or domain names: Beer, Brewery, …)
- Key links / events: which FK or edge is the “transaction” (e.g. Beer.brewery_id → Brewery)
- Measures vs language fields (align with mini-schema kinds)
- What “good evidence” means for this product (mode may tighten)
```

Beer-sample example (illustrative only):

```text
Beer and Brewery are the durable product/org entities.
Beer.brewery_id is the link Beer → Brewery (GSI FK; reverse = inverse_fks on Brewery).
name/description are language (text_fts → search); abv/ibu/srm are measures (gsi → find/order).
```

### Where each phrase lives

| Phrase / idea | Home | Hashed? |
| --- | --- | --- |
| Overlay + map + access path blurb | CORE system (base-5.3) | Yes |
| Mode hop/join/confidence posture | MODE_OVERLAY (already base-5.1) | Yes |
| Live shape + samples + walk_paths | SCOPE BRIEF / MINI-SCHEMA inject | No (runtime) |
| This business’s E–T–E story | `company_context` | No |
| Hard law | `rules{}` | Yes (merged freeze) |
| Layer A table + example | Terminate section (keep short) | Yes |
| Optional path hints | base-6 `hints.*` | No |

### Implementation plan (with skinny)

| Step | Owner | Deliverable |
| --- | --- | --- |
| 1. Land draft blurb in `work/mode_overlays/CORE.md` (or pack text SoT) | catalog / CR-26 | Diff vs base-5.2 shows one new short section |
| 2. Re-assemble all 10 modes CORE + overlay | `assemble_mode_prompts.py` | base-5.3 packs |
| 3. One line in Terminate: “Layer A from evidence only — not a second form for inventing data” | catalog | No Layer A field rename |
| 4. `company_context` recipe + beer example in BIBLE / PROMPT_ASSEMBLY or this ROADMAP | docs | Client authors know what to write |
| 5. Detective / gold: multi-hop + FTS questions still pass; no rediscovery spike | ops | Quality gate |
| 6. Optional: Prompt Helper chip “world model” points at blurb + mini-schema | Workbench | Later |

### Explicit non-goals

- Replacing MINI-SCHEMA with a long ontology essay  
- Teaching REA/ER/Kimball names in the hot system prompt (keep in design docs / talks)  
- Softening required four or growing always-on Helios Layer A fields  
- Runtime tool strip when inject green (still forbidden under enforcement)  
- Path B2 “restrict chat to raise hit rate” as the primary product story — modes/contracts bound **verbs and boundaries**, they do not replace a legible map ([ENTITY foundation](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) §7)

### Success signals

- [x] Vocabulary + draft blurb written in ROADMAP  
- [ ] CORE blurb in base-5.3 packs (≤ ~180 words)  
- [ ] Diff base-5.2 → base-5.3 shows worldview + skinny diet, no wire break  
- [ ] `company_context` pattern documented for Client (ZC-WISH / PROMPT_SETTINGS cross-link)  
- [ ] Gold: multi-entity / FK questions prefer find+link or traverse/walk over invent  
- [ ] Operators can point sales/docs at DESIGN §1 + foundation; chat_request stays short

### Why this also helps “faster” Zeus plans

| Effect | Mechanism |
| --- | --- |
| Fewer wrong first verbs | Access-class rule (fts → search, gsi → find, id → get) |
| Fewer join-blind pipelines | FK / inverse_fks / walk_paths as first-class in the story |
| Fewer invent rounds | “Absence ≠ invent” + emit-from-evidence |
| Not a free TTFT win | Single clean FTS round still pays the model floor (~3s) |

---

## Verb catalog clarity (base-5.2 review → base-5.3)

**Jira:** folds into **[CR-26](https://kotenai.atlassian.net/browse/CR-26)**  
**Reviewed:** 2026-07-26 · pack `v2/base/base-5.2/min/chat_request_*_base-5.2.json` (analytics representative)  
**SoT for behaviour:** Zeus [`docs/API/V2/*.md`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2) (`describe`, `get`, `find`, `traverse`, `search`, `analyze`, `explain`, `pipeline`, `return`, `transforms.md`)  
**Related:** § Getting skinny (diet / empirics) · § World model language (access path chooser in CORE)

### Verdict

base-5.2 tool surface is **uneven**. `search` and `return` teach well; most others are **cost tags + short labels** that do **not** encode the V2 docs’ “facts the LLM gets wrong constantly.” System essay partly compensates, but models weight **tool schemas** heavily — and several schemas **omit or contradict** real params (especially **order** vs system `direction`).

| Area | Grade (base-5.2) |
| --- | --- |
| `return` Layer A wording | Strong |
| `search` THINK line | Strong idea; schema incomplete vs examples |
| System efficiency / ranking prose | Partial; **order/direction bug** |
| Most tool `description`s | Too thin vs V2 |
| Param docs / demux completeness | Major gap |
| Transform verbs (`set`/`order`/`enrich`/`project`) | Under-taught pipeline glue |

### Cross-cutting issues

| Issue | Impact |
| --- | --- |
| Cost tags only (`[cheap]` / `[mod]` / `[exp]`) without when/when-not | Wrong first tool |
| Almost no param `description`s (except Layer A on `return`/`pipeline`) | Guessed `where` / `by` / `shape` |
| **System prose ≠ schema** | Ranking teaches `direction`; API uses `asc` + `field:<name>` |
| Examples only on `search` | Other demux verbs under-specified |
| Missing wire params that API accepts | `timeout_ms`/`where`/`seed_node_id` on search; `include` on describe; `asc`/`limit` on order; traverse shape knobs |
| Access-class chooser not on tools | Lives only weakly in system essay |
| `pipeline.steps` only types `as`+`verb` | Flexible bag; weak binding teaching |

### Description pattern (normative for base-5.3)

Every verb description:

```text
[cost] <what it does in one phrase>.
WHEN: …
WHEN NOT: …
KEY: <the V2 “LLM gets wrong” fact> …
```

| Target length | Verbs |
| --- | --- |
| ~80–160 chars | cheap transforms (`set`, `order`, `enrich`, `project`, thin `get`) |
| ~200–350 chars | demux / heavy (`find`, `search`, `traverse`, `pipeline`, `describe`, `analyze`) |

- Add **param `description`** on every non-obvious property (especially demux keys: `return`, `strategy`, `shape`, `by`, `include`, `job`).  
- Prefer **KEY constraints** over pasting full API pages into every description.  
- 1–2 `examples` on demux verbs when schema is non-obvious (keep total tools JSON honest vs base-5.2).

### Optional CORE one-liner (pairs with § World model language)

```text
Access path → verb
  exact id            → get
  equality / [gsi]    → find  (where equality only)
  language / text_fts → search (strategy:fts|hybrid)
  connected / hops    → traverse (or walk_path from WALK_PATHS)
  multi-step          → pipeline (bind @step.ids)
  final answer        → return OR terminating pipeline
  fresher inventory   → describe (only if brief/schema insufficient)
  corpus analytics    → analyze (heavy; may pending)
```

### Per-verb findings (base-5.2 → improve)

#### `describe` — weakest / most misleading

| Catalog (5.2) | V2 truth | Improve |
| --- | --- | --- |
| `[cheap] describe`; **empty params** | Companion to brief, **not replacement**; `include` defaults stats/entity_types/edge_types; metadata only | WHEN NOT inject green; add `include`; never returns rows |

Draft:

```text
[cheap] Scope orientation (stats/entity_types/edge_types). Use ONLY if SCOPE BRIEF /
MINI-SCHEMA missing or user asks for fresh inventory/indexes. Never a substitute for
inject; never returns node rows — use find/search for data. Optional include:
[stats|entity_types|edge_types|modes|tools|indexes] (default first three).
```

#### `get` — underspecified

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[cheap] exact by id` | Hydrate after find/search; ids 1..50; no `where` | Not a query; `include: body` opt-in; max 50 |

#### `find` — core verb, schema too thin (**P0**)

| Catalog | V2 | Improve |
| --- | --- | --- |
| predicate lookup + count/topK | **`return` is router**; `where` equality-only; MINI-SCHEMA authoritative | Desc + param docs; never text_fts in `where` |

Draft:

```text
[cheap] GSI/predicate anchor. return routes: rows|ids → find_nodes; count → count;
selectivity → entity_selectivity. where is EQUALITY-ONLY on MINI-SCHEMA [gsi]/scalar
paths — never text_fts (use search). Prefer return:ids then project/get.
entity_type = exact MINI-SCHEMA name.
```

#### `traverse` — router without map

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[mod] graph walk` | `shape` demux hop\|bfs\|path\|subgraph\|walk_path | Document shape + nested `walk_path`; seed from find/search first |

#### `search` — best description; schema lags examples (**P0**)

| Strength | Gap |
| --- | --- |
| THINK: fts vs find, entity_type exact, timeout | `timeout_ms`, `where`, `seed_node_id` in **examples** not **properties** |
| Strategy enum | Per-strategy required inputs (spatial → seed; hybrid → query_text) under-taught |
| | Spatial example may omit `entity_type` while schema requires it — align |

#### `analyze` — opaque job list

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[exp] analytics job` | Offline-backed; **pending ≠ fail**; mode-gated | WHEN NOT ordinary Q&A; pending/mode notes; optional `params` object |

#### `explain` — almost empty

| Catalog | Improve |
| --- | --- |
| `planner pass-through` | WHEN: cost/debug before heavy plan; not end-user answer — or mark workbench-primary |

#### Transforms — pipeline glue under-taught (**order = P0**)

| Verb | Catalog | Real contract | Priority |
| --- | --- | --- | --- |
| `set` | set ops on ids | 2..8 lists; union\|intersect\|difference\|xor | P2 — compose prior step id lists |
| **`order`** | sort ids | `by`: `id` \| `created_at` \| **`field:<name>`**; **`asc` bool** (default true); `limit` | **P0** — system + example use **`direction`** (wrong) |
| `enrich` | decorate ids | attach fields; preserve rank/cardinality | P2 — vs project |
| `project` | shape rows | `fields` allow-list; optional `format` | P2 — final user-facing rows |

**Critical mismatch (fix in same train):**

```text
WRONG (base-5.2 system example / prose):
  order … by: "<field>", direction: "desc"

RIGHT (Zeus order tool / transforms.md):
  order … by: "field:abv", asc: false, limit: 10
```

#### `pipeline` — good terminate hook; weak step grammar

| Strength | Gap |
| --- | --- |
| Prefer multi-step; Layer A terminate | steps only `as`+`verb`; no `@step.ids` in tool desc |
| | `return[]` omit ⇒ last step only; no `abort_if_empty` / `narrow_to` in desc |

Draft:

```text
[mod] Preferred multi-step DAG (max 8). Bind prior ids as @step.ids (not bare @step).
Put terminating Layer A fields top-level (same as return) to end the turn in one round.
Typical: find|search → order → project. One scope only.
```

#### `return` — strongest Layer A teaching

Minor polish: prefer terminating pipeline when multi-step already planned; keep required four.

### Priority backlog (implement in base-5.3 packs)

| P | Change | Why |
| --- | --- | --- |
| **P0** | Align **order**: schema + system example (`field:<name>`, `asc`, not `direction`) | Prompt teaches wrong API |
| **P0** | **find** desc: equality-only `where` + MINI-SCHEMA + `return` router | Zero-row bugs |
| **P0** | **search** properties: `timeout_ms`, `where`, `seed_node_id` (match examples/API) | Schema lies about wire shape |
| **P1** | **describe** not replacement for brief; add `include` | Rediscovery habit |
| **P1** | **get** hydrate-not-query; body opt-in | Wrong first tool |
| **P1** | **traverse** shape demux + walk_path vs edges | FK vs graph confusion |
| **P1** | **pipeline** `@step.ids` + terminate top-level in desc | Binding errors |
| **P2** | **set / enrich / project** when-to-use vs each other | Pipeline quality |
| **P2** | **analyze** pending / mode-gated | False “broken job” |
| **P2** | **explain** purpose or workbench-primary note | Clarity |
| **P3** | 1–2 mini-examples per demux verb (keep size honest) | Few-shot without essay |

### Explicit non-goals (verb clarity)

- Deleting platform verbs or changing HTTP paths  
- Runtime strip of tools when inject green (still § Getting skinny law)  
- Duplicating full V2 pages into every `description`  
- Growing Layer A required fields while clarifying tools  
- Renaming verb names (stability law: same 13 names)

### Success signals

- [x] Findings written in ROADMAP (this section)  
- [ ] P0 order/find/search fixed in base-5.3 packs + system examples  
- [ ] P1 describe/get/traverse/pipeline desc+key params  
- [ ] Diff base-5.2 → base-5.3 shows clearer tools; gold ranking/sort cases pass  
- [ ] Spot-check: no `direction` on `order` in any mode system text  
- [ ] Optional: gold cases for empty-where (text_fts mis-use) improve  

### Sequencing

```text
base-5.2 (current candidate)
    │
    ▼
base-5.3 content train (single pack bump preferred)
    ├── Verb clarity P0–P1  (this section)
    ├── World-model CORE blurb
    ├── Skinny prose / schema diet / empiric workflow docs
    └── (later) Hot Path A/B skinny stamps — not mid-session strip
```

Prefer **clarity before aggressive tool-count diet**: a wrong `order`/`where` costs more than an extra listed verb.

---

## base-5.3 — “Skinny + world-model + verb clarity” (content on base-5 wire)

**Jira:** **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** · parent epic **CR-3**  
**SoT:** § Getting skinny · § World model language · § Verb catalog clarity · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · Hot Path / Prompt Helper  
**Upstream words:** [DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) §1 · §7.8 · §14 · [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md)  
**Upstream API:** Zeus [`docs/API/V2`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2)  
**Theme:** Cut **token weight** and **bad rediscovery habits**; teach **overlay + map + access class** in short CORE prose; **rewrite 13 verb descriptions/params** so they teach correct use; cut **tool membership** only via **new stamps** from run empirics.

| | |
| --- | --- |
| **Wire** | Same base-5 objects / required four / app_output |
| **Content** | World-model blurb · **verb clarity (P0–P1)** · no-rediscovery prose · schema diet · empiric skinny-pack docs |
| **Workbench** | Hot Path verb histogram; A/B full vs skinny **stamped** packs |
| **Not** | Runtime inject-green tool list mutation under contract enforcement |
| **On disk** | **`v2/base/base-5.3/`** full snapshot · parent `base-5.2` · Diff vs `base-5.2/` |

### Goals

1. Document **hashed tools[] law** (enforcement ⇒ no mid-session strip).  
2. **CORE world-model blurb** (DESIGN: AI-Ready overlay · MINI-SCHEMA shape · access path → verb · evidence-only Layer A).  
3. **Verb catalog clarity** — align descriptions/params with V2 API; fix order/search mismatches (§ Verb catalog clarity).  
4. Prose: prefer inject; `describe` is fallback / freshness, not default orientation.  
5. Verb schema diet — drop duplicate Terminate text; keep KEY constraints.  
6. Hot Path + Prompt Helper: never/rare/common over last N runs → A/B candidates.  
7. Optional skinny customs / arms as **re-stamped** experiments — promote when green.  
8. `company_context` recipe for tenant E–T–E (Client inject).  
9. Gold-set non-regression on required four; size targets in RELEASE_NOTES.

### Explicit non-goals for base-5.3

- Delete Zeus platform verbs or change HTTP paths  
- Client “if mini-schema then remove describe from tools[]” under enforcement  
- Rename/remove required four  
- Long ontology / REA lecture in system prompt  
- Soft HINTS-only latency plan without stamp workflow  
- Pin promote (**CR-18**) without Hot Path evidence for any skinny pin  

### Success signals

- [ ] `v2/base/base-5.3/` scaffold + verify  
- [ ] Diff base-5.2 → base-5.3 is content only (world-model + verb clarity + skinny diet)  
- [ ] **P0:** order uses `field:` + `asc`; no system `direction`  
- [ ] **P0:** find/search KEY constraints + search properties complete  
- [ ] Contract/enforcement law called out in pack OVERVIEW  
- [ ] CORE blurb present in all 10 modes; mode overlays still distinct  
- [ ] Hot Path histogram path documented (even if implement lags pack)  
- [ ] Gold set + lessons-learned hop  
- [ ] CR-26 Done when prose/diet + worldview + verb clarity + empiric workflow are clear (Workbench may lag)

---

## base-6 — “Additive soft inject + optional Helios norms”

**Jira:** epic **[CR-4](https://kotenai.atlassian.net/browse/CR-4)** · stories **CR-13**, **CR-14** · status To Do (correct until base-5 Client residual prefers green).

**Theme:** **No breaking wire changes vs base-5.** Soft hints/A/B (hash-excluded); optional budget metrics; optional Helios norms as **cheap Zeus/Client** work — same spirit as Helios “nice to have.”  
**Depends on base-5:** frozen objects + company_context + settings/policy already ship (pack done; Client CR-20).  
**Prefer after base-5.3 skinny:** soft injects should not re-bloat a surface we just dieted; A/B tool-set experiments stay **stamped arms**, not mid-turn tools[] edits.

### Catalog / Client goals (all additive or optional)

1. **`wish_i_knew` hygiene** — already optional; shape/docs polish only.  
2. **G2 metrics hygiene** — never `summary`; dual path docs for `hooks_jailbreak_score` (base-5 already has dual scores).  
3. **Budget zone metrics (enforced reporting)** — size tags; caps already in base-5 design; **per-verb use rates** from Hot Path.  
4. **`hints` / Hot-Path / A/B paste** — **after** hard `rules`; hash-excluded; must not strip jailbreak rules.  
5. **Optional** terminate retry (“required four only”).  
6. **De-demo** efficiency prose (residual after base-5.3 skinny).  
7. Customs filename smoke in scan + Client.  
8. **`ab_arm`** on report (cheap Client scalar) — slice by full vs skinny **stamp**.  
9. **A/B stamped skinny packs** (fewer verbs or thinner schemas) promoted only after Hot Path + gold green — not runtime allowlists that unhash production.

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
base-5.2 ADDITIVE G2 on base-5 wire
         ★ keep wish_i_knew (ops feedback)
         ★ append data_gaps (Helios schema/data/index acquisition)
           │
base-5.3 SKINNY + WORLD-MODEL + VERB CLARITY on base-5 wire
         ★ CORE blurb: AI-Ready overlay · MINI-SCHEMA shape · access path → verb
         ★ 13-verb desc/params aligned to docs/API/V2 (P0 order/find/search)
         ★ prose no-rediscovery · schema diet · measure AI floor
         ★ Hot Path verb histogram → A/B re-stamped skinny packs
         ★ never strip hashed tools[] mid-session under enforcement
         ★ company_context = tenant people/places/things + key links
           │
base-6+ ADDITIVE / OPTIONAL only
        soft hints/A/B · optional norms · Workbench · pin when green
        Helios nice-to-haves stay cheap providers · never re-break base-5 wire
        do not re-bloat Layer A; tool-set A/B stays stamped
```

```text
Helios cost filter (every proposal):
  Can Zeus/Client emit it?  → do that (BASE guidance only if needed)
  Needs AI meaning?         → optional_when · never always-on hot path
  Needs dashboard GROUP BY? → precomputed scalar on report, not only arrays

Latency filter (every proposal):
  Does it cut rounds / rediscovery / completion tokens / schema bytes?
  Or only catalog quality?  → label it (quality ≠ wall-ms)
  Dropping verbs?           → new stamp / A/B arm, not runtime tools[] edit
  Inject green?             → prose + fix inject; do not unhash tools[]
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
| Always pin full 13 without looking at Hot Path | Empirics → A/B skinny **stamp**; platform still has 13 ([§ Getting skinny](#getting-skinny--latency--verb-surface-plan)) |
| Strip `describe` from tools[] when mini-schema arrives | **Breaks contract enforcement** — same stamp must keep tools[]; fix inject + prose, or re-stamp a skinny pack |
| Call `describe` when MINI-SCHEMA is already injected | Inject is authoritative; `describe` is fallback / refresh only (tool may still be listed) |
| Expect base bumps alone to drop AI wall ms | Measure tokens/rounds/verb rates; model floor is real |
| Teach data access as “fill the form / invent columns” | DESIGN: **AI-Ready overlay + mini-schema shape + access class** ([§ World model language](#world-model-language-for-chat_request-design-vocabulary)) |
| Paste DESIGN.md / foundation essay into system prompt | Short CORE blurb + `company_context` + live inject |
| Cost-tag-only tool descriptions (`[cheap] describe`) | WHEN / WHEN NOT / KEY per verb ([§ Verb catalog clarity](#verb-catalog-clarity-base-52-review--base-53)) |
| System `order` with `direction` / bare field name | Zeus: `by: "field:<name>"`, `asc: false` |

base-4 already has the **AI meaning** slots (QD facets + recommended G2/G3; triggers still arrays).  
base-5 puts **company + named rules + control plane** in product.  
base-5.3 makes **skinny + world-model language + honest latency** first-class.  
Helios volume is **report/session scalars**.

---

## Cross-cutting principles (every BASE)

1. **One Terminate surface** — extend the table; no second essay.  
2. **base-5 = last break; base-5.x content/skinny; base-6+ = additive/optional only** — until a new major is justified.  
3. **Platform keeps the same 13 verb names** until a major Zeus API train; **product pins use stamped tools[]** — subset only via **new hash / A/B pack**, never mid-session strip under enforcement ([§ Getting skinny](#getting-skinny--latency--verb-surface-plan)).  
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
15. **Inject green ⇒ no rediscovery habit** — SCOPE BRIEF + MINI-SCHEMA beat calling `describe` / list_* / get_stats; still **do not unhash tools[]** to force that.  
16. **Latency: measure AI floor** — rounds, **per-verb use**, rediscovery, tokens, `ai_ms`; catalog quality trains are not automatic wall-ms wins.  
17. **Skinny before soft bloat** — prefer base-5.3 prose/schema + empiric stamps before base-6 hints that re-grow the prompt.  
18. **Drop verbs via Hot Path → A/B stamp → pin** — Prompt Helper and Workbench own the experiment loop; production enforcement stays honest.  
19. **World model in front of the model** — chat_request teaches overlay + map + access class (DESIGN); Layer A is emit-from-evidence, not form-fill over empty slots.  
20. **Tenant texture in `company_context`** — durable entities + key links/events; not a second giant system essay.  
21. **Tool schemas match Zeus V2** — descriptions teach WHEN/KEY; param lists match dispatch (no prompt/`direction` vs API/`asc` drift).

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
19. **Skinny packs:** separate base-5.3-full pin vs optional customs, or only A/B arms until promote?  
20. **`traverse` / `explain` drop thresholds** from Hot Path (e.g. &lt;1% of runs in last 500)?  
21. ~~**Inject-green omit `describe` from tools[]?**~~ → **No under enforcement** — prose + inject fix; drop only in a **new stamp**. Safety `denied_verbs` after the fact is not a substitute for skinny stamp design.  
22. **Skinny size targets:** hard cap on verbs JSON chars / system chars per mode?  
23. Spin **docs/SKINNY.md** out of ROADMAP when base-5.3 implements, or keep single SoT here?  
24. Hot Path window defaults: last 100 / 500 / 7d runs — product owner?  
25. World-model blurb hard cap: 120 vs 180 words — enough for access-class rules?  
26. Put access-class cheat on every mode overlay, or only CORE once?  
27. Verb clarity: hard cap per-description chars vs quality of KEY lines?  
28. Ship P0 order/find/search in a hotfix on base-5.2 customs before full base-5.3 pack?

---

## Doc ownership

| Doc | Role |
| --- | --- |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Structured Helios Requests + priorities |
| [ROADMAP.md](ROADMAP.md) | BASE sequencing + Helios + **skinny** + **world-model language** + **verb catalog clarity** |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers + Client `output_request` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security · **verb allow/deny** · company_context |
| [zeus_design_docs DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) | Zeus architecture — overlay · tools · mini-schema §7.8 · modes §14 |
| [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) | E–T–E / schema-as-world-model storytelling SoT |
| Zeus [`docs/API/V2`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2) | Per-verb behaviour SoT for catalog descriptions |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold new base-N pack (`scripts/new_base.py`) |
| [COMPAT.md](../COMPAT.md) | Zeus × chat_request BASE × zeus_client matrix |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BIBLE.md](BIBLE.md) | Normative base-4 + §2 ownership |
| [RELEASE_NOTES.md](../RELEASE_NOTES.md) | What shipped + **breaking changes** |
| [migration/README.md](migration/README.md) | All BASE hops `base-X_to_base-Y` |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | AI comply / upgrade procedures |
| [../AGENTS.md](../AGENTS.md) | Repo AI entry |
| [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) | Experience (1→4 hop) |
| [migration/base-5_to_base-5.2/lessons-learned.md](migration/base-5_to_base-5.2/lessons-learned.md) | Experience (5→5.2 hop) |

---

*Align with Helios wishlist when HEL-WISH IDs change; revise BASE section when base-5 starts. Control-plane detail lives in PROMPT_SETTINGS.md. Latency / verb-surface detail lives in § Getting skinny. DESIGN vocabulary for catalog prose lives in § World model language. Per-tool description backlog lives in § Verb catalog clarity (base-5.3).*
