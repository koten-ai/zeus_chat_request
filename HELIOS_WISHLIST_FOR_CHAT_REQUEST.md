# Helios wishlist — chat_request / trace fields for better insights

**Canonical home:** this repo ([koten-ai/zeus_chat_request](https://github.com/koten-ai/zeus_chat_request)) — branch **`helios-beta`** (merge to `main` when ready)  
**Audience:** catalog / Workbench / Zeus emit owners · Helios motion designers  
**Consumer:** [Helios](https://github.com/koten-ai/Helios) Motions (Explore first, then Compare / Refine / …) via Couchbase Analytics on `` `zeus_sessions`.`session`.`traces` ``  

**Related in this repo:**

| Doc / path | Role |
| --- | --- |
| [CHAT_REQUEST.md](CHAT_REQUEST.md) | How catalogs work |
| [README.md](README.md) | Published V2 min catalogs |
| [`v2/min/`](v2/min/) · [`v2/base/`](v2/base/) | Live `chat_request*_v2_min.json` (terminate + `query_decomposition`) |
| [COMPAT.md](COMPAT.md) | Zeus version ↔ BASE |

**Related elsewhere:**

| Doc | Role |
| --- | --- |
| Helios `docs/analytics/QUERY_DECOMPOSITION.md` | What Helios groups on today |
| Helios `docs/motions/EXPLORE.md` §8 | Analytics → motions playbook |
| Zeus sessions Analytics | Persist path for turn reports |

This is a **wishlist**, not a committed catalog change. Prefer **additive optional** fields in guidance / report shape; keep core QD (`intent`, `entity`, …) stable for existing terminate contracts.

---

## 1. Why this list exists

Helios Explore already answers *“what are people thinking?”* from `query_decomposition` + cost rollups on Analytics. Operators immediately hit the next question:

> “OK — but **what are people thinking in Germany only?**”

Today optional `geo` is often free-text (`"Germany"`, `"DE"`, `"Berlin"`, `"near Munich"`) with **no lat/long**, no ISO country, no confidence. Same pattern for price, language, channel, outcome quality, etc.

Helios cannot invent trustworthy structure at query time over raw prose.  
**Emit once (Zeus runtime or AI extract under guidance) → store on the terminating turn → aggregate forever.**

That emit is taught and constrained by the **chat_request catalogs in this repo** (and Workbench customs that fork them). Hence the wishlist lives **here**, next to the real contracts.

---

## 2. Difficulty tiers

| Tier | Source | Cost / risk | Example |
| --- | --- | --- | --- |
| **Z — Zeus native** | Runtime already knows or can copy cheaply | Low — code emit on report | `scope`, `status`, `duration_ms`, `tool_usage`, model id, policy gate code |
| **C — Contract / guidance** | Teach model via `chat_request` / `guidance.query_decomposition` optional keys | Medium — prompt quality, catalog size | richer `geo`, structured `price`, `channel` |
| **A — AI extract** | Model derives facets not explicit in tools | Medium–high — wrong extractions poison dashboards | lat/long *guess* from place name, sentiment, “job to be done” |
| **G — Geo / external enrich** | Geocoder, IP, CRM join (post-model or sidecar) | Ops + privacy + keys | country ISO, admin1, coords from place string |
| **J — Join later** | Session/user/CRM/inventory ids | Identity + tenancy | account tier, SLA clock, inventory hit/miss |

**Rule of thumb:** Prefer **Z** over **A** when Zeus already has the truth (tool results, HTTP context, session config). Use **A** only with **confidence + provenance** so Helios can filter `confidence >= 0.8` or hide low-trust facets. Prefer **G** over pure model for lat/long.

**Where tier C lands in this repo:** optional keys under terminate `query_decomposition` / `guidance.query_decomposition` in `v2/**/chat_request*.json` (min + base). Full-profile guidance may document the richer shape; min may keep a shorter prompt and still require structured optional bags when present.

---

## 3. Worked example — “Germany only” in Helios Explore

| Need | Today | Wishlist |
| --- | --- | --- |
| User mental model | “People thinking about X **in Germany**” | Filter Explore / Compare by place |
| Free-text `geo` | `"Germany"`, `"DE"`, `"Berlin"` | Still useful for word clouds |
| Structured place | Missing | `geo_norm.country_iso = "DE"` |
| Map / radius | Missing | `geo_norm.lat`, `geo_norm.lon` (+ optional `radius_km`) |
| Ambiguity | “Frankfurt” (DE vs US) | `geo_norm.confidence`, `geo_norm.source` |

**Helios Analytics SQL once fields exist:**

```sql
-- Illustrative — not live until emit exists
FROM `zeus_sessions`.`session`.`traces` AS t
WHERE t.ts >= DATE_ADD_STR(NOW_STR(), -14, "day")
  AND t.report.query_decomposition.geo_norm.country_iso = "DE"
GROUP BY t.report.query_decomposition.intent AS intent,
         t.report.query_decomposition.entity AS entity
SELECT intent, entity, COUNT(*) AS demand
ORDER BY demand DESC
LIMIT 50;
```

**Motions unlocked:** Explore map layer · Compare “local vs global” · Monitor “spike in DE” · Route by region · Funnel conversion by market.

**Catalog angle:** guidance can require optional `geo` string always when place is signaled; Zeus post-process (G) fills `geo_norm` without blocking the user path.

---

## 4. Wishlist by category

Paths below use `qd.` = `report.query_decomposition` on the Analytics trace (or the terminate payload field that Zeus promotes there).

### 4.1 Place & geography (high value for Explore)

| Field (suggested path) | Tier | Why Helios wants it | Notes |
| --- | --- | --- | --- |
| `qd.geo` (string) | C | Demand language as spoken | Already optional in QD guidance; keep |
| `qd.geo_norm.country_iso` | A/G | Country filter (“Germany only”) | ISO-3166-1 alpha-2 |
| `qd.geo_norm.admin1` | A/G | State / Land / province | e.g. `BY` / Bavaria |
| `qd.geo_norm.locality` | A/G | City | Normalize spelling |
| `qd.geo_norm.lat` / `lon` | A/G | Maps, radius, “near me” analytics | WGS84; never invent precise coords without source |
| `qd.geo_norm.radius_km` | A/C | “Within 50 km of …” | Optional |
| `qd.geo_norm.confidence` | A | Trust filter on dashboards | 0–1 |
| `qd.geo_norm.source` | A/G | `user_text` \| `geocode` \| `ip` \| `session` \| `crm` | Provenance |
| `qd.geo_norm.place_id` | G | Stable join key | Google/Mapbox/etc. if licensed |
| Session `client.country` / IP geo | Z/G | Fallback when user never said a place | Privacy-sensitive; **separate** from ask geo |

**AI vs Zeus:** Place *mentioned in the question* → extract (A) then geocode (G). Place from browser / VPN → session context (Z/G). Do not mix “asked about Berlin” with “user sat in Berlin”.

---

### 4.2 Time & locale of the *ask* (not only server `ts`)

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `client.tz` / `utc_offset` | Z | Local hour-of-day demand | Browser / headers if available |
| `qd.time_ref` | A/C | “this weekend”, “next July” | Free text ok |
| `qd.time_norm.start` / `end` | A | Funnel / inventory windows | ISO-8601 |
| `qd.locale` / `language` | Z/C | Language split for word clouds | BCP-47 |
| `qd.currency` | C/A | Price comparability | ISO-4217 |

---

### 4.3 Money & constraints (Refine / Funnel / Compare)

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `qd.price` (string) | C | Demand language | Free text today |
| `qd.price_norm.min` / `max` / `currency` | A | Numeric bands, histograms | Helios `$` filters are mock without this |
| `qd.constraints[]` | C/A | `{type, op, value}` dates, party size, network | Refine blockers |
| `qd.party_size` / `adults` / `children` | A/C | Family vs solo | |
| `qd.flexibility` | A | Hard vs soft constraint | Recovery scoring |

---

### 4.4 Outcome quality (beyond `status=ok`)

Helios proxies **hits** = `report.status = "ok"`. Better insights need **why** and **user value**.

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `outcome.kind` | Z | `ok` \| `error` \| `empty` \| `policy_deny` \| `timeout` | Finer than status string |
| `outcome.empty_reason` | Z/A | no_hits, out_of_network, bad_params | Refine / Funnel drop-off |
| `outcome.user_visible_count` | Z | How many results shown | True fill rate |
| `outcome.top_result_ids[]` | Z | Join to inventory later | Cap length |
| `outcome.policy_codes[]` | Z | Verify / Route | Stable enums |
| `outcome.satisfaction` | A/J | thumbs, dwell, re-ask | Hard; optional later |
| `outcome.reask` | Z | same chat next turn reformulated | Refine recovery signal |

Prefer **sibling of QD** on the report (`report.outcome`), not nested only inside QD, so empty results still get a clean bag when QD is thin.

---

### 4.5 Path & tools (Explain / cost honesty)

Much already on the turn report; wishlist is **structure for SQL**.

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `tool_usage[]` | Z | Exists on report | Keep always populated |
| `path.stage` | Z | Funnel stage if product defines stages | Prefer product events over AI guess |
| `path.rail_id` / `named_query` | Z | Remember / Funnel rails | When path was a rail |
| `path.branch_count` | Z | True branches vs rounds proxy | If runtime knows |
| `path.evidence_ref_count` | Z | Explain coverage | Count of source refs |
| `path.missing_refs` | Z | Explain “should → 0” | boolean or count |

---

### 4.6 Identity & tenancy (safe aggregates)

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `scope` | Z | Exists | Keep path stable `bucket/scope` |
| `mode` / `source` | Z | Exists | Workbench vs app vs API |
| `tenant_id` / `app_id` | Z | Multi-tenant Helios | Low-cardinality |
| `actor_role` | Z | end_user \| agent \| system | Not PII |
| `session.channel` | Z/C | web, mobile, voice, slack | Compare channels |
| **Avoid raw PII** on Analytics path | — | GDPR / ops | Hash or omit email/name |

---

### 4.7 Intent semantics (Compare / Explore depth)

| Field | Tier | Why | Notes |
| --- | --- | --- | --- |
| `qd.intent` / `entity` / `theme` | C | Core terminate contract today | Keep free text; discover keys |
| `qd.intent_norm` | A/C | Closed enum for stable charts | e.g. `list` \| `best` \| `find` \| `count` \| `compare` |
| `qd.entity_type` | A/C | Hotel vs Account vs SKU class | Optional per-tenant registry |
| `qd.job_to_be_done` | A | Short phrase | Explore “insights” cards |
| `qd.sentiment` / `urgency` | A | Triage priority proxy | Low confidence common |
| `qd.parts[]` | C | Multi-ask turns | Already in guidance — **emit reliably** |
| `qd.synthetic` | Z | Exists when fallback | Always set when thin/harvest QD |

---

### 4.8 AI extraction metadata (required if tier A is used)

Any AI-derived object should carry:

```json
{
  "value": { },
  "confidence": 0.0,
  "model": "…",
  "prompt_version": "qd-geo-v3",
  "source_spans": ["user turn chars 12-40"],
  "extracted_at": "ISO-8601"
}
```

Helios default: **exclude** `confidence < threshold` or `synthetic` from “real demand” charts (same spirit as today’s synthetic QD filter).

---

## 5. Suggested storage shape (additive)

Prefer **structured bags next to classic free-text QD** so old terminate contracts and Helios SQL keep working:

```json
{
  "intent": "Find",
  "entity": "Beer",
  "theme": "craft",
  "geo": "near Munich",
  "geo_norm": {
    "country_iso": "DE",
    "admin1": "BY",
    "locality": "Munich",
    "lat": 48.137,
    "lon": 11.575,
    "confidence": 0.86,
    "source": "geocode",
    "prompt_version": "qd-geo-v1"
  },
  "price": "under 5 euro",
  "price_norm": {
    "min": null,
    "max": 5,
    "currency": "EUR",
    "confidence": 0.7,
    "source": "user_text"
  },
  "intent_norm": "find",
  "synthetic": false
}
```

Zeus-native outcome (sibling to QD on the report):

```json
"outcome": {
  "kind": "empty",
  "empty_reason": "no_hits",
  "user_visible_count": 0,
  "policy_codes": []
}
```

### Catalog implementation sketch (this repo)

1. **Guidance** — document optional `geo_norm` / `price_norm` / `intent_norm` in full-profile `guidance.query_decomposition` (and a short note in min system prompt if size allows).  
2. **Terminate schema** — allow additional properties (or explicit optional objects) on `query_decomposition` so validators don’t strip bags.  
3. **Zeus runtime** — promote QD + `outcome` onto Analytics report (existing QD path); optional geocode step fills `geo_norm` after model returns free-text `geo`.  
4. **Do not** require lat/long from the model on every turn — optional only when place is signaled.

---

## 6. Priority for Helios motions (what to build first)

| Priority | Fields | Unlocks |
| --- | --- | --- |
| **P0** | `outcome.kind` + `empty_reason` + `user_visible_count` (Z) | Honest hits/misses; Refine / Funnel |
| **P0** | `geo_norm.country_iso` (+ confidence) (A/G) | “Germany only” Explore / Compare |
| **P1** | `geo_norm.lat` / `lon` (G) | Map, radius, regional heat |
| **P1** | `price_norm.{min,max,currency}` (A) | Live price filters (replace mock $) |
| **P1** | `intent_norm` (C/A) | Stable Compare rankings across wording |
| **P2** | `constraints[]` (C/A) | Refine blocker histogram |
| **P2** | `path.rail_id` / stage (Z) | Remember + Funnel rails |
| **P2** | `client.tz` + `language` (Z) | Local peak hours, language clouds |
| **P3** | sentiment / JTBD / satisfaction (A/J) | Soft insights; high bar for trust |

---

## 7. What Helios will do *without* waiting

| Capability | Using only today’s fields |
| --- | --- |
| Demand language | `intent`, `entity`, `theme` word clouds |
| Cost / depth | `duration_ms`, `rounds_total`, tokens, tools, queries |
| Proxy quality | `status = ok` vs not |
| Rails | OK `intent×entity` frequency |
| Weak threads | high rounds / not ok / missing QD |

Wishlist items make those **segmentable** (by country, price band, true empty, channel) rather than global-only.

---

## 8. Implementation notes

### Catalog owners (this repo)

1. Keep **terminate must emit** `query_decomposition` with core `intent` + `entity` (current contract).  
2. Add **optional** structured bags in guidance; avoid exploding min payload size.  
3. Version guidance changes with BASE / release notes when shapes become normative.  
4. Customs (Workbench) may add tenant keys; prefer namespaced `other.*` or documented extensions over silent renames of core fields.

### Zeus runtime owners

1. **Emit on terminating turns** (same lifecycle as QD) so Analytics always sees a complete report.  
2. **Don’t block the user path** on geocoder failure — store free-text `geo` + optional `geo_norm` when enrich succeeds.  
3. **Version extractors** (`prompt_version`) so Helios can slice “before/after better geo”.  
4. **Cardinality:** ISO codes and enums for GROUP BY; keep display strings separate.  
5. **Privacy:** no raw IP, email, or precise home lat/long on long-lived Analytics without policy; country or H3 may be enough.  
6. Lab: extend Helios/Zeus Analytics probe when fields appear.

### Helios owners

1. Discover live keys; never hard-require wishlist fields before coverage exists.  
2. Filter synthetic / low-confidence from “real demand” charts.  
3. Document honest proxies until P0 outcome/geo land.

---

## 9. Open questions

- Is “place of interest in the ask” the same as “market of the user”? (Usually **no** — store both.)  
- Who owns geocoding keys and rate limits (Zeus vs offline enrich)?  
- Global `*_norm` conventions vs per-tenant QD extensions only?  
- Empty-result: `status=ok` + `outcome.kind=empty` vs distinct status? (Helios prefers **explicit outcome** either way.)  
- Min profile: document-only vs require optional bags when place/price signaled?

---

## 10. Change log

| Date | Note |
| --- | --- |
| 2026-07-24 | Initial wishlist from Helios Explore live work; **canonical file** moved to `zeus_chat_request` as `HELIOS_WISHLIST_FOR_CHAT_REQUEST.md` on branch `helios-beta` |
