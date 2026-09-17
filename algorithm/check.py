import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import networkx as nx
import z3


def graph(data, target=False):
    assert type(data) is dict and set(data) == {'n', 'edges'}
    n, edges = data['n'], data['edges']
    assert type(n) is int and n >= 1 and type(edges) is list
    assert all(type(e) is list and len(e) == 2 and all(type(v) is int for v in e)
               and 0 <= e[0] < e[1] < n for e in edges)
    assert len({tuple(e) for e in edges}) == len(edges)
    g = nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(edges)
    assert nx.is_connected(g)
    assert len(edges) >= 2 if target else max(dict(g.degree()).values()) <= 4
    return g


def adjacency(data, target):
    g = graph(data, target)
    if not target:
        return [list(g[v]) for v in range(data['n'])]
    edges = data['edges']
    return [[j for j, f in enumerate(edges) if i != j and set(e) & set(f)]
            for i, e in enumerate(edges)]


def valid(data, bits, target=False):
    adj = adjacency(data, target)
    return (type(bits) is list and len(bits) == len(adj)
            and all(type(b) is int and b in (0, 1) for b in bits)
            and len(set(bits)) == 2
            and all(sum(bits[i] != bits[j] for j in row) <= (2 if target else 1)
                    for i, row in enumerate(adj)))


def solve(data, target=False, limit=1):
    adj = adjacency(data, target)
    x = [z3.Bool(f'x{i}') for i in range(len(adj))]
    s = z3.Solver(); s.add(z3.Or(x), z3.Or([z3.Not(v) for v in x]))
    for i, row in enumerate(adj):
        s.add(z3.Sum([z3.If(x[i] != x[j], 1, 0) for j in row]) <= (2 if target else 1))
    out = []
    for _ in range(limit):
        status = s.check()
        if status == z3.unsat:
            break
        assert status == z3.sat, status
        m = s.model(); bits = [int(z3.is_true(m.eval(v))) for v in x]
        assert valid(data, bits, target)
        out.append(bits); s.add(z3.Or([v != bool(b) for v, b in zip(x, bits)]))
    return out


def call(path, payload, extract=False):
    p = subprocess.run([sys.executable, str(path)] + (['--extract'] if extract else []),
                       input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def check(path, cases):
    recoveries = 0
    for case in cases:
        source = case['source']; target = call(path, source)
        witnesses = solve(target, True, 16)
        assert bool(witnesses) == case['yes'], {'source': source, 'target': target}
        for y in witnesses:
            recovered = call(path, {'source': source, 'target_solution': y}, True)
            assert valid(source, recovered), {'source': source, 'target': target, 'witness': y, 'recovered': recovered}
            recoveries += 1
    return {'cases': len(cases), 'recoveries': recoveries}


def self_test(cases):
    counts = [0, 0]
    for g in nx.graph_atlas_g():
        if not 1 <= len(g) <= 5 or not nx.is_connected(g):
            continue
        data = {'n': len(g), 'edges': [sorted(e) for e in g.edges()]}
        for target in (False, True):
            if target and g.number_of_edges() < 2:
                continue
            n = g.number_of_edges() if target else len(g)
            expected = {bits for bits in itertools.product((0, 1), repeat=n) if valid(data, list(bits), target)}
            actual = {tuple(bits) for bits in solve(data, target, 2**n + 1)}
            assert expected == actual
            assert not valid(data, [0] * n, target)
            counts[target] += 1
    for c in cases:
        assert bool(solve(c['source'])) == c['yes']
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory) / 'bad.py'
        fixtures = [('import json; print(json.dumps({}))', cases[:1]),
                    ('import json; print(json.dumps({"n":3,"edges":[[0,1],[1,2]]}))', [c for c in cases if not c['yes']][:1]),
                    ('import sys,json; print(json.dumps([0,0] if "--extract" in sys.argv else {"n":3,"edges":[[0,1],[1,2]]}))', [c for c in cases if c['yes']][:1])]
        for script, subset in fixtures:
            p.write_text(script)
            try:
                check(p, subset)
            except AssertionError:
                pass
            else:
                raise AssertionError('Incorrect fixture was accepted')
    print(json.dumps({'solver': z3.get_version_string(), 'source_graphs': counts[0], 'target_roots': counts[1], 'stored_cases': len(cases), 'rejected_fixtures': 3}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--self-test', action='store_true'); parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    if args.self_test:
        self_test(cases)
    elif args.candidate:
        print(json.dumps(check(args.candidate.resolve(), cases)))
    else:
        parser.error('Choose --self-test or --candidate')
