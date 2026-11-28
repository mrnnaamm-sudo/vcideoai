"""CA KIỂM Ý NGHĨA (mục 0j): mỗi quy chuẩn bộ máy chấm có ví dụ dựng sẵn 'theo A1 thì kèo như thế này phải ra kết quả gì'.
Mọi ca phải ĐẠT trước mỗi lần phân tích (a1_sync.check chạy file này). Sửa đổi/bổ sung/bài học ở mục nào → sửa/thêm ca của mục đó."""
import copy,sys,os
import shutil as _sh,glob as _gl,sys as _sy; _sy.dont_write_bytecode=True
[_sh.rmtree(_p,ignore_errors=True) for _p in _gl.glob(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))),'**','__pycache__'),recursive=True)]   # không dùng mã biên dịch cũ: bộ máy chạy đúng mã nguồn hiện tại
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import engine, registry

def _q(gf,ga,home=True,cf=6,ca=4,cor=10,h1=4,cards=4): return dict(gf=gf,ga=ga,home=home,cf=cf,ca=ca,cor=cor,h1=h1,cards=cards)
def _s(side=0,odds=2.0,ps=0.65,psa=0.60,pm=0.60,pf=0.50,ev=0.16,evm=0.12,gap=0.08):
    return dict(side=side,odds=odds,ps=ps,psa=psa,pm=pm,pf=pf,pe=psa,ev=ev,evm=evm,gap=gap,n=10,edge=ps-1/odds if odds else None)
def bet(mk='hc',line=-0.5,side=0,o2=1.85,**kw):
    """Kèo chuẩn: nhà mạnh, phong độ tốt, mọi điều kiện ĐẠT → tier A (từ đó mỗi ca chỉ đổi đúng một yếu tố)."""
    s=_s(side=side,**{k:v for k,v in kw.items() if k in('odds','ps','psa','pm','pf','ev','evm','gap')})
    oth=dict(s,side=1-side,odds=o2)
    sides=[s,oth] if side==0 else [oth,s]
    H=[_q(2,0,True) for _ in range(10)]; A=[_q(0,2,False) for _ in range(10)]
    if mk in('tot','cor','h1'):   # Tài: hai đội nhiều bàn/góc
        H=[_q(3,1,True,cor=12,h1=6) for _ in range(10)]; A=[_q(2,2,False,cor=12,h1=6) for _ in range(10)]
        if side==1: H=[_q(0,0,True,cor=6,h1=2) for _ in range(10)]; A=[_q(0,1,False,cor=6,h1=2) for _ in range(10)]
    b=dict(league='PL',tab='T',row=1,mk=mk,x=dict(line=line,sides=sides),s=s,H=H,A=A,names=(['Nha'],['Khach']),hn='Nha',an='Khach',
           flags=[],kv={'tot':2.5,'cor':10,'h1':4.5},elo=(1700,1650),sched=(None,None),lineup=(None,None),price_src='Pinnacle',move=None,news=[])
    for k,v in kw.items():
        if k not in s: b[k]=v
    return b
def card(side=0,line=4.5,refd=0.6,kvc=5.3,elo=(1700,1680),pl=True,big=False,tc=None,ps=0.72,rm=12,**kw):
    b=bet('card',line=line,side=side,ps=ps,**kw)
    b['card']=dict(ref=dict(rm=rm,ryc=4.0+refd,ravg=4.0),kv_card=kvc,elo=elo,pl=pl,big=big); b['tinh_chat']=tc or {}
    return b
G=lambda b:engine.grade(copy.deepcopy(b) if 'trend_fn' not in b else b)
T=lambda b:G(b)['t']
def st(b,m): return [z for z in G(b)['steps'] if z[0]==m]

