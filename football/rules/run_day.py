"""Chạy QUY CHUẨN CHUNG cho mọi tab một ngày (hiện: PL, LL, BL, J1 ngày 28/11).
python3 rules/run_day.py  → results/engine_28-11.json (mỗi kèo: tier, các bước kiểm, ghi chú, Ưu tiên/TOP)
Cùng nguồn, cùng thứ tự kiểm cho mọi giải: mẫu 10 trận (mục 1) • giá Pinnacle mới nhất cho chấp/tài xỉu bàn, giá người dùng cho góc/thẻ/chấp góc (mục 6)
• engine.grade (mục 5, 8, 14(1), 14(8), 14(8b), 15, 16, 20(d), 23, 27, 28, 29, 30) • engine.rank (mục 9)."""
import json,sys,os,glob,re,datetime as dt,unicodedata
import shutil as _sh,glob as _gl,sys as _sy; _sy.dont_write_bytecode=True
[_sh.rmtree(_p,ignore_errors=True) for _p in _gl.glob(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'**','__pycache__'),recursive=True)]   # không dùng mã biên dịch cũ: bộ máy chạy đúng mã nguồn hiện tại
sys.path.insert(0,'.')
from model import evaluate,chc_eval
from gen3 import best
from rules.engine import grade,rank,ORD
from rules import a1_sync
QC_VER=a1_sync.require(os.environ.get('A1_META'),os.environ.get('A1_NOTES'))   # mục 0: A1 lệch bộ máy → DỪNG PHÂN TÍCH
SP='/tmp/claude-0/-home-user-vcideoai/bc9353a1-6091-5ff6-82cc-896d2667346b/scratchpad/fmt'
DAYK='28-11'; KICK=dt.datetime(2026,11,28)
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def toks(s): return {w for w in re.split(r'[^a-z0-9]+',norm(s)) if len(w)>=4 and w not in('borussia','club','real','united','city')}
def pin(path,hn,an):
    for e in json.load(open(path)):
        if toks(hn)&toks(e['home_team']) and toks(an)&toks(e['away_team']):
            b=next((b for b in e['bookmakers'] if b['key']=='pinnacle'),None)
            if not b: return None
            mk={m['key']:m['outcomes'] for m in b['markets']}; r={}
            if 'spreads' in mk:
                o={x['name']:x for x in mk['spreads']}; r['hc']=(o[e['home_team']]['point'],o[e['home_team']]['price'],o[e['away_team']]['price'])
            if 'totals' in mk:
                o={x['name']:x for x in mk['totals']}; r['tot']=(o['Over']['point'],o['Over']['price'],o['Under']['price'])
            return r
    return None
def moved(o1,o2,mk,side):
    """Mục 14(1): Pinnacle dịch mốc ngược cửa mình ≥ ¼ hoặc giá cửa mình tăng ≥ 5% giữa 2 lần lấy giá."""
    if not o1 or not o2 or mk not in o1 or mk not in o2: return None
    (l1,a1,b1),(l2,a2,b2)=o1[mk],o2[mk]
    if mk=='hc':
        d=(l2-l1) if side==0 else (l1-l2)      # mốc đội nhà tăng = bất lợi cho cửa khách được chấp? → tính theo cửa chọn
        # cửa nhà: mốc nhà l (âm = chấp). Mốc nhà tăng (chấp ít hơn) = thị trường đánh giá nhà yếu đi → ngược cửa nhà.
        back=(l2-l1>=0.25) if side==0 else (l1-l2>=0.25)
    else:
        back=(l2-l1<=-0.25) if side==0 else (l2-l1>=0.25)   # Tài: mốc giảm là ngược; Xỉu: mốc tăng là ngược
    p1,p2=(a1,a2) if side==0 else (b1,b2)
    up=(l1==l2) and p2>=p1*1.05
    return dict(back=back or up,txt=f"Pinnacle {os.environ.get('EU_GIA_MOC','20:40 → 22:45')}: mốc {l1:g} → {l2:g}, giá cửa chọn {p1} → {p2}")
