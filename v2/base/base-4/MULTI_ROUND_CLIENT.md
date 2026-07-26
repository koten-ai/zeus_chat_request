# Multi-round data model (zeus_client) — base-4

**Audience:** zeus_client / middleman  
**Related:** [OVERVIEW.md](OVERVIEW.md) · [response_output_schema.json](response_output_schema.json) · [response_output_example.json](response_output_example.json)

---

## Short answer: yes, still append an array

When everything was “JSON back and forth,” the easy pattern was:

```text
messages = []
messages.append(user)
messages.append(assistant tool_calls)
messages.append(tool results)
messages.append(...)
```

**That still works.** The middleman still owns one **transcript array** (`messages`) that grows every round.

What base-4 adds is **not** a different transport — it is:

1. **Clear bags** for what is *not* just another chat message (catalog, injects, UI artifacts, admin metrics).  
2. A **final Layer A object** on `return` (structured terminate), which you also store — not as free text, but as parsed JSON args.

```text
Bag C  messages[]     ← still append every round (AI + Zeus tool I/O)
Bag D  artifacts      ← Client copies/enrichment for UI (not raw re-prompt)
Layer A last_terminate ← only on final return (G1/G2/G3)
```

---

## Four bags (session state)

```text
A. CATALOG     chat_request base-4, contract pin          (stable)
B. INJECTS     brief, mini-schema, business_injection     (session/turn)
C. MESSAGES[]  OpenAI-style transcript                    (append-only)
D. ARTIFACTS   tables, id index, flags, last_terminate    (Client-built)
```

| Bag | Append array? | Notes |
| --- | --- | --- |
| **C messages** | **Yes** — primary loop | What the model sees next round |
| **D tool_log** | Optional parallel array | Meta only (latency, verb, ids) |
| **D tables / entities** | Upsert maps/lists | Enrichment, not full re-prompt |
| **A / B** | No | Replace when pin/inject changes |

---

## Two-round example (one user turn)

Scenario: user asks for top beers; Client has catalog + injects already loaded.

### Session skeleton (before round 1)

```json
{
  "session_id": "sess_001",
  "catalog": {
    "mode": "analytics",
    "base_id": "base-4",
    "file": "chat_request_analytics_base-4.json",
    "contract_id": "analytics_b4proto",
    "contract_hash": "md5:…"
  },
  "injects": {
    "scope": "beer-sample/_default",
    "scope_brief": "## SCOPE BRIEF …",
    "mini_schema": "## MINI-SCHEMA … Beer, Brewery …",
    "business_injection": {
      "message_failure": "Sorry — could you rephrase what you want to know about beers?",
      "rules": [
        "",
        "if they mention a coupon, note coupon applicable"
      ]
    }
  },
  "control": {
    "zeus_round": 0,
    "max_rounds": 8,
    "flags": {}
  },
  "messages": [],
  "artifacts": {
    "entities": {},
    "tables": [],
    "tool_log": [],
    "last_terminate": null
  }
}
```

---

### Round 1 — request to AI API

Client builds the model request from **A + B + C** (C still empty of tools):

```json
{
  "model": "…",
  "tools": ["describe", "get", "find", "…", "return"],
  "messages": [
    {
      "role": "system",
      "content": "<catalog system prompt + SCOPE BRIEF + MINI-SCHEMA + business rules>"
    },
    {
      "role": "user",
      "content": "Top 5 highest ABV beers with name and abv"
    }
  ]
}
```

**Client after send:**

```text
control.zeus_round = 1
messages (bag C) already includes system + user  // or system held separate — either works
```

Recommended: keep **one** `messages[]` the Client owns; system may be prepended only at call time if you cache catalog.

---

