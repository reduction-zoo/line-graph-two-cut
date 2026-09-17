# Independent review

**Decision: advance.** Reviewed on 2026-09-15. The complete forward construction
and witness recovery are eligible for expert review. No blocking correctness gap
was found. Novelty is supported within the primary-literature coverage below;
this decision is neither human verification nor publication acceptance.

## Correctness

Reviewed the fixed question and current `work/contract.md`, `algorithm.py`,
`proof.md`, `preparation.md`, and `verification.md`. The candidate and checkers
were not imported or modified. The following conclusions concern the general
argument, rather than extrapolation from the finite tests.

- **Local counting and reservoirs.** Simplicity makes the two endpoint counts
  disjoint. A mixed vertex has at most two incident edges of each color. A mixed
  degree-four vertex therefore has a 2+2 split, and its neighbors must be
  monochromatic. Every K6 vertex has degree at least five, including after
  attachment, so every reservoir and all incident terminals share one color.
  Attachments cannot consume any opposite-color budget at the reservoir end.
- **Exact interface.** The argument in `proof.md`, “Local facts”, excludes 010
  and 101 correctly. In the mixed-vertex-1 case, monochromatic neighbors force
  three zero core edges against the one terminal edge; in the monochromatic case,
  vertex 3 is forced into the forbidden 3+1 split. The constant-terminal argument
  then forces vertex 1 and vertex 3 to zero and excludes a residual one on 24 by
  its three opposite adjacent edges. The six displayed extensions satisfy every
  core and terminal constraint. No unstated uniqueness premise is needed.
- **Composition.** All clause cores are private and their terminal endpoints
  are monochromatic. Sharing reservoir vertices across arbitrarily many clauses
  adds no opposite cost. Every source edge in a connected graph on at least three
  vertices occurs in some neighbor-pair clause, so the root is connected even on
  NO inputs. Distinct labels and terminal endpoints also ensure simplicity.
- **Equivalence and recovery.** The forbidden triple is exactly the event that
  a vertex has two opposite neighbors. A legal source cut extends independently
  over all cores. Conversely, every target witness fixes reservoir bits satisfying
  every source constraint. If those bits were all equal, constant-terminal
  rigidity would force the entire target constant. The implemented positions
  `y[15*v]` select reservoir edges in the actual output order, so this argument
  applies to every valid target witness, including either color orientation.
- **Totality and bounds.** The singleton and two-vertex cases have the stated NO
  and YES outputs. Invalid source encodings are rejected before unsafe allocations;
  integer types, schema, ordering, duplicate edges, degree and connectivity are
  checked. The early n-versus-edge-count check is necessary for a binary encoding.
  The parser disables the decimal digit cap and handles malformed or excessively
  nested JSON. On legal sources, T is at most 6n, yielding exactly 6n+5T vertices
  and 15n+9T edges. The conservative polynomial bit-cost claim is sufficient;
  extraction reads n fixed positions and requires no oracle or saved state.

The shared [diamond interface](../../../../research/experience/line-graph-diamond-matching-cut-interface.md)
was inspected: its zero-external-cost premise is supplied by the reservoirs and
its terminal ordering agrees with the implementation. Its finite certificate is
also backed here by the analytic argument above. The
[star-junction limitation](../../../../research/experience/line-graph-star-junction-relations.md)
is a correctly scoped local exclusion, not a necessary premise of the final
reduction. No exact-one Perfect Matching Cut assumption is imported.

## Independent targeted evidence

[check.py](check.py) uses its own brute-force source predicate and its own Z3
edge-adjacency constraints. It executes the actual candidate and extractor in
fresh subprocesses. Run from the repository root:

```sh
python3 campaigns/line-graph-two-cut/reviews/complete-rule/check.py
```

[evidence.json](evidence.json) records a successful run:

- All 512 local assignments were counted independently. The six allowed triples
  have one extension each; 010 and 101 have none. Constant-terminal rigidity holds.
- Five complete source instances passed: singleton, edge, two K4s joined by a
  bridge, K4,4, and a degree-four tree. The largest actual root has 288 vertices
  and 552 edges. All roots passed direct simplicity and connectivity checks.
- Six actual witness recoveries passed, including complemented witnesses.
  For each of the three nonspecial instances, the solver also found UNSAT after
  demanding a nonconstant legal target coloring whose reservoir projection is
  constant or violates a source constraint. This checks all witnesses of those
  particular outputs, not all possible source instances.
- Five invalid strings mapped to `{}`, including a 5,000-digit vertex count and
  depth-2,000 malformed-schema input.

These checks supplement, rather than repeat, the existing full verification.
They do not replace the general proof.

## Novelty

Primary sources checked on 2026-09-15:

1. Chvatal, [Recognizing decomposable graphs](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.3190080106),
   J. Graph Theory 8 (1984), pp. 51–53. The publisher abstract defines precisely
   the nontrivial matching-cut predicate and states hardness at maximum degree
   four. Full source proof was not retrieved. The candidate's elementary
   connected-input restriction preserves this hardness.
2. Lucke et al., [Finding d-Cuts in Graphs of Bounded Diameter, Graphs of Bounded Radius and H-Free Graphs](https://eprints.cs.univie.ac.at/8514/1/Finding_d_cuts_in_Graphs_ALGORITMICA.pdf),
   Algorithmica 88:7 (2026). The published PDF was successfully opened during
   review. Theorem 13 and its construction, PDF pages 21–23, cover d >= 3 via
   positive NAE satisfiability and clique reservoirs. In particular, the argument
   uses inequalities that fail at d = 2. Section 5, PDF page 25, explicitly retains
   the line-graph 2-Cut question. Thus the current result is not merely a missing
   citation to that theorem. Reservoir rigidity is known and must not be claimed
   as novel. The root edge-coloring formulation is also explicitly present there.
3. Ahn et al., [Finding d-Cuts in Claw-Free Graphs](https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/html/LIPIcs.ISAAC.2025.4/LIPIcs.ISAAC.2025.4.html),
   ISAAC 2025, Theorem 4 and its proof in Section 4. This already establishes
   claw-free hardness for d = 2. It does not establish the simple-line-graph
   restriction; the published Algorithmica conclusion explicitly distinguishes
   these cases. Its clause construction differs from the current root interface.

Search queries included `"2-cut" "line graphs" "NP-complete"`,
`"2-cut" "line graphs" diamond`, `"2-Cut" "line graphs" 2026 2025 solved`,
`"red-blue edge 2-colouring" complexity`, and
`"Finding d-cuts in claw-free graphs" line graphs`. Inspected the arXiv record
2505.17993 and HTML 2404.11389 alongside the primary published sources. Results
about two-vertex separators or proper edge colorings were not treated as this
decision problem.

No exact prior resolution was located. This is a supported, bounded novelty
assessment, not proof of absence from the literature. Unindexed, unpublished and
overlooked work remains outside coverage. The novelty claim should concern the
explicit interface and resulting missing-case hardness, not generic gadget
composition or clique rigidity.

## Significance and closure

The candidate meets the fixed endpoints and provides the whole Karp rule,
including universal witness recovery and explicit size bounds. Combined with
source hardness and polynomial certificate checking, it establishes
NP-completeness for the line-graph case retained in the cited literature. That
is a meaningful classification result within this problem family. No stronger
venue or acceptance claim is warranted.

No algorithm or proof repair is requested. Before campaign closure, update the
preparation report's historical “No candidate exists yet” sentence, close the
pending round record, and record the diamond entry's actual use. These are
artifact-status updates, not missing mathematical premises. The final paper
should cite the published Theorem 13 and acknowledge the known claw-free result.
