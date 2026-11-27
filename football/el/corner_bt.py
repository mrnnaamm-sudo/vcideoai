# Backtest mục 28 trên 18 trận EL 27/11: kỳ vọng góc theo lối đá + cờ so với góc thực tế và cửa đã chọn
import json,sys,os
sys.path.insert(0,'.')
from corner_style import *
SP='/tmp/claude-0/-home-user/bc9353a1-6091-5ff6-82cc-896d2667346b/scratchpad'
fx=json.load(open('el/fm/fx.json')); out=json.load(open('el/out2.json'))
sel=json.load(open(SP+'/xg/selel.json')); kq=json.load(open('results/el_27-11_ketqua.json'))
ay=json.load(open('results/el_27-11_AY.json'))
res3=json.load(open('el/res3.json'))
def rows(t):
    R=[]
    for mid,*_ in sel.get(t,[]):
        p=f'{SP}/xg/m_{mid}.json'
        if os.path.exists(p):
            x=match_row(p,t)
            if x: R.append(x)
    return R
B=[]
for k,(f,o) in enumerate(zip(fx,out)):
    RH,RA=rows(f['h']),rows(f['a'])
    if len(RH)<5 or len(RA)<5: print('thiếu',f['hn'],f['an'],len(RH),len(RA)); continue
    PH,PA=profile_venue(RH,True),profile_venue(RA,False); m=matchup(PH,PA)
    r=kq.get(f['id']); act=sum(r['cor']) if r and r.get('cor') else None
    a1=sum(r['c1']) if r and r.get('c1') else None
    cf=[x for x in o['res'] if x['k'] in('cor','h1')]
    for x in cf:
        B.append(dict(m=f"{f['hn']}-{f['an']}",k=x['k'],cua=x['cua'],line=x['line'][0],E=m['tot'] if x['k']=='cor' else m['h1'],act=act if x['k']=='cor' else a1,fl=flags(PH,PA,m,f['hn'],f['an'])))
json.dump(B,open('results/corner_style_backtest_EL27.json','w'),ensure_ascii=False,indent=0)
for b in B: print(b['k'],b['m'][:34].ljust(34),b['cua'][:22].ljust(22),'mốc',b['line'],'E %.1f'%b['E'],'TT',b['act'],'|',' ; '.join(z[:60] for z in b['fl']))
