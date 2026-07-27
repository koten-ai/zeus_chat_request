# base-5.3 overview

**Parent:** `base-5.2` · **Wire:** base-5 (objects / required four / `app_output`) — **content train only**  
**Theme:** Skinny habits + world-model language + verb catalog clarity  
**ROADMAP:** docs/ROADMAP.md § base-5.3 · § Getting skinny · § World model language · § Verb catalog clarity (CR-26)

## What changed vs base-5.2

1. **CORE system blurb** — AI-Ready overlay · MINI-SCHEMA as shape · access path → verb · evidence-only Layer A  
2. **Verb clarity** — all 13 tools teach WHEN / WHEN NOT / KEY; params aligned to Zeus `docs/API/V2`  
3. **P0 order fix** — system + analytics example use `by: "field:<name>"` + `asc: false` (not `direction`)  
4. **search** schema adds `timeout_ms`, `where`, `seed_node_id`  
5. **describe** `include` + not-a-replacement-for-inject guidance  
6. Dual gaps (`wish_i_knew` + `data_gaps`) retained from base-5.2  

## Non-goals

- Layer A required-field rename/remove  
- Runtime strip of tools under contract enforcement  
- Pin promote (`CURRENT.json` stays base-1 until separate gate)  
- Hot Path product / Client allowlist implement  

## Verify

```bash
python3 scripts/verify_base_pack.py --base 5.3
```
