"""KHỐI PHONG ĐỘ 10 TRẬN (cột BP:CS của tab, công thức L5 lọc theo $B$1) – cùng định dạng j1/form.py.
python3 -B khuon/phong_do.py <mã giải> <YYYY-MM-DD> <tệp ra>
Mỗi đội: 10 dòng trận mẫu (mục 1–2, như bộ máy dùng) + 1 dòng 'TB 10 trận'."""
import json,sys,os,datetime as dt
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from khuon import nap, fotmob as FM
from corner_style import stats_of,_num
def pair(St,k,i,j):
    v=St.get(k); return (_num(v[i]),_num(v[j])) if v else (None,None)
def n(x): return '' if x is None else (int(x) if float(x).is_integer() else str(x).replace('.',','))
def ht_of(c,home):
    try:
        ev=c['matchFacts']['events']['events']
        gl=[e for e in ev if e.get('type')=='Goal' and ((e.get('time') or 0)<=45 or str(e.get('timeStr','')).startswith('45+'))]
        hh=sum(1 for e in gl if e.get('isHome')); aa=len(gl)-hh; return (hh,aa) if home else (aa,hh)
    except Exception: return None
def main(ma,ngay,out):
    d0=dt.date.fromisoformat(ngay); SER=(d0-dt.date(1899,12,30)).days
    F=[]
    for m in nap.nap_ngay(ma,ngay):
        for nm,R in ((m['hn'],m['H']),(m['an'],m['A'])):
            lab=f"{nm} • {m['hn']} (Nhà) – {m['an']} (Khách)"; rows=[]
            for q in R:
                d=FM.tran(q['mid'],True); c=d['content']; home=q['home']; i,j=(0,1) if home else (1,0)
                A=stats_of(c); H1=stats_of(c,'FirstHalf')
                c1=pair(H1,'corners',i,j); cf=pair(A,'corners',i,j); y=pair(A,'yellow_cards',i,j); rd=pair(A,'red_cards',i,j)
                sh=pair(A,'total_shots',i,j); so=pair(A,'ShotsOnTarget',i,j); fo=pair(A,'fouls',i,j); sv=pair(A,'keeper_saves',i,j)
                po=pair(A,'BallPossesion',i,j)[0]; ht=ht_of(c,home)
                c1t=(c1[0]+c1[1]) if c1[0] is not None else None; cft=(cf[0]+cf[1]) if cf[0] is not None else None
                ry=(rd[0] or 0,rd[1] or 0)
                rows.append([SER,lab,q['date'],q['opp'],'Nhà' if home else 'Khách','ACL Elite' if q.get('acl') else q['lg'] if q['lg']!='J1' else 'J1 League',
                  'Thắng' if q['gf']>q['ga'] else ('Hòa' if q['gf']==q['ga'] else 'Thua'),
                  f"{ht[0]}–{ht[1]}" if ht else '',f"{q['gf']}–{q['ga']}",n(c1t),n(cft-c1t if (cft is not None and c1t is not None) else None),n(cft),n(cf[0]),n(cf[1]),
                  n(y[0]),n(y[1]),n((y[0] or 0)+(y[1] or 0)) if y[0] is not None else '',n(ry[0]),n(ry[1]),n((y[0] or 0)+(y[1] or 0)+2*(ry[0]+ry[1])) if y[0] is not None else '',
                  n(po),f"{n(sh[0])}–{n(sh[1])}" if sh[0] is not None else '',f"{n(so[0])}–{n(so[1])}" if so[0] is not None else '',
                  f"{n(fo[0])}–{n(fo[1])}" if fo[0] is not None else '',f"{n(sv[0])}–{n(sv[1])}" if sv[0] is not None else '','FotMob'])
            def avg(ix):
                v=[float(str(x[ix]).replace(',','.')) for x in rows if x[ix]!='']; return (f"{sum(v)/len(v):.1f}".replace('.',',')) if v else ''
            gf=sum(q['gf'] for q in R)/len(R); ga=sum(q['ga'] for q in R)/len(R)
            F+=rows+[[SER,lab,f'TB {len(R)} trận','','','','','',f"{gf:.1f}–{ga:.1f}".replace('.',','),*[avg(k) for k in range(9,21)],'','','','','FotMob']]
    json.dump(F,open(out,'w'),ensure_ascii=False); print(len(F),'dòng →',out)
if __name__=='__main__': main(*sys.argv[1:])
