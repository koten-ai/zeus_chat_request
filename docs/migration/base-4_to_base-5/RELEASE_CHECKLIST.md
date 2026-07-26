# RELEASE checklist — base-4 → base-5

**Copied from** [../RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md)  
**Kind:** **BREAKING** — last wire/control-plane freeze before prod on this line ([ROADMAP](../../ROADMAP.md) BASE change law)

| Field | Value |
| --- | --- |
| **From** | base-4 |
| **To** | base-5 |
| **Breaking?** | **yes** |
| **Pack yet?** | **yes** — `v2/base/base-5/` |
| **Pin after?** | no until stamp + Client + Detective |

```bash
python3 scripts/new_base.py --from v2/base/base-4 --base 5
# then work this list top to bottom
```

---

## 0. Pre-flight

- [x] COMPAT: pin still base-1; base-4 candidate; base-5 design/last break  
- [x] ROADMAP § base-5 (breaking freeze + frozen surfaces)  
- [x] [README.md](README.md) hop status  
- [x] Do **not** flip `CURRENT.json` in this hop  
- [x] CR epic exists for base-5 (**CR-3**)  

---

## 1. Pack — `v2/base/base-5/` (when scaffolding)

- [x] `min/chat_request_<mode>_base-5.json` all modes from base-4  
- [x] `text/*_base-5.txt` regenerated  
- [x] `MANIFEST.json` lists all min + paths (`docs/BIBLE.md`, migration, playbook)  
- [x] `response_output_schema.json` — **object** `business_rules_triggers`; optional `app_output`  
- [x] `response_output_example.json` validates; uses object triggers / sample `app_output` if shown  
- [x] Thin README / OVERVIEW: base-5 theme + links to ROADMAP / RULES_OBJECT / PROMPT_SETTINGS  
- [x] `_lineage.base_id` = `base-5`  
- [x] Names `*_base-5.json`  
- [x] Doc pointers → `docs/…` (not old pack-local BIBLE)  
- [x] `_format: zeus.chat_request.v2`  
- [x] No invented `contract_hash`  
- [x] Terminate table in system prompt: objects + output_request notes  
- [x] `return` / pipeline params **in sync** with schema  

---

## 2. Scripts / regenerate (Phase D)

- [x] `python3 scripts/new_base.py --from v2/base/base-4 --base 5`  
- [x] Diet min JSON (objects, Terminate, schema-linked tool params)  
- [x] `export_base_text.py --from v2/base/base-5/min --base 5 --out v2/base/base-5 --no-set-base-id`  
- [x] `new_base.py --refresh-manifest --base 5`  
- [x] `scan_catalogs.py`  
- [x] **`python3 scripts/verify_base_pack.py --base 5` → OK**  
- [ ] Root manifest/index if applicable  

---

## 3. Docs / markdown

### Hop

- [x] `docs/migration/base-4_to_base-5/README.md`  
- [x] `GUIDE.md` — stayed / moved / added (fill when pack real)  
- [x] `lessons-learned.md` (after first real diet)  
- [x] **This RELEASE_CHECKLIST.md**  
- [x] `docs/migration/README.md` indexes this hop  

### Living design (already mostly written — re-check when pack ships)

- [x] ROADMAP base-5 = last breaking train  
- [ ] ROADMAP success signals (partial — pack shipped; Client/Zeus open)  
- [x] BASE_AGENT_PLAYBOOK §2.3 + §4.2 still accurate  
- [x] RULES_OBJECT: object rules + type+description output_request  
- [x] PROMPT_SETTINGS: settings + policy table + merge/freeze  
- [x] JAILBREAK: named rules pack  
- [ ] BIBLE: either still “base-4 era + base-5 design” or bump when base-5 is normative  
- [x] Doc banners: design line includes base-5 candidate when pack exists  

### Release + matrix

- [x] `RELEASE_NOTES.md` — **breaking** table (arrays→objects, app_output, settings contract)  
- [x] `COMPAT.md` — base-5 triple + object-only Client floor + dual-read ≤1 release  
- [ ] AGENTS.md / docs/README if labels change  

