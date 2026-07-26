# base-2-prototype

**Status:** prototype / feedback — **not** production BASE.  
**Parent:** `base-1`  
**Path:** `v2/base/base-2-prototype/min/chat_request_*_base-2-prototype.json`  
**Audience:** zeus_client team, Hub/Workbench, Detective schema alignment  

| Artifact | File |
| --- | --- |
| **Layer A JSON Schema** ([json-schema.org](https://json-schema.org/) draft 2020-12) | [`response_output_schema.json`](response_output_schema.json) |
| **Layer A example** | [`response_output_example.json`](response_output_example.json) |
| Catalogs | [`min/`](min/) |
| Design notes | [PROMPT_ASSEMBLY.md](../../../PROMPT_ASSEMBLY.md) · [simple_layout.txt](../../../simple_layout.txt) |


## File naming: BASE vs Workbench customs

**Envelope** (`_format: "zeus.chat_request.v2"`) is not the filename. Filenames carry **BASE id** and optional **custom revision**.

### Patterns

| Kind | Pattern | Example |
| --- | --- | --- |
| **BASE (everyone starts here)** | `chat_request_<mode>_base-<N>.json` | `chat_request_analytics_base-2.json` |
| **This prototype tree** | `chat_request_<mode>_base-2-prototype.json` | `chat_request_analytics_base-2-prototype.json` |
| **Custom (Hub Workbench / Prompt Helper)** | `chat_request_<mode>_base-<N>_cus_<bucket>_<scope>-<rev>.json` | `chat_request_analytics_base-2_cus_travel-sample_default-1.json` |
| **Custom next save** | same, **`<rev>` increments** | `…_cus_travel-sample_default-2.json` |
| **Legacy base-1 (current pin)** | `chat_request_<mode>_v2_min.json` | `chat_request_analytics_v2_min.json` |

### Lifecycle

```text
start (all tenants / demos)
  chat_request_<mode>_base-2.json
        │
        │  Zeus Hub :9091 → Workbench → Prompt Helper
        │  refine for bucket/scope, then save
        ▼
  chat_request_<mode>_base-2_cus_<bucket>_<scope>-1.json
        │
        │  change again & save
        ▼
  chat_request_<mode>_base-2_cus_<bucket>_<scope>-2.json
```

### Segment rules

| Segment | Rule |
| --- | --- |
| `<mode>` | analytics, auto, code, tenant, … |
| `base-<N>` | parent BASE pin (`base-2`, …) |
| `cus` | marks a Workbench custom fork (not BASE) |
| `<bucket>` | e.g. `travel-sample` |
| `<scope>` | normalize `_default` → `default` (no `/` in filenames) |
| `<rev>` | integer **1, 2, 3…** — bump on each material Workbench save; do not reuse |

### Lineage mapping (inside JSON)

```text
BASE file:
  _lineage.base_id   = "base-2"
  _lineage.custom_id = null
  _lineage.kind      = "base"

CUSTOM file:
  _lineage.base_id        = "base-2"          # parent BASE
  _lineage.parent_base_id = "base-2"
  _lineage.custom_id      = "cus_<bucket>_<scope>-<rev>"
  _lineage.kind           = "custom"
```

### Client / Hub notes

- Demos and new scopes load **BASE** until a custom exists for that mode+scope.
- Production pin prefers the **latest custom rev** for the scope (or explicit path in config), not always bare BASE.
- **Stamp** (`contract_id` / `contract_hash`) is independent of the filename; Hub verify/stamp still required for production.
- Do not invent production hashes; do not put `/` in filenames.



This fork standardizes **Layer A terminate** (what the model puts on `return` / terminating pipeline) and documents how that differs from **Layer B** (Detective / store). Engines or clients that assume base-1-only tool schemas may break — that is intentional for feedback.

---

## Assembled prompt shape (latest)

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1) ZEUS RULES  ·  CONTRACT / catalog  ·  HASHED when stamped    │
├─────────────────────────────────────────────────────────────────┤
│  meta: format, mode, base-{n}, custom-?, contract_hash          │
│                                                                 │
│  CONTRACT START                                                 │
│    Base-{n}                                                     │
│      • How Zeus works (efficiency, evidence-loop, tool use)     │
│      • 13 APIs (verbs + parameter schemas)                      │
│      • Response JSON schema (terminate shape)                   │
│    Base-{n}                                                     │
│      • api_weight_order[] + cost tiers                          │
│      • hard flags (ai_only_zeus_data, jail_break policy, …)     │
│  CONTRACT END                                                   │
│                                                                 │
│  optional (full profile; usually NOT hashed):                   │
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

**Wire note:** Layer A is **flat** on `return` (see schema) for model reliability. G1/G2/G3 above are **audiences** for Client redaction — not three nested JSON roots the model must invent.

**Size note:** healthy Layer A ~0.3–1.5 KB. Detective store (Layer B) is separate and much larger. Do not over-stuff Base/rules (10KB → 60KB trap).

---

## Why this exists

base-1 min catalogs require:

```text
summary · query_decomposition · decomposition · confidence
```

Production turns still often ship incomplete Layer A (Detective `output_grade: fail`). Meanwhile zeus_client needs:

- brandable fail/clarify paths (`policy_action`)
- round-stable business rule triggers
- admin-only signals (`jail_break_attempt`, `wish_i_knew`, `subject_confidence`)

without asking the model to invent the **Detective envelope** (attribution, diagnosis, spans, inject_inspect, …).

---

## Layer A vs Layer B (do not merge)

| Layer | What | Who fills | Size order |
| --- | --- | --- | --- |
| **A — terminate** | `return` tool args | **Model** | ~0.3–1.5 KB healthy |
| **B — store / Detective** | report, diagnosis, spans, inject_inspect, checklist… | **Zeus server** | ~100KB–1MB |

Client must parse **A** every turn. Server builds **B**. Model must **never** emit B fields.

Validate Layer A:

```bash
# example is self-contained; schema is draft 2020-12
# e.g. check-jsonschema -s response_output_schema.json response_output_example.json
```

---

## Layer A fields (prototype)

### Required (Detective-compatible) — G1 core

| Field | Type | Audience |
| --- | --- | --- |
| `summary` | string | **User** |
| `query_decomposition` | object | analytics / evidence loop |
| `decomposition` | object | data plan |
| `confidence` | `"high"` \| `"med"` \| `"low"` | soft UI / analytics |

### Recommended (new in base-2-prototype)

| Field | Type | Audience |
| --- | --- | --- |
| `policy_action` | `answer` \| `clarify` \| `refuse` \| `error` | **G3 Client** → `message_*` boilerplate |
| `subject_confidence` | number 0.0–1.0 | **G2 Admin** |
| `jail_break_attempt` | number 0.0–1.0 (subjective, not boolean) | **G2 Admin** |
| `wish_i_knew` | array max 3 `{what, kind, why?, severity?}` | **G2 Admin** |
| `business_rules_triggers` | `boolean[]` | **G3 Client** parallel to inject `rules[]` |
| `node_refs` / `entity_refs` / `provenance` | array | UI / grounding |

### Forbidden on terminate (server-only Layer B)

`attribution`, `decision`, `diagnosis`, `inject_inspect`, `prompt_checklist`, `spans`, `support_pack`, full `report.detail`, …

Authoritative machine schema: [`response_output_schema.json`](response_output_schema.json).  
Worked example: [`response_output_example.json`](response_output_example.json).

---

## zeus_client pass-in (not in catalog JSON body)

These stay **runtime inject / config** (not hashed into BASE body as tenant copy):

```text
business_injection.message_failure / message_clarify / …
business_injection.rules[]     # stable indexes for the session
session.zeus_round / turn_index
SCOPE BRIEF + MINI-SCHEMA
```

Client loop sketch:

```text
on return:
  show summary
  branch on policy_action → boilerplate
  apply business_rules_triggers[i] → state
  metrics.emit(jail_break_attempt, wish_i_knew)  # never UI
```

---

## What changed vs base-1 files

| Area | Change |
| --- | --- |
| `_lineage.base_id` | `base-2-prototype` (`parent_base_id: base-1`) |
| `_version` | `2` |
| `_prototype` | design metadata object |
| `return` / `pipeline` parameters | Layer A recommended fields + descriptions |
| `messages[0].content` | Layer A terminate addendum |
| `contract` | prototype builder hash (not Hub stamp) |
| Filename | `chat_request_<mode>_base-2-prototype.json` (not `*_v2_min.json`) |
| Size | ~25–27 KB per file (was ~15–17 KB base-1 min) — schema text + prompt addendum |

**Token budget:** still prefer short Client `rules[]`; do not paste policy novels into Base. Drop soft guidance first under pressure.

---

## What is *not* changed

- Still **13 verbs** (same names)
- Still **min** profile (no full `guidance` / `masq` blocks)
- **`v2/min/` latest alias** still points at **base-1** until promoted
- **CURRENT.json** still `base-1`

---

## Feedback ask (zeus_client)

1. Flat Layer A (as tool args) vs nested `{user, admin, client}` — **flat is in the verb schema + `response_output_schema.json`**; Client may re-nest when storing.  
2. Are recommended fields enough, or should any become **required** after a bake-in period?  
3. `business_rules_triggers` length policy: require `len(rules)` vs pad false?  
4. Redaction map: confirm UI never sees G2 floats / `wish_i_knew` / G3 triggers.  
5. Compat: load path for `base-2-prototype` without replacing base-1 production pin.

---

## Files

```text
v2/base/base-2-prototype/
  PROTOTYPE.md
  response_output_schema.json    # json-schema.org draft 2020-12
  response_output_example.json   # valid Layer A instance
  MANIFEST.json
  min/
    chat_request_<mode>_base-2-prototype.json   # 10 modes (not *_v2_min.json)
```
