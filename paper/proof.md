# Matching Cut to line-graph 2-Cut

## Theorem and status

There is a deterministic polynomial-time Karp reduction from connected simple
Matching Cut of maximum degree four to 2-Cut on connected simple line graphs,
represented by their roots. Every valid target cut admits deterministic polynomial
source-witness recovery. The proof below applies to arbitrary input size; experimental
checks are supporting evidence. Independent review returned [advance](../history/campaigns/line-graph-two-cut/reviews/complete-rule/review.md).
Human expert assessment remains outstanding.

## Local facts

Color the edges of a simple root H with bits. For edge uv of color t, its opposite
adjacency count in L(H) equals the number of edges of color 1-t at u plus that at v.
No edge is counted twice, since H is simple. A legal local coloring allows at most
two opposites; constants are allowed locally. A target witness must additionally
use both colors.

A mixed root vertex has at most two incident edges of either color, hence degree
at most four. If its degree is four, the split is 2+2 and every neighbor is
monochromatic: each incident edge already has two opposites at the mixed endpoint.
Consequently every vertex of a K6 reservoir, and all its incident attachment edges,
is monochromatic. Connectivity of K6 makes their common color one reservoir bit.

The clause root has private vertices 0,1,2,3,4 and core edges, in order,
01,13,14,23,24,34. Terminal edges 0A,1B,3C have colors a,b,c. External endpoints
A,B,C must be monochromatic, so add no opposite cost. The terminal relation is
R(a,b,c) = not(a=c!=b). Constant terminals force all core edges constant.

Proof of exclusion: consider a=c=0, b=1. Vertex 1 cannot be mixed. Otherwise its
neighbors 0,3,4 are monochromatic. Terminals at 0 and 3 force edges 01,13,34 to
zero; monochromatic vertex 4 forces 14 to zero. Vertex 1 then has split 3+1,
contradicting its degree-four rule. Thus vertex 1 is monochromatic one. Vertex 3
is now mixed because 13=1 and its terminal is zero. Its neighbors 2 and 4 are
monochromatic. Edge 14=1 forces 24=34=1, then monochromatic vertex 2 forces
23=1. Vertex 3 again has split 3+1, a contradiction. Color complementation excludes
(a,b,c)=(1,0,1).

Proof for constant terminals: by complementation assume all zero. If vertex 1
were mixed, the preceding neighbor argument would force 01=13=14=0, so vertex 1
is monochromatic zero. If vertex 3 were mixed, its two remaining edges 23 and 34
would both be one. But its neighbor 4 must then be monochromatic, inconsistent
with 14=0 and 34=1. Thus 13=23=34=0. Finally 24 cannot be one: it would have two
opposites at vertex 4 and one at vertex 2. All core edges are zero.

Existence for every allowed triple follows by direct counting in this explicit
extension table. Strings follow the six-edge core order above; each displayed
extension has at most two opposites at every edge, including terminals.

| a b c | Core extension |
|---|---|
| 000 | 000000 |
| 001 | 011111 |
| 011 | 111111 |
| 100 | 000000 |
| 110 | 100000 |
| 111 | 111111 |

These arguments prove the needed local statements without assuming that finite
source tests generalize. The independent verifier additionally enumerates all
512 local assignments; uniqueness for nonconstant triples is not needed.

## Forward construction and recovery

For a connected legal source G with n >= 3, create a disjoint K6 Q_v for every
source vertex v. For each b and each unordered pair a,c of distinct neighbors
of b, ordered a<c, add a fresh clause core and terminal edges to fixed vertices
of Q_a,Q_b,Q_c, respectively. Root labels are assigned first to reservoirs in
source order (six each), then cores in lexicographic (b,a,c) order (five each).
Output reservoir edges first, 15 per reservoir in lexicographic order; output
each core's six edges followed by its three terminals. The executable uses this
order. All pairs are sorted within edges; the full edge list need not be sorted.

For n=1, output K1,5, whose line graph K5 is NO because any nontrivial split
has a vertex with at least three opposites. For n=2, output a two-edge path,
whose line graph is K2 and is YES. Recover [0,1] in the latter case. Invalid
source strings map to `{}`, outside the target language. The forward parser
rejects invalid schemas, booleans as integers, loops, repeated edges, disconnected
graphs and degree violations. Before allocating vertices, it rejects n>2m+1,
which no connected source can satisfy. JSON parse failures map to `{}`.

