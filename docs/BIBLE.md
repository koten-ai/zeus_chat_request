# base-4 Bible

**One document so a human or AI can implement, review, or operate base-4 end-to-end.**

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **Status** | Prototype — **not** production pin (`CURRENT.json` is still base-1) |
| **Folder** | catalogs: `v2/base/base-4/` · this doc: `docs/BIBLE.md` |
| **Audience** | Zeus Client, Hub/Workbench, engine, coding agents |

### Companion files (read in this order after the Bible)

| Step | File | Why |
| --- | --- | --- |
| 1 | **This Bible** | Requirements + step-by-step |
| 1b | [base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md](base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md) | Map from production base-1 → base-4 |
| 2 | [`../v2/base/base-4/text/`](../v2/base/base-4/text/) | Full catalog text (easiest to read) |
| 3 | [`../v2/base/base-4/response_output_schema.json`](../v2/base/base-4/response_output_schema.json) | Machine Layer A schema |
| 4 | [`../v2/base/base-4/response_output_example.json`](../v2/base/base-4/response_output_example.json) | One valid terminate instance |
| 5 | [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) | Middleman multi-round detail |
| 6 | [multi_round_example.json](multi_round_example.json) | Full 2-round session snapshot |
| 7 | [`../v2/base/base-4/min/`](../v2/base/base-4/min/) | JSON source for stamp/Client loaders |
| 8 | [`../v2/base/base-4/OVERVIEW.md`](../v2/base/base-4/OVERVIEW.md) | Short diet changelog only |
| 9 | [INSPECTOR.md](INSPECTOR.md) | One index.html for multi-BASE |
| 10 | [base-1_to_base-4/lessons-learned.md](base-1_to_base-4/lessons-learned.md) | Migration experience |
| 11 | [ROADMAP.md](ROADMAP.md) | base-5 / base-6+ goals |
| 12 | [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + rules + hooks |
| 13 | [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · [assembled_prompt.svg](../images/assembled_prompt.svg) | Wire order |
| 14 | [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules + output_request |
| 15 | [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy |
| 16 | [CREATE_BASE.md](CREATE_BASE.md) | Scaffold next base-N pack |
| 17 | **§2 Ownership matrix** (this Bible) | Who may **set / unset / change** |

---

## 0. What is base-4 in one paragraph?

A **chat_request** is the LLM **catalog** for one agent mode: house rules + 13 Zeus tools (verbs) + **terminate contract** (how the turn must end). base-4 is the **new dieted chat_request line** of that catalog: same verbs and required evidence fields as before, but **one clear Terminate table + example** instead of two long overlapping essays. Zeus Client loads a catalog, injects live scope data, runs multi-round tool chat, and parses a final **Layer A** `return` object for UI, control flags, and admin metrics.

---

## 1. Mental model: assembled prompt (every round)

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1) ZEUS RULES  ·  CONTRACT / catalog  ·  HASHED when stamped    │
├─────────────────────────────────────────────────────────────────┤
│  meta: format, mode, base-4, custom-?, contract_hash            │
│                                                                 │
│  CONTRACT START                                                 │
│    Base-4                                                       │
│      • How Zeus works (efficiency, tool use)                    │
│      • 13 APIs (verbs + parameter schemas)                      │
│      • Terminate (Layer A) table + example                      │
│    Base-4                                                       │
│      • api weight / cost hints                                  │
│      • hard behavior (act, pipeline, no plain-text finale)      │
│  CONTRACT END                                                   │
│                                                                 │
│  optional (full profiles only; usually NOT hashed):             │
│    soft guidance — optimal_paths, facet docs                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2) ZEUS_CLIENT INJECTION  ·  pass-in / overrides  ·  NOT hashed │
├─────────────────────────────────────────────────────────────────┤
│  SCOPE BRIEF + MINI-SCHEMA     (live scope — from Zeus)         │
│  business_injection:                                            │
│    brand / locale / message_failure / clarify / …               │
│    rules[]  (indexed; base-5: rules{} by id — see §2.7)         │
│  session: zeus_session_id, zeus_round, turn_index, max_rounds   │
│  overrides: prompt_override, tenant_pin, extra denied verbs…    │
│  (AgentHooks = code; effects may appear as inject text)         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3) USER INPUT MESSAGE                                           │
├─────────────────────────────────────────────────────────────────┤
│  this turn’s question (+ history / tool results on later rounds)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                         ┌─────────┐
                         │   LLM   │
                         └────┬────┘
                              │ tools ↔ Zeus
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4) TERMINATE OUTPUT  (one return object; split by audience)     │
├─────────────────────────────────────────────────────────────────┤
│  G1 USER-FACING                                                 │
│     summary · confidence · query_decomposition · decomposition  │
│                                                                 │
│  G2 ADMIN-ONLY  (never chat UI)                                 │
│     subject_confidence 0.0..1.0                                 │
│     wish_i_knew[]                                               │
│     jail_break_attempt 0.0..1.0  (subjective AI)                │
│                                                                 │
│  G3 CLIENT CONTROL-PLANE  (never chat UI)                       │
│     business_rules_triggers[]  // base-5: {} by rule id          │
│     policy_action?  answer | clarify | refuse | error           │
└─────────────────────────────────────────────────────────────────┘
```

**Wire note:** Layer A is **flat** on the `return` tool (see schema). G1/G2/G3 are **audiences** for Client redaction — not three nested roots the model must invent.

**Without mini-schema** the model can still emit a **valid empty/clarify** terminate; it cannot safely invent field paths or inventory facts.

---

## 2. Ownership matrix — set · unset · change

**Normative for integrators.** Every field lives under one primary owner.  
Cross-writes are either **forbidden** or **only via an allowed path** (e.g. Client applies model triggers into `control.flags`).

### 2.0 Actors

| Actor | Who | Typical surface |
| --- | --- | --- |
| **App user** | Application code calling Zeus Client (`run_agent`, config, session options) | Config, injects content, user text, hooks *they* register, `output_request` |
| **Zeus Client (logic)** | SDK / middleman — not the LLM | Assemble prompt, append `messages[]`, execute Zeus verbs, parse/validate Layer A, redact G2, map G3 → state, clocks, caps |
| **AI (LLM / AI API)** | Model behind the chat/completions + tools API | Tool calls, Layer A fields on `return` / terminating pipeline |
| **Hub / ops** *(out of band)* | Workbench stamp, catalog author | BASE/custom JSON, `contract_hash` — **not** per-turn app code |

**Legend (cells)**

| Symbol | Meaning |
| --- | --- |
| **S** | May **set** (create / first provide / emit) |
| **U** | May **unset** (omit, clear, remove key, drop from bag) |
| **C** | May **change** (overwrite / mutate value) |
| **R** | **Read** only (must not write) |
| **—** | Never (forbidden / not that actor’s job) |
| **\*** | Allowed only under the constraint in *Notes* |

**Operation verbs (product language)**

| Verb | Means |
| --- | --- |
| **set** | Introduce a value that was absent (or establish session default) |
| **unset** | Remove / clear / stop sending (e.g. drop optional field, empty list, omit key) |
| **change** | Replace an existing value with another |

### 2.1 Session bags (A–D)

| Bag / item | App user | Client logic | AI | Notes |
| --- | --- | --- | --- | --- |
| **A Catalog** (file path, mode, base_id) | S\* C\* | R (load) | — | App picks mode/file; **re-stamp / new custom** is Hub. Do not invent hashes. |
| **A `contract_id` / `contract_hash`** | S\* | R + bind | — | Set only from **Hub stamp / sync** — never invent. **U** only by re-pin / resync. |
| **B SCOPE BRIEF** | — | S C U\* | R | Client merges from Zeus; may trim for budget. AI must not invent stats. |
| **B MINI-SCHEMA** | — | S C U\* | R | Same as brief. AI uses paths; does not rewrite schema bag. |
| **B `business_injection.message_*`** | **S C U** | R (inject) | R | App owns brand copy. Client may pick which string to **show** after `policy_action`. |
| **B `business_injection.rules`** | **S C U\*** | R (inject) | R | App owns rule text/ids. **U/C mid-session:** avoid renumber (base-4) / rename (base-5). Append-only safest. |
| **B `company_context`** (base-5) | **S C U** | C\* (truncate) | R | Client hard-truncate at word cap; must not rewrite meaning. |
| **B `output_request`** (base-5) | **S C U** | R (inject + validate) | R | App asks for extra structure; AI fills `app_output` only when set. |
| **B `session.zeus_session_id`** | S\* | **S C** | — | Client usually mints; app may resume known id. |
| **B `session.zeus_round` / `turn_index`** | — | **S C** | R echo only | **Client is clock.** AI must not advance the round. |
| **B `session.max_rounds`** | **S C** | C\* tighten | — | App sets budget; Client/hooks may **lower**, never raise past app/policy without consent. |
| **B overrides** (`prompt_override`, `tenant_pin`, extra deny verbs) | **S C U** | C\* via hooks | — | Hooks can force tighten (deny verbs, pin). AI cannot override hooks. |
| **B AgentHooks effects** | S\* (register) | **S C** (run) | — | App supplies functions; Client executes. AI never owns hooks. |
| **C `messages[]` (user turn text)** | **S** (each user msg) | C\* (wrap/send) | R | App provides content. Client must not silently rewrite user intent. |
| **C `messages[]` (system / inject assembly)** | — | **S C** | R | Client builds system blob each round. AI does not edit catalog text. |
| **C `messages[]` assistant tool_calls** | — | **S** (append) | **S** (emit) | AI emits; Client **appends** only. App does not forge tool_calls. |
| **C `messages[]` tool results** | — | **S** (append) U\* | — | Client appends Zeus JSON. May **truncate** old tool bodies for budget; keep full copy in **D**. AI does not write tool role. |
| **D `artifacts.tables` / entities** | R | **S C U** | — | Client enrichment for UI. Not a second model wire. |
| **D `artifacts.last_terminate`** | R | **S C** | — | Client stores last parsed Layer A. |
| **D `control.flags`** (coupon, …) | R C\* | **S C U** | — | Client applies G3 triggers → flags. App may seed UI flags carefully. |
| **D admin metrics buffer** | — | **S C** | — | G2 only; never chat UI. |

### 2.2 Layer A terminate fields (model wire → Client split)

Flat object on `return` / terminating `pipeline`.  
**Required four** must be **set** by AI on every successful terminate. Client may **reject** / soft-fail if missing (not invent facts).

| Field | App user | Client logic | AI | Notes |
| --- | --- | --- | --- | --- |
| **`summary`** | R → UI | R; may **replace display** with `message_*` when refuse/clarify\* | **S C** | AI sets facts. Client may **swap chrome** from brand templates; must not invent Zeus rows. |
| **`query_decomposition`** | R | R + forward analytics | **S C** | AI only. Client may synthesize **only** if product policy + mark `synthetic` (server path preferred). |
| **`decomposition`** | R | R | **S C** | AI only. |
| **`confidence`** | R (soft UI) | R | **S C** | AI only; enum string. |
| **`policy_action`** | R | R → maps `message_*` | **S C U\*** | AI preferred. Client may **force** `refuse`/`error` via hooks. Unset → Client default (often treat as `answer` or clarify path — product choice). |
| **`subject_confidence`** | — | R → metrics | **S C U** | G2. App never shows. Client may default missing → omit metric. |
| **`jail_break_attempt`** | — | R → metrics; hooks may set **parallel** score | **S C U** | G2. Never UI. Client must **not** overwrite model score with hooks score in the same field (store separately). |
| **`wish_i_knew`** | — | R → metrics / Workbench | **S C U** | G2. Max 3. Empty `[]` = unset-all gaps. |
| **`business_rules_triggers`** | R\* flags | **C\*** normalize; apply → `control.flags` | **S C U** | AI emits parallel to inject `rules`. Client pads/normalizes (array tails false / object missing=false). App reads **flags**, not raw if Client hides. |
| **`app_output`** (base-5) | R + validate expect | **C\*** validate/strip illegal keys; **renders field descriptions into prompt** | **S C U** | Only when App set `output_request.app.fields` with **type + description**. Type alone is insufficient for the model. Client **rejects** missing descriptions / oversize; does not invent app fields. |
| **`node_refs` / `entity_refs` / `provenance`** | R UI | R | **S C U** | Optional grounding. |
| **`round`** (echo) | — | **S** authoritative in session | S echo | Client clock wins on conflict. |
| **Layer B** (`diagnosis`, `spans`, …) | — | — | **—** | **Server only.** AI must not set. Client must not put in chat loop. |

\*Client **display replace**: when `policy_action` is `refuse`/`clarify`/`error`, Client **may** prefer `message_jailbreak_soft` / `message_clarify` / `message_failure` over raw `summary` for UI — still keep raw `summary` in artifacts for audit if needed.

### 2.3 What the AI must never set / change / unset

| Item | Why |
| --- | --- |
| `contract_hash` / stamp | Integrity; drift detection |
| Hub catalog verb schemas (as “truth”) | Server executes real verbs |
| `session.zeus_round` as authority | Client clock |
| AgentHooks outcomes | Code path, not model |
| Layer B Detective fields | Server-built |
| Invented Zeus inventory / freebies | Ground in tools + schema |
| G2 fields inside `summary` | Audience split |

### 2.4 What the App user must never set / change / unset

| Item | Why |
| --- | --- |
| Invented production `contract_hash` | Use stamp / sync only |
| Forge `messages[]` tool results | Client + Zeus only |
| Write G2 into chat UI | Admin-only |
| Rewrite model `business_rules_triggers` and pretend AI said it | Apply to **flags** instead; keep raw Layer A for audit |
| Drop required four and still claim success | Protocol miss |

### 2.5 What Client logic must never set / change / unset

| Item | Why |
| --- | --- |
| User’s intended question meaning | Don’t silently rewrite `user` content |
| Fabricate Layer A **facts** (`summary` data, entity lists) | May only map policy chrome / fail closed |
| “Fix” `jail_break_attempt` by overwriting model float | Separate `hooks_jailbreak_score` |
| Raise `max_rounds` past app/policy without explicit allow | Caps are safety |
| Put G2/G3 raw into user-visible chat | Redact |

### 2.6 Per-operation cheat sheet (common flows)

```text
APP sets:
  config, mode, scope, stamped contract pin,
  business_injection (messages, rules, company_context),
  output_request (base-5), user message, max_rounds, hooks registration

