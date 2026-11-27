"""BƯỚC KIỂM BẮT BUỘC sau khi ghi sheet: so từng dòng trên sheet với kết quả bộ máy quy chuẩn chung.
python3 rules/audit.py results/sheet_engine_<ngày>.json <file json chứa cột AW đọc ngược từ sheet {tab:{row:tier}}>
Có bất kỳ dòng lệch → KHÔNG được báo kèo cho người dùng."""
import json,sys,re
P=json.load(open(sys.argv[1])); S=json.load(open(sys.argv[2]))
err=[]
for tab,rows in P.items():
    pri={}
    for r,d in rows.items():
        t=d['t']; s=S.get(tab,{}).get(r)
        if s!=t: err.append(f"{tab}{r}: sheet {s} ≠ bộ máy {t}")
        ay=d['asy'][6]
        if 'Đã kiểm quy chuẩn' not in ay: err.append(f"{tab}{r}: thiếu dòng kiểm quy chuẩn")
        if ('Ưu tiên' in ay.split(' • ')[0] or 'TOP' in ay.split(' • ')[0]) and t not in('A','B'): err.append(f"{tab}{r}: Ưu tiên/TOP trên tier {t}")
        if d.get('pri'): pri.setdefault(d['mid'],[]).append(r)
        need={'hc':['6','15','16','8','14(8)','14(8b)','20(d)','27','14(1)','23'],'tot':['6','15','16','8','14(8b)','27','14(1)','23'],
              'cor':['6','15','16','8','28','14(8b)','27','23'],'h1':['6','15','16','8','28','14(8b)','27','23'],
              'chc':['6','15','16','8','30(c)','14(8)','14(8b)','27','23'],'card':['6','15','16','5','29']}[d['mk']]
        got={m for m,k,dd in d['steps']}
        if not ('15' in got and any(m=='15' and dd for m,k,dd in d['steps'])):
            miss=[m for m in need if m not in got]
            if miss: err.append(f"{tab}{r}: thiếu mục {miss}")
    for m,rs in pri.items():
        if len(rs)>2: err.append(f"{m}: {len(rs)} Ưu tiên (> 2)")
print('LỖI:' if err else 'ĐẠT – 0 lỗi', len(sum([list(v) for v in P.values()],[])),'kèo')
for e in err: print(' -',e)
sys.exit(1 if err else 0)
