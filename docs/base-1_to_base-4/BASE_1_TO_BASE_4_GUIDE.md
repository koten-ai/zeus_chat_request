# Guide: base-1 → base-4 mapping

**Purpose:** Show what stayed the same, what moved, and what was added from the production pin (**base-1**) through prototypes (**base-2**, **base-3**) to the current diet pack (**base-4**).

**Start here for full base-4 requirements:** [BIBLE.md](../BIBLE.md)  
**Experience / pitfalls:** [lessons-learned.md](lessons-learned.md)

| BASE | Role | Path |
| --- | --- | --- |
| **base-1** | Production pin today | `v2/base/base-1/min/`, alias `v2/min/` |
| **base-2-prototype** | Design fork: Layer A fields + docs | `v2/base/base-2-prototype/min/` |
| **base-3-prototype** | Text-only working copy (format) | `v2/base/base-3-prototype/text/` |
| **base-4** | Diet: one Terminate table + multi-round Client bible | `v2/base/base-4/` |

`CURRENT.json` still points at **base-1** until you promote.

---

## 1. Evolution in one picture

```text
base-1  (prod min JSON, *_v2_min.json)
   │
   │  + Layer A recommended fields on return
   │  + _prototype metadata, longer system addendum
   │  + naming → base-N in filename (prototype)
   ▼
base-2-prototype  (JSON design, still dense terminate prose)
   │
   │  format-only export (indented text)
   │  lineage base_id → base-3
   ▼
base-3-prototype  (*.txt diet surface — same ideas as base-2)
   │
   │  content diet: merge Evidence-loop + Layer A essays
   │  → single ## Terminate table + example
   │  + BIBLE, multi-round Client docs, JSON Schema
   ▼
base-4  (JSON + text — current BASE tip)
```

---

## 2. File naming map

| Era | Pattern | Example |
| --- | --- | --- |
| **base-1** | `chat_request_<mode>_v2_min.json` | `chat_request_analytics_v2_min.json` |
| **base-2-prototype** | `chat_request_<mode>_base-2-prototype.json` | `…_analytics_base-2-prototype.json` |
| **base-3-prototype** | `chat_request_<mode>_base-3.txt` | text only |
| **base-4** | `chat_request_<mode>_base-4.json` + `.txt` | `…_analytics_base-4.json` |
| **Future customs** | `chat_request_<mode>_base-4_cus_<bucket>_<scope>-<rev>.json` | Workbench |

| Concept | base-1 | base-4 |
| --- | --- | --- |
| Envelope field | `_format: zeus.chat_request.v2` | **same** |
| BASE in filename | **no** (`v2_min` instead) | **yes** (`base-4`) |
| Custom rev files | not standardized here | `…_cus_…-<rev>.json` (documented) |

**Note:** `v2` in **base-1 filenames** is legacy. In base-4+, **`v2` stays only as the JSON envelope** (`_format`), not the file stem.

---

## 3. Top-level JSON keys

| Key | base-1 | base-2/4 |
| --- | --- | --- |
| `_format`, `_version` | yes | yes (`_version` often 1 on b1, 2 on prototypes) |
| `_hash`, `_hash_policy` | yes | yes |
| `_note` | yes | yes (longer prototype notes) |
| `_lineage` | yes (`base_id: base-1`) | yes (`base-4`, parent links) |
| `contract` | thin (`builder`, `hash`) | richer prototype stamp fields |
| `messages` | yes | yes |
| `verbs` | yes (13) | yes (13) |
| `_prototype` | **no** | **yes** (design metadata) |
| `guidance` / `masq` / `instructions` | **no** on min | **no** on min (still full-profile only in engine) |

---

## 4. Lineage map

| Field | base-1 | base-4 |
| --- | --- | --- |
| `base_id` | `base-1` | `base-4` |
| `mode` | e.g. `analytics` | same modes |
| `profile` | `v2_min` | `v2_min` |
| `kind` | `base` | `base` |
| `custom_id` | null | null on BASE files |
| `parent_base_id` | — | `base-3` (diet parent) / chain from base-2 |
| `prototype` | — | `true` |
| `diet` | — | `single_terminate_table_plus_example` |

---

## 5. System prompt map

### base-1 sections