CLIENT sets / changes:
  assembled system prompt, SCOPE BRIEF/MINI-SCHEMA merge,
  messages[] append (assistant/tool), zeus_round++,
  Zeus execute, artifacts, last_terminate store,
  normalize triggers, map policy_action → UI boilerplate,
  redact G2, validate app_output, truncate budgets

AI sets / changes:
  tool_calls (non-terminate), Layer A on return
  (optional recommended fields; sparse triggers OK)

AI unsets:
  omits optional Layer A keys; empty wish_i_knew []; sparse triggers

CLIENT unsets:
  drops old tool bodies from prompt (budget); clears session flags on reset

APP unsets:
  omits optional inject keys; clears output_request; ends session
```

### 2.7 base-4 vs base-5 (mutability note)

| Surface | base-4 (this folder) | base-5 (design) |
| --- | --- | --- |
| `rules` | App **S/C/U** as `string[]` | App **S/C/U** as `{ id: text }` |
| `business_rules_triggers` | AI **S** as `boolean[]`; Client normalize | AI **S** as `{ id: bool }` sparse |
| `output_request` / `app_output` | Informal `structured` only | App **S** request; AI **S** `app_output`; Client validate |

Full base-5 design: [`docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md`](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · control plane: [`docs/PROMPT_SETTINGS.md`](PROMPT_SETTINGS.md).

### 2.8 Settings bag (structured — not prompt essays)

App / Client configure behavior via a **settings** object. Do not bury “max rounds = 3” only as free-form system text.

| Setting | App | Client | AI | Notes |
| --- | --- | --- | --- | --- |
| `max_rounds` | **S C** | **C\*** lower only | — | Caps |
| `model` / `temperature` | **S C U** | R | — | Not hashed |
| `tool_choice` / force final `return` | S C | **C\*** budget-low | — | Terminate reliability |
| `allowed_verbs` / `denied_verbs` | **S C** | hooks **C** tighten | — | Safety |
| `locale` / `timezone` / `channel` / `market_country` | **S C U** | inject meta | R | Helios cheap |
| `ab_arm` / `deployment_id` / `ruleset_id` | **S C U** | report | R | Experiment / slice |
| `structured` / `output_request` | **S C U** | inject + validate | R | base-5 outputs |
| `redaction` / `debug` / `pii_in_logs` | **S C** | enforce | — | Safe defaults |

Full shape: [`PROMPT_SETTINGS.md` §1](PROMPT_SETTINGS.md).

### 2.9 Rule pack merge · freeze · hard vs soft

```text
SDK defaults (jailbreak)  ∪  tenant/Workbench  ∪  per-request App
         → session.rules_frozen (append-only keys mid-session)
