"""KHUÔN GHI SHEET CHUNG (mục 10, 17, 0c): cùng câu chữ cho mọi tab – AS:AY (kèo, odds, mẫu, căn cứ, tier, nguồn, kết luận + dòng 'Đã kiểm quy chuẩn'),
BB:BJ (danh sách kèo), BL (lối đá/thẻ/chấp góc), BK (đội hình mục 27)."""
import re,sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen3 import line_text,f2,pc,sg,lg
from corner_style import verdict_flags
NM={'hc':'Chấp bàn FT','tot':'Tài/Xỉu bàn FT','cor':'Góc FT','h1':'Góc H1','card':'Thẻ FT (vàng + 2×đỏ)','chc':'Chấp góc FT'}
def chk(steps): return ' • Đã kiểm quy chuẩn: '+'; '.join(f"{m} {'→ '+d if d else ('= '+k.replace('tier ','') if m=='8' else '✓')}" for m,k,d in steps)
def vn_num(t): return re.sub(r'(\d)\.(\d)',r'\1,\2',t) if isinstance(t,str) else t
def full_names(lab): a,b=lab.split(' – '); return a.replace(' (Nhà)',''),b.replace(' (Khách)','')
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
        if S_ and S_['next'] and S_['rest'] is not None: t+=f" Lịch {nm}: nghỉ {S_['rest']:.1f} ngày sau {S_['prev']}; kế tiếp {S_['next']}."
    if b['mk']=='card' and b.get('card') and b['card'].get('ref'):
        r=b['card']['ref']
        if r.get('ryc'): t+=f" Trọng tài {r['name']}: {lg(r['ryc'])} vàng/trận (TB giải {lg(r['ravg'])}, {r['rm']} trận)."
        else: t+=f" Trọng tài {r.get('name') or 'chưa công bố'}: chưa có số liệu."
    return t
def bk_text(b,raw):
    """Mục 27(d): cột BK – đội hình giả định / chính thức."""
    out=[]
    for r,nm in zip(raw,(b['hn'],b['an'])):
        if not r: out.append(f"{nm}: thiếu dữ liệu đội hình"); continue
        a=r['idx']['att']; d=r['idx']['def']; ch=r.get('fm_pred_type')=='standard'
        va=a.get('rel_fm') if ch else ((a['rel']+a['rel_fm'])/2 if a.get('rel_fm') is not None else a['rel'])
        vd=d.get('rel_fm') if ch else ((d['rel']+d['rel_fm'])/2 if d.get('rel_fm') is not None else d['rel'])
        lab=lambda v:'YẾU HƠN mẫu' if v<=0.90 else ('MẠNH HƠN mẫu' if v>=1.10 else 'tương đương mẫu')
        out.append(f"{nm}: tấn công {lg(round(va,2))} – {lab(va)}, phòng ngự {lg(round(vd,2))} – {lab(vd)} ({'đội hình CHÍNH THỨC' if ch else 'trộn giả định + FotMob dự kiến, trùng '+str(r.get('agree'))+'/11'})"+(f"; vắng: {', '.join(o[0] for o in r['outs'][:5])}" if r.get('outs') else ''))
    return 'ĐỘI HÌNH (mục 27, tiêu chí phụ) • '+' | '.join(out)
def payload(MATCH,ser,src_txt):
    PAY={}
    for mid,bs in MATCH.items():
        hasB=any(o['t'] in('A','B') and o['mk']!='card' and not o.get('abn') for o in bs); hasCp=any(o['t']=='C+' and o['mk']!='card' for o in bs)
        for b in bs:
            s=b['s']; c,base=base_of(b); t=b['t']; notes=list(b['notes']); pre=[]
            if b.get('nodata') is not None: pre.append(notes.pop(0))
            if b.get('abn'): pre.append(next((n for n in notes if n.startswith('⚠')),'⚠ KÈO BẤT THƯỜNG')); notes=[n for n in notes if not n.startswith('⚠')]
            if b['mk']=='hc' and not hasB: pre.append('Trận không có tier B, chỉ có C+ ½R' if hasCp else 'KHÔNG VÀO (trận không có kèo tier B)')
            if b['mk']=='card':
                if b.get('card_pri'): pre.append('Thẻ ưu tiên (mục 29, RR riêng)')
                core=f"{base} • kèo thẻ RR riêng (mục 29) • tier {t}"+('' if t in('A','B') else (' • ½R' if t=='C+' else ' • không vào'))
            elif t in('A','B'):
                if b.get('pri'): pre.append(f"Ưu tiên {b['pri']}")
                if b.get('top'): pre.append(b['top'])
                core=base+(' • tier B dự phòng (trận đã đủ 2 ưu tiên)' if b.get('dp') else '')
            elif t=='C+': pre.append('C+ • ½R'); core=base+f" • mẫu (co về thị trường) {pc(s['psa'])}, giá ≥ 1,65 (mục 18b)"
            else: core=base+' • '+reason_c(b)+' • C • không vào'
            ay=' • '.join(pre+[core]+notes)+chk(b['steps'])+'.'
            fh,fa=full_names(b['lab']); x=b['x']
            c1,c2=(fh,fa) if b['mk'] in('hc','chc') else ('Tài','Xỉu')
            o1,o2=x['sides'][0]['odds'],x['sides'][1]['odds']
            odl=[ser,b['time'],f"{b['time']} • {b['lab']}",NM[b['mk']],lg(x['line']),c1,o1 or '',c2,o2 or '']
            if b['mk'] in('cor','h1'):
                v,why=verdict_flags('Tài' if s['side']==0 else 'Xỉu',b['flags'] or [])
                tail=f" • Kèo đang chọn: {c}{(' @'+f2(s['odds'])) if s['odds'] else ''} (tier {t}) → lối đá {v.upper() if v=='phản bác' else v}"+(': điểm cộng (không nâng tier)' if v=='ủng hộ' else '')
                m=b['cs'].get('m') or {}
                bl=(b['cs']['txt'] if b['mk']=='cor' else (f"Góc H1 theo lối đá: {lg(round(m['h1'],1))} (FT {lg(round(m['tot'],1))})" if m.get('h1') is not None else 'Góc H1 theo lối đá: thiếu số liệu'))+tail
            elif b['mk']=='chc':
                kq=next((k for mm,k,d in b['steps'] if mm=='30(c)'),'')
                bl=f"Chấp góc (mục 30): kỳ vọng mô hình {lg(round(b['kv']['ch'],1))}–{lg(round(b['kv']['ca_'],1))} • kèo đang chọn {c} (tier {t}) → cờ lối đá: {kq}"
            elif b['mk']=='card': bl='KÈO THẺ (mục 29, RR riêng): '+next((k for mm,k,d in b['steps'] if mm in('29','29(g)')),'')
            else: bl=''
            mau=sorted({q.get('lg') for q in b['H']+b['A'] if q.get('lg')})
            PAY.setdefault(b['tab'],{})[b['row']]=dict(mau=mau,price_src=b.get('price_src'),mk=b['mk'],
                asy=[c,s['odds'] if s['odds'] else '',vn_num(au_of(b)),vn_num(av_of(b)),t,src_txt,vn_num(ay)],odl=odl,bl=vn_num(bl),
                bk=vn_num(b.get('bk')) if b['mk']=='hc' else None,lab=b['lab'],ser=ser,
                pri=b.get('pri'),top=b.get('top'),t=t,mid=mid,steps=b['steps'],abn=b.get('abn'))
    return PAY
