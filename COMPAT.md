# Compatibility matrix — Zeus engine ↔ chat_request BASE

**Draft (CR-1).** Enforced as warnings first; hard gates later (ZE-222 / ZE-223).

| Zeus engine (semver) | Allowed BASE range | Notes |
| --- | --- | --- |
| `0.5.0` – `0.5.x` | `base-1` | Initial BASE: v2 min catalogs + `_lineage.base_id` |
| *future* | `base-2`+ | Bump when material catalog/generator changes |

## Rules

1. **BASE** identity is `base-N` (monotonic integer suffix). Not Zeus version.
2. **Customs** (`custom:<slug>-k`) always record `parent_base_id` = some `base-N`.
3. A client or Workbench stamp should refuse / warn when:
   - `base_id` is missing, or
   - `base_id` is outside the row for the running Zeus version.
4. Runtime injects (SCOPE BRIEF / MINI-SCHEMA) are **not** part of BASE identity.

## How to bump BASE

1. Change generator / fragments in Zeus.
2. `make ai-snapshot-min`
3. Bump `base_id` in Zeus `ai/chat_request/PIN.json`
4. `make chat-request-publish ZEUS_CHAT_REQUEST_ROOT=…`
5. Commit both repos; add a row here if compat range changes.

## Related authoring docs

- [PROMPT_ASSEMBLY.md](PROMPT_ASSEMBLY.md) — assembled prompt shape; BASE body stays hashed, Client inject does not  
- [simple_layout.txt](simple_layout.txt) — `base_id` / `custom_id` in the layout map

## Prototypes (not in compat matrix)

| Id | Notes |
| --- | --- |
| `base-2-prototype` | Authoring fork for Layer A terminate + Client triggers. Files: `chat_request_<mode>_base-2-prototype.json`. **Not** production BASE until promoted. Opt-in only. |

## File naming (BASE vs custom)

| Kind | Pattern |
| --- | --- |
| BASE | `chat_request_<mode>_base-<N>.json` |
| Custom (Workbench) | `chat_request_<mode>_base-<N>_cus_<bucket>_<scope>-<rev>.json` |

Customs always record `parent_base_id = base-N`. Compat rows above apply to the **parent BASE**, not each custom rev. Bumping custom `-1` → `-2` does not create a new BASE.

See [v2/base/base-2-prototype/PROTOTYPE.md](v2/base/base-2-prototype/PROTOTYPE.md#file-naming-base-vs-workbench-customs).
