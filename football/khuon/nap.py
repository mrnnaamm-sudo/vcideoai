"""NẠP DỮ LIỆU CHUNG cho mọi giải, mọi ngày (mục 1, 2, 19–25, 27, 28): FotMob → hồ sơ trận theo khuôn bộ máy chấm.
nap_ngay(ma_giai, 'YYYY-MM-DD') → danh sách trận (giờ VN) với H, A (10 trận mẫu), Elo, xG, trọng tài, đội hình (mục 27), lối đá (mục 28), lịch (mục 23)."""
import json,os,sys,datetime as dt,re,unicodedata
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from khuon import fotmob as FM
from khuon.giai import GIAI,ten_mau,CUP_CHAU_LUC
from corner_style import stats_of,_num,match_row,profile_venue,matchup,flags,summary
import lineup as LU
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def vn(t): return dt.datetime.fromisoformat(t.replace('Z','+00:00'))+dt.timedelta(hours=7)
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def toks(s): return {w for w in re.split(r'[^a-z0-9]+',norm(s)) if len(w)>=4 and w not in('borussia','club','real','united','city','sport','football')}
ELO_ALL=json.load(open(os.path.join(ROOT,'elo/elo_all.json'))); MAP=json.load(open(os.path.join(ROOT,'elo/map.json')))
DERBY=json.load(open(os.path.join(ROOT,'rules/derby.json')))
def is_derby(a,b): return any((toks(a)&toks(x) and toks(b)&toks(y)) or (toks(a)&toks(y) and toks(b)&toks(x)) for x,y in DERBY)
ALIAS=json.load(open(os.path.join(ROOT,'khuon','elo_alias.json'))) if os.path.exists(os.path.join(ROOT,'khuon','elo_alias.json')) else {}
def _w(s): return [w for w in re.split(r'[^a-z0-9]+',norm(s)) if w]
STOP={'fc','afc','cf','sc','ac','club','de','the','sv','vfl','vfb','tsg','fsv','1','04','05','1899','1846','1848','1910'}
def elo_club(name):
    """ClubElo đã lưu (elo/elo_all.json). Khớp: bảng alias → map cũ → trùng tên → mọi từ của tên ClubElo đều có trong tên FotMob (duy nhất).
    Không khớp chắc chắn → None (bộ chạy DỪNG và báo, không trộn thang Elo ước tính với ClubElo)."""
    for k in (ALIAS.get(name),MAP.get(name),name):
        if k and k in ELO_ALL: return ELO_ALL[k][1],'ClubElo'
    nw=set(_w(name.replace('Manchester','Man')))-STOP
    c=[k for k in ELO_ALL if (set(_w(k))-STOP) and (set(_w(k))-STOP)<=nw]
    if len(c)==1: return ELO_ALL[c[0]][1],'ClubElo'
    return None
def elo_bxh(lg,tid):
    """Mục 25: giải không có ClubElo → 1500 + 110 × hiệu số bàn/trận theo bảng xếp hạng."""
    try: tb=lg['table'][0]['data']['table']['all']
    except Exception: return None
    for r in tb:
        if str(r['id'])==str(tid):
            gf,ga=map(int,r['scoresStr'].split('-')); return 1500+110*(gf-ga)/max(1,r['played']),'Elo ước tính (BXH)'
    return None
def ban_ghi(mid,tid,tour_name):
    """Một trận mẫu → bản ghi theo khuôn bộ máy (gf, ga, cf, ca, cor, h1, cards, home, xg…)."""
    d=FM.tran(mid,True); c=d['content']; S=stats_of(c); S1=stats_of(c,'FirstHalf')
    g=d['general']; home=str(g['homeTeam']['id'])==str(tid); i,j=(0,1) if home else (1,0)
    hs,as_=[int(x) for x in d['header']['status']['scoreStr'].split(' - ')]
    gf,ga=(hs,as_) if home else (as_,hs)
    cor=S.get('corners'); c1=S1.get('corners'); yc=S.get('yellow_cards'); rc=S.get('red_cards'); xg=S.get('expected_goals')
    n=lambda v:_num(v) or 0
    return dict(mid=str(mid),lg=tour_name,acl=(tour_name=='ACL'),date=vn(g['matchTimeUTC'] if 'matchTimeUTC' in g else d['header']['status']['utcTime']).strftime('%d/%m/%Y') if False else '',
        opp=(g['awayTeam'] if home else g['homeTeam'])['name'],home=home,gf=gf,ga=ga,
        cf=_num(cor[i]) if cor else None,ca=_num(cor[j]) if cor else None,cor=(n(cor[0])+n(cor[1])) if cor else None,
        h1=(n(c1[0])+n(c1[1])) if c1 else None,
        cards=(n(yc[0])+n(yc[1])+2*(n(rc[0])+n(rc[1]) if rc else 0)) if yc else None,
        xgf=_num(xg[i]) if xg else None,xga=_num(xg[j]) if xg else None)
