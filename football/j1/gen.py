"""Sinh nội dung tab 'J1 League' (AQ:BL, khối phong độ BP:CF) từ j1/res_<ngày>.json. python3 j1/gen.py 28/11"""
import json,sys
sys.path.insert(0,'.')
from model import tier,tier_old
from gen3 import best,line_text,f2,pc,sg,lg
from corner_style import verdict_flags
import lineup as LU
DAY=sys.argv[1] if len(sys.argv)>1 else '28/11'; dk=DAY.replace('/','-')
D=json.load(open(f'j1/res_{dk}.json')); AB=json.load(open(f'j1/abs_{dk}.json'))
SER={'28/11':46354,'29/11':46355}[DAY]
FULL={'Kato':'Ren Kato'}
MK=['hc','tot','cor','h1','chc']  # kèo thẻ J1 tạm bỏ qua theo người dùng (27/11); dòng thứ 5 = chấp góc FT
NM={'hc':'Chấp bàn FT','tot':'Tài/Xỉu bàn FT','cor':'Góc FT','h1':'Góc H1','chc':'Chấp góc FT'}
SH={'Kyoto Sanga FC':'Kyoto','Cerezo Osaka':'Cerezo','Shimizu S-Pulse':'Shimizu','Urawa Red Diamonds':'Urawa','Kashima Antlers':'Kashima',
    'Fagiano Okayama FC':'Okayama','Vissel Kobe':'Kobe','JEF United Chiba':'Chiba','Kashiwa Reysol':'Kashiwa','Sanfrecce Hiroshima':'Hiroshima'}
ACL={'Kyoto Sanga FC':'ACL Elite 24/11 và 01/12','Kashima Antlers':'ACL Elite 25/11 và 02/12','Vissel Kobe':'ACL Elite 24/11 và 01/12','Kashiwa Reysol':'ACL Elite 24/11 và 01/12'}
TR={'A':0,'B':1}
# Điều chỉnh tier theo tin lực lượng (mục 7/27, Agent Reach, tối đa ±1 bậc) – chỉ khi nguồn đáng tin
ADJ={}
def lineup_idx(r,tid,R,names):
    files=[f"j1/fm/m_{x['mid']}.json" for x in R]
    P,XIs=LU.player_table(files,tid)
    if not P: return None
    sh=LU.shape(P,XIs); bestxi=LU.pick_xi(P,{},sh)
    av={}; outn=[]
    for s in names:
        for p in P:
            nm=P[p]['name']
            if (FULL.get(s,'')==nm) or (s not in FULL and nm.split()[-1].lower()==s.lower()):
                av[p]=0.0; outn.append(nm)
    mine=LU.pick_xi(P,av,sh); res={}
    for part in ('att','def'):
        b=LU.strength(P,bestxi,part) or 1; sm=sum(LU.strength(P,x,part)/b for x in XIs)/max(1,len(XIs))
        res[part]=LU.strength(P,mine,part)/b/sm if sm else 1
    key=[P[p]['name'] for p in sorted(P,key=lambda p:-P[p]['I'])[:6]]
    return dict(sh=sh,mine=[P[p]['name'] for p in mine],idx=res,outn=outn,keyout=[n for n in outn if n in key],key=key)
def lab(v): return 'MẠNH HƠN mẫu' if v>=1.05 else ('YẾU HƠN mẫu' if v<=0.95 else 'tương đương mẫu')
def shape_s(sh): return f"{sh['DEF']}-{sh['MID']}-{sh['FWD']}"
def cls29(r):
    g=r['gap']; big=('Kashiwa' in r['hn'] and 'Hiroshima' in r['an'])
    c='CÂN BẰNG' if g<100 else ('CHÊNH VỪA' if g<200 else 'QUÁ LỆCH')
    return c,big
