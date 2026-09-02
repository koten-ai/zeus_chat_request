# Prompt rule placement methodology

> **Doc status** · last reviewed **2026-07-28** · production pin **base-1** · candidate pack **base-6** · version matrix: [COMPAT.md](../COMPAT.md)  
> **Citation:** use this doc when adding or moving any instruction (CORE, mode overlay, `BP:N`, `OPT:N`, `hints.*`, Client law)  
> **Consumers:** catalog authors, Prompt Helper, zeus_client, Zeus Hub Workbench

**Related:** [BIBLE.md](BIBLE.md) · [MODE.md](MODE.md) · [BEST_PRACTICES.md](BEST_PRACTICES.md) · [OPTIMIZATION.md](OPTIMIZATION.md) · [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) (**WIP** pickable postures) · [HINTS.md](HINTS.md) · [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · [WISH_I_KNEW_DUAL.md](WISH_I_KNEW_DUAL.md) · [ROADMAP.md](ROADMAP.md) · design-docs [DESIGN.md §14](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) (engine modes)

**Why this exists:** Instruction reliability fails when authors put traffic-only polish in every stamp, or leave contract-critical law only in optional essays. This file is the **stable method** for *where* a rule lives — apply it to **old rules** and **new ones**.

---

## 0. One-sentence law

```text
CORE + MODE overlay + return schemas  =  always-on contract (hashed where applicable)
BP:N                                  =  day-one playbook floor (short; every scope)
OPT:N / hints.* / custom stamp        =  after traffic (or scope-specific pain)
Client / engine                       =  enforce security & success; never "hope" the model
```

**Looser mode (open/fraud) changes join/confidence *flavor* — not the contract wire.**

---

## 1. Placement surfaces

| Tag | Surface | Lives in | Hashed in stamp? | When loaded |
| --- | --- | --- | --- | --- |
| **CORE** | Shared system sections (execution, efficiency, terminate table, world model, dual-gaps names) | `work/mode_overlays/CORE.md` → assembled into every `chat_request_<mode>_*.json` | **Yes** (`messages[].content`) | Every turn |
| **MODE** | `## Mode: <name>` persona (noise, hops, terminate flavor) | `work/mode_overlays/<mode>.md` | **Yes** | Every turn for that mode |
| **SCHEMA** | Tool / return JSON Schema (required four, wish shape) | pack `verbs[]`, `response_output_schema.json` | **Yes** (verbs) | Every turn |
| **BP** | Short always/never laws `BP:N` | [BEST_PRACTICES.md](BEST_PRACTICES.md); thin lines may mirror CORE | Prefer **cite** in CORE; full card in BP file | Day-one / Helper; not full book in every pack |
| **OPT** | Traffic sharpen `OPT:N` | [OPTIMIZATION.md](OPTIMIZATION.md) | Only if stamped into custom | Hot Path / Helper / custom when pattern matches |
| **STRATEGY** | **WIP** staples `fast_pass` \| `scout` \| `thorough`; class `known_goal` \| `open_ended` as default | [OPTIMIZATION_STRATEGIES.md](OPTIMIZATION_STRATEGIES.md) · `guidance.optimization` / `hints.optimization` | **No** (hash-excluded) | Must be **rendered** into messages; named_query is not a pin verb |
| **HINTS** | Soft inject `hints.*` | Client runtime (base-6+) | **No** (hash-excluded) | After hard `rules{}`; size-capped |
| **CLIENT** | Assemble, redact G2, policy table, messages[], injects, validate | zeus_client / Zeus Hub | N/A | Every turn |
| **ENGINE** | Tenant wall, hop caps, mode confidence floors | Zeus `internal/modes/` | N/A | Always enforce |

Do **not** collapse ENGINE security into optional BP prose.

---

## 2. Decision procedure (every rule — old or new)

When you write or review a rule, answer in order:

### Step A — What fails if this rule is missing on turn 1 of a new scope?

| If missing causes… | Place |
| --- | --- |
| Invalid terminate / inventing facts / wrong audience in chat | **CORE + SCHEMA** |
| Cross-tenant leak / PII dump / unsafe tool | **ENGINE + CLIENT** (+ MODE language) |
| Wrong verb class / thrash rediscovery on any scope | **CORE** (+ **BP** short law) |
| Only hurts after hundreds of chats on one path | **OPT** or **HINTS** or custom stamp |
| How hard this turn may think | **STRATEGY** staple `fast_pass` \| `scout` \| `thorough` (WIP) — not MODE, not CORE |
| Sized bag vs in-graph unknown budget | **STRATEGY** `question_class` default — mixed traffic OK; don’t mix **gold books** |
| Only matters for one mode’s personality | **MODE** overlay |
| Only matters for one tenant brand | **CLIENT inject** (`company_context`, `rules{}`) — not CORE |

### Step B — Is it wire or flavor?

| Kind | Example | Place |
| --- | --- | --- |
| **Wire** | required four, G1≠G2, return schema, object triggers | CORE + SCHEMA (all modes identical) |
| **Flavor** | “noise OK”, “redact full content”, “deeper call-graph hops” | MODE overlay |
| **Recovery law** | empty streak, multi-turn reuse | BP floor; one line may sit in CORE |
| **Traffic rail** | named_query, skinny 5-verb stamp, seasonal | OPT / custom stamp |

### Step C — Token budget

| Length | Place |
| --- | --- |
| ≤ ~5 lines | CORE or MODE OK |
| Short always/never table | BP (cite `BP:N` from CORE if needed) |
| Medium operator card | OPT:0–28 |
| Verbose recipe | OPT:29+ **only** when Helper/Hot Path selects |

### Step D — Enforcement

| Need | Owner |
| --- | --- |
| Model “should” | CORE / MODE / BP |
| Product “must” for security | ENGINE + CLIENT |
| Product “must” for contract success | CLIENT validate required four; Hub stamp/bind |
| Soft product nudge this session | HINTS / `output_request` |

If security-critical, **never** leave it only in BP/OPT.

### Step E — Checklist (paste into PR)

```text
Rule: <one line>
Placement: CORE | MODE | SCHEMA | BP | OPT | STRATEGY | HINTS | CLIENT | ENGINE
Modes: all | list
Day-one?: yes | no (traffic-only)
Hashed?: yes | no | n/a
Enforced by: model | Client | engine
Citation: BP:N | OPT:N | none
Anti-pattern if misplaced: <one line>
```

---

## 3. Mode postures (all ten)

From [MODE.md](MODE.md) + design-docs DESIGN §14. **Wire (Layer A) is shared.** Overlay teaches **posture**.

| Mode | Primary job | Prompt posture (MODE) | Confidence / noise | Notes for placement |
| --- | --- | --- | --- | --- |
| **analytics** | Safe default BI / KG | Real links not noise; evidence before claim | Floor ~0.50 language | Default reference for BP examples |
| **open** | Public maps / crawls | Weak edges OK; super-node risk; serendipity | Floor ~0.20; noise OK | Looser **flavor**, not looser **wire** |
| **fraud** | Identity / AML | Weak signals are the product; candidate lists | Floor ~0.20; keep noise | G1 may list candidates + uncertainty; still no invent |
| **research** | Papers / citations | Citation & backlink first; semantic first-class | Semantic-heavy | MODE: entity vocabulary DOI/Paper/Author |
| **code** | Call graphs | Structure before embedding; code entities | Deeper hop posture | MODE: hop budget language; ENGINE caps still apply |
| **tenant** | Multi-tenant SaaS | Scope is a **wall** | Analytics-like retrieval + isolation | ENGINE enforces wall; MODE states never cross-tenant |
| **regulated** | Health/finance/GDPR | High bar; redact; provenance-minded terminate | Floor ~0.80 | ENGINE+CLIENT redact; MODE: no casual full dumps |
| **private** | Personal KB | User boundary; personal graph | No corpus-stat crutches | MODE: no global stats; same empty/wish laws |
| **auto** | Onboarding only | Discover & propose; hand off | Floor ~0.90 discovery | Do not treat as production long-term pack |
| **custom** | Operator escape | Conservative; follow injects | Analytics-like until hooks | Prefer injects over inventing a personality |

### Mode rule: what may vary vs must not

| May vary by MODE | Must not vary by MODE |
| --- | --- |
| Join/noise language | Required four fields |
| Hop/fan-out **posture** (within ENGINE caps) | G2 never in chat UI |
| Terminate **flavor** (candidates vs redact-safe) | Evidence-only summary (no invent) |
| Example pipelines | return / tool schema shapes |
| Preferred entity vocab | Dual-gap field names / max 3 wish |

```text
Need fraud + tenant governance?
  → two scopes / pipelines — not one mushy catalog (MODE.md)
```

---

## 4. Top-10 reliability topics × placement × all modes

### Legend

| Tag | Meaning |
| --- | --- |
| **ALL** | Same in every mode CORE/SCHEMA |
| **M↑** | Stronger in MODE overlay for that mode |
| **M↓** | Softened language only (still obeys ALL wire) |

---

### 1) Conflicting instructions

| Place | Content |
| --- | --- |
| **CORE ALL** | One Terminate table; hard rules before soft; evidence law once |
| **MODE** | Only posture deltas (open noise OK; regulated high bar) — no second law |
| **CLIENT ALL** | Policy table + AgentHooks = law after model |
| **HINTS OPT** | After `rules{}`; must not strip jailbreak |
| **BP** | BP:3 always/never short |

| Mode delta | |
| --- | --- |
| open / fraud | M↓ precision language |
| regulated / tenant | M↑ isolation / redact |
| auto | M↑ “propose, don’t commit graph policy” |

---

### 2) Optional fields ignored (soft terminate / wish)

| Place | Content |
| --- | --- |
| **SCHEMA ALL** | Required four **required** in return tool |
| **CORE ALL** | Table + QD vs wish distinction + dual-gap names |
| **BP ALL** | BP:13 empty; **progressive streak MUST wish** |
| **HINTS OPT** | soft_require when product needs |
| **CLIENT OPT→should** | `output_request.layer_a`; validate before success |

| Mode delta | |
| --- | --- |
| open / fraud | M↓ confidence OK with candidates; still fill required four |
| regulated | M↑ provenance-minded terminate; still no invent |
| ALL | Progressive empty inventory + wish — **not** mode-optional |

---

### 3) Prose-only contracts

| Place | Content |
| --- | --- |
| **SCHEMA ALL** | verbs + return schemas |
| **CORE ALL** | Terminate with tools, not free text only |
| **CLIENT ALL** | Parse tool_calls; reject plain-text final when bound |
| **OPT** | Stamp/verify UX |

| Mode delta | none on wire |

---

### 4) Tool bloat / wrong tools

| Place | Content |
| --- | --- |
| **CORE ALL** | Verb cost; no rediscovery when inject green |
| **MODE** | Hop/join posture (code↑ hops language; fraud keep weak edges) |
| **BP ALL** | BP:1–5 recipes; BP:2 field class |
| **OPT primary** | OPT:23 skinny stamps; OPT:9–12 rails; OPT:18 mode board density |
| **HINTS OPT** | hot_path, avoid_patterns after traffic |

| Mode delta | |
| --- | --- |
| code | M↑ structural verbs / deeper hops |
| research | M↑ citation/semantic first |
| open | M↑ multi-edge sample-then-expand |
| analytics/tenant/custom | M↑ degree caution / real links |
| Skinny verb sets | **OPT/custom stamp**, not “open CORE has 5 tools” |

---

### 5) Incomplete inject (brief/schema)

| Place | Content |
| --- | --- |
| **CORE ALL** | Use BRIEF/MINI-SCHEMA; no invent; wish/data_gaps path |
| **CLIENT ALL** | Inject live brief/schema every turn |
| **BP ALL** | BP:13–14; progressive streak inventory (G1) |
| **OPT** | OPT:15 params; OPT:31–32 virtual/stubs; sample policies |
| **MODE** | private: no corpus stats; others: evidence before claim |

| Mode delta | |
| --- | --- |
| private | M↑ no global stats crutches |
| ALL | Amenity/market inventory after filter miss — universal recovery |

---

### 6) Audience leak (G1/G2/G3)

| Place | Content |
| --- | --- |
| **CORE ALL** | Audience columns on terminate table |
| **CLIENT ALL** | Redact G2; show summary (+ Zeus tables) |
| **MODE** | regulated: redaction-safe **summary flavor** |
| **fraud/open** | Candidates in **G1** with uncertainty — not G2 scores in UI |

| Mode delta | flavor only |

---

### 7) Multi-turn amnesia

| Place | Content |
| --- | --- |
| **CORE thin ALL** | @step.ids; one plan |
| **BP ALL** | BP:4 multi-turn reuse |
| **CLIENT ALL** | Append messages[] + tool results |
| **CLIENT should** | `ai_process_result` default false |
| **OPT** | OPT:4, OPT:29, OPT:6; HINTS multipart |

| Mode delta | none on Client bags |

---

### 8) Latency vs correctness

| Place | Content |
| --- | --- |
| **CORE ALL** | Act-don’t-narrate **and** evidence-only (both) |
| **BP ALL** | BP:3 no thrash; BP:13 recovery |
| **MODE** | open/fraud: lower confidence OK; regulated: no dump for speed |
| **OPT** | skinny, cache OPT:17, rails |
| **CLIENT/Hub eval** | Quality-first A/B (outside pack prose) |

| Mode delta | confidence language only |

---

### 9) Evaluation ≠ product success

| Place | Content |
| --- | --- |
| **SCHEMA/CLIENT ALL** | Required four; stamp/bind |
| **BP ALL** | Empty honesty |
| **OPT primary** | OPT:33; gold books **per mode**; rail SLOs |
| **MODE** | Gold questions differ (fraud candidates vs regulated redact) |

| Mode delta | books & rails, not wire |

---

### 10) Unstable / huge prefixes

| Place | Content |
| --- | --- |
| **CORE ALL** | Stable section order; dieted terminate |
| **CLIENT ALL** | Hash boundary; injects not hashed; no timestamps in system head |
| **MODE** | Overlay **short** (not full BP book) |
| **OPT** | OPT:17 cache; OPT:23 skinny; hint size caps |
| **ROADMAP base-8** | Compression later |

| Mode delta | keep overlays short for all modes |

---

## 5. Per-mode “day-one pack” checklist

For each `chat_request_<mode>_base-N.json`:

### Universal (all modes)

- [ ] CORE: execution, efficiency, verb cost, terminate table, world model, dual-gap names  
- [ ] SCHEMA: return + verbs; required four  
- [ ] MODE: unique overlay (not analytics clone — `diff_modes` gate)  
- [ ] Evidence-only / no invent  
- [ ] G2 never in summary  

### Mode overlay must include (MODE.md template spirit)

- [ ] Mission (one paragraph)  
- [ ] Entities to prefer  
- [ ] Join / noise posture  
- [ ] Traversal budget posture  
- [ ] Terminate flavor  
- [ ] Don’t list  
- [ ] One example pipeline  

### Mode-specific emphasis

| Mode | Extra emphasis in MODE (still short) |
| --- | --- |
| **open** | Super-node warn; sample-then-expand; serendipity ≠ invent |
| **analytics** | Real links; degree caution; default BI recipes |
| **tenant** | Scope wall language; no cross-tenant implication |
| **regulated** | Redact; high bar; provenance; no full-content dump |
| **private** | User boundary; no corpus-stat crutches |
| **fraud** | Keep weak signals; candidate lists; analyst-facing uncertainty |
| **research** | Citation/backlink first; paper entities |
| **code** | Structure > embedding; code entities; deeper hop posture |
| **auto** | Discover/propose/handoff; not long-term policy |
| **custom** | Follow injects; conservative; no invented persona |

### Not required in every mode file day-one

- Full BP book, OPT rails, skinny verb lists, seasonal packs, verbose OPT:29+  

---

## 6. Applying methodology to **existing** rules

### 6.1 Audit pass (authors / Helper)

1. List rule (or `BP:N` / `OPT:N` / CORE paragraph).  
2. Run §2 Steps A–D.  
3. If rule is in CORE but traffic-only → **move** to OPT/HINTS/custom (or shorten CORE to one line + cite OPT).  
4. If rule is only in OPT but day-one critical → **promote** to BP floor or CORE.  
5. If rule differs by mode only by strength → MODE overlay, not a second CORE.  
6. Record in PR using Step E checklist.

### 6.2 Suggested homes for current citation families

| Family | Default home | Promote to CORE when… | Demote to OPT when… |
| --- | --- | --- | --- |
| BP:0–3, 5, 9 | BP floor; thin CORE | Missing causes invent/wrong terminate | — |
| BP:4 multi-turn | BP floor | Client also enforces messages[] | — |
| BP:13 empty + streak | BP floor; 1 line CORE dual-gaps | Always | — |
| BP:14 virtual | BP floor | Common empty City/Amenity miss | — |
| BP:6–8 multi/join | BP floor | — | Very long examples → OPT |
| OPT:0–28 portfolio | OPT | — | — |
| OPT:23 skinny | OPT / stamp | — | Never default CORE for all modes |
| OPT:29+ verbose | OPT rare | — | Never CORE |
| hints.* | HINTS | — | Never hashed jailbreak replacement |
| Progressive empty / wish | BP:13 + WISH_I_KNEW_DUAL | Already day-one | — |

### 6.3 Top-10 reliability map (compact)

| # | Topic | Day-one bake | Later optional |
| --- | --- | --- | --- |
| 1 | Conflicts | CORE + CLIENT policy | hints |
| 2 | Optional ignored | SCHEMA required four; BP:13 streak | soft_require |
| 3 | Prose-only | SCHEMA + return | — |
| 4 | Tool bloat | CORE cost + MODE hops | OPT:23 rails |
| 5 | Incomplete inject | CORE + CLIENT inject; BP:13–14 | OPT:15/31/32 |
| 6 | Audience leak | CORE + CLIENT redact | — |
| 7 | Multi-turn | BP:4 + CLIENT messages | OPT:4/29 |
| 8 | Speed vs correct | CORE both laws; BP:13 | skinny/cache |
| 9 | Bad eval | SCHEMA + books | OPT:33 A/B |
| 10 | Huge prefix | CORE diet + CLIENT hash | OPT:17/23 base-8 |

---

## 7. Applying methodology to **new** rules

1. Write the rule in one sentence.  
2. Fill Step E checklist in the PR.  
3. Prefer **smallest surface** that still enforces the failure mode.  
4. Add **BP:N** or **OPT:N** id (**append only**, never renumber).  
5. If MODE-specific, edit `work/mode_overlays/<mode>.md` and reassemble packs.  
6. If universal wire, edit CORE + schema + all modes get it via assemble.  
7. Update this doc’s §6.2 table if a new family appears.  
8. Helper: cite `BP:N` / `OPT:N` / “see PROMPT_RULE_PLACEMENT §2”.

---

## 8. Anti-patterns

| Don’t | Do instead |
| --- | --- |
| Paste full OPT book into CORE | Cite OPT; load on Hot Path match |
| Different required four per mode | Same wire; MODE flavor only |
| “Open mode can invent for serendipity” | Open may keep weak edges; still no invent |
| Mid-session strip hashed tools | New stamped skinny pack |
| Put G2 in summary “so user sees wish” | G1 inventory list; G2 for ops |
| New rule with no placement tag | Step E checklist |
| Security only in BP essay | ENGINE + CLIENT |

---

## 9. Success signals

- [ ] Authors can classify any new rule in under 5 minutes with §2  
- [ ] `diff_modes` still fails analytics clones  
- [ ] CORE length stays bounded; OPT absorbs growth  
- [ ] Progressive empty + G1/G2 split documented and cited from BP:13  
- [ ] Prompt Helper inserts cite BP/OPT ids, not anonymous paragraphs  

---

## 10. Doc ownership

| Change | Update |
| --- | --- |
| New placement rule / methodology | **This file** |
| New day-one recovery law | BEST_PRACTICES + maybe 1 CORE line |
| New traffic rail | OPTIMIZATION |
| New mode posture | MODE.md + mode overlay |
| Wire/Layer A | BIBLE + schema |
| Train sequencing | ROADMAP |

**SoT for “where does this instruction go?” → this file.**  
**SoT for “what is Layer A?” → BIBLE.**  
**SoT for “what is a mode?” → MODE.md + design-docs DESIGN §14.**
