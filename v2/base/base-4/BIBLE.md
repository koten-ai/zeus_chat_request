# base-4 Bible

**One document so a human or AI can implement, review, or operate base-4 end-to-end.**

| | |
| --- | --- |
| **BASE id** | `base-4` |
| **Status** | Prototype — **not** production pin (`CURRENT.json` is still base-1) |
| **Folder** | `v2/base/base-4/` |
| **Audience** | Zeus Client, Hub/Workbench, engine, coding agents |

### Companion files (read in this order after the Bible)

| Step | File | Why |
| --- | --- | --- |
| 1 | **This Bible** | Requirements + step-by-step |
| 1b | [BASE_1_TO_BASE_4_GUIDE.md](BASE_1_TO_BASE_4_GUIDE.md) | Map from production base-1 → base-4 |
| 2 | [`text/chat_request_<mode>_base-4.txt`](text/) | Full catalog (easiest to read) |
| 3 | [`response_output_schema.json`](response_output_schema.json) | Machine Layer A schema ([json-schema.org](https://json-schema.org/) draft 2020-12) |
| 4 | [`response_output_example.json`](response_output_example.json) | One valid terminate instance |
| 5 | [`MULTI_ROUND_CLIENT.md`](MULTI_ROUND_CLIENT.md) | Middleman multi-round detail |
| 6 | [`multi_round_example.json`](multi_round_example.json) | Full 2-round session snapshot |
| 7 | [`min/chat_request_<mode>_base-4.json`](min/) | JSON source for stamp/Client loaders |
| 8 | [`OVERVIEW.md`](OVERVIEW.md) | Short diet changelog only |
| 9 | [`INSPECTOR.md`](INSPECTOR.md) | Use one index.html for base-1 + base-4 |
| 10 | [`lessons-learned.md`](lessons-learned.md) | Migration experience base-1 → base-4 |
| 11 | [`docs/ROADMAP.md`](../../../docs/ROADMAP.md) | base-5 / base-6+ goals and why |
| 12 | [`docs/JAILBREAK_POLICY.md`](../../../docs/JAILBREAK_POLICY.md) | Score + rules + hooks + examples |
| 13 | [`docs/PROMPT_ASSEMBLY.md`](../../../docs/PROMPT_ASSEMBLY.md) | Wire order + [assembled_prompt.svg](../../../images/assembled_prompt.svg) |

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
│    rules[]  (indexed business rules; stable in-session)         │
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
│     business_rules_triggers[]  // parallel to rules[]           │
│     policy_action?  answer | clarify | refuse | error           │
└─────────────────────────────────────────────────────────────────┘
```

**Wire note:** Layer A is **flat** on the `return` tool (see schema). G1/G2/G3 are **audiences** for Client redaction — not three nested roots the model must invent.

**Without mini-schema** the model can still emit a **valid empty/clarify** terminate; it cannot safely invent field paths or inventory facts.

---

## 2. File naming requirements

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

## 3. Catalog contents (what’s in the file)

### 3.1 Top-level (min / base-4 JSON)

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

### 3.2 The 13 verbs (names)

```text
describe, get, find, traverse, search, analyze, explain,
set, order, enrich, project, pipeline, return
```

- Most verbs: fetch/transform data via Zeus.  
- `pipeline`: multi-step with `@as.ids`.  
- `return`: **terminate** with Layer A fields (no further Zeus call required).

### 3.3 System prompt sections (base-4 diet)

1. **Execution style** — act, don’t narrate; one decisive call; end with `return`  
2. **CRITICAL EFFICIENCY** — don’t rediscover stats; use brief/schema; top-N via find→order→project  
3. **Verb Priority & Cost** — prefer cheap tools  
4. **Terminate (Layer A) — copy this shape** — **single** table + example  

---

## 4. Terminate / Layer A requirements (normative)

Machine schema: [`response_output_schema.json`](response_output_schema.json).  
Example instance: [`response_output_example.json`](response_output_example.json).

### 4.1 Field table

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

### 4.2 One-line distinctions (must not confuse)

| Concept | Means |
| --- | --- |
| `query_decomposition` | What the **USER** wanted |
| `wish_i_knew` | What **I (the model)** was missing (rules/message/schema/data/tool) |
| `confidence` | Overall answer quality (`high`/`med`/`low`) |
| `subject_confidence` | Confidence in **entity/subject** identification (float) |
| `summary` | **Only** G1 — never scores, triggers, or Detective fields |
| Layer B | Detective/store (`diagnosis`, spans, …) — **server only**, never model emit |

### 4.3 Example skeleton (always-valid shape)

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

### 4.4 Forbidden on terminate

`attribution`, `decision`, `diagnosis`, `inject_inspect`, `prompt_checklist`, `spans`, `support_pack`, full `report.detail`, …

---

## 5. Zeus Client inject requirements (not in BASE file)

| Inject | Purpose |
| --- | --- |
| SCOPE BRIEF | Live scope stats / orientation — do not rediscover via tools |
| MINI-SCHEMA | Entity types + filterable fields for `where` / search |
| `business_injection.message_*` | Brand boilerplate (failure, clarify, out_of_scope, …) |
| `business_injection.rules[]` | Indexed rules; model returns `business_rules_triggers[]` |
| `session.zeus_round` | **Client-owned** round clock |
| AgentHooks | Hard policy code (pin tenant, reject verbs, caps) |

**Hash boundary:** injects and user text are **not** part of BASE identity; tenant brand must not thrash contract hash.

---

## 6. Multi-round middleman (step-by-step)

**Yes — still append a `messages[]` array.** That is the easy loop.  
Also keep **artifacts** for UI copies and **last_terminate** for Layer A.

Detail + full walkthrough: [`MULTI_ROUND_CLIENT.md`](MULTI_ROUND_CLIENT.md).  
Snapshot: [`multi_round_example.json`](multi_round_example.json).

### 6.1 Four bags

```text
A. CATALOG      base-4 file + contract pin
B. INJECTS      brief, mini-schema, business_injection
C. MESSAGES[]   append-only transcript (AI + tool results)
D. ARTIFACTS    tables, entities, tool_log, last_terminate
```

### 6.2 One user turn, two model rounds (happy path)

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

### 6.3 Full messages[] picture after 2 rounds

```text
[
  { role: system,    content: catalog + injects },
  { role: user,      content: "Top 5 highest ABV beers…" },
  { role: assistant, tool_calls: [pipeline] },   # round 1
  { role: tool,      content: "{ rows: […] }" }, # Zeus
  { role: assistant, tool_calls: [return] },     # round 2 Layer A
]
```

### 6.4 Pseudocode loop

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

### 6.5 What goes where

| Source | Store in |
| --- | --- |
| Catalog / stamp | Bag A |
| Brief, schema, rules, brand strings | Bag B |
| AI tool_calls + Zeus JSON strings | Bag C `messages[]` (**append**) |
| Flattened UI rows, id maps | Bag D `artifacts` |
| Final Layer A | Bag D `last_terminate` |
| Detective diagnosis/spans | Zeus server Layer B (not Client loop) |

---

## 7. Worked examples

### 7.1 Minimal valid terminate (clarify, no data yet)

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

### 7.2 Happy path after Zeus data

See [`multi_round_example.json`](multi_round_example.json) — top-5 ABV beers, two rounds, `policy_action: answer`, `jail_break_attempt: 0.0`.

### 7.3 Policy pressure + coupon (admin + client)

See [`response_output_example.json`](response_output_example.json) — `jail_break_attempt: 0.55`, `business_rules_triggers: [false, true, true]`, `wish_i_knew` filled.

**Client mapping example:**

```text
if policy_action == "clarify":
  maybe show business_injection.message_clarify chrome
if business_rules_triggers[1]:
  control.flags.coupon = true
# never show jail_break_attempt or wish_i_knew in chat UI
```

---

## 8. Token / size budget

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

## 9. Contract / stamp / drift

1. Production clients bind `contract_id` + `contract_hash` after Hub verify/stamp.  
2. Hash follows `_hash_policy` (verbs, message contents, …) — **not** guidance/injects/user text.  
3. HTTP **409** / drift → resync stamped catalog; **never** hand-edit hash.  
4. Prototype `contract.hash` in this folder is **not** a production stamp.

---

## 10. Requirements checklist (implementer)

### Catalog author / Hub

- [ ] Ship BASE as `chat_request_<mode>_base-4.json`  
- [ ] System prompt contains **one** Terminate table + example  
- [ ] `return` tool required: summary, query_decomposition, decomposition, confidence  
- [ ] Recommended Layer A fields documented on `return` parameters  
- [ ] Customs named `…_base-4_cus_<bucket>_<scope>-<rev>.json` with lineage  

### Zeus Client

- [ ] Load catalog + bind contract after stamp  
- [ ] Inject brief, mini-schema, business_injection each session/turn  
- [ ] Own `messages[]` append loop for multi-round  
- [ ] Upsert Zeus results into `artifacts` for UI  
- [ ] Parse final `return` against `response_output_schema.json`  
- [ ] Show only G1 to users; metrics for G2; state machine for G3  
- [ ] Map `policy_action` → `message_*` boilerplate  
- [ ] Apply `business_rules_triggers[i]` → flags  
- [ ] Cap transcript tool payloads; don’t lose UI copies  

### Model (behavioral)

- [ ] Act with tools; no plain-text finale  
- [ ] Prefer cheap tools / pipeline  
- [ ] Use brief/schema; don’t rediscover stats  
- [ ] Terminate with required four fields  
- [ ] Prefer recommended fields when known; empty `wish_i_knew: []` ok  
- [ ] Never put admin/client fields in `summary`  

### Detective / server

- [ ] Grade Layer A completeness (`has_summary`, missing fields, …)  
- [ ] Build Layer B report/spans separately  
- [ ] Do not expect model to emit diagnosis  

---

## 11. Step-by-step: “I am a new engineer / agent”

1. Read **this Bible** once.  
2. Open `text/chat_request_analytics_base-4.txt` — skim system + verb list.  
3. Open `response_output_schema.json` + `response_output_example.json`.  
4. Walk `MULTI_ROUND_CLIENT.md` + `multi_round_example.json`.  
5. Implement Client loop (section 6.4).  
6. Validate terminates with the schema.  
7. Only then wire Hub stamp + production pin.  

---

## 12. Step-by-step: “I am an AI operating a turn”

1. Read system rules + Terminate table.  
2. Read SCOPE BRIEF + MINI-SCHEMA (if present).  
3. Read user message (+ prior tool results).  
4. Call Zeus verbs; do not invent rows.  
5. When done, emit **one** `return` matching the table (required four + recommended if known).  
6. Put user facts only in `summary`.  
7. Put gaps in `wish_i_knew`, scores in floats, rule hits in `business_rules_triggers`.  

---

## 13. What base-4 deliberately changed (history)

| Before (base-2/3) | After (base-4) |
| --- | --- |
| Two long terminate essays | One Terminate table + example |
| Easy to drop “recommended” fields | Example skeleton always shows them |
| Dual confidence easy to mix | Explicit one-line distinction |
| `wish_i_knew` buried | Named in table + example as admin gaps |

Parents: **base-3** (text pack), **base-2-prototype** (JSON design).  
Production pin remains **base-1** until promoted.

---

## 14. Generator commands

```bash
# Rebuild text pack from base-4 JSON
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 4

# Next diet iteration later
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 5
```

---

## 15. Glossary

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

---

## 16. Document map

```text
v2/base/base-4/
  BIBLE.md                      ← you are here (start)
  BASE_1_TO_BASE_4_GUIDE.md     ← migration / mapping from base-1
  OVERVIEW.md                   ← short diet notes
  README.md                     ← folder index
  MULTI_ROUND_CLIENT.md         ← middleman deep dive
  multi_round_example.json      ← 2-round session
  response_output_schema.json   ← Layer A JSON Schema
  response_output_example.json  ← Layer A instance
  MANIFEST.json
  min/*.json                    ← catalogs (JSON)
  text/*.txt                    ← catalogs (indented text)

docs/                           ← education (repo)
  PROMPT_ASSEMBLY.md            ← wire order + diagram
  JAILBREAK_POLICY.md           ← score / rules / hooks
  ROADMAP.md                    ← base-5+

images/
  assembled_prompt.svg          ← README + PROMPT_ASSEMBLY diagram
```

---

**End of Bible.** If something is ambiguous, prefer: (1) Terminate table in the catalog system prompt, (2) `response_output_schema.json`, (3) this checklist order over ad-hoc prose elsewhere.
