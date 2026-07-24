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
2. **AI only for meaning in the ask** — Language the runtime cannot know (intent phrasing, place *mentioned in text*, budget *as spoken*).  
3. **Piggyback before expand** — Prefer enriching fields the model **already** emits (`geo`, `price`, `intent`) via **Zeus post-process** over new AI structured bags.  
4. **`optional_when` over always-on** — Never require expensive fields on every turn.  
5. **Priority is cost-aware** — High business value + cheap provider → top of queue. High value + AI-only → medium. Low value + AI → bottom (or reject).  
6. **Split pipelines** — e.g. AI free-text `geo` (already paid) → **Zeus geocode** `geo_norm` (cheap), not “ask the model for lat/long”.

```text
Cost-aware pipeline (good):
  User text
    → AI: only facets it already owes (intent, entity, optional geo/price strings)
    → Zeus Client: tz, language, channel, market country (cheap)
    → Zeus: outcome, tool_usage, geocode(geo), counts, Analytics sink (cheap)

Cost-blind pipeline (bad):
  → AI: lat/lon, sentiment, JTBD, 12 new structured bags every turn
```

---

## 1. Request schema

| Attribute | Meaning |
| --- | --- |
| **ID** | Stable id: `HEL-WISH-###` |
| **Title** | Short name |
| **Business requirement** | What the operator / product needs |
| **Insight sought** | Question Helios should answer |
| **Example** | Concrete “aha” |
| **Fields** | JSON paths on terminate / report / session |
| **Required?** | `required` · `optional` · `optional_when` · `recommended` |
| **Provider** | AI / Zeus Client / Zeus — **and who is primary** |
| **AI load** | `none` · `piggyback` (uses existing AI field) · `light` · `heavy` |
| **Cost class** | `cheap` (Zeus/Client) · `mixed` · `expensive` (AI-primary) |
| **Data kind** | `raw` · `precomputed` · `both` |
| **Motions** | Helios motions that benefit |
| **Cardinality** | GROUP BY safety |
| **Privacy** | PII / geo precision |
| **Provenance** | confidence / source needed? |
| **Priority** | **1–5** (see §1.1) |
| **Depends on** | Other IDs / features |
| **Acceptance** | Done when… |
| **Notes** | Risks, cheaper alternatives |

### 1.1 Priority scale (1–5)

| Score | Meaning | Typical profile |
| --- | --- | --- |
| **1** | **Do first** — ship ASAP | High insight value · **cheap** (Zeus and/or Client) · unblocks many motions |
| **2** | **Do soon** | High value · cheap **or** mixed with **no new AI surface** (enrich only) |
| **3** | **Scheduled** | Clear value · needs **AI** or larger catalog work · keep `optional_when` |
| **4** | **Backlog** | Nice-to-have · AI-heavy or narrow motion · wait for cheap path or proven need |
| **5** | **Defer / reject by default** | Soft/noisy AI · expensive · weak Analytics GROUP BY · only with strict confidence gates |

**Scoring guide (not a formula — judgment):**

| | High business value | Low business value |
| --- | --- | --- |
| **Cheap (Zeus / Client)** | **1–2** | **2–3** (still cheap — often just do it) |
| **Expensive (AI-primary)** | **3** (sometimes **2** if critical & no alternative) | **4–5** |

**Default when unsure:** lower the priority (higher number) if the provider is AI.

### Template

```markdown
### HEL-WISH-000 — Title

| Attribute | Value |
| --- | --- |
| **Business requirement** | … |
| **Insight sought** | … |
| **Example** | … |
| **Fields** | `path.a` |
| **Required?** | optional_when: … |
| **Provider** | primary / secondary |
| **AI load** | none \| piggyback \| light \| heavy |
| **Cost class** | cheap \| mixed \| expensive |
| **Data kind** | raw |
| **Motions** | … |
| **Cardinality** | low |
| **Privacy** | … |
| **Provenance** | yes/no |
| **Priority** | 1–5 |
| **Depends on** | — |
| **Acceptance** | … |
| **Notes** | cheaper alternative if any |
```

---

## 2. Provider & data-kind glossary

### Providers

| Provider | Cost | Role |
| --- | --- | --- |
| **AI** | **$$$** | Meaning in natural language under `chat_request` guidance |
| **Zeus Client (middle)** | **$** | Browser/SDK: tz, language, channel, UI filters, coarse market |
| **Zeus** | **$** | Report builder, tool results, policy, geocode, Analytics sink |

### Data kind

