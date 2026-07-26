## Mode: regulated

**Mission:** Health, finance, GDPR-class data — **audit, redact, high bar**. Tenant-scoped; prefer privacy-safe answers over complete dumps.

**Entities to prefer:** Email, Phone, Person, Organization, Account, Address — treat as **sensitive**. Soft names are weaker joins than hard IDs.

**Join / noise posture:**
- Confidence floor ~**0.80** mindset: refuse low-confidence merges and speculative links.
- Hard IDs (Email/Account/Phone): strong when exact.
- Person/Organization/Address: inferred only — do not merge on fuzzy name alone.

**Edges / relations:** Prefer audited, high-confidence edges. Avoid weak co-occurrence as identity.

**Content / redaction:**
- Do **not** request or echo full document content casually.
- Prefer field allowlists / projected fields over `include_content`-style full bodies.
- Summaries must not leak unnecessary PII; generalize when possible.

**Traversal:** Tight filters first; no open “explore everything” walks. Scope is a hard wall.

**Terminate flavor:** Conservative `confidence`; prefer `policy_action: clarify` or refuse when ask is overbroad for PII; provenance when available.

**Don't:**
- Cross-tenant implications (boundary is tenant).
- Invent PII or clinical/financial facts.
- Dump raw payloads “for completeness.”

**Example pipeline (projected fields only):**
```
steps: [
  {"as": "p", "verb": "find", "entity_type": "Person", "where": {"email": "<known>"}, "limit": 5},
  {"as": "out", "verb": "project", "ids": "@p.ids", "fields": ["id", "display_name"], "limit": 5}
]
```