```text
## Execution style (latency matters)
## CRITICAL EFFICIENCY & CORRECTNESS RULES
## Verb Priority & Cost Model
## Evidence loop / hot-path return contract (CRITICAL)
```

### base-2-prototype sections

```text
## Execution style …
## CRITICAL EFFICIENCY …
## Verb Priority …
## Evidence loop / hot-path return contract (CRITICAL)   ← kept
## Layer A terminate contract (base-2-prototype)         ← ADDED (overlap)
```

### base-4 sections

```text
## Execution style …
## CRITICAL EFFICIENCY …
## Verb Priority …
## Terminate (Layer A) — copy this shape                 ← MERGED (table + example)
```

| Topic | base-1 location | base-4 location |
| --- | --- | --- |
| Act / pipeline / no plain text | Execution style | **same** |
| No rediscover stats / top-N | CRITICAL EFFICIENCY | **same** |
| Cheap tools first | Verb Priority | **same** |
| Required terminate fields | Evidence loop | **Terminate table** (req=yes rows) |
| query_decomposition facets | Evidence loop | Terminate table + short notes |
| policy_action, scores, wish_i_knew, triggers | **absent** | Terminate table (req=no) + example |
| Dual confidence explained | **absent** | One-line distinctions |
| Full example return skeleton | partial / prose only | **explicit example block** |

Approx system size (analytics): base-1 ~4.5k chars → base-2 ~5.8k → base-4 ~5.7k (clarity diet, not max shrink).

---

## 6. Layer A / `return` tool map

### Required fields (unchanged core)

| Field | base-1 | base-4 |
| --- | --- | --- |
| `summary` | required | **required** |
| `query_decomposition` | required | **required** |
| `decomposition` | required | **required** |
| `confidence` (`high`\|`med`\|`low`) | required | **required** |

### Added on base-2+ / base-4 (recommended)

| Field | base-1 | base-4 | Audience |
| --- | --- | --- | --- |
| `policy_action` | — | optional | G3 Client |
| `subject_confidence` (0.0–1.0) | — | optional | G2 Admin |
| `jail_break_attempt` (0.0–1.0) | — | optional | G2 Admin |
| `wish_i_knew[]` (max 3) | — | optional | G2 Admin |
| `business_rules_triggers[]` | — | optional | G3 Client |
| `node_refs` / `entity_refs` / `provenance` | on pipeline; soft in prose | on `return` too | G1 / UI |

### Schema artifacts

| Artifact | base-1 | base-4 |
| --- | --- | --- |
| JSON Schema file for terminate | — | `response_output_schema.json` |
| Example terminate instance | — | `response_output_example.json` |
| Detective Layer B store | exists in Zeus (not in BASE file) | **same** — still server-side |

**Important:** base-4 does **not** ask the model to emit Detective `diagnosis` / spans. That stays Layer B.

---

## 7. Verbs map

| | base-1 | base-4 |
| --- | --- | --- |
| Count | 13 | **13** |
| Names | describe, get, find, traverse, search, analyze, explain, set, order, enrich, project, pipeline, return | **same** |
| Parameter schemas | full JSON Schema on each | **same bulk** (not the focus of base-4 diet) |
| `return` description | must emit 4 fields | points at **Terminate table** + recommended fields |
| `pipeline` terminating fields | summary / QD / decomposition / confidence / refs | **same + recommended extras** |

---

## 8. Contract / hash map

