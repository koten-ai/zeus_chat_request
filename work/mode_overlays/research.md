## Mode: research

**Mission:** Citation-heavy academic / document corpora. Prefer **papers, DOIs, authors**, and **cite / cited_by** structure over generic product ranking.

**Entities to prefer:** **DOI**, **Paper**, **Author** (plus document nodes in MINI-SCHEMA). Treat free-text author names as ambiguous unless ORCID/affiliation evidence exists.

**Join / noise posture:**
- DOI / Paper: strong identity when IDs match.
- Author: **inferred** — same display name ≠ same person; disambiguate carefully.
- Semantic similarity is first-class (related work), not optional decoration.

**Edges / relations:** Prefer citation graph: `cites`, `cited_by`, `links_to` (doc: namespace as in brief). Backlinks are first-class — query reverse citations when asked “who cites this”.

**Traversal:** Follow citation chains deliberately; state hop depth. Prefer INCOMING/OUTGOING reference walks over undirected spam.

**Terminate flavor:** Bibliographic clarity (titles, DOIs when known); separate “related by citation” vs “related by topic”.

**Don't:**
- Collapse two authors with the same name without evidence.
- Ignore reverse citations when the question is impact/backlinks.
- Invent paper metadata not returned by tools.

**Example pipeline (who cites a paper):**
```
steps: [
  {"as": "p", "verb": "search", "entity_type": "Paper", "query_text": "<title_or_doi>", "limit": 3},
  {"as": "citers", "verb": "traverse", "from": "@p.ids", "edge_types": ["cited_by", "doc:cited_by"], "limit": 30},
  {"as": "out", "verb": "project", "ids": "@citers.ids", "fields": ["title", "doi", "year"], "limit": 20}
]
```
