import json,sys
sys.path.insert(0,'.')
from model import *
AN=json.load(open('el/an.json')); fx=json.load(open('el/fm/fx.json')); O=json.load(open('el/out2.json'))
E=json.load(open('elo/elo_all.json')); MP=json.load(open('elo/map.json')); XG=json.load(open('xg/xgel.json'))
CN={'Czech Republic':'Czechia'}
def num(x): return x if isinstance(x,(int,float)) else None
def recs(tid):
    out=[]
    for v in AN[tid]['vals']:
        r=v['row']
        out.append(dict(gf=v['gf'],ga=v['ga'],home=v['home'],h1=num(r[7]),cor=num(r[9]),cf=num(r[10]),ca=num(r[11]),cards=num(r[17])))
    return out
RES=[]
for fi,f in enumerate(fx):
    o=O[fi]; h,a=f['h'],f['a']; hn,an=AN[h]['name'],AN[a]['name']
    H,A=recs(h),recs(a)
    eh=E.get(MP.get(hn)); ea=E.get(MP.get(an))
    ch=COEF.get(CN.get(eh[0],eh[0])) if eh else None; ca_=COEF.get(CN.get(ea[0],ea[0])) if ea else None
    r=o['ref']; ref=dict(name=r[0],rm=r[2],ryc=r[3],ravg=r[4])
    od={}
    for x in o['res']:
        L=x['line']
        if x['k']=='hc': od['hc']=(L[0],L[2],L[4])
        else: od[x['k']]=(L[0],L[2],L[4])
    gap=abs((eh[1] if eh else 1600)-(ea[1] if ea else 1600))
    char=0.92 if gap>=250 else 1.0
    kv,ev=evaluate(H,A,od,ref,(eh[1] if eh else None,ea[1] if ea else None),(ch,ca_),(XG.get(h),XG.get(a)),char)
    RES.append(dict(fi=fi,hn=hn,an=an,elo=(eh,ea),coef=(ch,ca_),kv=kv,ev=ev,od=od,ref=ref,xg=(XG.get(h),XG.get(a))))
json.dump(RES,open('el/res3.json','w'),ensure_ascii=False,default=str)
