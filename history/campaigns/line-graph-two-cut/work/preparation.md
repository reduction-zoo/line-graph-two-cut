# Testing foundation

Z3 5.1.0 decides both languages by one Boolean per source vertex or target root
edge, a nonconstant constraint and the corresponding opposite-neighbor sum bound.
SAT assignments are checked by direct counting; only UNSAT means NO, and unknown
fails explicitly. Every satisfying assignment is a witness by these exact
constraints, and every witness satisfies the encoding. No timeout is configured.

`python3 campaigns/line-graph-two-cut/work/check.py --self-test` passed:
[raw evidence](evidence/preparation/self-test.json). Z3 and exhaustive enumeration
agree on every witness of 31 connected source graphs and 29 eligible target roots
in the graph atlas through five vertices (at most ten target edges). Eight stored
source cases cover YES, NO, degree four, a singleton and bipartite graphs.
Three executed bad programs were rejected for malformed output, wrong decision,
and invalid recovery. Constants are rejected by both witness validators.

`--candidate PATH` executes actual forward outputs and recovery in separate
subprocesses and validates up to 16 distinct solver-produced witnesses per YES
target. The completed candidate subsequently passed this harness; see
[verification](verification.md). Arbitrary-size correctness and universal recovery
follow from the separately reviewed proof, not these finite checks.
