"""J1 League – phân tích theo quy chuẩn chung (mục 1–29). python3 j1/run.py <ngày dd/mm> (chạy từ thư mục football/)"""
import json,sys,glob,os,datetime as dt,math
sys.path.insert(0,'.')
from model import evaluate,tier,tier_old
from gen3 import best,line_text,f2,pc,sg,lg
from corner_style import stats_of,_num,match_row,profile_venue,matchup,flags,summary,verdict_flags
import lineup as LU
DAY=sys.argv[1] if len(sys.argv)>1 else '28/11'
FM='j1/fm'
L=json.load(open(f'{FM}/lg.json'))
ALL=L['fixtures']['allMatches']
def vn(t): return dt.datetime.fromisoformat(t.replace('Z','+00:00'))+dt.timedelta(hours=7)
FX=[m for m in ALL if vn(m['status']['utcTime']).strftime('%d/%m')==DAY]
FX.sort(key=lambda m:(m['status']['utcTime'],m['id']))
SER={'28/11':46354,'29/11':46355}[DAY]
ROW0={'28/11':150,'29/11':180}[DAY]
# BXH -> Elo ước tính (không có ClubElo cho J1): 1500 + 110 × hiệu số/trận
tb=L['table'][0]['data']['table']['all']
ELO={}
for r in tb:
    gf,ga=map(int,r['scoresStr'].split('-')); ELO[str(r['id'])]=1500+110*(gf-ga)/max(1,r['played'])
RANK={str(r['id']):(r['idx'],r['pts'],r['played'],r['scoresStr']) for r in tb}
def recs(tid,before):
    fin=[m for m in ALL if m['status'].get('finished') and not m['status'].get('cancelled') and str(tid) in (str(m['home']['id']),str(m['away']['id'])) and m['status']['utcTime']<before]
    fin.sort(key=lambda m:m['status']['utcTime'],reverse=True)
    out=[]
    for m in fin[:10]:
        p=f"{FM}/m_{m['id']}.json"
        if not os.path.exists(p): continue
        d=json.load(open(p)); c=d['content']; S=stats_of(c); S1=stats_of(c,'FirstHalf')
        home=str(m['home']['id'])==str(tid); i,j=(0,1) if home else (1,0)
        hs,as_=[int(x) for x in d['header']['status']['scoreStr'].split(' - ')]
        gf,ga=(hs,as_) if home else (as_,hs)
        ht=None
        try:
            ev=c['matchFacts']['events']['events']
            gl=[e for e in ev if e.get('type')=='Goal' and (e.get('time') or 0)<=45 and not str(e.get('timeStr','')).startswith('45+') or (e.get('type')=='Goal' and str(e.get('timeStr','')).startswith('45+'))]
            hh=sum(1 for e in gl if e.get('isHome')); aa=sum(1 for e in gl if not e.get('isHome')); ht=(hh,aa) if home else (aa,hh)
        except Exception: pass
        cor=S.get('corners'); c1=S1.get('corners'); yc=S.get('yellow_cards'); rc=S.get('red_cards')
        xg=S.get('expected_goals')
        r=dict(mid=m['id'],date=vn(m['status']['utcTime']).strftime('%d/%m/%Y'),opp=(m['away'] if home else m['home'])['name'],home=home,gf=gf,ga=ga,ht=ht,
               cf=_num(cor[i]) if cor else None,ca=_num(cor[j]) if cor else None,cor=(_num(cor[0])+_num(cor[1])) if cor else None,
               h1=(_num(c1[0])+_num(c1[1])) if c1 else None,c1f=_num(c1[i]) if c1 else None,c1a=_num(c1[j]) if c1 else None,
               cards=((_num(yc[0]) or 0)+(_num(yc[1]) or 0)+2*((_num(rc[0]) if rc else 0) or 0)+2*((_num(rc[1]) if rc else 0) or 0)) if yc else None,
               yf=_num(yc[i]) if yc else None,ya=_num(yc[j]) if yc else None,
               poss=_num(S.get('BallPossesion',[None,None])[i]),xgf=_num(xg[i]) if xg else None,xga=_num(xg[j]) if xg else None)
        out.append(r)
    return out
def xgsum(R):
    v=[r for r in R if r['xgf'] is not None]
    return dict(n=len(v),xgf=sum(r['xgf'] for r in v)/len(v),xga=sum(r['xga'] for r in v)/len(v)) if v else None
# odds (Pinnacle, Odds API)
OD=json.load(open('j1/odds.json'))
NM={'Kyoto Sanga FC':'Kyoto Purple Sanga','Sanfrecce Hiroshima':'Hiroshima Sanfrecce FC','Shimizu S-Pulse':'Shimizu S Pulse','Fagiano Okayama FC':'Fagiano Okayama',
    'Yokohama F.Marinos':'Yokohama F Marinos','Mito Hollyhock':'Mito HollyHock','Machida Zelvia':'FC Machida Zelvia'}
