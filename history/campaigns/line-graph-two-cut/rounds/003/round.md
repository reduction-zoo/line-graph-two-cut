# Round 003 — Reservoir composition and full rule

## Plan

Use [diamond interface](../../../../research/experience/line-graph-diamond-matching-cut-interface.md)
with zero external opposite cost supplied by K6 reservoirs. Each source vertex
gets a K6. For each unordered neighbor pair a,c of source vertex b, add the
six-edge core and connect its three terminal edges to reservoirs a,b,c.
Read one fixed reservoir edge to recover each source bit. Connected sources
with one or two vertices need explicit constant-size handling.

First discriminating check: independently pin all eight terminal assignments,
verify the local table and constant-internal property, then use the prepared
source and target oracles on the eight stored cases. Additional scope: all
connected atlas source graphs on at most five vertices with maximum degree four,
and all 64 connected graphs formed by a six-cycle plus a subset of its six
length-two chords (retaining maximum degree four). Check up to four independently
solved target witnesses per extra instance. No larger source family is authorized.

The general proof must establish reservoir rigidity, the exact local relation,
composition, connectedness on NO inputs, nontriviality and deterministic polynomial
recovery. A complete successful rule proceeds through verification and independent
review within this round; substantive mechanism changes would need new allocation.

## Evidence and diagnosis

One composition mechanism produced one complete candidate, without algorithm repairs or reruns. The analytic proof establishes the exact relation, constant-terminal rigidity, arbitrary reservoir fan-out, connectedness and universal recovery. The local table was independently checked over all 512 assignments. Commands and raw results are linked by [verification](../../work/verification.md): eight prepared cases/22 recoveries, then 95 additional cases/106 recoveries (34 YES, 61 NO; maximum root 216 vertices and 414 edges).

[Independent review](../../reviews/complete-rule/review.md) returned advance. Its own checks add five complete instances, six recoveries and three UNSAT bad-projection queries, covering the current candidate through 288 root vertices and 552 edges. These finite results support the general proof, not extrapolation from tested source sizes. The reviewer also opened the published Algorithmica PDF: Theorem 13, pages 21–23, and Section 5, page 25, distinguish known d>=3 hardness from the retained d=2 question. The known ISAAC 2025 claw-free result does not supply this restriction. Novelty remains bounded by the documented search coverage.

The first discriminating check succeeded: constant reservoir colors cannot hide a nonconstant core coloring. Zero opposite cost at shared reservoir endpoints is the compositional reason, proved generally rather than inferred from tests. No mismatch or mathematical repair occurred. Time/token usage was not measured.

**Experience extraction:** updated the [diamond entry](../../../../research/experience/line-graph-diamond-matching-cut-interface.md) with its analytic proof, successful application and independent review; updated the [star entry](../../../../research/experience/line-graph-star-junction-relations.md) with the review's scope assessment. These are the same two files created in this allocation, not two additional entries. No extraction remains pending.

Writing used research-write and how-to-technical-writing. The native [Typst paper](../../work/manuscript.typ) compiles without diagnostics to six pages. Exact vector figures were checked against the listed adjacency. Every final page was inspected after repairs to subscript scope, two figure labels and an orphaned lemma statement. These editorial fixes do not change the reviewed theorem. Compilation and figure checks are in [typst.log](typst.log) and [figures-check.txt](figures-check.txt); rendered pages are under work/evidence/paper/.

## Next action

Stop discovery after completing the allocated three rounds. The [paper](../../work/manuscript.pdf) and complete rule are ready for human expert assessment. No production integration or publication was performed.