ROWS={};FORMR=[];BK={};CL={}
for r in D['RES']:
    hn,an=r['hn'],r['an']; h_,a_=SH[hn],SH[an]; row=r['row']; tm=r['time']
    ab=AB[str(row)]; names=ab['susp']+ab['out']
    LH=lineup_idx(r,r['h'],r['H'],names); LA=lineup_idx(r,r['a'],r['A'],names)
    def tdesc(nm,L):
        if not L: return f"{nm}: không đủ dữ liệu"
        s=f"{nm} ({shape_s(L['sh'])}): tấn công {f2(L['idx']['att'])} – {lab(L['idx']['att'])}, phòng ngự {f2(L['idx']['def'])} – {lab(L['idx']['def'])}"
        if L['outn']: s+=f"; vắng (Football LAB): {', '.join(L['outn'])}"
        if L['keyout']: s+=f"; thiếu trụ cột: {', '.join(L['keyout'])}"
        return s
    bk=f"ĐỘI HÌNH GIẢ ĐỊNH (mục 27, tiêu chí phụ) • {tdesc(hn,LH)} | {tdesc(an,LA)} • so với đội hình TB 10 trận mẫu; FotMob chưa có danh sách vắng cho J1 nên dùng Football LAB (cập nhật 26/11) • đội hình chính thức công bố ~60 phút trước trận"
    acl=[f"{SH[t]} đá {ACL[t]} (lịch dày, nguy cơ xoay tua – mục 23)" for t in (hn,an) if t in ACL]
    c29,big=cls29(r)
    # đánh giá tier
    out=[]
    for i,mk in enumerate(MK):
        x=r['ev'][mk]; s=best(x); rr=row+i
        if mk=='chc':
            l=x['line'] if s['side']==0 else -x['line']; tn=h_ if s['side']==0 else a_
            c=f"{tn} {('+' if l>0 else '')+lg(l) if l!=0 else '0'} góc FT"
            kvs=f"kỳ vọng góc {lg(round(r['kv']['ch'],1))}–{lg(round(r['kv']['ca_'],1))}"
            base=(f"{c} @{f2(s['odds'])} • mẫu {pc(s['ps'])} / hòa vốn {pc(1/s['odds'])} • EV {sg(s['ev'])} (mô hình {pc((s['evm']+1)/s['odds'])}) • {kvs}" if s['odds'] else f"{c} (chờ giá) • mẫu {pc(s['ps'])} • mô hình {pc(s['pm'])} • {kvs}")
        else:
            c,base=line_text(mk,x,s,h_,a_,r['kv'])
        t=tier(s,mk); to=tier_old(s,mk)
        chg=None
        if t=='B?': t='C'; chg='đủ điều kiện "B chờ giá" (mẫu ≥ 65%, mô hình ≥ 58%) – chấm lại khi có giá'
        if mk in ('cor','h1'):
            CS=D['CS'][str(r['row'])]; v=verdict_flags('Tài' if s['side']==0 else 'Xỉu',CS['F'])[0]
            notes0=[]
            if v=='phản bác' and t in ('A','B'):
                t={'A':'B','B':'C+'}[t]; notes0.append('Mục 28: cờ lối đá PHẢN BÁC → hạ 1 bậc')
            elif v=='ủng hộ': notes0.append('Mục 28: lối đá ủng hộ (điểm cộng, không nâng)')
        else: notes0=[]
        # mục 14(8): đội được chọn sa sút rõ ở 5 trận gần nhất → tối đa C+
        if mk in ('hc','chc') and t in ('A','B'):
            RB,RO=(r['H'],r['A']) if s['side']==0 else (r['A'],r['H'])
            P=lambda R:sum(3 if q['gf']>q['ga'] else (1 if q['gf']==q['ga'] else 0) for q in R[:5])
            pb,gb,po=P(RB),sum(q['gf'] for q in RB[:5]),P(RO)
            if pb<=2 and gb<=2 and po>=4:
                t='C+'; notes0.append(f"Mục 14(8): {(h_ if s['side']==0 else a_)} chỉ {pb} điểm, ghi {gb} bàn trong 5 trận gần nhất (đối thủ {po} điểm) → phong độ ngắn hạn phản bác rõ, hạ B → C+, bỏ Ưu tiên/TOP")
        if t in ('A','B'):
            def v(q,mine):
                if mk in('hc','chc'):
                    if mk=='chc' and q['cf'] is None: return None
                    m=(q['gf']-q['ga']) if mk=='hc' else (q['cf']-q['ca']); return (m+L0) if mine else (-m+L0)
                k={'tot':q['gf']+q['ga'],'cor':q['cor'],'h1':q['h1']}[mk]
                return None if k is None else ((k-L0) if s['side']==0 else (L0-k))
            L0=x['line'] if s['side']==0 else -x['line']
            if mk not in('hc','chc'): L0=x['line']
            mineH=(s['side']==0)
            vv=[v(q,mineH) for q in r['H'][:5]]+[v(q,not mineH) for q in r['A'][:5]]
            vv=[z for z in vv if z is not None]; w=sum(z>0 for z in vv); l=sum(z<0 for z in vv)
            if w+l and w/(w+l)<=0.40:
                t={'A':'B','B':'C+'}[t]; notes0.append(f"Mục 14(8b): 5 trận gần nhất của hai đội chỉ đạt {w}/{w+l} ({w/(w+l):.0%}) ở kèo này, ngược mẫu 10 trận → hạ 1 bậc")
        out.append(dict(r=rr,mk=mk,x=x,s=s,c=c,base=base,t=t,to=to,chg=chg,notes=notes0))
    ROWS[row]=dict(r=r,out=out,bk=bk,acl=acl,c29=c29,big=big,LH=LH,LA=LA)
