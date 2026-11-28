"""BƯỚC 4 – CHẤM KẾT QUẢ SAU TRẬN + RR + RÀ SOÁT MỤC 26 + ỨNG VIÊN BÀI HỌC (mục 0k(1)).
  python3 -B khuon/ket_qua.py --ngay 2026-11-29 [--giai PL,LL]
Đọc results/engine_<dd-mm>.json (do khuon/chay.py tạo), lấy kết quả FotMob, chấm từng kèo (mục 13, 17), tính RR theo nhóm (thẻ riêng – mục 29),
z theo mục 26, và liệt kê ỨNG VIÊN BÀI HỌC (nhóm |z| ≥ 1,5; kèo Ưu tiên/TOP thua) để rút bài học theo mục 0k(1).
Đầu ra: results/ket_qua_<dd-mm>.json và results/ke_hoach_ket_qua_<dd-mm>.json (cột AZ 'Thực tế', BA 'Kết quả')."""
import json,os,sys,math,argparse,datetime as dt
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0,ROOT); sys.dont_write_bytecode=True
from khuon import fotmob as FM
from khuon.giai import GIAI
from corner_style import stats_of,_num
ap=argparse.ArgumentParser(); ap.add_argument('--ngay',required=True); ap.add_argument('--giai'); ap.add_argument('--ma-tep')
a=ap.parse_args(); DK=a.ma_tep or dt.date.fromisoformat(a.ngay).strftime('%d-%m')
E=json.load(open(f'results/engine_{DK}.json'))
if a.giai: E=[b for b in E if b['tab'] in a.giai.split(',')]
def so_lieu(fid):
    d=FM.tran(fid,True); h=d['header']
    if not h['status'].get('finished'): return None
    c=d['content']; S=stats_of(c); S1=stats_of(c,'FirstHalf'); n=lambda v:int(_num(v) or 0)
    ft=[t['score'] for t in h['teams']]
    ev=c['matchFacts']['events']['events']
    h1=[0,0]
    for e in ev:
        if e.get('type')=='Goal' and (e.get('time') or 99)<=45: h1[0 if e.get('isHome') else 1]+=1
    cor=S.get('corners'); c1=S1.get('corners'); yc=S.get('yellow_cards') or [0,0]; rc=S.get('red_cards') or [0,0]
    if cor is None: return dict(ft=ft,h1=h1,thieu=True)
    return dict(ft=ft,h1=h1,cor=[n(cor[0]),n(cor[1])],cor_h1=(n(c1[0])+n(c1[1])) if c1 else None,yc=[n(yc[0]),n(yc[1])],rc=[n(rc[0]),n(rc[1])])
def settle(v):
    if v>0.25+1e-9: return 'Thắng'
    if abs(v-0.25)<1e-9: return 'Thắng nửa'
    if abs(v)<1e-9: return 'Hoàn'
    if abs(v+0.25)<1e-9: return 'Thua nửa'
    return 'Thua'
RRv={'Thắng':lambda o:o-1,'Thắng nửa':lambda o:(o-1)/2,'Hoàn':lambda o:0,'Thua nửa':lambda o:-0.5,'Thua':lambda o:-1}
SL={}; OUT=[]
for b in E:
    fid=b['mid'][len(b['tab']):]
    if fid not in SL: SL[fid]=so_lieu(fid)
    r=SL[fid]
    if not r or r.get('thieu') or (b['mk']=='h1' and r.get('cor_h1') is None): OUT.append(dict(b,res='Chờ số liệu',rr=None,az='')); continue
    gh,ga=r['ft']; ch,ca=r['cor']; cards=sum(r['yc'])+2*sum(r['rc']); L=b['line']; sd=b['side']
    if b['mk'] in('hc','chc'):
        m=(gh-ga) if b['mk']=='hc' else (ch-ca); v=(m+L) if sd==0 else (-m-L)
    else:
        k={'tot':gh+ga,'cor':ch+ca,'h1':r['cor_h1'],'card':cards}[b['mk']]; v=(k-L) if sd==0 else (L-k)
    res=settle(v) if b['odds'] else 'Không có giá'
    az=f"H1 {r['h1'][0]}–{r['h1'][1]} | FT {gh}–{ga} | Góc H1 {r['cor_h1']} | Góc FT {ch}–{ca} = {ch+ca} | Vàng {r['yc'][0]}–{r['yc'][1]} = {cards} thẻ (quy đổi {r['yc'][0]+2*r['rc'][0]}–{r['yc'][1]+2*r['rc'][1]}) | Đỏ {sum(r['rc'])}"
    OUT.append(dict(b,res=res,rr=RRv[res](b['odds']) if b['odds'] else None,az=az,pe=((b['ev']+1)/b['odds']) if (b['odds'] and b['ev'] is not None) else None))
