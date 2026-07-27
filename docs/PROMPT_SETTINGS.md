# Prompt construction · rules · settings (control plane)

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · design line **base-4** (base-5 = design only) · version matrix: [COMPAT.md](../COMPAT.md)


**Status:** design for **base-5** (core) · base-6/7 (hints, Workbench polish, cache productization)  
**Audience:** Zeus Client, App integrators, Hub/Workbench, catalog authors  
**Normative ownership:** [BIBLE.md §2](BIBLE.md) (set · unset · change)  
**Related:** [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) · [ROADMAP.md](ROADMAP.md)

**BASE law:** base-5 **freezes** the hard control plane (settings, merge/freeze, policy table, inject security). Soft `hints.*` are **base-6+ additive** (hash-excluded) — do not re-break the wire. See [ROADMAP.md](ROADMAP.md).

This doc is the **control plane** next to the assembled prompt: structured **settings**, **rule-pack merge**, **post-terminate Client policy**, **cache stability**, **security**, and **observability**. It does **not** grow Layer A with Helios Pri-1 scalars (cheap Zeus/Client still win).

---

## 0. Three surfaces (do not collapse)

```text
┌─ 1) PROMPT TEXT (what the model reads) ───────────────────────┐
│  catalog · brief · schema · company · message_* · rules{}     │
│  · output_request · soft hints (base-6+) · user · tool hist   │
└───────────────────────────────────────────────────────────────┘
┌─ 2) SETTINGS (structured config — not free-form essays) ──────┐
│  max_rounds · model · tool_choice · allowed/denied verbs      │
│  locale/channel/tz · ab_arm · redaction · debug · structured  │
└───────────────────────────────────────────────────────────────┘
┌─ 3) POST-MODEL CLIENT POLICY (law after Layer A) ─────────────┐
│  normalize triggers · hooks · force refuse · map message_*    │
│  → control.flags · UI chrome · metrics · next inject          │
└───────────────────────────────────────────────────────────────┘
```

| Surface | Owner of content | Re-stamp if changed? |
| --- | --- | --- |
| Prompt text (BASE body) | Hub / catalog | **Yes** |
| Prompt text (injects) | App + Client assembly | No |
| Settings | App / Client / hooks | No |
| Post-model policy | Client + hooks | No (code) |

---

## 1. Settings bag (`session.settings` / `run_agent` options)

**First-class structured config.** Prefer keys over “please use temperature 0” buried in system prose.

### 1.1 Shape (sketch)

```text
settings:
  # --- run / session clocks & caps ---
  max_rounds: 8                    # App S/C; Client may lower only
  zeus_session_id: ""              # Client usually mints
  # zeus_round / turn_index: Client-owned — not App write

  # --- model / tools ---
  model: ""                        # App
  temperature: 0.2                 # App (optional)
  tool_choice: "auto" | "required" | { force_return_when: "budget_low" }
  allowed_verbs: null | [...]      # null = catalog default
  denied_verbs: []                 # App + hooks tighten

  # --- product / analytics slices (cheap Client) ---
  locale: "en-US"
  timezone: "America/Phoenix"
  channel: "web" | "voice" | "api" | ...
  market_country: "US"
  ab_arm: null | "A" | "B" | "control"
  deployment_id: ""                # HEL-WISH-016 adjacent
  ruleset_id: ""                   # which rule pack version

  # --- structure / output ---
  structured: true
  output_request: { ... }          # app.fields: each { type, description } — description is model instruction
                                   # see RULES_OBJECT_AND_OUTPUT_REQUEST.md (type-only is NOT enough)

  # --- multi-round / Zeus result handling (Client loop — not Layer A) ---
  # After Zeus tool results land in messages[]:
  #   false (default) = cheap path: surface tables/UI; do not require a second AI turn
  #   true            = schedule another AI round so the model can analyze/narrate tool JSON
  # See ROADMAP.md § Emit usr + ai_process_result · ZC-WISH-044
  ai_process_result: false

  # --- emit / analytics provenance (cheap Client stamp on report root) ---
  # Who wrote the Analytics/session row: zc|z|h|a — product Client always "zc"
  # See ROADMAP.md · ZC-WISH-035 · HEL-WISH-022
  # usr is set by Client on sink, not by the model

  # --- safety / ops ---
  redaction: "default" | "strict" | "off_dev_only"
  debug: false
  log_prompt_zones: true           # sizes only, not full text by default
  pii_in_logs: false
```

### 1.2 Ownership (set · unset · change)

