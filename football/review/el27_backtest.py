"""Rà soát RR EL 27/11 (trừ thẻ): kèo đã chốt vs chấm lại bằng mục 8 bản thử; tìm nguyên nhân RR thấp."""
import json,sys
sys.path.insert(0,'.'); sys.path.insert(0,'review')
from model import tier,tier_old
from gen3 import best
from the_data import M
R=json.load(open('el/res3.json')); fx=json.load(open('el/fm/fx.json')); K=json.load(open('results/el_27-11_ketqua.json'))
def val(mk,line,side,k):
    if mk=='hc':
        d=k['fs'][0]-k['fs'][1]; v=d+line; return v if side==0 else -v
    tot={'tot':sum(k['fs']),'cor':sum(k['cor']),'h1':sum(k['c1'])}[mk]
    return tot-line if side==0 else line-tot
def res(mk,line,side,k,odds):
    def one(l):
        v=val(mk,l,side,k); return (odds-1) if v>0 else 0 if v==0 else -1
    if abs(line*4-round(line*4))<1e-9 and round(line*4)%2!=0:
        return (one(line-0.25)+one(line+0.25))/2
    return one(line)
rows=[]
for fi,(m,f) in enumerate(zip(R,fx)):
    k=K[f['id']]; slot='00:45' if f['t'][11:13]=='17' else '03:00'
    orig=[x for x in M if x[0]=='EL'][fi][4]
    for i,mk in enumerate(['hc','tot','cor','h1']):
        x=m['ev'][mk]; o=orig[i]
        # side đã chốt: tìm side có odds khớp
        so=min(x['sides'],key=lambda s:abs((s['odds'] or 0)-o['odds']))
        sb=best(x)
        rows.append(dict(m=f"{m['hn']}–{m['an']}",slot=slot,mk=mk,elo=(m['elo'][0][1] if m['elo'][0] else None,m['elo'][1][1] if m['elo'][1] else None),
            o_keo=o['keo'],o_t=o['tier'],o_pr=o['pr'] and o['tier'] in('A','B'),o_top=o['top'],o_pl={'W':o['odds']-1,'HW':(o['odds']-1)/2,'H':0,'HL':-0.5,'L':-1}[o['res']],
            so=so,sb=sb,t_new=tier(sb,mk),t_old=tier_old(sb,mk),line=x['line'],pl_b=res(mk,x['line'],sb['side'],k,sb['odds']),
            pl_o=res(mk,x['line'],so['side'],k,so['odds'])))
json.dump([{k:v for k,v in r.items() if k not in('so','sb')}|{'ps':r['so']['ps'],'pm':(r['so']['evm']+1)/r['so']['odds'],'pf':r['so']['pf'],'psa':r['so']['psa'],'ev':r['so']['ev'],'evm':r['so']['evm']} for r in rows],open('results/el27_backtest.json','w'),ensure_ascii=False,indent=0)
def agg(lbl,S,key):
    n=len(S); s=sum(r[key] for r in S); w=sum(1 for r in S if r[key]>0); l=sum(1 for r in S if r[key]<0)
    print(f"  {lbl:42} {w:>2}T {l:>2}B {n-w-l}H n={n:<3} RR {s:+.2f}  ROI {100*s/n if n else 0:+.1f}%")
print('== KÈO ĐÃ CHỐT (trừ thẻ)')
agg('ưu tiên B+',[r for r in rows if r['o_pr']],'o_pl'); agg('TOP',[r for r in rows if r['o_top']],'o_pl')
for t in 'ABC': agg('tier '+t,[r for r in rows if r['o_t']==t],'o_pl')
agg('toàn bộ',rows,'o_pl')
print('== ưu tiên B+ đã chốt – từng kèo')
for r in rows:
    if r['o_pr']:
        s=r['so']; print(f"  {r['m'][:30]:30} {r['o_keo']:22} {r['o_t']} RR {r['o_pl']:+.2f} | mẫu {s['ps']:.0%} co {s['psa']:.0%} mô hình {(s['evm']+1)/s['odds']:.0%} thị trường {s['pf'] if s['pf'] is None else round(s['pf']*100)}% | EV thử {s['ev']:+.1%} → tier thử {tier(s,r['mk'])} | Elo {r['elo']}")
print('== CHẤM LẠI BẰNG BẢN THỬ (cửa EV cao nhất)')
for t in 'AB': agg('tier thử '+t,[r for r in rows if r['t_new']==t],'pl_b')
agg('tier thử C+',[r for r in rows if r['t_new']=='C+'],'pl_b')
agg('tier thử A+B',[r for r in rows if r['t_new'] in('A','B')],'pl_b')
print('== theo thị trường – kèo đã chốt / tier thử A+B')
for mk in ['hc','tot','cor','h1']:
    agg(mk+' chốt',[r for r in rows if r['mk']==mk],'o_pl'); agg(mk+' thử A+B',[r for r in rows if r['mk']==mk and r['t_new'] in('A','B')],'pl_b')
print('== kèo chấp cửa dưới (nhận chấp) vs cửa trên – đã chốt')
und=lambda r:r['mk']=='hc' and '+' in r['o_keo']
agg('nhận chấp',[r for r in rows if und(r)],'o_pl'); agg('chấp/đồng banh',[r for r in rows if r['mk']=='hc' and not und(r)],'o_pl')
agg('nhận chấp, đội trên ≥150 Elo',[r for r in rows if und(r) and r['elo'][0] and r['elo'][1] and abs(r['elo'][0]+65-r['elo'][1])>=150],'o_pl')
print('== hiệu chuẩn kèo đã chốt (trừ thẻ): mẫu / co / mô hình / thị trường vs thực tế')
for g,S in (('A/B',[r for r in rows if r['o_t'] in('A','B')]),('C',[r for r in rows if r['o_t']=='C'])):
    win=[1 if r['o_pl']>0 else 0.5 if r['o_pl']==0 else 0 for r in S]
    ps=[r['so']['ps'] for r in S]; pa=[r['so']['psa'] for r in S]; pm=[(r['so']['evm']+1)/r['so']['odds'] for r in S]; pf=[r['so']['pf'] for r in S if r['so']['pf']]
    av=lambda a:sum(a)/len(a)
    br=lambda p:sum((x-y)**2 for x,y in zip(p,win))/len(win)
    print(f"  {g}: n={len(S)} thực tế {av(win):.0%} | mẫu {av(ps):.0%} (Brier {br(ps):.3f}) | co {av(pa):.0%} ({br(pa):.3f}) | mô hình {av(pm):.0%} ({br(pm):.3f}) | thị trường {av(pf):.0%} ({br([r['so']['pf'] for r in S]):.3f})")
