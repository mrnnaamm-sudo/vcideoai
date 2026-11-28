"""BƯỚC 2 – PHÂN TÍCH (một lệnh cho mọi giải, mọi ngày):
  A1_META=results/a1_meta.json python3 -B khuon/chay.py --ngay 2026-11-29 --giai PL,LL,BL,J1 --so-do <so_do.json> [--tran Arsenal]
Đầu vào giá: khuon/gia/<ngay>/pinnacle_<mã odds>.json (Odds API, mới nhất), pinnacle_<mã odds>_truoc.json (lần trước – mục 14(1)),
             khuon/gia/<ngay>/nguoi_dung.json (giá góc FT/góc H1/thẻ/chấp góc người dùng gửi).
so_do.json: cột AQ:AR đọc từ sheet {mã giải: [[dòng, serial ngày, 'Nhà (Nhà) – Khách (Khách)'], ...]} để biết ghi vào dòng nào.
Đầu ra: results/engine_<dd-mm>.json, results/sheet_engine_<dd-mm>.json (cho rules/audit.py), results/ke_hoach_ghi_<dd-mm>.json (các vùng cần ghi lên sheet)."""
import json,os,sys,math,argparse,datetime as dt
import shutil as _sh,glob as _gl; sys.dont_write_bytecode=True
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0,ROOT)
[_sh.rmtree(p,ignore_errors=True) for p in _gl.glob(os.path.join(ROOT,'**','__pycache__'),recursive=True)]
from rules import a1_sync
QC=a1_sync.require(os.environ.get('A1_META'),os.environ.get('A1_NOTES'))      # mục 0(i): A1 lệch bộ máy → DỪNG
from model import evaluate,chc_eval
from gen3 import best
from rules.engine import grade,rank
from rules import registry as REG
from khuon.giai import GIAI
from khuon.nap import nap_ngay,toks
from khuon.trinh_bay import payload,bk_text
ap=argparse.ArgumentParser(); ap.add_argument('--ngay',required=True); ap.add_argument('--giai',required=True); ap.add_argument('--tran'); ap.add_argument('--so-do'); ap.add_argument('--ma-tep',help='hậu tố tệp kết quả (mặc định dd-mm)')
a=ap.parse_args(); NGAY=a.ngay; D=dt.date.fromisoformat(NGAY); DK=a.ma_tep or D.strftime('%d-%m'); SER=(D-dt.date(1899,12,30)).days
GD=f'khuon/gia/{NGAY}'; os.makedirs(GD,exist_ok=True)
UO=json.load(open(f'{GD}/nguoi_dung.json')) if os.path.exists(f'{GD}/nguoi_dung.json') else {}
TC=json.load(open(f'rules/tinh_chat_{DK}.json')) if os.path.exists(f'rules/tinh_chat_{DK}.json') else {}
if not a.so_do: raise SystemExit('DỪNG – thiếu --so-do: phải đọc AQ150:AR399 của tab trước (QUY_TRINH Bước 1.3) để không ghi đè dòng ngày khác')
SO=json.load(open(a.so_do))
for _ma in a.giai.split(','):
    if _ma not in SO: raise SystemExit(f'DỪNG – sơ đồ dòng chưa có tab {_ma}')
def pin(path,hn,an):
    if not os.path.exists(path): return None
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
    """Mục 14(1) – y hệt bộ chạy chuẩn: mốc dịch ngược ≥ ¼ hoặc giá cửa mình tăng ≥ 5%."""
    if not o1 or not o2 or mk not in o1 or mk not in o2: return None
    (l1,a1,b1),(l2,a2,b2)=o1[mk],o2[mk]
    back=((l2-l1>=0.25) if side==0 else (l1-l2>=0.25)) if mk=='hc' else ((l2-l1<=-0.25) if side==0 else (l2-l1>=0.25))
    p1,p2=(a1,a2) if side==0 else (b1,b2)
    return dict(back=back or ((l1==l2) and p2>=p1*1.05),txt=f"Pinnacle lần trước → lần chốt: mốc {l1:g} → {l2:g}, giá cửa chọn {p1} → {p2}")
def user_odds(ma,hn,an):
    for k,v in UO.get(ma,{}).items():
        h,_,w=k.partition(' – ')
        if toks(h)&toks(hn) and toks(w)&toks(an): return v
    return {}