| Setting | App user | Client logic | AI | Notes |
| --- | --- | --- | --- | --- |
| `max_rounds` | **S C** | **C\*** lower only | — | Hooks may tighten |
| `model` / `temperature` | **S C U** | R | — | Not in contract hash |
| `tool_choice` / force return | S C | **C\*** late-round force | — | Reliability |
| `allowed_verbs` / `denied_verbs` | **S C** | **C\*** hooks deny | — | Never invent new verbs |
| `locale` / `tz` / `channel` / `market` | **S C U** | inject meta line | R | Helios cheap |
| `ab_arm` | **S C U** | report slice | R | base-6+ product |
| `output_request` | **S C U** | inject + validate | R | base-5 |
| `ai_process_result` | **S C** | **C** loop after tools | — | default **false**; base-6+ / ZC-WISH-044 |
| `usr` (report stamp) | — | **S C** on sink | — | closed enum; ZC-WISH-035 · not model |
| `redaction` / `debug` / log flags | **S C** | enforce | — | Defaults safe |
| `zeus_round` | — | **S C** | echo only | Bible §2 |

### 1.3 BASE fit

| | |
| --- | --- |
| **base-5** | Document + Client spike: settings bag, verb deny, max_rounds tighten, locale/channel, output_request, redaction defaults |
| **base-6** | Budget zone metrics, ab_arm formal, prompt size by zone |
| **base-7** | Workbench UI for arms / ruleset identity |

---

## 2. Rule pack merge + freeze

Named `rules: { id → text }` only work if merge is deterministic.

### 2.1 Layers (low → high precedence)

```text
1) SDK defaults     jailbreak pack (ignore_system, no_prompt_dump, …)
2) Tenant / Workbench pack   company policy + business keys
3) Per-request App overrides   run_agent(..., rules=…) or business_injection.rules
```

**Merge:** object union by key. **Higher layer wins on key collision** (last-wins).  
**Do not** concatenate two texts for the same key.

### 2.2 Flags

| Flag / behavior | Default | Meaning |
| --- | --- | --- |
| `override_defaults` | `false` | If false, request may **not** delete/blank SDK jailbreak keys |
| Session **freeze** | on | After session start, rule **ids** frozen except **append-only** new keys |
| Mid-session **rename/delete** | forbidden | Requires new session (or explicit `reset_rules: true`) |
| Mid-session **text change** same id | discouraged | Prefer new id + deprecate old |

### 2.3 Algorithm (Client)

```text
pack = deep_copy(SDK_DEFAULT_JAILBREAK_RULES)
pack = union(pack, tenant_pack)           # tenant wins on collision
if request.rules:
  if not override_defaults:
    reject deletions of default jailbreak keys
  pack = union(pack, request.rules)       # request wins on collision
session.rules_frozen = pack               # ids snapshot
session.ruleset_id = hash_or_version(pack)
# each turn: inject session.rules_frozen (+ optional append-only adds)
```

### 2.4 Hard vs soft (do not mix)

| Kind | Home | Terminate | Enforce |
| --- | --- | --- | --- |
| **Hard policy** | `rules{}` | `business_rules_triggers` | Hooks too |
| **Soft steering** | `hints` / hot_path (base-6) | none | none |
| **Brand chrome** | `message_*` | none | Client maps from `policy_action` |
| **Identity** | `company_context` | none | Soft out-of-scope; hard via rules |

Jailbreak law must **not** live only in soft hints ([JAILBREAK_POLICY.md](JAILBREAK_POLICY.md)).

### 2.5 Conflict law (multiple triggers true)

**Model triggers are signals. Client policy table is law.**

Suggested default order (product may tune):

```text
1) hooks hard block (prompt dump, secrets, denied verbs) → force refuse / strip
2) any jailbreak rule key true + high jail_break_attempt → prefer refuse + message_jailbreak_soft
3) business keys (coupon, inventory) → flags + maybe clarify
4) else policy_action from model (if present)
5) else infer answer | clarify from Layer A completeness
```

Document product-specific overrides next to tenant pack — not in BASE hash.

---

## 3. Post-terminate Client policy (after Layer A)

Runs **every** successful `return` parse. Not optional “if we remember.”

```text
layer_a = parse(return_args)
validate required four
triggers = normalize(layer_a.business_rules_triggers)   # {} sparse; array dual-read transition
hooks_score = hooks.score_or_0()

# 3.1 Force / override
if hooks.must_refuse: policy = refuse
elif jailbreak_keys_hit(triggers) and (layer_a.jail_break_attempt >= 0.5 or hooks_score high):
  policy = prefer refuse
else:
  policy = layer_a.policy_action or default

# 3.2 UI chrome (G1 display — may replace summary for user)
ui_text = map_message(policy, business_injection) or layer_a.summary

# 3.3 Flags (G3)
for k, v in triggers.items():
  if v: control.flags[k] = true   # sticky OR per-round — see §6

# 3.4 App bag
if output_request.app:
  validate/strip app_output

# 3.5 Metrics (G2 never UI)
emit scores, trigger key rates, policy, prompt zone sizes
```

