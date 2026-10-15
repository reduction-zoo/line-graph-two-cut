import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import networkx as nx
import z3


def invoke(path, data, extract=False):
    return json.loads(subprocess.run([sys.executable,str(path)] + (['--extract'] if extract else []), input=json.dumps(data), text=True, capture_output=True, check=True).stdout)


def source_witness(source, x):
    return (type(x) is list and len(x) == source['n'] and all(type(v) is int and v in (0,1) for v in x)
            and len(set(x)) == 2 and all(sum(x[u] != x[v] for u,v in source['edges'] if u == i or v == i) <= 1 for i in range(source['n'])))


def target_models(data):
    assert set(data) == {'n','edges'} and type(data['n']) is int
    n, edges = data['n'],data['edges']; assert n >= 1 and len(edges) >= 2
    assert all(len(e)==2 and all(type(v)is int for v in e) and 0<=e[0]<e[1]<n for e in edges)
    assert len(set(map(tuple,edges))) == len(edges)
    g=nx.Graph();g.add_nodes_from(range(n));g.add_edges_from(edges);assert nx.is_connected(g)
    x=[z3.Bool(f'e{i}') for i in range(len(edges))];s=z3.Solver()
    s.add(z3.Or(x),z3.Or([z3.Not(v) for v in x]))
    incident=[[i for i,e in enumerate(edges) if v in e] for v in range(n)]
    for i,(u,v) in enumerate(edges):
        s.add(z3.Sum([z3.If(x[i]!=x[j],1,0) for j in incident[u]+incident[v]])<=2)
    result=[]
    for _ in range(4):
        status=s.check()
        if status==z3.unsat: break
        assert status==z3.sat,status
        bits=[int(z3.is_true(s.model().eval(v))) for v in x]
        assert len(set(bits))==2
        assert all(sum(bits[i]!=bits[j] for j,f in enumerate(edges) if i!=j and any(v in f for v in e))<=2 for i,e in enumerate(edges))
        result.append(bits);s.add(z3.Or([v!=bool(b) for v,b in zip(x,bits)]))
    return result


def local_certificate():
    edges=[(0,1),(1,3),(1,4),(2,3),(2,4),(3,4),(0,5),(1,6),(3,7)]
    table={}
    for terminals in itertools.product((0,1),repeat=3):
        extensions=[]
        for core in itertools.product((0,1),repeat=6):
            x=core+terminals
            if all(sum(x[i]!=x[j] for j,f in enumerate(edges) if i!=j and set(e)&set(f))<=2 for i,e in enumerate(edges)):
                extensions.append(''.join(map(str,core)))
        assert bool(extensions)==not_relation(terminals)
        if len(set(terminals))==1:
            assert extensions==[str(terminals[0])*6]
        table[''.join(map(str,terminals))]=extensions
    return table


def not_relation(t):
    return not(t[0]==t[2]!=t[1])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',required=True,type=Path);args=p.parse_args()
    graphs=[g for g in nx.graph_atlas_g() if 1<=len(g)<=5 and nx.is_connected(g) and max(dict(g.degree()).values())<=4]
    chords=[(0,2),(1,3),(2,4),(3,5),(0,4),(1,5)]
    for mask in range(64):
        g=nx.cycle_graph(6);g.add_edges_from(e for i,e in enumerate(chords) if mask>>i&1)
        if max(dict(g.degree()).values())<=4: graphs.append(g)
    records=[]
    for g in graphs:
        source={'n':len(g),'edges':[sorted(e) for e in g.edges()]}
        yes=any(source_witness(source,list(bits)) for bits in itertools.product((0,1),repeat=len(g)))
        target=invoke(args.candidate,source);witnesses=target_models(target)
        if bool(witnesses)!=yes:
            Path(__file__).with_name('failure.json').write_text(json.dumps({'source':source,'target':target,'yes':yes,'witnesses':witnesses}));raise AssertionError('Decision mismatch')
        for y in witnesses:
            recovered=invoke(args.candidate,{'source':source,'target_solution':y},True)
            if not source_witness(source,recovered):
                Path(__file__).with_name('failure.json').write_text(json.dumps({'source':source,'target':target,'witness':y,'recovered':recovered}));raise AssertionError('Recovery mismatch')
        records.append({'source':source,'yes':yes,'target_vertices':target['n'],'target_edges':len(target['edges']),'recoveries':len(witnesses)})
    print(json.dumps({'local_table':local_certificate(),'instances':len(records),'yes':sum(r['yes'] for r in records),'recoveries':sum(r['recoveries'] for r in records),'records':records},indent=2))