# ---------- mục 23: lịch thi đấu ----------
TC=json.load(open(f'rules/tinh_chat_{DAYK}.json')) if os.path.exists(f'rules/tinh_chat_{DAYK}.json') else {}
DERBY=json.load(open('rules/derby.json'))
def is_derby(a,b): return any((toks(a)&toks(x) and toks(b)&toks(y)) or (toks(a)&toks(y) and toks(b)&toks(x)) for x,y in DERBY)
def big_opp(name):
    """Đối thủ kế tiếp Elo ≥ 1800 (ClubElo, khớp tên theo từ khóa)."""
    t=toks(name)
    for k,v in ELO_ALL.items():
        if t & toks(k) and v[1]>=1800: return True
    return False
def sched(fix,kick,team_name=''):
    """Mục 23: (a) nghỉ < 3 ngày hoặc vừa đá cúp châu lục ≤ 4 ngày → mệt (ghi chú);
    (b) trận kế tiếp cách ≤ 4 NGÀY LỊCH là cúp châu lục (C1/C2/C3/ACL) hoặc gặp đội Elo ≥ 1800 (mọi giải) → NGUY CƠ XOAY TUA."""
    OK=('Premier League','LaLiga','Bundesliga','Serie A','Ligue 1','J. League','Champions League','Europa League','AFC Champions League')
    fix=[x for x in fix if any(x['tournament']['name']==o or x['tournament']['name'].startswith(o) for o in OK)]   # mục 1: chỉ VĐQG + C1/EL (+ACL)
    prev=[x for x in fix if x['status'].get('finished') and x['status']['utcTime']<kick]
    nxt=[x for x in fix if x['status']['utcTime']>kick and not x['status'].get('cancelled')]
    p=prev[-1] if prev else None; n=nxt[0] if nxt else None
    k=dt.datetime.fromisoformat(kick.replace('Z','+00:00'))
    f=lambda x:dt.datetime.fromisoformat(x['status']['utcTime'].replace('Z','+00:00'))
    rest=(k-f(p)).total_seconds()/86400 if p else None
    dn=(f(n).date()-k.date()).days if n else None
    cup=lambda x:any(w in x['tournament']['name'] for w in ('Champions League','Europa League','AFC Champions League'))   # C1/EL/ACL
    rot=bool(n and dn<=4 and (cup(n) or big_opp(n['opponent']['name']) or is_derby(team_name,n['opponent']['name'])))   # cúp quốc nội không xét
    return dict(rest=rest,prev=p and p['tournament']['name'],next=n and f"{n['tournament']['name']} gặp {n['opponent']['name']} sau {dn} ngày",
        tired=bool(p and (rest<3 or (cup(p) and rest<=4.5))),rot=rot)
def lin27(d):
    """Mục 27(c)(e): trung bình 2 nguồn (đội hình giả định + FotMob dự kiến); lệch nguồn (trùng ≤ 6/11 hoặc ngược chiều > 0,2) → ⚠ chưa hạ."""
    if not d: return None
    out={}
    for part in('att','def'):
        r=d['idx'][part]; a,b=r.get('rel'),r.get('rel_fm')
        v=(a+b)/2 if (a is not None and b is not None) else (a if a is not None else b)
        warn=(d.get('agree') is not None and d['agree']<=6) or (a is not None and b is not None and (a-1)*(b-1)<0 and abs(a-b)>0.2)
        out[part]=(v,warn)
    return out
