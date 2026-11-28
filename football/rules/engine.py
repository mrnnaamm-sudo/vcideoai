"""QUY CHUẨN CHUNG – BỘ MÁY CHẤM DUY NHẤT cho mọi giải (C1, EL, PL, LL, BL, J1 và giải mới).
Mọi tab phải chấm qua grade() + rank(); không giải nào được tự cài riêng quy tắc hay sửa tier bằng tay.
Thứ tự áp (cố định): mục 6 → mục 8 → mục 5/29 (thẻ) → mục 28 (góc) → mục 30(c) (chấp góc) → mục 14(8) → mục 14(8b) → mục 7/27 (tin lực lượng) → mục 9 (Ưu tiên/TOP).
Mỗi kèo trả về danh sách bước kiểm (steps) để đối chiếu: mục nào đã áp, kết quả, có đổi tier không."""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import tier,tier_old
from corner_style import verdict_flags
DOWN={'A':'B','B':'C+','C+':'C','C':'C'}
ORD={'A':0,'B':1,'C+':2,'C':3}
RR_CHUNG=('hc','tot','cor','h1','chc')   # mục 29(b): thẻ tính RR riêng

def pts5(R): return sum(3 if q['gf']>q['ga'] else (1 if q['gf']==q['ga'] else 0) for q in R[:5])
def goals5(R): return sum(q['gf'] for q in R[:5])

def trend5(mk,x,s,H,A):
    """Mục 14(8b): tỷ lệ thắng của CHÍNH kèo này trong 5 trận gần nhất mỗi đội (mẫu xếp mới → cũ)."""
    home_side=(s['side']==0)
    if mk in('hc','chc'):
        L0=x['line'] if home_side else -x['line']
        def v(q,mine):
            if mk=='chc' and q.get('cf') is None: return None
            m=(q['gf']-q['ga']) if mk=='hc' else (q['cf']-q['ca'])
            return (m+L0) if mine else (-m+L0)
        vv=[v(q,home_side) for q in H[:5]]+[v(q,not home_side) for q in A[:5]]
    else:
        L0=x['line']
        def v(q):
            k={'tot':q['gf']+q['ga'],'cor':q.get('cor'),'h1':q.get('h1')}[mk]
            return None if k is None else ((k-L0) if home_side else (L0-k))
        vv=[v(q) for q in H[:5]]+[v(q) for q in A[:5]]
    vv=[z for z in vv if z is not None]
    return sum(z>0 for z in vv),sum(z<0 for z in vv)

def elo_class(eh,ea,big=False):
    g=abs(eh+65-ea)
    return ('CÂN BẰNG' if g<100 else ('CHÊNH VỪA' if g<200 else 'QUÁ LỆCH')),round(g)

def check16(b):
    mk,x,s=b['mk'],b['x'],b['s']
    if not s['odds']: return None
    oo=[z['odds'] for z in x['sides'] if z['odds']]
    if len(oo)==2 and 1/oo[0]+1/oo[1]<1.0: return f"tổng 1/odds {1/oo[0]+1/oo[1]:.3f} < 1,00 – giá lỗi/giá cũ (16c)"
    eh,ea=b.get('elo') or (None,None)
    if mk=='hc' and eh and ea:
        Lh=x['line']; gap=eh+65-ea
        dog_side=0 if Lh>0 else 1; dog_odds=x['sides'][dog_side]['odds']
        if abs(Lh)>=2.5 and dog_odds and dog_odds>=2.3 and abs(gap)<150: return f"chấp sâu {abs(Lh):g} giữa hai đội gần sức (Elo chênh {abs(gap):.0f}) mà cửa dưới @{dog_odds} (16a)"
        strong=0 if gap>0 else 1
        if abs(gap)>=200 and s['side']==strong and abs(Lh)<=1 and s['odds']>=2.10: return f"đội mạnh hơn {abs(gap):.0f} Elo chỉ chấp {abs(Lh):g} mà giá {s['odds']} (16g)"
    if mk=='tot' and s['side']==0 and x['line']<=1.5 and s['odds']>=1.7: return "mốc Tài rất thấp mà giá cao (16b)"
    if s['odds']>=2.30 and mk!='card':
        kvk={'tot':'tot','cor':'cor','h1':'h1'}.get(mk); kvv=b['kv'].get(kvk) if kvk else None
        far=(kvv is not None and ((kvv-x['line']>=1.5) if s['side']==0 else (x['line']-kvv>=1.5)))
        if s['ps']>=0.70 or far: return f"phong độ nghiêng rất mạnh (mẫu {s['ps']*100:.0f}%) mà giá vẫn {s['odds']} (16e)"
    return None

