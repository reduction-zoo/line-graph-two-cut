---
status: ready-for-attempt
openness: supported-within-search-coverage
difficulty: moderate
importance: high
tags: [graph-cuts, line-graphs, NP-hardness]
last-literature-check: 2026-09-15
---

# Matching Cut to line-graph 2-Cut

[Board](../../research/open-problems/README.md) · [Karp contract](../../research/open-problems/README.md#shared-karp-contract)

**Reduction target:** Degree-four Matching Cut → line-graph 2-Cut

| Assessment | Evidence |
|---|---|
| Difficulty | Moderate, provisional: rigid variable available; clause and composition missing |
| Importance | High within this class: complete the remaining d-Cut case on line graphs |
| Proof readiness | Provisionally ready for a bounded attempt; first priority; no blocking gate |

**Exact endpoints.** A consists of connected simple graphs of maximum degree
four having a nontrivial cut with at most one opposite neighbor per vertex.
B is encoded by a connected simple root H with at least two edges. Its line
graph L(H) has one vertex per edge of H, with adjacency when two edges share
an endpoint. L(H) must
have a nontrivial cut with at most two opposite neighbors per vertex. Giving H
is polynomially equivalent to recognizing and reconstructing a simple line graph.

**Gap and value.** R1 explicitly retains d=2 after known tractability at d=1
and hardness at d≥3. General claw-free hardness does not supply a simple root.

**Route and actual evidence.** In an edge coloring of H, the opposite-color
degree of a red edge uv in L(H) is b(u)+b(v), where b(z) counts the blue
edges incident to root vertex z. The recorded checks verified
the identity on 3,246 small-root colorings and found a rigid nine-vertex line
graph from K4 with three pendant root edges. The earlier claw-free clause has
no simple root.

The rigid example attaches pendant edges at three distinct K4 vertices and
allows only the two constant legal colorings of its line graph. The root counting
identity also implies that a root vertex incident with both colors has degree
at most four. A mixed degree-four root vertex must split 2+2 and forces every
neighboring root vertex to be monochromatic. These constraints are useful when
screening candidate clause interfaces.

**Next exercise.** Realize the relation forbidding x_u=x_w≠x_v with a simple
root, where x_z is the binary color assigned to source vertex z and u,w are
distinct neighbors of v. Check attachment budgets, then prove nontriviality
and both directions.
The missing composition proof is why moderate difficulty remains provisional.

## Primary sources

- **R1:** [Finding d-Cuts in Graphs of Bounded Diameter, Graphs of Bounded Radius and H-Free Graphs](https://eprints.cs.univie.ac.at/8514/1/Finding_d_cuts_in_Graphs_ALGORITMICA.pdf), Algorithmica 88:7 (2026), Theorems 5 and 13, Section 5, PDF page 25.

## Research history

- [Recorded probe](../../research/evidence/graph-structure-probes.py): finite evidence only, not an independent proof review.

- 2026-09-14: Web and arXiv update queries: `"2-Cut" "line graphs" 2026`; `"2-cut" "line graphs" 2026`; `"perfect matching cut" "radius" 2026`; `"Perfect Matching Cut" "radius 3"`.
  No exact resolution was located within this search; unpublished, unindexed,
  and overlooked results remain outside the supported openness claim.

- 2026-09-15: Selected for an initial three-round campaign. Queries: `"2-cut" "line graphs" complexity 2026`, `"2-cut" "line graphs" solved`. Read [arXiv HTML](https://arxiv.org/html/2404.11389), Theorem 4.1 and Section 5: the proof assumes d >= 3 and the conclusion explicitly retains d = 2. Published-paper search text agrees. No later resolution was located; unindexed and unexamined results remain outside coverage.

## Acceptance

Construct a deterministic polynomial-time Karp reduction for these exact endpoints, with polynomial output bit length and recovery of a source witness from every valid target witness. Give a general proof, passing independent checks, novelty coverage and independent review.
