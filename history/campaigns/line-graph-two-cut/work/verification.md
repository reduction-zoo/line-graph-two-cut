# Verification

The current `algorithm.py` passed the prepared checker: eight source cases and
22 recovered target witnesses; [raw evidence](../rounds/003/prepared-check.json).
A separate `verify.py` imports neither the candidate nor the prepared checker.
It brute-forces source witnesses and uses Z3 incident-edge constraints for actual
subprocess outputs, directly recounting all returned target and source witnesses.

Additional scope: all 31 connected atlas graphs through five vertices and 64
six-cycle/chord instances, each of maximum degree at most four. All 95
instances passed: 34 YES, 61 NO, 106 recoveries.
Largest output: 216 vertices and 414 edges.
The eight-row local interface table was independently checked over all 512
assignments. See [raw evidence](../rounds/003/verification.json).

Commands from the repository root:

```sh
python3 campaigns/line-graph-two-cut/work/check.py --candidate campaigns/line-graph-two-cut/work/algorithm.py
python3 campaigns/line-graph-two-cut/work/verify.py --candidate campaigns/line-graph-two-cut/work/algorithm.py
```

No mismatches, repairs or reruns occurred. Finite instance tests do not prove
arbitrary-size correctness or universal witness recovery; `proof.md` supplies
those arguments. Independent review returned [advance](../reviews/complete-rule/review.md);
its targeted checks add five instances and six recoveries. Novelty is supported
within that review's coverage; human expert assessment remains outstanding.
