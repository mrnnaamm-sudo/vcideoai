"""Mục 8 BẢN THỬ 2 (27/11 tối): xác suất ước tính = 30% mô hình + 20% mẫu đã co + 50% thị trường (Brier EL 27/11: thị trường 0,2435 tốt nhất; mẫu 0,268, mô hình 0,259 – thiên cao 6–7 điểm)."""
import json,sys
sys.path.insert(0,'.')
W=(0.3,0.2,0.5)
def tier2(o,ps,psa,pm,pf,mk):
    pe=W[0]*pm+W[1]*psa+W[2]*pf; ev=pe*o-1; evm=pm*o-1; gap=pe-pf; ea=psa-1/o; same=ps>pf
    if mk=='card': return 'C',ev
    if ev>=0.10 and evm>=0.10 and gap<=0.12 and same and ea>=0: return 'A',ev
    if ev>=0.05 and evm>0 and same and ea>=0: return 'B',ev
    if ev>=0.02 and ea>=0.03 and o>=1.65 and evm>0 and same: return 'C+',ev
    return 'C',ev
RANK={'A':0,'B':1,'C+':2,'C':3}
def worse(a,b): return a if RANK[a]>=RANK[b] else b
out=[]
R=json.load(open('d28/res3.json'))
for m in R:
    for i,mk in enumerate(['hc','tot','cor','h1','card']):
        x=m['ev'].get(mk)
        if not x: continue
        s=max(x['sides'],key=lambda q:(q['ev'] if q['ev'] is not None else -9))
        if not s['odds'] or not s['pf']: continue
        pm=(s['evm']+1)/s['odds']; t,ev=tier2(s['odds'],s['ps'],s['psa'],pm,s['pf'],mk)
        out.append(dict(tab=m['tab'],row=m['row']+i,mk=mk,odds=s['odds'],t2=t,ev2=ev,ev1=s['ev'],ps=s['ps'],pm=pm,pf=s['pf']))
for o in json.load(open('results/chc_28-11.json')):
    t,ev=tier2(o['odds'],o['ps'],o['psa'],o['pm'],o['pf'],'chc')
    rowmap={150:200,155:201,160:202,165:203,170:204}
    r=rowmap[o['row']] if o['tab']=='BL' else {150:200,155:201,160:202}[o['row']]
    out.append(dict(tab=o['tab'],row=r,mk='chc',odds=o['odds'],t2=t,ev2=ev,ev1=o['ev'],ps=o['ps'],pm=o['pm'],pf=o['pf']))
J=json.load(open('j1/res_28-11.json'))
for m in J['RES']:
    for i,mk in enumerate(['hc','tot','cor','h1','chc']):
        x=m['ev'].get(mk)
        s=max(x['sides'],key=lambda q:(q['ev'] if q['ev'] is not None else -9))
        if not s['odds'] or not s['pf']: continue
        pm=(s['evm']+1)/s['odds']; t,ev=tier2(s['odds'],s['ps'],s['psa'],pm,s['pf'],mk)
        out.append(dict(tab='J1',row=m['row']+i,mk=mk,odds=s['odds'],t2=t,ev2=ev,ev1=s['ev'],ps=s['ps'],pm=pm,pf=s['pf']))
json.dump(out,open('results/thu2_28-11.json','w'),ensure_ascii=False)
