# Lessons: base-6 → base-6.1

**Audience:** catalog authors; Client / Helios implementers  
**Captured:** 2026-07-27  
**Related:** [README.md](README.md) · [ROADMAP § base-6.1](../../ROADMAP.md)

## 1. Readable enums beat short codes

Root field is **`user`**, not `usr`. Values are full names (`zeus_client`, `zeus`, `helios`, `admin`) — not `zc|z|h|a`. Companion **`ip_address`** is a single string (IPv4 or IPv6 textual form), not separate `ipv4`/`ipv6` fields. Analytics filters and dashboards stay human-readable; document size is not the constraint.

## 2. Cheap default wins

**`ai_process_result: false`** is the product default. Lab pattern (one AI plan → one Zeus pipeline → UI tables) must not force a second billable AI essay. Opt-in only when the product wants insight.

## 3. Client stamps; model never invents

`user` and optional `ip_address` are set by the **sink writer** (Client / Hub / engine). Never Layer A. Never model free text. Helios product purity = `user = "zeus_client"` **and** scope present. Missing `ip_address` is fine; inventing one is not.

Machine SoT for the sink (not Layer A): pack `report_sink_schema.json` + `report_sink_example.json`. Layer A remains `response_output_*.json` only.

## 4. Helios backlog stays in HELIOS_WISHLIST

Locale/channel/market/deployment Helios Pri-1 bulk is **not** the Client wishlist. Client file owns Client floor + base-6.1 emit/loop flags; Helios owns Motions field catalogue.

## 5. Pack can ship before Client implements

Candidate pack + CORE note document the contract. Runtime stamp and insight loop are Client residual. Do not block the pack on full product implementation; do not claim production soft-insight is live until Client lands.

## 6. Snapshot folders

Train id = pack folder = `_lineage.base_id`. Never apply base-6.1 only via `content_train` on base-6.
