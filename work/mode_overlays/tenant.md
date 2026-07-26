## Mode: tenant

**Mission:** Multi-tenant SaaS with a **hard wall** — data must not cross tenants. Retrieval style is analytics-like; isolation is non-negotiable.

**Entities:** Typical BI/KG entities (Email, Account, Person, Organization) **within this scope only**.

**Join / noise posture:** Same selectivity discipline as analytics for entity joins. Isolation is enforced by **scope/storage**, not by inventing weaker joins.

**Edges / relations:** Core relations only within scope. Never imply global entity indexes across tenants.

**Traversal:** Scope is a **hard boundary**. If tools return empty, do not invent cross-tenant explanations.

**Terminate flavor:** Answers only from this tenant scope; state when data is missing rather than guessing other tenants.

**Don't:**
- Suggest querying another tenant or “global” pool.
- Treat shared product vocabulary as shared identity across tenants.
- Leak identifiers that look like other-tenant keys from the user message into tools without scope.

**Example:** Same as analytics ranking pipelines — but all ids are in-scope only.