def cap_dong(ma,lab,n,vung):
    """Dòng ghi: dùng lại dòng đã có cùng ngày + cùng trận; nếu chưa có thì lấy dòng trống liền nhau trong vùng."""
    rows=SO.get(ma,[])
    def same(l):
        try: h1,a1=l.replace(' (Nhà)','').replace(' (Khách)','').split(' – '); h2,a2=lab.replace(' (Nhà)','').replace(' (Khách)','').split(' – ')
        except ValueError: return False
        return l==lab or (bool(toks(h1)&toks(h2)) and bool(toks(a1)&toks(a2)))
    have=sorted(r for r,s,l in rows if str(s)==str(SER) and same(l) and vung[0]<=r<=vung[1])
    if len(have)>=n: return have[:n]
    used={r for r,s,l in rows if s or l}|{r for t_,rs in CAP.items() if t_==ma for r in rs}
    for st in range(vung[0],vung[1]-n+2):
        if all((st+i) not in used for i in range(n)):
            CAP.setdefault(ma,set()).update(range(st,st+n)); return list(range(st,st+n))
    raise SystemExit(f'DỪNG – hết dòng trống trong vùng {vung} của tab {GIAI[ma]["tab"]}')
CAP={}
BETS=[];MATCH={};SLOT={};WARN=[]
for ma in a.giai.split(','):
    cf=GIAI[ma]; tt=cf['tt']
    for r in nap_ngay(ma,NGAY,a.tran):
        hn,an=r['hn'],r['an']; eh,ea=r['elo'][0][0],r['elo'][1][0]
        P2=pin(f"{GD}/pinnacle_{cf['odds']}.json",hn,an); P1=pin(f"{GD}/pinnacle_{cf['odds']}_truoc.json",hn,an)
        od={}
        if P2: od.update({k:P2[k] for k in('hc','tot') if k in P2})
        U=user_odds(ma,hn,an)
        for k in('hc','tot'):
            if k in U and k not in od: WARN.append(f"{r['lab']}: bỏ giá {k} người dùng – mục 6 chỉ nhận Pinnacle cho chấp/tài xỉu bàn")
        for k in('cor','h1','card','chc'):
            if U.get(k): od[k]=tuple(U[k])
        ref=r['ref'] if (r['ref'] and r['ref'].get('ryc')) else (dict(name=r['ref']['name'],ryc=None,ravg=None,rm=0) if r['ref'] else None)
        gap=abs(eh-ea); char=0.92 if gap>=250 else 1.0
        kv0,_=evaluate(r['H'],r['A'],{},ref,(eh,ea),(None,None),r['xg'],char)
        if 'hc' not in od:          # chưa có giá Pinnacle → mốc theo mô hình, để trống giá (mục 6: chờ giá, tier C)
            d=kv0['lh']-kv0['la']; od['hc']=(-round(d*4)/4 if abs(d)>=0.125 else 0.0,None,None)
        if 'tot' not in od: od['tot']=(math.floor(kv0['tot'])+0.5,None,None)
        for k in('cor','h1','card'):
            if k not in od: od[k]=(math.floor(kv0[k])+0.5,None,None)
        chc=od.pop('chc',None)
        if 'card' not in tt: od.pop('card',None)
        kv,ev=evaluate(r['H'],r['A'],od,ref,(eh,ea),(None,None),r['xg'],char)
        ev['chc']=chc_eval(r['H'],r['A'],*(chc if chc else (None,None,None)),kv)
        mid=f"{ma}{r['mid']}"; MATCH[mid]=[]; SLOT[mid]=f"{r['gio']}"
        main=[m for m in tt if m!='chc' or ma=='J1']
        rows=cap_dong(ma,r['lab'],len(main),(150,199) if ma!='J1' else (150,299))
        rmap=dict(zip(main,rows))
        if 'chc' not in rmap: rmap['chc']=cap_dong(ma,r['lab'],1,(200,249))[0]
        tcm=TC.get(mid,{}) or TC.get(r['lab'],{})
        bk=bk_text(dict(hn=hn,an=an),r['lineup_raw'])
        for mk in tt:
            if mk not in ev: continue
            x=ev[mk]; s=best(x)
            BETS.append(dict(league=ma,tab=ma,row=rmap[mk],mid=mid,mk=mk,x=x,s=s,H=r['H'],A=r['A'],names=([hn],[an]),flags=r['cs']['fl'],cs=r['cs'],kv=kv,
                price_src=(('Pinnacle '+NGAY) if mk in('hc','tot') else 'người dùng') if s['odds'] else None,
                move=moved(P1,P2,mk,s['side']) if mk in('hc','tot') else None,elo=(eh,ea),sched=r['sched'],lineup=r['lineup'],
                card=dict(ref=ref,kv_card=kv.get('card'),elo=(eh,ea),big=(eh>=1800 and ea>=1800),pl=(ma=='PL')),
                time=r['gio'],lab=r['lab'],hn=hn,an=an,od=od,bk=bk,tinh_chat=dict(tcm,derby=tcm.get('derby') or r['derby'])))
