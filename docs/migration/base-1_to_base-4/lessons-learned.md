# Lessons learned: mapping / migrating base-1 → base-4

**Audience:** humans and AIs doing the next BASE bump (base-5, base-6, …)  
**Context:** First real pass from production **base-1** min catalogs through prototypes **base-2 → base-3 → base-4**, plus inspector/`index.html` dual-BASE testing.  
**Related:** [GUIDE.md](GUIDE.md) · [BIBLE.md](../../BIBLE.md) · [INSPECTOR.md](../../INSPECTOR.md) · [ROADMAP.md](../../ROADMAP.md)

This is **experience**, not a second spec. Prefer the Bible for requirements; use this to avoid repeating mistakes.

---

## 1. Separate three different “payloads” early

The biggest confusion cost was treating **one JSON** as one concept.

| Layer | What it is | Who fills it | Size order |
| --- | --- | --- | --- |
| **Assembled prompt** | Catalog + injects + user + history | Client at request time | Can blow 10KB → 60KB+ |
| **Layer A terminate** | `return` tool args | Model | ~0.3–1.5 KB when healthy |
| **Layer B Detective** | report, diagnosis, spans, inject_inspect… | Zeus server | ~100KB–1MB |

**Lesson:** Do not compare Detective dumps to Layer A schema size. Do not ask the model to emit Layer B. Migration docs should label A vs B vs injects in the first page.

---

## 2. Same four required fields; migration is mostly *additive*

base-1 and base-4 share:

```text
summary · query_decomposition · decomposition · confidence
```

and the same **13 verb names**.

**Lesson:** Lead with “what did *not* change.” Migrators panic less. Base-4 risk is **optional fields ignored**, not a total protocol break — unless loaders hardcode `*_v2_min.json` only.

---

## 3. Filename ≠ envelope

| Concept | Example |
| --- | --- |
| Envelope | `_format: "zeus.chat_request.v2"` (stays) |
| base-1 file | `chat_request_analytics_v2_min.json` |
| base-4 file | `chat_request_analytics_base-4.json` |

**Lesson:** Put **BASE id in the filename** for base-2+; keep `v2` only as format. Customs:

```text
chat_request_<mode>_base-4_cus_<bucket>_<scope>-<rev>.json
```

Normalize `_default` → `default`. Bumping custom rev is **not** a new BASE.

---

## 4. Two terminate essays were worse than one longer table

base-2 added Layer A on top of Evidence-loop prose → **duplicate contracts**, easy to drop “recommended” fields.

base-4 merged into:

```text
## Terminate (Layer A) — copy this shape
  field table + one-line distinctions + one full example
```

**Lesson:** For model (and human) comprehension, **one surface + one copy-paste example** beats two narratives. Char count barely dropped (~100); **clarity** was the win, not tokens.

---

## 5. Easy-to-read fields ≠ high emit priority

`wish_i_knew`, dual confidence, `business_rules_triggers` are **easy to understand** and **easy to skip** under multi-round pressure.

**Lesson:**

- Required four stay hard requirements (Detective already grades them).  
- Recommended fields need an **example skeleton that always shows them** (`wish_i_knew: []`).  
- Don’t expect perfect calibration on `jail_break_attempt` (subjective float).  
- `business_rules_triggers` is useless without Client `rules[]` inject.

---

## 6. Text packs help *editing*; they don’t always cut tokens in half

| Form | Role |
| --- | --- |
| JSON | Source of truth, stamp, Client load, inspector |
| Indented `.txt` (base-3/4) | Diet/edit surface for humans/LLMs |

Measured analytics: text vs **pretty** JSON ~15% smaller; vs **compact** JSON text can be **larger**.

**Lesson:** Use text for **rework loops** (`scripts/export_base_text.py --base N`). Don’t sell “txt = half tokens” as a guarantee. Token wins come from **deleting sections**, not reformatting braces.

---

## 7. Multi-round Client still appends `messages[]`

The classic middleman pattern remains correct:

```text
messages.append(user)
messages.append(assistant tool_calls)
messages.append(tool results)   # Zeus JSON
…
messages.append(return)         # Layer A at end
```

**Lesson:** Don’t replace the array with a new transport. Add **bags**:

- **C** transcript (append)  
- **D** artifacts (UI tables, entity map, `last_terminate`)  
- **G2** metrics only (never UI)  
- **G3** triggers → control flags  