BETS=[];MATCH={};SLOT={}
ELO_ALL=json.load(open('elo/elo_all.json'))
# ================= CHÂU ÂU (PL, LL, BL) =================
src=open('d28/an.py').read(); exec(src[src.index('M=['):src.index(']\nREFS')+1])
G=json.load(open('g/games.json')); sel=json.load(open('d28/teams/sel.json'))
E=json.load(open('elo/elo_all.json')); MP=json.load(open('elo/map.json')); XG=json.load(open('xg/xg28.json')); T28=json.load(open('xg/teams28.json'))
E['Malaga']=['Spain',1649,1]; MP['Málaga']='Malaga'
REFBL={('BL',150):('Felix Zwayer',4.15,3.76,20),('BL',155):('Florian Exner',4.67,4.61,20),('BL',160):('Sören Storks',4.75,3.77,20),('BL',165):('Bastian Dankert',3.11,3.77,20),('BL',170):('Timo Gerach',4.77,4.61,13)}
UO=json.load(open('d28/odds_user_27-11.json'))
CHU={('PL',150):(-0.5,2.05,1.77),('PL',155):(-1.5,1.71,2.12),('PL',160):(-1.5,1.90,1.92),
   ('BL',150):(-1.5,1.98,1.84),('BL',170):(-2.5,1.86,1.96),('BL',165):(3.5,2.06,1.76),('BL',160):(-1.5,2.07,1.75),('BL',155):(-0.5,1.88,1.94),
   ('LL',150):(-0.5,1.63,2.23),('LL',155):(-1.5,1.76,2.06),('LL',160):(1.5,1.74,2.08)}
CS=json.load(open('results/corner_style_28-11.json')); LUP=json.load(open('results/lineup_28-11.json'))
SPORT={'PL':'soccer_epl','LL':'soccer_spain_la_liga','BL':'soccer_germany_bundesliga'}
def recs(t):
    out=[]
    for d,gid,lg in sel[t]:
        g=G.get(gid)
        if not g: continue
        home=g['h']==t; i,j=(0,1) if home else (1,0)
        out.append(dict(gf=g['fs'][i],ga=g['fs'][j],home=home,cf=g['cor'][i] if g['cor'] else None,ca=g['cor'][j] if g['cor'] else None,
            cor=sum(g['cor']) if g['cor'] else None,h1=sum(g['c1']) if g['ncom']>=30 else None,cards=(sum(g['yc'])+2*sum(g['rc'])) if g['yc'] else None,lg=lg,date=d))
    return out