for b in BETS:
    if not REG.official(b['mk']): b.update(t='—',steps=[('0(h)','chờ tích hợp',None)],notes=[]); MATCH[b['mid']].append(b); continue
    b.update(grade(b)); MATCH[b['mid']].append(b)
rank(MATCH,SLOT)
SRC='FotMob 10 trận gần nhất (VĐQG + C1/EL/ACL) • Pinnacle (Odds API) cho chấp/tài xỉu bàn • giá góc/thẻ/chấp góc: người dùng • ClubElo / Elo ước tính từ BXH • FotMob (đội hình, lối đá, trọng tài)'
PAY=payload(MATCH,SER,SRC)
out=[dict(tab=b['tab'],row=b['row'],mid=b['mid'],mk=b['mk'],time=b['time'],lab=b['lab'],side=b['s']['side'],line=b['x']['line'],odds=b['s']['odds'],
          ps=b['s']['ps'],psa=b['s']['psa'],pm=b['s']['pm'],pf=b['s']['pf'],ev=b['s']['ev'],evm=b['s']['evm'],t=b['t'],steps=b['steps'],notes=b['notes'],
          pri=b.get('pri'),top=b.get('top'),abn=b.get('abn'),sides=[dict(side=z['side'],odds=z['odds']) for z in b['x']['sides']],price_src=b['price_src'],elo=b['elo'])
     for b in BETS]
json.dump(out,open(f'results/engine_{DK}.json','w'),ensure_ascii=False,default=str)
json.dump(PAY,open(f'results/sheet_engine_{DK}.json','w'),ensure_ascii=False,default=str)
# kế hoạch ghi: AQ:AY, BB:BJ, BK:BL theo từng đoạn dòng liền nhau (không đụng AZ:BA kết quả)
KH=[]
for ma,rows in PAY.items():
    tab=GIAI[ma]['tab']; rs=sorted(rows)
    seg=[]
    for r in rs:
        if seg and r!=seg[-1]+1:
            KH.append((ma,seg)); seg=[]
        seg.append(r)
    if seg: KH.append((ma,seg))
PLAN=[]
for ma,seg in KH:
    tab=GIAI[ma]['tab']; P=PAY[ma]; r0,r1=seg[0],seg[-1]
    PLAN.append(dict(range=f"'{tab}'!AQ{r0}:AY{r1}",values=[[P[r]['ser'],P[r]['lab']]+P[r]['asy'] for r in seg]))
    PLAN.append(dict(range=f"'{tab}'!BB{r0}:BJ{r1}",values=[P[r]['odl'] for r in seg]))
    PLAN.append(dict(range=f"'{tab}'!BK{r0}:BL{r1}",values=[[P[r]['bk'],P[r]['bl']] for r in seg]))
json.dump(PLAN,open(f'results/ke_hoach_ghi_{DK}.json','w'),ensure_ascii=False,default=str)
print(f'Mã quy chuẩn {QC} • {len(BETS)} kèo • {len(MATCH)} trận • kế hoạch ghi {len(PLAN)} vùng → results/ke_hoach_ghi_{DK}.json')
for w in WARN: print('⚠',w)
for b in BETS:
    if b['t'] in('A','B') or b.get('top') or b.get('pri'):
        print(b['tab'],b['row'],b['time'],b['lab'][:40],b['mk'],b['s']['odds'],b['t'],b.get('pri') or '',b.get('top') or '')