---

## 4. Format / naming

- [x] `chat_request_<mode>_base-5.json` / `.txt`  
- [x] Customs: pattern documented `…_base-5_cus_<bucket>_<scope>-<rev>.json`  
- [ ] Inspector Diff: analytics (or any mode) **base-4 vs base-5**  

---

## 5. Content correctness (base-5 theme)

| Check | Pass if |
| --- | --- |
| Rules | `{ id: "one sentence" }` only — **not** `string[]` as SoT |
| Triggers | `{ id: bool }` sparse — **not** `boolean[]` as SoT |
| Dual-read | Documented ≤1 Client release; prefer none |
| company_context | Documented inject · ≤150/250 words |
| Jailbreak pack | Named keys in rules object ([JAILBREAK_POLICY](../../JAILBREAK_POLICY.md)) |
| message_* / policy_action | Soft-require mapping documented |
| output_request | Each field **type + description**; type-only rejected |
| app_output | Values only on terminate; Client validates types |
| Settings bag | Normative Client keys ([PROMPT_SETTINGS](../../PROMPT_SETTINGS.md)) |
| Policy table | Runs every terminate; triggers = signals |
| Merge/freeze | SDK ∪ tenant ∪ request; no silent default-key delete |
| Helios Pri-1 | Zeus/Client report emits — **not** new required Layer A fields |
| Frozen after ship | No base-6 wire rename of objects/app_output without new major |

- [x] Pack system prompt + schema reflect object triggers / app_output / inject notes (Client implement open)  

---

## 6. External

### Zeus

- [ ] Generator / snapshot can emit base-5 lineage  
- [ ] Return schema allows object triggers + app_output  
- [ ] Detective: required four; optional fields policy  
- [ ] Loaders accept `*_base-5.json`  
- [ ] Do not require Helios Pri-1 as model fields  

### zeus_client

- [ ] Object rules inject + object triggers parse  
- [ ] settings bag + policy table  
- [ ] output_request → prompt block from **descriptions**  
- [ ] validate app_output types  
- [ ] dual-read arrays ≤1 release then remove  
- [ ] G2 never UI; tool JSON untrusted  
- [ ] COMPAT Client floor when version ships  

---

## 7. Verify (Client trial) (Phase D + trial)

- [x] **`python3 scripts/verify_base_pack.py --base 5` OK**  
- [ ] schema validates example (structural gate done; full jsonschema optional)  
- [x] scan_catalogs clean  
- [ ] Diff base-4 vs base-5  
- [x] No invent hash  
- [ ] Refuse / coupon-style policy path smoke (docs examples)  

---

## 8. Pin gate (later)

- [ ] Hub stamp  
- [ ] Client spike green  
- [ ] Detective green  
- [ ] CURRENT → base-5 only with explicit promote  
- [ ] Pin epic **CR-18** prerequisites only (not same as pack ship)  

---

## 9. Jira / CR board (Phase J — after pack ship)

**Board:** [CR board 48](https://kotenai.atlassian.net/jira/software/projects/CR/boards/48)

- [x] Update epic **CR-3** — pack shipped, PR #5/#6, residual open, pin still base-1  
- [x] Transition **CR-3** → In Progress  
- [x] Comment on **CR-3** with ship notes + PR links  
- [x] Update children **CR-9…CR-12** — pack/docs vs Client/Zeus split; links → `main`  
- [x] Create residual under CR-3:  
  - [x] **CR-19** process verify + phased checklist (PR #6)  
  - [x] **CR-20** zeus_client base-5 implement  
  - [x] **CR-21** Zeus loaders / Detective / return schema  
  - [x] **CR-22** pack docs completion tracker  
- [x] Link **CR-20** + **CR-21** **blocks** **CR-18** (pin)  
- [x] Update **CR-4** (base-6) depends-on + additive-only  
- [x] Update **CR-18** pin prerequisites  

---

## Sign-off

| Role | Name | Date |
| --- | --- | --- |
| Catalog / docs | | |
| Zeus | | |
| zeus_client | | |
| CR board hygiene | 2026-07-26 | |
