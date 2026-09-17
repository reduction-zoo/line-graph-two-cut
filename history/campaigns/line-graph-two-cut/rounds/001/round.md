# Round 001 — Repeated-color star junctions

## Plan

Test whether a single root junction with repeated variable-colored incident edges
can implement the source relation R(a,b,c): not(a=c!=b). Scope: positive
multiplicities of all three colors, total degree 3 through 6 (20 templates), all
eight assignments. External endpoints are monochromatic variable reservoirs,
so all opposite-edge cost is at the junction. A K6 reservoir has monochromatic
incident edges because degree at least five cannot mix colors under bound two;
separate attachment vertices keep the root simple. Variable copies can supply
unbounded occurrences. Constant assignments must force the whole target constant.

First check: exact equality of the junction relation with R. If equality fails,
inspect which patterns are lost; do not enlarge stars without a structural reason.
Experience retrieval: `rg -n -i 'line.graph|2.cut|junction' research/experience`
found no applicable lemma; previous perfect-matching budget lemmas require exact
one and do not apply. The published d >= 3 construction uses degree 2d+1 clause
junctions; d=2 would produce degree five and lose all mixed assignments.
Source: https://arxiv.org/html/2404.11389, Theorem 4.1 construction, read 2026-09-15.

## Evidence and diagnosis

The [probe](probe.py) checked 20 templates and 160 assignments; [raw results](results.json) contain zero matches. Reproduce from repository root: `python3 campaigns/line-graph-two-cut/rounds/001/probe.py`. No repairs or reruns. Stage reached: local relation, no candidate.

The cause is proved for this whole star family: degree three permits every assignment; degree four allows constants and exactly the balanced 2+2 split, producing four assignments when one of three colors is repeated; degree at least five permits only constants. Thus no positive multiplicities realize the six-pattern relation, at any size. This excludes a junction mechanism, not general root gadgets.

**Experience extraction:** created [star-junction limitation](../../../../research/experience/line-graph-star-junction-relations.md). This general local lemma is not independently reviewed. Time/token usage not measured.

## Next action

Reconsider the single-junction assumption. Enumerate connected small cores with three pendant terminals and retain interfaces implementing the exact relation. This permits opposite budgets to interact across internal edges; global composition remains to check.
