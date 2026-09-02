# BASE + Helios roadmap

> **Doc status** · last reviewed **2026-07-28** · production pin **base-1** · **candidate line base-6.2** (`v2/base/base-6.2/` · [CR-34](https://kotenai.atlassian.net/browse/CR-34)) · prior **base-6.1** · last wire break **base-5** · Zeus 0.6 vendor **base-5.3** · next **Client residual (ZC-WISH-035/044/040)** · multi-turn reuse in **BEST_PRACTICES / OPTIMIZATION** · version matrix: [COMPAT.md](../COMPAT.md)


**Status:** living plan after base-1 → base-4 → **base-5 wire freeze** → **5.1 / 5.2 / 5.3 content** (5.3 pack on main)  
**Normative (base-4 era docs, base-5 wire freeze):** [BIBLE.md](BIBLE.md) · **Lessons:** [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) · [migration/base-4_to_base-5/lessons-learned.md](migration/base-4_to_base-5/lessons-learned.md) · [migration/base-5_to_base-5.2/lessons-learned.md](migration/base-5_to_base-5.2/lessons-learned.md) · [migration/base-5.2_to_base-5.3/lessons-learned.md](migration/base-5.2_to_base-5.3/lessons-learned.md)  
**Helios requests (analytics emits):** [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)  
**zeus_client backlog (implement floor):** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) (`ZC-WISH-*`)  
**base-5 inject / Layer A deltas:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) — **rules + triggers as objects**; Client **`output_request` → `app_output`** (each app field = **`type` + `description`**; type-only is not enough)  
**base-5 control plane:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) — **settings bag** · **rule pack merge/freeze** · **Client policy table** · cache zones · security · observability  
**Latency / skinny plan:** **§ Getting skinny** below — contract-safe tools[] · Hot Path empirics · stamped A/B · schema diet · measure AI floor · **end-of-6.x prefix diet → § base-6.2 / [CR-34](https://kotenai.atlassian.net/browse/CR-34)**  
**World-model language for packs:** **§ World model language for chat_request** — DESIGN vocabulary (AI-Ready overlay · mini-schema shape · access class · modes) · not form-fill  
**Verb catalog clarity:** **§ Verb catalog clarity** — base-5.2 13-API review vs Zeus `docs/API/V2/*.md` · description/schema gaps · P0 fixes  
**Retrieval playbook:** [BEST_PRACTICES.md](BEST_PRACTICES.md) — single-focus recipes + multi-intent + **multi-turn short law** (§1.3 Option B); open ≠ multi-ask  
**Soft HINTS (base-6):** [HINTS.md](HINTS.md) · **§ HINTS catalog** below + **§ base-6** — hash-excluded `hints.*` after `rules{}`  
**base-6.2 skinny prefix:** **§ base-6.2** · **[CR-34](https://kotenai.atlassian.net/browse/CR-34)** — system + `return`/`pipeline` diet · full 13 verbs · no wire break  
**End-goal optimization:** [OPTIMIZATION.md](OPTIMIZATION.md) — Pachinko funnel · Hot Path mine · **multi-turn CORE (Option A)** · **`named_query` rails** · Helios Funnel · **[ZE-267](https://kotenai.atlassian.net/browse/ZE-267)**  
**WIP pickable strategies:** [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) — `thorough` / `fast_pass` / `scout` (`OPT:36` reserved). Not a pack change. Not CORE.  

**Best practices vs optimization (pipeline) — designed stages + citation IDs:**

```text
STAGE DAY-ONE   BEST_PRACTICES.md   cite BP:N     spit tests · gold · every new scope
STAGE TRAFFIC   OPTIMIZATION.md     cite OPT:N    hundreds→10k · Hot Path · rails
Per-turn soft   hints.*             ZC-WISH-040   never hard law alone
Think-budget    OPTIMIZATION_STRATEGIES.md  WIP   thorough | fast_pass | scout (not mode)
```

Prompt Helper / stamps: e.g. `guidance.playbook_refs: ["BP:4","BP:5A"]` · `optimization_refs: ["OPT:4","OPT:29"]`.  
Verbose traffic cards **OPT:29+** (multi-turn recipe, dual-bag, virtual types, stubs) — load by fingerprint only.  
Indexes live at the top of each doc (**Citation index**).
**Ownership (set/unset/change):** [BIBLE.md §2](BIBLE.md)  
**Production pin:** still **base-1** (`CURRENT.json` / `v2/min`) until an explicit promote  
**Agent procedure:** [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) · hop [migration/base-4_to_base-5/](migration/base-4_to_base-5/)  
**Jira board:** [CR board 48](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48) · tracking table **§ CR board map** below

This is **what we want next and why**, not a commitment calendar.  
**Exception to “small bumps”:** **base-5 is intentionally the big wire/control-plane break** while nothing is in production on this line — then **base-5.x content / skinny** and **base-6+ additive/optional**.

---

## North star

```text
1. Model reliably emits complete Layer A (required + useful recommended)
2. Client multi-round state without prompt explosion
3. Humans/AIs can diet a BASE in text, re-encode JSON, Diff in one inspector
4. Helios gets typed, queryable scalars — prefer Zeus/Client over AI emit tax
5. Production pin only when stamp + Client + Detective are green
6. Clear control plane: settings ≠ prompt essays; triggers = signals; Client policy = law
7. Named rules + merge/freeze so multi-tenant packs stay auditable
8. Break once in base-5; additive/optional forever after (until a new major is justified)
9. Skinny path: full 13-verb platform stays; fewer tools only via stamped packs/A/B from Hot Path empirics
10. Measure AI floor honestly — catalog/control-plane trains ≠ automatic wall-ms wins; never unhash tools[] mid-chat
11. Chat_request teaches **world model + verbs** (DESIGN: AI-Ready overlay · mini-schema shape · access class) — not form-fill / slot extraction over raw tables
12. Each of the 13 tools teaches **when / when-not / KEY constraint** (aligned to Zeus V2 API docs) — not cost-tags alone
13. **Playbook** (recipes A–H + multi-intent + multi-turn short law) is policy of use; **hints.*** are per-turn soft bias — never replace hard rules or inject schema
14. Modes optimize **join/noise/hop appetite**; multi-paragraph multi-ask is **not** “switch to open”
15. End-goal: shape the board with **named_query rails** (PREPARED fast-pass) from mined hot paths — **shape the funnel, don’t shrink the box** ([OPTIMIZATION.md](OPTIMIZATION.md))
16. **Multi-turn:** prefer reusing prior Zeus tool evidence when the user points at it; sharpen under traffic (OPTIMIZATION Option A) — do not unconstrained-rediscover “those / listed” sets
17. **Emit provenance `user` + `ip_address`:** every Analytics / session back-and-forth root stamps **who wrote the row** (`zeus_client`|`zeus`|`helios`|`admin`) and optional **caller IP** (IPv4 or IPv6 string) so Helios can filter product traffic (`user="zeus_client"`) vs Hub/admin noise — **§ Emit `user` + `ip_address` + `ai_process_result`**
18. **Optional AI insight turn:** Client setting **`ai_process_result`** (default **false**) — after Zeus tool data lands, either surface rows cheaply (one AI plan + tools) **or** spend another AI round to analyze/talk about the data — **not** a Layer A tax
19. **End base-6.x with a skinny catalog prefix:** same wire + full 13 verbs; diet **system + tool schemas** so hashed prefix is not triple-taught Layer A essays — **§ base-6.2** · **[CR-34](https://kotenai.atlassian.net/browse/CR-34)** · placement: [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md)
```

---

## base-6.1 — `user` + `ip_address` emit + `ai_process_result` (Client loop)

**Jira residual:** Client **ZC-WISH-035 / 044** · Helios **HEL-WISH-022** (filters only)  
**Pack:** [`v2/base/base-6.1/`](../v2/base/base-6.1/) · parent **base-6** · hop [migration/base-6_to_base-6.1/](migration/base-6_to_base-6.1/)  
**Status:** **candidate pack on main** · **not** a base-5 wire break · Client runtime residual  
**SoT backlog:** [ZEUS_CLIENT_WISHLIST…](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) · multi-round [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) · settings [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · Helios filter [HEL-WISH-022](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)

### Emit `user` + `ip_address` + `ai_process_result`

### Why (lab example)

Hub AI Chat can already: **one model plan → one Zeus `pipeline` → rows in UI** (“Zeus results (25)”) with tokens on a single AI call. That is the **cheap default**.

Operators / products sometimes want a **second AI turn** that reads tool JSON and writes a human insight (“what to do in Tampa…”) without making every product path pay that cost.

Helios Motions over `` `zeus_sessions`.`session`.`traces` `` also need a **stable slice**: product Client traffic vs Hub admin vs engine-only — without parsing free-text “I called Zeus.” Companion **`ip_address`** (when known) supports abuse / geo / “who hit us” without a second AI tax.

### 1) Root fields `user` + `ip_address` (emit provenance)

Stamp on the **root of the session / turn / back-and-forth payload** that lands in Analytics (and any parallel report envelope). **Closed enum for `user` — do not invent codes. `ip_address` is a network address string only.**

| `user` | Writer | Typical surface |
| --- | --- | --- |
| **`zeus_client`** | **zeus_client** (middleman / product SDK) | Apps, product chat |
| **`zeus`** | **Zeus engine** (if engine sinks a row without Client) | Internal/engine paths |
| **`helios`** | **Helios** (if Helios writes/annotates a row) | Motions / ops enrich (rare) |
| **`admin`** | **admin / Hub** | Workbench, Debug AI Chat, admin tools |

| Field | Type | Rule |
| --- | --- | --- |
| **`user`** | closed enum above | Required-recommended on new sinks |
| **`ip_address`** | **string** — **IPv4 or IPv6** textual form (e.g. `203.0.113.42`, `2001:db8::1`) | Optional when known; omit / empty when unknown; never invent; product may redact per privacy policy |

```json
{
  "user": "zeus_client",
  "ip_address": "203.0.113.42",
  "ts": "2026-07-27T22:10:00.000Z",
  "scope": "yelp-demo/_default",
  "session_id": "…",
  "turn": { }
}
```

**Helios query shape (example):**

```sql
-- Product client traffic for "today", with a real scope
SELECT META().id, t.*
FROM `zeus_sessions`.`session`.`traces` t
WHERE t.`ts` >= /* start of today UTC or tenant tz */
  AND t.`ts` <  /* start of tomorrow */
  AND t.`scope` IS NOT MISSING
  AND t.`scope` != ""
  AND t.`user` = "zeus_client"
```

| Rule | |
| --- | --- |
| **Who sets them** | The **component that owns the write** to Analytics/report — Client stamps **`zeus_client`** + caller **`ip_address`** (when available) on product sinks; Hub/admin surfaces stamp **`admin`**; only stamp **`zeus`** if Zeus itself is the sink author |
| **Never AI** | Model must not invent `user` or `ip_address` |
| **Missing `user`** | Treat as **unknown / legacy** — Helios dashboards that care about product purity **filter `user = "zeus_client"`** (missing ≠ product) |
| **Missing `ip_address`** | OK (server-to-server, privacy redact, no remote addr) — do not invent |
| **Not Layer A** | Scalars on report/session root — cheap |

### 2) Client setting `ai_process_result` (optional insight turn)

**Name (chat_prompt / settings bag):** `ai_process_result`  
**Type:** boolean · **Default: `false`**

| Value | Client loop after Zeus tool result(s) |
| --- | --- |
| **`false` (default)** | Prefer **cheap path**: may surface structured tool data to UI (tables, graph, Zeus-results lightbox) and terminate with a thin summary / Layer A from what is already known — **no extra AI round required** for “show me the rows.” Matches the lab pattern: one plan + one Zeus pipeline. |
| **`true`** | After tool results are appended to `messages[]`, Client **schedules another AI turn** so the model can **analyze / narrate / recommend** from Zeus evidence (second hop of tokens + latency). Product opt-in for “AI insight on the data.” |

```text
ai_process_result = false (default, cheap):
  user → AI (tool_calls) → Zeus → UI/table (+ optional minimal return)
  # one AI call is enough when the product is "show data"

ai_process_result = true (insight):
  user → AI (tool_calls) → Zeus → AI (read tool JSON) → return/summary
  # second AI turn is intentional and billable
```

| Rule | |
| --- | --- |
| **Owner** | App / Client **settings** ([PROMPT_SETTINGS.md](PROMPT_SETTINGS.md)) — **S C**; not hashed catalog body |
| **Default** | **`false`** — never surprise operators with double AI cost |
| **Caps** | Still honor `max_rounds` / force-return; insight turn counts as a round |
| **Payload size** | Client may **prune** huge tool bodies before insight turn (bag D keeps rich copy for UI) |
| **Hub default** | Product Client default **false**; Hub Debug may default **true** for operator storytelling (document in COMPAT when implemented) |

### 3) BASE / ownership fit

| Piece | BASE / package | Breaking wire? |
| --- | --- | --- |
| `user` on report/session root | **Client + Zeus emit** (COMPAT when live) | **No** — additive scalar |
| `ip_address` on report/session root | **Client + Zeus emit** (IPv4/IPv6 string when known) | **No** — additive scalar |
| `ai_process_result` | **Client settings** (Pri-4 / base-6 era product) | **No** — loop policy |
| Catalog prose | Optional one-liner: “when product asks for insight, Client may call you again with tool results” | Content only |

### 4) Open questions (resolve before COMPAT floor)

1. When Hub **admin** chat uses a **product-shaped** catalog pin, is `user` always **`admin`** (surface) or **`zeus_client`** if a real Client session is under the hood? **Proposal:** stamp by **surface** (`admin` for Hub/Workbench/Debug).  
2. Does Zeus ever write Analytics rows **without** Client? If yes, engine must stamp **`zeus`**; if no, drop `zeus` from Helios filters.  
3. `ai_process_result=true` + `max_rounds=1` — refuse config or force `max_rounds ≥ 2`? **Proposal:** Client raises floor to 2 when insight is on, or logs and clamps.  
4. Should insight turn be **blocked** when tool status ≠ ok / empty rows (avoid paying for “I found nothing” essays)? **Proposal:** product policy flag later; default still call AI if true.  
5. Exact Analytics path for `user` (`session.user` vs per-turn `turn.user`) — **Proposal:** both session default + per-turn override if multi-writer sessions appear.

### Success signals (base-6.1)

- [x] Spec in ROADMAP + wishlists (**this section**)  
- [x] Pack `v2/base/base-6.1/` + hop + CORE note  
- [x] `verify_base_pack.py --base 6.1` OK  
- [x] COMPAT candidate row · RELEASE_NOTES  
- [x] Client wishlist stripped of Helios Pri-3 bulk; ZC-035/044 kept  
- [x] Pack `report_sink_schema.json` + `report_sink_example.json` (stamps **not** on Layer A)  
- [x] Pack `settings_ai_process_result.example.json`  
- [ ] Client stamps `user` (+ `ip_address` when known) on every report sink (ZC-WISH-035)  
- [ ] Helios Motions filter `user = "zeus_client"` + scope + day (HEL-WISH-022)  
- [ ] Client implements `ai_process_result` default false (ZC-WISH-044)  
- [ ] Hub documents Debug default if different from product  
- [ ] No new **required** Layer A fields for either feature  

### Sequencing

```text
base-6 (hints pack) ──► base-6.1 (user + ai_process_result pack + docs)
        │                      │
        │                      ├── Client ZC-WISH-035 / 044
        │                      ├── Helios HEL-WISH-022 filters only
        │                      └── base-6.2 skinny prefix (CR-34) — content diet, full-13
base-5 Client floor (CR-20) remains orthogonal floor
ZC-WISH-040 hints inject remains orthogonal soft steer
```

---

## base-6.2 — skinny chat_prompt (system + tools diet; full-13)

**Jira:** **[CR-34](https://kotenai.atlassian.net/browse/CR-34)** · parent epic **[CR-4](https://kotenai.atlassian.net/browse/CR-4)**  
**Pack:** [`v2/base/base-6.2/`](../v2/base/base-6.2/) · parent **base-6.1** · hop [migration/base-6.1_to_base-6.2/](migration/base-6.1_to_base-6.2/)  
**Status:** **candidate pack** · **not** a wire break · **not** production pin  
**Related:** § Getting skinny · [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) · prior diet **CR-26** (base-5.3) · A/B **ZE-285** · verb-membership later **ZE-267** · vendor 6.1 first **ZE-286**

**Theme:** End-of-**base-6.x** **content skinny** — reduce hashed **catalog prefix** (system + 13 verb schemas). Full 13 verbs stay. No Layer A rename. No mid-session tools[] strip.

### Catalog prefix (what we dieted)

```text
Catalog prefix   =  system message  +  verbs[]/tools[] schemas  (hashed when stamped)
Not in budget    =  BRIEF · MINI-SCHEMA · company_context · rules{} · hints.* · history
```

### Measured result (analytics min, 2026-07-28)

Method: chars÷4 ≈ tokens. Scope = system + `verbs[]` only.

| Pack | System ~tok | Tools ~tok | **Prefix ~tok** | Δ vs 6.1 |
| --- | --- | --- | --- | --- |
| base-6.1 | ~2,450 | ~3,960 | **~6,410** | — |
| **base-6.2** | **~1,420** | **~3,400** | **~4,820** | **−25% (~−1.6k/turn)** |

Ship band was conservative ~5.15k / moderate ~4.5k — landed **between** (system beat moderate; tools still have headroom for later A/B).

### What changed

| Area | Change |
| --- | --- |
| CORE | Compressed world-model, efficiency, Terminate; Client stamp enum **out**; one-line hints + insight |
| Mode overlays | analytics example pipeline shortened (others already short) |
| `return` | Shorter property descriptions; keep types/enums/required four |
| `pipeline` | Terminating Layer A props **thin-ref** return (no deep `wish_i_knew`/`data_gaps` trees) |
| Wire | Unchanged — objects, required four, dual gaps, 13 verbs |

### Placement law (while dieting)

```text
Model prompt  =  retrieve + terminate FROM EVIDENCE
Client docs   =  user/ip stamps, ai_process_result loop (report_sink / settings)
hints.*       =  per-turn soft bias — never sole home of jailbreak/contract law
SCHEMA        =  types/enums + KEY one-liners — not essays duplicated from CORE
```

### Success signals

- [x] Spec + ticket **CR-34**  
- [x] Pack `v2/base/base-6.2/` + hop  
- [x] `verify_base_pack.py --base 6.2` OK  
- [x] `diff_modes.py --fail-if-clone` OK  
- [x] Prefix ≥20% smaller vs base-6.1 analytics min  
- [x] Required four + `order.asc` + no-rediscovery + progressive-empty one-liner still explicit  
- [x] COMPAT/RELEASE_NOTES on this PR  
- [ ] A/B or books: 6.1 vs 6.2 quality_pass ≥ baseline (**ZE-285**)  
- [ ] Optional Zeus vendor after books green  


### Sequencing

```text
base-6.1 pack (CR-27) ──► base-6.2 skinny pack (CR-34) ──► base-7 product (CR-5)
        │                              │
        ├── Client CR-28/29/30 / CR-33   (orthogonal residual)
        ├── CR-32 progressive-empty assemble (keep law in CORE)
        ├── ZE-286 vendor 6.1 when CR-27 green
        └── ZE-267 verb-drop A/B remains later (not default 6.2 stamp)
```

---

## BASE change law (post base-4)

No production traffic on the **base-4/5 line** yet. Use that:

| BASE | Allowed change type | Examples |
| --- | --- | --- |
| **base-5** | **BREAKING OK** — freeze the contract | Object rules/triggers · settings bag · policy table · `output_request` · company+jailbreak in prompt |
| **base-5.1** | **Content patch on base-5 wire** — **not** a new wire break | Restore **mode overlays** in system prompt (`messages[].content`); core+overlay; no Layer A rename |
| **base-5.2** | **Additive G2 design on base-5 wire** | Keep classic **`wish_i_knew`** + append **`data_gaps`** for Helios acquisition ([WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md)) |
| **base-5.3** | **Content skinny train on base-5 wire** — **not** a wire break | Prose no-rediscovery · **verb clarity** (desc + params vs V2 API) · schema diet · **usage-driven** skinny packs (stamped A/B) · world-model CORE blurb · **no** runtime strip of hashed verbs · **no** Layer A rename |
| **base-6** | **ADDITIVE** soft inject | Soft **`hints.*`** after hard `rules{}` ([HINTS.md](HINTS.md)) |
| **base-6.1** | **ADDITIVE** Client-loop / emit train on base-6 | Root **`user`** enum · **`ip_address`** (IPv4/IPv6) · **`ai_process_result`** (default false) — **§ base-6.1** |
| **base-6.2** | **Content skinny** on base-6.1 wire — **not** a wire break | Diet system + `return`/`pipeline` · full 13 verbs · ~**−25%** catalog prefix — **§ base-6.2** · **[CR-34](https://kotenai.atlassian.net/browse/CR-34)** |
| **base-6.3+** | **ADDITIVE / OPTIONAL only** | Further soft inject productization · Workbench UX · pin when green |
| **Helios wishlist** | **Nice-to-have** (cheap provider first) | Pri-1 report scalars in [HELIOS_WISHLIST…](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) — **not** Client wishlist bulk |

```text
base-5    = last wire/control-plane break before real adoption of this line
            Prefer one clean object contract over dual-read forever.

base-5.1  = content/diet train ON the base-5 wire (mode personas in prompts)
            Same schema objects / required four / app_output — packs stop being
            “analytics × rename”. See docs/MODE.md · work/RECREATE_MODE.md

base-5.2  = additive G2: classic wish_i_knew (ops) + data_gaps (Helios acquisition)
            Optional fields only; not a wire break of required four. See WISH_I_KNEW_DUAL.md

base-5.3  = SKINNY + WORLD-MODEL + VERB CLARITY on the base-5 wire
            Platform keeps 13 verbs; production wire = stamped contract verbs[]
            (do NOT strip tools mid-session when enforcement is on).
            Diet via prose + schema bytes + empirics → new stamped packs / A/B.
            Plus short DESIGN-aligned worldview in CORE + rewrite tool
            descriptions/params so they teach use (aligned to docs/API/V2).
            See § Getting skinny · § World model language · § Verb catalog clarity.

base-6+   = additive / optional_when / hash-excluded soft injects / productization
            hints.* after rules{} (path/recipe, hot_path, multipart, ab_paste, …)
            No rename/remove of base-5 wire keys without a new major BASE + migration hop.
            See § HINTS catalog · [BEST_PRACTICES.md](BEST_PRACTICES.md).

base-6.2  = SKINNY PREFIX (system + verb schemas) on full-13 stamp
            Collapse triple-teach Terminate × return × pipeline; Client stamp
            law out of CORE; no verb drop; no wire break. See § base-6.2 · CR-34.

Helios    = analytics spine on Zeus/Client; optional_when if AI ever needed
            Never block pin on Pri-2/3/4/5 AI fields
```

**Naming note (normative):** train id **= pack folder = `_lineage.base_id`**.  
Examples: `v2/base/base-5/`, `v2/base/base-5.1/`, `v2/base/base-5.2/`.  
**Never** apply a train only via `content_train` on a parent pack — that blocks pull-by-path and simple JSON Diff.  
BASE ids are **not** Zeus or zeus_client semver.

**Dual-read** of base-4 `rules[]` / `boolean[]` triggers: **≤ one Client release** while migrating, then **drop**. base-5 catalogs and docs are **object-only**. Prefer **zero** dual-read if no external consumers.

---

## Cost law (Helios-aligned — every BASE)

From [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) §0:

| Provider | Cost | Role |
| --- | --- | --- |
| **AI / Layer A** | Expensive | Meaning only the model knows |
| **Zeus Client** | Cheap | tz, language, channel, market, deployment |
| **Zeus** | Cheap | tools, outcome, path, precomputed counts/sums |

**Rules:** Prefer cheap providers · AI only for meaning in the ask · piggyback before expand · `optional_when` over always-on · JSON numbers as numbers · sparse AI is normal · exception flags **true-only**.

Helios Motions read Analytics over **scalars** first; nested arrays are for drill-down.

---

## Latency law (chat wall time — every BASE + Client)

Detective-shaped truth (beer-sample / base-5.2 example, 2026-07-26):

| Slice | Typical share on a healthy 1-round turn |
| --- | --- |
| **`ai.chat.round.N` (LLM)** | **~95–99%** of wall |
| Zeus tool / pipeline execution | often **&lt;1–5%** when path is correct |
| Dispatch / inject / encode | noise unless broken |

**Implications:**

1. **base-5 / 5.1 / 5.2 were not latency trains.** They grew catalog quality (modes, dual gaps, control plane). System + verbs JSON on disk **increased** base-1 → base-5.2 — do not expect wall-ms to drop from pin alone.
2. **Structural wins** = fewer rounds + no rediscovery (`describe` / `get_stats` when inject is green) + one terminating `pipeline`. Measure **rounds**, `tool_calls_total`, **per-verb use rates**, and rediscovery rate — not only wall ms on already-1-round chats.
3. **Token wins** = shorter verb schemas (especially `return` / `pipeline`), smaller **completion**, stable prefix + prompt cache for multi-turn, and — only via a **new stamped pack/custom** — fewer tools in the hashed catalog.  
4. **Model floor** remains real: ~3s for one rich tool call on a “fast” model can still be `speed_grade=pass`. Skinny cannot invent a sub-second LLM if generation stays ~1k completion tokens.
5. **Fix inject before teaching discovery.** If `describe()` “because mini-schema wasn’t sent,” that is a **Client/Zeus inject** bug or a **missing inject** path — fix inject reliability; do **not** silently mutate the hashed tools list mid-chat.
6. **Contract enforcement law:** `verbs[]` participate in **`contract_hash`**. When enforcement is on, **do not strip tools from the wire at runtime** (e.g. “mini-schema present ⇒ drop `describe`”) — Zeus/Client will refuse or fail the turn as a contract mismatch. Skinny verb sets are **new stamps / A/B packs**, not per-turn list surgery.

Full plan: **§ Getting skinny**.

---

## Where we are

| Done | Why it mattered | CR |
| --- | --- | --- |
| base-4 pack + Terminate table + Layer A G1/G2/G3 | Candidate foundation | **CR-2** Done |
| Multi-BASE inspector (`index.html`) | Diff packs | **CR-7** Done |
| Policy docs + RELEASE_NOTES + ROADMAP on main | Train language | **CR-8** Done |
| Multi-round Client **docs** | Bags A–D | **CR-17** Done |
| **base-5 pack on disk** (`v2/base/base-5/`) | **Last breaking freeze**: object triggers, `app_output`, inject contracts | **CR-3** / **CR-22** |
| Docs: playbook, migration hops, RELEASE_CHECKLIST, COMPAT | Agent-friendly BASE bumps | PR #4–#5 |
| Process: `verify_base_pack.py` + phased checklist + Jira §9 | Scaffold ≠ ship | **CR-19** (PR #6) |
| `scripts/new_base.py` | Repeatable pack scaffold | — |
| zeus_client **wishlist** (`ZC-WISH-*`) | Prioritized Client backlog | [ZEUS_CLIENT_WISHLIST…](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) |
| **base-5.1 mode overlays** pack + CORE/overlay | Stop analytics×rename | **CR-23** |
| **base-5.2 dual gaps** design + pack path | `wish_i_knew` + `data_gaps` | **CR-24** |
| Latency diagnosis + skinny plan in ROADMAP | Honest AI-floor + verb surface | **CR-26** |
| base-5.2 13-verb review vs Zeus `docs/API/V2` in ROADMAP | Findings + P0/P1 clarity backlog | **CR-26** |
| **base-5.3 pack on main** — world-model CORE + verb clarity P0–P2 + hop docs | Content train closed (PR #12) | **CR-26** Done (pack) |
| Playbook + HINTS catalog + Pachinko OPTIMIZATION | Day-one recipes + base-6 design + rails end-goal | PR #13 |
| **base-6 pack on main** — soft `hints.*` contract + CORE note | Additive train (CR-4 pack) | **CR-4** pack |

| Still open | Risk | CR |
| --- | --- | --- |
| zeus_client implements object triggers + settings/policy/`output_request` | Catalogs ready; Client floor TBD | **CR-20** (+ CR-9/10/11) |
| Zeus loaders / return schema / Detective for base-5+ | Can’t pin CURRENT | **CR-21** |
| ~~**Zeus vendor pin base-5.2 → base-5.3**~~ | ~~Hub taught order.`direction`~~ | **ZE-273** Done on 5TH train (0.6.15) |
| Hot Path / Prompt Helper: per-verb use over last N runs | Guessing which verbs to diet | Workbench / **ZE-267** (CR-26 residual) |
| Inject reliability (brief + mini-schema always on product path) | Model rediscovers when inject missing | Client + Zeus CR-20/21 |
| Helios Pri-1 report emits (cheap spine) | Not catalog tax | **CR-12** |
| Required four incomplete in the wild | Detective / soft-require levers | CR-21 + Client |
| CURRENT still base-1 | Expected until green | **CR-18** (blocked by CR-20/21) |
| Client injects `hints.*` after rules{} | Soft steer not live until Client | **CR-4** residual · ZC-WISH-040 |
| **base-6.1 pack** — CORE + report_sink schema + docs | Candidate pack | **CR-27** |
| Client stamps `user` + `ip_address` + `ai_process_result` loop | base-6.1 residual | **CR-28 / CR-29** · ZC-WISH-035 / 044 |
| Helios filter `user="zeus_client"` | base-6.1 residual | **CR-30** · HEL-WISH-022 |
| ~~**base-6.2 pack** — skinny system + tools~~ | ~~Catalog prefix diet~~ | **CR-34** pack **landed** · A/B residual |
| base-7 Workbench / stamp product | Later | **CR-5** |

**Pack SoT for new work:** **base-5 wire** · **candidate pack base-6.2** (`v2/base/base-6.2/`) · prior **base-6.1** · **base-6** · **base-5.3**.  
**Production pin:** **base-1**.  
**Zeus 0.6 vendor:** **base-5.3** as of **ZE-273** / `0.6.15` (base-6 / 6.1 / 6.2 packs available; not required pin).  
**Hop:** [migration/base-6.1_to_base-6.2/](migration/base-6.1_to_base-6.2/) · prior [base-6_to_base-6.1/](migration/base-6_to_base-6.1/) · [HINTS.md](HINTS.md).  
**Modes:** [MODE.md](MODE.md) · plan [work/RECREATE_MODE.md](../work/RECREATE_MODE.md).  
**Client implement order:** [ZEUS_CLIENT_WISHLIST…](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) · **ZC-WISH-035/044** (base-6.1) · soft hints **ZC-WISH-040**.

---

## CR board map (project CR)

Board: https://kotenai.atlassian.net/jira/software/projects/CR/boards/48  
Last status pass: **2026-07-28** (CR-34 + full **§ base-6.2** train doc: baseline, targets, goals, placement, success split).

| Key | Role | Board status (intent) | ROADMAP home |
| --- | --- | --- | --- |
| **CR-1** | Epic — repo SoT / BASE sequence / COMPAT | In Progress | This repo strategy (ongoing) |
| **CR-2** | Epic — base-4 ship | **Done** | § Where we are (base-4) |
| **CR-3** | Epic — base-5 pack + residual | In Progress | § base-5 |
| **CR-4** | Epic — base-6 additive (pack green; Client residual open) | **In Review** | § base-6 · [HINTS.md](HINTS.md) · **§ base-6.2** |
| **CR-5** | Epic — base-7 Workbench | To Do | § base-7 · **ZE-267** / **ZE-285** |
| **CR-6…8, CR-17** | base-4 stories | **Done** | base-4 train |
| **CR-9** | company_context inject (Client) | In Progress (spec/pack done) | base-5 · ZC-WISH-006 |
| **CR-10** | jailbreak rules{} + hooks | In Progress (spec/pack done) | base-5 · ZC-WISH-002/013 |
| **CR-11** | object triggers + policy table | In Progress (pack done) | base-5 · ZC-WISH-004/010 |
| **CR-12** | Helios Pri-1 cheap spine | To Do | Helios Pri-1 · ZC-WISH-030… |
| **CR-13** | base-6 pack: HINTS / hot_path / ab_paste slots | **Done** (pack) · residual **CR-33** | § base-6 · **§ HINTS catalog** |
| **CR-14** | base-6 G2 hygiene + budget + norms | To Do | § base-6 |
| **CR-15…16** | base-7 stories | To Do | § base-7 |
| **CR-18** | Pin promote CURRENT | To Do (**blocked** CR-20/21) | § base-8+ |
| **CR-19** | Process verify + checklist | Done | Process / CREATE_BASE |
| **CR-20** | zeus_client base-5 floor | In Progress | § base-5 · full wishlist |
| **CR-21** | Zeus base-5 loaders/Detective (+ vendor) | To Do / residual | § base-5 external · **ZE-286** vendor 6.1 |
| **CR-22** | Pack docs completion tracker | Done | § base-5 pack |
| **CR-23** | **base-5.1** mode overlays | **Done** (pack) | § base-5.1 · [MODE.md](MODE.md) |
| **CR-24** | **base-5.2** dual gaps design | **Done** (pack) · residual **CR-32** | § base-5.2 · [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) |
| **CR-25** | Snapshot folders process | **Done** | process P0 |
| **CR-26** | **base-5.3** pack — residual Hot Path **ZE-267** | **Done** (pack) · residual product | § Getting skinny · § base-5.3 |
| **CR-27** | **base-6.1** pack sink stamps + ai_process_result docs | **In Review** (parent **CR-4**) | § base-6.1 |
| **CR-28** | Client residual: stamp `user` + `ip_address` (ZC-WISH-035) | To Do (parent **CR-4**) | § base-6.1 · Client |
| **CR-29** | Client residual: `ai_process_result` loop (ZC-WISH-044) | To Do (parent **CR-4**) | § base-6.1 · Client |
| **CR-30** | Helios residual: filter `user="zeus_client"` (HEL-WISH-022) | To Do (parent **CR-4**) | § base-6.1 · Helios |
| **CR-31** | PROMPT_RULE_PLACEMENT methodology (all modes) | **In Review** (docs; parent **CR-1**) | [PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md) |
| **CR-32** | Progressive empty → wish_i_knew (assemble CORE → min packs) | To Do (parent **CR-3**) | § base-5.2 · BP:13 |
| **CR-33** | Client residual: inject `hints.*` (ZC-WISH-040) | To Do (parent **CR-4** · pairs CR-13) | § base-6 · Client |
| **CR-34** | **base-6.2** skinny chat_prompt (system + tools; full-13) | **In Review** (pack) · A/B residual | **§ base-6.2** · § Getting skinny |

**Zeus project (engine/Hub) companions**

| Key | Role | Status |
| --- | --- | --- |
| **ZE-273** | Vendor pin base-5.3 | **Done** |
| **ZE-267** | Hot Path → named_query rails (base-5.3 residual + base-7) | To Do · relates CR-26 / CR-5 · **not** default base-6.2 verb drop |
| **ZE-285** | A/B promotion doctrine visibility (code 0.6.49; Hub banner AC open) | To Do · relates CR-5 · use for **6.1 vs 6.2** A/B |
| **ZE-286** | Vendor pull base-6.1 when CR-27 green | To Do · **blocked by CR-27** · 6.2 vendor later |

**Jira links:** CR-18 ←blocked-by CR-20/CR-21 · ZE-286 ←blocked-by CR-27 · CR-13↔CR-33 · CR-27↔CR-28/29/30 · CR-24↔CR-32 · CR-26↔ZE-267 · CR-5↔ZE-267/ZE-285 · **CR-34↔CR-26/CR-27/ZE-267**.

When a train lands: update epic + create residual stories (checklist [§9](migration/RELEASE_CHECKLIST_TEMPLATE.md)).

---

## Helios wishlist → BASE / emit owner

Canonical detail: [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) §3–§5.  
**Do not** shove Pri-1 cheap items into AI Layer A.

### Priority 1 (cheap — ship first, almost never AI)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **003** | Outcome quality beyond `status=ok` | **Zeus** report | No catalog growth — Zeus emit |
| **008** | Path / rail / evidence counts | **Zeus** | No |
| **013** | User text preview (privacy-safe) | **Zeus** | No |
| **014** | Funnel / path stage enum | **Zeus** | No |
| **007** | Locale / language / timezone | **Client** → Zeus | Client inject / session headers |
| **009** | Channel & tenant-safe identity | **Client + Zeus** | Client session |

→ Track under **base-5 “emit spine”** (Zeus/Client workstreams), not “more return fields.”

### Priority 2 (cheap / mixed — next)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **002** | Session market geo | **Client** | Inject / config |
| **001** | `geo_norm` | AI `geo` string **piggyback** → **Zeus geocode** | Guidance: keep free-text `geo` on QD; Zeus fills norm |
| **012** | `multi_part` true-only + sparse AI | **Zeus** normalize; AI may propose parts | Guidance in Terminate / QD docs (not always-on) |
| **016** | Deployment / ruleset / mode slice | **Client + Zeus** | Session config (ties to base-id pin) |
| **017** | Context dump metrics | **Zeus** | No |
| **018** | Compare score parts | **Zeus** when ranking | No |
| **019** | Refine offer / recovery | **Zeus / Client UI** | No |

→ **base-5:** document QD optional facets (`geo`, `parts`) in Terminate notes (guidance only).  
→ **base-6+:** implement norms on Zeus/Client as **optional / additive** (nice-to-have; not wire breaks).

### Priority 3 (scheduled — optional_when / map first)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **004** | `price_norm` numeric | Client slider preferred; AI last | Guidance types; not required every turn |
| **005** | `intent_norm` enum | Zeus synonym map preferred | Optional closed set in guidance |
| **011** | Demand rollups | Zeus jobs | No Layer A |
| **020** | chat_id recovery link | Zeus | No |
| **021** | Tool sequence fingerprint | Zeus from `tool_usage` | No |

### Priority 4–5 (defer AI-heavy)

| ID | Title | Primary owner | BASE touch? |
| --- | --- | --- | --- |
| **006** | Constraints / party size | Client forms preferred | Avoid AI-required bags |
| **010** | JTBD / sentiment | AI only | **Do not** put on hot-path terminate |

### Helios Motions → BASE alignment (quick)

| Motion | Wishlist unlocks | Prefer |
| --- | --- | --- |
| Explore | 013, 001, 017 | Zeus scalars + geo_norm |
| Compare | 018, 005, 013 | Zeus scores; intent_norm map |
| Refine | 019, 006, 004 | Product events; forms not AI |
| Funnel | 014, 016, 003 | Zeus stage + outcome.kind |

### Build order (from Helios §3 — unchanged)

```text
1. Zeus: outcome.kind + user_visible_count (003)
2. Zeus: path/funnel stage + evidence counts (008, 014)
3. Zeus: user_text_preview; context.chars (013, 017)
4. Client: language, tz, channel, tenant, market, deployment_id
5. Zeus: multi_part true-only; geocode geo_norm
6. Product: compare scores (018); refine (019)
7. AI only if needed: intent_norm / price_norm (optional_when)
8. Defer: soft AI JTBD/sentiment (010)
```

---

## base-5 — “Last breaking freeze + company + control plane”

**Theme:** Take **all remaining wire/control-plane breaks now** (nothing prod on this line yet). Freeze a clean contract: company + hard named rules; Layer A **objects** + **`app_output`**; Client **settings + policy table + merge/freeze**. Helios Pri-1 stays **Zeus/Client report emits** (nice spine, not Layer A tax).

**Design detail:**

| Doc | Covers |
| --- | --- |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers · `output_request` → `app_output` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security · multi-turn · observability |
| [BIBLE.md §2](BIBLE.md) | Who may set / unset / change |
| [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) | Score + hard rules + hooks |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | Agent comply/upgrade checklists |
| [migration/base-4_to_base-5/](migration/base-4_to_base-5/) | Hop + GUIDE + RELEASE_CHECKLIST |
| Pack | [`v2/base/base-5/`](../v2/base/base-5/) | Candidate on disk |

### Headline deliverables (must ship in base-5)

| Deliverable | Where | Notes |
| --- | --- | --- |
| **`company_context` / service brief** | Prompt inject | After MINI-SCHEMA, before `rules` · ≤150 soft / 250 hard words · hash-excluded |
| **Jailbreak + hard `rules` as object** | Prompt inject | `{ rule_id: "one sentence" }` · [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) |
| **`business_rules_triggers` as object** | Terminate G3 | `{ rule_id: bool }` · missing = false · sparse |
| **`output_request` → `app_output`** | Inject + Terminate | See **§ base-5 output_request (type + description)** below — not type-only |
| **`message_jailbreak_soft`** (+ `message_*`) | Boilerplate | User-facing refuse; never show score |
| **`policy_action` soft-required** | Terminate G3 | Client maps → `message_*` |
| **Settings bag** | Client config (not essays) | `max_rounds`, model, verb deny, locale/channel/tz, redaction, debug, `output_request` · [PROMPT_SETTINGS §1](PROMPT_SETTINGS.md) |
| **Rule pack merge + freeze** | Client logic | SDK defaults ∪ tenant ∪ request · `override_defaults` · append-only keys mid-session · [§2](PROMPT_SETTINGS.md) |
| **Hard vs soft separation** | Docs + Client | Hard = `rules{}`; soft = hints later; brand = `message_*` |
| **Client post-terminate policy table** | After every `return` | Triggers = signals; Client (+ hooks) = law · chrome · flags · metrics · [§3](PROMPT_SETTINGS.md) |
| **Dual jailbreak scores** | Metrics | Model `jail_break_attempt` + Client `hooks_jailbreak_score` (do not overwrite) |
| **Session prefix vs refresh zones** | Assembly | Stable catalog+company+rules; dirty brief/schema; prune tool bodies · [§4](PROMPT_SETTINGS.md) |
| **Terminate reliability levers** | Client | Soft-require from `output_request.layer_a`; optional force final `return` when budget low |
| **Inject security** | Client | Schema caps; strip secrets; tool JSON = untrusted data; safe log defaults · [§8](PROMPT_SETTINGS.md) |
| **Multi-turn semantics** | Client | Sticky OR flags for business keys; clarify loop keeps `output_request`; mode switch = new session · [§6](PROMPT_SETTINGS.md) |
| **Cheap observability** | Client/Zeus | `ruleset_id`, inject-present bools, zone size estimates, trigger key rates · [§9](PROMPT_SETTINGS.md) |
| **AgentHooks baseline** | Client code | Prompt-dump / secrets / denied verbs even if model cooperates |

**Why base-5 (not base-4, not base-6):**  
base-4 has the **thermometer** and Terminate table (triggers still **arrays**). Real products need **policy in the prompt**, **named control-plane**, **settings not essays**, and **post-model law**. Soft HINTS/A-B and Helios norms are **additive later** — they must **not** re-open the wire.

### Breaking vs base-4 (take **all** of this now — document in RELEASE_NOTES)

| base-4 | base-5 (**canonical; no multi-BASE dual-read plan**) |
| --- | --- |
| `rules: string[]` (index `0` often empty) | `rules: { [id]: string }` **only** |
| `business_rules_triggers: boolean[]` | `business_rules_triggers: { [id]: boolean }` **only** (sparse) |
| No first-class app bag | `app_output` when Client sends `output_request.app.fields` |
| Type-only app maps (e.g. `sum_favorites: "INT"`) | **Rejected** — each field needs **`type` + `description`** |
| Informal Client behavior | Normative settings bag + merge + policy table + hooks dual score |
| Array triggers forever / dual-read lifestyle | **Migrate once** · Client dual-read **≤ 1 release** then **remove** |

### Frozen after base-5 (do not break without a new major BASE + migration hop)

| Surface | Frozen shape |
| --- | --- |
| `rules` / `business_rules_triggers` | **Objects** keyed by stable `rule_id` |
| `app_output` | Optional G3/app bag; field map is type+description on inject |
| Settings bag | Structured keys (max_rounds, locale, redaction, verb deny, …) — extend additively |
| G1 / G2 / G3 audiences | User / admin / client split on Layer A |
| Required four | Unchanged forever unless major BASE |
| Soft inject slot names | Reserve hash-excluded `hints.*` for base-6+ (**additive**; implement later) |

After base-5 ships as candidate: **prefer only additive optional fields and soft injects** until pin.

### base-5 `output_request` — type + description (summary)

**Rule:** each app field is **`type` (validate) + `description` (model instruction in the prompt)**. Type-only maps like `{ "sum_favorites": "INT" }` are **rejected**.

```text
App:  fields.sum_favorites = { type: integer, description: "Sum favorites…; 0 if none" }
Client → prompt "Output request" block from descriptions
AI → app_output: { "sum_favorites": 1284 }
Client → type-check values (descriptions not re-emitted)
```

**Canonical detail + full examples:** [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) §2  
**Ownership:** [BIBLE.md](BIBLE.md) §2 · **Version floors:** [COMPAT.md](../COMPAT.md)

### Catalog / Client goals (full list)

**Prompt / Layer A**

1. **`company_context` formal inject** — tenant identity + do/don’t; Client truncate at hard max.  
2. **Default jailbreak `rules` pack as named object** — keys: `ignore_system`, `no_prompt_dump`, `no_unrestricted_agent`, `no_invent_data`, `no_secrets`, `stay_in_company_context` (+ tenant keys).  
3. **`message_jailbreak_soft`** mapped from `policy_action: refuse` when jailbreak-like.  
4. **`business_rules_triggers` object contract** — G3; sparse; no pad-to-length.  
5. **`output_request`** — `layer_a.soft_require` / `include`; **`app.fields` each `{ type, description }`** → prompt block + terminate **`app_output`**; optional `rows.fields`; **reject type-only**; cannot remove required four.  
6. **`policy_action` soft-required** — Client `message_*` mapping.  
7. **Required four always practiced** — Terminate example first; Detective-aligned missing-field language.  
8. **Verb schema diet (names stay)** — shorter descriptions · **deferred implement to base-5.3 skinny** (§ Getting skinny) while base-5 freezes wire.  
9. **Text↔JSON policy** — import script or “edit JSON only”; pick one.

**Control plane (new — most of “the above”)**

10. **Settings bag** — structured run/session options; ownership per Bible §2.8.  
11. **Rule pack merge** — SDK ∪ tenant ∪ request; reject silent deletion of default jailbreak keys unless `override_defaults`.  
12. **Session freeze** — rule ids frozen; append-only mid-session; rename/delete ⇒ new session.  
13. **Hard vs soft** — never put jailbreak law only in hints.  
14. **Post-terminate policy table** — every return: normalize triggers → hooks force → map chrome → sticky flags → validate `app_output` → metrics.  
15. **Conflict law** — jailbreak keys + hooks beat business keys for refuse paths.  
16. **Assembly zones** — document stable prefix vs dirty brief; allow full re-assemble v1 or frozen prefix.  
17. **Artifacts vs prompt** — full tool JSON in artifacts; prune in `messages[]`; tool rows untrusted.  
18. **Terminate reliability** — soft-require list; optional force `return` near `max_rounds`; no new system essay as first fix.  
19. **Security** — `output_request` size caps; redaction defaults; `pii_in_logs: false`; allowlist inject keys.  
20. **Multi-turn** — sticky business flags; clarify-loop semantics; catalog/mode switch = new pin/session.  
21. **Observability** — `ruleset_id`, zone sizes, dual scores, per-key trigger rates (no full prompt dumps by default).  
22. **AgentHooks baseline** — hard block prompt-dump / critical paths.  
23. **Bible §2 ownership** — App / Client / AI set·unset·change enforced in Client reviews.

### Helios goals (Pri-1 cheap — primary Zeus/Client)

| Work | HEL-WISH | Why here |
| --- | --- | --- |
| Outcome.kind + counts | **003** | Fill rate without re-parsing tools |
| Path/evidence scalars | **008** | Rail health charts |
| Funnel stage enum | **014** | Funnel Motion |
| user_text_preview | **013** | Explore samples without PII dump |
| Client locale/tz/channel/tenant | **007, 009** | Slice dashboards · **settings bag** |
| Document: do **not** add these to Layer A | — | Cost law |

### Catalog guidance only (no required AI tax)

| Work | HEL-WISH |
| --- | --- |
| QD optional `geo` piggyback for geocode | **001** |
| Sparse / `multi_part` true-only semantics in Terminate notes | **012** |

### Explicit non-goals for base-5

- Require `wish_i_knew` / make `jail_break_attempt` required (still recommended telemetry; **rules go in prompt**)  
- Soft **HINTS / A/B paste UI** (**base-6+ additive** — not a second wire break)  
- AI-primary HEL-WISH-004/005/006/010 (nice-to-have / off-path)  
- Multi-year dual-read of array triggers (objects only after ≤1 Client release)  
- TOON as SoT · separate index HTML · pin CURRENT without Client proof  
- Multi-page company manifesto in the inject (hard-cap 250 words)  
- Giant `app` JSON Schema dumps (soft max ~8 properties; hard ~15)  
- Replacing required four with app schema alone  
- Provider prompt-cache **product** as a hard dependency  
- Auto-summarize tool history via a second LLM (truncate first)  
- Workbench full key/value editor (additive **base-7** product)  
- Blocking base-5 on Helios Pri-2+ dashboard norms  

### Success signals

**Pack / docs (this repo) — largely green after PR #5:**

- [x] Diff base-4 → base-5 documents **all breaking wire** (array→object, app_output, control plane) — RELEASE_NOTES + hop GUIDE  
- [x] base-5 catalogs: **object rules/triggers only** (no array as SoT)  
- [x] COMPAT: base-5 **candidate** row (object-only Client floor noted; package TBD)  
- [x] Playbook + migration hop describe base-5 as **last breaking** train  
- [x] Pack verified: `python3 scripts/verify_base_pack.py --base 5`  

**Client / Zeus residual — still open (CR-20 / CR-21):**

- [ ] Client: object triggers; dual-read arrays **≤1 release** then removed  
- [ ] Client injects **company_context** + **merged frozen jailbreak `rules` object**  
- [ ] Client spike: `triggers.get("coupon_presented")` + sticky flags + `policy_action` + `message_jailbreak_soft`  
- [ ] Client spike: **settings bag** + **policy table** every terminate  
- [ ] Client spike: `output_request.app.fields` type+description → prompt + validated **`app_output`**  
- [ ] Client **rejects** type-only fields  
- [ ] Merge rejects deleting default jailbreak keys without `override_defaults`  
- [ ] Tool JSON untrusted; G2 never in chat UI  
- [ ] Cheap emit: `ruleset_id` / zone sizes (ops, not Layer A tax)  
- [ ] Refuse path works on [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) examples  
- [ ] Helios Pri-1 path on **Zeus report** (003 or 014) — not new required AI fields (**CR-12**)  
- [ ] COMPAT: Client package version row when floor ships  
- [ ] Catalog bytes ≤ base-4 or justified  

**Track Client work as `ZC-WISH-*`:** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) · umbrella **CR-20**.

### Why this order

**Break the wire once (base-5)** while no one is prod on this line, then **content patches (base-5.1)** and **only additive/optional** (base-6+) changes. Soft A/B and Helios norms must not force a second contract rewrite. Helios Pri-1 remains **report/session emit**.

---

## base-5.1 — “Mode overlays restored” (content on base-5 wire)

**Jira:** **[CR-23](https://kotenai.atlassian.net/browse/CR-23)** · parent epic **CR-3** · status To Do  
**SoT:** [MODE.md](MODE.md) · **Plan:** [work/RECREATE_MODE.md](../work/RECREATE_MODE.md)  
**Design:** [zeus_design_docs DESIGN.md §14](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) · Zeus `internal/modes/`

**Theme:** base-5 **froze the wire** but left **10 mode packs nearly identical** (analytics system essay × rename; only `auto` shorter). **base-5.1** restores DESIGN mode intent into the **stamped system prompt** (`messages[].content` = shared CORE + per-mode **MODE_OVERLAY**). **Not** a Layer A / object break.

| | |
| --- | --- |
| **Wire** | Same as base-5 objects / app_output / required four (content on that wire) |
| **Content** | Mode personas: entities, join/noise posture, edges, don’ts, example pipelines |
| **On disk** | **`v2/base/base-5.1/`** full snapshot · parent `base-5` · Diff vs `base-5/` |
| **Generator** | Fill Zeus `ai/V2/prompt/core/modes/<mode>.md` (optional follow-up) |

### Goals

1. Core + thin overlay architecture (not 10 full forked essays).  
2. Overlays for all 10 modes (priority: analytics → fraud → research → code → regulated → tenant/private/open → auto → custom).  
3. Clean clone leftovers (`[exp] analytics job`, etc.).  
4. `diff_modes` / clone gate so `new_base` cannot re-ship analytics×rename.  
5. Port overlays into Zeus snapshot path.  
6. Inspector Diff analytics vs fraud/research/code is human-meaningful.

### Explicit non-goals for base-5.1

- Rename/remove base-5 wire keys or required four  
- Soft HINTS/A/B (**base-6**)  
- Pin promote (**CR-18**)  
- Client policy-table implement (**CR-20**) — orthogonal; can parallel  
- Full Zeus `AppliesTo` tool matrix rewrite (optional later)

### Success signals

- [x] [MODE.md](MODE.md) + [RECREATE_MODE.md](../work/RECREATE_MODE.md) authored  
- [x] CORE extracted; all 10 modes assembled CORE + overlay  
- [x] fraud / research / code / regulated (+ tenant/private/open/auto/custom) overlays in packs  
- [x] Keyword/entity smoke via `diff_modes.py --fail-if-clone`  
- [x] Neutralize-mode signatures unique per mode  
- [x] `verify_base_pack.py --base 5` OK  
- [ ] Zeus `modes/<mode>.md` ported (follow-up; dual-home = `work/mode_overlays/`)  
- [x] RELEASE_NOTES notes base-5.1 content train  
- [ ] CR-23 Done (after PR merge)  

### Sequencing vs other work

```text
base-5 pack (wire)  ──done──►  base-5.1 (mode prompts)  ──►  base-5.2 (dual gaps)
        │                            │                              │
        │                            │                              ▼
        │                            │                       base-5.3 (skinny)
        │                            │                              │
        └── Client CR-20 / Zeus CR-21 ┴──────────────────────────────┴── pin last
                                                                         │
                                                                    base-6 soft injects
```

Prefer **base-5.1 before or in parallel with Client spike** so trials exercise real mode personas, not 10 analytics clones.  
Prefer **base-5.3 skinny before pin** so production surface is not “always 13 + rediscover.”

---

## base-5.2 — “Dual gap channels: wish_i_knew + data_gaps”

**Jira:** **[CR-24](https://kotenai.atlassian.net/browse/CR-24)** · parent epic **CR-3**  
**SoT:** [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md)  
**Related:** [BIBLE.md](BIBLE.md) §5 · [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)

**Theme:** Keep the **classic** operator feedback channel (`wish_i_knew`) and **append** a Helios-oriented acquisition channel (`data_gaps`) when the model cannot fully answer because **schema / data / index** is missing. Both G2, optional, never chat UI. **Additive** on base-5 wire — not a required-four break.

| Stream | Field | Consumer |
| --- | --- | --- |
| **A classic** | `wish_i_knew[]` (keep) | Detective, Workbench, prompt ops |
| **B acquisition** | `data_gaps[]` (new) | Helios backlog / Motions (+ precomputed counts) |

**Progressive empty (doctrine add-on):** ≥2 tool-backed empties on the **same topic/facet** (user may broaden constraints) → treat as systemic gap: G1 inventory when possible + **MUST** `wish_i_knew` (still optional on smooth single turns). See [WISH_I_KNEW_DUAL.md §3.3.1](WISH_I_KNEW_DUAL.md) · BP:13.

### Goals

1. Design doc with A vs B rules and examples.  
2. Additive wire: keep array `wish_i_knew`; add optional `data_gaps` with machine keys.  
3. Document Zeus string dual-read for A; Helios cost law for B.  
4. Implement PR later: schema + terminate table + Client/Zeus parse + report rollups.  
5. Progressive same-topic empty → G2 must-fire + G1 facet inventory (docs + CORE blurb).

### Explicit non-goals

- Require A or B every turn *(except same-topic empty streak ≥2 — still cap max 3 items)*  
- Nest-break `wish_i_knew` into `{feedback, acquisition}` without dual-read  
- Soft HINTS/A/B (**base-6**)  
- Pin promote  

### Success signals

- [x] [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) design authored  
- [x] ROADMAP § base-5.2  
- [x] CR-24 created  
- [x] Progressive empty streak doctrine (§3.3.1 + BP:13 + CORE dual-gaps line)  
- [ ] Design PR merged to main  
- [ ] Schema + pack terminate table implement (follow-up)  
- [ ] Rebuild min packs so Dual gaps line ships in stamped catalogs  
- [ ] Client/Zeus parse + Helios precomputed counters  

---

## Getting skinny — latency + verb surface plan

**Jira:** **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** (create if missing) · parent epic **CR-3**  
**Train:** **base-5.3** (content on base-5 wire — **not** a Layer A / object break)  
**Related:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · Zeus `docs/API/V2/describe.md` · Detective / Hot Path / Prompt Helper · stamp + `contract_hash`  

**Why now:** base-5 → 5.2 improved contracts, modes, and dual gaps. Live Detective packs show wall time still dominated by **`ai.chat.round.*`**. Catalog bytes grew. Operators still see wasteful **`describe()`** (sometimes because inject was missing — a different bug). We need an explicit **skinny** train — and we must **not** “optimize” by mutating the hashed tool list mid-session.

### North star (skinny)

```text
1. Platform keeps all 13 Zeus verbs (names + HTTP stay)
2. Production tools[] = stamped contract verbs[] when enforcement is on
3. Prefer inject + data plane over rediscovery; teach via prose, not runtime strip
4. Prefer one terminating pipeline over multi-round orientation
5. Measure: rounds, per-verb use rates, rediscovery, tokens, ai_ms — not vibes
6. Drop verbs only after empirics → new stamped pack / A/B arm (re-hash)
7. Never grow always-on Layer A for Helios or “maybe useful” fields
```

### Law: hashed contract owns tools[] (critical)

`verbs[]` (OpenAI-style tools) participate in **`contract_hash`** when a pack is stamped. With **contract enforcement on**:

| Do | Don't |
| --- | --- |
| Ship the **full stamped** tools list for that pin | **Strip** `describe` (or any verb) from tools[] mid-chat because mini-schema arrived |
| Re-pin / re-stamp a **new** pack/custom that omits unused verbs | Mutate tools[] after bind and expect Zeus to execute happily |
| Use **prompt prose** + inject reliability so the model *doesn't call* escape verbs | Assume “deny after the model already planned the call” is free |
| Use **Prompt Helper / Hot Path / A/B** to *decide* which verbs to drop next stamp | Guess a subset without run data |

**Why strip-at-runtime fails:** Client/Zeus bind a pin to a hash of catalog body including tool schemas. If tools[] on the wire no longer match the stamped contract, **enforcement refuses the chat or tool path** — the “optimization” becomes a hard failure.

**Hooks `denied_verbs`:** fine for **safety** (refuse a call the model still *could* name) — that is not the same as removing the tool from the LLM tools list under a stamped hash. Safety deny after a wasted tool_call is still a wasted round. Prefer not listing a verb only in a **new stamped** skinny pack used by A/B or a deliberate pin.

### How to actually drop APIs (right venues)

| Venue | Role in skinny |
| --- | --- |
| **Hot Path / Detective analytics** | Over last **N hundreds of runs** (scope/mode/pin): count uses of each of the 13 verbs. Output: never / rare / common. |
| **Prompt Helper** | Operator co-pilot: surface the use histogram, propose “drop candidates,” draft a skinny custom or guidance, run books. |
| **A/B testing** | Arm A = current full stamp; Arm B = **re-stamped** pack with candidate verbs removed (or thinner schemas). Promote B only if quality + latency win. |
| **base-5.3 content pack** | Prose + schema **byte** diet on the full-13 baseline (still hashable); optional **documented** skinny customs once empirics exist. |
| **Production pin** | Change verb membership only by **promoting a stamped** skinny pin — never by Client list surgery. |

#### Empirical report shape (target)

```text
window: last 500 runs · scope=beer-sample/_default · mode=analytics · pin=base-5.2
verb          calls   runs_with≥1   share_of_tool_calls
return          …         …              …
pipeline        …         …              …
search          …         …              …
find            …         …              …
…
describe        …         …              …   ← rediscovery rate vs inject_green
explain         …         …              …
```

**Decision rule (sketch):**

```text
never used in window     → strong A/B drop candidate (keep on platform)
hardly used (< threshold)→ drop candidate or workbench-only pack
often used + wasteful    → prose / inject fix first (e.g. describe + inject green)
always needed            → keep; diet schema text only
```

Pair with **inject_green** × **describe_called** so “describe because schema missing” is separated from “describe despite schema present.”

### Verb tiers (planning / A/B design — not runtime mutation)

Use as a **hypothesis** for Hot Path reports and skinny stamps; do **not** apply as per-turn tools[] surgery under enforcement.

| Tier | Verbs | Role |
| --- | --- | --- |
| **Usually hot** | `find`, `search`, `get`, `order`, `project`, `set`, `enrich`, `pipeline`, `return` | Data + shape + terminate on healthy packs |
| **Conditional** | `traverse` | Graph / walk_path scopes |
| **Job / heavy** | `analyze` | Analytics jobs / Motions |
| **Escape / debug** | **`describe`**, **`explain`** | Orientation + planner — valuable when inject missing or admin; costly as default habit |

#### `describe` — normative guidance (still true)

From Zeus (`docs/API/V2/describe.md`): `describe` is the **callable companion** to the brief/schema — **never a replacement**.

| Inject state | **Correct** response | **Wrong** response under enforcement |
| --- | --- | --- |
| BRIEF + MINI-SCHEMA **present** | Prose: do not rediscover; model should skip `describe`. Metrics if it still calls. | Strip `describe` from tools[] for this turn only |
| Inject **missing / bad** | **Fix inject** (or use a pack/session that includes `describe` by stamp); treat as reliability incident | Leave broken inject and hope discovery saves quality every time |
| User asks fresh inventory / indexes | Model may call `describe` (tool still on stamped list) | — |
| Workbench / Prompt Helper | Full 13 or experiment arms | — |

```text
Inject OK?  → use brief/schema; call data-plane verbs (still all listed if stamp says so)
Inject bad? → fix inject / re-assemble; do not “unhash” the catalog
Want fewer tools? → new stamp / A/B arm from Hot Path empirics
```

### What actually moves the AI floor

| Lever | Owner | Effect | Contract-safe? |
| --- | --- | --- | --- |
| **Prose no-rediscovery** | catalog base-5.3 | Fewer wasteful first calls | Yes (same tools[]) |
| **Verb schema diet** (names stay) | catalog base-5.3 | Less prompt tokens | Yes |
| **Verb clarity** (desc + params vs V2) | catalog base-5.3 | Fewer wrong tools / empty results | Yes — same 13 names |
| **Soft Layer A diet** | Client `output_request.layer_a` | Less completion | Yes (settings, not hash body if excluded) |
| **Inject reliability** | Client + Zeus | Stops “describe because no schema” | Yes |
| **Hot Path verb histogram** | Workbench / Detective | Evidence for what to drop | Yes (observe only) |
| **A/B skinny stamped pack** | Hub stamp + Prompt Helper | Real tools[] reduction | Yes — **new hash** |
| **Runtime strip tools when inject green** | — | Breaks enforcement | **No** |
| **Tool-history truncate** | Client multi-round | Round 2+ size | Yes |
| **Inject text diet** | Zeus Client | Moderate | Yes |
| **Model SKU** | App settings | Large | Yes |
| **One terminating pipeline** | catalog prose | Structural | Yes |

### Explicit non-goals (skinny)

- Removing verbs from Zeus / OpenAPI platform  
- **Runtime** remove/rewrite of stamped `tools[]` under contract enforcement  
- Renaming or dropping required four Layer A fields  
- Replacing inject with `describe` as the schema channel  
- Expecting base-5.3 prose alone to turn a 3s LLM call into &lt;1s if completion stays large  
- Stuffing more Helios fields into terminate “while we’re dieting”  
- Soft A/B *hints* as the only latency control without **stamped** tool-set A/B when dropping verbs  

### Phased plan

#### Phase 0 — Measure (now)

| Action | Owner | Success |
| --- | --- | --- |
| Gold set: same questions on base-1 vs base-5.2, same model | Ops / Prompt Helper | wall, ai_ms, rounds, tokens, rediscovery |
| **Per-verb use histogram** over last N runs (mode/scope/pin) | Hot Path / Detective | never / rare / common table |
| Cross-tab: `describe` × inject present | Detective | split “schema missing” vs “ignored schema” |
| Zone sizes: system / tools JSON / inject | inject_inspect | which zone dominates |

#### Phase 1 — Prompt Helper + Hot Path product (primary “drop API” path)

| Action | Owner | Success |
| --- | --- | --- |
| UI/report: “of 13 verbs, last N runs: unused / rare / hot” | Workbench Prompt Helper | Operators see candidates without guessing |
| Propose skinny **custom** or A/B arm from histogram | Prompt Helper | Draft pack with fewer verbs **for stamp** |
| A/B run full-13 stamp vs skinny stamp | Workbench A/B | promote only if quality holds |
| Document: **never** strip tools mid-session when enforcement on | docs / Hub | Operators don’t ship the anti-pattern |

#### Phase 2 — base-5.3 pack content (this repo)

| Action | Owner | Success |
| --- | --- | --- |
| **CORE world-model blurb** (DESIGN vocab — § World model language) | catalog | ≤ ~180 words; all modes via CORE + overlay |
| **Verb clarity P0–P1** (order/find/search/describe/get/traverse/pipeline — § Verb catalog clarity) | catalog | Schema matches Zeus V2; system example uses `asc` + `field:` |
| Pack prose: no rediscovery when inject present; `describe` = fallback, not default habit | catalog | Diff vs base-5.2 |
| Verb schema diet: drop duplicate Terminate text in params; keep KEY constraints | catalog | Clearer, not necessarily longer overall |
| Terminate one-liner: Layer A from evidence only | catalog | No field rename |
| Document empiric → stamp workflow (Hot Path → A/B → pin) | ROADMAP + playbook | Agents don’t invent runtime strip |
| Optional: **example** skinny custom in samples/ (not production pin) | pack | Template for A/B |
| `verify_base_pack.py` + Diff | process | Green |

Production default pin may **keep all 13** until Hot Path evidence says a skinny stamp is safe.

#### Phase 3 — Inject + multi-turn polish

| Action | Owner | Success |
| --- | --- | --- |
| Inject reliability: product path always sends brief + mini-schema | Client + Zeus | describe-for-missing-schema rate → 0 |
| Scope-aware inject diet (no empty noise; keep zero-row guards) | Zeus | Smaller inject |
| Multi-round tool body prune | Client | Round N doesn’t explode |
| Prompt-cache stable zones | Client + provider | Multi-turn savings |
| **Multi-turn prior-set law** in playbook (Option B) + OPTIMIZATION CORE candidate (Option A) | pack docs → content train | [BEST_PRACTICES §1.3](BEST_PRACTICES.md) · [OPTIMIZATION multi-turn](OPTIMIZATION.md#multi-turn-reuse-prior-zeus-evidence) |
| Soft `hints.multipart` / prior_result inject when Client ready | Client | ZC-WISH-040; follow-ups constrain to prior Zeus rows |
| Gold / Hot Path: “list set → filter among those” | Zeus Hub books | Unconstrained rediscovery rate down on “those/listed” asks |

#### Phase 4 — Optional later (base-6 / base-8+)

| Action | When |
| --- | --- |
| Soft hints that reduce bad paths without growing Layer A | base-6 |
| **Catalog prefix skinny (system + verb schemas; full-13)** | **base-6.2 · [CR-34](https://kotenai.atlassian.net/browse/CR-34)** · § base-6.2 |
| Productized prompt-cache | base-8+ |
| Structured-output constrained `return` | provider-proven |
| Promote skinny stamp to CURRENT only after gold + Hot Path green | pin gate |

### Success signals (skinny overall)

- [x] Latency law + skinny plan written in ROADMAP  
- [x] **Contract law:** no runtime strip of hashed tools under enforcement (documented)  
- [x] base-5.2 13-verb review vs V2 API findings in ROADMAP (§ Verb catalog clarity)  
- [x] CR-26 on board · **pack Done** (PR #12); residual product → ZE-267 / Hot Path  
- [ ] Phase 0 gold + **per-verb histogram** baseline  
- [ ] Prompt Helper / Hot Path surfaces never/rare/common verbs  
- [ ] At least one A/B: full stamp vs skinny stamp (re-hashed)  
- [x] base-5.3 pack: prose + **verb clarity P0** + schema diet; Diff content-only  
- [ ] Rediscovery rate down **without** breaking enforcement chats  
- [ ] Inject-missing rate down (root cause for many `describe` calls)  
- [x] COMPAT / RELEASE_NOTES note base-5.3 skinny train  
- [ ] ZC-WISH / Workbench notes: empirics → stamp, not mid-turn tools[] edit  

### Sequencing vs other work

```text
base-5.2 (dual gaps) ──► base-5.3 skinny + world-model + verb clarity
        │                      │
        │                      ├── CORE blurb (DESIGN overlay / shape / access class)
        │                      ├── Verb clarity P0–P1 (order/find/search/… vs V2 API)
        │                      ├── Hot Path / Prompt Helper (Phase 1) can lead
        │                      ├── A/B skinny stamps before production pin change
        │                      └── do NOT “fix inject ⇒ drop describe” under enforcement
        │
        └── Helios Pri-1 stays Zeus/Client report emits
```

Prefer **measure → A/B stamp → pin**, not **strip tools because inject looked green**.  
Prefer **short DESIGN worldview in CORE** over pasting foundation essays.  
Prefer **verb clarity before aggressive tool-count diet**.

---

## World model language for chat_request (DESIGN vocabulary)

**Jira:** folds into **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** (base-5.3 content)  
**Upstream SoT (Zeus product design):**

| Doc | Use for |
| --- | --- |
| [zeus_design_docs DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) §1 | **AI-Ready overlay** — source targets vs Zeus store; never mutate source bodies |
| DESIGN.md §7 (tool classes) + §7.8 | **Access class** (discovery / kv / lookup / vector / traversal / …) · **MINI-SCHEMA = shape** (legal `where`, FTS vs GSI, FK / inverse_fks, walk_paths) |
| DESIGN.md §14 | **Modes** — persona + limits (hop caps, confidence floors); analytics = safe default |
| [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) | E–T–E ancestry · **schema-as-world-model** vs form · “predicates as verbs for discovery” |

**Gap today (base-5.2):** packs already *have* tools, brief, mini-schema, and mode overlays, but they read like **efficiency + Layer A form**. The DESIGN / foundation thesis — *overlay world map + instruments, not form-fill* — is **implicit**, not taught. Layer A terminate is intentionally form-shaped (emit contract); the **data path** must not be taught the same way.

### Prefer / avoid (catalog copy)

| Prefer (DESIGN-aligned) | Avoid (as the main story) |
| --- | --- |
| **AI-Ready overlay** — project identity/relations from operator data; source of record stays owner’s docs | “Dump the table / fill the spreadsheet” |
| **World map** — entity types, attributes, edges/FKs, samples in SCOPE BRIEF + MINI-SCHEMA | Schema as **slots to invent values into** |
| **MINI-SCHEMA = shape** — legal `where` keys, index kind (`gsi` / `fts` / `display`), `fk_to`, `inverse_fks`, walk_paths | Treating every field as equality-filterable |
| **Access class / lens** — pick verb by how the fact is stored (id → get, equality → find, language → search, hop → traverse) | One giant “answer from context” or invent joins |
| **Navigator** — plan, call tools, answer from evidence | **Clerk** — invent nulls / SKUs / counts into a form |
| **Predicates for discovery** (tool args grounded in map) | Predicates as **field slots for invention** |
| **Mode** bounds hops, join noise, confidence floor | Unbounded multi-hop “explore everything” |
| Layer A terminate = **emit contract from evidence** | Layer A = invent analytics facets when tools found nothing |

### Two contracts (must stay distinct in prose)

```text
1) DATA contract  — world model in front of the model
   SCOPE BRIEF + MINI-SCHEMA + verbs → retrieve / hop / filter → evidence

2) EMIT contract  — Layer A terminate (required four + recommended)
   summary / QD / decomposition / confidence … filled FROM evidence
   (Helios/Client shape — not a substitute for retrieval)
```

base-5.2 already has (2) strong and (1) mechanical. base-5.3 must **name (1)** in ~one short CORE block so the model does not collapse both into form-fill.

### Canonical short blurb (draft for CORE — ship in base-5.3)

Keep **≤ ~120–180 words** in shared CORE (all modes). Mode overlays stay thin (DESIGN §14 persona). Do **not** paste DESIGN.md or the foundation essay.

```text
## How Zeus data works (read this once)

Zeus is an AI-Ready overlay over operator-owned documents: it projects
entities, attributes, and relations you can navigate — it does not replace
the system of record, and you must not invent facts into empty fields.

1) World map (already in this message when present)
   - SCOPE BRIEF = scale + vocabulary for this scope/mode
   - MINI-SCHEMA = shape: legal where keys, index kind (gsi|fts|display),
     entity_fk / inverse_fks, samples (ex:). Absence ≠ invent.
   - WALK_PATHS (if present) = pre-validated FK chains

2) Access path → verb (prefer cheapest that answers)
   - id / exact key     → get
   - equality / GSI     → find  (where only on [gsi] / scalar paths)
   - language / text_fts → search (never put text_fts paths in find where)
   - multi-hop / graph  → traverse (respect mode hop caps; real links > noise)
   - multi-step         → pipeline; terminate with return (or terminating pipeline)

3) Answer from evidence only
   - Layer A fields are an emit contract: fill from tool results / brief.
   - Missing data → clarify, empty rows, or wish_i_knew / data_gaps — do not invent.
```

**Company / tenant texture** stays in **`company_context`** (hash-excluded inject), not CORE:

```text
# company_context pattern (App/Client — ≤150 soft / 250 hard words)
- Durable things: people / places / things (or domain names: Beer, Brewery, …)
- Key links / events: which FK or edge is the “transaction” (e.g. Beer.brewery_id → Brewery)
- Measures vs language fields (align with mini-schema kinds)
- What “good evidence” means for this product (mode may tighten)
```

Beer-sample example (illustrative only):

```text
Beer and Brewery are the durable product/org entities.
Beer.brewery_id is the link Beer → Brewery (GSI FK; reverse = inverse_fks on Brewery).
name/description are language (text_fts → search); abv/ibu/srm are measures (gsi → find/order).
```

### Where each phrase lives

| Phrase / idea | Home | Hashed? |
| --- | --- | --- |
| Overlay + map + access path blurb | CORE system (base-5.3) | Yes |
| Mode hop/join/confidence posture | MODE_OVERLAY (already base-5.1) | Yes |
| Live shape + samples + walk_paths | SCOPE BRIEF / MINI-SCHEMA inject | No (runtime) |
| This business’s E–T–E story | `company_context` | No |
| Hard law | `rules{}` | Yes (merged freeze) |
| Layer A table + example | Terminate section (keep short) | Yes |
| Optional path hints | base-6 `hints.*` | No |

### Implementation plan (with skinny)

| Step | Owner | Deliverable |
| --- | --- | --- |
| 1. Land draft blurb in `work/mode_overlays/CORE.md` (or pack text SoT) | catalog / CR-26 | Diff vs base-5.2 shows one new short section |
| 2. Re-assemble all 10 modes CORE + overlay | `assemble_mode_prompts.py` | base-5.3 packs |
| 3. One line in Terminate: “Layer A from evidence only — not a second form for inventing data” | catalog | No Layer A field rename |
| 4. `company_context` recipe + beer example in BIBLE / PROMPT_ASSEMBLY or this ROADMAP | docs | Client authors know what to write |
| 5. Detective / gold: multi-hop + FTS questions still pass; no rediscovery spike | ops | Quality gate |
| 6. Optional: Prompt Helper chip “world model” points at blurb + mini-schema | Workbench | Later |

### Explicit non-goals

- Replacing MINI-SCHEMA with a long ontology essay  
- Teaching REA/ER/Kimball names in the hot system prompt (keep in design docs / talks)  
- Softening required four or growing always-on Helios Layer A fields  
- Runtime tool strip when inject green (still forbidden under enforcement)  
- Path B2 “restrict chat to raise hit rate” as the primary product story — modes/contracts bound **verbs and boundaries**, they do not replace a legible map ([ENTITY foundation](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) §7)

### Success signals

- [x] Vocabulary + draft blurb written in ROADMAP  
- [x] CORE blurb in base-5.3 packs (world-model + access path)  
- [x] Diff base-5.2 → base-5.3 shows worldview + skinny diet, no wire break  
- [ ] `company_context` pattern documented for Client (ZC-WISH / PROMPT_SETTINGS cross-link)  
- [ ] Gold: multi-entity / FK questions prefer find+link or traverse/walk over invent  
- [ ] Operators can point sales/docs at DESIGN §1 + foundation; chat_request stays short

### Why this also helps “faster” Zeus plans

| Effect | Mechanism |
| --- | --- |
| Fewer wrong first verbs | Access-class rule (fts → search, gsi → find, id → get) |
| Fewer join-blind pipelines | FK / inverse_fks / walk_paths as first-class in the story |
| Fewer invent rounds | “Absence ≠ invent” + emit-from-evidence |
| Not a free TTFT win | Single clean FTS round still pays the model floor (~3s) |

---

## Verb catalog clarity (base-5.2 review → base-5.3)

**Jira:** folds into **[CR-26](https://kotenai.atlassian.net/browse/CR-26)**  
**Reviewed:** 2026-07-26 · pack `v2/base/base-5.2/min/chat_request_*_base-5.2.json` (analytics representative)  
**SoT for behaviour:** Zeus [`docs/API/V2/*.md`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2) (`describe`, `get`, `find`, `traverse`, `search`, `analyze`, `explain`, `pipeline`, `return`, `transforms.md`)  
**Related:** § Getting skinny (diet / empirics) · § World model language (access path chooser in CORE)

### Verdict

base-5.2 tool surface is **uneven**. `search` and `return` teach well; most others are **cost tags + short labels** that do **not** encode the V2 docs’ “facts the LLM gets wrong constantly.” System essay partly compensates, but models weight **tool schemas** heavily — and several schemas **omit or contradict** real params (especially **order** vs system `direction`).

| Area | Grade (base-5.2) |
| --- | --- |
| `return` Layer A wording | Strong |
| `search` THINK line | Strong idea; schema incomplete vs examples |
| System efficiency / ranking prose | Partial; **order/direction bug** |
| Most tool `description`s | Too thin vs V2 |
| Param docs / demux completeness | Major gap |
| Transform verbs (`set`/`order`/`enrich`/`project`) | Under-taught pipeline glue |

### Cross-cutting issues

| Issue | Impact |
| --- | --- |
| Cost tags only (`[cheap]` / `[mod]` / `[exp]`) without when/when-not | Wrong first tool |
| Almost no param `description`s (except Layer A on `return`/`pipeline`) | Guessed `where` / `by` / `shape` |
| **System prose ≠ schema** | Ranking teaches `direction`; API uses `asc` + `field:<name>` |
| Examples only on `search` | Other demux verbs under-specified |
| Missing wire params that API accepts | `timeout_ms`/`where`/`seed_node_id` on search; `include` on describe; `asc`/`limit` on order; traverse shape knobs |
| Access-class chooser not on tools | Lives only weakly in system essay |
| `pipeline.steps` only types `as`+`verb` | Flexible bag; weak binding teaching |

### Description pattern (normative for base-5.3)

Every verb description:

```text
[cost] <what it does in one phrase>.
WHEN: …
WHEN NOT: …
KEY: <the V2 “LLM gets wrong” fact> …
```

| Target length | Verbs |
| --- | --- |
| ~80–160 chars | cheap transforms (`set`, `order`, `enrich`, `project`, thin `get`) |
| ~200–350 chars | demux / heavy (`find`, `search`, `traverse`, `pipeline`, `describe`, `analyze`) |

- Add **param `description`** on every non-obvious property (especially demux keys: `return`, `strategy`, `shape`, `by`, `include`, `job`).  
- Prefer **KEY constraints** over pasting full API pages into every description.  
- 1–2 `examples` on demux verbs when schema is non-obvious (keep total tools JSON honest vs base-5.2).

### Optional CORE one-liner (pairs with § World model language)

```text
Access path → verb
  exact id            → get
  equality / [gsi]    → find  (where equality only)
  language / text_fts → search (strategy:fts|hybrid)
  connected / hops    → traverse (or walk_path from WALK_PATHS)
  multi-step          → pipeline (bind @step.ids)
  final answer        → return OR terminating pipeline
  fresher inventory   → describe (only if brief/schema insufficient)
  corpus analytics    → analyze (heavy; may pending)
```

### Per-verb findings (base-5.2 → improve)

#### `describe` — weakest / most misleading

| Catalog (5.2) | V2 truth | Improve |
| --- | --- | --- |
| `[cheap] describe`; **empty params** | Companion to brief, **not replacement**; `include` defaults stats/entity_types/edge_types; metadata only | WHEN NOT inject green; add `include`; never returns rows |

Draft:

```text
[cheap] Scope orientation (stats/entity_types/edge_types). Use ONLY if SCOPE BRIEF /
MINI-SCHEMA missing or user asks for fresh inventory/indexes. Never a substitute for
inject; never returns node rows — use find/search for data. Optional include:
[stats|entity_types|edge_types|modes|tools|indexes] (default first three).
```

#### `get` — underspecified

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[cheap] exact by id` | Hydrate after find/search; ids 1..50; no `where` | Not a query; `include: body` opt-in; max 50 |

#### `find` — core verb, schema too thin (**P0**)

| Catalog | V2 | Improve |
| --- | --- | --- |
| predicate lookup + count/topK | **`return` is router**; `where` equality-only; MINI-SCHEMA authoritative | Desc + param docs; never text_fts in `where` |

Draft:

```text
[cheap] GSI/predicate anchor. return routes: rows|ids → find_nodes; count → count;
selectivity → entity_selectivity. where is EQUALITY-ONLY on MINI-SCHEMA [gsi]/scalar
paths — never text_fts (use search). Prefer return:ids then project/get.
entity_type = exact MINI-SCHEMA name.
```

#### `traverse` — router without map

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[mod] graph walk` | `shape` demux hop\|bfs\|path\|subgraph\|walk_path | Document shape + nested `walk_path`; seed from find/search first |

#### `search` — best description; schema lags examples (**P0**)

| Strength | Gap |
| --- | --- |
| THINK: fts vs find, entity_type exact, timeout | `timeout_ms`, `where`, `seed_node_id` in **examples** not **properties** |
| Strategy enum | Per-strategy required inputs (spatial → seed; hybrid → query_text) under-taught |
| | Spatial example may omit `entity_type` while schema requires it — align |

#### `analyze` — opaque job list

| Catalog | V2 | Improve |
| --- | --- | --- |
| `[exp] analytics job` | Offline-backed; **pending ≠ fail**; mode-gated | WHEN NOT ordinary Q&A; pending/mode notes; optional `params` object |

#### `explain` — almost empty

| Catalog | Improve |
| --- | --- |
| `planner pass-through` | WHEN: cost/debug before heavy plan; not end-user answer — or mark workbench-primary |

#### Transforms — pipeline glue under-taught (**order = P0**)

| Verb | Catalog | Real contract | Priority |
| --- | --- | --- | --- |
| `set` | set ops on ids | 2..8 lists; union\|intersect\|difference\|xor | P2 — compose prior step id lists |
| **`order`** | sort ids | `by`: `id` \| `created_at` \| **`field:<name>`**; **`asc` bool** (default true); `limit` | **P0** — system + example use **`direction`** (wrong) |
| `enrich` | decorate ids | attach fields; preserve rank/cardinality | P2 — vs project |
| `project` | shape rows | `fields` allow-list; optional `format` | P2 — final user-facing rows |

**Critical mismatch (fix in same train):**

```text
WRONG (base-5.2 system example / prose):
  order … by: "<field>", direction: "desc"

RIGHT (Zeus order tool / transforms.md):
  order … by: "field:abv", asc: false, limit: 10
```

#### `pipeline` — good terminate hook; weak step grammar

| Strength | Gap |
| --- | --- |
| Prefer multi-step; Layer A terminate | steps only `as`+`verb`; no `@step.ids` in tool desc |
| | `return[]` omit ⇒ last step only; no `abort_if_empty` / `narrow_to` in desc |

Draft:

```text
[mod] Preferred multi-step DAG (max 8). Bind prior ids as @step.ids (not bare @step).
Put terminating Layer A fields top-level (same as return) to end the turn in one round.
Typical: find|search → order → project. One scope only.
```

#### `return` — strongest Layer A teaching

Minor polish: prefer terminating pipeline when multi-step already planned; keep required four.

### Priority backlog (implement in base-5.3 packs)

| P | Change | Why |
| --- | --- | --- |
| **P0** | Align **order**: schema + system example (`field:<name>`, `asc`, not `direction`) | Prompt teaches wrong API |
| **P0** | **find** desc: equality-only `where` + MINI-SCHEMA + `return` router | Zero-row bugs |
| **P0** | **search** properties: `timeout_ms`, `where`, `seed_node_id` (match examples/API) | Schema lies about wire shape |
| **P1** | **describe** not replacement for brief; add `include` | Rediscovery habit |
| **P1** | **get** hydrate-not-query; body opt-in | Wrong first tool |
| **P1** | **traverse** shape demux + walk_path vs edges | FK vs graph confusion |
| **P1** | **pipeline** `@step.ids` + terminate top-level in desc | Binding errors |
| **P2** | **set / enrich / project** when-to-use vs each other | Pipeline quality |
| **P2** | **analyze** pending / mode-gated | False “broken job” |
| **P2** | **explain** purpose or workbench-primary note | Clarity |
| **P3** | 1–2 mini-examples per demux verb (keep size honest) | Few-shot without essay |

### Explicit non-goals (verb clarity)

- Deleting platform verbs or changing HTTP paths  
- Runtime strip of tools when inject green (still § Getting skinny law)  
- Duplicating full V2 pages into every `description`  
- Growing Layer A required fields while clarifying tools  
- Renaming verb names (stability law: same 13 names)

### Success signals

- [x] Findings written in ROADMAP (this section)  
- [x] P0 order/find/search fixed in base-5.3 packs + system examples  
- [x] P1 describe/get/traverse/pipeline desc+key params  
- [x] Diff base-5.2 → base-5.3 shows clearer tools (gold ranking deferred)  
- [x] Spot-check: no `direction` on `order` in any mode system text  
- [ ] Optional: gold cases for empty-where (text_fts mis-use) improve  

### Sequencing

```text
base-5.2 (current candidate)
    │
    ▼
base-5.3 content train (single pack bump preferred)
    ├── Verb clarity P0–P1  (this section)
    ├── World-model CORE blurb
    ├── Skinny prose / schema diet / empiric workflow docs
    └── (later) Hot Path A/B skinny stamps — not mid-session strip
```

Prefer **clarity before aggressive tool-count diet**: a wrong `order`/`where` costs more than an extra listed verb.

---

## base-5.3 — “Skinny + world-model + verb clarity” (content on base-5 wire)

**Jira:** **[CR-26](https://kotenai.atlassian.net/browse/CR-26)** · parent epic **CR-3**  
**SoT:** § Getting skinny · § World model language · § Verb catalog clarity · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · Hot Path / Prompt Helper  
**Upstream words:** [DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) §1 · §7.8 · §14 · [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md)  
**Upstream API:** Zeus [`docs/API/V2`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2)  
**Theme:** Cut **token weight** and **bad rediscovery habits**; teach **overlay + map + access class** in short CORE prose; **rewrite 13 verb descriptions/params** so they teach correct use; cut **tool membership** only via **new stamps** from run empirics.

| | |
| --- | --- |
| **Wire** | Same base-5 objects / required four / app_output |
| **Content** | World-model blurb · **verb clarity (P0–P1)** · no-rediscovery prose · schema diet · empiric skinny-pack docs |
| **Workbench** | Hot Path verb histogram; A/B full vs skinny **stamped** packs |
| **Not** | Runtime inject-green tool list mutation under contract enforcement |
| **On disk** | **`v2/base/base-5.3/`** full snapshot · parent `base-5.2` · Diff vs `base-5.2/` |

### Goals

1. Document **hashed tools[] law** (enforcement ⇒ no mid-session strip).  
2. **CORE world-model blurb** (DESIGN: AI-Ready overlay · MINI-SCHEMA shape · access path → verb · evidence-only Layer A).  
3. **Verb catalog clarity** — align descriptions/params with V2 API; fix order/search mismatches (§ Verb catalog clarity).  
4. Prose: prefer inject; `describe` is fallback / freshness, not default orientation.  
5. Verb schema diet — drop duplicate Terminate text; keep KEY constraints.  
6. Hot Path + Prompt Helper: never/rare/common over last N runs → A/B candidates.  
7. Optional skinny customs / arms as **re-stamped** experiments — promote when green.  
8. `company_context` recipe for tenant E–T–E (Client inject).  
9. Gold-set non-regression on required four; size targets in RELEASE_NOTES.

### Explicit non-goals for base-5.3

- Delete Zeus platform verbs or change HTTP paths  
- Client “if mini-schema then remove describe from tools[]” under enforcement  
- Rename/remove required four  
- Long ontology / REA lecture in system prompt  
- Soft HINTS-only latency plan without stamp workflow  
- Pin promote (**CR-18**) without Hot Path evidence for any skinny pin  

### Success signals

- [x] `v2/base/base-5.3/` scaffold + verify  
- [x] Diff base-5.2 → base-5.3 is content only (world-model + verb clarity + skinny diet)  
- [x] **P0:** order uses `field:` + `asc`; no system `direction`  
- [x] **P0:** find/search KEY constraints + search properties complete  
- [x] Contract/enforcement law called out in pack OVERVIEW  
- [x] CORE blurb present in all 10 modes; mode overlays still distinct  
- [x] PR #12 merged to main (2026-07-27) · pack train **closed**  
- [x] Hop `docs/migration/base-5.2_to_base-5.3/` + lessons-learned  
- [ ] Hot Path histogram path productized (residual → **ZE-267** / Workbench)  
- [ ] Gold set non-regression on live Zeus pin after vendor → 5.3  
- [x] CR-26 **pack acceptance Done** (Hot Path residual tracked outside pack Done)

---

## HINTS catalog (soft steer — base-6+)

**Jira:** epic **[CR-4](https://kotenai.atlassian.net/browse/CR-4)** · stories **CR-13**, **CR-14**  
**SoT playbook (recipes, multi-intent):** [BEST_PRACTICES.md](BEST_PRACTICES.md)  
**Assembly:** after hard `rules{}` · hash-excluded · must not erase jailbreak / company law  
**Related:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) § assembly zones · § Getting skinny (no runtime tools[] strip)

### Principle

```text
Rules / CORE     = what is always true (law + house style)
MINI-SCHEMA      = live map (authoritative shape)
hints.*          = given this scope / channel / arm / recent evidence,
                   which playbook bias applies THIS turn?
```

If a hint is true **every** turn for **every** tenant forever → promote to CORE or `rules{}`, do not leave as soft paste forever.

### Surfaces (do not collapse)

| Surface | Role | Mid-session change? |
| --- | --- | --- |
| Hard `rules{}` | Law | Frozen / append-only |
| CORE + verbs | Stable house style + tool keys | New BASE only |
| BRIEF / MINI-SCHEMA | Live map | Dirty when scope changes |
| **`hints.*`** | Soft bias (path, hot_path, multipart, A/B, budget, …) | **Yes** (hash-excluded) |

### Hint families (priority)

| Pri | Family | Example keys | Why |
| --- | --- | --- | --- |
| **P0** | **Path / recipe** | `hints.path.default_recipe`, `prefer[]`, `avoid[]` | Steer LOOKUP/TEXT/TOP_N/HOP without re-stamp |
| **P0** | **Field gotchas** | `hints.fields[]` (3–5 lines) | “description is text_fts → search”; `ex:` conventions |
| **P0** | **Multi-intent** | `hints.multipart.force_parts`, `max_parts`, `join_default`, `if_underspecified` | Paragraph users — **not** “switch mode to open” |
| **P1** | **Hot Path paste** | `hints.hot_path[]` named winning pipelines | Empiric per scope from Path Finder / books; **graduates to `named_query` rails** ([OPTIMIZATION.md](OPTIMIZATION.md)) |
| **P1** | **Negative / last-fail** | `hints.avoid_patterns[]` | Detective: don’t describe when inject green; no `direction` on order |
| **P2** | **Join bias** | `hints.join.prefer_edges`, `noise_floor`, `super_node_cap` | Soft echo of mode; engine mode remains hard for authz |
| **P2** | **A/B** | `hints.ab_arm`, `hints.ab_paste` | Experiments without thrashing `contract_hash` |
| **P2** | **Terminate soft** | `hints.terminate.soft_require`, `summary_style` | Extra G2/G3 nudge; required four stay catalog |
| **P2** | **Budget / channel** | `hints.budget.max_steps`, `search_timeout_ms`, `channel` | Voice / low-latency SKUs |
| **P3** | **Product / motion** | `hints.product.motion`, `default_limit` | Explore/compare/refine product chrome |
| **P3** | **Recovery** | `hints.recovery.last_error`, `try_next` | Session-only after tool fail |
| **P3** | **Playbook chip** | `hints.playbook_id` + params | Workbench chip → named recipe |

### Sketch shapes (Client inject — not hashed)

```text
hints:
  path:
    default_recipe: TEXT | LOOKUP | TOP_N | HOP | COMPOSE
    prefer: ["search→project"]
    avoid: ["describe first", "find where on text_fts"]
  fields:
    - "Beer.description is text_fts → search"
  multipart:
    force_parts: true
    max_parts: 4
    join_default: set_intersect | hop_fk | separate_answers
    if_underspecified: clarify
  hot_path:
    - name: fruit_beers
      when: "fruit|flavor"
      steps: [search fts → project]
  avoid_patterns: ["do not use direction on order"]
  join:
    prefer_edges: ["brewery_id"]
    noise_floor: 0.5
  ab_arm: "B"
  ab_paste: "Prefer hybrid over pure fts for description."
  terminate:
    soft_require: [policy_action]
    summary_style: "bullets per part when multi-intent"
  budget:
    prefer_one_pipeline: true
    max_steps: 5
    search_timeout_ms: 5000
  product:
    motion: explore | compare | refine
    channel: web | voice
```

Caps: soft ~1–2 KB inject; hard reject oversized pastes (PROMPT_SETTINGS security spirit).

### Explicit non-goals for hints

| Temptation | Better home |
| --- | --- |
| Jailbreak / never dump prompt | Hard `rules{}` |
| Required four | Catalog terminate (BASE) |
| Full mini-schema | Runtime inject |
| Permanent verb deletion same stamp | New skinny **stamped** pack (Hot Path A/B) |
| Company manifesto | `company_context` (word caps) |
| Always-on Helios JTBD/sentiment | Off-path / optional_when |
| “Long paragraph ⇒ mode=open” | [BEST_PRACTICES § multi-intent](BEST_PRACTICES.md) + `hints.multipart` |

### Multi-intent vs **open** mode (normative)

| Concern | Mechanism |
| --- | --- |
| User pastes a **paragraph** with several goals | Decompose → `query_decomposition.parts[]` → recipes → `set`/hop; optional `hints.multipart` |
| Product wants **serendipity / link maps / low floor** | Scope **mode = open** (+ optional looser `hints.join`) |
| Scope’s winning pipeline | `hints.hot_path` / `hints.path` from empirics |

**Open is not the multi-ask mode.** Multi-ask is planning; open is join/noise appetite ([BEST_PRACTICES.md](BEST_PRACTICES.md) · DESIGN §14.7).

### Success signals (hints)

- [x] BEST_PRACTICES playbook authored  
- [x] HINTS catalog written in ROADMAP (this section)  
- [x] **docs/HINTS.md** SoT + base-6 pack CORE note (pack train)  
- [ ] Client injects `hints.*` after `rules{}` (hash-excluded) — **ZC-WISH-040**  
- [ ] At least P0: path + fields + multipart live on one product path  
- [ ] Hot Path can emit `hints.hot_path` without re-stamp  
- [ ] A/B arm reported as cheap Client scalar  
- [ ] Jailbreak rules still present when ab_paste is set  

---

## base-6 — “Additive soft inject + optional Helios norms”

**Jira:** epic **[CR-4](https://kotenai.atlassian.net/browse/CR-4)** · stories **CR-13** (pack Done), **CR-14**, **CR-33** (Client inject), **CR-27…30** (base-6.1), **[CR-34](https://kotenai.atlassian.net/browse/CR-34)** (base-6.2 skinny) · epic **In Review** (pack green; residuals open).

**Theme:** **No breaking wire changes vs base-5.** Soft **`hints.*`** / A/B (hash-excluded); optional budget metrics; optional Helios norms as **cheap Zeus/Client** work — same spirit as Helios “nice to have.”  
**Depends on base-5:** frozen objects + company_context + settings/policy already ship (pack done; Client CR-20).  
**Prefer after base-5.3:** playbook + verb clarity landed in pack; soft injects should not re-bloat CORE — put steer in `hints.*`. A/B tool-set experiments stay **stamped arms**, not mid-turn tools[] edits.  
**End of base-6.x:** **§ base-6.2** content skinny (system + verb schemas; full-13) — diet the prefix **after** additive trains, before base-7 productization.  
**Detail:** **§ HINTS catalog** above · [BEST_PRACTICES.md](BEST_PRACTICES.md) · **§ base-6.1** · **§ base-6.2**

### Catalog / Client goals (all additive or optional)

1. **`wish_i_knew` hygiene** — already optional; shape/docs polish only.  
2. **G2 metrics hygiene** — never `summary`; dual path docs for `hooks_jailbreak_score` (base-5 already has dual scores).  
3. **Budget zone metrics (enforced reporting)** — size tags; caps already in base-5 design; **per-verb use rates** from Hot Path.  
4. **`hints.*` catalog (P0–P2)** — path/recipe, field gotchas, multipart, hot_path, avoid_patterns, join bias, ab_paste, terminate soft, budget — **after** hard `rules`; hash-excluded; must not strip jailbreak rules. See **§ HINTS catalog**.  
5. **Playbook excerpt in CORE (optional thin)** — recipes A–H one-screen; long form stays BEST_PRACTICES (prefer with verb description diet so pack KB does not only grow).  
6. **Optional** terminate retry (“required four only”).  
7. **De-demo** efficiency prose (residual after base-5.3).  
8. Customs filename smoke in scan + Client.  
9. **`ab_arm`** on report (cheap Client scalar) — slice by full vs skinny **stamp** and by soft ab_paste arm.  
10. **A/B stamped skinny packs** (fewer verbs or thinner schemas) promoted only after Hot Path + gold green — not runtime allowlists that unhash production.  
11. **`user` + `ip_address` emit** on session/turn report root (`zeus_client`|`zeus`|`helios`|`admin`; IPv4/IPv6 when known) — **ZC-WISH-035** · **§ Emit `user` + `ip_address` + `ai_process_result`**.  
12. **`ai_process_result`** Client setting (default **false**) — optional post-Zeus AI insight turn — **ZC-WISH-044**.  
13. **base-6.2 catalog prefix diet** (full-13) — collapse triple-teach Terminate × return × pipeline; Client stamp law out of CORE — **§ base-6.2** · **[CR-34](https://kotenai.atlassian.net/browse/CR-34)**.

### Helios goals (Pri-2/3 — optional / nice-to-have)

| Work | HEL-WISH | AI load |
| --- | --- | --- |
| `geo_norm` via Zeus geocode from QD `geo` | **001** | piggyback only |
| Client market geo | **002** | none |
| deployment / ruleset / mode / base_id slice | **016** | none |
| context dump metrics | **017** | none |
| multi_part normalize on Zeus | **012** | flag cheap |
| intent_norm map (Zeus first) | **005** | light if AI · optional_when |
| price_norm (Client slider preferred) | **004** | light if AI · optional_when |
| Tool fingerprint / chat recovery | **021, 020** | none |
| **`user` filter** (product vs Hub/admin) | **022** | none |

### Explicit non-goals for base-6

- **Any breaking rename/remove** of base-5 wire keys  
- Full wishlist as always-on Layer A  
- HEL-WISH-010 on hot path  
- Auto-ban on jailbreak float  
- “Must wait for base-6 to have company_context” (already base-5)  
- Encoding multi-intent as “force mode=open”  
- Jailbreak-only defense via `ab_paste` / hints  

### Success signals

- [x] Diff base-5.3 → base-6 shows **additive-only** (CORE soft-hints note; no Layer A rename)  
- [x] Pack `v2/base/base-6/` + hop + [HINTS.md](HINTS.md)  
- [x] lessons-learned / migration note  
- [x] BEST_PRACTICES ↔ hints.path recipe ids aligned in docs  
- [x] Design: **`user` + `ip_address` + `ai_process_result`** on ROADMAP + wishlists (**§ Emit `user` + `ip_address` + `ai_process_result`**)  
- [x] Design: **base-6.2 skinny prefix** on ROADMAP + **CR-34** (**§ base-6.2**)  
- [ ] Pack base-6.2 + verify + A/B (**CR-34** implement)  
- [ ] Client: `hints.*` after `rules{}`; hash-excluded; size caps (**ZC-WISH-040** · **CR-33**)  
- [ ] Client: stamp **`user`** + optional **`ip_address`** on report sinks (**ZC-WISH-035**); Helios filters **`user="zeus_client"`** (**HEL-WISH-022**)  
- [ ] Client: **`ai_process_result`** default false; insight-turn path (**ZC-WISH-044**)  
- [ ] P0 path + fields + multipart on one integration path  
- [ ] G2 metrics without UI leak  
- [ ] At least one `*_norm` path live without new **required** AI fields  

---

## base-7 — “Workbench + stamp + product events” (additive product)

**Jira:** epic **[CR-5](https://kotenai.atlassian.net/browse/CR-5)** · stories **CR-15**, **CR-16** · status To Do (future).

**Theme:** Productize authoring and ops; **no Layer A wire break** vs base-5. Helios product-path events remain optional/nice.

| Goal | Why | Breaking? |
| --- | --- | --- |
| Hub load/save base-N + custom rev | Customs lifecycle | No |
| Rules key/value editor + company_context word meter | Authors | No |
| Lint (rule length, dup keys, caps) | Catch bad packs | No |
| Preview assembled prompt + zone sizes | Debug | No |
| Prompt Helper A/B UI | Experiments | No |
| **Hot Paths → draft `named_query` rail** (Pachinko shaping) | End-goal Funnel optimization ([OPTIMIZATION.md](OPTIMIZATION.md)) | No |
| **Named rail hit rate / rounds-to-order** in Funnel ops | Helios + Hub | No |
| Stamp/verify for base-N | Real hashes | No |
| Detective: optional Layer A = **warn** not fail | Soften | No (softer) |
| COMPAT rows kept current | Versions | No |
| Compare / refine / demand events | HEL 018, 019, 011 | No (product) |

---

## base-8+ — “Pin + optional compression / AI-heavy”

**Jira:** epic **[CR-18](https://kotenai.atlassian.net/browse/CR-18)** — pin promote · **blocked by CR-20 + CR-21** · do not start until green.

| Idea | Why | Breaking wire? |
| --- | --- | --- |
| Promote base-N to `CURRENT` / `v2/min` | Users get diet | Pin gate only |
| **Mature named_query coverage** (top patterns = 1–2 hop rails; action rails e.g. book) | Pachinko stage 3 ([OPTIMIZATION.md](OPTIMIZATION.md)) | No (ops + PREPARED catalog) |
| Provider prompt-cache productization | Cost | No |
| Structured-output constrained `return` | Reliability | Optional path |
| Tool-history auto-summarize | Long sessions | No |
| TOON view for Workbench | Editor tokens | No (JSON SoT) |
| Per-mode default rule packs | Mode matrix | Additive packs |
| Soft AI JTBD/sentiment (**010**) | Insights | Off-path only |
| Constraints AI (006) if forms fail | Cost | Optional |
| Multimodal user parts | Product | Additive message parts |
| Require more Layer A fields | Quality | **Only with measured rates + new major if required** |

---

## Suggested sequencing (summary)

```text
base-4  Terminate table + Layer A scores (triggers still boolean[])
           │
base-5  ★ LAST BREAKING WIRE / CONTROL-PLANE FREEZE
        ★ rules{} + triggers{} (object-only; dual-read ≤1 Client release)
        ★ company_context + jailbreak pack + message_*
        ★ output_request (type+description) → app_output
        ★ settings bag + merge/freeze + policy table + hooks
        ★ inject security + multi-turn flags + cheap ops metrics
        ★ Helios Pri-1 = Zeus/Client emits only (nice spine, not Layer A tax)
           │
base-5.1 CONTENT on base-5 wire (not a wire break)
         ★ mode overlays in messages[].content (CORE + MODE_OVERLAY)
         ★ stop analytics×rename packs · DESIGN §14 personas
         ★ diff_modes / clone gate · Zeus modes/*.md port
           │
base-5.2 ADDITIVE G2 on base-5 wire
         ★ keep wish_i_knew (ops feedback)
         ★ append data_gaps (Helios schema/data/index acquisition)
           │
base-5.3 SKINNY + WORLD-MODEL + VERB CLARITY on base-5 wire
         ★ CORE blurb: AI-Ready overlay · MINI-SCHEMA shape · access path → verb
         ★ 13-verb desc/params aligned to docs/API/V2 (P0 order/find/search)
         ★ prose no-rediscovery · schema diet · measure AI floor
         ★ Hot Path verb histogram → A/B re-stamped skinny packs
         ★ never strip hashed tools[] mid-session under enforcement
         ★ company_context = tenant people/places/things + key links
           │
base-6+ ADDITIVE / OPTIONAL only
        soft hints.* after rules{} (path · hot_path · multipart · ab_paste · …)
        hot_path hints graduate → named_query rails (PREPARED fast-pass)
        optional norms · Workbench · pin when green
        Helios Funnel measures shaping (hops ↓, rail hit rate ↑)
        Helios nice-to-haves stay cheap providers · never re-break base-5 wire
        do not re-bloat Layer A; tool-set A/B stays stamped
        multi-intent = playbook + hints.multipart — NOT mode=open
        end-goal: shape funnel (Pachinko rails) — don’t shrink the box (not Path B2)
```

```text
Helios cost filter (every proposal):
  Can Zeus/Client emit it?  → do that (BASE guidance only if needed)
  Needs AI meaning?         → optional_when · never always-on hot path
  Needs dashboard GROUP BY? → precomputed scalar on report, not only arrays

Latency filter (every proposal):
  Does it cut rounds / rediscovery / completion tokens / schema bytes?
  Or only catalog quality?  → label it (quality ≠ wall-ms)
  Dropping verbs?           → new stamp / A/B arm, not runtime tools[] edit
  Inject green?             → prose + fix inject; do not unhash tools[]
```

---

## Why not dump Helios into base-5 Layer A

| Temptation | Why not |
| --- | --- |
| AI emits outcome.kind / path.stage | Zeus already knows — cheaper and exact |
| AI lat/lon | Geocode from free-text geo |
| Always-on sentiment/JTBD | Poisons Analytics; Pri 5 |
| Require price_norm every turn | Client slider; optional_when |
| Grow return schema for every HEL-WISH | Violates Helios §0 cost law |
| Put company manifesto / jailbreak law only in base-6 hints | Soft A/B can strip it — belongs in **base-5 rules + company_context** |
| Rely on `jail_break_attempt` without rules in the prompt | Score without policy ([JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)) |
| Keep `triggers[i]` forever | Opaque for Client/Helios — use **named keys** |
| Stuff app-specific fields into free-form system text | Use **`output_request.app.fields`** (`type` + `description`) → `app_output` |
| Type-only maps (`sum_favorites: "INT"`) | Model needs a **description** instruction in the prompt |
| Bury max_rounds / verb deny only in system essays | Use **settings bag** |
| Trust model triggers as final law | **Client policy table + hooks** |
| Soft A/B paste as only jailbreak defense | Hard **rules{}** in base-5 first |
| Log full prompts with PII by default | Zone sizes + redaction settings |
| Always pin full 13 without looking at Hot Path | Empirics → A/B skinny **stamp**; platform still has 13 ([§ Getting skinny](#getting-skinny--latency--verb-surface-plan)) |
| Strip `describe` from tools[] when mini-schema arrives | **Breaks contract enforcement** — same stamp must keep tools[]; fix inject + prose, or re-stamp a skinny pack |
| Call `describe` when MINI-SCHEMA is already injected | Inject is authoritative; `describe` is fallback / refresh only (tool may still be listed) |
| Expect base bumps alone to drop AI wall ms | Measure tokens/rounds/verb rates; model floor is real |
| Teach data access as “fill the form / invent columns” | DESIGN: **AI-Ready overlay + mini-schema shape + access class** ([§ World model language](#world-model-language-for-chat_request-design-vocabulary)) |
| Paste DESIGN.md / foundation essay into system prompt | Short CORE blurb + `company_context` + live inject |
| Cost-tag-only tool descriptions (`[cheap] describe`) | WHEN / WHEN NOT / KEY per verb ([§ Verb catalog clarity](#verb-catalog-clarity-base-52-review--base-53)) |
| System `order` with `direction` / bare field name | Zeus: `by: "field:<name>"`, `asc: false` |

base-4 already has the **AI meaning** slots (QD facets + recommended G2/G3; triggers still arrays).  
base-5 puts **company + named rules + control plane** in product.  
base-5.3 makes **skinny + world-model language + honest latency** first-class.  
Helios volume is **report/session scalars**.

---

## Cross-cutting principles (every BASE)

1. **One Terminate surface** — extend the table; no second essay.  
2. **base-5 = last break; base-5.x content/skinny; base-6+ = additive/optional only** — until a new major is justified.  
3. **Platform keeps the same 13 verb names** until a major Zeus API train; **product pins use stamped tools[]** — subset only via **new hash / A/B pack**, never mid-session strip under enforcement ([§ Getting skinny](#getting-skinny--latency--verb-surface-plan)).  
4. **One inspector** — Diff is the migration test.  
5. **Text for diet, JSON for ship.**  
6. **Helios: cheap provider first; nice-to-have never blocks pin.**  
7. **Sparse AI + true-only exceptions** (HEL-WISH-012).  
8. **Pin last.**  
9. **Settings ≠ prompt essays** — structured control plane ([PROMPT_SETTINGS.md](PROMPT_SETTINGS.md)).  
10. **Triggers = signals; Client policy + hooks = law.**  
11. **Hard rules before soft hints** (base-5 freeze; base-6+ soft only).  
12. **Ownership is explicit** — App / Client / AI set·unset·change ([BIBLE §2](BIBLE.md)).  
13. **Tool results are untrusted data** in the prompt.  
14. **Any base-6+ wire break** needs a new major BASE + `docs/migration/base-X_to_base-Y/` — **default is no**.  
15. **Inject green ⇒ no rediscovery habit** — SCOPE BRIEF + MINI-SCHEMA beat calling `describe` / list_* / get_stats; still **do not unhash tools[]** to force that.  
16. **Latency: measure AI floor** — rounds, **per-verb use**, rediscovery, tokens, `ai_ms`; catalog quality trains are not automatic wall-ms wins.  
17. **Skinny before soft bloat** — prefer base-5.3 prose/schema + empiric stamps before base-6 hints that re-grow the prompt.  
18. **Drop verbs via Hot Path → A/B stamp → pin** — Prompt Helper and Workbench own the experiment loop; production enforcement stays honest.  
19. **World model in front of the model** — chat_request teaches overlay + map + access class (DESIGN); Layer A is emit-from-evidence, not form-fill over empty slots.  
20. **Tenant texture in `company_context`** — durable entities + key links/events; not a second giant system essay.  
21. **Tool schemas match Zeus V2** — descriptions teach WHEN/KEY; param lists match dispatch (no prompt/`direction` vs API/`asc` drift).  
22. **Rule placement is explicit** — CORE / MODE / BP / OPT / hints / Client ([PROMPT_RULE_PLACEMENT.md](PROMPT_RULE_PLACEMENT.md)); looser modes change flavor, not Layer A wire.

---

## Open questions

1. Text pack review-only vs text→JSON import?  
2. `policy_action` required in tool schema or docs/tests only?  
3. Who owns Client spike (named triggers + `output_request` + settings bag + policy table + 007/009)?  
4. Who owns Zeus spike (003/014) vs this repo’s catalog docs?  
5. Max min-profile catalog KB?  
6. ~~When does `COMPAT.md` gain base-4/5 rows?~~ → **Done** (see [COMPAT.md](../COMPAT.md)); keep Client TBD floors updated  

7. Closed enums for `path.stage` / `intent_norm` — registry owner? (Helios §9)  
8. company_context: hard-truncate at 250 words in Client, or reject save in Workbench?  
9. A/B: one `ab_paste` slot vs named arms `ab.A` / `ab.B` in the paste UI?  
10. Jailbreak default `rules` object: ship as Client SDK defaults, Workbench template, or both?  
11. ~~Array→object dual-read: one release or two?~~ → **≤1 Client release, prefer 0**; objects only after  
12. `output_request` / settings API: top-level `run_agent(...)` kwargs vs nested only?  
13. Cap on `app_output` properties: 8 soft / 15 hard — enough?  
13b. Description soft max ~40 words / hard ~80 — enough for integrators?  
13c. Shorthand API: reject type-only vs require parallel `descriptions` map?  
14. Sticky flags: OR across session for all keys, or only business keys (jailbreak per-round)?  
15. `ruleset_id`: content hash vs Workbench version string?  
16. Force final `return`: always at `max_rounds-1`, or only after tool data exists?  
17. Frozen session prefix vs full re-assemble as Client v1 default?  
18. Any proposed base-6+ **breaking** change — force new major BASE? (**default yes**)  
19. **Skinny packs:** separate base-5.3-full pin vs optional customs, or only A/B arms until promote?  
20. **`traverse` / `explain` drop thresholds** from Hot Path (e.g. &lt;1% of runs in last 500)?  
21. ~~**Inject-green omit `describe` from tools[]?**~~ → **No under enforcement** — prose + inject fix; drop only in a **new stamp**. Safety `denied_verbs` after the fact is not a substitute for skinny stamp design.  
22. **Skinny size targets:** hard cap on verbs JSON chars / system chars per mode?  
23. Spin **docs/SKINNY.md** out of ROADMAP when base-5.3 implements, or keep single SoT here?  
24. Hot Path window defaults: last 100 / 500 / 7d runs — product owner?  
25. World-model blurb hard cap: 120 vs 180 words — enough for access-class rules?  
26. Put access-class cheat on every mode overlay, or only CORE once?  
27. Verb clarity: hard cap per-description chars vs quality of KEY lines?  
28. Ship P0 order/find/search in a hotfix on base-5.2 customs before full base-5.3 pack?  
29. Hints soft max KB / hard reject size — 1 KB / 2 KB enough?  
30. `hints.multipart` Client-default on for analytics product, or opt-in per App?  
31. Hot Path → `hints.hot_path` automatic inject vs operator paste only?

---

## Doc ownership

| Doc | Role |
| --- | --- |
| [HELIOS_WISHLIST_FOR_CHAT_REQUEST.md](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) | Structured Helios Requests + priorities |
| [ROADMAP.md](ROADMAP.md) | BASE sequencing + Helios + **skinny** + **world-model language** + **verb catalog clarity** |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | Retrieval playbook (single-focus + multi-intent; mode bias; open ≠ multi-ask) |
| [OPTIMIZATION.md](OPTIMIZATION.md) | End-goal fine-tuning: Pachinko → `named_query` (SQL++ PREPARED) rails · Funnel |
| ROADMAP **§ HINTS catalog** | Soft `hints.*` families + assembly law (base-6 / CR-4) |
| [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) | Named rules/triggers + Client `output_request` |
| [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) | Settings · merge · Client policy · cache · security · **verb allow/deny** · company_context |
| [zeus_design_docs DESIGN.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) | Zeus architecture — overlay · tools · mini-schema §7.8 · modes §14 |
| [ENTITY_TRANSACTION_ENTITY_FOUNDATION.md](https://github.com/fujio-turner/zeus_design_docs/blob/main/ENTITY_TRANSACTION_ENTITY_FOUNDATION.md) | E–T–E / schema-as-world-model storytelling SoT |
| Zeus [`docs/API/V2`](https://github.com/Fujio-Turner/Zeus/tree/main/docs/API/V2) | Per-verb behaviour SoT for catalog descriptions |
| [CREATE_BASE.md](CREATE_BASE.md) | Scaffold new base-N pack (`scripts/new_base.py`) |
| [COMPAT.md](../COMPAT.md) | Zeus × chat_request BASE × zeus_client matrix |
| [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) | Wire order + budgets |
| [BIBLE.md](BIBLE.md) | Normative base-4 + §2 ownership |
| [RELEASE_NOTES.md](../RELEASE_NOTES.md) | What shipped + **breaking changes** |
| [migration/README.md](migration/README.md) | All BASE hops `base-X_to_base-Y` |
| [BASE_AGENT_PLAYBOOK.md](BASE_AGENT_PLAYBOOK.md) | AI comply / upgrade procedures |
| [../AGENTS.md](../AGENTS.md) | Repo AI entry |
| [migration/base-1_to_base-4/lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md) | Experience (1→4 hop) |
| [migration/base-5_to_base-5.2/lessons-learned.md](migration/base-5_to_base-5.2/lessons-learned.md) | Experience (5→5.2 hop) |

---

*Align with Helios wishlist when HEL-WISH IDs change; revise BASE section when base-5 starts. Control-plane detail lives in PROMPT_SETTINGS.md. Latency / verb-surface detail lives in § Getting skinny. DESIGN vocabulary for catalog prose lives in § World model language. Per-tool description backlog lives in § Verb catalog clarity (base-5.3).*