for tab,row,time,lab,h,a,hn,an,hc,tt,cr,cd,ref,fid in M:
    n=json.load(open(f'd28/fm/n_{fid}.json'))['general']
    fh,fa=str(n['homeTeam']['id']),str(n['awayTeam']['id']); fhn,fan=n['homeTeam']['name'],n['awayTeam']['name']
    kick=n['matchTimeUTCDate'] if 'matchTimeUTCDate' in n else n.get('matchTimeUTC')
    eh=E.get(MP.get(T28[fh])); ea=E.get(MP.get(T28[fa]))
    P1=pin(os.environ.get(f'EU_GIA_TRUOC_{tab}',f'd28/odds/{SPORT[tab]}.json'),fhn,fan); P2=pin(os.environ.get(f'EU_GIA_MOI_{tab}',f'd28/odds2/{SPORT[tab]}.json'),fhn,fan)   # lượt chốt: giá mới qua biến môi trường (QUY_TRINH – tự chuyển nguồn)
    od={'hc':(P2 or P1)['hc'],'tot':(P2 or P1)['tot']}
    U=UO.get(tab,{}).get(str(row))
    if U:
        for k,v in zip(('cor','h1','card'),U):
            if v: od[k]=tuple(v)
    r=ref or REFBL.get((tab,row)); rr=dict(name=r[0],ryc=r[1],ravg=r[2],rm=r[3]) if r else None
    gap=abs(eh[1]-ea[1]); char=0.92 if gap>=250 else 1.0
    H,A=recs(h),recs(a)
    kv0,_=evaluate(H,A,{},rr,(eh[1],ea[1]),(None,None),(XG.get(fh),XG.get(fa)),char)
    import math
    for k in ('cor','h1','card'):          # mục 6: chưa có giá → mốc theo kỳ vọng, để trống giá, vẫn phân tích đủ
        if k not in od: od[k]=(math.floor(kv0[k])+0.5,None,None)
    kv,ev=evaluate(H,A,od,rr,(eh[1],ea[1]),(None,None),(XG.get(fh),XG.get(fa)),char)
    if (tab,row) in CHU: ev['chc']=chc_eval(H,A,*CHU[(tab,row)],kv)
    cs=CS[f'{tab}{row}']; fl=cs['fl'] if isinstance(cs['fl'],list) else [str(cs['fl'])]
    def fx(tid):
        p=f'{SP}/t_{tid}.json'
        return json.load(open(p))['fixtures']['allFixtures']['fixtures'] if os.path.exists(p) else []
    sh,sa=sched(fx(fh),kick,fhn),sched(fx(fa),kick,fan)
    LH,LA=lin27(LUP.get(f'{tab}{row}_homeTeam')),lin27(LUP.get(f'{tab}{row}_awayTeam'))
    mid=f'{tab}{row}'; MATCH[mid]=[]; SLOT[mid]=time
    chrow={'PL':200,'LL':200,'BL':200}[tab]+sorted(r_ for (t_,r_) in CHU if t_==tab).index(row) if (tab,row) in CHU else None
    for i,mk in enumerate(['hc','tot','cor','h1','card','chc']):
        if mk not in ev: continue
        x=ev[mk]; s=best(x)
        rw=row+i if mk!='chc' else chrow
        BETS.append(dict(league=tab,tab=tab,row=rw,mid=mid,mk=mk,x=x,s=s,H=H,A=A,names=([hn,fhn],[an,fan]),flags=fl,kv=kv,
            price_src=(os.environ.get(f'EU_GIA_NHAN_{tab}','Pinnacle 27/11 22:45') if mk in('hc','tot') else 'người dùng 27/11') if s['odds'] else None,
            move=moved(P1,P2,mk,s['side']) if mk in('hc','tot') else None,elo=(eh[1],ea[1]),sched=(sh,sa),lineup=(LH,LA),
            card=dict(ref=rr,kv_card=kv.get('card'),elo=(eh[1],ea[1]),big=(eh[1]>=1800 and ea[1]>=1800),pl=(tab=='PL')),
            time=time,lab=lab,hn=hn,an=an,od=od,tinh_chat=dict(TC.get(mid,{}),derby=TC.get(mid,{}).get('derby') or is_derby(fhn,fan))))
# ================= J1 =================
J=json.load(open(f'j1/res_{DAYK}.json'))
sys.argv=['x','28/11']
import lineup as LU
AB=json.load(open(f'j1/abs_{DAYK}.json')); FULL={'Kato':'Ren Kato'}
def lineup_idx(R,tid,names):
    files=[f"j1/fm/m_{x['mid']}.json" for x in R]
    P,XIs=LU.player_table(files,tid)
    if not P: return None
    sh=LU.shape(P,XIs); bestxi=LU.pick_xi(P,{},sh); av={}
    for s_ in names:
        for p in P:
            nm=P[p]['name']
            if (FULL.get(s_,'')==nm) or (s_ not in FULL and nm.split()[-1].lower()==s_.lower()): av[p]=0.0
    mine=LU.pick_xi(P,av,sh); res={}
    for part in ('att','def'):
        b=LU.strength(P,bestxi,part) or 1; sm=sum(LU.strength(P,x_,part)/b for x_ in XIs)/max(1,len(XIs))
        res[part]=(LU.strength(P,mine,part)/b/sm if sm else 1, False)
    return res
SH={'Kyoto Sanga FC':'Kyoto','Cerezo Osaka':'Cerezo','Shimizu S-Pulse':'Shimizu','Urawa Red Diamonds':'Urawa','Kashima Antlers':'Kashima',
    'Fagiano Okayama FC':'Okayama','Vissel Kobe':'Kobe','JEF United Chiba':'Chiba','Kashiwa Reysol':'Kashiwa','Sanfrecce Hiroshima':'Hiroshima'}