def grade(b):
    """b: dict(league, tab, row, mk, x, s, H, A, names=(tên nhà[], tên khách[]), flags=[cờ lối đá],
       price_src='nhà cái'|'quy đổi'|None, news=[dict(how='down'|'C'|'note', muc, why)],
       card=dict(ref=..., kv_card, elo=(eh,ea), big, pl) cho kèo thẻ)."""
    mk,x,s=b['mk'],b['x'],b['s']; steps=[]; notes=[]
    def step(muc,kq,doi=None): steps.append((muc,kq,doi))
    # mục 29(g): J1 bỏ kèo thẻ
    if mk=='card' and b['league']=='J1':
        step('29(g)','J1 bỏ kèo thẻ'); return dict(t='C',steps=steps,notes=notes)
    # mục 6: chỉ giá nhà cái thật
    if s['odds'] and b.get('price_src')=='quy đổi':
        step('6','giá quy đổi từ 1X2 – không phải giá nhà cái → coi như chờ giá','C')
        return dict(t='C',steps=steps,notes=['Mục 6: giá quy đổi từ 1X2, không phải giá nhà cái → chờ giá thật mới chấm'])
    step('6','giá nhà cái' if s['odds'] else 'chưa có giá')
    H,A=b['H'],b['A']
    # mục 15: không đủ số liệu góc/thẻ (< 8 trận) → cả trận C
    need=('cor',) if b['league']=='J1' else ('cor','cards')
    nmin=min(sum(1 for q in R if all(q.get(k) is not None for k in need)) for R in (H,A))
    if nmin<8:
        step('15',f"chỉ {nmin} trận đủ số liệu",'C'); b['nodata']=nmin
        return dict(t='C',steps=steps,notes=[f"KHÔNG ĐỦ SỐ LIỆU PHÂN TÍCH (chỉ {nmin} trận có số liệu góc/thẻ)"])
    step('15',f"đủ số liệu ({nmin}/10)")
    # mục 16: kèo bất thường → tối đa C, không Ưu tiên/TOP
    abn=check16(b)
    if abn: step('16','⚠ '+abn,'tối đa C'); b['abn']=abn
    else: step('16','không bất thường')
    # mục 8 (+5 cho thẻ)
    if mk=='card':
        c=b['card']; ref=c.get('ref'); pick_tai=(s['side']==0)
        if ref and ref.get('rm',0)>=10:
            d=ref['ryc']-ref['ravg']; d_pick=d if pick_tai else -d
            ref_ok=d_pick>-0.5
        else: d_pick=None; ref_ok=None
        tc=b.get('tinh_chat') or {}
        f24=(1.15 if tc.get('derby') else 1)*(1.10 if tc.get('quyet_dinh') else 1)*(1.05 if tc.get('nhieu_loi') else 1)*(0.92 if tc.get('het_dong_luc') else 1)
        kvc=c['kv_card']*f24 if c.get('kv_card') is not None else None
        cdev=abs(kvc-x['line']) if kvc is not None else None
        t=tier(s,'card',True,ref_ok,cdev,d_pick)
        if t=='B?': t='C'
        step('5',f"trọng tài lệch {d_pick:+.2f} theo cửa chọn" if d_pick is not None else 'trọng tài thiếu mẫu (< 10 trận) → không lên C+/B',t)
        # mục 24: Tài thẻ chỉ xét B khi hệ số ≥ 1,0; derby/trận quyết định không vào Xỉu thẻ
        if pick_tai and f24<1.0 and t in('A','B'): t='C+'
        if (not pick_tai) and (tc.get('derby') or tc.get('quyet_dinh')): t='C'
        step('24',f"hệ số tính chất trận {f24:.2f}"+(' (derby)' if tc.get('derby') else '')+(' (trận quyết định)' if tc.get('quyet_dinh') else ''),t)
        cls,g=elo_class(*c['elo'])
        cap='C' if cls=='QUÁ LỆCH' else ('B' if (cls=='CHÊNH VỪA' and not c.get('big') and not c.get('pl')) else 'A')
        if ORD[t]<ORD[cap]: t=cap
        uu=(t in('A','B') and (cls=='CÂN BẰNG' or c.get('big') or (c.get('pl') and g<200)))
        step('29',f"{cls} (chênh {g})"+(f" → tối đa {cap}" if cap!='A' else '')+f"; {'Thẻ ưu tiên' if uu else 'không ưu tiên'}",t)
        if uu: notes.append('Thẻ ưu tiên (mục 29, RR riêng)')
        for n in b.get('news',[]):
            if n['how']=='C' and t!='C': t='C'; step(n['muc'],n['why'],'C'); notes.append(n['why'])
            elif n['how']=='down' and t!='C': t=DOWN[t]; step(n['muc'],n['why'],t); notes.append(n['why'])
            elif n['how']=='note': notes.append(n['why'])
        if b.get('abn') and t!='C': t='C'; notes.insert(0,f"⚠ KÈO BẤT THƯỜNG ({b['abn']})"); uu=False
        return dict(t=t,steps=steps,notes=notes,card_pri=uu)
    t=tier(s,mk)
    to=tier_old(s,mk) if s['odds'] else 'C'; b['t_old']='C' if to=='B?' else to      # mục 8: tier cách cũ để so sánh ở tổng kết tuần
    if t=='B?':
        t='C'; step('8','đủ "B chờ giá" (mẫu ≥ 65%, mô hình ≥ 58%) – chấm lại khi có giá','C')
    else: step('8',f"tier {t}")
    # mục 8: lệch thị trường (ước tính − công bằng) > 8 điểm → tối đa C+ (rà soát 28/11: nhóm lệch > 8 điểm 12 kèo ROI −23,8%)
    if t in('A','B') and s.get('gap') is not None and s['gap']>0.08:
        t='C+'; step('8',f"lệch thị trường {s['gap']*100:.1f} điểm > 8 → tối đa C+",t)
        notes.append(f"Mục 8: ước tính lệch thị trường {s['gap']*100:.1f} điểm (> 8) → tối đa C+, không Ưu tiên/TOP")
    # mục 8: C+ cần mẫu ≥ 8 trận
    if t=='C+' and (s.get('n') or 10)<8:
        t='C'; step('8',f"mẫu chỉ {s.get('n')} trận (< 8) → C+ không đạt",t)
    # mục 28: cờ lối đá cho góc FT/H1
    if mk in('cor','h1'):
        v,why=verdict_flags('Tài' if s['side']==0 else 'Xỉu',b.get('flags') or [])
        if v=='phản bác' and t in('A','B','C+'):
            t=DOWN[t]; step('28','cờ lối đá PHẢN BÁC: '+'; '.join(why),t); notes.append('Mục 28: cờ lối đá PHẢN BÁC ('+'; '.join(why)+') → hạ 1 bậc')
        else:
            step('28',f"lối đá {v}")
            if v=='ủng hộ': notes.append('Mục 28: lối đá ủng hộ (điểm cộng, không nâng)')
    # mục 30(c): cờ NHIỀU GÓC CHO / DỒN ÉP của đối thủ phản bác cửa mình
    if mk=='chc':
        mine,opp=(b['names'][0],b['names'][1]) if s['side']==0 else (b['names'][1],b['names'][0])
        hit=lambda f,ns:(('NHIỀU GÓC CHO' in f or 'DỒN ÉP' in f) and any(n and n in f for n in ns))
        contra=[f for f in (b.get('flags') or []) if hit(f,opp)]; sup=[f for f in (b.get('flags') or []) if hit(f,mine)]
        if contra and t in('A','B','C+'):
            t=DOWN[t]; step('30(c)','cờ phản bác: '+'; '.join(contra),t); notes.append('Mục 30(c): '+'; '.join(contra)+' → hạ 1 bậc')
        else:
            step('30(c)','phản bác' if contra else ('ủng hộ' if sup else 'trung tính'))
            if sup: notes.append('Mục 30(c): cờ lối đá ủng hộ (điểm cộng, không nâng)')
    # mục 14(8): phong độ ngắn hạn của đội được chọn
    if mk in('hc','chc'):
        RB,RO=(H,A) if s['side']==0 else (A,H)
        pb,gb,po=pts5(RB),goals5(RB),pts5(RO)
        if pb<=2 and gb<=2 and po>=4 and ORD[t]<ORD['C+']:
            t='C+'; step('14(8)',f"đội chọn {pb}đ/{gb} bàn 5 trận, đối thủ {po}đ → tối đa C+",t)
            notes.append(f"Mục 14(8): đội được chọn chỉ {pb} điểm, ghi {gb} bàn trong 5 trận gần nhất (đối thủ {po} điểm) → tối đa C+, bỏ Ưu tiên/TOP")
        else: step('14(8)',f"đội chọn {pb}đ/{gb} bàn, đối thủ {po}đ – đạt")
    # mục 14(8b): xu hướng 5 trận gần nhất của chính kèo – áp cho MỌI kèo trừ thẻ (kể cả kèo mới, mục 0h)
    if mk!='card':
        if mk in RR_CHUNG: w,l=trend5(mk,x,s,H,A)
        elif b.get('trend_fn'):            # kèo mới: bộ nạp dữ liệu phải cung cấp hàm kết quả từng trận (dương = cửa chọn thắng)
            vv=[z for z in (b['trend_fn'](q,True) for q in H[:5])]+[z for z in (b['trend_fn'](q,False) for q in A[:5])]
            vv=[z for z in vv if z is not None]; w,l=sum(z>0 for z in vv),sum(z<0 for z in vv)
        else: raise ValueError(f"mục 0(h): kèo mới '{mk}' thiếu hàm xu hướng cho mục 14(8b) – chưa được chấm")
        if w+l and w/(w+l)<=0.40 and t in('A','B'):
            t=DOWN[t]; step('14(8b)',f"5 trận gần nhất {w}/{w+l}",t)
            notes.append(f"Mục 14(8b): 5 trận gần nhất của hai đội chỉ đạt {w}/{w+l} ({w/(w+l):.0%}) ở kèo này → hạ 1 bậc")
        else: step('14(8b)',f"5 trận gần nhất {w}/{w+l} – đạt" if w+l else 'không đủ số liệu')
    # mục 14(2): cửa dưới nhận chấp trước đội mạnh hơn ≥ 150 Elo → chỉ ghi lưu ý (không hạ)
    if mk in('hc','chc') and b.get('elo') and all(b['elo']):
        g=b['elo'][0]+65-b['elo'][1]; dog=(s['side']==1 and g>=150) or (s['side']==0 and g<=-150)
        if dog: notes.append(f"Mục 14(2): cửa dưới gặp đội mạnh hơn {abs(g):.0f} Elo – lưu ý (EL 27/11 thua 2/3), không hạ")
        step('14(2)','lưu ý cửa dưới' if dog else 'không áp')
    # mục 20(d): đội khách chấp ≥ 1 trái mà thắng cách biệt ≥ mốc ở < 50% trận sân khách → hạ 1 bậc
    if mk=='hc':
        Lh=x['line']
        if Lh>=1 and s['side']==1:
            aw=[q for q in A if not q['home']]; ok=sum(1 for q in aw if q['gf']-q['ga']>=Lh)
            if aw and ok/len(aw)<0.5 and t in('A','B','C+'):
                t=DOWN[t]; step('20(d)',f"khách chấp {Lh:g}: thắng cách biệt ≥ mốc {ok}/{len(aw)} trận sân khách",t)
                notes.append(f"Mục 20(d): đội khách chấp {Lh:g} trái nhưng chỉ thắng cách biệt ≥ mốc {ok}/{len(aw)} trận sân khách → hạ 1 bậc")
            else: step('20(d)',f"khách chấp: {ok}/{len(aw)} – đạt")
        elif Lh>0 and s['side']==0:
            hm=[q for q in H if q['home']]; ok=sum(1 for q in hm if q['gf']-q['ga']>=-1)
            if hm and ok/len(hm)>=0.7: notes.append(f"Mục 20(d): đội nhà nhận chấp thua ≤ 1 bàn ở {ok}/{len(hm)} trận sân nhà → điểm cộng")
            step('20(d)','nhà nhận chấp – ghi chú')
        else: step('20(d)','không áp')
    # mục 27: đội hình giả định (tối đa ±1 bậc, ủng hộ không nâng)
    LH,LA=b.get('lineup') or (None,None)
    if LH and LA and mk!='card':
        lo=lambda L,p:L[p][0]<=0.90 and not L[p][1]
        warn=[nm for L,nm in ((LH,b['hn']),(LA,b['an'])) if L['att'][1] or L['def'][1]]
        con=[];sup=[]
        if mk in('hc','chc'):
            Lm,Lo,nm,no=(LH,LA,b['hn'],b['an']) if s['side']==0 else (LA,LH,b['an'],b['hn'])
            if mk=='hc':
                if lo(Lm,'att'): con.append(f"{nm} tấn công {Lm['att'][0]:.2f}")
                if lo(Lm,'def'): con.append(f"{nm} phòng ngự {Lm['def'][0]:.2f}")
                if lo(Lo,'att') or lo(Lo,'def'): sup.append(f"{no} yếu hơn mẫu")
            else:
                if lo(Lm,'att'): con.append(f"{nm} tấn công {Lm['att'][0]:.2f} (ít góc hơn)")
                if lo(Lo,'att'): sup.append(f"{no} tấn công {Lo['att'][0]:.2f}")
        elif s['side']==0:   # Tài
            for L,nm in ((LH,b['hn']),(LA,b['an'])):
                if lo(L,'att'): con.append(f"{nm} tấn công {L['att'][0]:.2f}")
                if mk=='tot' and lo(L,'def'): sup.append(f"{nm} phòng ngự {L['def'][0]:.2f}")
        else:                # Xỉu
            for L,nm in ((LH,b['hn']),(LA,b['an'])):
                if mk=='tot' and lo(L,'def'): con.append(f"{nm} phòng ngự {L['def'][0]:.2f}")
                if lo(L,'att'): sup.append(f"{nm} tấn công {L['att'][0]:.2f}")
        if con and t in('A','B','C+'):
            t=DOWN[t]; step('27','đội hình PHẢN BÁC: '+', '.join(con)+' (≤ 0,90)',t)
            notes.append('Mục 27: đội hình giả định phản bác ('+', '.join(con)+' ≤ 0,90 so với mẫu) → hạ 1 bậc')
        else:
            step('27','phản bác nhưng đã ở C' if con else ('ủng hộ' if sup else 'trung tính')+(' (⚠ hai nguồn lệch: '+', '.join(warn)+')' if warn else ''))
            if sup: notes.append('Mục 27: đội hình ủng hộ ('+', '.join(sup)+') – điểm cộng, không nâng')
    elif mk!='card': step('27','chưa có đội hình giả định')
    # mục 14(1): giá Pinnacle đi ngược trước giờ đá → C
    mv=b.get('move')
    if mk in('hc','tot'):
        if mv and mv['back'] and t!='C':
            t='C'; step('14(1)','giá đi ngược: '+mv['txt'],'C'); notes.append('Mục 14(1): '+mv['txt']+' → giá đi ngược cửa chọn, hạ thẳng C')
        else: step('14(1)',(mv['txt']+' – không đi ngược') if mv else 'mới 1 lần giá – kiểm lại lúc chốt')
    # mục 23: lịch thi đấu – xoay tua (không làm TOP), mệt (ghi chú)
    sh,sa=b.get('sched') or (None,None)
    for S_,nm,side_ in ((sh,b['hn'],0),(sa,b['an'],1)):
        if not S_: continue
        if S_['tired']: notes.append(f"Mục 23(a): {nm} vừa đá {S_['prev']} cách {S_['rest']:.1f} ngày (mệt)")
        if S_['rot']:
            backs=(mk in('hc','chc') and s['side']==side_)
            if backs: b['noTOP']=True; notes.append(f"Mục 23(b): {nm} đá {S_['next']} → NGUY CƠ XOAY TUA, không chọn cửa {nm} làm TOP")
            elif mk in('hc','chc'): notes.append(f"Mục 23(b): {nm} đá {S_['next']} → nguy cơ xoay tua, điểm cộng cho cửa đối thủ")
    tc=b.get('tinh_chat') or {}
    if mk=='hc' and tc.get('het_dong_luc_doi'):
        Lm=x['line'] if s['side']==0 else -x['line']; nm=b['hn'] if s['side']==0 else b['an']
        if nm in tc['het_dong_luc_doi'] and Lm<=-1 and t!='C':
            t='C'; notes.append(f"Mục 23(c): {nm} hết động lực mà phải chấp {abs(Lm):g} → không theo, tối đa C")
    step('23','xoay tua: '+(', '.join(nm for S_,nm in ((sh,b['hn']),(sa,b['an'])) if S_ and S_['rot']) or 'không'))
    # mục 16 (áp sau cùng): tối đa C
    if b.get('abn') and t!='C': t='C'; notes.insert(0,f"⚠ KÈO BẤT THƯỜNG ({b['abn']})")
    # mục 7/27: tin lực lượng – chỉ hạ hoặc ghi chú, không nâng (mục 27e)
    for n in b.get('news',[]):
        if n['how']=='C' and t!='C': t='C'; step(n['muc'],n['why'],'C'); notes.append(n['why'])
        elif n['how']=='down' and t!='C': t=DOWN[t]; step(n['muc'],n['why'],t); notes.append(n['why'])
        else:
            notes.append(n['why']); step(n['muc'],'ghi chú (không nâng tier)')
    return dict(t=t,steps=steps,notes=notes)