CASES=[
 ('8','Kèo chuẩn đủ điều kiện (EV ≥ 10%, EV mô hình ≥ 10%, lệch thị trường ≤ 12, mẫu nghiêng hơn thị trường) → A', lambda: T(bet())=='A'),
 ('8','EV 6% (≥ 5%), mô hình > 0 → B', lambda: T(bet(ev=0.06,evm=0.03))=='B'),
 ('8','Lệch thị trường > 8 điểm → tối đa C+ (rà soát 28/11)', lambda: T(bet(gap=0.15))=='C+'),
 ('8','Mẫu thô KHÔNG nghiêng hơn thị trường → không A/B', lambda: T(bet(ps=0.45))=='C'),
 ('8','Mô hình ngược chiều (EV mô hình < 0) → tối đa C', lambda: T(bet(evm=-0.02,ev=0.06))=='C'),
 ('8','C+: EV 3%, mẫu co ≥ hòa vốn +3, odds ≥ 1,65, mô hình cùng chiều → C+', lambda: T(bet(ev=0.03,evm=0.01,psa=0.54,odds=2.0))=='C+'),
 ('8','Chưa có giá thật → luôn C (đủ B ghi "B chờ giá")', lambda: T(bet(odds=None,ps=0.7,pm=0.6,ev=None,evm=None))=='C'),
 ('6','Giá quy đổi từ 1X2 (không phải giá nhà cái) → coi như chờ giá, C', lambda: T(bet(price_src='quy đổi'))=='C'),
 ('15','Đội có dưới 8 trận đủ số liệu góc/thẻ → cả trận C, ghi KHÔNG ĐỦ SỐ LIỆU', lambda: (lambda b:(b['H'].__setitem__(slice(0,3),[dict(q,cor=None) for q in b['H'][:3]]),G(b))[1])(bet()) ['t']=='C'),
 ('15','J1 chỉ xét số liệu góc (thiếu thẻ vẫn đủ)', lambda: T(bet(league='J1',H=[dict(_q(2,0,True),cards=None) for _ in range(10)]))=='A'),
 ('16','(c2) Tổng 1/odds hai cửa < 1,00 → ⚠ bất thường, tối đa C', lambda: T(bet(odds=2.10,o2=2.05))=='C'),
 ('16','(b) Tài bàn mốc ≤ 1,5 mà giá ≥ 1,70 → bất thường, C', lambda: T(bet('tot',line=1.5,odds=1.8,o2=2.0))=='C'),
 ('16','(e) Mẫu ≥ 70% mà giá ≥ 2,30 → bất thường, C', lambda: T(bet(ps=0.72,odds=2.4,o2=1.6))=='C'),
 ('16','(a) Chấp ≥ 2,5 giữa hai đội chênh < 150 Elo mà cửa dưới ≥ 2,30 → bất thường, C', lambda: T(bet(line=-2.5,o2=2.4,odds=1.6))=='C'),
 ('16','(g) Đội mạnh hơn ≥ 200 Elo chỉ chấp ≤ 1 mà giá ≥ 2,10 → bất thường, C', lambda: T(bet(line=-1,odds=2.2,o2=1.7,elo=(1900,1600)))=='C'),
 ('16','Kèo bất thường không được Ưu tiên/TOP', lambda: (lambda o:(engine.rank({'m':[o]},{'m':'20:00'}),o.get('pri'))[1])(dict(bet(odds=2.10,o2=2.05),t='B',abn='x')) is None),
 ('5','Thẻ: mẫu ≥ 70%, trọng tài cùng chiều ≥ 0,5, kỳ vọng lệch mốc ≥ 0,6, EV ≥ 5% → B', lambda: T(card())=='B'),
 ('5','Thẻ: trọng tài thiếu mẫu (< 10 trận) → không lên B', lambda: (lambda b:(b['card'].__setitem__('ref',None),T(b))[1])(card())!='B'),
 ('24','Tài thẻ khi hệ số tính chất < 1,0 (hết động lực) → tối đa C+', lambda: T(card(tc={'het_dong_luc':True},kvc=5.9))=='C+'),
 ('24','Derby / trận quyết định → không vào Xỉu thẻ (C)', lambda: T(card(side=1,line=4.5,refd=-0.6,kvc=3.7,tc={'derby':True}))=='C'),
 ('29','Trận QUÁ LỆCH (chênh ≥ 200 Elo) → thẻ tối đa C', lambda: T(card(elo=(1900,1600)))=='C'),
 ('29','Trận CHÊNH VỪA ngoài PL/trận lớn → thẻ tối đa B', lambda: T(card(elo=(1750,1550),pl=False))in('B','C+','C')),
 ('29(g)','J1 bỏ kèo thẻ', lambda: T(card(league='J1'))=='C' and st(card(league='J1'),'29(g)')),
 ('28','Góc: cờ lối đá PHẢN BÁC cửa chọn → hạ 1 bậc (A → B)', lambda: T(bet('cor',line=10.5,side=1,flags=['DỒN ÉP TẠO GÓC → bất lợi Xỉu góc']))=='B'),
 ('28','Góc: cờ lối đá ỦNG HỘ → chỉ điểm cộng, không nâng', lambda: T(bet('cor',line=10.5,side=1,ev=0.06,evm=0.03,flags=['HAI ĐỘI ÍT TẠT → bất lợi Tài góc']))=='B'),
 ('30(c)','Chấp góc: cờ NHIỀU GÓC CHO / DỒN ÉP của đối thủ → hạ 1 bậc', lambda: T(bet('chc',line=-1.5,flags=['NHIỀU GÓC CHO Khach']))=='B'),
 ('14(8)','Đội được chọn ≤ 2 điểm và ≤ 2 bàn trong 5 trận, đối thủ ≥ 4 điểm → tối đa C+', lambda: T(bet(H=[_q(0,1,True)]*5+[_q(2,0,True)]*5,A=[_q(1,0,False)]*5+[_q(0,2,False)]*5))=='C+'),
 ('14(8b)','Xu hướng 5 trận gần nhất của chính kèo ≤ 40% → hạ 1 bậc (A → B)', lambda: T(bet('tot',line=2.5,H=[_q(1,0,True)]*5+[_q(3,1,True)]*5,A=[_q(0,1,False)]*5+[_q(2,2,False)]*5))=='B'),
 ('14(2)','Cửa dưới nhận chấp trước đội mạnh hơn ≥ 150 Elo → chỉ ghi lưu ý, KHÔNG hạ', lambda: (lambda g:g['t']=='A' and any('14(2)' in n for n in g['notes']))(G(bet(line=-1.5,side=1,elo=(1900,1650),H=[_q(0,0,True)]*10,A=[_q(0,0,False)]*10)))),
 ('20(d)','Đội khách chấp ≥ 1 mà thắng cách biệt ≥ mốc < 50% trận sân khách → hạ 1 bậc', lambda: T(bet(line=1,side=1,elo=(1600,1700),H=[_q(0,3,True)]*10,A=[_q(3,0,True)]*5+[_q(1,1,False)]*5))=='B'),
 ('27','Đội hình giả định phản bác (tấn công đội mình theo ≤ 0,90) → hạ 1 bậc', lambda: T(bet(lineup=({'att':(0.85,False),'def':(1.0,False)},{'att':(1.0,False),'def':(1.0,False)})))=='B'),
 ('27','Đội hình ủng hộ → chỉ điểm cộng, KHÔNG nâng (B giữ B)', lambda: T(bet(ev=0.06,evm=0.03,lineup=({'att':(1.0,False),'def':(1.0,False)},{'att':(0.8,False),'def':(0.8,False)})))=='B'),
 ('27','Hai nguồn đội hình lệch (⚠) → chưa hạ', lambda: T(bet(lineup=({'att':(0.85,True),'def':(1.0,False)},{'att':(1.0,False),'def':(1.0,False)})))=='A'),
 ('14(8c)','Tin lực lượng ỦNG HỘ kèo chỉ ghi điểm cộng, KHÔNG nâng tier', lambda: T(bet(ev=0.06,evm=0.03,news=[dict(how='note',muc='7',why='tin ủng hộ')]))=='B'),
 ('7','Tin lực lượng phản bác (hạ) → hạ 1 bậc', lambda: T(bet(news=[dict(how='down',muc='7',why='vắng trụ cột')]))=='B'),
 ('14(1)','Giá Pinnacle đi ngược cửa chọn trước giờ đá → hạ thẳng C', lambda: T(bet(move=dict(back=True,txt='mốc dịch ngược ¼')))=='C'),
 ('23','Đội được chọn có nguy cơ xoay tua (trận C1/EL/ACL, Elo ≥ 1800 hoặc derby ≤ 4 ngày) → không làm TOP, tier giữ nguyên', lambda: (lambda b:(lambda g:g['t']=='A' and b.get('noTOP'))(engine.grade(b)))(bet(sched=(dict(tired=False,rot=True,next='C1 sau 3 ngày',prev='',rest=6),None)))),
 ('23','(c) Đội hết động lực mà phải chấp ≥ 1 → tối đa C', lambda: T(bet(line=-1,tinh_chat={'het_dong_luc_doi':['Nha']}))=='C'),
 ('9','Mỗi trận tối đa 2 Ưu tiên, chỉ tier A/B', lambda: (lambda os_:(engine.rank({'m':os_},{'m':'20:00'}),[o.get('pri') for o in os_])[1])([dict(bet(),t=t) for t in('B','A','B','C')])==[2,1,None,None]),
 ('9','Cùng tier, EV kém ≤ 2 điểm → kèo góc xếp TOP trên kèo bàn', lambda: (lambda a,c:(engine.rank({'m1':[a],'m2':[c]},{'m1':'20:00','m2':'20:00'}),c.get('top'))[1])(dict(bet(ev=0.10),t='B'),dict(bet('cor',line=9.5,ev=0.09),t='B'))=='★ TOP 1 khung 20:00'),
 ('9','Cửa có nguy cơ xoay tua không làm TOP', lambda: (lambda o:(engine.rank({'m':[o]},{'m':'20:00'}),o.get('top'))[1])(dict(bet(),t='A',noTOP=True)) is None),
 ('0(h)','Kèo mới hoàn toàn thiếu hàm xu hướng 5 trận → bộ máy dừng, không chấm', lambda: _raises(lambda: engine.grade(bet('x1',line=0.5)))),
 ('0(h)','Kèo mới hoàn toàn được chấm bằng phần chung (6, 8, 15, 16, 14(8b), 23, 27)', lambda: set(registry.COMMON)<= {m for m,_,_ in engine.grade(bet('x1',line=0.5,trend_fn=lambda q,h:1))['steps']}|{'23'}),
 ('1','Mẫu chỉ VĐQG + C1/EL (+ACL); không cúp quốc nội', lambda: 'Spanish Copa del Rey' not in registry.MAU_GIAI and 'UEFA Champions League' in registry.MAU_GIAI),
]