OLDJ=json.load(open('j1/odds.json'))
for r in J['RES']:
    row=r['row']; mid=f'J1{row}'; MATCH[mid]=[]; SLOT[mid]=r['time']
    ab=AB[str(row)]; names=ab['susp']+ab['out']
    LH,LA=lineup_idx(r['H'],r['h'],names),lineup_idx(r['A'],r['a'],names)
    lg=json.load(open('j1/fm/lg.json'))['fixtures']['allMatches']; m=next(z for z in lg if z['id']==r['mid']); kick=m['status']['utcTime']
    def fx(tid):
        p=f'j1/fm/t_{tid}.json'
        return json.load(open(p))['fixtures']['allFixtures']['fixtures'] if os.path.exists(p) else []
    sh,sa=sched(fx(r['h']),kick,r['hn']),sched(fx(r['a']),kick,r['an'])
    NM={'Kyoto Sanga FC':'Kyoto Purple Sanga','Sanfrecce Hiroshima':'Hiroshima Sanfrecce FC','Shimizu S-Pulse':'Shimizu S Pulse','Fagiano Okayama FC':'Fagiano Okayama'}
    P1=pin('j1/odds.json',NM.get(r['hn'],r['hn']),NM.get(r['an'],r['an'])); P2=pin(os.environ.get('J1_ODDS_MOI','d28/odds2/soccer_japan_j_league.json'),NM.get(r['hn'],r['hn']),NM.get(r['an'],r['an']))
    fl=J['CS'][str(row)]['F']
    for i,mk in enumerate(['hc','tot','cor','h1','chc']):
        x=r['ev'][mk]; s=best(x)
        BETS.append(dict(league='J1',tab='J1',row=row+i,mid=mid,mk=mk,x=x,s=s,H=r['H'],A=r['A'],names=([SH[r['hn']],r['hn']],[SH[r['an']],r['an']]),flags=fl,kv=r['kv'],
            price_src=(os.environ.get('J1_GIA_NHAN','Pinnacle 27/11 22:45') if mk in('hc','tot') else 'người dùng 27/11') if s['odds'] else None,
            move=moved(P1,P2,mk,s['side']) if mk in('hc','tot') else None,elo=tuple(r['elo']),sched=(sh,sa),lineup=(LH,LA),card=None,
            time=r['time'],lab=f"{r['hn']} (Nhà) – {r['an']} (Khách)",hn=SH[r['hn']],an=SH[r['an']],tinh_chat=dict(TC.get(mid,{}),derby=TC.get(mid,{}).get('derby') or is_derby(r['hn'],r['an']))))
# ================= CHẤM =================
from rules import registry as REGI
for b in BETS:
    if not REGI.official(b['mk']):      # mục 0(h): kèo mới chưa tích hợp đủ → chỉ lưu giá, không chấm/xếp/báo
        b.update(t='—',steps=[('0(h)','chờ tích hợp',None)],notes=[]); MATCH[b['mid']].append(b); continue
    g=grade(b); b.update(g); MATCH[b['mid']].append(b)
rank(MATCH,SLOT)
out=[]
for b in BETS:
    s=b['s']
    out.append(dict(tab=b['tab'],row=b['row'],mid=b['mid'],mk=b['mk'],time=b['time'],lab=b['lab'],hn=b['hn'],an=b['an'],side=s['side'],line=b['x']['line'],
        odds=s['odds'],ps=s['ps'],psa=s['psa'],pm=s['pm'],pf=s['pf'],ev=s['ev'],evm=s['evm'],t=b['t'],steps=b['steps'],notes=b['notes'],pri=b.get('pri'),top=b.get('top'),
        dp=b.get('dp'),abn=b.get('abn'),nodata=b.get('nodata'),card_pri=b.get('card_pri'),kv={k:v for k,v in b['kv'].items() if isinstance(v,(int,float))},
        sides=[dict(side=z['side'],odds=z['odds']) for z in b['x']['sides']],price_src=b['price_src'],elo=b['elo'],
        H=[{k:q.get(k) for k in('gf','ga','cf','ca','cor','h1','cards','home')} for q in b['H']],A=[{k:q.get(k) for k in('gf','ga','cf','ca','cor','h1','cards','home')} for q in b['A']]))
