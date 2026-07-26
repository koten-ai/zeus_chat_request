# BASE agent playbook — comply & upgrade

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · candidate pack **base-5** · prior candidate **base-4** · version matrix: [COMPAT.md](../COMPAT.md)

**Audience:** coding agents (and humans) changing **catalogs**, **Zeus engine**, or **zeus_client** for a given `base-N`.  
**Not:** a second Bible or Roadmap — **procedures + checklists** only. Depth lives in linked SoT docs.

| Entry | Link |
| --- | --- |
| Short start | [../AGENTS.md](../AGENTS.md) |
| Versions | [../COMPAT.md](../COMPAT.md) |
| Migration hops | [migration/README.md](migration/README.md) → `migration/base-X_to_base-Y/` |
| Scaffold pack | [CREATE_BASE.md](CREATE_BASE.md) |

---

## 0. Hard rules

1. Never invent production `contract_hash`.  
2. Pin last (`CURRENT.json`).  
3. BASE ≠ Zeus semver ≠ Client version.  
4. Pack = `v2/base/base-N/`; design = `docs/`; hops = `docs/migration/base-X_to_base-Y/`.  
5. Required four always: `summary`, `query_decomposition`, `decomposition`, `confidence`.  
6. G2 admin never in chat UI; tool JSON is untrusted data.

---

## 1. Detect which BASE you are on

| Signal | Where | Means |
| --- | --- | --- |
| Production pin | `CURRENT.json` → `base_id` | What prod clients should use |
| Pack present | `v2/base/base-N/` + `_lineage.base_id` | Catalogs on disk |
| Compat row | [COMPAT.md](../COMPAT.md) | Supported / candidate / design |
| Design only | [ROADMAP.md](ROADMAP.md) | Spec without pack (base-6+ themes until scaffolded) |

```text
Pin base-1  +  packs base-4 + base-5 on disk
→ production still base-1; trials may use base-4 or base-5 candidate; pin last
```

---

## 2. Comply with `base-X`

For each track (catalog / Zeus / Client), complete the checklist for **your target BASE**.

### 2.1 base-1 (production pin)

| Track | Must | Must not |
| --- | --- | --- |
| **Catalog** | Load `v2/min/` or `v2/base/base-1/min/`; `*_v2_min.json`; required four | Treat base-4 files as pin |
| **Zeus** | Stamp/hash path for min catalogs; Detective core four | Require base-4-only fields as hard fail on pin |
| **Client** | Bind contract; parse required four; multi-round `messages[]` | Invent hash; show admin scores in UI |

**SoT:** [CHAT_REQUEST.md](CHAT_REQUEST.md) · [COMPAT.md](../COMPAT.md)

### 2.2 base-4 (candidate pack)

| Track | Must | Must not |
| --- | --- | --- |
| **Catalog** | `v2/base/base-4/min/*_base-4.json`; one Terminate table; Layer A schema at pack root | Put long essays in the pack folder |
| **Zeus** | Accept extended `return` / terminating pipeline properties as **optional**; lineage `base_id`; loaders accept `*_base-N.json` | Break base-1 pin path |
| **Client** | Validate required four; map optional G2/G3; `business_rules_triggers` as **array** (index-aligned) if present; redaction G1 only for UI | Require object triggers (that is base-5) |

**SoT:** [BIBLE.md](BIBLE.md) · pack [response_output_schema.json](../v2/base/base-4/response_output_schema.json) · hop [migration/base-1_to_base-4/](migration/base-1_to_base-4/)

**Client quick list (base-4):**

- [ ] Parse recommended: `policy_action`, `subject_confidence`, `jail_break_attempt`, `wish_i_knew`, `business_rules_triggers[]`  
- [ ] Never put G2 in chat UI  
- [ ] Prefer `policy_action` → `message_*` chrome when brand inject present  

**Zeus quick list (base-4):**

- [ ] Return tool schema allows extra Layer A properties  
- [ ] Detective: required four; optional fields warn not fail (product choice)  
- [ ] Snapshot/publish can emit `base-4` lineage  

### 2.3 base-5 (**candidate pack** — last breaking train)

| Track | Must | Notes |
| --- | --- | --- |
| **Catalog** | Use **`v2/base/base-5/`**; object triggers + optional `app_output` in schema/tools | No array SoT |
| **Zeus** | Accept object triggers + optional `app_output`; optional Detective soft-require | Don’t require Helios Pri-1 on Layer A |
| **Client** | Settings bag; merge/freeze; **object** triggers; `output_request` type+description; policy table | Dual-read arrays **≤1 release** then **remove** |

