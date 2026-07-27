# Lessons: base-5.2 → base-5.3

**Audience:** catalog authors; Zeus/Client pin agents  
**Captured:** 2026-07-26 (pack content train)  
**Related:** [README.md](README.md) · [ROADMAP § Verb catalog clarity](../../ROADMAP.md) · Zeus `docs/API/V2/transforms.md`

## 1. Order API: `asc` not `direction`

base-5.2 CORE and analytics example taught:

```text
order … by: "<field>", direction: "desc"
```

Zeus v2 `order` accepts:

```text
by: "id" | "created_at" | "field:<name>"
asc: true|false   # default true
```

`direction` is ignored / wrong. base-5.3 fixes CORE + analytics pipeline example.  
**Check:** grepping packs for `direction": "desc"` on order steps should be empty.

## 2. Contract enforcement: do not strip tools[] mid-session

Even if MINI-SCHEMA is present, **do not** remove `describe` (or any verb) from the stamped tools list under enforcement — hash mismatch fails the chat. Diet membership only via a **new stamp** / A/B pack after Hot Path empirics (ROADMAP § Getting skinny).

## 3. Verb descriptions beat long essays alone

Models weight tool schemas. Cost-tags only (`[cheap] describe`) under-taught V2 “LLM gets wrong” facts. Prefer WHEN / WHEN NOT / KEY on each verb; keep full API pages in Zeus docs.

## 4. Assemble order of operations

`assemble_mode_prompts.py` **replaces** system message from CORE + overlay. Dual-gap notes must live in CORE (or overlays), not only in a prior min JSON tail — or they disappear on assemble.

## 5. search schema must match examples

If examples include `timeout_ms` / `where` / `seed_node_id`, put them in `properties`. Otherwise the model invents or omits knobs inconsistently.
