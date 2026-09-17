from pathlib import Path
import itertools
import math
from xml.sax.saxutils import escape
out = Path(__file__).resolve().parents[2] / 'work/figures'


def svg(path, width, height, pos, edges, labels, ports=()):
    assert len({tuple(sorted(e)) for e in edges}) == len(edges)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/>']
    for u,v in edges:
        x,y=pos[u];xx,yy=pos[v]
        parts.append(f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="#555" stroke-width="2"/>')
    for v,(x,y) in pos.items():
        parts.append(f'<circle cx="{x}" cy="{y}" r="{8 if v in ports else 5}" fill="{"white" if v in ports else "#222"}" stroke="#222" stroke-width="2"/>')
        if v in labels:
            text,dx,dy=labels[v]
            parts.append(f'<text x="{x+dx}" y="{y+dy}" font-family="serif" font-size="19" text-anchor="middle">{escape(text)}</text>')
    parts.append('</svg>');path.write_text(''.join(parts))

core=[(0,1),(1,3),(1,4),(2,3),(2,4),(3,4)]
edges=core+[(0,5),(1,6),(3,7)]
pos={0:(100,85),1:(220,85),2:(340,190),3:(340,85),4:(220,190),5:(25,85),6:(220,20),7:(440,85)}
labels={i:(str(i),0,28) for i in range(5)};labels[1]=('1',-18,25);labels[3]=('3',18,25);labels.update({5:('A',0,30),6:('B',27,5),7:('C',0,30)})
assert len(edges)==9 and len(pos)==8
svg(out/'interface.svg',480,240,pos,edges,labels,(5,6,7))
pos={};labels={};edges=[]
for cluster,(cx,cy) in enumerate([(85,85),(265,85),(445,85)]):
    for i in range(6):
        angle=math.pi/2 + i*math.pi/3
        pos[6*cluster+i]=(cx+44*math.cos(angle),cy+44*math.sin(angle))
    edges += [(6*cluster+i,6*cluster+j) for i,j in itertools.combinations(range(6),2)]
    labels[6*cluster+3]=(f'Q{chr(97+cluster)}',0,-22)
pos.update({18:(85,205),19:(200,205),20:(340,300),21:(365,205),22:(220,300)})
labels.update({18:('0',-18,0),19:('1',0,28),20:('2',20,7),21:('3',18,5),22:('4',0,28)})
edges += [(18+u,18+v) for u,v in core]+[(18,0),(19,6),(21,12)]
assert len(pos)==23 and len(edges)==54
svg(out/'composition.svg',530,345,pos,edges,labels,(0,6,12))
print('interface: 8 vertices, 9 edges; composition: 23 vertices, 54 edges; adjacency matches proof')
