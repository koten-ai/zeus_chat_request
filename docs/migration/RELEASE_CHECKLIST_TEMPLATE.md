# BASE bump release checklist (template)

**Copy to:** `docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md`  
**Meaning:** readiness to **trial / ship this BASE bump** (pack + docs + COMPAT + RELEASE_NOTES + Zeus/Client) — not only a git tag.

| Field | Fill |
| --- | --- |
| **From** | `base-X` |
| **To** | `base-Y` |
| **Breaking?** | yes / no (if no, base-6+ additive law) |
| **Owner** | |
| **Date** | |

**Commands:** [CREATE_BASE.md](../CREATE_BASE.md) · [BASE_AGENT_PLAYBOOK.md](../BASE_AGENT_PLAYBOOK.md) · [COMPAT.md](../../COMPAT.md)

```bash
# scaffold pack
python3 scripts/new_base.py --from v2/base/base-X --base Y
```

---

## 0. Pre-flight

- [ ] Read [COMPAT.md](../../COMPAT.md) — pin vs candidate vs design  
- [ ] Read [ROADMAP.md](../ROADMAP.md) for base-Y theme  
- [ ] Confirm **breaking vs additive** (base-5 = last break; base-6+ additive only)  
- [ ] Read hop notes if any: `docs/migration/base-X_to_base-Y/`  
- [ ] Know production pin still (`CURRENT.json`) — do **not** flip until §9  

---

## 1. Pack on disk — `v2/base/base-Y/`

- [ ] `min/chat_request_<mode>_base-Y.json` for every mode parent had  
- [ ] `text/chat_request_<mode>_base-Y.txt` regenerated and readable  
- [ ] `MANIFEST.json` — schema_version 2, catalogs[], paths to docs  
- [ ] `response_output_schema.json` present  
- [ ] `response_output_example.json` present and **validates** against schema  
- [ ] Thin `README.md` (pack index → docs, not a second Bible)  
- [ ] Thin `OVERVIEW.md` (what changed in Y only)  
- [ ] `_lineage.base_id` = `base-Y` on all min JSON  
- [ ] File stems / names match `chat_request_<mode>_base-Y.json`  
- [ ] `_note` / `_base_meta.docs` point at **current** doc paths (`docs/…`)  
- [ ] Envelope still `_format: "zeus.chat_request.v2"`  
- [ ] **No invented** production `contract_hash`  
- [ ] `return` / terminating `pipeline` tool params in min JSON **match** `response_output_schema.json`  

---

## 2. Scripts / regenerate

- [ ] Scaffold: `python3 scripts/new_base.py --from v2/base/base-X --base Y`  
- [ ] After diet:  
  `python3 scripts/export_base_text.py --from v2/base/base-Y/min --base Y --out v2/base/base-Y --no-set-base-id`  
- [ ] `python3 scripts/new_base.py --refresh-manifest --base Y`  
- [ ] `python3 scripts/scan_catalogs.py` (inspector `catalog-index.json`)  
- [ ] Root `manifest.json` updated if it lists packs  

---

## 3. Docs / markdown (this repo)

### Migration hop

- [ ] `docs/migration/base-X_to_base-Y/README.md` — status, links  
- [ ] `docs/migration/base-X_to_base-Y/GUIDE.md` — stayed / moved / added  
- [ ] `docs/migration/base-X_to_base-Y/lessons-learned.md` (recommended)  
- [ ] **This file** filled: `docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md`  
- [ ] `docs/migration/README.md` index row for X→Y  

### Living design / process

- [ ] `docs/ROADMAP.md` — Y status + success signals  
- [ ] `docs/BASE_AGENT_PLAYBOOK.md` — §2 comply card for Y + §4 jump row  
- [ ] `AGENTS.md` / `docs/README.md` if pin or design line label changes  
- [ ] Design SoT updated if wire changed:  
  - [ ] `docs/BIBLE.md` (or successor when Y is normative)  
  - [ ] `docs/PROMPT_ASSEMBLY.md`  
  - [ ] `docs/PROMPT_SETTINGS.md`  
  - [ ] `docs/RULES_OBJECT_AND_OUTPUT_REQUEST.md`  
  - [ ] `docs/JAILBREAK_POLICY.md`  
  - [ ] `docs/MULTI_ROUND_CLIENT.md` (if multi-round contract changed)  
- [ ] Doc status banners: pin / design line / last reviewed  

### Release + matrix

- [ ] `RELEASE_NOTES.md` — highlights + **breaking** table if any  
- [ ] `COMPAT.md` — supported triples + feature capability row for Y  
- [ ] Client dual-read / floor notes if breaking  

---

## 4. Format / naming

- [ ] BASE: `chat_request_<mode>_base-Y.json` / `.txt`  
- [ ] Custom: `…_base-Y_cus_<bucket>_<scope>-<rev>.json`  
- [ ] Legacy pin only if still base-1: `*_v2_min.json`  
- [ ] Inspector Diff: same mode **base-X vs base-Y** looks sane  

---

## 5. Content correctness (theme of Y)

_Fill for this hop — see hop-specific RELEASE_CHECKLIST for base-5._

- [ ] Theme of Y applied in Terminate table / system prompt (not only README)  
- [ ] Layer A schema matches theme  
- [ ] No accidental copy of old wire shapes as SoT (e.g. arrays if Y is objects)  
- [ ] Helios: no new **required** AI Layer A tax unless ROADMAP says so  

---

## 6. External repos

### Zeus engine

- [ ] Snapshot / generator emits `base-Y` lineage  
- [ ] PIN / publish path aware of candidate vs pin  
- [ ] Hash strip still correct  
- [ ] `return` / pipeline tool schema matches pack  
- [ ] Detective: required four; optional field policy  
- [ ] Loaders: `*_base-N.json` + legacy if needed  
- [ ] COMPAT / base_id warnings if any  

### zeus_client

- [ ] Load base-Y filenames  
- [ ] Parse/validate Layer A for Y  
- [ ] G1/G2/G3 redaction  
- [ ] Injects (rules shape, company_context, output_request, settings)  
- [ ] Dual-read policy if breaking (≤1 release)  
- [ ] Package version / COMPAT Client column when shipped  

---

## 7. Verify (green bar for Client trial)

- [ ] Example validates: schema ↔ example  
- [ ] `scan_catalogs.py` clean  
- [ ] Inspector Diff X vs Y  
- [ ] No production hash invented  
- [ ] CREATE_BASE “Client trial” items done  

---

## 8. Pin gate (usually later — not same day as scaffold)

- [ ] Hub stamp on real cluster  
- [ ] Client spike green  
- [ ] Detective green  
- [ ] `CURRENT.json` + `v2/min` only after explicit promote  

---

## Sign-off

| Role | Name | Date |
| --- | --- | --- |
| Catalog / docs | | |
| Zeus | | |
| zeus_client | | |
