# Helios wishlist — structured requests for chat_request / traces

**Canonical home:** [koten-ai/zeus_chat_request](https://github.com/koten-ai/zeus_chat_request) · branch **`helios-beta`**  
**Audience:** catalog / Workbench / Zeus / Zeus Client · Helios Motions  
**Consumer:** [Helios](https://github.com/koten-ai/Helios) via Analytics `` `zeus_sessions`.`session`.`traces` ``  

| Related | |
| --- | --- |
| Catalogs | [`v2/min/`](v2/min/) · [`v2/base/`](v2/base/) · [CHAT_REQUEST.md](CHAT_REQUEST.md) |
| Helios today | `QUERY_DECOMPOSITION` on report · Explore live charts |
| Process | Each item is a **Request** — not a committed schema until accepted into a BASE / Zeus emit |

---

## 0. Cost sensitivity (read this first)

Helios must be **stingy about what it asks the AI to emit**.

| Provider | Relative cost | Why |
| --- | --- | --- |
| **AI** | **Expensive** | Tokens, latency, failure modes, prompt bloat, wrong extractions poison Analytics forever |
| **Zeus** | **Cheap** | Code path on terminate — already has tools, status, counts, policy |
| **Zeus Client (middle)** | **Cheap** | Headers / SDK fields once per session or turn — no model |

### Rules for every Request

1. **Prefer cheap providers** — If Zeus or Zeus Client can supply the fact, **do not** put it on the model.  
2. **AI only for meaning in the ask** — Language the runtime cannot know.  
3. **Piggyback before expand** — Enrich fields the model already emits via **Zeus post-process**.  
4. **`optional_when` over always-on** — Never require expensive fields on every turn.  
5. **Priority is cost-aware** — See §1.1 (scale **1–5**).  
6. **Emit types Helios can query** — numbers as **JSON numbers**, not strings; add **precomputed sums** when dashboards would otherwise scan arrays (§0.1).

```text
Cost-aware pipeline (good):
  User text
    → AI: only facets it already owes (intent, entity, optional geo/price strings)
    → Zeus Client: tz, language, channel, market country (cheap)
    → Zeus: outcome, tool_usage, geocode(geo), counts/sums, Analytics sink (cheap)

Cost-blind pipeline (bad):
  → AI: lat/lon, sentiment, JTBD, 12 new structured bags every turn
```

---

## 0.1 Raw vs precomputed — query cost (read this second)

Helios runs **SQL++ over Analytics**. Every chart is either:

- a cheap filter / `GROUP BY` / `AVG` on **scalar fields**, or  
- an expensive (or impossible) walk of nested arrays at query time.

**Rule:** If Helios will **count, sum, average, or filter on a metric often**, Zeus should emit a **precomputed scalar** on the turn (or session). Keep the **raw array** only when drill-down needs detail.

### Anti-pattern (hard for Helios)

```json
{
  "turns": [
    { "time_ms": 2, "step": "search" },
    { "time_ms": 4, "step": "rank" }
  ]
}
```

To get total time Helios must UNNEST/scan every turn on every dashboard query:

```sql
-- painful at scale / awkward in Analytics
SUM(t.time_ms) over unnested turns …
```

### Preferred (raw **and** precomputed)

```json
{
  "turns": [
    { "time_ms": 2, "step": "search" },
    { "time_ms": 4, "step": "rank" }
  ],
  "turn_time_sum_ms": 6,
  "turn_count": 2,
  "turn_time_avg_ms": 3.0
}
```

| Field | JSON type | Role |
| --- | --- | --- |
| `turns[]` | array of objects | **raw** — Detective / Explain drill-down |
| `turn_time_sum_ms` | **number** (int) | **precomputed** — charts, filters, AVG across sessions |
| `turn_count` | **number** (int) | **precomputed** |
| `turn_time_avg_ms` | **number** (float) | **precomputed** (optional if sum+count present) |

Helios chart query becomes:

```sql
AVG(t.report.turn_time_sum_ms) AS avg_path_ms
```

### Data kind values (use on every Request)

| Kind | Emit | Helios does |
| --- | --- | --- |
| **raw** | Detail arrays / free text / ids for drill-down | Rare UNNEST, sample lists, deep links |
| **precomputed** | Scalars: counts, sums, rates, mins, maxes | Default for Motions charts |
| **both** | Raw **plus** scalars derived at emit time | Best default when detail exists |

**Who computes precomputed?** Almost always **Zeus** (cheap, exact). Not AI. Not Helios at query time if avoidable.

### JSON typing rules (explicit)

| Want | Do | Don’t |
| --- | --- | --- |
| Integer count / ms | `"user_visible_count": 0`, `"duration_ms": 2408` | `"user_visible_count": "0"` |
| Float rate / avg | `"miss_rate": 12.5`, `"lat": 48.137` | `"lat": "48.137"` |
| Boolean | `"synthetic": false` | `"synthetic": "false"` |
| Enum / code | `"kind": "empty"`, `"country_iso": "DE"` | free prose in enum fields |
| Money | `"max": 100`, `"currency": "EUR"` | `"max": "100"` or `"$100"` only |
| Missing | omit key or `null` | `""` for numbers |

**Examples in each Request below are normative shape sketches** — types in the sample are intentional.

---

## 1. Request schema

| Attribute | Meaning |
| --- | --- |
| **ID** | `HEL-WISH-###` |
| **Title** | Short name |
| **Business requirement** | Operator / product need |
| **Insight sought** | Question Helios answers |
| **Example** | Concrete “aha” |
| **Fields** | Paths + **JSON types** |
| **JSON example** | Minimal object with correct types |
| **Required?** | required · optional · optional_when · recommended |
| **Provider** | AI / Zeus Client / Zeus (primary first) |
| **AI load** | none · piggyback · light · heavy |
| **Cost class** | cheap · mixed · expensive |
| **Data kind** | raw · precomputed · **both** (list which fields are which) |
| **Motions** | Helios motions |
| **Cardinality** | GROUP BY safety |
| **Privacy** | PII / geo precision |
| **Provenance** | confidence / source? |
| **Priority** | **1–5** |
| **Depends on** | Other IDs |
| **Acceptance** | Done when… |
| **Notes** | Cheaper alternatives |

### 1.1 Priority scale (1–5)

| Score | Meaning |
| ---: | --- |
| **1** | Do first — high value · **cheap** (Zeus/Client) |
| **2** | Do soon — high value · cheap or enrich-only (no new AI tax) |
| **3** | Scheduled — needs AI or larger work · `optional_when` |
| **4** | Backlog — AI-heavy / narrow |
| **5** | Defer — soft AI; default off |

| | High business value | Low business value |
| --- | --- | --- |
| **Cheap (Zeus / Client)** | **1–2** | **2–3** |
| **Expensive (AI-primary)** | **3** | **4–5** |

### Template

```markdown
### HEL-WISH-000 — Title

| Attribute | Value |
| --- | --- |
| **Business requirement** | … |
| **Insight sought** | … |
| **Example** | … |
| **Fields** | `a` number(int), `b` string, `items[]` raw |
| **JSON example** | see fenced block |
| **Required?** | optional_when: … |
| **Provider** | Zeus (primary) |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | both — raw: … · precomputed: … |
| **Motions** | … |
| **Priority** | 1 |
| **Acceptance** | … |
```

```json
{
  "example_count": 3,
  "example_sum_ms": 12,
  "example_items": [
    { "ms": 4, "name": "a" },
    { "ms": 8, "name": "b" }
  ]
}
```

---

## 2. Provider glossary

| Provider | Cost | Role |
| --- | --- | --- |
| **AI** | $$$ | Meaning in natural language |
| **Zeus Client** | $ | tz, language, channel, UI filters, market |
| **Zeus** | $ | report, tools, geocode, **sums/counts**, Analytics |

---

## 3. Request index (priority order)

| Pri | ID | Title | Cost | AI load | Data kind | Primary |
| ---: | --- | --- | --- | --- | --- | --- |
| **1** | [003](#hel-wish-003--outcome-quality-beyond-statusok) | Outcome quality | cheap | none | **both** | Zeus |
| **1** | [008](#hel-wish-008--path--rail--evidence-counts) | Path / rail / evidence | cheap | none | **both** | Zeus |
| **1** | [007](#hel-wish-007--locale-language-timezone) | Locale / tz | cheap | none | raw | Client |
| **1** | [009](#hel-wish-009--channel--tenant-safe-identity) | Channel / tenant | cheap | none | raw | Client+Zeus |
| **2** | [002](#hel-wish-002--client--session-market-geo) | Market geo | cheap | none | raw | Client |
| **2** | [001](#hel-wish-001--structured-place-geo_norm) | `geo_norm` | mixed | piggyback | raw (+ optional precompute later) | Zeus geocode |
| **3** | [004](#hel-wish-004--numeric-price_norm) | `price_norm` | mixed | light / none | raw | Client or AI |
| **3** | [005](#hel-wish-005--intent_norm-stable-enum) | `intent_norm` | mixed | light / none | raw | Zeus map or AI |
| **3** | [011](#hel-wish-011--optional-precomputed-demand-rollups) | Demand rollups | cheap | none | **precomputed** | Zeus jobs |
| **4** | [006](#hel-wish-006--constraints--party) | Constraints / party | mixed | light–heavy | raw | Client forms preferred |
| **5** | [010](#hel-wish-010--soft-ai-insights-jtbdsentiment) | JTBD / sentiment | expensive | heavy | raw | AI |

### Build order

```text
1. Zeus: outcome scalars + path/evidence counts/sums
2. Client: language, tz, channel, tenant, market geo
3. Zeus: geocode existing free-text geo → geo_norm numbers
4. AI only if needed: intent_norm / price_norm (optional_when)
5. Defer: AI constraints, soft sentiment
```

---

## 4. Requests (detail)

### HEL-WISH-003 — Outcome quality beyond `status=ok`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Know empty vs error vs success **with how many results** — without re-parsing tool payloads. |
| **Insight sought** | Real fill rate · empty reasons · Refine queues. |
| **Example** | Hits = `kind=="ok"` AND `user_visible_count > 0`. |
| **Fields** | See JSON — all counts are **numbers**, kind is **string enum**. |
| **Required?** | `kind` + `user_visible_count` recommended → required on terminate. |
| **Provider** | **Zeus** (from tools / return payload). Not AI. |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | **both** — precomputed scalars always; raw ids optional for drill-down |
| **Motions** | Explore, Refine, Funnel, Verify, Triage |
| **Priority** | **1** |
| **Acceptance** | `AVG(user_visible_count)`, `GROUP BY empty_reason` work without UNNEST. |

**JSON example** (types intentional):

```json
{
  "outcome": {
    "kind": "empty",
    "empty_reason": "no_hits",
    "user_visible_count": 0,
    "top_result_ids": [],
    "policy_codes": [],
    "reask": false
  }
}
```

Success example:

```json
{
  "outcome": {
    "kind": "ok",
    "user_visible_count": 12,
    "top_result_ids": ["doc:1", "doc:2", "doc:3"],
    "policy_codes": [],
    "reask": false
  }
}
```

| Path | Type | Kind |
| --- | --- | --- |
| `outcome.kind` | string enum | raw (low cardinality) |
| `outcome.empty_reason` | string enum \| null | raw |
| `outcome.user_visible_count` | **number (int ≥ 0)** | **precomputed** |
| `outcome.top_result_ids` | string[] | raw (drill-down; cap length e.g. 10) |
| `outcome.policy_codes` | string[] | raw |
| `outcome.reask` | boolean | precomputed flag |

**Notes:** Do not store counts as strings. Helios must not sum array lengths at query time if a scalar exists.

---

### HEL-WISH-008 — Path / rail / evidence counts

| Attribute | Value |
| --- | --- |
| **Business requirement** | Path metrics as **scalars** for Explain/Remember charts; keep step detail only for drill-down. |
| **Insight sought** | Coverage · rail usage · total path time · tool call volume. |
| **Example** | `AVG(path.duration_sum_ms)`, `GROUP BY path.rail_id`. |
| **Provider** | **Zeus** only |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | **both** |
| **Motions** | Explain, Remember, Funnel, Explore |
| **Priority** | **1** |

**JSON example:**

```json
{
  "path": {
    "stage": "candidates",
    "rail_id": null,
    "named_query": null,
    "branch_count": 2,
    "evidence_ref_count": 3,
    "missing_refs": 0,
    "step_count": 4,
    "duration_sum_ms": 6,
    "duration_max_ms": 4,
    "tool_calls_sum": 3,
    "steps": [
      { "name": "search", "time_ms": 2, "ok": true },
      { "name": "rank", "time_ms": 4, "ok": true }
    ]
  },
  "tool_usage": [
    { "name": "search", "count": 1, "ms": 2, "bytes": 1200 },
    { "name": "rank", "count": 1, "ms": 4, "bytes": 400 }
  ],
  "tool_calls_total": 2,
  "duration_ms": 2408
}
```

| Path | Type | Kind |
| --- | --- | --- |
| `path.steps[]` | object[] | **raw** (drill-down) |
| `path.step_count` | **number (int)** | **precomputed** = `len(steps)` |
| `path.duration_sum_ms` | **number (int)** | **precomputed** = sum of step times |
| `path.duration_max_ms` | **number (int)** | **precomputed** |
| `path.branch_count` | **number (int)** | precomputed |
| `path.evidence_ref_count` | **number (int)** | precomputed |
| `path.missing_refs` | **number (int)** | precomputed |
| `path.tool_calls_sum` | **number (int)** | precomputed |
| `tool_usage[]` | object[] | raw (already exists) |
| `tool_calls_total` | **number** | precomputed (already exists — keep numeric) |
| `duration_ms` | **number** | precomputed total turn |

**Why both:** Explain timeline needs `steps[]`; Explore cost board needs `duration_sum_ms` / `tool_calls_total` without UNNEST.

---

### HEL-WISH-007 — Locale, language, timezone

| Attribute | Value |
| --- | --- |
| **Business requirement** | Local clock and language without AI. |
| **Insight sought** | Language split · local hour peaks. |
| **Provider** | **Zeus Client** → Zeus |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | raw (session/turn envelope scalars) |
| **Motions** | Explore, Monitor, Compare |
| **Priority** | **1** |

**JSON example:**

```json
{
  "client": {
    "language": "de",
    "locale": "de-DE",
    "tz": "Europe/Berlin",
    "utc_offset_minutes": 120
  }
}
```

| Path | Type | Kind |
| --- | --- | --- |
| `client.language` | string (BCP-47 primary) | raw |
| `client.locale` | string | raw |
| `client.tz` | string (IANA) | raw |
| `client.utc_offset_minutes` | **number (int)** | raw/precomputed from tz at emit |

**Notes:** `utc_offset_minutes` is a **number** so Helios can bucket local hour with server `ts` without a tz database in SQL.

---

### HEL-WISH-009 — Channel & tenant-safe identity

| Attribute | Value |
| --- | --- |
| **Business requirement** | Multi-tenant / channel filters; no PII. |
| **Provider** | Client + Zeus |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | raw scalars |
| **Motions** | All (ops) |
| **Priority** | **1** |

**JSON example:**

```json
{
  "tenant_id": "acme",
  "app_id": "acme-web",
  "actor_role": "end_user",
  "session": {
    "channel": "web"
  }
}
```

| Path | Type |
| --- | --- |
| `tenant_id` | string |
| `app_id` | string |
| `actor_role` | string enum |
| `session.channel` | string enum |

**No** email, name, raw IP.

---

### HEL-WISH-002 — Client / session market geo

| Attribute | Value |
| --- | --- |
| **Business requirement** | Where the **user is** (market), not where the **ask points**. |
| **Insight sought** | DE-market traffic vs content-about-DE (001). |
| **Provider** | **Zeus Client** · Zeus stores · AI: no |
| **AI load** | none |
| **Cost class** | cheap |
| **Data kind** | raw |
| **Motions** | Explore, Funnel, Monitor, Route |
| **Priority** | **2** |

**JSON example:**

```json
{
  "client": {
    "market": {
      "country_iso": "DE",
      "admin1": null,
      "source": "ip",
      "confidence": 0.7
    }
  }
}
```

| Path | Type |
| --- | --- |
| `client.market.country_iso` | string (ISO-3166-1 alpha-2) |
| `client.market.admin1` | string \| null |
| `client.market.source` | string enum |
| `client.market.confidence` | **number** 0–1 |

**Notes:** Prefer this for “users in Germany” before paying for ask-geo AI.

---

### HEL-WISH-001 — Structured place (`geo_norm`)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Place **mentioned in the ask** as queryable country / coords. |
| **Insight sought** | *Thinking **about** Germany only?* |
| **Provider** | AI free-text `geo` (existing) → **Zeus geocode** fills `geo_norm`. Not model lat/long. |
| **AI load** | piggyback |
| **Cost class** | mixed |
| **Data kind** | raw per turn; optional precomputed rollups in 011 |
| **Motions** | Explore, Compare, Monitor, Route, Funnel |
| **Priority** | **2** |

**JSON example:**

```json
{
  "query_decomposition": {
    "intent": "Find",
    "entity": "Beer",
    "geo": "near Munich",
    "geo_norm": {
      "country_iso": "DE",
      "admin1": "BY",
      "locality": "Munich",
      "lat": 48.137,
      "lon": 11.575,
      "radius_km": 50,
      "confidence": 0.86,
      "source": "geocode",
      "place_id": null,
      "prompt_version": null
    },
    "synthetic": false
  }
}
```

| Path | Type | Notes |
| --- | --- | --- |
| `geo` | string | free text (AI) |
| `geo_norm.country_iso` | string | `"DE"` not `"Germany"` for GROUP BY |
| `geo_norm.lat` / `lon` | **number** (float) | **not** strings |
| `geo_norm.radius_km` | **number** \| null | |
| `geo_norm.confidence` | **number** | 0–1 |
| `synthetic` | boolean | |

**Helios query:**

```sql
WHERE t.report.query_decomposition.geo_norm.country_iso = "DE"
```

---

### HEL-WISH-004 — Numeric `price_norm`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Numeric price filters (no mock `$` UI). |
| **Provider** | **Client slider preferred (cheap)**; else AI parse (expensive); Zeus validate |
| **AI load** | none or light |
| **Cost class** | cheap if Client · expensive if AI |
| **Data kind** | raw scalars on turn |
| **Motions** | Explore, Refine, Compare, Funnel |
| **Priority** | **3** (AI) · **2** if Client sends numbers |

**JSON example:**

```json
{
  "query_decomposition": {
    "price": "under 5 euro",
    "price_norm": {
      "min": null,
      "max": 5,
      "currency": "EUR",
      "confidence": 0.7,
      "source": "user_text"
    }
  }
}
```

| Path | Type |
| --- | --- |
| `price` | string |
| `price_norm.min` | **number** \| null |
| `price_norm.max` | **number** \| null |
| `price_norm.currency` | string (ISO-4217) |
| `price_norm.confidence` | **number** |

**Bad:** `"max": "5"` or `"max": "€5"`.  
**Good:** `"max": 5`, `"currency": "EUR"`.

---

### HEL-WISH-005 — `intent_norm` stable enum

| Attribute | Value |
| --- | --- |
| **Business requirement** | Stable GROUP BY for Compare. |
| **Provider** | Prefer **Zeus** synonym map from free-text `intent`; else AI closed set |
| **AI load** | none or light |
| **Cost class** | mixed |
| **Data kind** | raw |
| **Motions** | Compare, Explore, Funnel |
| **Priority** | **3** |

**JSON example:**

```json
{
  "query_decomposition": {
    "intent": "What beers",
    "intent_norm": "find",
    "entity": "Beer",
    "entity_type": "Beer",
    "synthetic": false
  }
}
```

| Path | Type |
| --- | --- |
| `intent` | string |
| `intent_norm` | string enum (`list`\|`best`\|`find`\|`count`\|`compare`\|`detect`\|`other`) |
| `entity_type` | string \| null |

---

### HEL-WISH-011 — Optional precomputed demand rollups

| Attribute | Value |
| --- | --- |
| **Business requirement** | Scale: dashboards without scanning all turns. |
| **Provider** | Zeus / batch jobs |
| **AI load** | none |
| **Cost class** | cheap (compute, not AI) |
| **Data kind** | **precomputed only** (source of truth remains turn raw) |
| **Motions** | Explore, Monitor, Compare at scale |
| **Priority** | **3** |

**JSON example** (materialized row, not a chat_request field):

```json
{
  "bucket_day": "2026-07-24",
  "scope": "beer-sample/_default",
  "country_iso": "DE",
  "intent_norm": "find",
  "demand": 42,
  "hits": 38,
  "misses": 4,
  "miss_rate": 9.52,
  "duration_sum_ms": 120000,
  "duration_avg_ms": 2857.14,
  "job_version": "demand-rollup-v1",
  "generated_at": "2026-07-24T18:00:00Z"
}
```

All metrics are **numbers**. Helios reads `demand` / `miss_rate` directly — no array fold.

---

### HEL-WISH-006 — Constraints & party size

| Attribute | Value |
| --- | --- |
| **Business requirement** | Refine blockers as codes + numeric party size. |
| **Provider** | **Client forms preferred**; Zeus tool failures; AI last |
| **AI load** | none / light–heavy |
| **Cost class** | cheap if forms · expensive if AI |
| **Data kind** | raw (+ precomputed counts of constraint types if useful) |
| **Motions** | Refine, Funnel, Compose |
| **Priority** | **4** (AI) · **2–3** (Client) |

**JSON example:**

```json
{
  "query_decomposition": {
    "party_size": 4,
    "adults": 2,
    "children": 2,
    "constraints": [
      { "type": "date_range", "op": "eq", "value": "2026-08-01/2026-08-07", "hard": true },
      { "type": "radius_km", "op": "lte", "value": 50, "hard": false }
    ],
    "constraint_count": 2,
    "hard_constraint_count": 1
  }
}
```

| Path | Type | Kind |
| --- | --- | --- |
| `party_size` | **number (int)** | raw |
| `adults` / `children` | **number (int)** | raw |
| `constraints[]` | object[] | raw |
| `constraints[].value` for radius | **number** when numeric | raw |
| `constraint_count` | **number (int)** | **precomputed** |
| `hard_constraint_count` | **number (int)** | **precomputed** |

**Why precomputed counts:** Refine KPI “avg hard constraints” = `AVG(hard_constraint_count)` — no array scan.

---

### HEL-WISH-010 — Soft AI insights (JTBD / sentiment)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Optional narrative only — **not** hot-path GROUP BY. |
| **Provider** | AI only |
| **AI load** | heavy |
| **Cost class** | expensive |
| **Data kind** | raw (display); **no** demand aggregates from these |
| **Motions** | Explore cards, Triage |
| **Priority** | **5** |

**JSON example:**

```json
{
  "query_decomposition": {
    "job_to_be_done": "find a family-friendly hotel near the park",
    "sentiment": "neutral",
    "urgency": 0.2,
    "soft_meta": {
      "confidence": 0.55,
      "model": "…",
      "prompt_version": "soft-v1",
      "extracted_at": "2026-07-24T12:00:00Z"
    }
  }
}
```

| Path | Type |
| --- | --- |
| `job_to_be_done` | string |
| `sentiment` | string enum |
| `urgency` | **number** 0–1 |
| `soft_meta.confidence` | **number** |

**Default off** on terminate. Never use for core demand GROUP BY.

---

## 5. Provider × cost matrix

| Request | AI | Client | Zeus | Precomputed scalars? | Pri |
| --- | --- | --- | --- | --- | ---: |
| 003 outcome | — | optional | **yes** | **yes** counts | **1** |
| 008 path | — | — | **yes** | **yes** sums/counts | **1** |
| 007 locale | — | **yes** | store | offset minutes number | **1** |
| 009 channel | — | **yes** | **yes** | — | **1** |
| 002 market | — | **yes** | store | — | **2** |
| 001 geo_norm | piggyback geo | pin optional | **geocode** | lat/lon **numbers** | **2** |
| 004 price | optional | **slider** | validate | min/max **numbers** | **3** |
| 005 intent_norm | optional | — | map first | enum string | **3** |
| 011 rollups | — | — | **jobs** | **all metrics** | **3** |
| 006 constraints | last | **forms** | tools | constraint_count | **4** |
| 010 soft | **only** | — | store | — | **5** |

---

## 6. Catalog impact

| Change | Requests | Note |
| --- | --- | --- |
| No prompt growth | 002–003, 007–009, 011, 008 | Ship first |
| Zeus enrich only | 001 geocode | Best Germany path |
| Minimal AI | 004, 005 | types must be numbers/enums in guidance examples |
| Avoid hot path | 006 AI, 010 | Client forms / offline |

When documenting guidance, **show numeric JSON examples** so models and validators don’t emit `"5"` instead of `5`.

---

## 7. Helios without waiting

Today’s cheap raw scalars already on report: `duration_ms`, `rounds_total`, `tokens_*`, `tool_calls_total`, `status`, QD strings. Motions charts prefer those; wishlist adds **more scalars** and **typed norms**, not more array-only shapes.

---

## 8. How to add a Request

1. Business requirement + insight sought.  
2. **JSON example with correct types** (int/float/bool/enum).  
3. Mark each field **raw / precomputed / both**.  
4. If Helios would sum an array often → **require a precomputed scalar**.  
5. Can Zeus/Client do it? If yes, AI load = none, priority 1–2.  
6. If AI-only → priority ≥ 3, optional_when, provenance.  
7. Update index + matrix · PR `helios-beta`.

---

## 9. Open questions

- Empty: `status=ok` + `outcome.kind=empty` vs distinct status?  
- Cap length for `top_result_ids` / `path.steps`?  
- Session-level sums vs turn-level only?  
- Materialized rollup collection naming in Analytics?

---

## 10. Change log

| Date | Note |
| --- | --- |
| 2026-07-24 | Initial wishlist → structured Requests → cost-aware priority 1–5. |
| 2026-07-24 | **Explicit JSON examples + types**; **raw vs precomputed/both** with turn-time sum pattern; precomputed counts/sums on outcome/path/constraints. |