| | base-1 | base-4 |
| --- | --- | --- |
| `_hash_policy.pointers` | instructions/*, masq, verbs, messages content | **same policy shape** (min may not materialize all pointer paths as top-level keys) |
| Excluded | guidance, contract, metadata, `_.*` | **same idea** |
| Production stamp | Hub verify on live Zeus | **still required** — prototype hashes are not prod |
| `contract` object | thin | prototype builder fields + parent notes |

Customs / injects still **outside** hash identity of BASE body.

---

## 9. Client / multi-round map

| Concern | base-1 era (typical) | base-4 docs |
| --- | --- | --- |
| Transcript | append `messages[]` | **same** — still append |
| Final answer | often free text or partial return | structured **Layer A** `return` |
| Admin telemetry | ad hoc / none in catalog | G2 fields on terminate |
| Business rules | inject text only | `rules[]` → `business_rules_triggers[]` |
| Session state bags | informal | A catalog / B injects / C messages / D artifacts |
| Guide | scattered | `MULTI_ROUND_CLIENT.md` + `multi_round_example.json` |

---

## 10. Size snapshot (analytics, illustrative)

| Pack | File form | ~bytes (analytics) |
| --- | --- | --- |
| base-1 min | JSON | ~17 KB |
| base-2-prototype | JSON | ~28 KB |
| base-3-prototype | text | ~24 KB |
| base-4 | JSON | ~27 KB |
| base-4 | text | ~24 KB |

Growth base-1 → base-2/4 is mostly **Layer A schema text + system addendum**, not more verbs.

---

## 11. Compatibility / migration cheat sheet

### Loaders that only know base-1

| Still works | May break / need updates |
| --- | --- |
| 13 verb **names** | Assuming `return` has only 4 properties (extra props are additive — usually OK) |
| Required 4 terminate fields | Filename globs `*_v2_min.json` only |
| OpenAI tool calling shape | Ignoring new recommended fields (product features missing) |
| | Treating prototype `contract.hash` as production stamp |

### Migrating a base-1 integration toward base-4

1. Keep validating **required four** fields (unchanged).  
2. Accept **additionalProperties** on `return` args.  
3. Optionally parse G2/G3; strip from UI.  
4. Switch file discovery to `*_base-4.json` (or pin path).  
5. Wire `business_injection.rules[]` if using triggers.  
6. Stamp on Hub before production — do not reuse prototype hashes.  
7. Read [BIBLE.md](../BIBLE.md) §10 checklists.

### What you do **not** need to relearn

- Zeus verb set (same 13)  
- Pipeline `@as.ids` idea  
- Evidence-loop intent of QD + decomposition  
- Scope brief / mini-schema as runtime injects  
- Append-only multi-round `messages[]`  

---

## 12. Concept rename / clarify table

| base-1 language | base-4 language |
| --- | --- |
| Evidence-loop return contract | **Terminate (Layer A)** |
| (nothing) | **G1 / G2 / G3** audiences |
| (nothing) | **wish_i_knew** (admin gaps) |
| (nothing) | **jail_break_attempt** float |
| (nothing) | **policy_action** |
| (nothing) | **business_rules_triggers** |
| min profile | still `profile: v2_min` |
| `*_v2_min.json` file | `*_base-4.json` file |
| Detective report | **Layer B** (server; not in BASE) |

---

## 13. Doc map across BASE lines

| Need | base-1 | base-4 |
| --- | --- | --- |
| What is a catalog | [docs/CHAT_REQUEST.md](../CHAT_REQUEST.md) | + [BIBLE.md](../BIBLE.md) |
| Assembled prompt | [docs/PROMPT_ASSEMBLY.md](../PROMPT_ASSEMBLY.md) · [diagram](../../images/assembled_prompt.svg) | Bible §1 |
| Terminate schema | implied by tools + prompt | `response_output_schema.json` |
| Multi-round Client | informal | `MULTI_ROUND_CLIENT.md` |
| Naming customs | — | Bible §2 + this guide §2 |
| This migration | — | **this file** |

---

## 14. Quick “am I on base-1 or base-4?” test

| Signal | base-1 | base-4 |
| --- | --- | --- |
| Filename | `*_v2_min.json` | `*_base-4.json` |
| `_lineage.base_id` | `base-1` | `base-4` |
| System has `## Terminate (Layer A) — copy this shape` | no | **yes** |
| System has both Evidence loop **and** Layer A prototype sections | no / only Evidence | **no** (merged) |
| `return` properties include `wish_i_knew` | no | **yes** |
| Folder `response_output_schema.json` | no | **yes** |

---

## 15. Recommended reading path (migrator)

1. This guide (orientation)  
2. [BIBLE.md](../BIBLE.md) (normative base-4)  
3. Diff mentally: base-1 Evidence loop ↔ base-4 Terminate table  
4. `response_output_schema.json` vs base-1 four fields  
5. `MULTI_ROUND_CLIENT.md` if building/updating Client  

---

**Bottom line:** base-4 keeps the **same 13 verbs and the same four required terminate fields** as base-1, adds **Client/admin control fields** and **clearer single Terminate contract**, renames files to **base-N**, and documents **multi-round append + artifacts**. Promote only after Hub stamp and Client checklist; until then base-1 remains production.