For n>=3 recover x_v from target edge position 15v, a fixed edge in Q_v. This
requires only the original source n and target witness; it works in a fresh
process. No source-solving oracle, preferred target witness or optimization
premise is used. No extraction obligation exists for the n=1 NO output or an
invalid source.

## Composition, equivalence and nontriviality

The root is simple: all cores are private, the three source vertices in a clause
are distinct, and each terminal joins a private vertex to a reservoir. It is
connected. Indeed, every source edge has at least one endpoint of degree at
least two when G is connected and n>=3. A corresponding clause connects both
endpoint reservoirs. Every core is connected and attached to those reservoirs.
This structural argument holds for both YES and NO sources.

If x is a source matching cut, every neighbor-pair triple satisfies R; otherwise
some vertex would have two opposite neighbors. Color each reservoir and all its
incident terminals by its source bit. Extend each clause by the table. At every
reservoir endpoint all incident edges agree, so the local zero-cost premise holds
regardless of the number of occurrences. Different cores share only such endpoints;
there is no unaccounted opposite cost. The resulting target coloring is valid and
nonconstant because the source uses both colors.

Conversely, take any nonconstant valid target edge coloring. Reservoir rigidity
assigns one bit x_v per source vertex and fixes every terminal color. Each clause
then satisfies R, so no source vertex has two opposite neighbors. If all x_v were
equal, all terminals of every clause would be equal and the constant-terminal
lemma would force every private edge to that same bit. This contradicts target
nontriviality. Thus the recovered x is a valid source witness. This proves both
YES/NO equivalence and recovery from every valid target witness.

## Bounds and implementation

Let T=sum_v binom(deg(v),2). For n>=3, T<=6n and the output has exactly
6n+5T vertices and 15n+9T edges, hence at most 36n vertices and 69n edges.
Root output bit length is O(n log(n+1)). Construction takes O(n) bounded-degree
graph operations plus serialization; the explicit line graph, if required instead
of its root, has O(n) vertices and O(n^2) edges and can be formed in polynomial time.
Recovery selects n positions and outputs n bits.

For arbitrary encoded input length L, checking and decoding binary integers,
JSON parsing and validation have conservative polynomial bit cost O((L+1)^3).
Python integer-set operations need no expected-time assumption for this bound:
even a worst-case quadratic comparison bound is polynomial. The preliminary
n<=2m+1 check prevents exponentially large allocations from binary n. On legal
inputs n<=L+1, so the construction and serialization also fit that bound.
Recovery has polynomial cost in the full encoded source-and-witness length,
including JSON parsing, and O(n) bit output. The executable uses no runtime solver,
randomness, external state or LLM decision.

## Literature and significance

Chvatal, *Recognizing decomposable graphs*, J. Graph Theory 8 (1984), 51–53,
https://doi.org/10.1002/jgt.3190080106, proves maximum-degree-four Matching Cut
NP-complete (the abstract states the same witness predicate). Restricting to
connected inputs preserves hardness: disconnected nonempty graphs with at least
two vertices are immediate YES instances and may map to K2; connected instances
are retained, and the empty input maps to a fixed connected NO graph.

Lucke, Momeni, Paulusma and Smith, *Finding d-Cuts in Graphs of Bounded Diameter,
Graphs of Bounded Radius and H-Free Graphs*, Algorithmica 88:7 (2026),
https://arxiv.org/html/2404.11389, Theorem 4.1 in the HTML and Section 5, proves
line-graph hardness for d>=3 and explicitly asks the d=2 case. Its clique-reservoir
technique is known; novelty is not claimed for that technique or for generic CSP
composition. The proposed contribution is the explicit diamond terminal relation
with constant-terminal rigidity and its use to obtain the missing d=2 reduction.
It would establish NP-completeness, since edge-color witnesses are polynomially
checkable. This is high importance within the line-graph d-Cut classification.

Search date: 2026-09-15. Queries included `"2-cut" "line graphs" complexity 2026`,
`"2-cut" "line graphs" solved`, `"line graphs" "2-Cut" diamond`, and
`"line graphs" "2-cut" "NP-complete" 2026 Ahn`. Inspected the arXiv HTML
construction and conclusion, the published-paper search text, and Chvatal's
primary publisher record. No exact prior resolution was located. Coverage does
not exclude unpublished, unindexed or overlooked results. The published PDF
initially failed to open through Web; no claim of reading its full proof is made.
