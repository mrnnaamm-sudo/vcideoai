"""BƯỚC KIỂM BẮT BUỘC sau khi ghi sheet: so từng dòng trên sheet với kết quả bộ máy quy chuẩn chung.
python3 rules/audit.py results/sheet_engine_<ngày>.json <file json chứa cột AW đọc ngược từ sheet {tab:{row:tier}}>
Có bất kỳ dòng lệch → KHÔNG được báo kèo cho người dùng."""
import json,sys,re,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import registry
# A1 ↔ bảng đối chiếu: mọi mục trong A1 phải có trong REG và ngược lại
A1=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'quy_chuan.md')).read()
mucA1={int(x) for x in re.findall(r'(?m)^(\d+)\. ',A1)}
mucREG=set(registry.REG)
P=json.load(open(sys.argv[1])); S=json.load(open(sys.argv[2]))
err=[f'A1 có mục {m} nhưng bộ máy không có' for m in sorted(mucA1-mucREG)]+[f'bộ máy có mục {m} nhưng A1 không có' for m in sorted(mucREG-mucA1)]
for tab,rows in P.items():
    pri={}
    for r,d in rows.items():
        t=d['t']; s=S.get(tab,{}).get(r)
        if s!=t: err.append(f"{tab}{r}: sheet {s} ≠ bộ máy {t}")
        ay=d['asy'][6]
        # mục 1: mẫu chỉ gồm VĐQG + C1/EL (+ACL với giải châu Á)
        OKL={'English Premier League','Spanish LALIGA','German Bundesliga','Italian Serie A','French Ligue 1','UEFA Champions League','UEFA Europa League','J1 League','ACL'}
        bad=[l for l in d.get('mau',[]) if l not in OKL]
        if bad: err.append(f"{tab}{r}: mẫu có giải ngoài mục 1: {bad}")
        # mục 6: chấp/tài xỉu bàn phải là giá Pinnacle; không giá quy đổi
        if d['mk'] in('hc','tot') and d['asy'][1] not in('',None) and not str(d.get('price_src','')).startswith('Pinnacle'): err.append(f"{tab}{r}: giá {d['mk']} không phải Pinnacle (mục 6)")
        if 'Đã kiểm quy chuẩn' not in ay: err.append(f"{tab}{r}: thiếu dòng kiểm quy chuẩn")
        if ('Ưu tiên' in ay.split(' • ')[0] or 'TOP' in ay.split(' • ')[0]) and t not in('A','B'): err.append(f"{tab}{r}: Ưu tiên/TOP trên tier {t}")
        if d.get('pri'): pri.setdefault(d['mid'],[]).append(r)
        need=registry.need(d['mk']) if d['mk']!='card' or tab!='J1' else ['6','29(g)']
        got={m for m,k,dd in d['steps']}
        if not ('15' in got and any(m=='15' and dd for m,k,dd in d['steps'])):
            miss=[m for m in need if m not in got]
            if miss: err.append(f"{tab}{r}: thiếu mục {miss}")
    for m,rs in pri.items():
        if len(rs)>2: err.append(f"{m}: {len(rs)} Ưu tiên (> 2)")
print('LỖI:' if err else 'ĐẠT – 0 lỗi', len(sum([list(v) for v in P.values()],[])),'kèo')
for e in err: print(' -',e)
sys.exit(1 if err else 0)
