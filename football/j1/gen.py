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
MK=['hc','tot','cor','h1','card']
NM={'hc':'Chấp bàn FT','tot':'Tài/Xỉu bàn FT','cor':'Góc FT','h1':'Góc H1','card':'Thẻ FT (vàng + 2×đỏ)'}
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
        c,base=line_text(mk,x,s,h_,a_,r['kv'])
        t=tier(s,mk); to=tier_old(s,mk)
        chg=None
        if t=='B?': t='C'; chg='đủ điều kiện "B chờ giá" (mẫu ≥ 65%, mô hình ≥ 58%) – chấm lại khi có giá'
        if mk=='card' and t in ('A','B'): t='C'
        out.append(dict(r=rr,mk=mk,x=x,s=s,c=c,base=base,t=t,to=to,chg=chg,notes=[]))
    ROWS[row]=dict(r=r,out=out,bk=bk,acl=acl,c29=c29,big=big,LH=LH,LA=LA)
# điều chỉnh theo tin lực lượng (Agent Reach / Football LAB) – mục 7, 27: tối đa ±1 bậc
def bump(row,mk,new,why):
    for o in ROWS[row]['out']:
        if o['mk']==mk: o['t0']=o['t']; o['t']=new; o['notes'].append(why)
bump(165,'hc','B','Agent Reach (Football LAB, cập nhật 26/11): Chiba mất 2 trụ cột phòng ngự – Tsukui (treo giò) và Nduka (cầu thủ mượn từ Kobe, không được đá gặp đội chủ quản); Kobe mất trung vệ Yamakawa (treo giò) → tin lực lượng phản bác một phần cửa Chiba, hạ A → B (mục 7/27, tối đa 1 bậc)')
bump(150,'hc','C+','Agent Reach (Football LAB, cập nhật 26/11): Cerezo vắng Lucas Fernandes, Kagawa, Okazawa và 2 người treo giò (Sakuragawa, Cools) → ủng hộ Kyoto, nâng C → C+ (mục 7/27, tối đa 1 bậc)')
bump(160,'hc','C+','Agent Reach (Football LAB): Kashima vắng Kim Tae-hyeon, Higuchi, Hirose, Koike, Anzai (hàng thủ – hai biên) và vừa đá ACL 25/11 → ủng hộ Okayama, nâng C → C+ (mục 7/23/27, tối đa 1 bậc)')
# ghi chú riêng
EXTRA={(155,'hc'):'Shimizu chỉ 1 điểm/5 trận gần nhất, ghi 1 bàn (đã nằm trong mẫu 10 trận) và 6 trận liền không thắng Urawa (Agent Reach: dongqiudi, Football LAB) → rủi ro cao; chỉ mức B, không lên A',
       (165,'hc'):'Kobe 5 trận chính thức không thắng (Football LAB) và đá ACL 24/11, 01/12 (mục 23)',
       (165,'tot'):'Kobe mất trung vệ Yamakawa, Chiba mất Tsukui + Nduka → hai hàng thủ yếu đi, cùng chiều Tài'}
# ưu tiên / TOP
for row,M in ROWS.items():
    cand=[o for o in M['out'] if o['t'] in ('A','B') and o['mk']!='card']
    cand.sort(key=lambda o:(TR[o['t']],-(o['s']['ev'] or 0)))
    for k,o in enumerate(cand[:2]): o['pri']=k+1
slots={}
for row,M in ROWS.items():
    for o in M['out']:
        if o.get('pri') and o['s']['odds']: slots.setdefault(M['r']['time'],[]).append(o)
for sl,c in slots.items():
    c.sort(key=lambda o:(TR[o['t']],-o['s']['ev']))
    for k,o in enumerate(c[:2]): o['top']=f"★ TOP {k+1} khung {sl}"
SRC='FotMob 10 trận J1 gần nhất • Odds API 27/11 (Pinnacle) • Elo ước tính từ BXH (không có ClubElo cho J1) • Football LAB'
VAL=[];ODDS=[];BKL=[]
for row,M in sorted(ROWS.items()):
    r=M['r']; hn,an=r['hn'],r['an']; h_,a_=SH[hn],SH[an]; labx=f"{hn} (Nhà) – {an} (Khách)"
    H,A=r['H'],r['A']; hasB=any(o['t'] in('A','B') for o in M['out'] if o['mk']!='card'); hasCp=any(o['t']=='C+' for o in M['out'])
    for k,o in enumerate(M['out']):
        mk=o['mk']; s=o['s']; x=o['x']; L=x['line']
        if mk=='hc':
            mh=[q['gf']-q['ga'] for q in H]; ma=[q['gf']-q['ga'] for q in A]
            au=f"Hiệu số 10 trận – {h_}: {', '.join(('+' if v>0 else '')+str(v) for v in mh)}; {an.split()[0] if False else a_}: {', '.join(('+' if v>0 else '')+str(v) for v in ma)}."
        else:
            key={'tot':None,'cor':'cor','h1':'h1','card':'cards'}[mk]
            def vals(R): return [(q['gf']+q['ga']) if mk=='tot' else q[key] for q in R if (mk=='tot' or q[key] is not None)]
            vh,va=vals(H),vals(A)
            def d(nm,v): return f"{nm} TB {lg(round(sum(v)/len(v),1))}, Tài {sum(1 for z in v if z>L)}/{len(v)}" if v else f"{nm} không có số liệu"
            au=f"Mẫu 10 trận (mốc {lg(L)}): {d(h_,vh)}; {d(a_,va)}."
        av=f"Gộp {pc(s['ps'])} (mẫu) / mô hình {pc(s['pm'])}"+(f" so với hòa vốn {pc(1/s['odds'])}; thị trường (Pinnacle, bỏ biên) {pc(s['pf'])}" if s['odds'] and s['pf'] else '')+'.'
        if mk=='hc' and M['acl']: av+=' '+'; '.join(M['acl'])+'.'
        if mk=='card': av+=' Trọng tài J1 chưa công bố (FotMob trống) → chưa xét mục 5 phần trọng tài.'
        if mk in('cor','h1','card') and not s['odds']: av+=' Chưa có giá – người dùng bổ sung sau.'
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
        if mk=='card':
            txt+=f" • KÈO THẺ (mục 29, RR riêng): {M['c29']}"+(' + TRẬN LỚN (3 gặp 2)' if M['big'] else '')
        if k==0 and not hasB: txt=('Trận không có tier B, chỉ có C+ ½R • ' if hasCp else 'KHÔNG VÀO (trận không có kèo tier B) • ')+txt
        VAL.append([SER,labx,o['c'],s['odds'] if s['odds'] else '',au,av,t,SRC,txt,'',''])
        # danh sách kèo BB:BJ
        if mk=='hc':
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
        elif mk=='card':
            g=round(r['gap']); bl=f"KÈO THẺ (mục 29, RR riêng): {M['c29']}"+(' • TRẬN LỚN (đội 3 gặp đội 2)' if M['big'] else '')+f" • Elo ước tính {round(r['elo'][0])}–{round(r['elo'][1])}, chênh {g} (tính cả lợi thế sân nhà 65) → "+("được xét Thẻ ưu tiên nếu đạt B" if (M['c29']=='CÂN BẰNG' or M['big']) else "phân tích đủ, không ưu tiên thẻ")
        else: bl=''
        BKL.append([bkv,bl])
json.dump(dict(VAL=VAL,ODDS=ODDS,BKL=BKL,FORM=D['FORM']),open(f'j1/sheet_{dk}.json','w'),ensure_ascii=False)
for v in VAL:
    if v[6]!='C': print(v[2],v[3],v[6],'|',v[8][:200])