json.dump(out,open(f'results/engine_{DAYK}.json','w'),ensure_ascii=False,default=str)
for o in out:
    if o['t']!='C' or o.get('pri') or o.get('top'):
        print(o['tab'],o['row'],o['mk'],o['side'],o['line'],o['odds'],o['t'],o.get('pri') or '',o.get('top') or '',' | '.join(f"{m}:{d}" for m,k,d in o['steps'] if d))
# ================= SINH NỘI DUNG SHEET (một khuôn cho mọi tab) =================
from gen3 import line_text,f2,pc,sg,lg
from corner_style import verdict_flags
SER=46354
NM={'hc':'Chấp bàn FT','tot':'Tài/Xỉu bàn FT','cor':'Góc FT','h1':'Góc H1','card':'Thẻ FT (vàng + 2×đỏ)','chc':'Chấp góc FT'}
SRC={'J1':'FotMob 10 trận gần nhất (J1 + ACL Elite) • '+os.environ.get('J1_GIA_NGUON','Pinnacle 27/11 22:45 (Odds API)')+' • giá góc/chấp góc: người dùng 27/11 • Elo ước tính từ BXH • Football LAB',
     'EU':'ESPN/FotMob 10 trận gần nhất (VĐQG + cúp châu Âu) • '+os.environ.get('EU_GIA_NGUON','Pinnacle 27/11 22:45 (Odds API)')+' • giá góc/thẻ/chấp góc: người dùng 27/11 • ClubElo • FotMob (đội hình, lối đá, trọng tài)'}
def full_names(lab): a,b=lab.split(' – '); return a.replace(' (Nhà)',''),b.replace(' (Khách)','')
def chk(steps): return ' • Đã kiểm quy chuẩn: '+'; '.join(f"{m} {'→ '+d if d else ('= '+k.replace('tier ','') if m=='8' else '✓')}" for m,k,d in steps)
def vn_num(t): return re.sub(r'(\d)\.(\d)',r'\1,\2',t) if isinstance(t,str) else t
def cua_chc(b):
    x,s=b['x'],b['s']; l=x['line'] if s['side']==0 else -x['line']; tn=b['hn'] if s['side']==0 else b['an']
    return f"{tn} {('+' if l>0 else '')+lg(l) if l!=0 else '0'} góc FT"
def base_of(b):
    x,s,kv=b['x'],b['s'],b['kv']
    if b['mk']=='chc':
        c=cua_chc(b); kvs=f"kỳ vọng góc {lg(round(kv['ch'],1))}–{lg(round(kv['ca_'],1))}"
        return c,(f"{c} @{f2(s['odds'])} • mẫu {pc(s['ps'])} / hòa vốn {pc(1/s['odds'])} • EV {sg(s['ev'])} (mô hình {pc((s['evm']+1)/s['odds'])}) • {kvs}" if s['odds'] else f"{c} (chờ giá) • mẫu {pc(s['ps'])} • mô hình {pc(s['pm'])} • {kvs}")
    return line_text(b['mk'],x,s,b['hn'],b['an'],kv)
def reason_c(b):
    s=b['s']
    ha=[f"hạ theo mục {m}" for m,k,d in b.get('steps',[]) if d in('C+','C') and m not in('15',)]
    if ha and s['odds'] is not None and (s['ev'] or 0)>=0.02: return '; '.join(dict.fromkeys(ha))
    if s['odds'] is None: return 'chờ giá (mục 6: không tự đoán giá)'
    if s['evm'] is not None and s['evm']<=0: return 'mô hình ngược chiều'
    if s['pf'] and s['ps']<=s['pf']: return 'mẫu không nghiêng hơn thị trường'
    return 'không đủ lợi thế (EV < 2–5% sau khi co mẫu về thị trường)'
