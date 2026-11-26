import json
OUT=json.load(open('el/out2.json'))
def pc(x): return f"{x*100:.0f}%"
def pv(x): return f"{x*100:.1f}%".replace('.',',')
def odd(x): return f"{x:.2f}".replace('.',',')
def lg(x): return f"{x:g}".replace('.',',')
PSV="Bài học PSV +2,5: đội dưới cơ có trận thua đậm (≤ −4) trong mẫu → hạ C."
CROSS="Lưu ý: mẫu hai đội ở hai giải khác trình độ nên hiệu số có thể bị phóng đại."
D={ (1,'tot'):('C','Bài học Gala–Villa: Celta vắng tiền đạo Borja Iglesias, Hugo González → không theo Tài.'),
 (8,'tot'):('C','Palace vắng Mateta, Sarr → không theo Tài.'),
 (8,'cor'):('C','Bài học Gala–Villa: Palace vắng Mateta, Sarr → không theo Tài góc.'),
 (8,'hc'):('C','⚠ KÈO BẤT THƯỜNG (mẫu 85% nhưng thị trường chỉ 55%, lệch 30 điểm – giống Atlético–Viking) → tối đa C. Palace vắng 5 trụ cột (Mateta, Sarr, Mingueza, Riad, Tomiyasu) → ủng hộ Real Sociedad. Hai giải cùng trình độ.'),
 (10,'hc'):('C','⚠ KÈO BẤT THƯỜNG (mẫu 80% nhưng thị trường chỉ 50%, lệch 30 điểm) → tối đa C. Sturm vắng Kiteishvili, Koller, Grgić nhưng Hoffenheim cũng vắng 4 hậu vệ. '+CROSS),
 (11,'hc'):('B','Juventus vắng Yıldız, Locatelli, Thuram, Kalulu, Grabara, N. González → khó thắng đậm. '+CROSS),
 (16,'hc'):('B','Sunderland vắng Xhaka, Brobbey, Diarra, Ballard, Mundle → khó thắng đậm. '+CROSS),
 (4,'hc'):('B','Olympiacos vắng El Kaabi, Chiquinho, Puerta, Hezze; Milan vắng Modrić, Pavlović. Tin lực lượng chia đều.'),
}
PRI={1:[(1,'cor')],2:[(1,'cor')],3:[(1,'tot'),(2,'cor')],4:[(1,'hc'),(2,'cor')],5:[(1,'h1')],6:[(1,'h1')],8:[(1,'hc')],9:[(1,'hc')],10:[(1,'hc'),(2,'tot')],11:[(1,'hc'),(2,'tot')],12:[(1,'tot')],14:[(1,'cor')],16:[(1,'hc'),(2,'tot')]}
TOP={(3,'tot'):'★ TOP 1 khung 00:45',(4,'hc'):'★ TOP 2 khung 00:45',(8,'hc'):'★ TOP 1 khung 03:00',(16,'hc'):'★ TOP 2 khung 03:00'}
MK={'hc':'Chấp bàn FT','tot':'Tài/Xỉu bàn FT','cor':'Góc FT','h1':'Góc H1','card':'Thẻ FT (vàng + 2×đỏ)'}
SHORT=lambda m: (m['hn'] if m['nh']<8 else m['an'])+f" chỉ có {min(m['nh'],m['na'])} trận đủ số liệu góc/thẻ (giải quốc nội không công bố, đã bù hết trận cúp châu Âu có số liệu) → mẫu mỏng, giữ C."
ANOM={16:'Tài 4,5 thẻ giá 2,45',17:'Tài 4,5 thẻ giá 2,40',11:'Tài 4,5 thẻ giá 2,50'}
def tierof(i,m,r):
    ref=m['ref']; rdir=ref[8]; k=r['k']; p=r['p']; o=r['od']; e=r['e']; t='C'
    if k=='card':
        want=1 if r['side']=='Tài' else -1
        if rdir==want and e is not None and e>=0.09 and p>=0.55: t='B'
    else:
        if e is not None and e>=0.25: t='A'
        elif e is not None and e>=0.09 and p>=0.55: t='B'
        if k=='hc' and r.get('psv'): t='C'
    if (i,k) in D: t=D[(i,k)][0]
    if m['nh']<8 or m['na']<8: t='C'
    return t
PRI2={};CAND=[]
for i,m in enumerate(OUT):
    bs=sorted([r for r in m['res'] if tierof(i,m,r) in('A','B')],key=lambda r:-r['e'])[:2]
    PRI2[i]={r['k']:n+1 for n,r in enumerate(bs)}
    CAND+=[(m['time'],r['e'],r['p'],i,r['k']) for r in bs]
TOP={}
for t in ('00:45','03:00'):
    c=sorted([x for x in CAND if x[0]==t],key=lambda x:(-x[1],-x[2]))[:2]
    for n,x in enumerate(c): TOP[(x[3],x[4])]=f'★ TOP {n+1} khung {t}'
