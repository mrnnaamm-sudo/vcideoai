import json,sys
sys.path.insert(0,'.')
from model import tier,tier_old
from gen3 import best,line_text
R=json.load(open('d28/res3.json'))
MK=['hc','tot','cor','h1','card']
FORCE_C={('PL',155):'Coventry vắng 7 người (gồm 2 tiền đạo Wright, Awoniyi) và mẫu có trận thua −5 → không theo cửa Coventry (mục 7, 14)',
 ('PL',154):'trọng tài Andy Madley NHẸ TAY (3,45 vàng/trận, TB giải 3,87) phản bác Tài (mục 5)',
 ('PL',164):'mẫu 50% < 70%, trọng tài Robert Jones trung bình; Tài thẻ giá cao 2,30 (bài học mục 14)',
 ('BL',151):'Gladbach vắng Kleindienst, Bremen vắng Grüll + 4 người (bài học Gala–Villa)',
 ('BL',169):'mẫu 60% < 70% (mục 5); trọng tài Dankert nhẹ tay, trận chênh lệch (Elo 1673–2041, hệ số 0,92) cùng chiều Xỉu → chỉ ghi lưu ý',
 ('BL',174):'trọng tài Timo Gerach lệch < 0,5 vàng/trận, 4 thẻ đỏ/13 trận phản bác Xỉu (mục 5)',
 ('BL',164):'trọng tài Sören Storks CHẶT TAY phản bác Xỉu (mục 5)'}
NOTE={('BL',165):'bỏ hạ C theo bài học PSV từ 27/11 (5/5 kèo cửa dưới bị hạ C ở EL 27/11 đều thắng – mục 14); Bayern đá C1 3 ngày trước, Pokal 3 ngày sau (mục 23, nguy cơ xoay tua), vắng Kane, Olise; đội hình giả định Bayern tấn công 0,92 (mục 27); HSV có 2 trận thua −5 trong mẫu → chỉ lưu ý',('PL',156):'Coventry mất 2 tiền đạo chính → ủng hộ Xỉu',('PL',160):'MU đá C1 3 ngày trước (mục 23), Elo hai đội ngang nhau (1845–1856)',
 ('LL',161):'Athletic vắng 2 tiền đạo Guruzeta, Sannadi',('BL',160):'Köln vắng Dallinga, Skhiri; 3 ngày sau Köln đá Pokal (mục 23)',
 ('BL',170):'tay chấp +1 < 1,5 nên không áp bài học PSV',('BL',171):'Mainz TB 4,1 bàn, Union lọt xG 2,38/trận',('LL',155):'Betis vừa đá C1 4 ngày trước (mục 23)',
 ('BL',162):'Köln TB 10,6 góc, Elversberg 11,6 góc'}
TIME={'PL':{150:'03:00',155:'22:00',160:'22:00'},'LL':{150:'03:00',155:'20:00',160:'22:15'},'BL':{150:'02:30',155:'21:30',160:'21:30',165:'21:30',170:'21:30'}}
TR={'A':0,'B':1}
OUT={}
for m in R:
    tab=m['tab']; rows=[]
    for i,mk in enumerate(MK):
        r=m['row']+i; x=m['ev'].get(mk); s=best(x)
        c,base=line_text(mk,x,s,m['hn'],m['an'],m['kv'])
        t=tier(s,mk); to=tier_old(s,mk)
        if t=='B?': t='B' if (tab,r)==('PL',158) else 'C'
        if to=='B?': to='B' if (tab,r)==('PL',158) else 'C'
        if mk=='card' and t in('A','B'): t='C'
        why=FORCE_C.get((tab,r))
        if why: t='C'; to='C'
        rows.append(dict(r=r,t=t,to=to,base=base,why=why,s=s,mk=mk))
    OUT.setdefault(tab,[]).append(rows)
# priorities per match
for tab,ms in OUT.items():
    for rows in ms:
        cand=[x for x in rows if x['t'] in('A','B')]
        cand.sort(key=lambda x:(TR[x['t']],-(x['s']['ev'] if x['s']['ev'] is not None else 0.05)))
        for k,x in enumerate(cand[:2]): x['pri']=k+1
        for x in cand[2:]: x['pri']=None; x['dp']=True
    # TOP per slot
    slots={}
    for rows in ms:
        for x in rows:
            if x.get('pri') and x['s']['odds']: slots.setdefault(TIME[tab][rows[0]['r']],[]).append(x)
    for sl,c in slots.items():
        c.sort(key=lambda x:(TR[x['t']],-x['s']['ev']))
        if len(c)>1 and c[0]['t']==c[1]['t'] and c[1]['mk'] in('cor','h1') and c[0]['mk'] not in('cor','h1') and c[0]['s']['ev']-c[1]['s']['ev']<=0.02: c[0],c[1]=c[1],c[0]
        for k,x in enumerate(c[:2]): x['top']=f"★ TOP {k+1} khung {sl}"
res={}
for tab,ms in OUT.items():
    for rows in ms:
        hasB=any(x['t'] in('A','B') for x in rows); hasCp=any(x['t']=='C+' for x in rows)
        for k,x in enumerate(rows):
            s=x['s']; old=f" • [Thử mục 8 (a)(b); tier cách cũ: {x['to']}]"
            if x['t'] in('A','B'):
                pre=' • '.join(p for p in (f"Ưu tiên {x['pri']}" if x.get('pri') else '', x.get('top','')) if p)
                txt=(pre+' • ' if pre else '')+x['base']+(' • '+NOTE[(tab,x['r'])] if (tab,x['r']) in NOTE else '')+(' • tier B dự phòng (trận đã đủ 2 ưu tiên)' if x.get('dp') else '')+old+'.'
            elif x['t']=='C+':
                txt=f"C+ • ½R • {x['base']} • mẫu (co về thị trường) {s['psa']*100:.0f}%, mô hình cùng chiều, giá ≥ 1,65 (mục 18b){old}."
            else:
                if x['why']: rs=x['why']
                elif s['odds'] is None: rs='chờ giá; mẫu/mô hình chưa đủ (B chờ giá cần mẫu ≥ 65% và mô hình ≥ 58%)'
                elif s['evm'] is not None and s['evm']<=0: rs='mô hình ngược chiều'
                elif s['pf'] and s['ps']<=s['pf']: rs='mẫu không nghiêng hơn thị trường'
                else: rs='không đủ lợi thế (EV < 2–5% sau khi co mẫu về thị trường)'
                txt=f"{x['base']} • {rs} • C • không vào{old}."
            if k==0 and not hasB: txt=('Trận không có tier B, chỉ có C+ ½R • ' if hasCp else 'KHÔNG VÀO (trận không có kèo tier B) • ')+txt
            res.setdefault(tab,[]).append((x['r'],x['t'],x['to'],txt))
json.dump(res,open('d28/out_v2.json','w'),ensure_ascii=False)
for tab,v in res.items():
    for r,t,to,txt in v:
        if t!='C' or to!='C': print(tab,r,t,'(cũ',to,')',txt[:120])
