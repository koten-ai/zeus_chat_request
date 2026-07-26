# Catalog inspector (`index.html`) — multi-BASE

> **Doc status** · last reviewed **2026-07-26** · production pin **base-1** · design line **base-4** (base-5 = design only) · version matrix: [COMPAT.md](../COMPAT.md)


**Decision:** one `index.html` for all BASE lines (not a separate `index-base-4.html`).

## Why

- First migration test is **compare** base-1 vs base-4 → use **Diff** / **Matrix**
- Dropdown already lists every `v2/**/chat_request*.json` via `catalog-index.json`
- Badge shows `_lineage.base_id`

## How to run

```bash
python3 scripts/scan_catalogs.py
python3 -m http.server 8766 --bind 127.0.0.1
# open http://127.0.0.1:8766/index.html
# or: docker compose up → :3333
```

## Tips

1. Mode dropdown labels: `folder · mode · base_id · proto?`
2. Diff: pick same mode from `v2/min` (base-1) and `base/base-4/min` (base-4)
3. Full requirements: [BIBLE.md](BIBLE.md) · mapping: [base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md](base-1_to_base-4/BASE_1_TO_BASE_4_GUIDE.md)
4. New pack scaffold: [CREATE_BASE.md](CREATE_BASE.md)

## Optional later

A thin multi-round Client lab page — only if you need UX beyond catalog structure (not a fork of this inspector).
