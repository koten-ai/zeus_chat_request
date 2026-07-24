# Helios wishlist — structured requests for chat_request / traces

**Canonical home:** [koten-ai/zeus_chat_request](https://github.com/koten-ai/zeus_chat_request) · branch **`helios-beta`**  
**Audience:** catalog / Workbench / Zeus / Zeus Client · Helios Motions  
**Consumer:** [Helios](https://github.com/koten-ai/Helios) via Analytics `` `zeus_sessions`.`session`.`traces` ``  

| Related | |
| --- | --- |
| Catalogs | [`v2/min/`](v2/min/) · [`v2/base/`](v2/base/) · [CHAT_REQUEST.md](CHAT_REQUEST.md) |
| Helios today | `QUERY_DECOMPOSITION` on report · Explore live charts |
| Process | Each item below is a **Request** — not a committed schema until accepted into a BASE / Zeus emit |

---

## 1. Request schema (use this shape for every item)

Every wishlist item is a **Request** with the same fields so product, client, and engine can triage ownership.

| Attribute | Meaning |
| --- | --- |
| **ID** | Stable id: `HEL-WISH-###` |
| **Title** | Short name |
| **Business requirement** | What the operator / product needs in plain language |
| **Insight sought** | Question Helios should answer once the data exists |
| **Example** | Concrete “aha” (e.g. Germany-only Explore) |
| **Fields** | Proposed JSON paths on terminate payload / report / session |
| **Required?** | `required` · `optional` · `optional_when` (condition) · `recommended` |
| **Provider** | Who produces the value (see §2) — can be multi-step |
| **Data kind** | `raw` · `precomputed` · `both` (see §2) |
| **Motions** | Which Helios motions benefit (if applicable) |
| **Cardinality** | Safe for Analytics `GROUP BY`? (low / medium / high / avoid) |
| **Privacy** | PII / geo precision / retention notes |
| **Provenance** | confidence, source, prompt_version required? |
| **Priority** | `P0` · `P1` · `P2` · `P3` |
| **Depends on** | Other request IDs or Zeus features |
| **Acceptance** | How we know it’s done (lab SQL, UI filter, probe) |
| **Notes** | Risks, non-goals, open questions |

### Template (copy for new requests)

```markdown
### HEL-WISH-000 — Title

| Attribute | Value |
| --- | --- |
| **Business requirement** | … |
| **Insight sought** | … |
| **Example** | … |
| **Fields** | `path.a`, `path.b` |
| **Required?** | optional / optional_when: … / recommended / required |
| **Provider** | AI → Zeus Client → Zeus (pipeline) |
| **Data kind** | raw · precomputed · both |
| **Motions** | Explore, Compare, … |
| **Cardinality** | low / medium / high |
| **Privacy** | … |
| **Provenance** | confidence + source required: yes/no |
| **Priority** | P0 |
| **Depends on** | — |
| **Acceptance** | … |
| **Notes** | … |
```

---

## 2. Provider & data-kind glossary

### Providers (who fills the field)

| Provider | Role | Typical work |
| --- | --- | --- |
| **AI** | Model under `chat_request` guidance | Free-text facets, optional structured bags, intent wording |
| **Zeus Client (middle)** | App / SDK / BFF in front of Zeus | Client context: timezone, language, channel, coarse IP country, UI filters user picked |
| **Zeus** | Engine / report builder / post-process | Promote QD to report, tool_usage, status, geocode enrich, empty_reason, Analytics sink |

**Pipeline pattern (common):**

```text
User text
  → AI extracts free-text + optional structure (tier A/C)
  → Zeus Client may attach session/client context (middle)
  → Zeus validates, enriches (geocode), emits report → Analytics
```

Prefer **Zeus** when the truth is already in tool results or runtime. Prefer **Client** for browser-only facts Zeus never sees. Prefer **AI** only for meaning in the natural-language ask — always with provenance when structured.

### Data kind

| Kind | Meaning | Helios use |
| --- | --- | --- |
| **raw** | Per-turn (or per-session) fact on the document | Filter, facet, drill to `req_id` |
| **precomputed** | Aggregate / sum / rate Zeus (or a job) already rolled up | Fast dashboards, avoid heavy GROUP BY |
| **both** | Store raw on the turn **and** optional rollups elsewhere | Best of both; Helios usually starts on **raw** in Analytics |

**Default for this wishlist:** prefer **raw on the terminating turn** so Helios can compose any chart. Precomputed series are optional later (jobs / materialized views).

---

## 3. Request index

| ID | Title | Priority | Provider (primary) | Data | Motions (primary) |
| --- | --- | --- | --- | --- | --- |
| [HEL-WISH-001](#hel-wish-001--structured-place-geo_norm) | Structured place (`geo_norm`) | **P0** | AI → Zeus (geocode) | raw | Explore, Compare, Monitor, Route, Funnel |
| [HEL-WISH-002](#hel-wish-002--client--session-market-geo) | Client/session market geo | P1 | Zeus Client → Zeus | raw | Explore, Monitor, Funnel |
| [HEL-WISH-003](#hel-wish-003--outcome-quality-beyond-statusok) | Outcome quality bag | **P0** | Zeus | raw | Explore, Refine, Funnel, Verify |
| [HEL-WISH-004](#hel-wish-004--numeric-price_norm) | Numeric `price_norm` | **P1** | AI (+ optional Zeus parse) | raw | Explore, Refine, Compare, Funnel |
| [HEL-WISH-005](#hel-wish-005--intent_norm-stable-enum) | `intent_norm` stable enum | **P1** | AI (+ catalog guidance) | raw | Compare, Explore, Funnel |
| [HEL-WISH-006](#hel-wish-006--constraints--party) | Constraints & party size | P2 | AI | raw | Refine, Funnel, Compose |
| [HEL-WISH-007](#hel-wish-007--locale-language-timezone) | Locale / language / timezone | P2 | Zeus Client → Zeus | raw | Explore, Monitor |
| [HEL-WISH-008](#hel-wish-008--path--rail--evidence-counts) | Path / rail / evidence counts | P2 | Zeus | raw | Explain, Remember, Funnel |
| [HEL-WISH-009](#hel-wish-009--channel--tenant-safe-identity) | Channel & tenant-safe identity | P2 | Zeus Client + Zeus | raw | All (ops) |
| [HEL-WISH-010](#hel-wish-010--soft-ai-insights-jtbdsentiment) | Soft AI insights (JTBD / sentiment) | P3 | AI | raw | Explore insights, Triage |
| [HEL-WISH-011](#hel-wish-011--optional-precomputed-demand-rollups) | Optional precomputed demand rollups | P3 | Zeus / jobs | precomputed | Explore, Monitor |

---

## 4. Requests (detail)

### HEL-WISH-001 — Structured place (`geo_norm`)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Operators must segment “what people are thinking” by **place of interest in the ask** (country / region / city), not only free-text `geo` strings that never group cleanly. |
| **Insight sought** | *What are people thinking **in Germany only**?* · *Which intents cluster around Munich vs Berlin?* · map / radius heat later. |
| **Example** | Explore word cloud + 3D filtered to `country_iso = "DE"`; Compare local vs global fill rates. |
| **Fields** | Keep `qd.geo` (string). Add `qd.geo_norm.{country_iso, admin1, locality, lat, lon, radius_km?, confidence, source, place_id?, prompt_version?}`. Path: `report.query_decomposition.geo_norm.*` on Analytics. |
| **Required?** | **`optional_when`:** place is signaled in the user turn (or tools return a place). Never required on every turn. Free-text `geo` remains optional as today. |
| **Provider** | **AI:** extract place mention / free-text `geo` (and optional rough structure). **Zeus:** geocode / normalize to ISO + lat/lon (preferred over model inventing coordinates). **Zeus Client:** usually *not* for ask-geo (unless user picked a map pin — then client may send structured place). |
| **Data kind** | **raw** (per turn). Optional later: precomputed “demand by country_iso” (see HEL-WISH-011). |
| **Motions** | **Explore** (filter, map), **Compare** (rank by market), **Monitor** (spike by country), **Route** (regional handoff), **Funnel** (conversion by market). |
| **Cardinality** | `country_iso` **low**; `locality` **medium**; raw lat/lon **high** (use for filter/map, not GROUP BY buckets — prefer H3/grid if grouping). |
| **Privacy** | Ask-geo is about **content**, not home address. Still avoid over-precise coords without policy; country/admin1 often enough. |
| **Provenance** | **Yes** — `confidence`, `source` (`user_text` \| `geocode` \| `session` \| …), `prompt_version` when AI involved. |
| **Priority** | **P0** (country_iso); P1 for lat/lon. |
| **Depends on** | Geocoder keys / policy (Zeus or shared service). |
| **Acceptance** | Lab traces with `geo_norm.country_iso`; Helios SQL filter returns non-empty DE slice; Explore UI country filter (when built) uses ISO not string match. |
| **Notes** | Do **not** conflate with HEL-WISH-002 (user market / IP). Model should not be sole source of lat/lon. |

---

### HEL-WISH-002 — Client / session market geo

| Attribute | Value |
| --- | --- |
| **Business requirement** | Separate **where the user is** (market / network) from **what place they asked about**. |
| **Insight sought** | *Are DE users asking about US hotels?* · *Demand from mobile in FR vs content about FR.* |
| **Example** | Funnel conversion for sessions with `client.country_iso = "DE"` regardless of QD geo. |
| **Fields** | `session.client.country_iso` / `region` / coarse only; optional `source: ip|ui|crm`. **Not** nested under QD. |
| **Required?** | **optional** / **recommended** when client can supply without PII abuse. |
| **Provider** | **Zeus Client (middle)** primary (browser locale, optional geo consent, CRM). **Zeus** stores on session/report. **AI:** no. |
| **Data kind** | **raw** on session or turn envelope. |
| **Motions** | Explore (secondary filter), Funnel, Monitor, Route. |
| **Cardinality** | low (ISO). |
| **Privacy** | **High care** — IP geo is sensitive; prefer country only; document retention. |
| **Provenance** | `source` required. |
| **Priority** | P1. |
| **Depends on** | Client SDK / app contract. |
| **Acceptance** | Session docs show client country when enabled; Helios can filter without reading QD. |
| **Notes** | Explicitly labeled “user market” in Helios UI so operators don’t mix with ask-geo. |

---

### HEL-WISH-003 — Outcome quality beyond `status=ok`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Helios must distinguish **true empty**, **policy deny**, **error**, and **success with N results** — not only HTTP-ish `status=ok`. |
| **Insight sought** | *Real fill rate* · *Why did this miss?* · Refine queues that aren’t just “not ok”. |
| **Example** | Explore hits = `outcome.kind=ok` AND `user_visible_count > 0`; empty_reason histogram for Refine. |
| **Fields** | `report.outcome.{kind, empty_reason?, user_visible_count?, top_result_ids[]?, policy_codes[]?, reask?}`. Sibling of QD, not only inside it. |
| **Required?** | **`recommended` → required** on terminating turns once Zeus supports it. `kind` always; others when applicable. |
| **Provider** | **Zeus** primary (tool results, policy engine, UI return payload). **AI:** optional narrative only, not source of truth. **Client:** may send user thumbs later (satisfaction). |
| **Data kind** | **raw** per turn. Optional precomputed empty-rate by day (WISH-011). |
| **Motions** | **Explore**, **Refine**, **Funnel**, **Verify**, **Triage**. |
| **Cardinality** | `kind` / `empty_reason` **low** (closed enums). |
| **Privacy** | Avoid PII in empty_reason strings; use codes. |
| **Provenance** | Enum version / schema version nice-to-have. |
| **Priority** | **P0**. |
| **Depends on** | Zeus report builder changes. |
| **Acceptance** | Probe shows outcome bag; Helios miss definition can switch from `status!=ok` to outcome-based with documented migration. |
| **Notes** | Open product choice: empty with `status=ok` vs distinct status — Helios wants **explicit `outcome.kind`** either way. |

---

### HEL-WISH-004 — Numeric `price_norm`

| Attribute | Value |
| --- | --- |
| **Business requirement** | Price filters and bands on Explore/Refine must be **numeric**, not mock `$` UI over free-text `price`. |
| **Insight sought** | *Unmet demand under €100* · *Miss rate by price band* · Compare cheap vs premium language. |
| **Example** | Filter word cloud to `price_norm.max <= 100 AND currency = EUR`. |
| **Fields** | Keep `qd.price` string. Add `qd.price_norm.{min?, max?, currency, confidence, source, prompt_version?}`. |
| **Required?** | **`optional_when`:** user signals budget/price. |
| **Provider** | **AI** extracts numbers + currency from language. **Zeus** may normalize currency / validate. **Client** if user used a price slider (send structured). |
| **Data kind** | **raw**. |
| **Motions** | Explore, Refine, Compare, Funnel. |
| **Cardinality** | currency low; min/max continuous (bucket in Helios). |
| **Privacy** | Low. |
| **Provenance** | **Yes** (confidence). |
| **Priority** | **P1**. |
| **Depends on** | Catalog guidance for optional bag. |
| **Acceptance** | Traces with price_norm; Helios can drop mock-only price filters when coverage > threshold. |
| **Notes** | Never invent currency; if unknown leave null and keep free-text. |

---

### HEL-WISH-005 — `intent_norm` stable enum

| Attribute | Value |
| --- | --- |
| **Business requirement** | Stable charts across wording (“Find beers” vs “List me beer”) for ranking and funnels. |
| **Insight sought** | *Share of list vs best vs compare intents* · Compare leaderboards that don’t fragment on phrasing. |
| **Example** | GROUP BY `intent_norm` instead of raw `intent`. |
| **Fields** | `qd.intent` (free text, keep). `qd.intent_norm` enum e.g. `list` \| `best` \| `find` \| `count` \| `compare` \| `detect` \| `other`. |
| **Required?** | **recommended** when QD present; **optional** during rollout. |
| **Provider** | **AI** under catalog guidance (closed set). **Zeus** may map known synonyms post-hoc. **Client:** no. |
| **Data kind** | **raw**. |
| **Motions** | **Compare**, Explore, Funnel, Monitor. |
| **Cardinality** | **low** (closed enum). |
| **Privacy** | None. |
| **Provenance** | prompt_version / enum_version recommended. |
| **Priority** | **P1**. |
| **Depends on** | Catalog documents allowed enum (this repo). |
| **Acceptance** | ≥80% of non-synthetic QD has intent_norm in lab; Compare SQL groups cleanly. |
| **Notes** | Don’t replace free-text intent — dual write. |

---

### HEL-WISH-006 — Constraints & party size

| Attribute | Value |
| --- | --- |
| **Business requirement** | Refine needs **blocker types** (dates, party, network, radius), not only miss rate. |
| **Insight sought** | *Top blockers* · *Recovery when party_size relaxed*. |
| **Example** | Histogram of `constraints[].type` on empty outcomes. |
| **Fields** | `qd.constraints[]` as `{type, op, value, hard?}`. `qd.party_size` / `adults` / `children`. `qd.flexibility` optional. |
| **Required?** | **`optional_when`:** constraints signaled. |
| **Provider** | **AI** primary. **Client** if form UI collected structured filters. **Zeus** if tools return structured constraint failures. |
| **Data kind** | **raw**. |
| **Motions** | **Refine**, Funnel, Compose, Compare. |
| **Cardinality** | type low; value varies. |
| **Privacy** | Low–medium. |
| **Provenance** | confidence on AI-extracted constraints. |
| **Priority** | P2. |
| **Depends on** | HEL-WISH-003 for empty + constraint fail linkage. |
| **Acceptance** | Refine blocker chart prototype on lab data. |
| **Notes** | Prefer codes for `type` (`date_range`, `party`, `network`, …). |

---

### HEL-WISH-007 — Locale, language, timezone

| Attribute | Value |
| --- | --- |
| **Business requirement** | Demand language and peak hours by **locale**, not only server UTC `ts`. |
| **Insight sought** | *German-language asks* · *Local evening peaks*. |
| **Example** | Word cloud filtered `language=de`; Monitor by local hour. |
| **Fields** | `client.language` / `locale` (BCP-47), `client.tz` or `utc_offset`. Optional `qd.language` if ask language ≠ UI. |
| **Required?** | **recommended** from client when available. |
| **Provider** | **Zeus Client** primary. **Zeus** stores. **AI** optional for ask language ≠ UI. |
| **Data kind** | **raw**. |
| **Motions** | Explore, Monitor, Compare. |
| **Cardinality** | low–medium. |
| **Privacy** | Low. |
| **Provenance** | source: `accept_language` \| `app_setting` \| `ai`. |
| **Priority** | P2. |
| **Depends on** | Client SDK headers / payload. |
| **Acceptance** | Session/turn carries tz+language in lab client traffic. |
| **Notes** | — |

---

### HEL-WISH-008 — Path / rail / evidence counts

| Attribute | Value |
| --- | --- |
| **Business requirement** | Explain and Remember need **structured path facts**, not only `rounds_total` proxies. |
| **Insight sought** | *Coverage of answers with evidence refs* · *Which rail was used* · true branch count. |
| **Example** | Explain gauge from `evidence_ref_count`; Remember list by `rail_id`. |
| **Fields** | `report.path.{stage?, rail_id?, named_query?, branch_count?, evidence_ref_count?, missing_refs?}`. Keep `tool_usage[]`. |
| **Required?** | **optional** → **recommended** when rails/stages exist in product. |
| **Provider** | **Zeus** only (runtime truth). **AI:** no for counts. **Client:** no. |
| **Data kind** | **raw**. |
| **Motions** | **Explain**, **Remember**, Funnel, Explore (rails board). |
| **Cardinality** | rail_id medium; stages low. |
| **Privacy** | Low. |
| **Provenance** | N/A (engine). |
| **Priority** | P2. |
| **Depends on** | Named-query / stage product design. |
| **Acceptance** | Explain mock can switch to live tool/path histogram. |
| **Notes** | Prefer product stage events over AI-guessed stages. |

---

### HEL-WISH-009 — Channel & tenant-safe identity

| Attribute | Value |
| --- | --- |
| **Business requirement** | Multi-tenant / multi-channel ops without PII in Analytics. |
| **Insight sought** | *Web vs mobile demand* · *Per app_id volume*. |
| **Example** | Explore scope + `channel=mobile`. |
| **Fields** | `tenant_id` / `app_id`, `session.channel` (`web`\|`mobile`\|`voice`\|`slack`\|…), `actor_role` (`end_user`\|`agent`\|`system`). **No** raw email/name. |
| **Required?** | **recommended** for production multi-tenant. |
| **Provider** | **Zeus Client** (channel, app). **Zeus** (auth tenant, actor). **AI:** no. |
| **Data kind** | **raw**. |
| **Motions** | All (ops filters). |
| **Cardinality** | low–medium. |
| **Privacy** | **Critical** — no PII on Analytics path. |
| **Provenance** | N/A. |
| **Priority** | P2. |
| **Depends on** | Auth / tenancy model. |
| **Acceptance** | Helios can filter by channel without scope hacks. |
| **Notes** | — |

---

### HEL-WISH-010 — Soft AI insights (JTBD / sentiment)

| Attribute | Value |
| --- | --- |
| **Business requirement** | Optional narrative insight cards (“job to be done”, urgency) — **never** block core analytics. |
| **Insight sought** | Soft Explore insights · Triage urgency proxy. |
| **Example** | Insights card from `job_to_be_done` + demand. |
| **Fields** | `qd.job_to_be_done?`, `qd.sentiment?`, `qd.urgency?` + full AI metadata bag. |
| **Required?** | **optional** always. |
| **Provider** | **AI** only. **Zeus** stores if present. **Client:** no. |
| **Data kind** | **raw**. |
| **Motions** | Explore (insights placeholder), Triage. |
| **Cardinality** | high (free text) — don’t GROUP BY raw JTBD; use as display. |
| **Privacy** | May echo user language — treat carefully. |
| **Provenance** | **Mandatory** confidence + prompt_version. |
| **Priority** | P3. |
| **Depends on** | HEL-WISH-001/003 for real dashboards first. |
| **Acceptance** | Helios insights can show when confidence ≥ threshold; hidden otherwise. |
| **Notes** | Easy to poison charts — default exclude from demand GROUP BYs. |

---

### HEL-WISH-011 — Optional precomputed demand rollups

| Attribute | Value |
| --- | --- |
| **Business requirement** | Heavy dashboards / multi-tenant scale may need **pre-aggregated** series without scanning all turns. |
| **Insight sought** | Same as Explore boards, cheaper to serve. |
| **Example** | Daily `demand by country_iso × intent_norm` table. |
| **Fields** | Materialized Analytics collection or job output — **not** a substitute for raw turn fields. |
| **Required?** | **optional** (ops scale). |
| **Provider** | **Zeus** or **batch job** (not AI, not client). |
| **Data kind** | **precomputed** (aggregates/sums/rates). Source of truth remains **raw** turns. |
| **Motions** | Explore, Monitor, Compare (at scale). |
| **Cardinality** | controlled by rollup keys. |
| **Privacy** | Inherit raw policies; no re-identification. |
| **Provenance** | job version, window, generated_at. |
| **Priority** | P3. |
| **Depends on** | P0/P1 raw fields exist first. |
| **Acceptance** | Helios can read rollup **or** raw with same definitions. |
| **Notes** | Don’t start here — raw first (Explore lesson). |

---

## 5. Provider matrix (summary)

| Request | AI | Zeus Client | Zeus |
| --- | --- | --- | --- |
| 001 geo_norm | extract place / geo text | map pin (optional) | **geocode + promote** |
| 002 market geo | — | **primary** | store |
| 003 outcome | — | thumbs later | **primary** |
| 004 price_norm | **extract** | price slider | normalize |
| 005 intent_norm | **classify** | — | optional map |
| 006 constraints | **extract** | form filters | tool failures |
| 007 locale/tz | ask language optional | **primary** | store |
| 008 path/rail | — | — | **primary** |
| 009 channel/tenant | — | channel/app | tenant/actor |
| 010 JTBD/sentiment | **only** | — | store if present |
| 011 rollups | — | — | **jobs** |

---

## 6. Catalog impact (this repo)

| Change type | Requests | Action when accepted |
| --- | --- | --- |
| Guidance text | 001, 004, 005, 006, 010 | Document optional bags / enums in `guidance.query_decomposition` |
| Terminate schema | 001, 004, 005, 006 | Allow additionalProperties / explicit optional objects on QD |
| Min payload size | all C/A | Prefer short prompt notes; full shape in full profile or docs |
| Zeus-only (no catalog) | 002, 003, 007, 008, 009, 011 | Engine / client contracts — still track here for Helios alignment |
| BASE bump | when optional → normative | RELEASE_NOTES + COMPAT |

---

## 7. What Helios does without waiting

| Capability | Today’s fields (raw) |
| --- | --- |
| Demand language | `intent`, `entity`, `theme` |
| Cost / depth | `duration_ms`, `rounds_total`, tokens, tools, queries |
| Proxy quality | `status = ok` vs not |
| Rails | OK `intent×entity` frequency |
| Weak threads | high rounds / not ok / missing QD |

Structured **Requests** above make those insights **segmentable** (country, price band, true empty, channel).

---

## 8. How to add a new Request

1. Copy the template in §1.  
2. Assign next `HEL-WISH-0xx`.  
3. Fill **business requirement** and **insight sought** first (if you can’t, it’s not ready).  
4. Mark **Provider** and **Data kind** explicitly — never leave “someone”.  
5. List **Motions** or write `ops only`.  
6. Add row to §3 index + provider matrix §5.  
7. PR to `helios-beta` (then `main`).

---

## 9. Open questions (cross-cutting)

- Empty-result: `status=ok` + `outcome.kind=empty` vs distinct status?  
- Geocoder ownership and rate limits (Zeus vs shared service)?  
- Global `*_norm` conventions vs tenant-only extensions?  
- Min profile: document-only vs require bags when place/price signaled?  
- When do we promote a Request from wishlist → BASE-required?

---

## 10. Change log

| Date | Note |
| --- | --- |
| 2026-07-24 | Initial free-form wishlist (Explore live work). |
| 2026-07-24 | Canonical file on `helios-beta` as `HELIOS_WISHLIST_FOR_CHAT_REQUEST.md`. |
| 2026-07-24 | **Restructured as Requests** (business requirement, insight, fields, required?, provider AI/Client/Zeus, data kind raw/precomputed/both, motions, privacy, acceptance). |