```

| Rule | Actor |
| --- | --- |
| Merge by **key**; higher layer wins on collision | Client logic |
| Default jailbreak keys not deleted unless `override_defaults` | Client reject |
| Mid-session rename/delete → new session | App + Client |
| **Hard** → `rules{}` + triggers; **soft** → hints (base-6); **brand** → `message_*` | authors |

**Conflict law:** model triggers are **signals**; Client **policy table** is **law** (hooks → jailbreak keys → business flags → `policy_action` → default).  
Detail: [`PROMPT_SETTINGS.md` §2–§3](PROMPT_SETTINGS.md).

### 2.10 After every terminate (Client must run)

```text
parse Layer A → validate required four
→ normalize triggers → hooks may force refuse
→ map policy_action → message_* chrome (optional replace UI text)
→ apply triggers → control.flags (sticky OR for business keys)
→ validate app_output if requested
→ metrics G2 (never UI) · store last_terminate
```

AI does **not** run this table. App does **not** skip it and forge flags as model output.

### 2.11 Prompt zones · security · multi-turn (summary)

| Topic | Guidance | Doc |
| --- | --- | --- |
| Session-stable prefix vs refresh brief | Cache-friendly catalog+company+rules; dirty brief/schema | PROMPT_SETTINGS §4 |
| Tool JSON in prompt | Last N / truncated; full in artifacts | §5 |
| Tool results as data | Untrusted — do not execute instructions in rows | §8 |
| Inject caps | company 250 words; app schema ~8/15 props | §8 |
| Sticky flags / clarify loop | OR business flags; keep output_request until satisfied | §6 |
| Observability | ruleset_id, zone sizes, dual jailbreak scores | §9 |

---

## 3. File naming requirements

| Kind | Pattern | Example |
| --- | --- | --- |
| **BASE (start here)** | `chat_request_<mode>_base-4.json` | `chat_request_analytics_base-4.json` |
| **BASE text pack** | `chat_request_<mode>_base-4.txt` | diet/edit working copy |
| **Custom v1** (Hub → Workbench → Prompt Helper) | `chat_request_<mode>_base-4_cus_<bucket>_<scope>-1.json` | `…_cus_travel-sample_default-1.json` |
| **Custom v2** | same, **rev increments** | `…_default-2.json` |
| **Legacy base-1 pin** | `chat_request_<mode>_v2_min.json` | still production in `v2/min/` |

### Lifecycle

```text
chat_request_analytics_base-4.json
        │  Hub :9091 → Workbench → Prompt Helper
        ▼