| Kind | Meaning |
| --- | --- |
| **raw** | Per-turn / per-session fact (Helios default) |
| **precomputed** | Aggregate/sum/rate from jobs (scale later) |
| **both** | Raw + optional rollups |

---

## 3. Request index (priority order)

Sorted by **Priority** (1 first), then cheap-before-expensive within a band.

| Pri | ID | Title | Cost class | AI load | Primary provider | Motions |
| --- | ---: | --- | --- | --- | --- | --- |
| **1** | [003](#hel-wish-003--outcome-quality-beyond-statusok) | Outcome quality bag | **cheap** | none | **Zeus** | Explore, Refine, Funnel, Verify |
| **1** | [008](#hel-wish-008--path--rail--evidence-counts) | Path / rail / evidence counts | **cheap** | none | **Zeus** | Explain, Remember, Funnel |
| **1** | [007](#hel-wish-007--locale-language-timezone) | Locale / language / timezone | **cheap** | none | **Zeus Client** | Explore, Monitor |
| **1** | [009](#hel-wish-009--channel--tenant-safe-identity) | Channel & tenant-safe identity | **cheap** | none | **Client + Zeus** | All (ops) |
| **2** | [002](#hel-wish-002--client--session-market-geo) | Client/session market geo | **cheap** | none | **Zeus Client** | Explore, Funnel, Monitor |
| **2** | [001](#hel-wish-001--structured-place-geo_norm) | Structured place (`geo_norm`) | **mixed** | **piggyback** | **Zeus geocode** (+ existing AI `geo`) | Explore, Compare, Monitor, Route |
| **3** | [004](#hel-wish-004--numeric-price_norm) | Numeric `price_norm` | mixed→expensive | light (or Client slider = none) | AI *or* **Client** | Explore, Refine, Compare |
| **3** | [005](#hel-wish-005--intent_norm-stable-enum) | `intent_norm` stable enum | expensive | light | AI (prefer Zeus synonym map first) | Compare, Explore, Funnel |
| **3** | [011](#hel-wish-011--optional-precomputed-demand-rollups) | Precomputed demand rollups | **cheap** | none | Zeus / jobs | Explore, Monitor (scale) |
| **4** | [006](#hel-wish-006--constraints--party) | Constraints & party size | expensive | light–heavy | AI (Client forms = cheap alt) | Refine, Funnel, Compose |
| **5** | [010](#hel-wish-010--soft-ai-insights-jtbdsentiment) | Soft AI (JTBD / sentiment) | **expensive** | **heavy** | AI only | Explore cards, Triage |

### Build order (recommended)

```text
1. Zeus outcome + path/evidence counts          (001-class cheap wins)
2. Client: language, tz, channel, tenant, market geo
3. Zeus geocode of existing free-text geo       (Germany filter without new AI tax)
4. Only then: AI intent_norm / price_norm       (optional_when, minimal prompt)
5. Defer constraint bags & soft AI              (or Client forms instead)
```

---

## 4. Requests (detail)

### HEL-WISH-003 — Outcome quality beyond `status=ok`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Distinguish true empty, policy deny, error, and success with N results — not only `status=ok`. |
| **Insight sought** | Real fill rate · why miss · Refine queues that aren’t generic “not ok”. |
| **Example** | Hits = `outcome.kind=ok` AND `user_visible_count > 0`. |
| **Fields** | `report.outcome.{kind, empty_reason?, user_visible_count?, top_result_ids[]?, policy_codes[]?, reask?}` |
| **Required?** | `kind` **recommended → required** on terminate once supported. |
| **Provider** | **Zeus** primary. AI must not invent outcome. Client: optional thumbs later. |
| **AI load** | **none** |
| **Cost class** | **cheap** |
| **Data kind** | raw |
| **Motions** | Explore, Refine, Funnel, Verify, Triage |
| **Cardinality** | low (enums) |
| **Privacy** | codes not free-text PII |
| **Provenance** | schema/enum version nice |
| **Priority** | **1** |
| **Depends on** | Zeus report builder |
| **Acceptance** | Probe shows outcome; Helios can migrate miss definition from `status!=ok`. |
| **Notes** | Highest leverage cheap ask. Do this before any new AI facet. |

---

### HEL-WISH-008 — Path / rail / evidence counts

| Attribute | Value |
| --- | --- |
| **Business requirement** | Explain / Remember need engine path facts, not only `rounds_total` proxies. |
| **Insight sought** | Evidence coverage · which rail · branch count. |
| **Example** | Explain gauge from `evidence_ref_count`. |
| **Fields** | `report.path.{stage?, rail_id?, named_query?, branch_count?, evidence_ref_count?, missing_refs?}` + existing `tool_usage[]` |
| **Required?** | optional → recommended when rails/stages exist |
| **Provider** | **Zeus** only |
| **AI load** | **none** |
| **Cost class** | **cheap** |
| **Data kind** | raw |
| **Motions** | Explain, Remember, Funnel, Explore (rails) |
| **Cardinality** | stages low; rail_id medium |
| **Privacy** | low |
| **Provenance** | N/A |
| **Priority** | **1** |
| **Depends on** | product stages / named queries |
| **Acceptance** | Live tool/path histogram possible |
| **Notes** | Never AI-guess stages. |

---

### HEL-WISH-007 — Locale, language, timezone

| Attribute | Value |
| --- | --- |
| **Business requirement** | Demand and peaks by locale / local clock, not only server UTC. |
| **Insight sought** | German-language asks · evening local peaks. |
| **Example** | Word cloud `language=de`; Monitor by local hour. |
| **Fields** | `client.language` / `locale`, `client.tz` or `utc_offset` |
| **Required?** | recommended when client can send |
| **Provider** | **Zeus Client** primary · Zeus stores |
| **AI load** | **none** (optional AI only if ask language ≠ UI — avoid for v1) |
| **Cost class** | **cheap** |
| **Data kind** | raw |
| **Motions** | Explore, Monitor, Compare |
| **Cardinality** | low–medium |
| **Privacy** | low |
| **Provenance** | source: accept_language \| app_setting |
| **Priority** | **1** |
| **Depends on** | client SDK |
| **Acceptance** | lab client traffic carries tz + language |
| **Notes** | Trivial cost — ship early. |

---

### HEL-WISH-009 — Channel & tenant-safe identity

| Attribute | Value |
| --- | --- |
| **Business requirement** | Multi-tenant / multi-channel filters without PII. |
| **Insight sought** | Web vs mobile · per app_id volume. |
| **Example** | Explore + `channel=mobile`. |
| **Fields** | `tenant_id` / `app_id`, `session.channel`, `actor_role` — **no** email/name |
| **Required?** | recommended in multi-tenant prod |
| **Provider** | Client (channel/app) + Zeus (tenant/actor) |
| **AI load** | **none** |
| **Cost class** | **cheap** |
| **Data kind** | raw |
| **Motions** | All (ops) |
| **Cardinality** | low–medium |
| **Privacy** | **critical** — Analytics must stay non-PII |
| **Provenance** | N/A |
| **Priority** | **1** |
| **Depends on** | auth model |
| **Acceptance** | filter by channel without scope hacks |
| **Notes** | Cheap hygiene. |

---

### HEL-WISH-002 — Client / session market geo

| Attribute | Value |
| --- | --- |
| **Business requirement** | Separate **where the user is** from **what place they asked about**. |
| **Insight sought** | DE users asking about US inventory? |
| **Example** | Funnel for `client.country_iso=DE` independent of QD geo. |
| **Fields** | `session.client.country_iso` (coarse); `source: ip|ui|crm` — **not** under QD |
| **Required?** | optional / recommended with consent policy |
| **Provider** | **Zeus Client** · Zeus stores · **AI: no** |
| **AI load** | **none** |
| **Cost class** | **cheap** |
| **Data kind** | raw |
| **Motions** | Explore, Funnel, Monitor, Route |
| **Cardinality** | low |
| **Privacy** | high care — country only |
| **Provenance** | source required |
| **Priority** | **2** |
| **Depends on** | client / privacy policy |
| **Acceptance** | Helios filter without QD |
| **Notes** | Often answers “Germany” questions **without** ask-geo AI work — prefer this when market = user location. |

---

### HEL-WISH-001 — Structured place (`geo_norm`)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Segment demand by **place of interest in the ask** (country/region/city). |
| **Insight sought** | *What are people thinking **in Germany only**?* (content about DE) |
| **Example** | Explore filter `geo_norm.country_iso=DE`. |
| **Fields** | Keep existing AI **`qd.geo`** string. Add **`qd.geo_norm.{country_iso, admin1, locality, lat, lon, confidence, source, …}`** filled preferably by **Zeus geocode**, not new model fields. |
| **Required?** | `optional_when` place signaled; never every turn |
| **Provider** | **Primary: Zeus** (geocode / normalize). **AI:** only free-text `geo` **already in QD guidance** (piggyback — do not add lat/lon to the prompt). **Client:** only if user dropped a map pin (structured, cheap). |
| **AI load** | **piggyback** (existing `geo`) — **not** heavy new extraction |
| **Cost class** | **mixed** (cheap Zeus enrich; AI cost already paid for QD) |
| **Data kind** | raw |
| **Motions** | Explore, Compare, Monitor, Route, Funnel |
| **Cardinality** | country_iso low; lat/lon high (don’t GROUP BY raw coords) |
| **Privacy** | content-geo ≠ home; prefer country/admin1 |
| **Provenance** | confidence + source (`geocode` preferred) |
| **Priority** | **2** |
| **Depends on** | geocoder keys; existing QD `geo` quality |
| **Acceptance** | ISO filter works on lab; UI uses ISO not string match |
| **Notes** | **Sensitive ask:** do **not** request model lat/long. If free-text `geo` is empty, improve guidance lightly — don’t invent a second AI pass. For “users in Germany” use **002** first. |

---

### HEL-WISH-004 — Numeric `price_norm`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Real price bands / filters (kill mock `$` UI). |
| **Insight sought** | Unmet demand under €100 · miss rate by band. |
| **Example** | `price_norm.max <= 100 AND currency=EUR`. |
| **Fields** | `qd.price` string; `qd.price_norm.{min,max,currency,confidence,source}` |
| **Required?** | `optional_when` budget signaled |
| **Provider** | **Prefer Client** price slider/filter when UI has one (**cheap**). Else **AI** parse from language (**expensive**). Zeus validate currency. |
| **AI load** | none (client path) · **light** (AI path) |
| **Cost class** | cheap if Client · **expensive** if AI-primary |
| **Data kind** | raw |
| **Motions** | Explore, Refine, Compare, Funnel |
| **Cardinality** | currency low; amounts continuous |
| **Privacy** | low |
| **Provenance** | yes if AI |
| **Priority** | **3** (AI path) · treat Client path as **2** when product has sliders |
| **Depends on** | UI or guidance |
| **Acceptance** | live filters when coverage exists |
| **Notes** | **Don’t expand AI prompt if Client can send numbers.** |

---

### HEL-WISH-005 — `intent_norm` stable enum

| Attribute | Value |
| --- | --- |
| **Business requirement** | Stable charts across wording for Compare / Funnel. |
| **Insight sought** | Share of list vs best vs find without phrase fragmentation. |
| **Example** | GROUP BY `intent_norm`. |
| **Fields** | keep `qd.intent`; add `qd.intent_norm` enum |
| **Required?** | optional → recommended |
| **Provider** | **Prefer Zeus** synonym / rules map from free-text intent (**cheap** experiment first). Else **AI** closed-set classify (**expensive**). |
| **AI load** | none (Zeus map) · **light** (AI) |
| **Cost class** | cheap if Zeus map works · expensive if AI |
| **Data kind** | raw |
| **Motions** | Compare, Explore, Funnel, Monitor |
| **Cardinality** | low |
| **Privacy** | none |
| **Provenance** | enum_version |
| **Priority** | **3** (try Zeus map before catalog AI tax) |
| **Depends on** | lab intent distribution |
| **Acceptance** | ≥80% non-synthetic coverage |
| **Notes** | Dual-write free-text + norm. |

---

### HEL-WISH-011 — Optional precomputed demand rollups

| Attribute | Value |
| --- | --- |
| **Business requirement** | Scale dashboards without full turn scans. |
| **Insight sought** | Same Explore boards, cheaper serve. |
| **Example** | Daily demand by country_iso × intent_norm. |
| **Fields** | job/materialized collection — not a substitute for raw |
| **Required?** | optional (ops scale) |
| **Provider** | Zeus / batch jobs |
| **AI load** | **none** |
| **Cost class** | **cheap** (compute $, not AI $) |
| **Data kind** | **precomputed** |
| **Motions** | Explore, Monitor, Compare at scale |
| **Cardinality** | controlled by rollup keys |
| **Privacy** | inherit raw |
| **Provenance** | job version, window |
| **Priority** | **3** (after raw P1–2 fields exist) |
| **Depends on** | 001/003/005 raw fields |
| **Acceptance** | same definitions as raw SQL |
| **Notes** | Not AI. Don’t prioritize before cheap raw emits. |

---

### HEL-WISH-006 — Constraints & party size

| Attribute | Value |
| --- | --- |
| **Business requirement** | Refine blocker types (dates, party, network). |
| **Insight sought** | Top blockers · recovery when relaxed. |
| **Example** | Histogram of `constraints[].type` on empties. |
| **Fields** | `qd.constraints[]`, party_size / adults / children |
| **Required?** | `optional_when` signaled |
| **Provider** | **Prefer Client forms** (**cheap**). **Zeus** if tools return structured fails. **AI** extract only if no form (**expensive**). |
| **AI load** | none (forms) · light–heavy (AI) |
| **Cost class** | cheap / expensive by path |
| **Data kind** | raw |
| **Motions** | Refine, Funnel, Compose |
| **Cardinality** | type low |
| **Privacy** | low–medium |
| **Provenance** | if AI |
| **Priority** | **4** (AI path) · **2–3** if Client forms ship |
| **Depends on** | 003 outcome |
| **Acceptance** | Refine blocker prototype |
| **Notes** | Don’t burn tokens if the app already collected party size. |

---

### HEL-WISH-010 — Soft AI insights (JTBD / sentiment)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Optional narrative cards only. |
| **Insight sought** | Soft “why” language · urgency proxy. |
| **Example** | Insights card if confidence high. |
| **Fields** | `qd.job_to_be_done?`, `sentiment?`, `urgency?` + AI metadata |
| **Required?** | **optional always** — never required |
| **Provider** | **AI only** |
| **AI load** | **heavy** (extra concepts every turn if enabled) |
| **Cost class** | **expensive** |
| **Data kind** | raw |
| **Motions** | Explore insights, Triage |
| **Cardinality** | high free text — **do not GROUP BY** |
| **Privacy** | may echo user language |
| **Provenance** | **mandatory** confidence + prompt_version |
| **Priority** | **5** |
| **Depends on** | cheap P1–2 shipping first |
| **Acceptance** | show only if confidence ≥ threshold; default off |
| **Notes** | **Default reject for terminate contract.** Easy to poison Analytics. Use offline/sample jobs if needed, not hot path. |

---

## 5. Provider × cost matrix

| Request | AI | Zeus Client | Zeus | Cost class | Pri |
| --- | --- | --- | --- | --- | ---: |
| 003 outcome | — | thumbs later | **yes** | cheap | **1** |
| 008 path/rail | — | — | **yes** | cheap | **1** |
| 007 locale/tz | avoid | **yes** | store | cheap | **1** |
| 009 channel/tenant | — | **yes** | **yes** | cheap | **1** |
| 002 market geo | — | **yes** | store | cheap | **2** |
| 001 geo_norm | piggyback `geo` only | map pin optional | **geocode** | mixed | **2** |
| 004 price_norm | light *or* | **slider preferred** | validate | mixed | **3** |
| 005 intent_norm | light *or* | — | **map first** | mixed | **3** |
| 011 rollups | — | — | **jobs** | cheap | **3** |
| 006 constraints | last resort | **forms preferred** | tool fails | mixed | **4** |
| 010 JTBD/sentiment | **only** | — | store | expensive | **5** |

---

## 6. Catalog impact (this repo)

| Change | Requests | Cost note |
| --- | --- | --- |
| **No prompt growth** | 002, 003, 007, 008, 009, 011 | Prefer these first — zero AI tax |
| **No new AI fields** — Zeus enrich only | 001 (geocode existing `geo`) | Best “Germany” path |
| **Minimal guidance** | 004, 005 if AI path | `optional_when`, tiny enums |
| **Avoid min-profile bloat** | 006, 010 | Client forms / offline / reject |

---

## 7. What Helios does without waiting

| Capability | Today (raw, already paid) |
| --- | --- |
| Demand language | intent, entity, theme |
| Cost / depth | duration, rounds, tokens, tools, queries |
| Proxy quality | status ok vs not |
| Rails | OK intent×entity |
| Weak threads | high rounds / not ok / missing QD |

---

## 8. How to add a Request

1. Write **business requirement** + **insight sought**.  
2. Ask: **Can Zeus or Client do this?** If yes, set AI load = none and priority 1–2.  
3. If AI-only: justify why · set priority **≥ 3** · `optional_when` · provenance required.  
4. Fill template · update index + matrix.  
5. PR to `helios-beta`.

---

## 9. Open questions

- Empty: `status=ok` + `outcome.kind=empty` vs distinct status?  
- Geocoder ownership (Zeus vs shared)?  
- When does Zeus synonym map for intent beat catalog AI?  
- When is market geo (002) “good enough” vs ask-geo (001)?

---

## 10. Change log

| Date | Note |
| --- | --- |
| 2026-07-24 | Initial wishlist; moved to `zeus_chat_request` / `helios-beta`. |
| 2026-07-24 | Structured Requests (business, insight, fields, provider, motions…). |
| 2026-07-24 | **Cost-aware priority 1–5:** AI expensive · Zeus/Client cheap; AI load + cost class; reordered build plan. |