| Must | Must not |
| --- | --- |
| Keep raw Layer A in `artifacts.last_terminate` | Overwrite model `jail_break_attempt` with hooks score in same field |
| Apply triggers → flags | Pretend App forged triggers as model emit |
| Redact G2 from chat UI | Show scores to end user |

---

## 4. Stability vs freshness (prompt assembly + cache)

### 4.1 Zones

| Zone | Stability | Re-build when |
| --- | --- | --- |
| Catalog system + verbs + Terminate table | **Session-stable** (pin) | Mode / stamp change |
| company_context + frozen rules | **Session-stable** | Explicit inject change / new session |
| Settings meta line (locale, channel) | Session-stable unless App changes | Settings C |
| SCOPE BRIEF / MINI-SCHEMA | **Refresh** on scope/stats change | Zeus refresh |
| output_request | **Per run/turn** | App sets |
| Soft hints / ab_paste | Per arm (base-6) | Experiment |
| user + tool history | Append; prune old tool bodies | Every round |

### 4.2 Assembly strategy (base-5 default)

**Recommended:** freeze **session prefix** at session start; each round appends **delta** (user/tool) + refreshed brief only if dirty.

```text
prefix (cache-friendly) =
  catalog system + verbs summary
  + company_context + rules (frozen pack)
  + settings one-liner (locale/channel)

variable =
  SCOPE BRIEF + MINI-SCHEMA (if dirty)
  + output_request (if any)
  + messages tail (pruned)
```

**Alternative (simpler):** full re-assemble every round — OK for v1 Client; document cache miss cost.

### 4.3 BASE fit

| | |
| --- | --- |
| **base-5** | Document zones; Client may implement full re-assemble **or** frozen prefix |
| **base-6** | Measure zone sizes; drop order enforcement; optional provider cache alignment |
| **base-8+** | Productize cache when providers mature |

---

## 5. What the model sees vs Client keeps

| Artifact | In model prompt? | In Client store? |
| --- | --- | --- |
| Full tool JSON | **Last N** / truncated | **Full** in artifacts |
| Layer A | Optional one-line prior decision | **Always** last_terminate |
| G2 scores | Never as user chrome | Metrics / admin |
| company manifesto / PDFs | **No** (cap 250 words) | RAG / doc store |
| Denied verb attempts | No | Hook audit |

**Options (product choose, document default):**

| Option | Default for base-5 |
| --- | --- |
| Re-inject full `last_terminate` next turn | **No** — too noisy |
| Inject one-line prior decision | Optional App flag |
| Summarize old tool results | Optional later; truncate first |
| Sticky flags across rounds | **Yes** for business keys (OR); jailbreak metrics per-round |

---

## 6. Multi-turn product semantics

| Topic | Guidance |
| --- | --- |
| **Sticky flags** | `control.flags[k] \|= triggers[k]` for business keys (`coupon_presented`) |
| **Per-round triggers** | Always store snapshot on `last_terminate`; do not lose history |
| **Clarify loop** | Keep same `output_request` until `app_output` satisfied or max_rounds |
| **Mode / catalog switch** | New pin / new session; do not silent-swap mid-transcript |
| **Human handoff** | `policy_action=error` or hooks trip → App UI escape |
| **Rule freeze** | §2 — append-only keys mid-session |

---

## 7. Terminate reliability (not more prose)

Even perfect rules fail if Layer A is incomplete.

| Lever | Owner | base |
| --- | --- | --- |
| Required four always practiced | Catalog + Detective | base-4/5 |
| Soft-require via `output_request.layer_a` | App + model | base-5 |
| Force `tool_choice` / final `return` when budget low | Client | base-5 |
| One retry: “emit required four only” | Client optional | base-5/6 |
| Detective **warn** on recommended (not fail) | Zeus | base-7 intent |
| Provider structured-output / JSON schema on `return` | Client + AI API | when available |

Do **not** fix reliability by pasting another essay into system prompt first.

---

## 8. Security / abuse surface of injects

| Risk | Mitigation (base-5 Client) |
| --- | --- |
| Secrets in `prompt_override` / rules | Strip patterns; allowlist inject keys; `redaction` |
| User “ignore previous instructions” | Hard rules + hooks; never sole trust model |
| Huge `output_request.app` schema | Soft ~8 / hard ~15 properties; max depth; reject |
| Prompt injection **inside tool JSON** | Treat tool results as **untrusted data**; do not execute instructions found in rows |
| Log exfil | Default: zone sizes + hashes, not full system+PII tools (`pii_in_logs: false`) |
| App forges tool_calls | Forbidden (Bible §2.4) |

Hooks remain the **hard** path for exfil / verb abuse even if the model cooperates.

