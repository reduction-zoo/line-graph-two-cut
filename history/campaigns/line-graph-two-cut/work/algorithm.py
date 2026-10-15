import itertools
import json
import sys


def source_graph(data):
    if type(data) is not dict or set(data) != {'n', 'edges'}:
        return None
    n, edges = data['n'], data['edges']
    if type(n) is not int or n < 1 or type(edges) is not list or n > 2 * len(edges) + 1:
        return None
    adj = [set() for _ in range(n)]
    for e in edges:
        if (type(e) is not list or len(e) != 2 or any(type(v) is not int for v in e)
                or not 0 <= e[0] < e[1] < n or e[1] in adj[e[0]]):
            return None
        u, v = e; adj[u].add(v); adj[v].add(u)
        if len(adj[u]) > 4 or len(adj[v]) > 4:
            return None
    seen = {0}; stack = [0]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return adj if len(seen) == n else None


def forward(data):
    adj = source_graph(data)
    if adj is None:
        return {}
    n = len(adj)
    if n == 1:
        return {'n': 6, 'edges': [[0, i] for i in range(1, 6)]}
    if n == 2:
        return {'n': 3, 'edges': [[0, 1], [1, 2]]}
    edges = [[6*v+i, 6*v+j] for v in range(n) for i,j in itertools.combinations(range(6), 2)]
    count = 6*n
    for b in range(n):
        for a,c in itertools.combinations(sorted(adj[b]), 2):
            edges.extend([[count+i, count+j] for i,j in [(0,1),(1,3),(1,4),(2,3),(2,4),(3,4)]])
            edges.extend([sorted([count+i, 6*v]) for i,v in [(0,a),(1,b),(3,c)]])
            count += 5
    return {'n': count, 'edges': edges}


def extract(data):
    source, y = data['source'], data['target_solution']
    if source['n'] == 2:
        return [0, 1]
    return [y[15*v] for v in range(source['n'])]


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, RecursionError):
        if '--extract' in sys.argv:
            raise
        print('{}')
    else:
        print(json.dumps(extract(data) if '--extract' in sys.argv else forward(data)))
