# Encoding contract

Both instances are JSON objects with exactly `n` and `edges`. Vertices are integers
0 through n-1. Each edge is a two-integer list [u,v] with u < v; edges are distinct.
The edge-list order defines target witness positions. Graphs are connected and
simple. Source graphs have n >= 1 and maximum degree at most four. Target roots
have at least two edges. Invalid strings are outside the corresponding language.
A total forward map may send invalid sources to `{}`, outside the target language;
all legal sources, including NO instances, must produce legal target roots.

A source witness is an n-bit integer list using both values, with at most one
opposite neighbor per vertex. A target witness is an |E(H)|-bit list using both
values, with at most two opposite-colored adjacent root edges per edge. This is
exactly a 2-cut of L(H). Constants are not witnesses.

`python3 algorithm.py` reads a source JSON string and emits its target root.
`python3 algorithm.py --extract` reads `{"source":...,"target_solution":...}`
and emits a source witness, for every valid witness of that constructed output.
Both modes are deterministic polynomial-time algorithms in fresh subprocesses.
Diagnostics use stderr; execution failure is nonzero. General equivalence,
structural legality, nontriviality, and polynomial time/bit size require proofs.
