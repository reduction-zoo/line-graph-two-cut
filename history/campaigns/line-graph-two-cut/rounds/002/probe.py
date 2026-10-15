import itertools
import json
import networkx as nx
cores = templates = colorings = hits = 0
relations = {}; first = None
for g in nx.graph_atlas_g():
    n = len(g)
    if not 1 <= n <= 5 or not nx.is_connected(g) or g.number_of_edges() > 7:
        continue
    cores += 1
    for ports in itertools.combinations_with_replacement(range(n), 3):
        edges = list(g.edges()) + [(v, n+i) for i, v in enumerate(ports)]
        m = len(edges); templates += 1
        masks = [sum(1 << j for j,f in enumerate(edges) if i != j and set(e) & set(f)) for i,e in enumerate(edges)]
        relation = set(); constant_forces = True
        for bits in range(1 << m):
            colorings += 1
            if any(((mask & (bits if not (bits >> i & 1) else ((1 << m)-1) ^ bits)).bit_count() > 2) for i,mask in enumerate(masks)):
                continue
            terminal = bits >> (m-3); relation.add(terminal)
            if terminal in (0,7) and bits not in (0,(1<<m)-1):
                constant_forces = False
        key = ','.join(map(str,sorted(relation))); relations[key] = relations.get(key,0)+1
        if len(relation) == 6 and 0 in relation and 7 in relation:
            hits += 1
            if first is None:
                first = {'n':n+3,'edges':edges,'relation':sorted(relation),'constant_forces':constant_forces,'ports':ports}
print(json.dumps({'cores':cores,'templates':templates,'colorings':colorings,'hits':hits,'first':first,'relations':relations},indent=2))