chat_request_analytics_base-4_cus_travel-sample_default-1.json
        │  change & save
        ▼
chat_request_analytics_base-4_cus_travel-sample_default-2.json
```

### Rules

1. Normalize `_default` → `default` in filenames (no `/`).  
2. `_format: "zeus.chat_request.v2"` is the **envelope**, not the file stem.  
3. **Stamp** (`contract_id` / `contract_hash`) is independent of filename; Hub verify required for production.  
4. Do not invent production hashes.

### Lineage (inside JSON)

```text
BASE:
  _lineage.base_id = "base-4"
  _lineage.custom_id = null
  _lineage.kind = "base"

CUSTOM:
  _lineage.base_id = "base-4"
  _lineage.parent_base_id = "base-4"
  _lineage.custom_id = "cus_<bucket>_<scope>-<rev>"
  _lineage.kind = "custom"
```

---

## 4. Catalog contents (what’s in the file)

### 4.1 Top-level (min / base-4 JSON)

| Key | Role |
| --- | --- |
| `_format` / `_version` | Envelope identity (`zeus.chat_request.v2`) |
| `_hash` / `_hash_policy` | What participates in contract hash |
| `_lineage` | base_id, mode, parent, prototype flags |
| `_note` / `_prototype` | Human/design metadata |
| `contract` | Stamp envelope (prototype hash until Hub stamps) |
| `messages[]` | System prompt (rules + Terminate table) |
| `verbs[]` | 13 OpenAI-style tools |

base-4 **min** does **not** ship full `guidance` / `masq` / rich `instructions` blocks (those appear on full engine profiles). Cost/order hints live in system prose + verb descriptions.

### 4.2 The 13 verbs (names)

```text
describe, get, find, traverse, search, analyze, explain,
set, order, enrich, project, pipeline, return
```

- Most verbs: fetch/transform data via Zeus.  
- `pipeline`: multi-step with `@as.ids`.  
- `return`: **terminate** with Layer A fields (no further Zeus call required).

### 4.3 System prompt sections (base-4 diet)

1. **Execution style** — act, don’t narrate; one decisive call; end with `return`  
2. **CRITICAL EFFICIENCY** — don’t rediscover stats; use brief/schema; top-N via find→order→project  
3. **Verb Priority & Cost** — prefer cheap tools  
4. **Terminate (Layer A) — copy this shape** — **single** table + example  

---

## 5. Terminate / Layer A requirements (normative)

Machine schema: [`response_output_schema.json`](../v2/base/base-4/response_output_schema.json).  
Example instance: [`response_output_example.json`](../v2/base/base-4/response_output_example.json).

### 5.1 Field table

| field | req | audience | type / notes |
| --- | --- | --- | --- |
| `summary` | **yes** | **G1 user** | string — facts only |
| `query_decomposition` | **yes** | analytics | object — intent+entity core |
| `decomposition` | **yes** | analytics | object — targets/predicates/output |
| `confidence` | **yes** | soft UI | `high` \| `med` \| `low` (string, **not** a number) |
| `policy_action` | no | **G3 client** | `answer` \| `clarify` \| `refuse` \| `error` |
| `subject_confidence` | no | **G2 admin** | number 0.0–1.0 — right entity? |
| `jail_break_attempt` | no | **G2 admin** | number 0.0–1.0 — subjective (not boolean) |
| `wish_i_knew` | no | **G2 admin** | max 3 `{what, kind, why?, severity?}` |
| `business_rules_triggers` | no | **G3 client** | `boolean[]` ∥ `rules[]` indexes |
| `node_refs` / `entity_refs` / `provenance` | no | user/ui | optional grounding |

### 5.2 One-line distinctions (must not confuse)

| Concept | Means |
| --- | --- |
| `query_decomposition` | What the **USER** wanted |
| `wish_i_knew` | What **I (the model)** was missing (rules/message/schema/data/tool) |
| `confidence` | Overall answer quality (`high`/`med`/`low`) |
| `subject_confidence` | Confidence in **entity/subject** identification (float) |
| `summary` | **Only** G1 — never scores, triggers, or Detective fields |
| Layer B | Detective/store (`diagnosis`, spans, …) — **server only**, never model emit |

### 5.3 Example skeleton (always-valid shape)

```text
summary: "…"
confidence: med
query_decomposition: { intent: "List", entity: "Beer" }
decomposition: { targets: [{ entity_type: "Beer", focus: ["name"] }], predicates: {}, output: "rows" }
policy_action: answer
subject_confidence: 0.8
jail_break_attempt: 0.0
wish_i_knew: []
business_rules_triggers: []
node_refs: []
entity_refs: []
```

### 5.4 Forbidden on terminate

`attribution`, `decision`, `diagnosis`, `inject_inspect`, `prompt_checklist`, `spans`, `support_pack`, full `report.detail`, …

---

## 6. Zeus Client inject requirements (not in BASE file)

**Who may set / unset / change these:** see **§2 Ownership matrix**.

| Inject | Purpose | Primary setter |
| --- | --- | --- |
| SCOPE BRIEF | Live scope stats / orientation — do not rediscover via tools | Client logic (from Zeus) |
| MINI-SCHEMA | Entity types + filterable fields for `where` / search | Client logic (from Zeus) |
| `business_injection.message_*` | Brand boilerplate (failure, clarify, out_of_scope, …) | **App user** |
| `business_injection.rules[]` | Indexed rules (base-4); model returns `business_rules_triggers[]` | **App user** (base-5: named object) |
| `company_context` / `output_request` | Product identity / app terminate bag (base-5) | **App user** |
| `session.zeus_round` | Round clock | **Client logic** only |
| AgentHooks | Hard policy code (pin tenant, reject verbs, caps) | App registers · Client runs |

**Hash boundary:** injects and user text are **not** part of BASE identity; tenant brand must not thrash contract hash.

---

## 7. Multi-round middleman (step-by-step)

**Yes — still append a `messages[]` array.** That is the easy loop.  
Also keep **artifacts** for UI copies and **last_terminate** for Layer A.

Detail + full walkthrough: [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md).  
Snapshot: [multi_round_example.json](multi_round_example.json).

### 7.1 Four bags

```text
A. CATALOG      base-4 file + contract pin
B. INJECTS      brief, mini-schema, business_injection
C. MESSAGES[]   append-only transcript (AI + tool results)
D. ARTIFACTS    tables, entities, tool_log, last_terminate
```

### 7.2 One user turn, two model rounds (happy path)

```text
messages = [system, user]

