# Pack: base-6.1

Thin index for the **base-6.1** snapshot (additive Client-loop train on base-6).

| | |
| --- | --- |
| **Theme** | `user` emit enum + `ip_address` (IPv4/IPv6) + `ai_process_result` (default false) |
| **Parent** | base-6 |
| **Wire** | base-5 (no break) |
| **OVERVIEW** | [OVERVIEW.md](OVERVIEW.md) |
| **ROADMAP** | [docs/ROADMAP.md § base-6.1](../../../docs/ROADMAP.md) |
| **Migration hop** | [docs/migration/base-6_to_base-6.1/](../../../docs/migration/base-6_to_base-6.1/) |
| **Client backlog** | [ZC-WISH-035](../../../docs/ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) · [ZC-WISH-044](../../../docs/ZEUS_CLIENT_WISHLIST_FOR_CHAT_REQUEST.md) |
| **Helios** | [HEL-WISH-022](../../../docs/HELIOS_WISHLIST_FOR_CHAT_REQUEST.md) |

```text
v2/base/base-6.1/
  min/chat_request_<mode>_base-6.1.json
  text/…
  response_output_schema.json      # Layer A (model) — unchanged wire
  response_output_example.json
  report_sink_schema.json          # Client sink stamps (user, ip_address)
  report_sink_example.json
  settings_ai_process_result.example.json
  MANIFEST.json
```

| Concern | Schema | Example |
| --- | --- | --- |
| Model terminate (Layer A) | [`response_output_schema.json`](response_output_schema.json) | [`response_output_example.json`](response_output_example.json) |
| Analytics/report sink root | [`report_sink_schema.json`](report_sink_schema.json) | [`report_sink_example.json`](report_sink_example.json) |
| Client settings loop flag | — | [`settings_ai_process_result.example.json`](settings_ai_process_result.example.json) |

**Pin:** do not flip `CURRENT.json` until Client + stamp + Detective green.
