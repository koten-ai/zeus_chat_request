# Work plan — recreate mode intent in chat_request prompts

> **Status:** plan only (not started) · **Created:** 2026-07-26  
> **Roadmap train:** **base-5.1** (content on base-5 wire — not a wire break) · [ROADMAP.md § base-5.1](../docs/ROADMAP.md)  
> **Jira:** [CR-23](https://kotenai.atlassian.net/browse/CR-23) · parent epic [CR-3](https://kotenai.atlassian.net/browse/CR-3)  
> **SoT for mode meaning:** [../docs/MODE.md](../docs/MODE.md)  
> **Engine design:** [zeus_design_docs DESIGN.md §14](https://github.com/fujio-turner/zeus_design_docs/blob/main/DESIGN.md)  
> **Packs:** `v2/base/base-5/min/chat_request_<mode>_base-5.json` (candidate; pin still base-1)

## Goal

Restore **mode-specific behavior in the LLM-facing prompt** so `fraud`, `research`, `code`, `regulated`, etc. are not “analytics with a different mode string.”

**Primary edit surface:** the **system prompt string** that participates in the stamped contract:

```text
messages[0].content   # role=system
```

This is included via `_hash_policy.pointers` → `/messages/*/content`.

**Not the primary surface:** top-level `contract{}` metadata (`id`, `hash`, `builder`, `name`). That object is hash-excluded packaging metadata. Updating only `contract.name` does **not** restore mode behavior.

```text
RESTORE = core discipline (shared) + MODE_OVERLAY (per mode) inside messages[].content
        (+ optional verb blurb cleanup; optional guidance for soft tips)
```

---

## Why this plan (vs alternatives)

| Approach | Verdict |
| --- | --- |
| **A. Core + thin mode overlay in system prompt** | **Chosen** — matches DESIGN, maintainable, aligns with Zeus `modes/<mode>.md` hook |
| B. Fully fork 10 independent 6k essays | Reject — will re-drift within one BASE |
| C. Engine-only (no catalog change) | Insufficient — LLM never sees fraud/research persona |
| D. Verb list only (no prose) | Insufficient — same verbs, wrong planning language |
| E. Soft `guidance` only (hash-excluded) | Optional **addon**; hard posture should stay in hashed system text |

---

## Non-goals

- Flip `CURRENT.json` / invent production `contract_hash`
- Break base-5 Layer A wire (objects, `app_output`, required four stay)
- Rewrite all of Zeus ingest in this ticket
- Make every tool mode-gated on day one (optional later)
- Dual-read array triggers work

---

## Open decisions (resolve in Phase 0)

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | Ship train / folder | Keep diet in `v2/base/base-5/` labeled **base-5.1** vs new folder `base-5.1` | **Keep base-5 folder**; train id **base-5.1** in ROADMAP/RELEASE_NOTES (content patch) |
| D2 | Author SoT for overlays | This repo only vs Zeus `ai/V2/prompt/core/modes/` first | **Author in this repo** under `work/mode_overlays/` then port to Zeus generator |
| D3 | Overlay length | Short (≤800 words) vs long | **Short**; link DESIGN for depth |
| D4 | Soft tips | All in system vs split to hash-excluded `guidance` | **Hard posture in system**; demos/tips may use `guidance` later |
| D5 | auto | Keep min pipeline essay vs full discovery persona | **Rewrite auto** as discovery/handoff (not second analytics min) |
| D6 | Jira | New CR story vs attach CR-1 | **CR-23** under **CR-3** — “[base-5.1] Restore mode overlays in system prompt” |

---

## Success criteria

1. For each mode M ≠ analytics: after neutralizing mode token M, **diff vs analytics** shows a dedicated **MODE_OVERLAY** (or equivalent section headers), not only hash/`analytics job` leftovers.  
2. Keyword/entity smoke passes for fraud, research, code, regulated, tenant, private, open, auto, custom (checklist in [docs/MODE.md](../docs/MODE.md) §6.1).  
3. `python3 scripts/verify_base_pack.py --base 5` remains **OK**.  
4. Inspector Diff analytics ↔ fraud (and research, code) is human-meaningful.  
5. No invented production stamps.  
6. Zeus generator can load the same overlays (or documented dual-home until ported).  
7. [docs/MODE.md](../docs/MODE.md) remains accurate; this file marked **done** when PR merges.

---

## Architecture to implement

```text
                    ┌─────────────────────────┐
                    │  CORE (shared fragment) │
                    │  efficiency, pipeline,  │
                    │  return / base-5 Layer A│
                    └───────────┬─────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
   modes/analytics.md    modes/fraud.md         modes/research.md
   (default persona)     (weak signal …)        (citations …)
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
              assemble → messages[0].content
                                ▼
              verbs[] (shared + optional blurb fix)
                                ▼
              export_base_text + verify_base_pack + Diff
```

### Suggested on-disk authoring layout (this repo)

```text
work/mode_overlays/
  README.md                 # how to assemble
  CORE.md                   # shared (extracted from analytics)
  analytics.md
  open.md
  tenant.md
  regulated.md
  private.md
  fraud.md
  research.md
  code.md
  auto.md
  custom.md
  examples/                 # optional sample pipelines per mode
```

Assembly (future script or manual first):

```text
content = CORE.md + "\n\n## Mode: {mode}\n\n" + overlays/{mode}.md
→ write into min JSON messages[0].content
→ export_base_text.py
→ refresh MANIFEST / verify
```

### Zeus port (later phase)

```text
ai/V2/prompt/core/*.md          # already exists
ai/V2/prompt/core/modes/*.md    # CREATE — systemPromptV2 already loads them
```

---

## Phases

### Phase 0 — Align (no pack edit)

**Owner:** product + catalog  
**Exit:** D1–D6 decided; CR ticket open

- [ ] Read [docs/MODE.md](../docs/MODE.md) + DESIGN §14  
- [ ] Confirm restore target = `messages[].content` (not only `contract{}`)  
- [ ] Record D1–D6 answers at top of this file  
- [ ] Create/update Jira story; link CR board  
- [ ] Branch off agreed base (e.g. `main` after process PR or ticket branch)

### Phase 1 — Inventory automation

**Exit:** baseline similarity report checked in or attached

- [ ] Add `scripts/diff_modes.py` (or one-shot under `work/`):  
  - pairwise neutralize mode token  
  - flag leftover `analytics` strings  
  - list verb name equality  
  - score “clone risk”  
- [ ] Run on base-5 and base-1; save report under `work/mode_overlays/BASELINE_REPORT.md`  
- [ ] Fix or ticket any **wrong** leftover strings as first cleanup P0 (`[exp] analytics job`)

### Phase 2 — Extract CORE

**Exit:** CORE.md is the shared discipline; analytics pack can be rebuilt from CORE + analytics overlay

- [ ] Split current analytics `messages[0].content` into:  
  - **CORE** — execution style, efficiency, pipeline rules, terminate / Layer A (base-5 objects)  
  - **analytics overlay** — “real links not noise”, degree caution, default BI posture  
- [ ] Ensure CORE does **not** hard-code `analytics` (use `{{mode}}` or neutral wording)  
- [ ] Dry-run assemble analytics; Diff vs current analytics ≈ empty of intentional persona loss

### Phase 3 — Write overlays (priority order)

Write one overlay at a time; re-assemble one pack; Diff; then next.

| Order | Mode | Overlay must include (from MODE.md §6) |
| --- | --- | --- |
| 1 | analytics | Reference default |
| 2 | fraud | Weak signal; Device/Phone/Address/IBAN; shares_*; analyst review |
| 3 | research | DOI/Paper/Author; cites/cited_by; semantic bias |
| 4 | code | Function/Class/Module/Package; calls/imports; structural first; hop posture |
| 5 | regulated | Floor/high bar language; redact; no casual full content; audit posture |
| 6 | tenant | Hard wall; no cross-tenant |
| 7 | private | User boundary; no corpus-stat crutches; backlinks |
| 8 | open | Noise OK; super-node warning |
| 9 | auto | Discovery + propose + handoff; high caution; not permanent policy |
| 10 | custom | Conservative; operator hooks; don’t invent personality |

Per mode checklist:

- [ ] Mission paragraph  
- [ ] Entities  
- [ ] Noise/join posture  
- [ ] Edges vocabulary  
- [ ] Don’ts  
- [ ] One example pipeline (optional file under `examples/`)  
- [ ] Assembled into `min/chat_request_<mode>_base-5.json`  
- [ ] `export_base_text` for that mode  
- [ ] Diff vs analytics shows overlay  

### Phase 4 — Verb / schema hygiene

- [ ] Remove or mode-fix residual **`[exp] analytics job`** (and similar) across all packs  
- [ ] Confirm verb **names** still match engine registry for trial  
- [ ] Optional later: mode-specific verb **description** lines (not full schema fork)  
- [ ] Optional later: tighten Zeus `AppliesTo` only where DESIGN requires (separate Zeus PR)

### Phase 5 — Tooling & gates

- [ ] Document assemble command in `work/mode_overlays/README.md`  
- [ ] Extend `verify_base_pack.py` **or** add `diff_modes.py --fail-if-clone` for CI/local  
- [ ] Wire note into [docs/CREATE_BASE.md](../docs/CREATE_BASE.md): scaffold copies parent; **re-apply overlays** after `new_base`  
- [ ] Update [docs/MODE.md](../docs/MODE.md) “current state” when green  

### Phase 6 — Zeus generator parity

- [ ] Port overlays to `Zeus/ai/V2/prompt/core/modes/<mode>.md`  
- [ ] Confirm `systemPromptV2` includes them  
- [ ] Snapshot path does not overwrite zeus_chat_request overlays blindly  
- [ ] Keep COMPAT note if generator version matters  

### Phase 7 — Docs, COMPAT, ship

- [ ] RELEASE_NOTES: “mode overlays restored in catalogs (content; not wire break)”  
- [ ] ROADMAP / MODE.md status  
- [ ] COMPAT: optional note “base-5+ packs include mode overlays”  
- [ ] PR → main (zeus_chat_request); optional Zeus PR  
- [ ] CR board §9 hygiene  
- [ ] Mark this work plan **Done** with date + PR links  

---

## Suggested PR slicing

| PR | Contents |
| --- | --- |
| **PR-A** | `docs/MODE.md` + this plan + `diff_modes` baseline (docs only) — *this change set can stop here* |
| **PR-B** | CORE extract + analytics rebuild + leftover string cleanup |
| **PR-C** | fraud + research + code overlays |
| **PR-D** | regulated + tenant + private + open |
| **PR-E** | auto + custom + verify gate |
| **PR-F** | Zeus generator port |

Do not mix mode diet with unrelated base-6 soft hints unless intentional.

---

## File touch map (expected)

| Path | Action |
| --- | --- |
| `docs/MODE.md` | Living SoT (modes) |
| `work/RECREATE_MODE.md` | This plan |
| `work/mode_overlays/*` | Authoring fragments |
| `v2/base/base-5/min/chat_request_*_base-5.json` | `messages[0].content` diet |
| `v2/base/base-5/text/*` | Re-export |
| `scripts/diff_modes.py` | New (recommended) |
| `scripts/verify_base_pack.py` | Optional clone check |
| `docs/CREATE_BASE.md` / playbook | Wire “re-apply overlays” |
| Zeus `ai/V2/prompt/core/modes/*.md` | Port (PR-F) |

---

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Overlay contradicts engine | Cross-check `internal/modes` Extract/Join/Floor; engine enforces security |
| Prompt bloat | Hard cap overlay size; keep CORE once |
| Drift after `new_base` | CREATE_BASE + verify clone gate |
| Tool names not registered | Existing Zeus prompt drift tests |
| Reviewers can’t see delta | Require Diff screenshots / unified diff of overlays in PR |

---

## Execution order (short)

```text
0. Decide D1–D6 + Jira
1. Baseline diff_modes report
2. Extract CORE + analytics overlay
3. Write fraud → research → code → regulated → … overlays
4. Clean analytics leftovers in verbs
5. Gate + docs
6. Port to Zeus generator
7. Ship PRs; update board
```

---

## Sign-off

| Role | Name | Date | Notes |
| --- | --- | --- | --- |
| Catalog / docs | | | |
| Zeus | | | generator port |
| zeus_client | | | load mode packs only (no API break expected) |
| Product | | | D1 ship train |

---

## Appendix — current clone evidence (2026-07-26)

- All 10 base-5 modes share the **same 13 verb names**.  
- Neutralized pairwise diffs vs analytics ≈ **hash + leftover “analytics job” string** for non-auto modes.  
- **auto** is the only structural prompt outlier (shorter min pipeline essay) — still not a full discovery persona.  
- Zeus `systemPromptV2` supports `modes/<mode>.md` but **directory not populated**.

See [docs/MODE.md](../docs/MODE.md) §3 for full diagnosis.