# ROUND 1
AI → tool_calls: pipeline(find→order→project)
messages.append(assistant tool_calls)
Zeus runs pipeline → rows
messages.append(tool result)              # append array
artifacts.tables / entities.update(rows)  # Client enrichment copy

# ROUND 2
AI → tool_calls: return({ Layer A … })
messages.append(assistant return)         # optional audit
layer_a = parse(arguments)
artifacts.last_terminate = layer_a
ui.show(layer_a.summary)                  # G1 only
apply(layer_a.business_rules_triggers)  # G3
metrics.emit(admin fields)                # G2 never UI
# stop
```

### 7.3 Full messages[] picture after 2 rounds

```text
[
  { role: system,    content: catalog + injects },
  { role: user,      content: "Top 5 highest ABV beers…" },
  { role: assistant, tool_calls: [pipeline] },   # round 1
  { role: tool,      content: "{ rows: […] }" }, # Zeus
  { role: assistant, tool_calls: [return] },     # round 2 Layer A
]
```

### 7.4 Pseudocode loop

```text
messages = [system, user]
for round in 1..max_rounds:
  resp = ai.chat(messages, tools=verbs)

  if tool_calls and not terminate:
    messages.append(assistant+tool_calls)
    for tc in tool_calls:
      result = zeus.execute(tc)
      messages.append(tool_result)       # still just append
      artifacts.upsert(result)
    continue

  if return / terminating pipeline:
    layer_a = parse(return_args)         # validate vs response_output_schema.json
    assert required fields present
    ui.show(layer_a.summary)
    client.apply(layer_a.policy_action, layer_a.business_rules_triggers)
    admin.metrics(layer_a.subject_confidence, layer_a.jail_break_attempt, layer_a.wish_i_knew)
    break

  # plain text without return → protocol miss → clarify / message_failure