# ---- CA BIÊN NGƯỠNG: mỗi con số trong A1 được kiểm ở hai phía (đúng ngưỡng / vừa qua ngưỡng) → bộ máy đổi số mà A1 không đổi là bị bắt ----
def _tot(hw,aw):   # Tài 2,5: 5 trận gần nhất – hw trận nhà nổ Tài, aw trận khách nổ Tài; 5 trận cũ đều nổ
    H=[_q(3,1,True)]*hw+[_q(1,0,True)]*(5-hw)+[_q(3,1,True)]*5; A=[_q(2,2,False)]*aw+[_q(0,1,False)]*(5-aw)+[_q(2,2,False)]*5
    return bet('tot',line=2.5,H=H,A=A)
def _f8(hres,ares):  # 14(8): kết quả 5 trận gần nhất đội chọn (nhà) / đối thủ
    return bet(H=hres+[_q(2,0,True)]*5,A=ares+[_q(0,2,False)]*(10-len(ares)))
W,D_,L_=_q(1,0,True),_q(1,1,True),_q(0,1,True); WA,DA,LA=_q(1,0,False),_q(1,1,False),_q(0,1,False)
def _20d(k):  # khách chấp 1: 6 trận sân khách, k trận thắng cách biệt ≥ 1
    A=[_q(3,0,True)]*4+[_q(3,0,False)]+[_q(1,0,False)]*(k-1)+[_q(1,1,False)]*(6-k)
    return bet(line=1,side=1,elo=(1600,1700),H=[_q(0,3,True)]*10,A=A)