def rank(matches,slot_of):
    """Mục 9: mỗi trận tối đa 2 Ưu tiên (A trước B, rồi EV); TOP 1–2 mỗi khung giờ trong các kèo Ưu tiên có giá;
    góc FT/H1/chấp góc được xếp trên kèo bàn khi cùng tier và EV kém ≤ 2 điểm. Thẻ không tham gia (mục 29b)."""
    ev=lambda o:(o['s']['ev'] if o['s']['ev'] is not None else 0)
    for mid,os_ in matches.items():
        c=[o for o in os_ if o['mk']!='card' and o['t'] in('A','B') and not o.get('abn')]
        c.sort(key=lambda o:(ORD[o['t']],-ev(o)))
        # mục 9: khi chọn Ưu tiên – kèo góc (góc FT/H1/chấp góc) xếp trên kèo bàn cùng tier nếu EV kém ≤ 2 điểm
        for k in range(len(c)-1):
            a_,b_=c[k],c[k+1]
            if a_['t']==b_['t'] and a_['mk'] not in('cor','h1','chc') and b_['mk'] in('cor','h1','chc') and ev(a_)-ev(b_)<=0.02: c[k],c[k+1]=b_,a_
        for k,o in enumerate(c): o['pri']=k+1 if k<2 else None; o['dp']=k>=2
    slots={}
    for mid,os_ in matches.items():
        for o in os_:
            if o.get('pri') and o['s']['odds'] and not o.get('noTOP'): slots.setdefault(slot_of[mid],[]).append(o)
    for sl,c in slots.items():
        c.sort(key=lambda o:(ORD[o['t']],-ev(o)))
        if len(c)>1 and c[0]['t']==c[1]['t'] and c[1]['mk'] in('cor','h1','chc') and c[0]['mk'] not in('cor','h1','chc') and ev(c[0])-ev(c[1])<=0.02: c[0],c[1]=c[1],c[0]
        for k,o in enumerate(c[:2]): o['top']=f"★ TOP {k+1} khung {sl}"
