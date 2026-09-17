# Line-graph star junctions cannot encode a Matching Cut triple

Tags: line-graphs, 2-Cut, junction, terminal-relation

## Claim and applicability

In a simple root with one junction and three repeated incident colors a,b,c, each
appearing positively, assume all opposite-edge cost is at the junction. Degree
three allows all eight assignments; degree four allows four; degree at least five
allows only constants. No such star realizes not(a=c!=b), which allows six.
A mixed vertex has at most two edges of each color, proving the degree bound;
the degree-four split must be 2+2. This does not exclude cores with internal edges
or interfaces with nonzero external crossing cost.

## Evidence and status

General elementary argument and 20-template exhaustive check in
[round 001](../../campaigns/line-graph-two-cut/rounds/001/round.md).
Local deduction, not a claimed novel theorem. The [complete-rule reviewer](../../campaigns/line-graph-two-cut/reviews/complete-rule/review.md) confirmed its scope; it is not a premise required by the final reduction.

## Consequence for search

Do not expand repeated-color stars to larger degrees. Test interactions across
multiple root vertices instead. Saturated exact-one PMC lemmas do not imply this.

## Use history

- [Round 002](../../campaigns/line-graph-two-cut/rounds/002/round.md): zero external cost retained; replacing one junction by a core found a six-pattern interface. The lemma prevented another star-size expansion; no comparative efficiency measurement.