# điều chỉnh theo tin lực lượng (Agent Reach / Football LAB) – mục 7, 27: tối đa ±1 bậc
def bump(row,mk,how,why):
    """Tin lực lượng (mục 7/27): PHẢN BÁC → hạ 1 bậc; ỦNG HỘ → chỉ ghi điểm cộng, KHÔNG nâng tier (mục 27e)."""
    DOWN={'A':'B','B':'C+','C+':'C','C':'C'}
    for o in ROWS[row]['out']:
        if o['mk']==mk:
            if how=='down': o['t']=DOWN[o['t']]
            o['notes'].append(why)
bump(165,'hc','down','Agent Reach (Football LAB, cập nhật 26/11): Chiba mất 2 trụ cột phòng ngự – Tsukui (treo giò) và Nduka (cầu thủ mượn từ Kobe, không được đá gặp đội chủ quản); Kobe mất trung vệ Yamakawa (treo giò) → tin lực lượng phản bác một phần cửa Chiba, hạ 1 bậc (mục 7/27)')
bump(150,'hc','note','Agent Reach (Football LAB, cập nhật 26/11): Cerezo vắng Lucas Fernandes, Kagawa, Okazawa và 2 người treo giò (Sakuragawa, Cools) → điểm cộng cho Kyoto (mục 27e: ủng hộ chỉ ghi nhận, không nâng tier)')
bump(160,'hc','note','Agent Reach (Football LAB): Kashima vắng Kim Tae-hyeon, Higuchi, Hirose, Koike, Anzai (hàng thủ – hai biên) và vừa đá ACL 25/11 → điểm cộng cho Okayama (không nâng tier)')
# ghi chú riêng
EXTRA={(155,'hc'):'Cơ sở của mô hình: Urawa sân khách rất kém (5 trận khách gần nhất 1T–1H–3B, ghi 4 lọt 11), Shimizu sân nhà 2T–1H–2B; nhưng Shimizu 6 trận liền không thắng Urawa (Agent Reach: dongqiudi, Football LAB)',
       (165,'hc'):'Kobe 5 trận chính thức không thắng (gồm thua Công An Hà Nội 1–3 ở ACL 24/11) và đá ACL lại 01/12 (mục 23)',
       (165,'tot'):'Kobe mất trung vệ Yamakawa, Chiba mất Tsukui + Nduka → hai hàng thủ yếu đi, cùng chiều Tài'}