```

### 7.5 What goes where

| Source | Store in |
| --- | --- |
| Catalog / stamp | Bag A |
| Brief, schema, rules, brand strings | Bag B |
| AI tool_calls + Zeus JSON strings | Bag C `messages[]` (**append**) |
| Flattened UI rows, id maps | Bag D `artifacts` |
| Final Layer A | Bag D `last_terminate` |
| Detective diagnosis/spans | Zeus server Layer B (not Client loop) |

---

## 8. Worked examples

### 8.1 Minimal valid terminate (clarify, no data yet)

```json
{
  "summary": "I need city/dates (and live schema) before I can search rooms.",
  "confidence": "low",
  "query_decomposition": { "intent": "Book", "entity": "Hotel" },
  "decomposition": {
    "targets": [{ "entity_type": "Hotel", "focus": ["city", "dates"] }],
    "predicates": {},
    "output": "rows",
    "context": { "needs": ["city", "check_in", "check_out"] }
  },
  "policy_action": "clarify",
  "subject_confidence": 0.4,
  "jail_break_attempt": 0.0,
  "wish_i_knew": [
    { "what": "city and stay dates", "kind": "message", "severity": "med" }
  ],
  "business_rules_triggers": [],
  "node_refs": [],
  "entity_refs": []
}
```

### 8.2 Happy path after Zeus data

See [multi_round_example.json](multi_round_example.json) — top-5 ABV beers, two rounds, `policy_action: answer`, `jail_break_attempt: 0.0`.

### 8.3 Policy pressure + coupon (admin + client)

See [`response_output_example.json`](../v2/base/base-4/response_output_example.json) — `jail_break_attempt: 0.55`, `business_rules_triggers: [false, true, true]`, `wish_i_knew` filled.

**Client mapping example:**

```text
if policy_action == "clarify":
  maybe show business_injection.message_clarify chrome