Zeus rows belong in tool messages **and** Client enrichment copies; model `summary` should not re-serialize full tables.

---

## 8. Inspector: one `index.html`, not `index-base-4.html`

For the first migration test, **Diff / Matrix** on a single inspector is the product.

**Lessons:**

1. Rescan after adding JSON: `python3 scripts/scan_catalogs.py`.  
2. Fix `mode_from_name` for `*_base-N.json` and `*_cus_*` (otherwise mode becomes `analytics_base-4` when lineage is missing). Prefer `_lineage.mode` when present.  
3. Dropdown labels need **folder · mode · base_id** so base-1 and base-4 are obvious.  
4. A second HTML fork would fight Diff and double maintenance. Fork only later for a **Client lab** UI, sharing one JS core.

See [INSPECTOR.md](../../INSPECTOR.md).

---

## 9. Scan / tooling assumptions break silently

| Pitfall | What we hit |
| --- | --- |
| Glob `*_v2_min.json` | Misses base-4 files |
| Mode regex only strips `_v2_min` | Mis-labels `*_base-4.json` |
| Stale `catalog-index.json` | UI shows 20 files, not 40 |
| Docker volume on wrong tree | Container serves old catalogs |

**Lesson:** Every BASE bump checklist: **rename pattern + scan + index + one Diff smoke test**.

---

## 10. Production pin vs prototype pin

| Pin | Meaning |
| --- | --- |
| `CURRENT.json` / `v2/min` | Still **base-1** until you promote |
| base-2/3/4-prototype | Design + diet + docs — **not** Hub stamps |

**Lesson:** Prototype `contract.hash` is for development only. Migration is not complete until:

1. Client validates Layer A (required + optional)  
2. Hub stamp path works  
3. Pin / sync points at the new BASE (or customs)  
4. 409 drift story still “resync, don’t invent hash”

---

## 11. Process that worked (repeat for base-5+)

```text
1. Decide the *one* clarity win (e.g. single Terminate table)
2. Apply to JSON catalogs (source of truth)
3. export_base_text.py --base N          # text pack for review
4. Update BIBLE + mapping guide + samples
5. scan_catalogs.py + Diff base-(N-1) vs N in index.html
6. Capture lessons-learned (this file pattern)
7. Only then talk production pin
```

Generator:

```bash
python3 scripts/export_base_text.py --from v2/base/base-4/min --base 5
```

---

## 12. What we would do differently next time

1. **Write Layer A schema + one example *before* expanding system prose.**  
2. **Never add a second terminate section** — extend the table only.  
3. **Fix filename/mode scan in the same PR as the first `*_base-N.json`.**  
4. **Keep a living mapping guide** from day one of a BASE bump (not after base-4).  
5. **Measure prompt size by assembled zones** (system / verbs / inject / tools), not only catalog file bytes.  
6. **Client multi-round bags (A–D)** documented next to Layer A so middleman doesn’t invent a parallel schema.

---

## 13. One-line takeaways

| Topic | Takeaway |
| --- | --- |
| A vs B | Model terminate ≠ Detective store |
| Required | Same four fields as base-1 |
| Optional | Easy to read, easy to drop — show in example |
| Naming | BASE in stem; `v2` in `_format` only |
| Diet | Clarity over clever compression |
| Text pack | Edit surface, not automatic half-size |
| Client | Still `messages.append`; add artifacts |
| Inspector | One index.html; Diff is the migration test |
| Tooling | Rescan + mode parse or BASE is invisible |
| Ship | Stamp + pin last; prototype first |

---

## 14. Pointers

| Doc | Use |
| --- | --- |
| [GUIDE.md](GUIDE.md) | Field/section mapping tables |
| [BIBLE.md](../../BIBLE.md) | Normative base-4 requirements |
| [MULTI_ROUND_CLIENT.md](../../MULTI_ROUND_CLIENT.md) | Append loop + examples |
| [response_output_schema.json](../../../v2/base/base-4/response_output_schema.json) | Layer A machine schema |
| [INSPECTOR.md](../../INSPECTOR.md) | Running Diff base-1 vs base-4 |

---

*Captured after the first base-1 → base-4 migration pass (catalog diet, Client model, inspector dual-BASE). Update this file when base-5 lands with anything that surprised you.*