def grp(L):
    L=[o for o in L if o['rr'] is not None]
    if not L: return None
    rr=sum(o['rr'] for o in L); ev=sum(o['ev'] for o in L if o['ev'] is not None)
    var=sum(o['pe']*(o['odds']-1)**2+(1-o['pe'])-o['ev']**2 for o in L if o.get('pe') is not None)
    sd=math.sqrt(var) if var>0 else 0
    return dict(n=len(L),thang=sum(o['res'].startswith('Thắng') for o in L),thua=sum(o['res'].startswith('Thua') for o in L),hoan=sum(o['res']=='Hoàn' for o in L),
                rr=round(rr,2),roi=round(rr/len(L)*100,1),ky_vong=round(ev,2),sd=round(sd,2),z=round((rr-ev)/sd,2) if sd else 0)
nc=[o for o in OUT if o['mk']!='card']
G={'Toàn bộ (trừ thẻ)':grp(nc),'Ưu tiên':grp([o for o in nc if o.get('pri')]),'Không ưu tiên':grp([o for o in nc if not o.get('pri')]),'TOP':grp([o for o in nc if o.get('top')])}
for t in('A','B','C+','C'): G['Tier '+t]=grp([o for o in nc if o['t']==t])
for mk,nm in(('hc','Chấp bàn'),('tot','Tài/Xỉu bàn'),('cor','Góc FT'),('h1','Góc H1'),('chc','Chấp góc FT')): G[nm]=grp([o for o in nc if o['mk']==mk])
G['Thẻ (RR riêng)']=grp([o for o in OUT if o['mk']=='card'])
UV=[f"nhóm {k}: z {v['z']:+.2f} (RR {v['rr']:+.2f}, kỳ vọng {v['ky_vong']:+.2f}) → BẮT BUỘC tìm nguyên nhân (mục 26b)" for k,v in G.items() if v and abs(v['z'])>=1.5]
UV+=[f"{o['tab']}{o['row']} {o['lab']} – {o['mk']} {o['res']} ({'TOP' if o.get('top') else 'Ưu tiên '+str(o['pri'])}, tier {o['t']}) → xem lại cờ đội hình/lối đá/giá đi ngược/diễn biến (mục 26e)"
     for o in OUT if (o.get('pri') or o.get('top')) and o['res'].startswith('Thua')]
json.dump(dict(ngay=a.ngay,keo=OUT,nhom=G,ung_vien_bai_hoc=UV),open(f'results/ket_qua_{DK}.json','w'),ensure_ascii=False,default=str)
PLAN=[]
for o in OUT:
    if o['res']=='Chờ số liệu': continue
    PLAN.append(dict(range=f"'{GIAI[o['tab']]['tab']}'!AZ{o['row']}:BA{o['row']}",values=[[o['az'],o['res'] if o['res']!='Không có giá' else '']]))
json.dump(PLAN,open(f'results/ke_hoach_ket_qua_{DK}.json','w'),ensure_ascii=False)
cho=sorted({o['lab'] for o in OUT if o['res']=='Chờ số liệu'})
print(f"Đã chấm {len(OUT)-sum(o['res']=='Chờ số liệu' for o in OUT)}/{len(OUT)} kèo • kế hoạch ghi {len(PLAN)} ô → results/ke_hoach_ket_qua_{DK}.json")
if cho: print('Chờ số liệu (đặt lịch kiểm lại):',cho)
for k,v in G.items():
    if v: print(f"{k:22s} {v['thang']}T-{v['thua']}B-{v['hoan']}H n={v['n']} RR {v['rr']:+.2f} ROI {v['roi']:+.1f}% | kỳ vọng {v['ky_vong']:+.2f} z {v['z']:+.2f}")
print('ỨNG VIÊN BÀI HỌC:' if UV else 'Không có ứng viên bài học (dao động bình thường).'); [print(' -',u) for u in UV]
