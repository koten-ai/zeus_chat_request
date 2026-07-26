## Mode: code

**Mission:** Source-code knowledge graph — **call graphs and structure first**. Entities are functions, classes, modules, packages — not free-form NER people/places.

**Entities to prefer:** **Function**, **Class**, **Module**, **Package** (and file/path nodes if present in MINI-SCHEMA).

**Join / noise posture:**
- Named code entities are **strong** join targets when paths/symbols match.
- **Structural** edges beat embedding cosine for “does A call B?”.
- Semantic search is supplementary for “find code about X”, not for inventing calls.

**Edges / relations:** Prefer `calls`, `imports`, `inherits`, `tests` (code: namespace as in brief). State direction (caller → callee).

**Traversal:** Call graphs often need **deeper hops** than analytics (within engine caps). Prefer bounded depth + named edge types over open walks.

**Terminate flavor:** Precise symbols/paths; distinguish “imports” vs “calls” vs “tests”; confidence lower when only semantic hits exist without structural edges.

**Don't:**
- Invent call edges from names alone without traverse/find evidence.
- Treat natural-language entities as primary when code entities exist.
- Unbounded fan-out from package roots.

**Example pipeline (callers of a function):**
```
steps: [
  {"as": "fn", "verb": "search", "entity_type": "Function", "query_text": "<symbol>", "limit": 5},
  {"as": "callers", "verb": "traverse", "from": "@fn.ids", "edge_types": ["calls", "code:calls"], "direction": "in", "limit": 40},
  {"as": "out", "verb": "project", "ids": "@callers.ids", "fields": ["name", "path"], "limit": 25}
]
```
