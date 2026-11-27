"""Chạy mục 28 cho một danh sách trận: python3 corner_run.py <fixtures.json> <sel.json> <matchdir> <out.json>
fixtures: [[key, tên nhà, id nhà, tên khách, id khách], ...]; sel: {team_id: [[match_id, ngày, giải, sân nhà?], ...]}"""
import json,sys,os
from corner_style import *
fxf,self_,md,outf=sys.argv[1:5]
FX=json.load(open(fxf)); sel=json.load(open(self_))
def rows(t):
    R=[]
    for mid,*_ in sel.get(str(t),[]):
        p=f'{md}/m_{mid}.json'
        if os.path.exists(p):
            x=match_row(p,str(t))
            if x: R.append(x)
    return R
OUT={}
for key,hn,h,an,a in FX:
    RH,RA=rows(h),rows(a)
    PH,PA=profile_venue(RH,True),profile_venue(RA,False); m=matchup(PH,PA)
    F=flags(PH,PA,m,hn,an)
    OUT[key]=dict(hn=hn,an=an,PH=PH,PA=PA,m=m,fl=F,txt=summary(hn,an,PH,PA,m),
                  v_tai=verdict_flags('Tài',F)[0],v_xiu=verdict_flags('Xỉu',F)[0])
json.dump(OUT,open(outf,'w'),ensure_ascii=False,indent=0)
for k,o in OUT.items(): print(k,'|',o['txt'],'| Tài:',o['v_tai'],'Xỉu:',o['v_xiu']); print()