# ưu tiên / TOP
for row,M in ROWS.items():
    cand=[o for o in M['out'] if o['t'] in ('A','B')]
    cand.sort(key=lambda o:(TR[o['t']],-(o['s']['ev'] or 0)))
    for k,o in enumerate(cand[:2]): o['pri']=k+1
slots={}
for row,M in ROWS.items():
    for o in M['out']:
        if o.get('pri') and o['s']['odds']: slots.setdefault(M['r']['time'],[]).append(o)
for sl,c in slots.items():
    c.sort(key=lambda o:(TR[o['t']],-o['s']['ev']))
    for k,o in enumerate(c[:2]): o['top']=f"★ TOP {k+1} khung {sl}"
SRC='FotMob 10 trận gần nhất (J1 + ACL Elite) • Odds API 27/11 (Pinnacle; giá góc: người dùng) • Elo ước tính từ BXH (không có ClubElo cho J1) • Football LAB'
VAL=[];ODDS=[];BKL=[]
for row,M in sorted(ROWS.items()):
    r=M['r']; hn,an=r['hn'],r['an']; h_,a_=SH[hn],SH[an]; labx=f"{hn} (Nhà) – {an} (Khách)"
    H,A=r['H'],r['A']; hasB=any(o['t'] in('A','B') for o in M['out']); hasCp=any(o['t']=='C+' for o in M['out'])
    for k,o in enumerate(M['out']):
        mk=o['mk']; s=o['s']; x=o['x']; L=x['line']
        if mk=='chc':
            mh=[int(q['cf']-q['ca']) for q in H if q['cf'] is not None]; ma=[int(q['cf']-q['ca']) for q in A if q['cf'] is not None]
            au=f"Hiệu số góc 10 trận – {h_}: {', '.join(('+' if v>0 else '')+str(v) for v in mh)}; {a_}: {', '.join(('+' if v>0 else '')+str(v) for v in ma)}."
        elif mk=='hc':
            mh=[q['gf']-q['ga'] for q in H]; ma=[q['gf']-q['ga'] for q in A]
            au=f"Hiệu số 10 trận – {h_}: {', '.join(('+' if v>0 else '')+str(v) for v in mh)}; {an.split()[0] if False else a_}: {', '.join(('+' if v>0 else '')+str(v) for v in ma)}."
        else:
            key={'tot':None,'cor':'cor','h1':'h1','card':'cards'}[mk]
            def vals(R): return [(q['gf']+q['ga']) if mk=='tot' else q[key] for q in R if (mk=='tot' or q[key] is not None)]
            vh,va=vals(H),vals(A)
            def d(nm,v): return f"{nm} TB {lg(round(sum(v)/len(v),1))}, Tài {sum(1 for z in v if z>L)}/{len(v)}" if v else f"{nm} không có số liệu"
            au=f"Mẫu 10 trận (mốc {lg(L)}): {d(h_,vh)}; {d(a_,va)}."
        av=f"Gộp {pc(s['ps'])} (mẫu) / mô hình {pc(s['pm'])}"+(f" so với hòa vốn {pc(1/s['odds'])}; thị trường ({'giá người dùng' if mk in ('cor','h1','chc') else 'Pinnacle'}, bỏ biên) {pc(s['pf'])}" if s['odds'] and s['pf'] else '')+'.'
        if mk=='hc' and M['acl']: av+=' '+'; '.join(M['acl'])+'.'
        if mk in('cor','h1','chc') and s['odds']: av+=' Giá góc do người dùng cung cấp 27/11.'
        t=o['t']; old=f" • [Thử mục 8 (a)(b); tier cách cũ: {o['to']}]"
        notes=o['notes']+([EXTRA[(row,mk)]] if (row,mk) in EXTRA else [])
        if t in('A','B'):
            pre=' • '.join(p for p in (f"Ưu tiên {o['pri']}" if o.get('pri') else '',o.get('top','')) if p)
            txt=(pre+' • ' if pre else '')+o['base']+''.join(' • '+n for n in notes)+old+'.'
        elif t=='C+':
            txt=f"C+ • ½R • {o['base']}"+''.join(' • '+n for n in notes)+f" • mẫu (co về thị trường) {pc(s['psa'])}, giá ≥ 1,65 (mục 18b){old}."
        else:
            if s['odds'] is None: rs='chờ giá' + (f"; {o['chg']}" if o['chg'] else '; mẫu/mô hình chưa đủ (B chờ giá cần mẫu ≥ 65% và mô hình ≥ 58%)')
            elif s['evm'] is not None and s['evm']<=0: rs='mô hình ngược chiều'
            elif s['pf'] and s['ps']<=s['pf']: rs='mẫu không nghiêng hơn thị trường'
            else: rs='không đủ lợi thế (EV < 2–5% sau khi co mẫu về thị trường)'
            txt=f"{o['base']} • {rs}"+''.join(' • '+n for n in notes)+f" • C • không vào{old}."
        if k==0 and not hasB: txt=('Trận không có tier B, chỉ có C+ ½R • ' if hasCp else 'KHÔNG VÀO (trận không có kèo tier B) • ')+txt
        VAL.append([SER,labx,o['c'],s['odds'] if s['odds'] else '',au,av,t,SRC,txt,'',''])
        # danh sách kèo BB:BJ
        if mk in('hc','chc'):
            l1,o1,o2=x['line'],x['sides'][0]['odds'],x['sides'][1]['odds']; c1,c2=hn,an
        else:
            l1,o1,o2=x['line'],x['sides'][0]['odds'],x['sides'][1]['odds']; c1,c2='Tài','Xỉu'
        ODDS.append([SER,r['time'],f"{r['time']} • {labx}",NM[mk],lg(l1),c1,o1 or '',c2,o2 or ''])
        # BK, BL
        bkv=M['bk'] if k==0 else ''
        if mk in('cor','h1'):
            CS=D['CS'][str(row)]; pick='Tài' if s['side']==0 else 'Xỉu'
            v=verdict_flags(pick,CS['F'])[0]
            bl=(CS['txt'] if mk=='cor' else f"Góc H1 theo lối đá (xem dòng góc FT)")+f" • Kèo đang chọn: {o['c']} (tier {t}) → lối đá {v}"
        elif mk=='chc':
            mm=D['CS'][str(row)]['m']
            bl=f"Chấp góc theo lối đá (mục 28): {h_} {lg(round(mm['eh'],1))} – {a_} {lg(round(mm['ea'],1))} góc; mô hình {lg(round(r['kv']['ch'],1))}–{lg(round(r['kv']['ca_'],1))} • Kèo thẻ J1 tạm bỏ qua theo người dùng (27/11)" if mm else ''
        elif False:
            g=round(r['gap']); bl=f"KÈO THẺ (mục 29, RR riêng): {M['c29']}"+(' • TRẬN LỚN (đội 3 gặp đội 2)' if M['big'] else '')+f" • Elo ước tính {round(r['elo'][0])}–{round(r['elo'][1])}, chênh {g} (tính cả lợi thế sân nhà 65) → "+("được xét Thẻ ưu tiên nếu đạt B" if (M['c29']=='CÂN BẰNG' or M['big']) else "phân tích đủ, không ưu tiên thẻ")
        else: bl=''
        BKL.append([bkv,bl])
json.dump(dict(VAL=VAL,ODDS=ODDS,BKL=BKL,FORM=D['FORM']),open(f'j1/sheet_{dk}.json','w'),ensure_ascii=False)
for v in VAL:
    if v[6]!='C': print(v[2],v[3],v[6],'|',v[8][:200])