def au_of(b):
    mk,x,H,A=b['mk'],b['x'],b['H'],b['A']; h_,a_=b['hn'],b['an']
    if mk=='chc':
        f=lambda R:', '.join(('+' if v>0 else '')+str(int(v)) for v in [q['cf']-q['ca'] for q in R if q.get('cf') is not None])
        return f"Hiệu số góc 10 trận – {h_}: {f(H)}; {a_}: {f(A)}."
    if mk=='hc':
        f=lambda R:', '.join(('+' if v>0 else '')+str(v) for v in [q['gf']-q['ga'] for q in R])
        return f"Hiệu số 10 trận – {h_}: {f(H)}; {a_}: {f(A)}."
    key={'tot':None,'cor':'cor','h1':'h1','card':'cards'}[mk]; L=x['line']
    def vals(R): return [(q['gf']+q['ga']) if mk=='tot' else q[key] for q in R if (mk=='tot' or q.get(key) is not None)]
    def d(nm,v): return f"{nm} TB {lg(round(sum(v)/len(v),1))}, Tài {sum(1 for z in v if z>L)}/{len(v)}" if v else f"{nm} không có số liệu"
    return f"Mẫu 10 trận (mốc {lg(L)}): {d(h_,vals(H))}; {d(a_,vals(A))}."
def av_of(b):
    s=b['s']; src='giá người dùng' if b['mk'] in('cor','h1','card','chc') else 'Pinnacle'
    t=f"Gộp {pc(s['ps'])} (mẫu) / mô hình {pc(s['pm'] if not s['odds'] else (s['evm']+1)/s['odds'])}"+(f" so với hòa vốn {pc(1/s['odds'])}; thị trường ({src}, bỏ biên) {pc(s['pf'])}" if s['odds'] and s['pf'] else '')+'.'
    if b['mk']=='hc': t+=f" Elo {round(b['elo'][0])}–{round(b['elo'][1])} (mục 25, chênh {round(b['elo'][0]+65-b['elo'][1]):+d} tính sân nhà)."
    sh,sa=b['sched']
    for S_,nm in ((sh,b['hn']),(sa,b['an'])):
        if S_ and S_['next']: t+=f" Lịch {nm}: nghỉ {S_['rest']:.1f} ngày sau {S_['prev']}; kế tiếp {S_['next']}." if S_['rest'] is not None else ''
    if b['mk']=='card' and b.get('card') and b['card'].get('ref'):
        r=b['card']['ref']; t+=f" Trọng tài {r['name']}: {lg(r['ryc'])} vàng/trận (TB giải {lg(r['ravg'])}, {r['rm']} trận)."
    return t