def odds_for(hn,an):
    h=NM.get(hn,hn); a=NM.get(an,an)
    for e in OD:
        if e['home_team']==h and e['away_team']==a:
            bk={b['key']:b for b in e['bookmakers']}
            b=bk.get('pinnacle') or next(iter(bk.values()))
            mk={m['key']:m['outcomes'] for m in b['markets']}
            r={}
            if 'spreads' in mk:
                o={x['name']:x for x in mk['spreads']}; r['hc']=(o[h]['point'],o[h]['price'],o[a]['price'])
            if 'totals' in mk:
                o={x['name']:x for x in mk['totals']}; r['tot']=(o['Over']['point'],o['Over']['price'],o['Under']['price'])
            if 'h2h' in mk:
                o={x['name']:x['price'] for x in mk['h2h']}; r['1x2']=(o.get(h),o.get('Draw'),o.get(a))
            return r,b['key']
    return {},None
UO={}
if os.path.exists('j1/odds_user.json'): UO=json.load(open('j1/odds_user.json')).get(DAY,{})
def half(x): return math.floor(x)+0.5
RES=[];FORM=[];CS={}
for k,m in enumerate(FX):
    h,a=str(m['home']['id']),str(m['away']['id']); hn,an=m['home']['name'],m['away']['name']
    t=vn(m['status']['utcTime']); tm=t.strftime('%H:%M'); row=ROW0+5*k
    H,A=recs(h,m['status']['utcTime']),recs(a,m['status']['utcTime'])
    od,src=odds_for(hn,an)
    # mốc góc/H1/thẻ: theo kỳ vọng (chờ giá người dùng)
    kv0,_=evaluate(H,A,{},None,(ELO[h],ELO[a]),(None,None),(xgsum(H),xgsum(A)),1.0)
    o={'hc':od.get('hc',(None,None,None)),'tot':od.get('tot',(None,None,None)),'cor':(half(kv0['cor']),None,None),'h1':(half(kv0['h1']),None,None),'card':(half(kv0['card']),None,None)}
    for kk,v in UO.get(str(row),{}).items():
        if v: o[kk]=tuple(v)
    gap=abs(ELO[h]+65-ELO[a]); char=0.92 if gap>=250 else 1.0
    kv,ev=evaluate(H,A,o,None,(ELO[h],ELO[a]),(None,None),(xgsum(H),xgsum(A)),char)
    # mục 28
    files=lambda R:[f"{FM}/m_{r['mid']}.json" for r in R]
    RH=[x for x in (match_row(p,h) for p in files(H)) if x]; RA=[x for x in (match_row(p,a) for p in files(A)) if x]
    PH,PA=profile_venue(RH,True),profile_venue(RA,False); mm=matchup(PH,PA); F=flags(PH,PA,mm,hn,an)
    CS[row]=dict(txt=summary(hn,an,PH,PA,mm),F=F,m=mm)
    # mục 27
    nf=f"{FM}/n_{m['id']}.json"
    LR={tid:LU.team_report(files(R),tid,nf) for tid,R in ((h,H),(a,A))}
    RES.append(dict(row=row,time=tm,hn=hn,an=an,h=h,a=a,mid=m['id'],elo=(ELO[h],ELO[a]),gap=gap,kv=kv,ev=ev,src=src,od=od,n=(len(H),len(A)),lr=LR,H=H,A=A))
    for tid,nm,R in ((h,hn,H),(a,an,A)):
        for r in R:
            FORM.append([SER,f"{nm} • {hn} (Nhà) – {an} (Khách)",r['date'],r['opp'],'Nhà' if r['home'] else 'Khách','J1 League',
              'Thắng' if r['gf']>r['ga'] else ('Hòa' if r['gf']==r['ga'] else 'Thua'),
              f"{r['ht'][0]}–{r['ht'][1]}" if r['ht'] else '',f"{r['gf']}–{r['ga']}",
              f"{r['cf']:.0f}–{r['ca']:.0f}" if r['cf'] is not None else '',f"{r['cor']:.0f}" if r['cor'] is not None else '',
              f"{r['c1f']:.0f}–{r['c1a']:.0f}" if r['c1f'] is not None else '',f"{r['yf']:.0f}–{r['ya']:.0f}" if r['yf'] is not None else '',
              f"{r['cards']:.0f}" if r['cards'] is not None else '',f"{r['poss']:.0f}%" if r['poss'] is not None else '',
              (f"{r['xgf']:.2f}–{r['xga']:.2f}".replace('.',',')) if r['xgf'] is not None else '','FotMob'])
json.dump(dict(RES=RES,FORM=FORM,CS={str(k):v for k,v in CS.items()}),open(f'j1/res_{DAY.replace("/","-")}.json','w'),ensure_ascii=False,default=str)
for r in RES:
    print(r['row'],r['time'],r['hn'],'-',r['an'],'elo',round(r['elo'][0]),round(r['elo'][1]),'n',r['n'],'src',r['src'],{k:round(v,2) for k,v in r['kv'].items()})
    for mk,x in r['ev'].items():
        s=best(x); print('   ',mk,x['line'],s['side'],s['odds'],'ps',round(s['ps'],2),'pm',round(s['pm'],2),'ev',s['ev'] and round(s['ev'],3),'tier',tier(s,mk),tier_old(s,mk))
    print('   CS:',CS[r['row']]['txt'][:300])
