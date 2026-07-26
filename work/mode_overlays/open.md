## Mode: open

**Mission:** Public-data / link maps / crawls — **every possible edge is interesting**. Serendipity over precision; explicitly **not** the safe default.

**Entities:** Broad registered types; join liberally when MINI-SCHEMA allows.

**Join / noise posture:**
- Low confidence floor (~**0.20**) mindset: prefer noise over miss.
- Strong-join bias: many entity types are traversable.
- Expect super-nodes; still warn and limit fan-out in practice to avoid blow-ups.

**Edges / relations:** Explore available edge types; map-making OK. Label weak vs strong in summary when possible.

**Traversal:** Wider than analytics, but still hard-cap steps. Prefer “sample then expand” over unbounded crawl in one pipeline.

**Terminate flavor:** Rich link maps; lower confidence OK; surface interesting candidates without claiming BI certainty.

**Don't:**
- Pretend analytics-grade precision.
- Unbounded fan-out that times out — sample first.
- Invent edges not returned by tools.

**Example:** find seed → traverse multiple edge types with limits → project sample.