if business_rules_triggers[1]:
  control.flags.coupon = true
# never show jail_break_attempt or wish_i_knew in chat UI
```

---

## 9. Token / size budget

| Zone | Guidance |
| --- | --- |
| BASE catalog | Prefer min; base-4 diet targets **clear terminate**, not max shrink |
| Soft guidance | Drop first under pressure |
| `rules[]` | Short, indexed one-liners — not policy novels |
| MINI-SCHEMA | Lite; don’t dump full inventory |
| `messages[]` tool results | Cap/truncate old rounds; keep full copy in **artifacts** |
| `wish_i_knew` | Max 3 short items |
| Layer B Detective | Never feed full spans back into the model loop |

**Anti-pattern:** stuffing rules until assembled prompt jumps ~10KB → ~60KB.

---

## 10. Contract / stamp / drift

1. Production clients bind `contract_id` + `contract_hash` after Hub verify/stamp.  
2. Hash follows `_hash_policy` (verbs, message contents, …) — **not** guidance/injects/user text.  
3. HTTP **409** / drift → resync stamped catalog; **never** hand-edit hash.  
4. Prototype `contract.hash` in this folder is **not** a production stamp.

---

## 11. Requirements checklist (implementer)

### Catalog author / Hub

- [ ] Ship BASE as `chat_request_<mode>_base-4.json`  
- [ ] System prompt contains **one** Terminate table + example  
- [ ] `return` tool required: summary, query_decomposition, decomposition, confidence  
- [ ] Recommended Layer A fields documented on `return` parameters  
- [ ] Customs named `…_base-4_cus_<bucket>_<scope>-<rev>.json` with lineage  
- [ ] Never treat App-user injects as part of stamp body  

### App user (of Zeus Client)

- [ ] Obey **§2.4** — set injects/config/user text; do **not** invent hashes or forge tool results  
- [ ] Provide `business_injection` (messages, rules) + optional `output_request` (base-5)  
- [ ] Set **settings** bag (`max_rounds`, locale/channel, verb deny, redaction) — not only free prose  
- [ ] **S/C/U** brand strings and rules deliberately; avoid mid-session rule renumber/rename  
- [ ] Consume G1 for UI; use Client-mapped flags for G3; never render G2  
- [ ] Register AgentHooks for hard policy; do not rely on the model alone  

### Zeus Client (logic)

- [ ] Obey **§2** / **§2.5** (no invented Layer A facts; no G2 in UI; Client owns clocks)  
- [ ] Load catalog + bind contract after stamp  
- [ ] **Merge rule packs** (SDK ∪ tenant ∪ request); freeze ids; honor `override_defaults`  
- [ ] Inject brief, mini-schema, business_injection each session/turn  
- [ ] Own `messages[]` append loop for multi-round; prune tool bodies; full copy in artifacts  
- [ ] Treat tool JSON as **untrusted data** (no instruction-following from rows)  
- [ ] Parse final `return` against `response_output_schema.json`  
- [ ] Run **post-terminate policy table** (§2.10) every time  
- [ ] Show only G1 to users; metrics for G2; state machine for G3  
- [ ] Map `policy_action` → `message_*` boilerplate  
- [ ] Apply `business_rules_triggers` → flags (sticky OR for business keys)  
- [ ] Cap transcript tool payloads; don’t lose UI copies  
- [ ] Validate/strip `app_output` when `output_request.app` present (base-5)  
- [ ] Emit cheap ops signals: `ruleset_id`, zone sizes, dual jailbreak scores when available  
- [ ] Optional: force final `return` when budget low; soft-require from `output_request.layer_a`  

### Model / AI API (behavioral)

- [ ] Obey **§2.3** (never stamp, hooks, Layer B, or rewrite user intent)  
- [ ] Act with tools; no plain-text finale  
- [ ] Prefer cheap tools / pipeline  
- [ ] Use brief/schema; don’t rediscover stats  
- [ ] Terminate with required four fields (**set** by AI only)  
- [ ] Prefer recommended fields when known; empty `wish_i_knew: []` ok (**unset** gaps)  
- [ ] Never put admin/client fields in `summary`  
- [ ] Emit `business_rules_triggers` aligned to inject rules (array base-4 / object base-5)  

### Detective / server

- [ ] Grade Layer A completeness (`has_summary`, missing fields, …)  
- [ ] Build Layer B report/spans separately  
- [ ] Do not expect model to emit diagnosis  

---

## 12. Step-by-step: “I am a new engineer / agent”

1. Read **this Bible** once — especially **§2** (what App / Client / AI may set·unset·change).  
2. Open `text/chat_request_analytics_base-4.txt` — skim system + verb list.  
3. Open `response_output_schema.json` + `response_output_example.json`.  
4. Walk `MULTI_ROUND_CLIENT.md` + `multi_round_example.json`.  
5. Implement Client loop (section 7.4); keep **Client clock** and G2 redaction.  
6. Validate terminates with the schema; map G3 triggers → flags (do not forge triggers).  
7. Only then wire Hub stamp + production pin.  

---

## 13. Step-by-step: “I am an AI operating a turn”

1. Read system rules + Terminate table (**you set Layer A; you do not set stamp/hooks/Layer B** — §2.3).  
2. Read SCOPE BRIEF + MINI-SCHEMA (if present) — **read only**.  
3. Read user message (+ prior tool results) — **do not rewrite** user intent.  
4. Call Zeus verbs; do not invent rows.  
5. When done, emit **one** `return` matching the table (required four + recommended if known).  
6. Put user facts only in `summary`.  
7. Put gaps in `wish_i_knew`, scores in floats, rule hits in `business_rules_triggers` (sparse OK).  
8. If Client sent `output_request.app` (base-5), fill **`app_output`** only for those keys.  

---

## 14. What base-4 deliberately changed (history)

| Before (base-2/3) | After (base-4) |
| --- | --- |
| Two long terminate essays | One Terminate table + example |
| Easy to drop “recommended” fields | Example skeleton always shows them |
| Dual confidence easy to mix | Explicit one-line distinction |
| `wish_i_knew` buried | Named in table + example as admin gaps |

Parents: **base-3** (text pack), **base-2-prototype** (JSON design).  
Production pin remains **base-1** until promoted.

---

## 15. Generator commands

```bash
# Rebuild text pack from base-4 JSON
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 4