**Law:** base-5 freezes the wire. **base-6+ must be additive/optional only** ([ROADMAP.md](ROADMAP.md) BASE change law).

**SoT:** pack [`v2/base/base-5/`](../v2/base/base-5/) · [ROADMAP.md](ROADMAP.md) · [RULES_OBJECT…](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · hop [migration/base-4_to_base-5/](migration/base-4_to_base-5/)

---

## 3. Upgrade `base-X` → `base-Y` (generic recipe)

Execute in order. Skip only if the hop folder says “design only” and you are not scaffolding yet.

```text
0. Copy docs/migration/RELEASE_CHECKLIST_TEMPLATE.md
     → docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md  (phases A–G)
1. Read COMPAT.md + ROADMAP (for Y)
2. Read docs/migration/base-X_to_base-Y/  (GUIDE + lessons if present)
3. Scaffold pack (when Y is a real pack):
     python3 scripts/new_base.py --from v2/base/base-X --base Y
4. DIET Y deltas (Terminate table, Layer A schema, verb params, inject contracts)
     — scaffold copies parent wire; never ship undieted
5. Re-export text; refresh MANIFEST; scan_catalogs
6. VERIFY (P0):
     python3 scripts/verify_base_pack.py --base Y   # must OK before pack PR
7. Zeus engine: snapshot / PIN / Detective / loaders / return schema (see §5; often separate ticket)
8. zeus_client: parse/validate new fields; dual-read only if X→Y break and ≤1 release; redaction; policy table
9. Update COMPAT.md triples + feature table + RELEASE_NOTES.md
10. Ensure hop folder complete:
     GUIDE.md + lessons-learned.md + RELEASE_CHECKLIST.md
11. Update this playbook: §2 card for Y + §4 jump row
12. Inspector Diff: same mode base-X vs base-Y
13. Jira / CR board (Phase J): update base-Y epic, create residual
    zeus_client + Zeus stories, blocks pin epic — checklist §9
    Board: https://kotenai.atlassian.net/jira/software/projects/CR/boards/48
14. Client spike + Hub stamp BEFORE CURRENT.json pin flip
```

**Master checklist:** [migration/RELEASE_CHECKLIST_TEMPLATE.md](migration/RELEASE_CHECKLIST_TEMPLATE.md) · base-5: [migration/base-4_to_base-5/RELEASE_CHECKLIST.md](migration/base-4_to_base-5/RELEASE_CHECKLIST.md)

### 3.1 Where deltas live

| Y state | Primary delta source |
| --- | --- |
| Hop archived | `docs/migration/base-X_to_base-Y/GUIDE.md` |
| Design only | [ROADMAP.md](ROADMAP.md) + design docs linked from hop README |
| Scaffold only | [CREATE_BASE.md](CREATE_BASE.md) then fill GUIDE |

---

## 4. Jump table

| Jump | Migration path | Status | Comply card |
| --- | --- | --- | --- |
| base-1 → base-4 | [migration/base-1_to_base-4/](migration/base-1_to_base-4/) | Candidate pack | §2.1 → §2.2 |
| base-4 → base-5 | [migration/base-4_to_base-5/](migration/base-4_to_base-5/) | **Candidate pack** (breaking freeze shipped; pin still base-1) | §2.2 → §2.3 |
| base-5 → base-6+ | (add hop only if needed) | **Additive only** by default | No wire rename/remove |

### 4.1 base-1 → base-4 (summary)

| Area | Delta |
| --- | --- |
| Catalog | `*_base-4.json`; one Terminate table; recommended Layer A on return tool |
| Zeus | Optional extra return properties; lineage |
| Client | Optional G2/G3; array triggers |

**Detail:** [migration/base-1_to_base-4/GUIDE.md](migration/base-1_to_base-4/GUIDE.md) · [lessons-learned.md](migration/base-1_to_base-4/lessons-learned.md)

### 4.2 base-4 → base-5 (summary — **breaking**; take all wire pain here)

| Area | Delta |
| --- | --- |
| Catalog | Named `rules{}`; object triggers **only**; company_context; output_request |
| Zeus | Prefer not to grow always-on AI fields; Detective soft-require policy TBD |
| Client | Merge/freeze; settings bag; type+description → prompt; policy table; drop array dual-read ASAP |

**After this hop:** only additive/optional BASE changes until a new major is justified.

**Detail:** [ROADMAP.md](ROADMAP.md) · [RULES_OBJECT…](RULES_OBJECT_AND_OUTPUT_REQUEST.md) · [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) · [migration/base-4_to_base-5/](migration/base-4_to_base-5/)

---

## 5. Zeus engine touchpoints (every BASE bump)

Search/update these **areas** in the Zeus repo (names vary; treat as checklist):

| Area | Why |
| --- | --- |
| AI snapshot / catalog generator | Emits min JSON + lineage `base_id` |
| PIN / publish to zeus_chat_request | What becomes pin vs candidate |
| Hash strip / `_hash_policy` | Contract stability |
| `return` / terminating `pipeline` tool JSON Schema | Must match pack `response_output_schema.json` |
| Detective / Layer A grading | Required four; optional field policy |
| Filename loaders | `*_v2_min.json` and `*_base-N.json` and customs |
| Compat / base_id warnings | Align with COMPAT.md (later hard gates) |
| Admin Workbench stamp | Production hashes only from Hub |

Do **not** invent Zeus Version bumps solely for docs; bump engine when behavior/schema requires it, then update COMPAT.

---

## 6. zeus_client touchpoints (every BASE bump)

| Area | Why |
| --- | --- |
| Catalog load path | min vs base-N filenames |
| Layer A parse + validate | Required four + optional fields for that BASE |
| G1/G2/G3 redaction | UI safety |
| Injects | company_context, rules shape, output_request |
| Multi-round | messages append, artifacts, Client clock |
| Policy table | base-5: triggers → flags → message_* |
| Package version | Bump only when behavior ships; update COMPAT Client column |

**Prioritized backlog (Requests):** [ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md](ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) (`ZC-WISH-*`, base-5 floor first).

---

## 7. Agent reading order

```text
1. AGENTS.md
2. COMPAT.md
3. This playbook (§2 or §3 only)
4. docs/migration/base-X_to_base-Y/ if upgrading
5. BIBLE / ROADMAP / RULES / SETTINGS as linked
6. v2/base/base-N/ pack
```

---

## 8. Anti-patterns

| Don’t | Do |
| --- | --- |
| Invent `contract_hash` | Hub stamp / sync |
| Flip CURRENT early | Client spike + Diff + stamp first |
| Put BIBLE inside pack folder | Link to `docs/` |
| Create `docs/base-4_to_base-5_guide.md` at root | Use `docs/migration/base-4_to_base-5/` |
| Mix base-4 array triggers with base-5 object API without dual-read | Document dual-read in COMPAT + Client |
| Copy Helios Pri-1 into always-on Layer A | Cheap Zeus/Client emits ([HELIOS wishlist](HELIOS_WISHLIST_FOR_CHAT_REQUEST.md)) |

---

## 9. Template — new hop `base-X` → `base-Y`

When a hop becomes real:

```bash
mkdir -p docs/migration/base-X_to_base-Y
cp docs/migration/RELEASE_CHECKLIST_TEMPLATE.md \
   docs/migration/base-X_to_base-Y/RELEASE_CHECKLIST.md
# fill RELEASE_CHECKLIST + GUIDE.md + lessons-learned.md
# update docs/migration/README.md index
# update this playbook §2 card + §4 jump table
# update COMPAT.md + RELEASE_NOTES.md
# scaffold: python3 scripts/new_base.py --from v2/base/base-X --base Y
```

Hop `GUIDE.md` should cover:

- [ ] Filename / lineage changes  
- [ ] Terminate / Layer A wire deltas  
- [ ] Client-breaking parse changes  
- [ ] Zeus-breaking schema / Detective changes  
- [ ] Hash / stamp impact  
- [ ] Pin readiness criteria  

Full ship bar: hop **`RELEASE_CHECKLIST.md`** (not GUIDE alone).

---

## 10. SoT map (do not duplicate)

| Topic | Canonical |
| --- | --- |
| Ownership set/unset/change | [BIBLE.md](BIBLE.md) §2 |
| Wire order / budget | [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) |
| Settings / policy table | [PROMPT_SETTINGS.md](PROMPT_SETTINGS.md) |
| Rules object / output_request | [RULES_OBJECT_AND_OUTPUT_REQUEST.md](RULES_OBJECT_AND_OUTPUT_REQUEST.md) |
| Jailbreak | [JAILBREAK_POLICY.md](JAILBREAK_POLICY.md) |
| Multi-round | [MULTI_ROUND_CLIENT.md](MULTI_ROUND_CLIENT.md) |
| Future BASE themes | [ROADMAP.md](ROADMAP.md) |
| Versions | [COMPAT.md](../COMPAT.md) |
| Pack scaffold | [CREATE_BASE.md](CREATE_BASE.md) |
