# Diamond interface for line-graph 2-Cut

Tags: line-graphs, 2-Cut, Matching Cut, diamond, terminal-relation

## Claim and applicability

Root core edges are 01,13,14,23,24,34. Three terminal edges are 05,16,37,
with colors a,b,c respectively. External endpoints 5,6,7 must contribute zero
opposite-edge cost. Under bound two, the allowed terminal assignments are exactly
not(a=c!=b). Constant terminals force every core edge constant. Terminal order matters.

## Evidence and status

Exhaustive nine-edge local check in [round 002](../../campaigns/line-graph-two-cut/rounds/002/round.md).
The raw record preserves the exact root and relation. An analytic proof and
full reservoir composition are in [the campaign proof](../../campaigns/line-graph-two-cut/work/proof.md).
[Independent review](../../campaigns/line-graph-two-cut/reviews/complete-rule/review.md)
returned advance, checking the local argument, zero-cost attachment premise and
universal recovery. Novelty remains supported only within the recorded literature
coverage; human expert assessment is outstanding.

## Consequence for search

Try K6 monochromatic variable reservoirs, identifying terminal leaves with
reservoir vertices. Check composition and nontriviality before expanding gadgets.
Do not use this relation when external endpoints spend opposite-edge budget.

## Use history

- [Round 003](../../campaigns/line-graph-two-cut/rounds/003/round.md): K6 reservoirs supplied the required zero external cost. The interface composed into a full rule; 8 prepared and 95 additional cases passed, followed by independent review. This use produced a valid candidate under agent review, not a measured comparison with another search policy.