# Next diet iteration later
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 5
```

---

## 16. Glossary

| Term | Meaning |
| --- | --- |
| **BASE** | Published template catalog (`base-4`) |
| **Custom** | Workbench fork for a bucket/scope + rev |
| **Layer A** | Model terminate payload (`return` args) |
| **Layer B** | Server Detective/store envelope |
| **G1 / G2 / G3** | User / admin / client audiences of Layer A |
| **Verb** | Zeus tool the model may call |
| **Inject** | Runtime text/data not in BASE file |
| **Stamp** | Hub-verified contract_id + hash |
| **Round** | One LLM call inside a user turn |
| **Artifacts** | Client enrichment (tables, flags), not raw transcript only |
| **App user** | Application code using Zeus Client (config / inject / user msg) |
| **Client logic** | Zeus Client SDK middleman (assemble, execute, redact, clocks) |
| **AI / AI API** | LLM that emits tool_calls + Layer A terminate |
| **Set / unset / change** | Create · remove/omit · overwrite — see **§2** |
| **Settings bag** | Structured run/session config — [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) |
| **Rule pack merge** | SDK ∪ tenant ∪ request → frozen ids — §2.9 |
| **Client policy table** | Post-terminate law — §2.10 |

---

## 17. Document map

```text
docs/
  BIBLE.md                      ← you are here (design; §2 ownership)
  MULTI_ROUND_CLIENT.md · multi_round_example.json
  PROMPT_ASSEMBLY.md · PROMPT_SETTINGS.md
  RULES_OBJECT_AND_OUTPUT_REQUEST.md
  JAILBREAK_POLICY.md · ROADMAP.md · CREATE_BASE.md
  INSPECTOR.md
  base-1_to_base-4/             ← migration archive only

v2/base/base-4/                 ← ship pack only
  min/*.json · text/*.txt
  MANIFEST.json
  response_output_schema.json · response_output_example.json
  README.md · OVERVIEW.md

images/assembled_prompt.svg
scripts/new_base.py · export_base_text.py
```

---

**End of Bible.** If something is ambiguous, prefer: (1) **§2 ownership + settings + Client policy**, (2) [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md), (3) Terminate table in the catalog system prompt, (4) `response_output_schema.json`, (5) this checklist order over ad-hoc prose elsewhere.
