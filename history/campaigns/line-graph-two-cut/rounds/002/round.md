# Round 002 — Connected cores with three reservoir terminals

## Plan

Reconsider the single-junction restriction using the star limitation from
[experience](../../../../research/experience/line-graph-star-junction-relations.md).
Its zero external-cost premise also holds here, but separate junctions can
interact through core edges. Enumerate every connected graph-atlas core on 1–5
vertices, with at most seven core edges, and every multiset of three attachment
vertices. Add three distinct terminal leaves. Enumerate all edge colorings with
at most two opposite adjacent edges, allowing constants for local interfaces.

First check: does projection onto terminals exclude exactly one complementary
nonconstant pair (the desired relation after terminal relabeling)? For each hit,
also check whether constant terminals force constant internal edges. A K6 variable
reservoir can replace each leaf endpoint and forces that terminal's color while
adding zero opposite cost. Decoding would read reservoir colors. Spurious
nontriviality and combining repeated occurrences remain full-rule obligations.
Finish this finite family, preserving the first matching root if any.

## Evidence and diagnosis

The [probe](probe.py) evaluated 27 connected cores, 740 attachment templates and 315,272 complete edge assignments. [Raw output](results.json) records six hits; the first has eight root vertices and nine edges, realizes exactly R(a,b,c), and constant terminals force every core edge constant. Reproduce from repository root: `python3 campaigns/line-graph-two-cut/rounds/002/probe.py`. No repairs or reruns.

The useful mechanism is a diamond core with a subdivided terminal attachment. Unlike a single junction, its internal edge couples opposite-color budgets across two endpoints. Finite exhaustive evidence establishes this particular interface table; there is no general reduction proof yet. Other hits were counted, not retained as separate discoveries.

**Experience extraction:** created [diamond interface](../../../../research/experience/line-graph-diamond-matching-cut-interface.md); updated the consuming history of [star limitation](../../../../research/experience/line-graph-star-junction-relations.md). No pending extraction. Time/token usage unavailable.

## Next action

Continue with the first interface, without increasing the local search. Attach each terminal to a K6 variable reservoir and test source equivalence plus universal recovery premises. The first discriminating observation is whether a constant global assignment can leave a nonconstant auxiliary coloring after composition.
