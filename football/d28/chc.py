"""Mục 30 – chấp góc FT cho các trận châu Âu 28/11 (giá người dùng 27/11)."""
import json,sys,re
sys.path.insert(0,'.')
from model import *
from gen3 import f2,pc,sg,lg
src=open('d28/an.py').read(); exec(src[src.index('M=['):src.index(']\nREFS')+1])
G=json.load(open('g/games.json')); sel=json.load(open('d28/teams/sel.json'))
CS=json.load(open('results/corner_style_28-11.json'))
def recs(t):
    out=[]
    for d,gid,lg_ in sel[t]:
        g=G.get(gid)
        if not g: continue
        home=g['h']==t; i,j=(0,1) if home else (1,0)
        out.append(dict(gf=g['fs'][i],ga=g['fs'][j],home=home,cf=g['cor'][i] if g['cor'] else None,ca=g['cor'][j] if g['cor'] else None))
    return out
# mốc theo đội nhà, giá nhà, giá khách
U={('PL',150):(-0.5,2.05,1.77),('PL',155):(-1.5,1.71,2.12),('PL',160):(-1.5,1.90,1.92),
   ('BL',150):(-1.5,1.98,1.84),('BL',170):(-2.5,1.86,1.96),('BL',165):(3.5,2.06,1.76),('BL',160):(-1.5,2.07,1.75),('BL',155):(-0.5,1.88,1.94),
   ('LL',150):(-0.5,1.63,2.23),('LL',155):(-1.5,1.76,2.06),('LL',160):(1.5,1.74,2.08)}
OUT=[]
for tab,row,time,lab,h,a,hn,an,*_ in M:
    if (tab,row) not in U: continue
    H,A=recs(h),recs(a); kv={}
    x=chc_eval(H,A,*U[(tab,row)],kv)
    s=max(x['sides'],key=lambda q:q['ev'])
    t=tier(s,'chc'); to=tier_old(s,'chc')
    L=x['line'] if s['side']==0 else -x['line']; tn=hn if s['side']==0 else an; opp=an if s['side']==0 else hn
    cs=CS[f'{tab}{row}']; fl=' | '.join(cs['fl']) if isinstance(cs['fl'],list) else str(cs['fl'])
    # mục 30(c): cờ NHIỀU GÓC CHO / DỒN ÉP của đối thủ phản bác cửa mình
    contra=[f for f in (cs['fl'] if isinstance(cs['fl'],list) else [str(cs['fl'])]) if (('NHIỀU GÓC CHO' in f or 'DỒN ÉP' in f) and opp.split()[0] in f)]
    sup=[f for f in (cs['fl'] if isinstance(cs['fl'],list) else [str(cs['fl'])]) if (('NHIỀU GÓC CHO' in f or 'DỒN ÉP' in f) and tn.split()[0] in f)]
    t0=t
    if contra and t in('A','B'): t={'A':'B','B':'C+'}[t]
    mm=cs['m']
    OUT.append(dict(tab=tab,row=row,time=time,lab=lab,hn=hn,an=an,line=x['line'],oh=U[(tab,row)][1],oa=U[(tab,row)][2],
        side=s['side'],cua=f"{tn} {('+' if L>0 else '')+lg(L)} góc FT",odds=s['odds'],ps=s['ps'],psa=s['psa'],pm=(s['evm']+1)/s['odds'],pf=s['pf'],ev=s['ev'],evm=s['evm'],
        t=t,t0=t0,to=to,kh=kv['ch'],ka=kv['ca_'],eh=mm['eh'] if mm else None,ea=mm['ea'] if mm else None,contra=contra,sup=sup,
        mh=[int(q['cf']-q['ca']) for q in H if q['cf'] is not None],ma=[int(q['cf']-q['ca']) for q in A if q['cf'] is not None]))
    print(tab,row,time,hn,'-',an,'|',OUT[-1]['cua'],'@',s['odds'],'ps',round(s['ps'],2),'pm',round(OUT[-1]['pm'],2),'pf',round(s['pf'],2),'EV',round(s['ev'],3),'evm',round(s['evm'],3),'tier',t,'(gốc',t0,'cũ',to,')','kv',round(kv['ch'],1),round(kv['ca_'],1),'lối đá',mm and (round(mm['eh'],1),round(mm['ea'],1)),'contra',contra,'sup',sup)
json.dump(OUT,open('results/chc_28-11.json','w'),ensure_ascii=False)
