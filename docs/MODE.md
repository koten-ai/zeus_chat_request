# Modes — engine projection vs chat_request catalog

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · candidate pack **base-5** · next content train **base-5.1** (mode overlays) · version matrix: [COMPAT.md](../COMPAT.md)

**Audience:** catalog authors, Zeus engine, zeus_client, Workbench  
**Roadmap train:** **base-5.1** — pack folder **`v2/base/base-5.1/`** · [ROADMAP.md § base-5.1](ROADMAP.md)  
**Executable restore plan:** [../work/RECREATE_MODE.md](../work/RECREATE_MODE.md)  
**Jira:** [CR-23](https://kotenai.atlassian.net/browse/CR-23) · snapshot layout [CR-25](https://kotenai.atlassian.net/browse/CR-25)  
**Normative product design (engine modes):** [zeus_design_docs DESIGN.md §14](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md) · runtime hooks `Zeus/internal/modes/`  
**Related:** [CHAT_REQUEST.md](CHAT_REQUEST.md) · [BIBLE.md](BIBLE.md) · [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) · [ROADMAP.md](ROADMAP.md)

This doc explains **what a mode is**, **why catalogs look identical today**, and **what must differ in the LLM-facing prompt** so each mode does its intended job. It does **not** invent production `contract_hash` values.

---

## 0. One-sentence definition

A **mode** is a **per-scope** product profile that decides how Zeus **builds and queries the graph** (ingest, edges, confidence, tenancy, enrichment) and how the **chat_request catalog** teaches the model to **ask, traverse, and terminate** under that profile.

```text
Scope (bucket/scope)  →  bound to one mode (or auto → proposes, then commits)
Mode                  →  engine hooks + rate/enrichment + chat_request pack
chat_request pack     →  system prompt + verbs + terminate contract the LLM sees
```

Modes are **not** Zeus semver, **not** BASE `base-N`, and **not** a Client package version.

---

## 1. Two layers (do not collapse)

| Layer | What it controls | Where it lives | Changes often? |
| --- | --- | --- | --- |
| **A. Engine mode hooks** | Boundary, entity extract list, join policy, confidence floor, strength weights, extra edge types, enrichment pipelines | Zeus `internal/modes/`, ingest, rate profiles, DESIGN §14.6 packages | Code release |
| **B. chat_request catalog (LLM)** | System prompt, verb list/descriptions, terminate expectations, examples | This repo `v2/base/base-N/min/chat_request_<mode>_base-N.json` | BASE pack PR |

Both layers must **agree**. Today **A is partially differentiated**; **B is almost not**.

### 1.1 What the LLM actually reads

In current BASE packs the durable “house rules” string is:

```text
messages[0].role = "system"
messages[0].content = <long prompt string>
```

That content is part of the **stamp/contract surface**: `_hash_policy.pointers` includes `/messages/*/content` (and legacy `/instructions/*` paths). The top-level **`contract` object** is **metadata only** (`id`, `hash`, `builder`, …) — it is **hash-excluded** and is **not** where mode prose lives.

```text
┌─ Catalog document ─────────────────────────────────────────────┐
│  messages[].content     ← MODE PERSONA + CORE DISCIPLINE (LLM) │
│  verbs[]                ← tool schemas (mostly shared today)   │
│  contract{}             ← stamp metadata (not the essay)       │
│  _lineage.mode          ← which mode file this is              │
│  _hash / _hash_policy   ← what participates in stamp           │
└────────────────────────────────────────────────────────────────┘
```

**Restore target for mode intent:** primarily **`messages[].content`** (and secondarily verb descriptions / optional `guidance` if we choose hash-excluded soft text). Not `contract.name` alone.

---

## 2. Mode catalog (product intent)

From DESIGN §14.1 and Zeus `internal/modes` comments. “Tour” detail: design-docs `2ND_IDEA.md` §9 (referenced from DESIGN).

| Mode | Built for | Engine hook highlights | What the **prompt** should teach |
| --- | --- | --- | --- |
| **open** | Public data, link maps, crawls | Strong joins; floor **0.20**; noise OK | Expect weak edges; watch super-nodes; serendipity over precision |
| **analytics** | Safe default BI / knowledge graph | Defaults floor **0.50**; structural+semantic weights | Prefer real links not noise; degree-aware traversal; evidence before claim |
| **tenant** | Multi-tenant SaaS hard walls | Boundary always **tenant**; extract Email/Account/Person/Org | Scope is a wall; never imply cross-tenant facts; same retrieval style as analytics, stronger isolation language |
| **regulated** | Health/finance/GDPR | Tenant boundary; floor **0.80**; PII-shaped extract; audit | High confidence only; redaction; no casual full-content dumps; provenance-minded terminate |
| **private** | Personal KB / single user | Boundary **user**; statistical weight **0** | Backlinks and personal graph; no corpus-wide stats assumptions |
| **fraud** | Identity correlation / AML | Floor **0.20**; strong joins; Device/Phone/Address/IBAN; `shares_*` edges | Weak signals are the product; surface candidates for analyst review; do not “clean away” noise |
| **research** | Academic / citation corpora | DOI/Paper/Author; cites/cited_by; semantic-heavy | Citation & backlink first; paper entities; semantic similarity as first-class |
| **code** | Source / call graphs | Function/Class/Module/Package; calls/imports/inherits/tests; structural-heavy | AST/structure before embedding; deeper hop budgets; code entities only |
| **auto** | First-contact onboarding | Floor **0.90** during discovery; proposers pick a named mode | Discover & propose; do not commit long-term graph policy; hand off to named mode |
| **custom** | Operator escape hatch | Analytics-like defaults until hooks wired | Stay conservative; follow tenant/operator injects; do not invent a mode personality |

### 2.1 Fit matrix (read once)

DESIGN §14.2: each named mode wins **one** primary use-case column. **`analytics` is the safe default** (never below ~3★). **`auto` is onboarding, not production.** **`custom` is only as good as the hooks you wire.**

```text
Need fraud + tenant governance?
  → two pipelines / scopes — not one mushy catalog
```

### 2.2 Universal limits vs per-mode tightenings

Universal (every mode): hop/fan-out/timeout caps (DESIGN §14.3).  
Tightenings (DESIGN §14.4): e.g. regulated audit+redact, fraud no degree cap / low floor, code higher hops + code embeddings, auto high floor during discovery.

The **prompt** should **state the posture** the model can follow; the **engine** must still **enforce** what is security-critical (tenant wall, regulated content rules).

---

## 3. Current state

### 3.1 After base-5.1 (content train)

| Surface | Reality |
| --- | --- |
| File names | 10 packs: `chat_request_<mode>_base-5.json` |
| `_lineage.mode` | Correct per file |
| System prompt | **CORE + `## Mode: <name>` overlay** per mode (`work/mode_overlays/`) |
| **auto** | Discovery / propose / handoff overlay (not analytics clone) |
| Verbs | Same 13 names (wire shared); blurbs no longer say only “analytics job” |
| Layer A / terminate | Same object shape (base-5 wire) across modes |
| Assemble | `scripts/assemble_mode_prompts.py --base 5` |
| Clone gate | `scripts/diff_modes.py --base 5 --fail-if-clone` |
| Zeus generator | Overlay port to `ai/V2/prompt/core/modes/` still optional follow-up |

### 3.2 Pre–base-5.1 failure (historical)

Packs were **analytics × rename** (only mode string differed; `auto` shorter min essay). Engine hooks differed; LLM catalogs did not.

```text
Intended:   mode ──► graph projection + LLM menu/persona
base-5.0:   mode ──► graph projection (partial); LLM ≈ analytics × rename
base-5.1:   mode ──► graph projection + CORE + MODE_OVERLAY in messages[].content
```

### 3.3 Why it drifted (pre-5.1)

1. V2 minify / shared prompt fragments optimized for **one** efficient pipeline essay.  
2. BASE diet trains (base-4/5) focused on **wire shape** (Terminate, objects), not mode personas.  
3. Scaffold/`new_base` **copies parent packs** mode-by-mode without a mode matrix.  
4. Overlay path in the generator was never filled.  
5. Tests guarded tool-name drift more than “modes differ.”

---

## 4. What “restoring modes” means (scope)

### In scope

- Differentiated **system prompt** sections (mode persona + constraints + preferred entities/edges + example pipelines).  
- Optional **verb description** tweaks / experimental tool blurbs that still say “analytics job.”  
- Optional **hash-excluded** `guidance` for soft tips (if product wants softer text out of stamp).  
- Generator **core + overlay** so packs stop being manual renames.  
- Verify gate: non-auto mode must not collapse to analytics after neutralizing the mode token.

### Out of scope (unless a separate Zeus ticket)

- Replacing DESIGN §14 or rewriting all of `internal/modes`.  
- Flipping production pin.  
- Inventing stamps / `contract_hash`.  
- Making Layer A required fields mode-specific (keep base-5 required four universal).  
- Dual-read of base-4 arrays (unrelated).

### Relationship to BASE law

Mode **prose/overlays** are **content**. They do **not** require a wire break if Layer A schema and object rules stay base-5.

**Roadmap name: base-5.1** — content on the base-5 **wire**, shipped as its **own snapshot folder** `v2/base/base-5.1/` (parent `base-5`).  
**Do not** mutate `base-5/` in place with `content_train` — pullable Diff requires separate trees.

See [ROADMAP.md § base-5.1](ROADMAP.md) · [work/RECREATE_MODE.md](../work/RECREATE_MODE.md) · **CR-25**.

---

## 5. Architecture for differentiated catalogs

### 5.1 Core + overlay (recommended)

```text
messages[0].content =
    CORE_DISCIPLINE          # shared: efficiency, pipeline, return, base-5 objects
  + MODE_OVERLAY             # DESIGN persona: entities, edges, floors, do/don’t
  + (optional) EXAMPLES      # 1–2 mode-shaped pipelines
```

| Piece | Shared? | In stamp hash? |
| --- | --- | --- |
| Core discipline | **yes** | yes (`messages/*/content`) |
| Mode overlay | **per mode** | yes (default — persona is policy) |
| Soft tips / demos | optional | prefer `guidance` **excluded** if noisy |

Do **not** put 10 fully forked 6k essays. Overlays should be **short and sharp** (target order: 400–1200 words of mode-specific text, not another full core).

### 5.2 Zeus generator alignment

Zeus already has:

```go
// systemPromptV2 … loadCoreFragment("modes/" + mode + ".md")
```

Restore path:

1. Author `modes/<mode>.md` fragments (design → Zeus `ai/V2/prompt/…` and/or this repo source-of-truth copy).  
2. Snapshot / export into `zeus_chat_request` packs.  
3. `export_base_text` / verify after diet.

### 5.3 What still belongs only in the engine

| Concern | Prompt may mention | Engine must enforce |
| --- | --- | --- |
| Tenant wall | yes | yes |
| Regulated redaction / content allowlists | yes | yes |
| Confidence floor at materialize time | guidance | yes |
| GROBID / MinHash / PII pipelines | “prefer citation tools / expect device entities” | packages in DESIGN §14.6 |
| Rate classes | optional | yes |

---

## 6. Per-mode overlay checklist (LLM-facing)

Use this when writing or reviewing an overlay. Each mode’s overlay should answer:

1. **Mission** — one paragraph (from §2 table).  
2. **Entities to prefer** — from `Extract()` / DESIGN.  
3. **Join / noise posture** — strong vs inferred; floor language.  
4. **Edges / relations vocabulary** — core 4 + extras (`cites`, `calls`, `shares_device`, …).  
5. **Traversal budget** — hops / fan-out posture (within universal caps).  
6. **Terminate flavor** — e.g. fraud: candidate lists + uncertainty; regulated: redaction-safe summary.  
7. **Hard don’ts** — e.g. auto: don’t pretend permanent mode policy; tenant: no cross-tenant.  
8. **One example pipeline** — mode-shaped, not beer-analytics-only.

### 6.1 Minimum differentiators (acceptance flavor)

| Mode | Must appear in overlay (examples) |
| --- | --- |
| analytics | real links not noise; degree caution |
| open | noise OK; super-node risk |
| fraud | weak signal; device/address/account correlation |
| research | DOI/Paper/Author; cite / cited_by |
| code | Function/Class; calls/imports; structure > embed |
| regulated | high bar; redact; no casual full content |
| tenant | hard scope wall |
| private | single-user; no corpus-stat crutches |
| auto | propose & hand off; high caution |
| custom | operator-defined; conservative default |

---

## 7. Interaction with Client injects

Mode pack ≠ injects. Still:

| Inject | Mode interaction |
| --- | --- |
| `company_context` | Orthogonal brand; all modes |
| `rules{}` | Hard policy; all modes |
| `output_request` | App bag; all modes |
| Settings locale/channel | Cheap; all modes |

Mode overlay must **not** re-encode tenant brand. It encodes **Zeus graph help style**.

Mode switch mid-session: DESIGN/Client practice = **new session / new pin** for catalog mode change (see Bible multi-turn / PROMPT_SETTINGS).

---

## 8. Verification

| Check | Pass |
| --- | --- |
| Neutralize mode token + compare to analytics | Diff shows a **MODE_OVERLAY** block (or equivalent), not only hash |
| Keyword/entity smoke | fraud/research/code/regulated hit expected vocabulary |
| Tool-name drift | Prompt only names verbs present in pack / registry (existing Zeus tests) |
| `verify_base_pack.py` | Still green for base-N wire invariants |
| Inspector Diff | analytics vs fraud readable human delta |
| Engine contradiction | Overlay does not claim tools/edges engine cannot do |

Suggested automation (plan): `scripts/diff_modes.py` + CI note in [work/RECREATE_MODE.md](../work/RECREATE_MODE.md).

---

## 9. Tracking

| Item | Link |
| --- | --- |
| Restore plan | [work/RECREATE_MODE.md](../work/RECREATE_MODE.md) |
| DESIGN modes | design-docs DESIGN §14 |
| Zeus hooks | `internal/modes/mode_*.go` |
| Packs | `v2/base/base-5/min/` |
| Process checklist | [migration/RELEASE_CHECKLIST_TEMPLATE.md](migration/RELEASE_CHECKLIST_TEMPLATE.md) |
| Jira | Open CR story when execution starts (mode restore under CR-1 or base-5 residual) |

---

## 10. Agent quick path

```text
1. Read this doc §1–3 (layers + current failure)
2. Read work/RECREATE_MODE.md for execution phases
3. Do not rename modes or invent hashes
4. Diet messages[0].content = core + MODE_OVERLAY
5. Re-export text; verify_base_pack; Diff analytics vs target mode
```