def mau10(tid,kick):
    """Mục 1: 10 trận gần nhất trước giờ đá, chỉ VĐQG + C1/EL (+ACL). Mục 2: trận thiếu số liệu góc/thẻ không tính vào 10, lùi thêm."""
    fx=FM.doi(tid)['fixtures']['allFixtures']['fixtures']
    fin=[f for f in fx if f['status'].get('finished') and not f['status'].get('cancelled') and f['status']['utcTime']<kick and ten_mau(f['tournament'])]
    fin.sort(key=lambda f:f['status']['utcTime'],reverse=True)
    R=[]; files=[]
    for f in fin:
        if len(R)>=10: break
        try: r=ban_ghi(f['id'],tid,ten_mau(f['tournament']))
        except Exception: continue
        if r['cor'] is None and len(fin)>len(R)+1 and len([x for x in fin])>12: continue   # mục 2: bù bằng trận cũ hơn khi thiếu góc
        r['date']=vn(f['status']['utcTime']).strftime('%d/%m/%Y'); R.append(r); files.append(FM.duong_dan_tran(f['id']))
    return R,files,fx
def lich(fx,kick,team_name,elo_of):
    """Mục 23 (y hệt bộ chạy 28/11): mệt / nguy cơ xoay tua (trận kế tiếp ≤ 4 ngày là C1/EL/ACL, gặp đội Elo ≥ 1800 hoặc derby)."""
    fx=[x for x in fx if ten_mau(x['tournament'])]
    prev=[x for x in fx if x['status'].get('finished') and x['status']['utcTime']<kick]
    nxt=[x for x in fx if x['status']['utcTime']>kick and not x['status'].get('cancelled')]
    p=prev[-1] if prev else None; n=nxt[0] if nxt else None
    k=dt.datetime.fromisoformat(kick.replace('Z','+00:00')); f=lambda x:dt.datetime.fromisoformat(x['status']['utcTime'].replace('Z','+00:00'))
    rest=(k-f(p)).total_seconds()/86400 if p else None; dn=(f(n).date()-k.date()).days if n else None
    cup=lambda x:ten_mau(x['tournament']) in CUP_CHAU_LUC
    eo=(elo_of(n['opponent']['name']) or (0,))[0] if n else 0
    rot=bool(n and dn<=4 and (cup(n) or eo>=1800 or is_derby(team_name,n['opponent']['name'])))
    return dict(rest=rest,prev=p and p['tournament']['name'],next=n and f"{n['tournament']['name']} gặp {n['opponent']['name']} sau {dn} ngày",
                tired=bool(p and (rest<3 or (cup(p) and rest<=4.5))),rot=rot)
def trong_tai(md):
    """Mục 4/5: trọng tài và vàng TB/trận so với TB giải (FotMob)."""
    try: R=md['content']['matchFacts']['infoBox']['Referee']
    except Exception: return None
    st={s['type']:s for s in R.get('stats',[])}
    y=st.get('yellowCards'); m=st.get('matches')
    if not y: return dict(name=R.get('text'),ryc=None,ravg=None,rm=0)
    return dict(name=R.get('text'),ryc=y.get('value'),ravg=y.get('average'),rm=(m or {}).get('value',0))
def doi_hinh(files,tid,next_path):
    """Mục 27: đội hình giả định + FotMob dự kiến/chính thức (lineup.team_report)."""
    try: r=LU.team_report(files,str(tid),next_path)
    except Exception: return None,None
    if not r: return None,None
    out={}
    for part in('att','def'):
        x=r['idx'][part]; a,b=x.get('rel'),x.get('rel_fm')
        v=(a+b)/2 if (a is not None and b is not None) else (a if a is not None else b)
        warn=(r.get('agree') is not None and r['agree']<=6 and r.get('fm_pred_type')!='standard') or (a is not None and b is not None and (a-1)*(b-1)<0 and abs(a-b)>0.2 and r.get('fm_pred_type')!='standard')
        if r.get('fm_pred_type')=='standard' and b is not None: v,warn=b,False      # mục 27(f): có đội hình chính thức → dùng chính thức
        out[part]=(v,warn)
    return out,r