### Round 1 — response from AI API (tool call, not final)

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_1",
      "type": "function",
      "function": {
        "name": "pipeline",
        "arguments": "{\"steps\":[{\"as\":\"cands\",\"verb\":\"find\",\"entity_type\":\"Beer\",\"limit\":100},{\"as\":\"ord\",\"verb\":\"order\",\"ids\":\"@cands.ids\",\"by\":\"abv\",\"direction\":\"desc\"},{\"as\":\"top\",\"verb\":\"project\",\"ids\":\"@ord.ids\",\"fields\":[\"name\",\"abv\"],\"limit\":5}]}"
      }
    }
  ]
}
```

**Middleman append (bag C) — still just an array push:**

```json
messages.push({
  "role": "assistant",
  "content": null,
  "tool_calls": [ /* same as above */ ]
})
```

---

### Round 1 — Zeus executes tools → data back

Client calls Zeus with the pipeline (or demuxed verbs). Example **tool result** payload (simplified):

```json
{
  "tool_call_id": "call_1",
  "name": "pipeline",
  "status": "ok",
  "result": {
    "top": {
      "rows": [
        { "id": "beer:1", "name": "Skull Crusher", "abv": 12.5 },
        { "id": "beer:2", "name": "Barley Monster", "abv": 11.8 },
        { "id": "beer:3", "name": "Night Oil", "abv": 11.2 },
        { "id": "beer:4", "name": "Iron Bock", "abv": 10.9 },
        { "id": "beer:5", "name": "Forge Ale", "abv": 10.5 }
      ]
    }
  }
}
```

**Append to transcript (bag C) — model needs this next round:**

```json
messages.push({
  "role": "tool",
  "tool_call_id": "call_1",
  "content": "{\"top\":{\"rows\":[{\"id\":\"beer:1\",\"name\":\"Skull Crusher\",\"abv\":12.5},…]}}"
})
```

**Also enrich (bag D) — product/UI copy, not only string blob:**

```json
artifacts.tool_log.push({
  "round": 1,
  "tool_call_id": "call_1",
  "verb": "pipeline",
  "status": "ok",
  "latency_ms": 12
})

artifacts.tables.push({
  "source": "call_1",
  "columns": ["name", "abv"],
  "rows": [ /* same 5 rows, structured */ ]
})

