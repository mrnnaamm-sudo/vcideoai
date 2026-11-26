import json,sys,re
sys.path.insert(0,'.')
from model import *
src=open('d28/an.py').read()
Mtxt=src[src.index('M=['):src.index(']\nREFS')+1]
exec(Mtxt)
G=json.load(open('g/games.json')); sel=json.load(open('d28/teams/sel.json'))
OUT=json.load(open('d28/out.json'))
E=json.load(open('elo/elo_all.json')); MP=json.load(open('elo/map.json')); XG=json.load(open('xg/xg28.json')); T28=json.load(open('xg/teams28.json'))
E['Malaga']=['Spain',1649,1]; MP['Málaga']='Malaga'
REFBL={('BL',150):('Felix Zwayer',4.15,3.76,20),('BL',155):('Florian Exner',4.67,4.61,20),('BL',160):('Sören Storks',4.75,3.77,20),('BL',165):('Bastian Dankert',3.11,3.77,20),('BL',170):('Timo Gerach',4.77,4.61,13)}
def recs(t):
    out=[]
    for d,gid,lg in sel[t]:
        g=G.get(gid)
        if not g: continue
        home=g['h']==t; i,j=(0,1) if home else (1,0)
        out.append(dict(gf=g['fs'][i],ga=g['fs'][j],home=home,cf=g['cor'][i] if g['cor'] else None,ca=g['cor'][j] if g['cor'] else None,
            cor=sum(g['cor']) if g['cor'] else None,h1=sum(g['c1']) if g['ncom']>=30 else None,cards=(sum(g['yc'])+2*sum(g['rc'])) if g['yc'] else None))
    return out
RES=[]
for (tab,row,time,lab,h,a,hn,an,hc,tt,cr,cd,ref,fid),o in zip(M,OUT):
    assert o['row']==row and o['tab']==tab
    n=json.load(open(f'd28/fm/n_{fid}.json'))['general']
    fh,fa=str(n['homeTeam']['id']),str(n['awayTeam']['id'])
    eh=E.get(MP.get(T28[fh])); ea=E.get(MP.get(T28[fa]))
    od={}
    for x in o['res']:
        L=x['line']; od[x['k']]=(L[0],L[2],L[4])
    od.update({('PL',155):{'card':(3.5,1.93,1.84)},('PL',160):{'card':(4.5,2.3,1.68)}}.get((tab,row),{}))
    r=ref or REFBL.get((tab,row))
    rr=dict(name=r[0],ryc=r[1],ravg=r[2],rm=r[3]) if r else None
    gap=abs(eh[1]-ea[1]); char=0.92 if gap>=250 else 1.0
    H,A=recs(h),recs(a)
    kv,ev=evaluate(H,A,od,rr,(eh[1],ea[1]),(None,None),(XG.get(fh),XG.get(fa)),char)
    RES.append(dict(tab=tab,row=row,time=time,lab=lab,hn=hn,an=an,elo=(eh,ea),kv=kv,ev=ev,ref=rr,n=(len(H),len(A))))
json.dump(RES,open('d28/res3.json','w'),ensure_ascii=False)
