"""KIỂM CHI TIẾT QUY TẮC LỆCH THỊ TRƯỜNG (mục 8, áp từ 28/11 10:40 – A1 7fd416a771fb).
Quy tắc A1: lệch = xác suất ước tính − xác suất công bằng nhà cái; kèo đạt A/B mà lệch > 8 điểm → tối đa C+,
không Ưu tiên/TOP; tier A cần lệch ≤ 8 điểm.

python3 -B rules/kiem_lech_tt.py [results/engine_*.json ...] [--kq kq.json]
  kq.json (tùy chọn) = {"<tab>:<dòng>": "Thắng|Thua|Hoàn|Thắng nửa|Thua nửa"} để tính RR từng nhóm.
Chỉ đọc, không sửa gì. Lỗi chấm → in 'SAI' kèm kèo; không lỗi → 'ĐÚNG'."""
import json,sys,glob,re,datetime as dt
AP=dt.datetime(2026,11,28,10,40)          # thời điểm áp quy tắc (giờ VN)
NG=0.08
args=[a for a in sys.argv[1:] if not a.startswith('--')]
kq=json.load(open(sys.argv[sys.argv.index('--kq')+1])) if '--kq' in sys.argv else {}
if kq: args=[a for a in args if a!=sys.argv[sys.argv.index('--kq')+1]]
files=args or sorted(glob.glob('results/engine_*.json'))
def rr(r,o):
    return {'Thắng':o-1,'Thắng nửa':(o-1)/2,'Hoàn':0,'Thua nửa':-0.5,'Thua':-1}.get(r)
err=[];rows=[];truoc=0
for f in files:
    m=re.search(r'engine_(\d\d)-(\d\d)',f)
    if not m: continue
    d,mo=int(m.group(1)),int(m.group(2))
    for o in json.load(open(f)):
        if o['mk']=='card' or not o.get('odds') or not o.get('pf'): continue
        hh,mm=map(int,o['time'].split(':')); ko=dt.datetime(2026,mo,d,hh,mm)
        tag=f"{o['tab']}{o['row']} {o['lab']} • {o['mk']} @{o['odds']}"
        # (1) xác suất công bằng tính lại từ giá hai cửa
        od=[s['odds'] for s in o['sides']]; oo=od[1-o['side']]
        if oo:
            pf2=(1/o['odds'])/(1/o['odds']+1/oo)
            if abs(pf2-o['pf'])>1e-6: err.append(f"{tag}: xác suất công bằng lưu {o['pf']:.4f} ≠ tính lại {pf2:.4f}")
        pe=(o['ev']+1)/o['odds']; gap=pe-o['pf']
        pre=next((k.replace('tier ','') for mm_,k,dd in o['steps'] if mm_=='8' and k.startswith('tier ')),None)
        cap=any(mm_=='8' and dd=='C+' and 'lệch thị trường' in k for mm_,k,dd in o['steps'])
        rows.append(dict(tag=tag,key=f"{o['tab']}:{o['row']}",odds=o['odds'],gap=gap,pre=pre,t=o['t'],cap=cap,pri=o.get('pri'),top=o.get('top'),truoc=ko<AP))
        if ko<AP: truoc+=1; continue          # kèo đã chốt/đã đá trước khi áp: giữ nguyên, không tính lỗi
        if pre in('A','B') and gap>NG and not cap: err.append(f"{tag}: lệch {gap*100:.1f} > 8 nhưng KHÔNG bị chặn (tier {o['t']})")
        if cap and gap<=NG: err.append(f"{tag}: lệch {gap*100:.1f} ≤ 8 nhưng bị chặn")
        if cap and (o['t'] not in('C+','C') or o.get('pri') or o.get('top')): err.append(f"{tag}: bị chặn mà vẫn tier {o['t']} / Ưu tiên {o.get('pri')} / {o.get('top')}")
        if cap and not any(f"{gap*100:.1f} điểm" in n for n in o['notes']): err.append(f"{tag}: ghi chú mục 8 thiếu hoặc sai số điểm lệch ({gap*100:.1f})")
        if o['t']=='A' and gap>NG: err.append(f"{tag}: tier A mà lệch {gap*100:.1f} > 8")
sau=[r for r in rows if not r['truoc']]
print(f"Đã kiểm {len(rows)} kèo có giá hai cửa ({len(sau)} sau khi áp, {truoc} trước khi áp – giữ nguyên).")
print('Nhóm: bị chặn', sum(r['cap'] for r in sau), '• A/B giữ (lệch ≤ 8)', sum(r['t'] in('A','B') for r in sau),
      '• sát ngưỡng 6–8 điểm', sum(r['t'] in('A','B') and 0.06<r['gap']<=NG for r in sau))
for r in sau:
    if r['cap']: print('  chặn:',r['tag'],f"lệch {r['gap']*100:.1f} • {r['pre']} → {r['t']}")
if kq:
    def g(nm,L):
        v=[rr(kq[r['key']],r['odds']) for r in L if kq.get(r['key']) in('Thắng','Thắng nửa','Hoàn','Thua nửa','Thua')]
        print(f"  RR {nm}: {len(v)} kèo đã chấm, {sum(v):+.2f}R" + (f", ROI {sum(v)/len(v)*100:+.1f}%" if v else ''))
    print('RR theo nhóm (1R/kèo, tính như chưa chặn):')
    g('bị chặn (lệch > 8)',[r for r in sau if r['cap']])
    g('A/B giữ lại',[r for r in sau if r['t'] in('A','B')])
    g('sát ngưỡng 6–8 điểm',[r for r in sau if r['t'] in('A','B') and 0.06<r['gap']<=NG])
    g('trước khi áp, lệch > 8 & A/B',[r for r in rows if r['truoc'] and r['gap']>NG and r['pre'] in('A','B')])
print('SAI – '+str(len(err))+' lỗi:\n  '+'\n  '.join(err) if err else 'ĐÚNG – quy tắc lệch thị trường chấm đúng A1 ở mọi kèo sau khi áp.')
sys.exit(1 if err else 0)