artifacts.entities["beer:1"] = { "name": "Skull Crusher", "abv": 12.5 }
// … beer:2–5
```

So: **yes, append array for the middleman loop**; **plus** optional structured copies for UI.

---

### Round 2 — request to AI API (same array, grown)

```json
{
  "model": "…",
  "tools": ["…", "return"],
  "messages": [
    { "role": "system", "content": "…" },
    { "role": "user", "content": "Top 5 highest ABV beers with name and abv" },
    {
      "role": "assistant",
      "tool_calls": [ { "id": "call_1", "function": { "name": "pipeline", "arguments": "…" } } ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_1",
      "content": "{ \"top\": { \"rows\": [ …5 beers… ] } }"
    }
  ]
}
```

**This is the same “append-only messages[]” pattern as classic JSON chat.**  
Nothing about base-4 Layer A changes that mid-turn.

`control.zeus_round = 2`

---

### Round 2 — response from AI API (terminate / Layer A)

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_2",
      "type": "function",
      "function": {
        "name": "return",
        "arguments": {
          "summary": "Top 5 highest ABV beers: Skull Crusher 12.5%, Barley Monster 11.8%, Night Oil 11.2%, Iron Bock 10.9%, Forge Ale 10.5%.",
          "confidence": "high",
          "query_decomposition": {
            "intent": "Top",
            "entity": "Beer",
            "attribute": "abv"
          },
          "decomposition": {
            "targets": [{ "entity_type": "Beer", "focus": ["name", "abv"] }],
            "predicates": {},
            "output": "rows"
          },
          "policy_action": "answer",
          "subject_confidence": 0.93,
          "jail_break_attempt": 0.0,
          "wish_i_knew": [],
          "business_rules_triggers": [false, false],
          "node_refs": ["beer:1", "beer:2", "beer:3", "beer:4", "beer:5"],
          "entity_refs": [],
          "provenance": [{ "step": "pipeline", "as": "top" }]
        }
      }
    }
  ]
}
```

*(Some providers pass `arguments` as a stringified JSON object — parse it.)*

**Append assistant tool_call (optional for audit):**

```json
messages.push({ role: "assistant", tool_calls: [/* call_2 return */] })
```

**Do not need another Zeus call** for pure `return` (Client-local terminate).

**Parse Layer A → split audiences:**

```json
artifacts.last_terminate = { /* parsed arguments object */ }

// G1 USER
ui.show(artifacts.last_terminate.summary)
// optional: render artifacts.tables already filled from round 1

// G3 CLIENT
// business_rules_triggers[1] === true → control.flags.coupon = true
control.flags = { /* from triggers */ }

// G2 ADMIN (never UI)
metrics.emit({
  subject_confidence: 0.93,
  jail_break_attempt: 0.0,
  wish_i_knew: []
})
```

**User turn complete.**

---

## Full `messages[]` after two rounds (picture)

```text
messages = [
  { role: system,  content: catalog+injects },           // or injected at call time
  { role: user,    content: "Top 5 highest ABV…" },
  { role: assistant, tool_calls: [pipeline call_1] },    // round 1 AI
  { role: tool,    tool_call_id: call_1, content: "…" }, // round 1 Zeus
  { role: assistant, tool_calls: [return call_2] },      // round 2 AI (terminate)
]
```

That is still **one array, append each hop.**

---

## What is *not* in `messages[]`

| Data | Where |
| --- | --- |
| Flattened UI table of 5 beers | `artifacts.tables` |
| Entity map by id | `artifacts.entities` |
| Layer A admin scores | `artifacts.last_terminate` + metrics backend |
| Detective spans / diagnosis | Zeus server Layer B (not Client loop) |
| Full re-copy of catalog every time | Cache bag A |

---

## Second user turn (optional)

New user message → **append** again:

```json
messages.push({ "role": "user", "content": "Which of those is hoppiest?" })
control.zeus_round = 1  // reset round clock for this user turn, or keep global — product choice
```

Policy choice:

- **Keep** prior tool results in `messages` (multi-turn memory), or  
- **Summarize/truncate** old tool JSON and rely on `artifacts.entities` + a short client note  

Either way, the mechanical pattern stays **append (or compact-then-append)**.

---

## Minimal Client loop (pseudocode)

```text
messages = [system, user]

for round in 1..max_rounds:
  resp = ai.chat(messages, tools)

  if resp.tool_calls are all non-return verbs:
    messages.append(assistant with tool_calls)
    for tc in tool_calls:
      result = zeus.execute(tc)
      messages.append(tool result)              # append array
      artifacts.upsert_from_zeus(result)        # enrichment copy
    continue

  if resp has return (or terminating pipeline fields):
    messages.append(assistant with return)      # optional audit
    layer_a = parse(return.arguments)
    artifacts.last_terminate = layer_a
    ui.show(layer_a.summary)                    # G1
    apply_triggers(layer_a.business_rules_triggers)
    metrics.emit(layer_a admin fields)          # G2
    break

  # plain text without return → treat as protocol miss / force clarify
```

---

## Two-round vs “all JSON blob”

| Old comfort | base-4 middleman |
| --- | --- |
| Append JSON messages | **Same** |
| Zeus result as JSON string in tool message | **Same** |
| Final answer as free text | **Prefer** structured `return` args (Layer A) |
| Everything in one array forever | **Split**: transcript vs artifacts vs metrics |

So: **keep the array for the middleman brain-loop**; use **extra bags** so UI and admin don’t fight the prompt.

---

## Tiny “happy path” checklist

1. `messages.append` user  
2. Round 1: AI tools → `append` assistant + tool results; **upsert artifacts**  
3. Round 2: AI `return` → parse Layer A  
4. Show **summary** only to user  
5. Store **last_terminate** + metrics  
6. Ready for next user message (append again)

---

## Files in this folder

| File | Role |
| --- | --- |
| This doc | Multi-round Client model + examples |
| `response_output_schema.json` | Layer A schema (final return) |
| `response_output_example.json` | Layer A example instance |
| `min/*.json` / `text/*.txt` | base-4 catalogs |

For a fuller hotel/coupon Layer A example, see `response_output_example.json`. For the terminate field table the model sees, open any `text/chat_request_*_base-4.txt` section `## Terminate (Layer A)`.
