# Understanding `chat_request*.json`

**Platform docs (published):** [https://docs.koten.ai/](https://docs.koten.ai/)  
*(site may still be a placeholder while GitBook is wired)*

This document explains what a **chat_request** file is, what each part does, what a **contract** is, when you may change things, and where refinement actually happens (**Zeus Hub → Workbench**).

Files in this repo (`v2/min/chat_request_*_v2_min.json`) are **baseline templates** — starting points for modes (analytics, code, tenant, …), not final production catalogs for your data.

---

## What is a chat_request?

A **chat_request** is the **LLM-facing catalog** Zeus (and Zeus Client) uses for one agent turn (or session):

- Which **tools / verbs** the model is allowed to call  
- How it should **behave** (system instructions, routing, response shape)  
- Optional **guidance** for your business (injections, optimal paths, decomposition)  
- A **contract** binding so production stays auditable and drift-resistant  

Think of it as the **menu + house rules** the model sees when talking to your operational data through Zeus.

```text
User question (advice-shaped)
        │
        ▼
  Zeus Client (middleman)
        │  loads chat_request (catalog)
        │  binds contract_id + contract_hash
        ├──► LLM   (plans tools using verbs + instructions)
        └──► Zeus  (executes verbs against live data)
```

Without a catalog, the model has no governed tool surface (or falls back to inventing unsafe behavior). With a **stamped** catalog, “help” stays within **your** allowed verbs and policy.

---

## Baseline vs your dataset

| Kind | Where | Role |
| --- | --- | --- |
| **Baseline** (this repo) | `v2/min/chat_request_<mode>_v2_min.json` | Generic **mode** templates (analytics, fraud, tenant, …). Good for demos, scaffolds, MCP fallbacks. |
| **Engine full snapshots** | Zeus repo `ai/V2/chat_request_*_v2.json` | Generated full profiles for Hub / A/B (larger than min). |
| **Your refined catalog** | **Zeus Hub → Workbench** | Tuned for **your** bucket/scope, entity map, business language, and stamped for production. |

**Important**

- This repo = **baseline\*** (portable starting point).  
- **Hub Workbench** = where you **refine for your data set** (scope brief, guidance, verb emphasis, business injections).  
- **Stamp / verify on Zeus** = what production clients must bind.  

Do **not** treat a baseline file from GitHub as “already stamped for my cluster.”

---

## Anatomy of a chat_request (V2)

Standard format: `_format: "zeus.chat_request.v2"`.

### Full shape (engine / Workbench)

| Section | Purpose | In hash? |
| --- | --- | --- |
| **`_format` / `_version`** | Envelope identity | Metadata / policy |
| **`_hash_policy`** | What is included vs excluded when hashing | Defines contract fingerprint rules |
| **`instructions`** | System behavior: `system_prompt`, verb usage guide, order, response expectations | **Yes** (core rules) |
| **`masq`** | Cost / tier model for verbs | **Yes** |
| **`verbs`** | OpenAI-style tool definitions the model may call (`describe`, `find`, `search`, `pipeline`, `return`, …) | **Yes** |
| **`messages`** | Portable message list (often system prompt mirrored for compatibility) | **Yes** (content) |
| **`guidance`** | Advisory: injections, optimal paths, query/data decomposition, debug, assembler hints | **No** (excluded from hash) |
| **`contract`** | Stamp metadata: id, name, hash, scope, builder, timestamps | **No** (excluded; hash is the result of stamping) |
| **`metadata`** | Generation notes, mode label, etc. | **No** |

### Min profile (this repo)

`*_v2_min.json` trims bulky guidance/instructions for a **smaller wire payload** while keeping the **verb surface** and contract envelope. Top-level keys you typically see:

```text
_format, _version, _hash_policy, _hash, _note,
contract, messages, verbs
```

Full Workbench/engine files additionally carry rich `instructions`, `masq`, `guidance`, and fuller `contract` fields.

### What “hash policy” means

`_hash_policy` lists:

- **Pointers** into the document that participate in the server-side contract hash (rules the model must not silently drift from).  
- **Excluded** paths (`guidance`, `contract`, `metadata`, `_.*`) so operators can tune advisory text without always changing the hash.

Only **Zeus** (verify/stamp) is the source of truth for the production hash. Clients and templates must not invent one.

---

## What is a contract — and why it matters

A **contract** is the **stamped agreement** between:

1. The **catalog rules** (verbs + instructions + masq, per hash policy)  
2. The **scope** (bucket/scope and enablement on Zeus)  
3. The **client** (Zeus Client binds `contract_id` + `contract_hash` on the session)

### Why it is important

| Without contracts | With contracts |
| --- | --- |
| Model may see drifting tools | Tool menu is **pinned** to a known stamp |
| Hard to audit “why that answer” | Detective / traces can attribute drift vs engine fault |
| Easy to ship a jailbroken tool set | Enforcement can **reject** unbound or drifted clients |
| Every env reinvented by hand | Ops stamp once; apps **sync** the stamped file |

In Zeus Client config this looks like:

```json
"zeus": {
  "scope_contracts": {
    "my-bucket/my-scope": {
      "contract_id": "… from stamp …",
      "contract_hash": "… from stamp — never invent …"
    }
  }
}
```

**Drift (often HTTP 409):** client hash ≠ Zeus stamp → resync stamped catalog and re-pin. **Never** hand-edit the hash to “make it work.”

---

## What you can change vs must not

### Safe / expected places to change behavior

| Where | What you change | Who |
| --- | --- | --- |
| **Hub → Workbench** | Refine catalog for **your** data: guidance, business injections, emphasis, mode copy, preview against live scope | Admin / operator |
| **Hub → stamp / verify** | Produce authoritative `contract_id` / `contract_hash` for a scope | Admin |
| **Zeus Client `AgentHooks`** | Policy that prompts cannot override: pin tenant filters, reject verbs, cap rounds, inject labeled data | Developer |
| **Zeus Client config** | `ZEUS_URL`, auth, sample bucket/scope/collection, mode, LLM provider, which stamped catalog to load | Developer |
| **App prompt / user question** | Advice-shaped user text (untrusted) | App |

### Do **not** do these in production paths

| Action | Why |
| --- | --- |
| Invent or paste a random `contract_hash` | Breaks enforcement / audit; causes drift |
| Hand-edit baseline JSON from this repo and ship as “stamped” | No Hub stamp = not your production contract |
| Change **verb schemas** in a fork without regenerating/stamping on Zeus | Model and server will disagree |
| Put PATs / passwords into the chat_request or system prompt | Security anti-pattern |
| Point app at Hub **:9091** to “edit” catalogs | Hub is ops UI; apps use public **:8080** + Client |

### Baseline files in **this** repo

| OK | Not OK |
| --- | --- |
| Copy as a **starting** template for demos / scaffold | Treat as production stamp for your cluster |
| Reference mode + verb list for learning | Expect guidance for *your* entities to already be perfect |
| Refresh via Zeus `ai-snapshot --min` + sync scripts | Hand-maintain forks as long-lived production truth |

**Refinement for your dataset belongs in Hub Workbench**, then stamp, then Client sync — not in a long-lived private fork of these baselines alone.

---

## How Zeus Client uses a chat_request

Typical production loop:

```text
1. Ops: enable scope + refine catalog in Hub Workbench
2. Ops: Verify + Stamp → authoritative contract_hash
3. Client: sync_chat_requests(cfg)  → stamped files under config dir
4. Client: run_agent(...)
      Auth → load catalog → bind contract → LLM rounds → Zeus verbs → commit/audit
```

### What the developer changes in **zeus_client** (not the catalog JSON)

| Concern | Client-side lever |
| --- | --- |
| Which Zeus / scope | `zeus.url`, samples, `ZEUS_URL`, bucket/scope/collection |
| Which mode | `default_mode` / mode arg to `run_agent` |
| Which stamp | `zeus.scope_contracts` after sync |
| Runtime policy | `AgentHooks` (`before_zeus_dispatch`, `should_continue`, …) |
| UI rows | `structured=True`, `output_schema` |
| Multi-turn | `zeus_session_id` + `zeus_round` from `session_meta` |

### What the developer should **not** do in Client

- Re-implement free-form SQL instead of verbs  
- Skip sync and ship unstamped baseline hashes  
- Override stamp by editing local JSON hash fields  

See: [Using Zeus Client](https://docs.koten.ai/zeus-client/using-zeus-client) · [Contracts & catalog](https://docs.koten.ai/zeus-client/contracts-and-catalog)

---

## Hub Workbench: refine for **your** data

**Zeus Hub → Workbench** is the product surface to:

1. Load or select a **baseline / mode** catalog  
2. Align language and guidance with **your** inventory (entities, fields, business rules)  
3. Preview against a **live enabled scope**  
4. **Verify** and **Stamp** so clients can bind safely  

```text
Baseline (this repo or engine snapshot)
        │
        ▼
  Hub Workbench  ── refine for your dataset ──► guidance, brief, emphasis
        │
        ▼
  Verify + Stamp  ──► contract_id + contract_hash
        │
        ▼
  Zeus Client sync + scope_contracts bind
```

Workbench changes that stay under **excluded** hash paths (e.g. much of `guidance`) may be easier to iterate without hash thrash; changes to **verbs / instructions / masq** typically require a **new stamp**. Prefer the Hub flow over hand-editing Git JSON for production.

---

## Modes in this distribution

Each baseline file targets a **mode** (tool/policy slice), not a customer dataset:

| Mode file pattern | Intent (high level) |
| --- | --- |
| `…_analytics_v2_min.json` | Analysis-oriented help |
| `…_code_v2_min.json` | Code-oriented tool use |
| `…_tenant_v2_min.json` | Multi-tenant-aware patterns |
| `…_fraud` / `regulated` / `private` / … | Stricter or domain-shaped defaults |

Pick a mode that matches the **kind of help**, then refine in Workbench for **your** scope.

---

## Mental model (one page)

| Question | Answer |
| --- | --- |
| What is this file? | LLM catalog: verbs + rules (+ guidance) |
| What is this repo? | **Baseline** min catalogs for integrators |
| Where do I customize for my data? | **Hub Workbench** |
| What is a contract? | Stamped fingerprint of allowed catalog rules for a scope |
| Why care? | Safety, audit, drift control, production enforcement |
| What does Client change? | Config, hooks, questions, session — not invented hashes |
| Production path? | Workbench → stamp → `sync_chat_requests` → `run_agent` |

---

## Related

| Resource | Link |
| --- | --- |
| Modes + files | [README.md](README.md) |
| Version history | [RELEASE_NOTES.md](RELEASE_NOTES.md) |
| Manifest | [manifest.json](manifest.json) |
| Platform docs | https://docs.koten.ai/ |
| Zeus Client usage | https://docs.koten.ai/zeus-client/using-zeus-client |
| Helper MCP | https://github.com/koten-ai/zeus_dev_helper_mcp |
| Engine generator | Zeus: `go run . ai-snapshot --mode=all --api-version=v2 --min` |
