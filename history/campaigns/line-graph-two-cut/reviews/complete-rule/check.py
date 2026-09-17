import itertools
import json
from pathlib import Path
import subprocess
import sys

import z3


CANDIDATE = Path(__file__).resolve().parents[2] / 'work' / 'algorithm.py'


def execute(value, extract=False, raw=False):
    result = subprocess.run([sys.executable, str(CANDIDATE)] + (['--extract'] if extract else []),
                            input=value if raw else json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def valid_source(n, edges, bits):
    return (len(bits) == n and set(bits) == {0, 1}
            and all(sum(bits[u] != bits[v] for u, v in edges if w in (u, v)) <= 1 for w in range(n)))


def local_check():
    edges = [(0,1),(1,3),(1,4),(2,3),(2,4),(3,4),(0,5),(1,6),(3,7)]
    counts = {''.join(map(str, p)): 0 for p in itertools.product((0,1), repeat=3)}
    for bits in itertools.product((0,1), repeat=9):
        good = all(sum(bits[i] != bits[j] for j, f in enumerate(edges)
                       if i != j and set(e) & set(f)) <= 2 for i, e in enumerate(edges))
        if good:
            key = ''.join(map(str, bits[6:]))
            counts[key] += 1
            if len(set(bits[6:])) == 1:
                assert len(set(bits)) == 1
    assert {key for key, count in counts.items() if count} == {'000','001','011','100','110','111'}
    return counts


def check_instance(name, n, edges):
    source = {'n': n, 'edges': [list(e) for e in edges]}
    target = execute(source)
    vertices, root = target['n'], target['edges']
    assert vertices >= 3 and len(root) >= 2
    assert all(type(u) is int and type(v) is int and 0 <= u < v < vertices for u, v in root)
    assert len(set(map(tuple, root))) == len(root)
    reached = {0}
    while True:
        after = reached | {w for u, v in root if u in reached or v in reached for w in (u, v)}
        if after == reached:
            break
        reached = after
    assert len(reached) == vertices
    bits = z3.Bools(' '.join(f'e{i}' for i in range(len(root))))
    solver = z3.Solver()
    solver.add(z3.Or(bits), z3.Or([z3.Not(b) for b in bits]))
    for i, edge in enumerate(root):
        adjacent = [j for j, other in enumerate(root) if j != i and set(edge) & set(other)]
        solver.add(z3.Sum([z3.If(bits[i] != bits[j], 1, 0) for j in adjacent]) <= 2)
    expected = any(valid_source(n, edges, p) for p in itertools.product((0,1), repeat=n))
    decision = solver.check()
    assert decision in (z3.sat, z3.unsat) and (decision == z3.sat) == expected
    recoveries = 0
    if decision == z3.sat:
        model = solver.model()
        witness = [int(z3.is_true(model.eval(b, model_completion=True))) for b in bits]
        for y in (witness, [1-v for v in witness]):
            x = execute({'source': source, 'target_solution': y}, extract=True)
            assert valid_source(n, edges, x)
            recoveries += 1
    if n >= 3:
        x = [bits[15*v] for v in range(n)]
        bad = [z3.And(x), z3.And([z3.Not(v) for v in x])]
        for v in range(n):
            neighbors = [b if a == v else a for a, b in edges if v in (a, b)]
            bad.append(z3.Sum([z3.If(x[v] != x[u], 1, 0) for u in neighbors]) > 1)
        solver.add(z3.Or(bad))
        assert solver.check() == z3.unsat
    return {'name': name, 'source_yes': expected, 'vertices': vertices, 'edges': len(root),
            'recoveries': recoveries, 'bad_projection': 'UNSAT' if n >= 3 else 'special case'}


if __name__ == '__main__':
    cases = [('singleton', 1, []), ('edge', 2, [(0,1)]),
             ('two_cliques_bridge', 8, list(itertools.combinations(range(4),2))
              + list(itertools.combinations(range(4,8),2)) + [(0,4)]),
             ('complete_bipartite', 8, [(a,b) for a in range(4) for b in range(4,8)]),
             ('degree_four_tree', 7, [(0,1),(0,2),(0,3),(0,4),(1,5),(1,6)])]
    malformed = ['{', '[]', '{"n":true,"edges":[]}', '{"n":' + '9'*5000 + ',"edges":[]}',
                 '['*2000 + '0' + ']'*2000]
    for item in malformed:
        assert execute(item, raw=True) == {}
    print(json.dumps({'local_assignments': 512, 'local_extension_counts': local_check(),
                      'invalid_strings': len(malformed),
                      'instances': [check_instance(*case) for case in cases]}, indent=2))
