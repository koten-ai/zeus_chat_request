# Dual gap channels — `wish_i_knew` + `data_gaps` (base-5.2 design)

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · pack wire **base-5** · content **base-5.1** · design train **base-5.2** · version matrix: [COMPAT.md](../COMPAT.md)

**Audience:** catalog authors, zeus_client, Zeus Detective, Helios  
**Roadmap:** [ROADMAP.md § base-5.2](ROADMAP.md)  
**Related:** [BIBLE.md](BIBLE.md) §5 · [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) · [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)  
**Jira:** [CR-24](https://kotenai.atlassian.net/browse/CR-24) (parent CR-3)

**Status:** **design** — wire sketch + semantics. Pack schema / return-tool props land in a follow-up implement PR (not required for this doc).

---

## 0. One-sentence answer

**Yes — keep the old idea and append the new one.**  
Do **not** overload a single free-text field. Ship **two G2 channels** on terminate:

| Stream | Field | Idea |
| --- | --- | --- |
| **A — classic** | `wish_i_knew` (keep) | What *I* lacked this turn so **ops** improve brief / catalog / tools / rules / user message |
| **B — acquisition** | `data_gaps` (**new**, additive) | What **platform schema / data / index** was missing so **Helios** can rank what to collect |

Both optional · max-capped · never chat UI · sparse.

---

## 1. Why two streams

### 1.1 Product loop (shared)

```text
User question
  → catalog (system + verbs + MINI-SCHEMA / SCOPE BRIEF)
  → AI tools / pipeline
  → terminate Layer A
       ├─ summary (G1 user)
       ├─ wish_i_knew (G2 ops feedback)      ← A
       └─ data_gaps (G2 acquisition)         ← B  (base-5.2)
  → Client store / Zeus report → Detective + Helios
```

### 1.2 Different questions

| | **A `wish_i_knew`** | **B `data_gaps`** |
| --- | --- | --- |
| Question | “What confused or blocked *me* this turn?” | “What should the **platform store/index** next?” |
| Consumer | Detective 💡, Workbench, prompt authors | Helios Motions / data backlog |
| Text | Prose OK | Prefer **machine keys** (`entity_type`, `field`) |
| Includes user omitted dates? | Yes (`kind: message`) | **No** — that is form UX, not ingest |
| Includes missing `Beer.abv` in schema? | Can note as `schema` | **Yes** — primary use |

Collapsing both into one array forces Helios to filter noise (rules / message / tool) and makes `GROUP BY field` unreliable.

---

## 2. Stream A — classic `wish_i_knew` (unchanged intent)

### 2.1 Semantics (keep)

- **Past tense:** gaps **this turn** that the **model** lacked.  
- **Not** “what the user wanted” → that is `query_decomposition`.  
- **G2 admin only** — never `summary` / chat UI.  
- **Optional.** Empty `[]` or omit when the turn was smooth.  
- **Cap:** max **3** items.

### 2.2 Shape (base-4 / base-5 catalog SoT)

```json
"wish_i_knew": [
  {
    "what": "city and stay dates",
    "kind": "message",
    "why": "cannot search inventory without a stay window",
    "severity": "med"
  }
]
```

| Field | Req |
| --- | --- |
| `what` | Short gap statement (required) |
| `kind` | `rules` \| `message` \| `schema` \| `data` \| `tool` \| `other` (required) |
| `why` | Optional how knowing it would change the answer |
| `severity` | Optional `low` \| `med` \| `high` |

### 2.3 Zeus engine note (today)

Live Zeus `return_result` still documents **`wish_i_knew` as an optional string** (Detective 💡 bubbles).  

**Migration:** Client/Zeus should **dual-read** until one shape wins:

| Wire | Accept as A |
| --- | --- |
| `string` | → one synthetic item `{ what: s, kind: "other" }` or keep string in trace only |
| `object[]` | canonical base-4/5 |

Dual-read window: **≤1 Client/engine release** after array is universal (same spirit as base-5 array triggers).

### 2.4 Classic examples

| Situation | Item |
| --- | --- |
| User said “list IPAs” but no city/dates needed? N/A | — |
| User asked free-night promo; no rule | `{ kind: "rules", what: "authorized free-night promo" }` |
| Brief didn’t say description is FTS | `{ kind: "schema", what: "description is text_fts not where-eq" }` |
| Tool docs unclear on traverse direction | `{ kind: "tool", what: "beer→brewery edge direction" }` |

---

## 3. Stream B — `data_gaps` (new, base-5.2)

### 3.1 Semantics

When the model **cannot fully answer** because the **platform** lacks:

- a **field / type** in schema or map,  
- **rows / coverage** for an entity, or  
- an **index / query capability** (e.g. FTS facet),

emit **structured acquisition gaps** for Helios — not for end users.

**Not for:** missing user parameters (use A `message`), missing jailbreak rules (A `rules`), model uncertainty alone (use `confidence` / `wish_i_knew`).

### 3.2 Shape (design sketch — additive Layer A)

```json
"data_gaps": [
  {
    "what": "ABV not available on Beer nodes for ranking",
    "kind": "schema",
    "entity_type": "Beer",
    "field": "abv",
    "path": "metadata.abv",
    "why": "user asked top-5 highest ABV; field absent from MINI-SCHEMA and samples",
    "severity": "high",
    "blocked_answer": true
  }
]
```

| Field | Required | Notes |
| --- | --- | --- |
| `what` | **yes** | Short human label |
| `kind` | **yes** | **`schema`** \| **`data`** \| **`index`** only |
| `entity_type` | recommended | Closed when known from MINI-SCHEMA |
| `field` | recommended | Property / facet name |
| `path` | optional | JSON path if nested |
| `why` | optional | How it blocked the answer |
| `severity` | optional | `low` \| `med` \| `high` |
| `blocked_answer` | optional | `true` if this gap prevented a full answer |

**Cap:** max **3** items (same budget discipline as A; Helios wants rates not essays).  
**Optional field:** omit or `[]` when nothing acquisition-related.

### 3.3 Decision rules (A vs B)

| Situation | A `wish_i_knew` | B `data_gaps` |
| --- | --- | --- |
| User omitted city / dates | `kind: message` | — |
| Policy / coupon rule missing | `kind: rules` | — |
| Field not in MINI-SCHEMA / map | optional note | **`kind: schema`** + `entity_type`/`field` |
| Type exists, zero matching rows | optional | **`kind: data`** |
| Need FTS / vector / index capability | optional | **`kind: index`** |
| Wasted round on wrong tool syntax | `kind: tool` or `schema` | — unless true missing field |
| Answered fully from tools | `[]` / omit | `[]` / omit |

**Anti-pattern:** listing every field not used this turn. Only gaps that **blocked or forced a weak answer**.

### 3.4 Examples

**Blocked by missing field (Helios gold):**

```json
{
  "summary": "I can list beers by name, but cannot rank by ABV with current schema.",
  "confidence": "low",
  "policy_action": "clarify",
  "wish_i_knew": [],
  "data_gaps": [
    {
      "what": "Beer.abv missing",
      "kind": "schema",
      "entity_type": "Beer",
      "field": "abv",
      "blocked_answer": true,
      "severity": "high"
    }
  ]
}
```

**User message gap only (no Helios ingest):**

```json
{
  "summary": "Which city and dates should I search?",
  "confidence": "low",
  "policy_action": "clarify",
  "wish_i_knew": [
    {
      "what": "city and stay dates",
      "kind": "message",
      "severity": "med"
    }
  ],
  "data_gaps": []
}
```

**Both (rule + data coverage):**

```json
{
  "wish_i_knew": [
    {
      "what": "whether free-night promos are allowlisted",
      "kind": "rules",
      "severity": "low"
    }
  ],
  "data_gaps": [
    {
      "what": "no Inventory rows for requested window",
      "kind": "data",
      "entity_type": "Inventory",
      "blocked_answer": true,
      "severity": "high"
    }
  ]
}
```

---

## 4. Helios / cost law

From [HELIOS_WISHLIST](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) §0: prefer **cheap** Zeus/Client emits; AI free text is expensive for dashboards.

| Emit | Who | Use |
| --- | --- | --- |
| Raw `data_gaps[]` | Client or Zeus report (copy from terminate) | Drill-down / samples |
| `data_gaps_count` | **Precomputed** (Client/Zeus) | Charts |
| `data_gaps_by_kind` | Precomputed map | Motions filters |
| Top `entity_type.field` | Session/job rollup | “What to collect” leaderboard |

**Do not** require Helios to UNNEST prose from A to build the backlog — use **B** only for acquisition Motions.

Optional HEL-WISH cross-link: treat B as **Pri-2 mixed** (AI proposes structured gaps; Zeus/Client roll up). Not new required Layer A every turn.

---

## 5. Audience / ownership

| Field | App | Client | AI | UI chat |
| --- | --- | --- | --- | --- |
| `wish_i_knew` | R metrics | R → store / Detective; never UI | **S C U** | **no** |
| `data_gaps` | R Helios | R → report + precompute | **S C U** | **no** |

Client must not forge B and pretend the model said it (same as triggers → flags pattern).

---

## 6. Wire / BASE law

| | |
| --- | --- |
| **Train** | **base-5.2** — additive optional G2 on base-5 wire |
| **Breaking?** | **No** if `data_gaps` is optional and `wish_i_knew` stays array |
| **Required four** | Unchanged |
| **Objects / app_output** | Unchanged (base-5 freeze) |
| **On disk** | **`v2/base/base-5.2/`** full snapshot (parent `base-5.1`); Diff vs 5.1 |

### Rejected for default

| Shape | Why not default |
| --- | --- |
| Nest `wish_i_knew: { feedback, acquisition }` | Breaks array consumers + Zeus string harder |
| Only extend A kinds with free text | Helios cannot GROUP BY reliably |
| Put acquisition prose in `summary` | Wrong audience; pollutes G1 |

---

## 7. Implement checklist (follow-up PR — not this design alone)

- [ ] `response_output_schema.json`: add `data_gaps` + `$defs/data_gap_item`  
- [ ] `response_output_example.json`: one B item when useful  
- [ ] Return / pipeline tool params in min JSON (all modes)  
- [ ] CORE terminate table: row for `data_gaps`  
- [ ] Re-export text; `verify_base_pack.py`  
- [ ] Client: parse A (array|string) + B; redaction; report emit  
- [ ] Zeus: Detective badge optional for B; dual-read A string  
- [ ] Helios: ingest report fields + precomputed counters  
- [ ] RELEASE_NOTES + COMPAT note  

---

## 8. Non-goals

- Make A or B **required** every turn  
- Full inventory of all unused schema fields  
- Replace Detective string path overnight without dual-read  
- Soft HINTS / A/B paste (**base-6**)  
- Pin promote  

---

## 9. Agent quick path

```text
1. Keep wish_i_knew = operator turn gaps (array design)
2. Add data_gaps = Helios acquisition gaps (schema|data|index + keys)
3. Never mix user message gaps into data_gaps
4. Never show either in chat UI
5. Helios: structure B + precompute counts
```
