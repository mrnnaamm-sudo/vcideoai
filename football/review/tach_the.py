"""Rà soát lại RR tuần 23–29/11: tách kèo thẻ khỏi khung RR chung (mục 29)."""
import json,sys,difflib
sys.path.insert(0,'review'); from the_data import M
E=json.load(open('elo/elo_all.json')); MP=json.load(open('elo/map.json'))
FIX={'Slovan Bratislava':1580,'Sabah':1480,'Union SG':1720,'Club Brugge':'Brugge','Inter':'Internazionale','Bayern':'Bayern München','PSG':'Paris SG','NEC':'Nijmegen'}
def elo(t):
    f=FIX.get(t)
    if isinstance(f,int): return f
    k=f or MP.get(t) or (t if t in E else difflib.get_close_matches(t,list(E),1,0.5)[0])
    return E[k][1]
def pl(x):
    o=x['odds'];r=x['res']
    return {'W':o-1,'HW':(o-1)/2,'H':0,'HL':-0.5,'L':-1}[r]
def mkt(k):
    k=k.lower()
    return 'thẻ' if 'thẻ' in k else 'góc H1' if 'góc h1' in k else 'góc FT' if 'góc' in k else 'bàn' if 'bàn' in k else 'chấp'
def kind(eh,ea):
    g=abs(eh+65-ea)
    big=eh>=1800 and ea>=1800
    cls='cân bằng (<100)' if g<100 else 'chênh vừa (100–199)' if g<200 else 'quá lệch (≥200)'
    return g,big,cls
R=[]
for c,d,h,a,L in M:
    eh,ea=elo(h),elo(a); g,big,cls=kind(eh,ea)
    for x in L:
        R.append(dict(c=c,d=d,m=f'{h}–{a}',eh=eh,ea=ea,gap=g,big=big,cls=cls,mk=mkt(x['keo']),pl=pl(x),**x))
def agg(lbl,S):
    w=sum(1 for x in S if x['res'] in('W','HW'));l=sum(1 for x in S if x['res'] in('L','HL'));h=sum(1 for x in S if x['res']=='H')
    n=len(S);s=sum(x['pl'] for x in S)
    return [lbl,w,l,h,n,round(s,2),round(100*s/n,1) if n else '']
nt=[x for x in R if x['mk']!='thẻ']; th=[x for x in R if x['mk']=='thẻ']
B=lambda x:x['tier'] in('A','B')
T={}
T['old']=[agg('★ TOP khung giờ',[x for x in R if x['top']]),agg('2 kèo ưu tiên (B trở lên)',[x for x in R if x['pr'] and B(x)]),
          agg('Tier A',[x for x in R if x['tier']=='A']),agg('Tier B',[x for x in R if x['tier']=='B']),agg('Tier C',[x for x in R if x['tier']=='C']),agg('Toàn bộ kèo',R)]
T['new']=[agg('★ TOP khung giờ',[x for x in nt if x['top']]),agg('2 kèo ưu tiên (B trở lên)',[x for x in nt if x['pr'] and B(x)]),
          agg('Kèo không ưu tiên',[x for x in nt if not (x['pr'] and B(x))]),
          agg('Tier A',[x for x in nt if x['tier']=='A']),agg('Tier B',[x for x in nt if x['tier']=='B']),agg('Tier C',[x for x in nt if x['tier']=='C']),
          agg('Toàn bộ (trừ thẻ)',nt)]
T['mk']=[agg(m,[x for x in nt if x['mk']==m]) for m in ('chấp','bàn','góc FT','góc H1')]
T['mkB']=[agg(m+' (A/B)',[x for x in nt if x['mk']==m and B(x)]) for m in ('chấp','bàn','góc FT','góc H1')]
T['the']=[agg('KÈO THẺ • toàn bộ',th),agg('Thẻ tier A/B',[x for x in th if B(x)]),agg('Thẻ tier C',[x for x in th if x['tier']=='C']),
          agg('Thẻ từng làm Ưu tiên/TOP',[x for x in th if x['pr'] or x['top']]),
          agg('Tài thẻ',[x for x in th if x['keo'].startswith('Tài')]),agg('Xỉu thẻ',[x for x in th if x['keo'].startswith('Xỉu')])]
T['the_cls']=[agg('Thẻ • '+k,[x for x in th if x['cls']==k]) for k in ('cân bằng (<100)','chênh vừa (100–199)','quá lệch (≥200)')]+[agg('Thẻ • trận lớn (2 đội ≥1800)',[x for x in th if x['big']])]
T['the_cls_side']=[agg(f'{s} thẻ • {k}',[x for x in th if x['cls']==k and x['keo'].startswith(s)]) for k in ('cân bằng (<100)','chênh vừa (100–199)','quá lệch (≥200)') for s in ('Tài','Xỉu')]
T['day']=[]
for d in ('25/11','26/11','27/11'):
    S=[x for x in nt if x['d']==d]
    T['day']+= [agg(d+' • tổng (trừ thẻ)',S),agg(d+' • ưu tiên B+ (trừ thẻ)',[x for x in S if x['pr'] and B(x)]),agg(d+' • thẻ (RR riêng)',[x for x in th if x['d']==d])]
T['cards']=[[x['d'],x['m'],x['keo'],x['odds'],x['tier'],x['res'],x['gap'],x['cls'],x['big']] for x in th]
json.dump(T,open('results/rr_tuan_23-29_tach_the.json','w'),ensure_ascii=False,indent=0)
for k,v in T.items():
    if k=='cards': continue
    print('==',k)
    for r in v: print('  ',r)