PAY={}
for mid,bs in MATCH.items():
    hasB=any(o['t'] in('A','B') and o['mk']!='card' and not o.get('abn') for o in bs); hasCp=any(o['t']=='C+' and o['mk']!='card' for o in bs)
    for b in bs:
        s=b['s']; c,base=base_of(b); t=b['t']; notes=list(b['notes'])
        pre=[]
        if b.get('nodata') is not None: pre.append(notes.pop(0))
        if b.get('abn'): pre.append(next((n for n in notes if n.startswith('⚠')),'⚠ KÈO BẤT THƯỜNG')); notes=[n for n in notes if not n.startswith('⚠')]
        if b['mk']=='hc' and not hasB: pre.append('Trận không có tier B, chỉ có C+ ½R' if hasCp else 'KHÔNG VÀO (trận không có kèo tier B)')
        if t=='—':
            core=f"CHỜ TÍCH HỢP (mục 0h) • {c}"+(f" @{f2(s['odds'])}" if s['odds'] else '')+" • loại kèo mới chưa tích hợp đủ A1 + bộ máy + bảng đối chiếu + khuôn sheet → chưa chấm, không Ưu tiên/TOP, không báo, không tính RR"
            pre=[]
        elif b['mk']=='card':
            if b.get('card_pri'): pre.append('Thẻ ưu tiên (mục 29, RR riêng)')
            core=f"{base} • kèo thẻ RR riêng (mục 29) • tier {t}"+('' if t in('A','B') else (' • ½R' if t=='C+' else ' • không vào'))
        elif t in('A','B'):
            if b.get('pri'): pre.append(f"Ưu tiên {b['pri']}")
            if b.get('top'): pre.append(b['top'])
            core=base+(' • tier B dự phòng (trận đã đủ 2 ưu tiên)' if b.get('dp') else '')
        elif t=='C+': pre.append('C+ • ½R'); core=base+f" • mẫu (co về thị trường) {pc(s['psa'])}, giá ≥ 1,65 (mục 18b)"
        else: core=base+' • '+reason_c(b)+' • C • không vào'
        ay=' • '.join(pre+[core]+notes)+chk(b['steps'])+(f" • [Thử mục 8 (a)(b); tier cách cũ: {b['t_old']}]" if b.get('t_old') and b['mk']!='card' else '')+'.'
        # danh sách kèo
        fh,fa=full_names(b['lab']); x=b['x']
        c1,c2=(fh,fa) if b['mk'] in('hc','chc') else ('Tài','Xỉu')
        o1,o2=x['sides'][0]['odds'],x['sides'][1]['odds']
        odl=[SER,b['time'],f"{b['time']} • {b['lab']}",NM[b['mk']],lg(x['line']),c1,o1 or '',c2,o2 or '']
        # cột BL (mục 28/30) cho góc FT, góc H1, chấp góc
        bl=None
        if b['mk'] in('cor','h1'):
            v,why=verdict_flags('Tài' if s['side']==0 else 'Xỉu',b['flags'] or [])
            bl=f" • Kèo đang chọn: {c}{(' @'+f2(s['odds'])) if s['odds'] else ''} (tier {t}) → lối đá {v.upper() if v=='phản bác' else v}"+(': điểm cộng (không nâng tier)' if v=='ủng hộ' else '')
        elif b['mk']=='chc':
            st=next((d for m,k,d in b['steps'] if m=='30(c)'),None); kq=next((k for m,k,d in b['steps'] if m=='30(c)'),'')
            bl=f"Chấp góc (mục 30): kỳ vọng mô hình {lg(round(b['kv']['ch'],1))}–{lg(round(b['kv']['ca_'],1))} • kèo đang chọn {c} (tier {t}) → cờ lối đá: {kq}"
        mau=sorted({q.get('lg') or ('ACL' if q.get('acl') else 'J1 League') for q in b['H']+b['A']})
        PAY.setdefault(b['tab'],{})[b['row']]=dict(mau=mau,price_src=b.get('price_src'),mk=b['mk'],asy=[c,s['odds'] if s['odds'] else '',vn_num(au_of(b)),vn_num(av_of(b)),t,SRC['J1' if b['tab']=='J1' else 'EU'],vn_num(ay)],odl=odl,bl=vn_num(bl),
            pri=b.get('pri'),top=b.get('top'),t=t,mid=mid,steps=b['steps'],abn=b.get('abn'))
json.dump(PAY,open(f'results/sheet_engine_{DAYK}.json','w'),ensure_ascii=False,default=str)
print('payload',{k:len(v) for k,v in PAY.items()})
# cột BL đầy đủ (mục 28 / 29 / 30) theo cùng khuôn
CSJ=J['CS']
for tab,rows in PAY.items():
    for r,d in rows.items():
        b=next(z for z in BETS if z['tab']==tab and z['row']==r)
        cs=(CSJ[str(int(b['mid'][2:]))] if tab=='J1' else CS[b['mid']])
        m=cs.get('m') or {}
        if d['mk']=='cor': d['bl']=vn_num(cs['txt'])+d['bl']
        elif d['mk']=='h1': d['bl']=(f"Góc H1 theo lối đá: {lg(round(m['h1'],1))} (FT {lg(round(m['tot'],1))})" if m else 'Góc H1 theo lối đá: thiếu số liệu')+d['bl']
        elif d['mk']=='card': d['bl']='KÈO THẺ (mục 29, RR riêng): '+vn_num(next((k for mm,k,dd in b['steps'] if mm in('29','29(g)')),''))
        elif d['mk']=='chc': pass
        else: d['bl']=''
json.dump(PAY,open(f'results/sheet_engine_{DAYK}.json','w'),ensure_ascii=False,default=str)