A=[];B=[];R=[]
for i,m in enumerate(OUT):
    ref=m['ref']; rname,rc,rm,ryc,ravg,rred,rfo,rv,rdir=ref
    pri=PRI2.get(i,{})
    rows=[]
    for r in m['res']:
        k=r['k']; p=r['p']; o=r['od']; e=r['e']
        be=(1/o) if o else None
        tier='C'; note=''
        if k=='card':
            want=1 if r['side']=='Tài' else -1
            refs=f"Trọng tài {rname} {lg(ryc) if ryc else '?'} vàng/trận (TB giải {lg(ravg) if ravg else '?'}, {rm} trận) → {rv}"
            agree=(rdir==want)
            note=refs+(' → cùng chiều.' if agree else ' → không cùng chiều, giữ C theo quy tắc thẻ.')
            if agree and ((e is not None and e>=0.09 and p>=0.55) or (o is None and p>=0.65)): tier='B'
        else:
            if e is not None and e>=0.25: tier='A'
            elif e is not None and e>=0.09 and p>=0.55: tier='B'
            elif o is None and p>=0.65: tier='B'
            if k=='hc' and r.get('psv'): tier='C'; note=PSV
        if (i,k) in D: tier,note=D[(i,k)][0],D[(i,k)][1]
        if (m['nh']<8 or m['na']<8) and tier!='C': tier='C'; note=SHORT(m)
        if m['nh']<8 or m['na']<8: note=note or SHORT(m)
        if k=='card' and i in ANOM: note='⚠ KÈO BẤT THƯỜNG ('+ANOM[i]+' ở mốc thấp – nhà cái định giá ít thẻ, giống Atlético–Viking) → KHÔNG theo Tài, tối đa C. '+note
        av=f"Gộp {pc(p)} ({r['n']})"+(f" so với hòa vốn {pv(be)}." if be else ". Chưa có giá – bạn bổ sung"+(f", cần ≥{odd(1/(p-0.08))}." if p>0.6 else "."))
        if note: av+=' '+note
        if k=='hc': av+=' '+m['inj']
        cua=r['cua']; os_=f" @{odd(o)}" if o else " (chờ giá)"
        body=f"{cua}{os_} • mẫu {pc(p)}"+(f" / hòa vốn {pc(be)}" if be else '')
        pre=''
        if k in pri and tier in('A','B'): pre=f"Ưu tiên {pri[k]} • "+(TOP[(i,k)]+' • ' if (i,k) in TOP else '')
        if k=='card' and i in ANOM: pre='⚠ KÈO BẤT THƯỜNG ('+ANOM[i]+') • '+pre
        if k=='hc' and i in(8,10): pre='⚠ KÈO BẤT THƯỜNG (mẫu cao hơn hòa vốn 30 điểm) • '+pre
        ay=pre+body+(" (TIER A)" if tier=='A' else '')+(' • tham khảo.' if tier=='C' else '.')
        rows.append([46353,m['match'],cua,round(o,2) if o else '',r['ar'],av,tier,'FotMob/ESPN 10 trận • Pinnacle 26/11 + giá góc/thẻ người dùng • UEFA',ay])
        L=r['line']
        if k=='hc':
            Lh,hn,oh,an,oa=L; B.append([46353,m['time'],m['lab'],MK[k],Lh,hn,oh,an,oa])
        else:
            line,_,oo,_,uu=L; B.append([46353,m['time'],m['lab'],MK[k],line,'Tài',round(oo,2) if oo else '','Xỉu',round(uu,2) if uu else ''])
    if m['nh']<8 or m['na']<8:
        sn=m['hn'] if m['nh']<8 else m['an']
        for x in rows: x[8]=f"KHÔNG ĐỦ SỐ LIỆU PHÂN TÍCH ({sn} chỉ có {min(m['nh'],m['na'])} trận có số liệu góc/thẻ) • "+x[8]
    elif not any(x[6] in('A','B') for x in rows): rows[0][8]='KHÔNG VÀO (trận không có kèo tier B) • '+rows[0][8]
    A+=rows
    R.append([46353,m['lab'],f"{rname} ({rc}) • đã xác nhận (UEFA)","FotMob 12 tháng",rm,ryc,ravg,rred,round(rfo,1) if rfo else '–',rv,
        ('Thấp hơn' if rdir<0 else 'Cao hơn' if rdir>0 else 'Gần')+f" TB giải ({lg(ryc)} so với {lg(ravg)}) → "+('nghiêng Xỉu thẻ.' if rdir<0 else 'nghiêng Tài thẻ.' if rdir>0 else ('mẫu trọng tài mỏng, không dùng để nâng tier.' if rm<10 else 'trung tính.'))])
json.dump(dict(A=A,B=B,R=R),open('el/rows2.json','w'),ensure_ascii=False)
for x in A:
    if x[6]!='C' or x[8].startswith('KHÔNG'): print(x[6],x[1][:28],'|',x[8][:110])