def loi_da(files_h,files_a,th,ta,hn,an):
    """Mục 28: hồ sơ lối đá & chuyển đổi ra góc từ 10 trận mẫu."""
    RH=[x for x in (match_row(p,str(th)) for p in files_h) if x]; RA=[x for x in (match_row(p,str(ta)) for p in files_a) if x]
    if not RH or not RA: return dict(fl=[],txt='Lối đá: thiếu số liệu',m={})
    PH,PA=profile_venue(RH,True),profile_venue(RA,False); m=matchup(PH,PA); F=flags(PH,PA,m,hn,an)
    return dict(fl=F,txt=summary(hn,an,PH,PA,m),m=m)
def xgsum(R):
    v=[r for r in R if r.get('xgf') is not None]
    return dict(n=len(v),xgf=sum(r['xgf'] for r in v)/len(v),xga=sum(r['xga'] for r in v)/len(v)) if v else None
def nap_ngay(ma,ngay,chi_tran=None):
    """ngay: 'YYYY-MM-DD' theo GIỜ VIỆT NAM. chi_tran: lọc theo tên đội (vd 'Arsenal')."""
    cf=GIAI[ma]; lg=FM.giai(cf['fotmob'])
    M=[m for m in lg['fixtures']['allMatches'] if vn(m['status']['utcTime']).strftime('%Y-%m-%d')==ngay and not m['status'].get('cancelled')]
    if chi_tran: M=[m for m in M if any(norm(chi_tran) in norm(m[s]['name']) for s in('home','away'))]
    M.sort(key=lambda m:(m['status']['utcTime'],str(m['id'])))
    out=[]
    for m in M:
        kick=m['status']['utcTime']; th,ta=str(m['home']['id']),str(m['away']['id']); hn,an=m['home']['name'],m['away']['name']
        md=FM.tran(m['id'],False); nxt=FM.duong_dan_tran(m['id'])
        H,fh,fxh=mau10(th,kick); A,fa,fxa=mau10(ta,kick)
        if cf['elo']=='clubelo':
            eh=elo_club(hn); ea=elo_club(an)
            thieu=[n_ for n_,e_ in ((hn,eh),(an,ea)) if not e_]
            if thieu: raise SystemExit(f"DỪNG – chưa khớp Elo (mục 25) cho: {thieu}. Thêm vào khuon/elo_alias.json dạng {{\"Tên FotMob\": \"Tên ClubElo\"}} rồi chạy lại.")
        else: eh=elo_bxh(lg,th); ea=elo_bxh(lg,ta)
        eof=lambda nm:elo_club(nm) if cf['elo']=='clubelo' else None
        LH,rh=doi_hinh(fh,th,nxt); LA,ra=doi_hinh(fa,ta,nxt)
        out.append(dict(giai=ma,mid=str(m['id']),kick=kick,gio=vn(kick).strftime('%H:%M'),ngay=vn(kick).strftime('%d/%m/%Y'),
            hn=hn,an=an,th=th,ta=ta,lab=f"{hn} (Nhà) – {an} (Khách)",H=H,A=A,elo=(eh,ea),xg=(xgsum(H),xgsum(A)),
            ref=trong_tai(md),lineup=(LH,LA),lineup_raw=(rh,ra),cs=loi_da(fh,fa,th,ta,hn,an),
            sched=(lich(fxh,kick,hn,eof),lich(fxa,kick,an,eof)),derby=is_derby(hn,an)))
    return out
if __name__=='__main__':
    ma,ngay=sys.argv[1],sys.argv[2]
    R=nap_ngay(ma,ngay,sys.argv[3] if len(sys.argv)>3 else None)
    for r in R: print(r['gio'],r['lab'],'| mẫu',len(r['H']),len(r['A']),'| Elo',r['elo'],'| TT',(r['ref'] or {}).get('name'),'| lối đá',len(r['cs']['fl']))
