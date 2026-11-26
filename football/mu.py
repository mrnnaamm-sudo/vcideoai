import json
def sc(s):
    a,b=s.replace('–','-').split('-'); return int(a),int(b)
def stats(rows,off):
    # off: index shift (EL=0, d28=2)
    g=lambda r,i:r[i+off]
    v=[r for r in rows if g(r,9)!='' ]
    n=len(v)
    gf=[sc(g(r,6))[0] for r in rows]; ga=[sc(g(r,6))[1] for r in rows]
    d=dict(gf=sum(gf)/len(rows),ga=sum(ga)/len(rows))
    def av(i):
        x=[g(r,i) for r in rows if isinstance(g(r,i),(int,float))]
        return sum(x)/len(x) if x else None
    d.update(cf=av(10),ca=av(11),h1=av(7),cards=av(17))
    return d
def mu(A,B,kind,ref=1.0):
    if kind=='tot': return (A['gf']+B['ga'])/2+(B['gf']+A['ga'])/2
    if kind=='cor': return (A['cf']+B['ca'])/2+(B['cf']+A['ca'])/2
    if kind=='h1': return (A['h1']+B['h1'])/2
    if kind=='card': return (A['cards']+B['cards'])/2*ref  # cards = match total incl. opponent; avg of two
