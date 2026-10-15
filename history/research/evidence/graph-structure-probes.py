"""Finite screening checks, not proofs of the portfolio's open questions."""
from itertools import combinations, permutations, product
import time
import networkx as nx


def cuts(g, perfect=False):
    vertices = list(g)
    answers = []
    for tail in product((0, 1), repeat=len(vertices) - 1):
        color = dict(zip(vertices, (0,) + tail))
        counts = [sum(color[u] != color[v] for u in g[v]) for v in g]
        if any(tail) and all(c == 1 if perfect else c <= 1 for c in counts):
            answers.append(color)
    return answers


def line_graphs():
    root = nx.complete_graph(4)
    root.add_edges_from((v, v + 4) for v in range(3))
    variable = nx.line_graph(root)
    assert len(variable) == 9 and variable.number_of_edges() == 21
    legal = 0
    for bits in product((0, 1), repeat=9):
        color = dict(zip(variable, bits))
        legal += all(sum(color[u] != color[v] for u in variable[v]) <= 2
                     for v in variable)
    assert legal == 2
    clause = nx.complete_graph(5)
    clause.add_edges_from([(5, 0), (5, 1), (6, 0), (6, 1), (6, 5),
                           (7, 2), (7, 3), (7, 4), (8, 5)])
    try:
        nx.inverse_line_graph(clause)
    except nx.NetworkXError:
        pass  # Expected rejection: the existing clause has no simple root.
    else:
        raise AssertionError('The clause unexpectedly has a simple line-graph root')
    # Check the root-edge counting identity independently on every small root.
    checked = 0
    for g in nx.graph_atlas_g():
        if not 2 <= len(g) <= 5 or not nx.is_connected(g):
            continue
        edges = list(g.edges())
        h = nx.line_graph(g)
        for bits in product((0, 1), repeat=len(edges)):
            color = dict(zip(edges, bits))
            for e in edges:
                opposite = sum(color[f] != color[e] for f in h[e])
                incident = sum(color[f] != color[e] for v in e for f in edges if v in f)
                assert opposite == incident
            checked += 1
    print(f'LINE: rigid simple-root variable; clause rejected; {checked} root colorings checked')


def radius_three():
    total = matching = perfect = 0
    for g in nx.graph_atlas_g():
        if len(g) < 2 or not nx.is_connected(g) or not nx.is_bipartite(g):
            continue
        if nx.radius(g) != 3:
            continue
        total += 1
        matching += bool(cuts(g))
        perfect += bool(cuts(g, True))
    tree, cube = nx.path_graph(7), nx.cubical_graph()
    tree.add_edge(1, 7)
    assert nx.radius(tree) == nx.radius(cube) == 3
    assert cuts(tree) and not cuts(tree, True) and cuts(cube, True)
    print(f'RADIUS: atlas through 7 vertices: {total} graphs, MC={matching}, PMC={perfect}')
    print('RADIUS: P7 plus leaf at vertex 1 has MC but no PMC; Q3 has both')


def triple_partitions(items):
    if not items:
        yield ()
        return
    for pair in combinations(items[1:], 2):
        triple = (items[0],) + pair
        rest = tuple(x for x in items if x not in triple)
        for suffix in triple_partitions(rest):
            yield (triple,) + suffix


def crossing_load(stars, order):
    rank = {s: i for i, s in enumerate(order)}
    return max(sum((x - y) * (rank[s] - rank[t]) < 0
                   for t, leaves in enumerate(stars) if t != s for y in leaves)
               for s, leaves in enumerate(stars) for x in leaves)


def stars():
    checked, failures, first = 0, 0, None
    for instance in triple_partitions(tuple(range(9))):
        values = [(crossing_load(instance, order), order)
                  for order in permutations(range(3))]
        optimum, order = min(values)
        median = tuple(sorted(range(3), key=lambda s: instance[s][1]))
        measured = crossing_load(instance, median)
        checked += 1
        if measured > optimum:
            failures += 1
            if first is None:
                first = (instance, median, measured, order, optimum)
    assert checked == 280
    print(f'STARS: all {checked} partitions into 3 triples; median failures={failures}; first={first}')


def induced_paths():
    # ponytail: cap each DFS at 200,000 states; larger cases need a stronger proof or search.
    for q, p in ((5, 3), (7, 3), (7, 4), (7, 5), (9, 3), (9, 4)):
        n, target = q * p - 2, 3 * q - 2
        adj = [{(i + d) % n for d in [-1, 1] + [q * j - 1 for j in range(1, p)]}
               for i in range(n)]
        assert all(i not in adj[i] and all(i in adj[j] for j in adj[i]) for i in range(n))
        visits, maximum = 0, 1
        started = time.monotonic()

        def dfs(path, blocked):
            nonlocal visits, maximum
            visits += 1
            if visits > 200_000 or time.monotonic() - started > 5:
                raise TimeoutError('bounded induced-path search exhausted')
            maximum = max(maximum, len(path))
            if len(path) == target:
                return path
            for v in sorted(adj[path[-1]] - blocked - set(path)):
                answer = dfs(path + (v,), blocked | adj[path[-1]])
                if answer:
                    return answer
            return None

        try:
            witness = dfs((0,), set())  # Translation symmetry covers all starting vertices.
            status = 'COUNTEREXAMPLE' if witness else 'EXHAUSTIVE ABSENCE'
        except TimeoutError:
            status, witness = 'UNKNOWN (cap)', None
        if witness:
            assert all((witness[j] in adj[witness[i]]) == (j == i + 1)
                       for i in range(len(witness)) for j in range(i + 1, len(witness)))
        print(f'PATH: q={q}, p={p}, n={n}, target={target}, states={visits}, '
              f'max_seen={maximum}, status={status}, witness={witness}')


if __name__ == '__main__':
    line_graphs()
    radius_three()
    stars()
    induced_paths()
