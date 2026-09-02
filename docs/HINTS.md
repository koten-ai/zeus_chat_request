# Soft HINTS inject contract (base-6+)

> **Doc status** · last reviewed **2026-07-27** · production pin **base-1** · candidate pack **base-6** · version matrix: [COMPAT.md](../COMPAT.md)

**Audience:** Zeus Client, Hub Workbench, catalog authors  
**Jira:** epic [CR-4](https://kotenai.atlassian.net/browse/CR-4) · stories CR-13 / CR-14  
**Playbook (recipes, multi-intent):** [BEST_PRACTICES.md](BEST_PRACTICES.md)  
**Assembly zones:** [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md)  
**Pack:** [`v2/base/base-6/`](../v2/base/base-6/)  
**ROADMAP home:** [ROADMAP.md](ROADMAP.md) § base-6

**Wire law:** base-5 hard control plane is frozen. `hints.*` are **hash-excluded soft injects** after `rules{}`. They never replace jailbreak keys, `company_context`, MINI-SCHEMA, or required Layer A.

**Client residual:** runtime inject is **ZC-WISH-040** (not required for this pack to ship as candidate).

---

## Catalog (soft steer)

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
| **P2** | **Optimization (WIP)** | `hints.optimization.strategy` = `fast_pass` \| `scout` \| `thorough`; optional `question_class` | Staples are the theory. Class is a **default**, not a second product. [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) |
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
  optimization:   # WIP — see OPTIMIZATION_STRATEGIES.md; not live until Client injects
    strategy: fast_pass | scout | thorough    # staples
    question_class: known_goal | open_ended   # default; turn may mix on one overlay
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
| “Explore because inject is thin ⇒ mode=open” | Staple **`scout`**, then `fast_pass` or `thorough` |
| “Why Rome fell” on hotel inventory | Out of corpus → wish/clarify, not thorough; in-graph “why Tulum in April” is open_ended on that overlay |

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
- [ ] Client injects `hints.*` after `rules{}` (hash-excluded)  
- [ ] At least P0: path + fields + multipart live on one product path  
- [ ] Hot Path can emit `hints.hot_path` without re-stamp  
- [ ] A/B arm reported as cheap Client scalar  
- [ ] Jailbreak rules still present when ab_paste is set  

---
