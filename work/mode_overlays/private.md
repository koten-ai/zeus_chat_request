## Mode: private

**Mission:** Personal / single-user knowledge base — **scope of one**. Backlinks and personal graph matter more than corpus-wide statistics.

**Entities:** Whatever MINI-SCHEMA shows for this personal graph (notes, people, docs, tags). Prefer user-local types.

**Join / noise posture:**
- Statistical / corpus-selectivity signals are **weak or meaningless** on a single-user corpus.
- Prefer structural + semantic links the user actually created.
- Boundary is **user** — never assume multi-tenant walls or shared global indices.

**Edges / relations:** Backlinks first-class when present. Prefer explicit links the user authored.

**Traversal:** Local neighborhood + backlinks; avoid “popularity” or global ranking language.

**Terminate flavor:** Personal context; honest when the KB is sparse; no fake global stats.

**Don't:**
- Cite “corpus averages” or super-node market stats.
- Assume other users’ data exists.
- Over-trust weak co-occurrence as identity.

**Example:** search → traverse backlinks → project titles.
