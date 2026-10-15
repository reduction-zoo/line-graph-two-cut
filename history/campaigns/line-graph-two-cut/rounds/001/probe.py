import itertools
import json
wanted = {x for x in itertools.product((0, 1), repeat=3) if not (x[0] == x[2] != x[1])}
results = []
for total in range(3, 7):
    for m in itertools.product(range(1, total), repeat=3):
        if sum(m) != total:
            continue
        relation = []
        for bits in itertools.product((0, 1), repeat=3):
            colors = [b for b, count in zip(bits, m) for _ in range(count)]
            if all(sum(c != d for d in colors) <= 2 for c in colors):
                relation.append(bits)
        results.append({'multiplicities': m, 'relation': relation, 'matches': set(relation) == wanted})
print(json.dumps({'templates': len(results), 'assignments': 8 * len(results), 'matches': sum(r['matches'] for r in results), 'results': results}, indent=2))