def _c25(eh): return bet(line=-2.5,odds=1.6,o2=2.30,ps=0.75,psa=0.70,pf=0.6,elo=(eh,1700),H=[_q(4,0,True)]*10,A=[_q(0,4,False)]*10)
def _lu(v): return bet(lineup=({'att':(v,False),'def':(1.0,False)},{'att':(1.0,False),'def':(1.0,False)}))
def _h15(k): b=bet(); b['H']=[dict(q,cor=None) for q in b['H'][:k]]+b['H'][k:]; return b
CASES+=[
 ('14(8b)','Biên: 5 trận gần nhất đạt đúng 40% (4/10) → hạ 1 bậc', lambda: T(_tot(2,2))=='B'),
 ('14(8b)','Biên: đạt 50% (5/10) → không hạ', lambda: T(_tot(3,2))=='A'),
 ('8','Biên A: EV 10,01% → A; EV 9,99% → B', lambda: T(bet(ev=0.1001))=='A' and T(bet(ev=0.0999))=='B'),
 ('8','Biên A: EV mô hình 10,01% → A; 9,99% → B', lambda: T(bet(evm=0.1001))=='A' and T(bet(evm=0.0999))=='B'),
 ('8','Biên lệch thị trường: 7,99 điểm → giữ A; 8,01 điểm → C+', lambda: T(bet(gap=0.0799))=='A' and T(bet(gap=0.0801))=='C+'),
 ('8','Biên lệch thị trường ở tier B: 8,01 điểm → C+; 7,99 → B', lambda: T(bet(ev=0.06,evm=0.03,gap=0.0801))=='C+' and T(bet(ev=0.06,evm=0.03,gap=0.0799))=='B'),
 ('8','Biên B: EV 5,01% → B; 4,99% → C+', lambda: T(bet(ev=0.0501,evm=0.03))=='B' and T(bet(ev=0.0499,evm=0.03))=='C+'),
 ('8','Biên C+: odds 1,65 → C+; 1,64 → C', lambda: T(bet(ev=0.03,evm=0.01,psa=0.65,ps=0.66,pf=0.6,odds=1.65,o2=2.3))=='C+' and T(bet(ev=0.03,evm=0.01,psa=0.65,ps=0.66,pf=0.6,odds=1.64,o2=2.3))=='C'),
 ('8','Biên C+: mẫu co ≥ hòa vốn + 3 điểm → C+; + 2 điểm → C', lambda: T(bet(ev=0.03,evm=0.01,psa=0.531))=='C+' and T(bet(ev=0.03,evm=0.01,psa=0.52))=='C'),
 ('15','Biên: đúng 8 trận đủ số liệu → vẫn chấm; 7 trận → C', lambda: T(_h15(2))=='A' and T(_h15(3))=='C'),
 ('16','Biên (e): mẫu 70% @2,30 → bất thường; mẫu 69% @2,30 → không', lambda: T(bet(ps=0.70,odds=2.30,o2=1.6))=='C' and T(bet(ps=0.69,odds=2.30,o2=1.6))=='A'),
 ('16','Biên (e): mẫu 72% @2,29 → không bất thường', lambda: T(bet(ps=0.72,odds=2.29,o2=1.6))=='A'),
 ('16','Biên (b): Tài 1,5 @1,70 → bất thường; @1,69 → không', lambda: T(bet('tot',line=1.5,odds=1.70,o2=2.0))=='C' and T(bet('tot',line=1.5,odds=1.69,o2=2.0))!='C'),
 ('16','Biên (g): chênh 200 Elo, chấp 1 @2,10 → bất thường; chênh 199 → không; @2,09 → không', lambda: T(bet(line=-1,odds=2.10,o2=1.75,elo=(1835,1700)))=='C' and T(bet(line=-1,odds=2.10,o2=1.75,elo=(1834,1700)))=='A' and T(bet(line=-1,odds=2.09,o2=1.75,elo=(1835,1700)))=='A'),
 ('16','Biên (a): chấp 2,5, cửa dưới @2,30, chênh 149 Elo → bất thường; 150 → không', lambda: T(_c25(1784))=='C' and T(_c25(1785))=='A'),
 ('16','Biên (c2): tổng 1/odds = 1,00 trở lên → không bất thường', lambda: T(bet(odds=2.0,o2=2.0))=='A'),
 ('14(8)','Biên: đội chọn 2 điểm/2 bàn, đối thủ 4 điểm → tối đa C+', lambda: T(_f8([D_,D_,L_,L_,L_],[WA,DA,LA,LA,LA]))=='C+'),
 ('14(8)','Biên: đội chọn 3 điểm → không áp 14(8)', lambda: 'tối đa' not in str(st(_f8([W,L_,L_,L_,L_],[WA,DA,LA,LA,LA]),'14(8)'))),
 ('14(8)','Biên: đối thủ 3 điểm → không áp 14(8)', lambda: 'tối đa' not in str(st(_f8([D_,D_,L_,L_,L_],[WA,LA,LA,LA,LA]),'14(8)'))),
 ('14(8)','Biên: đội chọn ghi 3 bàn (2 điểm) → không áp 14(8)', lambda: 'tối đa' not in str(st(_f8([_q(2,2,True),_q(1,1,True),L_,L_,L_],[WA,DA,LA,LA,LA]),'14(8)'))),
 ('20(d)','Biên: khách chấp 1 thắng cách biệt đúng 50% trận sân khách → không hạ; 33% → hạ', lambda: T(_20d(3))=='A' and T(_20d(2))=='B'),
 ('27','Biên: chỉ số đội hình 0,90 → hạ; 0,91 → không', lambda: T(_lu(0.90))=='B' and T(_lu(0.91))=='A'),
 ('29','Biên: chênh 200 Elo → QUÁ LỆCH (C); 199 → CHÊNH VỪA (PL giữ B)', lambda: T(card(elo=(1835,1700)))=='C' and T(card(elo=(1834,1700)))=='B'),
 ('29','Biên: CHÊNH VỪA ngoài PL/trận lớn bị giới hạn B (không lên A)', lambda: 'tối đa B' in str(st(card(elo=(1834,1700),pl=False),'29'))),
 ('5','Biên: trọng tài lệch +0,51 → B; +0,49 → không B', lambda: T(card(refd=0.51))=='B' and T(card(refd=0.49))!='B'),
 ('5','Biên: kỳ vọng thẻ lệch mốc 0,61 → B; 0,59 → không B', lambda: T(card(kvc=5.11))=='B' and T(card(kvc=5.09))!='B'),
 ('5','Biên: mẫu thẻ 70% → B; 69% → không B', lambda: T(card())=='B' and (lambda b:(b['s'].__setitem__('ps',0.69),T(b))[1])(card())!='B'),
 ('24','Biên: Tài thẻ hệ số đúng 1,0 → được B', lambda: T(card(tc={}))=='B'),
]

