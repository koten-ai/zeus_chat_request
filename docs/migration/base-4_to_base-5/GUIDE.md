# Guide: base-4 → base-5

**Purpose:** What stayed, moved, and broke between candidate **base-4** and candidate **base-5**.  
**Kind:** **BREAKING** — last wire/control-plane freeze on this line ([ROADMAP](../../ROADMAP.md)).  
**Pack:** [`v2/base/base-5/`](../../../v2/base/base-5/)  
**Pin:** still **base-1** until explicit promote.

| | Path |
| --- | --- |
| From | `v2/base/base-4/` |
| To | `v2/base/base-5/` |
| Checklist | [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) |
| Lessons | [lessons-learned.md](lessons-learned.md) |

---

## 1. Stayed the same

| Item | Notes |
| --- | --- |
| Required four | `summary`, `query_decomposition`, `decomposition`, `confidence` |
| 13 verb names | describe…return |
| Envelope | `_format: "zeus.chat_request.v2"` |
| G1/G2/G3 audiences | User / admin / client |
| Filename pattern | `chat_request_<mode>_base-N.json` |
| Flat Layer A on `return` | Still flat tool args |

---

## 2. Breaking wire (base-4 → base-5)

| base-4 | base-5 |
| --- | --- |
| `business_rules_triggers: boolean[]` (index-aligned) | **`{ rule_id: boolean }` object**, sparse |
| inject design: `rules[]` | inject design: **`rules { id → text }`** |
| no first-class app bag | optional **`app_output`** |
| type-only structured maps | **`type` + `description`** per field (Client validates type) |
| informal Client control plane | settings bag + policy table + merge/freeze (Client contract) |

**Dual-read:** Client may accept arrays for **≤1 release** while migrating; base-5 catalogs/schema are **object-only**. Prefer zero dual-read if no external consumers.

---

## 3. Added (documented for inject / Client)

| Piece | Where |
| --- | --- |
| `company_context` | Client inject (not BASE essay) |
| Jailbreak default named rules | Client / Workbench pack |
| `message_*` + soft-require `policy_action` | Client mapping |
| `output_request` → prompt “Output request” block | Client render descriptions |
| `app_output` on terminate | Layer A optional |
| Session / multi-turn flags semantics | PROMPT_SETTINGS |

---

## 4. Explicitly not in this hop

| Item | Where instead |
| --- | --- |
| Soft hints / A/B paste | base-6+ additive |
| Helios Pri-1 as required AI fields | Zeus/Client report emits |
| CURRENT pin flip | Later gate |
| Workbench full editor | base-7 product |

---

## 5. File map

| Artifact | base-5 |
| --- | --- |
| Catalogs | `v2/base/base-5/min/*_base-5.json` |
| Text | `v2/base/base-5/text/*_base-5.txt` |
| Schema | `v2/base/base-5/response_output_schema.json` |
| Example | `v2/base/base-5/response_output_example.json` |

---

## 6. Upgrade steps (short)

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and [BASE_AGENT_PLAYBOOK.md](../../BASE_AGENT_PLAYBOOK.md) §3–4.2.

```bash
python3 scripts/new_base.py --from v2/base/base-4 --base 5
# diet already applied in release/base-5 branch for first pack
python3 scripts/scan_catalogs.py
```

**Zeus / zeus_client:** implement object triggers + optional `app_output` + inject contracts; do not invent hashes; pin only after stamp + green spikes.
