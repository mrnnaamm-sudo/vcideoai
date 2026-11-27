import json,sys
sys.path.insert(0,'.')
from corner_style import stats_of,_num
DAY=sys.argv[1]; dk=DAY.replace('/','-'); SER={'28/11':46354,'29/11':46355}[DAY]
D=json.load(open(f'j1/res_{dk}.json')); S=json.load(open(f'j1/sheet_{dk}.json'))
def pair(St,k,i,j):
    v=St.get(k); return (_num(v[i]),_num(v[j])) if v else (None,None)
def n(x): return '' if x is None else (int(x) if float(x).is_integer() else str(x).replace('.',','))
F=[]
for r in D['RES']:
    lab=f"{r['time']} • {r['hn']} (Nhà) – {r['an']} (Khách)"
    for tid,nm,R in ((r['h'],r['hn'],r['H']),(r['a'],r['an'],r['A'])):
        for q in R:
            d=json.load(open(f"j1/fm/m_{q['mid']}.json")); c=d['content']; home=q['home']; i,j=(0,1) if home else (1,0)
            A=stats_of(c); H1=stats_of(c,'FirstHalf')
            c1=pair(H1,'corners',i,j); cf=pair(A,'corners',i,j); y=pair(A,'yellow_cards',i,j); rd=pair(A,'red_cards',i,j)
            sh=pair(A,'total_shots',i,j); so=pair(A,'ShotsOnTarget',i,j); fo=pair(A,'fouls',i,j); sv=pair(A,'keeper_saves',i,j)
            c1t=(c1[0]+c1[1]) if c1[0] is not None else None; cft=(cf[0]+cf[1]) if cf[0] is not None else None
            ry=(rd[0] or 0,rd[1] or 0)
            F.append([SER,f"{nm} • {r['hn']} (Nhà) – {r['an']} (Khách)",q['date'],q['opp'],'Nhà' if home else 'Khách','J1 League',
              'Thắng' if q['gf']>q['ga'] else ('Hòa' if q['gf']==q['ga'] else 'Thua'),
              f"{q['ht'][0]}–{q['ht'][1]}" if q['ht'] else '',f"{q['gf']}–{q['ga']}",n(c1t),n(cft-c1t if (cft is not None and c1t is not None) else None),n(cft),n(cf[0]),n(cf[1]),
              n(y[0]),n(y[1]),n((y[0] or 0)+(y[1] or 0)) if y[0] is not None else '',n(ry[0]),n(ry[1]),n((y[0] or 0)+(y[1] or 0)+2*(ry[0]+ry[1])) if y[0] is not None else '',
              n(q['poss']),f"{n(sh[0])}–{n(sh[1])}" if sh[0] is not None else '',f"{n(so[0])}–{n(so[1])}" if so[0] is not None else '',
              f"{n(fo[0])}–{n(fo[1])}" if fo[0] is not None else '',f"{n(sv[0])}–{n(sv[1])}" if sv[0] is not None else '','FotMob'])
        # dòng TB
        rows=[x for x in F if x[1].startswith(nm+' •')][-len(R):]
        def avg(ix):
            v=[float(str(x[ix]).replace(',','.')) for x in rows if x[ix]!='']; return (f"{sum(v)/len(v):.1f}".replace('.',',')) if v else ''
        gf=sum(q['gf'] for q in R)/len(R); ga=sum(q['ga'] for q in R)/len(R)
        F.append([SER,f"{nm} • {r['hn']} (Nhà) – {r['an']} (Khách)",'TB 10 trận','','','','',''
                  ,f"{gf:.1f}–{ga:.1f}".replace('.',','),avg(9),avg(10),avg(11),avg(12),avg(13),avg(14),avg(15),avg(16),avg(17),avg(18),avg(19),avg(20),'','','','','FotMob'])
S['FORM']=F; json.dump(S,open(f'j1/sheet_{dk}.json','w'),ensure_ascii=False); print(len(F)); print(F[0]); print(F[10])