# ---- CA BIÊN bổ sung (quét đổi từng con số trong bộ máy) ----
def _cp(**k): return card(ps=0.65,**k)          # thẻ không đủ B → xét C+
def _pri(**k): g=G(card(**k)); return g.get('card_pri')
def _st24(tc): return str(st(card(tc=tc),'24'))
def _p8b():   # chấp −1: 4 thắng, 1 hòa (hoàn), 5 thua → 4/9 = 44%
    H=[_q(3,0,True)]*2+[_q(1,0,True)]+[_q(0,1,True)]*2+[_q(2,0,True)]*5; A=[_q(0,3,False)]*2+[_q(1,0,False)]*3+[_q(0,2,False)]*5
    return bet(line=-1,H=H,A=A)
def _142(eh): return G(bet(line=1.5,side=1,elo=(eh,1700),H=[_q(0,3,True)]*10,A=[_q(2,0,False)]*10))
def _20d9(): A=[_q(3,0,True)]+[_q(3,0,False)]*4+[_q(1,1,False)]*5; return bet(line=1,side=1,elo=(1600,1700),H=[_q(0,3,True)]*10,A=A)
def _20dn(ok,n): H=[_q(1,1,True)]*ok+[_q(0,3,True)]*(n-ok)+[_q(1,1,False)]*(10-n); return G(bet(line=1,H=H,A=[_q(0,2,False)]*10,odds=2.0,o2=1.85))
def _far(kv,side=0): b=bet('tot',line=2.5,side=side,ps=0.6,odds=2.30,o2=1.62); b['kv']['tot']=kv; return b
CASES+=[
 ('29','Biên: chênh 99 Elo = CÂN BẰNG → Thẻ ưu tiên; 100 = CHÊNH VỪA (ngoài PL) → không ưu tiên', lambda: _pri(elo=(1715,1681),pl=False)==True and _pri(elo=(1715,1680),pl=False)==False),
 ('29','Biên: Ngoại hạng Anh chênh 190 Elo vẫn được Thẻ ưu tiên (chênh < 200)', lambda: _pri(elo=(1825,1700),pl=True)==True),
 ('16','(a) chỉ áp khi chấp từ 2,5: chấp 2,25 cửa dưới @2,30 chênh 149 → không bất thường', lambda: T(bet(line=-2.25,odds=1.6,o2=2.30,ps=0.75,psa=0.70,pf=0.6,elo=(1784,1700),H=[_q(4,0,True)]*10,A=[_q(0,4,False)]*10))=='A'),
 ('16','(a) cửa dưới @2,29 → không bất thường', lambda: T(bet(line=-2.5,odds=1.6,o2=2.29,ps=0.75,psa=0.70,pf=0.6,elo=(1784,1700),H=[_q(4,0,True)]*10,A=[_q(0,4,False)]*10))=='A'),
 ('16','(e) Tài: kỳ vọng vượt mốc 1,5 mà giá @2,30 → bất thường; vượt 1,4 → không', lambda: T(_far(4.0))=='C' and T(_far(3.9))!='C'),
 ('16','(e) Xỉu: kỳ vọng thấp hơn mốc 1,5 mà giá @2,30 → bất thường; 1,4 → không', lambda: T(_far(1.0,1))=='C' and T(_far(1.1,1))!='C'),
 ('5','Biên: trọng tài đủ 10 trận → xét B; 9 trận → không B', lambda: T(card(rm=10))=='B' and T(card(rm=9))!='B'),
 ('5','Biên: Thẻ EV 5,01% → B; 4,99% → không B', lambda: T(card(ev=0.0501))=='B' and T(card(ev=0.0499))!='B'),
 ('5','Thẻ C+: trọng tài ngược −0,49 → C+; −0,51 → C', lambda: T(_cp(refd=-0.49))=='C+' and T(_cp(refd=-0.51))=='C'),
 ('5','Thẻ C+: mẫu co ≥ hòa vốn +3 → C+; +2,9 → C', lambda: T(_cp(psa=0.531))=='C+' and T(_cp(psa=0.529))=='C'),
 ('5','Thẻ C+: EV 2,01% → C+; 1,99% → C', lambda: T(_cp(ev=0.0201))=='C+' and T(_cp(ev=0.0199))=='C'),
 ('5','Thẻ C+: odds 1,65 → C+; 1,64 → C', lambda: T(_cp(odds=1.65,o2=2.3,psa=0.65))=='C+' and T(_cp(odds=1.64,o2=2.3,psa=0.65))=='C'),
 ('24','Hệ số: derby ×1,15; trận quyết định ×1,10; phạm lỗi nhiều ×1,05; hết động lực ×0,92', lambda: '1.15' in _st24({'derby':True}) and '1.10' in _st24({'quyet_dinh':True}) and '1.05' in _st24({'nhieu_loi':True}) and '0.92' in _st24({'het_dong_luc':True})),
 ('14(8b)','Biên: 4/9 (44%, có 1 trận hoàn) → không hạ', lambda: T(_p8b())=='A'),
 ('14(2)','Biên: chênh đúng 150 Elo (tính +65 sân nhà) → ghi lưu ý; 149 → không', lambda: any('14(2)' in n for n in _142(1785)['notes']) and not any('14(2)' in n for n in _142(1784)['notes'])),
 ('14(2)','Biên: đội NHÀ nhận chấp trước khách mạnh hơn đúng 150 Elo → lưu ý; 149 → không', lambda: any('14(2)' in n for n in G(bet(line=1.5,elo=(1500,1715),H=[_q(2,0,True)]*10,A=[_q(0,2,False)]*10))['notes']) and not any('14(2)' in n for n in G(bet(line=1.5,elo=(1500,1714),H=[_q(2,0,True)]*10,A=[_q(0,2,False)]*10))['notes'])),
 ('20(d)','Biên: khách chấp 1 thắng cách biệt 4/9 trận sân khách (44%) → hạ', lambda: T(_20d9())=='B'),
 ('20(d)','Nhà nhận chấp thua ≤ 1 bàn ở 70% trận sân nhà → điểm cộng; 6/9 (67%) → không', lambda: any('20(d)' in n for n in _20dn(7,10)['notes']) and not any('20(d)' in n for n in _20dn(6,9)['notes'])),
 ('8','Biên "B chờ giá": mẫu 65% + mô hình 58% → ghi đủ B chờ giá; 64,9% hoặc 57,9% → không', lambda: 'chờ giá' in str(st(bet(odds=None,ps=0.65,pm=0.58,ev=None,evm=None),'8')) and 'chờ giá' not in str(st(bet(odds=None,ps=0.649,pm=0.58,ev=None,evm=None),'8')) and 'chờ giá' not in str(st(bet(odds=None,ps=0.65,pm=0.579,ev=None,evm=None),'8'))),
 ('8','Biên C+: EV 2,01% → C+; 1,99% → C', lambda: T(bet(ev=0.0201,evm=0.01,psa=0.54))=='C+' and T(bet(ev=0.0199,evm=0.01,psa=0.54))=='C'),
]

