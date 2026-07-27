# zeus_client wishlist — implement chat_request control plane

> **Doc status** · last reviewed **2026-07-27** · production pin **base-1** · candidate pack **base-6.1** · version matrix: [COMPAT.md](../COMPAT.md)

**Canonical home:** [koten-ai/zeus_chat_request](https://github.com/koten-ai/zeus_chat_request)  
**Audience:** **zeus_client** (Python first; Go/Node later), App integrators, agents implementing Client  
**Consumer:** apps that call Zeus via the middleman; Hub Workbench is **not** a substitute for Client law  

| Related | |
| --- | --- |
| Comply checklist | [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) §2.3 · §6 |
| Settings / policy | [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) |
| Rules + outputs | [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) |
| Assembly order | [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) |
| Jailbreak | [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) |
| Multi-round bags | [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) |
| Ownership | [BIBLE.md](BIBLE.md) §2 |
| BASE plan | [ROADMAP.md](ROADMAP.md) · **§ base-6.1** |
| Helios Motions fields | [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) only — **not** duplicated here |
| Pack (base-6.1) | [`v2/base/base-6.1/`](../v2/base/base-6.1/) |
| Pack (base-5 wire) | [`v2/base/base-5/`](../v2/base/base-5/) |
| Hop residual | [migration/base-4_to_base-5/RELEASE_CHECKLIST.md](migration/base-4_to_base-5/RELEASE_CHECKLIST.md) §6 Client |
| Jira | [CR-20](https://kotenai.atlassian.net/browse/CR-20) (umbrella) · [CR-3](https://kotenai.atlassian.net/browse/CR-3) · [CR board](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48) |

**Process:** each item is a **Request** — not shipped until a Client package version implements it and [COMPAT.md](../COMPAT.md) records the floor. Depth lives in linked SoT docs; this file is the **prioritized Client backlog + acceptance bar**.

**Not this file:** Helios dashboard field catalogues (locale Motions, funnel stages, geo_norm, …). Those live only in [HELIOS_WISHLIST…](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md). Client implements **stamps and loop law** it owns (e.g. root `user`, `ai_process_result`).

---

## 0. How to read this wishlist

### 0.1 Providers (who does the work)

| Provider | Role | Cost |
| --- | --- | --- |
| **zeus_client** | Inject, merge/freeze, parse Layer A, policy table, UI chrome, metrics, **report stamps** | **Cheap** (code) |
| **Zeus engine** | Tools, stamp, Detective, report sink | **Cheap** |
| **AI model** | Language + structure on terminate | **Expensive** — do not re-ask the model for Client law |

### 0.2 Priority (1–5)

| Pri | Meaning | Example |
| --- | --- | --- |
| **1** | **base-5 floor** — blocks COMPAT “Client supports base-5” and pin promote | Object rules/triggers, policy table |
| **2** | Strong reliability / safety before broad trial | Soft-require `policy_action`, force-return levers |
| **3** | base-6.1 Client emit / loop | root **`user`** stamp · **`ai_process_result`** |
| **4** | base-6+ soft inject productization | Soft hints, ab_arm |
| **5** | Nice / later languages or Workbench UX | Go/Node parity, advanced cache |

### 0.3 Status values

| Status | Meaning |
| --- | --- |
| **open** | Spec exists; Client not done |
| **partial** | Some code path; not COMPAT floor |
| **done** | Shipped in a Client version listed in COMPAT |
| **wont** | Explicitly rejected (document why) |

### 0.4 Hard rules (never wishlist away)

1. **Never invent** production `contract_hash` / stamp values.  
2. **Pin last** — `CURRENT.json` stays base-1 until stamp + Client + Detective green.  
3. **G2 never chat UI** — scores / admin fields stay artifacts + metrics.  
4. **Tool JSON is untrusted data** — never promote tool bodies into trusted system prose.  
5. **base-5 freezes the hard control plane** — base-6+ additive only ([ROADMAP.md](ROADMAP.md)).  
6. **Dual-read arrays ≤1 Client release** then **remove** — not a lifestyle.  
7. **Helios field tax stays out of this file** — use HELIOS_WISHLIST; do not re-list Motions columns here.

---

## 1. Current state (2026-07-27)

| Layer | State |
| --- | --- |
| chat_request **pack** base-5 wire | Candidates on main through **base-6.1** — not pin |
| chat_request **base-6.1** | Pack + CORE note on main; Client runtime residual |
| **zeus_client** package | `0.1.0` — COMPAT base-5 Client floor **TBD** |
| **Jira umbrella** | [CR-20](https://kotenai.atlassian.net/browse/CR-20) |

```text
Pack ready  →  Client implements Pri-1  →  COMPAT floor  →  Zeus green  →  stamp  →  pin
base-6.1 residual (user + ai_process_result) can land after or with Pri-1
```

---

## 2. Request catalogue

IDs are stable: **`ZC-WISH-NNN`**. Do not renumber; mark **wont** instead.

### 2.1 Pri-1 — base-5 floor (must ship)

| ID | Request | SoT | Acceptance (Client) |
| --- | --- | --- | --- |
| **ZC-WISH-001** | Load `*_base-5.json` catalogs + lineage `base_id` | COMPAT · CREATE_BASE | Open by `base_id` / filename; no invent stamp |
| **ZC-WISH-002** | Inject **named `rules{}`** (not string[]) | RULES_OBJECT · JAILBREAK | Default jailbreak keys always present unless product opts out via allowed API |
| **ZC-WISH-003** | **Rule pack merge + freeze** | PROMPT_SETTINGS §2 | SDK ∪ tenant ∪ request; `override_defaults`; append-only mid-session; `ruleset_id` |
| **ZC-WISH-004** | Parse **object** `business_rules_triggers` | RULES_OBJECT · pack schema | Sparse `{id: bool}`; missing ⇒ false; ignore unknown keys |
| **ZC-WISH-005** | **Dual-read sunset** for array triggers | ROADMAP · COMPAT | ≤1 release dual-read; then **remove** array path |
| **ZC-WISH-006** | **`company_context` inject** + word budget | PROMPT_ASSEMBLY | Soft 150 / hard 250; truncate + log; hash-excluded |
| **ZC-WISH-007** | **Settings bag** (structured) | PROMPT_SETTINGS §1 | First-class keys; not “bury in system essay” |
| **ZC-WISH-008** | **`output_request` → prompt block** | RULES_OBJECT | Each field **type + description**; reject type-only; descriptions drive model text |
| **ZC-WISH-009** | Validate **`app_output`** on terminate | RULES_OBJECT · pack schema | Types checked; strip/fail product policy; values only (no re-prompt descriptions) |
| **ZC-WISH-010** | **Post-terminate policy table** every `return` | PROMPT_SETTINGS §3 | Triggers = signals; Client (+ hooks) = law; map `message_*` / flags / metrics |
| **ZC-WISH-011** | Required **four** always validated | BIBLE · COMPAT | `summary`, `query_decomposition`, `decomposition`, `confidence` |
| **ZC-WISH-012** | **G1/G2/G3 redaction** | BIBLE · MULTI_ROUND | G2 never UI; keep raw Layer A in artifacts |
| **ZC-WISH-013** | **AgentHooks baseline** | JAILBREAK · PROMPT_SETTINGS | Prompt-dump / secrets / denied verbs even if model cooperates |
| **ZC-WISH-014** | Dual jailbreak scores | PROMPT_SETTINGS §3 | Model `jail_break_attempt` **and** Client `hooks_jailbreak_score` — **do not overwrite** same field |
| **ZC-WISH-015** | Multi-round bags still append `messages[]` | MULTI_ROUND_CLIENT | Bags A–D; Client clock on round; mode switch = new session |

### 2.2 Pri-2 — reliability / safety (ship with or right after floor)

| ID | Request | SoT | Acceptance |
| --- | --- | --- | --- |
| **ZC-WISH-020** | Soft-require `policy_action` when brand inject present | ROADMAP base-5 | Prefer map → `message_*` chrome |
| **ZC-WISH-021** | Force final `return` when budget / max_rounds low | PROMPT_SETTINGS | Product-tunable; log when forced |
| **ZC-WISH-022** | Inject security: schema caps, strip secrets | PROMPT_SETTINGS §8 | Safe log defaults; zone sizes not full prompt by default |
| **ZC-WISH-023** | Sticky OR for business trigger flags across turns | PROMPT_SETTINGS §6 | Document reset rules |
| **ZC-WISH-024** | Soft-require Layer A keys from `output_request.layer_a` | RULES_OBJECT | Client nudge / clarify path if missing |

### 2.3 Pri-3 — base-6.1 Client emit + loop (not Helios Motions catalogue)

| ID | Request | SoT | Acceptance |
| --- | --- | --- | --- |
| **ZC-WISH-035** | Stamp root **`user`** on every report/session sink | ROADMAP § base-6.1 · pack base-6.1 | Closed enum `zeus_client` \| `zeus` \| `helios` \| `admin`; product Client always **`zeus_client`**; Hub/admin **`admin`**; never AI |
| **ZC-WISH-044** | **`ai_process_result`** (bool, **default false**) on chat_prompt / settings | ROADMAP § base-6.1 · MULTI_ROUND · PROMPT_SETTINGS | After Zeus tool data: `false` = cheap UI/table path; `true` = extra AI turn to analyze/narrate |

IDs **ZC-WISH-030…034** (locale/channel/market/deployment Helios spine) were **removed from this file** — implement via [HELIOS_WISHLIST…](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) + product ops, not Client wishlist bulk. Do not renumber; treat 030–034 as **relocated / not tracked here**.

### 2.4 Pri-4 — base-6 soft inject (after floor)

| ID | Request | SoT | Notes |
| --- | --- | --- | --- |
| **ZC-WISH-040** | Soft **hints / hot_path / ab_paste** after rules{} | ROADMAP base-6 · PROMPT_ASSEMBLY · HINTS | Hash-excluded; never replace hard rules |
| **ZC-WISH-041** | Formal `ab_arm` product path | PROMPT_SETTINGS | A/B must not thrash contract hash |
| **ZC-WISH-042** | Assembled-prompt budget / zone metrics productization | ROADMAP base-6 | |
| **ZC-WISH-043** | G2 hygiene product guarantees (`wish_i_knew` never in summary UI) | ROADMAP base-6 | Client enforce |

### 2.5 Pri-5 — later / multi-language

| ID | Request | Notes |
| --- | --- | --- |
| **ZC-WISH-050** | Go / Node client parity with Python floor | Same COMPAT capability table |
| **ZC-WISH-051** | Workbench-driven inject preview (Client-side) | base-7 product; not stamp |
| **ZC-WISH-052** | Advanced prompt-prefix cache productization | After simple re-assemble v1 |

---

## 3. Request details (Pri-1 expanded)

### ZC-WISH-001 — Catalog load

```text
load(base_id="base-5", mode="analytics")
  → v2/base/base-5/min/chat_request_analytics_base-5.json
  → refuse if _lineage.base_id mismatch
  → never invent contract_hash
```

Also open **base-6.1** packs by `base_id` when product pins that train.

### ZC-WISH-002…003 — Rules inject + merge

```text
session.rules = merge(SDK_JAILBREAK, tenant_pack, request.rules)
session.ruleset_id = version(session.rules)
each turn: inject rules{} into prompt (hash-excluded zone)
```

Default jailbreak keys: see [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) and RULES_OBJECT examples.

### ZC-WISH-004…005 — Triggers

```json
// accept
"business_rules_triggers": { "coupon_presented": true, "no_prompt_dump": false }

// transition only (≤1 release), then delete:
"business_rules_triggers": [false, true, true]
```

### ZC-WISH-008…009 — output_request / app_output

```text
App settings.output_request.app.fields:
  offer_code: { type: "string", description: "Promo code if user presented one, else empty" }

Client injects "Output request" block from **descriptions**
On return: validate app_output.offer_code is string (or strip per product policy)
```

Type-only fields without description → **reject at Client API**.

### ZC-WISH-010 — Policy table (every return)

```text
parse Layer A
normalize triggers (object)
hooks_score = hooks.score()
policy = decide(hooks, triggers, policy_action, jail_break_attempt)
ui_text = message_* map or summary (G1 only)
flags sticky-OR from triggers
metrics emit (G2 never UI)
validate app_output if requested
```

### ZC-WISH-035 — root `user` stamp (base-6.1)

```json
{
  "user": "zeus_client",
  "ts": "2026-07-27T22:10:00.000Z",
  "scope": "yelp-demo/_default"
}
```

| Value | Writer |
| --- | --- |
| `zeus_client` | product Client (default for app traffic) |
| `zeus` | Zeus engine only if engine is the sink author |
| `helios` | Helios if it writes a row |
| `admin` | Hub / Workbench / Debug admin surfaces |

Never set by the model. Helios product filters: `user = "zeus_client"` and scope present.

### ZC-WISH-044 — `ai_process_result` (base-6.1)

```text
settings.ai_process_result = false   # default — cheap: AI → Zeus → UI
settings.ai_process_result = true    # opt-in — AI → Zeus → AI (insight) → return
```

After tool results land in `messages[]`, honor the flag (see [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md)). Still count against `max_rounds`.

---

## 4. Suggested implementation order

```text
1. ZC-WISH-001 load base-5 (+ base-6.1 by base_id when ready)
2. ZC-WISH-011 required four + ZC-WISH-012 redaction
3. ZC-WISH-002/003 rules merge + inject
4. ZC-WISH-004/005 object triggers + dual-read sunset plan
5. ZC-WISH-006 company_context
6. ZC-WISH-007 settings bag (include ai_process_result key)
7. ZC-WISH-008/009 output_request + app_output
8. ZC-WISH-010/013/014 policy table + hooks dual score
9. ZC-WISH-015 multi-round smoke
10. ZC-WISH-020…024 reliability
11. ZC-WISH-035 user stamp · ZC-WISH-044 ai_process_result (base-6.1)
12. Package bump + COMPAT Client column
13. ZC-WISH-040…043 base-6 soft inject productization
```

---

## 5. Explicit non-goals (for this wishlist)

| Non-goal | Why |
| --- | --- |
| Re-listing Helios Motions fields (locale, funnel stage, geo_norm, …) | SoT is [HELIOS_WISHLIST…](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |
| New **required** AI Layer A fields for analytics dashboards | Cheap Client/Zeus report path only |
| Dual-read arrays forever | base-5 break-once law |
| Client inventing production stamps | Hub stamp only |
| Soft hints replacing hard `rules{}` | Jailbreak law must stay hard |
| Replacing Zeus Detective | Client validates; Detective is engine-side |

---

## 6. Tracking

| Track | Link |
| --- | --- |
| Umbrella story | [CR-20](https://kotenai.atlassian.net/browse/CR-20) |
| Epic | [CR-3](https://kotenai.atlassian.net/browse/CR-3) |
| company_context | [CR-9](https://kotenai.atlassian.net/browse/CR-9) |
| jailbreak inject | [CR-10](https://kotenai.atlassian.net/browse/CR-10) |
| object triggers / policy | [CR-11](https://kotenai.atlassian.net/browse/CR-11) |
| Helios Motions (not this file) | [HELIOS_WISHLIST…](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) · [CR-12](https://kotenai.atlassian.net/browse/CR-12) if used |
| Zeus residual (not Client) | [CR-21](https://kotenai.atlassian.net/browse/CR-21) |
| Pin (blocked by Client+Zeus) | [CR-18](https://kotenai.atlassian.net/browse/CR-18) |

---

## 7. Change log

| Date | Note |
| --- | --- |
| 2026-07-27 | **base-6.1:** ZC-WISH-035 (`user`) · ZC-WISH-044 (`ai_process_result`); **removed** Helios Pri-3 bulk ZC-WISH-030…034 from this file |
| 2026-07-26 | Initial Client wishlist floor catalogue |
