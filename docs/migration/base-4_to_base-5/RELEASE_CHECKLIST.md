# RELEASE checklist — base-4 → base-5

**Copied from** [../RELEASE_CHECKLIST_TEMPLATE.md](../RELEASE_CHECKLIST_TEMPLATE.md)  
**Kind:** **BREAKING** — last wire/control-plane freeze before prod on this line ([ROADMAP](../../ROADMAP.md) BASE change law)

| Field | Value |
| --- | --- |
| **From** | base-4 |
| **To** | base-5 |
| **Breaking?** | **yes** |
| **Pack yet?** | no until `new_base.py --from v2/base/base-4 --base 5` |
| **Pin after?** | no until stamp + Client + Detective |

```bash
python3 scripts/new_base.py --from v2/base/base-4 --base 5
# then work this list top to bottom
```

---

## 0. Pre-flight

- [ ] COMPAT: pin still base-1; base-4 candidate; base-5 design/last break  
- [ ] ROADMAP § base-5 (breaking freeze + frozen surfaces)  
- [ ] [README.md](README.md) hop status  
- [ ] Do **not** flip `CURRENT.json` in this hop  

---

## 1. Pack — `v2/base/base-5/` (when scaffolding)

- [ ] `min/chat_request_<mode>_base-5.json` all modes from base-4  
- [ ] `text/*_base-5.txt` regenerated  
- [ ] `MANIFEST.json` lists all min + paths (`docs/BIBLE.md`, migration, playbook)  
- [ ] `response_output_schema.json` — **object** `business_rules_triggers`; optional `app_output`  
- [ ] `response_output_example.json` validates; uses object triggers / sample `app_output` if shown  
- [ ] Thin README / OVERVIEW: base-5 theme + links to ROADMAP / RULES_OBJECT / PROMPT_SETTINGS  
- [ ] `_lineage.base_id` = `base-5`  
- [ ] Names `*_base-5.json`  
- [ ] Doc pointers → `docs/…` (not old pack-local BIBLE)  
- [ ] `_format: zeus.chat_request.v2`  
- [ ] No invented `contract_hash`  
- [ ] Terminate table in system prompt: objects + output_request notes  
- [ ] `return` / pipeline params **in sync** with schema  

---

## 2. Scripts / regenerate

- [ ] `python3 scripts/new_base.py --from v2/base/base-4 --base 5`  
- [ ] Diet min JSON (objects, Terminate, schema-linked tool params)  
- [ ] `export_base_text.py --from v2/base/base-5/min --base 5 --out v2/base/base-5 --no-set-base-id`  
- [ ] `new_base.py --refresh-manifest --base 5`  
- [ ] `scan_catalogs.py`  
- [ ] Root manifest/index if applicable  

---

## 3. Docs / markdown

### Hop

- [x] `docs/migration/base-4_to_base-5/README.md`  
- [ ] `GUIDE.md` — stayed / moved / added (fill when pack real)  
- [ ] `lessons-learned.md` (after first real diet)  
- [x] **This RELEASE_CHECKLIST.md**  
- [x] `docs/migration/README.md` indexes this hop  

### Living design (already mostly written — re-check when pack ships)

- [x] ROADMAP base-5 = last breaking train  
- [ ] ROADMAP success signals checked off as work completes  
- [ ] BASE_AGENT_PLAYBOOK §2.3 + §4.2 still accurate  
- [ ] RULES_OBJECT: object rules + type+description output_request  
- [ ] PROMPT_SETTINGS: settings + policy table + merge/freeze  
- [ ] JAILBREAK: named rules pack  
- [ ] BIBLE: either still “base-4 era + base-5 design” or bump when base-5 is normative  
- [ ] Doc banners: design line includes base-5 candidate when pack exists  

### Release + matrix

- [ ] `RELEASE_NOTES.md` — **breaking** table (arrays→objects, app_output, settings contract)  
- [ ] `COMPAT.md` — base-5 triple + object-only Client floor + dual-read ≤1 release  
- [ ] AGENTS.md / docs/README if labels change  

---

## 4. Format / naming

- [ ] `chat_request_<mode>_base-5.json` / `.txt`  
- [ ] Customs: `…_base-5_cus_<bucket>_<scope>-<rev>.json`  
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

- [ ] All rows above reflected in pack system prompt + schema + Client docs  

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

## 7. Verify (Client trial)

- [ ] schema validates example  
- [ ] scan_catalogs clean  
- [ ] Diff base-4 vs base-5  
- [ ] No invent hash  
- [ ] Refuse / coupon-style policy path smoke (docs examples)  

---

## 8. Pin gate (later)

- [ ] Hub stamp  
- [ ] Client spike green  
- [ ] Detective green  
- [ ] CURRENT → base-5 only with explicit promote  

---

## Sign-off

| Role | Name | Date |
| --- | --- | --- |
| Catalog / docs | | |
| Zeus | | |
| zeus_client | | |