def _khong_doc_tab_ket_qua():
    """Mục 0(k): bộ máy (rules/*.py trừ kiem_thu, model.py, corner_style.py, lineup.py) không đọc tab 'Tổng kết RR tuần'/'Kèo đã vào' (sheetId 204, 206)."""
    import glob,re
    D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fs=[f for f in glob.glob(os.path.join(D,'rules','*.py')) if not f.endswith(('kiem_thu.py','doi_chieu.py'))]+[os.path.join(D,x) for x in ('model.py','corner_style.py','lineup.py')]
    for f in fs:
        s=open(f).read()
        if re.search(r"Tổng kết RR tuần|Kèo đã vào",s): return False
    from rules import a1_sync
    return not ({204,206}&set(a1_sync.TABS))
CASES+=[('0(k)','Bộ máy không đọc tab Tổng kết RR tuần / Kèo đã vào và hai tab này không nằm trong danh sách tab kèo của A1', _khong_doc_tab_ket_qua)]

def _w8():
    """Mục 8(b): ước tính = 40% mô hình (ở đúng giá) + 30% mẫu đã co + 30% công bằng; thiếu giá cửa kia 55% mô hình + 45% mẫu; mẫu đã co = (mẫu + công bằng)/2."""
    from model import evaluate,chc_eval
    H=[_q(2,1,True,cf=6,ca=3,cor=9,h1=4,cards=4)]*5+[_q(1,1,True,cf=5,ca=5,cor=10,h1=5,cards=3)]*5
    A=[_q(0,1,False,cf=4,ca=6,cor=10,h1=4,cards=5)]*5+[_q(2,2,False,cf=5,ca=5,cor=11,h1=5,cards=4)]*5
    kv,ev=evaluate(H,A,{'hc':(-0.5,1.95,1.95),'tot':(2.5,1.90,2.00),'cor':(9.5,1.85,None)},None,(1700,1650),(None,None),(None,None),1.0)
    ev['chc']=chc_eval(H,A,-1.5,1.90,1.90,kv)
    ok=0
    for mk,x in ev.items():
        for s in x['sides']:
            if not s['odds']: continue
            pmg=(s['evm']+1)/s['odds']
            if s['pf'] is not None:
                if abs(s['psa']-(s['ps']+s['pf'])/2)>1e-9: return False
                pe=0.4*pmg+0.3*s['psa']+0.3*s['pf']
            else: pe=0.55*pmg+0.45*s['psa']
            if abs(pe*s['odds']-1-s['ev'])>1e-9: return False
            ok+=1
    return ok>=6