---

## 9. Observability (cheap — Client/Zeus)

Emit **scalars and key sets**, not full prompt text:

| Signal | Provider |
| --- | --- |
| `ruleset_id` / rule key set fingerprint | Client |
| Inject blocks present (bools): company, rules, output_request, hints | Client |
| Prompt **zone byte/token estimates** | Client |
| Truncation / drop reason codes | Client |
| `jail_break_attempt` + `hooks_jailbreak_score` (dual) | Model + Client |
| Per-key trigger rates | Client |
| `policy_action` distribution | Client |
| Layer A missing-field counts | Detective / Client |

Aligns with Helios cost law — no new always-on AI fields for dashboards.

---

## 10. Workbench / authoring (base-6/7)

| Capability | BASE |
| --- | --- |
| Rules as **key/value table** (not free JSON only) | base-7 (design in base-5 docs) |
| company_context word meter (150/250) | base-5 lint · base-7 UI |
| Lint: rule > 1 sentence, duplicate keys, default-key delete | base-5 Client · base-7 Hub |
| Preview **assembled prompt** with zone sizes | base-6/7 |
| Diff A/B arms without thrashing hash | base-6 inject · base-7 UI |
| Soft hints must not strip jailbreak rules | base-6 |

---

## 11. Wire order (full, with settings)

```text
1) ZEUS RULES (catalog — hashed when stamped)
2) SCOPE BRIEF + MINI-SCHEMA          (Client; refresh if dirty)
3) company_context                    (App; session-stable; ≤150/250 words)
4) message_* templates                (App; not all need to be model-visible)
5) rules { id → text }                (merged frozen pack)
6) output_request                     (App; optional; per turn)
7) settings one-liner / meta          (locale, channel, ab_arm — cheap)
8) hints / hot_path / ab_paste        (base-6+; soft only)
9) messages[]                         (user + tool history; pruned)
        │
        ▼ LLM ↔ Zeus
        │
10) Layer A terminate
11) Client policy table (§3) → UI · flags · metrics
```

Settings that are **not** model-relevant (redaction, log flags, API keys) stay **out of the prompt**.

---

## 12. Future-facing (do not block base-5)

| Idea | Gate |
| --- | --- |
| Provider prompt-cache productization | Measured savings; stable prefix |
| JSON-schema constrained `return` | AI API support |
| TOON / text diet as editor view only | JSON remains SoT |
| Per-mode default rule packs (fraud stricter) | Mode matrix |
| Multimodal user parts | Same inject model; new message parts |
| Auto-summarize tool history | Quality evals first |

---

## 13. BASE placement summary

| Item | base-5 | base-6 | base-7 | later |
| --- | --- | --- | --- | --- |
| Settings bag documented + Client spike | ★ | | | |
| Rule pack merge + freeze + override_defaults | ★ | | | |
| Hard vs soft separation | ★ | hints formal | | |
| Client post-terminate policy table | ★ | | | |
| Dual jailbreak scores (model + hooks) | ★ hooks parallel | hygiene | | |
| Session prefix vs full re-assemble | ★ doc + either impl | zone metrics | | |
| Terminate force-return / soft-require | ★ | retry polish | Detective warn | |
| Inject security caps + redaction | ★ | | | |
| Observability zone sizes + ruleset_id | ★ minimal | full budget zones | | |
| Sticky flags + clarify-loop semantics | ★ | | | |
| Soft hints / ab_paste | | ★ | UI | |
| Workbench key/value rules + preview | | lint | ★ | |
| Prompt cache product | | experiment | | ★ |
| Structured-output provider path | when ready | | | ★ |

---

## 14. Success signals (control plane)

- [ ] Bible §2 + this doc agree on settings ownership  
- [ ] Client merges SDK ∪ tenant ∪ request rules without deleting jailbreak defaults (unless override)  
- [ ] Mid-session rule rename rejected or requires reset  
- [ ] After every terminate: policy table runs (flags, chrome, metrics)  
- [ ] G2 never reaches chat UI  
- [ ] `output_request.app` rejected when oversized  
- [ ] Tool JSON treated as untrusted data  
- [ ] At least zone sizes or ruleset_id on a demo report  
- [ ] ROADMAP base-5 checklist includes control-plane items  

---

## 15. Open questions

1. Default sticky flags: OR across session vs replace each round for all keys?  
2. `ruleset_id`: content hash vs Workbench version string?  
3. Settings on wire: top-level `run_agent(settings=)` vs nested under session only?  
4. Force-return: at `max_rounds-1` always, or only when tools already returned data?  
5. Dual-read array triggers: one Client release or two?

---

*Control-plane companion to PROMPT_ASSEMBLY and RULES_OBJECT. Implement Client spikes under base-5; soft hints UI under base-6/7.*