def _n8(n): b=bet(ev=0.03,evm=0.01,psa=0.54); b['s']['n']=n; return T(b)
def _pri_goc():
    a=dict(bet(ev=0.10),t='B',mk='hc'); c=dict(bet('cor',line=9.5,ev=0.085),t='B')
    engine.rank({'m':[a,c]},{'m':'20:00'}); return c.get('pri')==1 and a.get('pri')==2
CASES+=[
 ('8','Trọng số ước tính 40/30/30 (thiếu giá cửa kia 55/45) và mẫu đã co = (mẫu + công bằng)/2 – đúng như A1 mục 8(b)', _w8),
 ('8','C+ cần mẫu ≥ 8 trận: 8 trận → C+; 7 trận → C', lambda: _n8(8)=='C+' and _n8(7)=='C'),
 ('8','Kết luận có tier cách cũ để so sánh (mục 8)', lambda: (lambda b:(engine.grade(b),b.get('t_old') in('A','B','C+','C'))[1])(bet())),
 ('9','Chọn Ưu tiên: kèo góc cùng tier, EV kém ≤ 2 điểm → xếp trên kèo bàn', _pri_goc),
]

def _raises(f):
    try: f(); return False
    except ValueError: return True

def run():
    """→ (số ca, danh sách lỗi). Kiểm thêm: mục nào bộ máy chấm mà không có ca kiểm."""
    err=[]
    for m,y,f in CASES:
        try: ok=bool(f())
        except Exception as e: ok=False; y+=f' (lỗi {type(e).__name__}: {e})'
        if not ok: err.append(f"ca kiểm mục {m} KHÔNG ĐẠT: {y}")
    have={m for m,_,_ in CASES}
    for m,r in registry.REG.items():
        if r['loai']!='cham': continue
        bb=[r['buoc']] if isinstance(r['buoc'],str) else list(r['buoc'])
        for b_ in bb:
            if b_ not in have: err.append(f"mục {m}: bước '{b_}' bộ máy chấm nhưng KHÔNG có ca kiểm ý nghĩa")
    return len(CASES),err
if __name__=='__main__':
    n,e=run(); print(f"{n} ca kiểm ý nghĩa –",'ĐẠT' if not e else 'LỖI'); [print(' -',x) for x in e]
