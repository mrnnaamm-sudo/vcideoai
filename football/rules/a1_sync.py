"""A1 ↔ BỘ MÁY: kiểm TRƯỚC khi phân tích (mục 0). Lệch → DỪNG PHÂN TÍCH, báo ngay.
- Mã phiên bản quy chuẩn = 12 ký tự đầu SHA-256 của rules/quy_chuan.md (văn bản A1).
- Bộ máy ghim mã này ở registry.A1_VERSION: sửa A1 mà không sửa bộ máy (hoặc ngược lại) → lệch.
- Mỗi tab kèo bóng đá mang mã phiên bản trong siêu dữ liệu 'quy_chuan_a1' (ghi cùng lúc với ô A1) → tab nào chưa cập nhật A1 → lệch.
- Mã từng mục (mục 0j): mỗi mục 0–30 có mã riêng ghim ở registry.MUC_HASH → sửa chữ mục nào mà bộ máy chưa cập nhật mục đó → báo đúng mục.
- Ca kiểm ý nghĩa (rules/kiem_thu.py) phải ĐẠT hết; mục bộ máy chấm mà không có ca kiểm → lệch.
- Kiểm toàn văn: so ghi chú A1 đọc từ sheet với quy_chuan.md (từng ký tự).
CLI: python3 rules/a1_sync.py [a1_meta.json] [a1_notes.json]   |   python3 rules/a1_sync.py --ma-muc  (in mã từng mục để ghim khi sửa CÙNG LÚC A1 + bộ máy)"""
import hashlib,json,os,re,sys
D=os.path.dirname(os.path.abspath(__file__))
TABS={100:'Champions League',200:'Ngoại hạng Anh',201:'La Liga',202:'Bundesliga',203:'Europa League',207:'J1 League'}
def text(): return open(os.path.join(D,'quy_chuan.md')).read()
def version(t=None): return hashlib.sha256((t or text()).encode()).hexdigest()[:12]
def sections(t=None):
    t=t or text(); parts=re.split(r'(?m)^(?=\d+\. )',t)
    out={'đầu':parts[0]}
    for p in parts[1:]: out[p.split('.',1)[0]]=p
    return out
def muc_hash(t=None): return {k:hashlib.sha256(v.encode()).hexdigest()[:12] for k,v in sections(t).items()}
class Lech(SystemExit): pass
HUONG_DAN=("THIẾU MÃ A1 ĐỌC TỪ SHEET (mục 0i) – chưa được phân tích. Trước khi chạy: đọc siêu dữ liệu 'quy_chuan_a1' của 6 tab "
 "(get_spreadsheet fields sheets.properties.sheetId + sheets.developerMetadata), ghi {sheetId: mã} vào results/a1_meta.json rồi chạy với A1_META=results/a1_meta.json")
def require(meta_file,notes_file=None):
    """Dùng trong run_day/audit: BẮT BUỘC có mã A1 đọc từ sheet; lệch → dừng."""
    if not meta_file or not os.path.exists(meta_file): raise Lech('DỪNG PHÂN TÍCH – '+HUONG_DAN)
    return check(meta_file,notes_file)
def check(meta_file=None,notes_file=None):
    sys.path.insert(0,os.path.dirname(D)); from rules import registry
    v=version(); err=[]
    if registry.A1_VERSION!=v: err.append(f"A1 (quy_chuan.md, mã {v}) ≠ bộ máy (registry.A1_VERSION {registry.A1_VERSION}) – A1 hoặc bộ máy đã bị sửa một bên")
    MH=muc_hash(); RH=getattr(registry,'MUC_HASH',{})
    for k in MH:
        if k not in RH: err.append(f"mục {k}: có trong A1 nhưng bộ máy chưa có (bổ sung chưa vào bộ máy)")
        elif RH[k]!=MH[k]: err.append(f"mục {k}: nội dung A1 (mã {MH[k]}) ≠ bộ máy (mã {RH[k]}) – mục này đã sửa/bổ sung ở một bên")
    for k in RH:
        if k not in MH: err.append(f"mục {k}: bộ máy có nhưng A1 không có")
    from rules import kiem_thu
    n,ek=kiem_thu.run(); err+=ek
    if meta_file:
        M=json.load(open(meta_file))
        for sid,name in TABS.items():
            if M.get(str(sid))!=v: err.append(f"tab {name}: mã A1 trên sheet {M.get(str(sid))} ≠ {v} – A1 tab này chưa cập nhật giống bộ máy")
    if notes_file:
        N=json.load(open(notes_file)); t=text()
        for sid,name in TABS.items():
            if N.get(str(sid))!=t: err.append(f"tab {name}: nội dung ghi chú A1 khác quy chuẩn của bộ máy")
    if err: raise Lech('DỪNG PHÂN TÍCH – A1 VÀ BỘ MÁY LỆCH NHAU (mục 0):\n - '+'\n - '.join(err))
    return v
if __name__=='__main__':
    if sys.argv[1:2]==['--ma-muc']: print('MUC_HASH=',json.dumps(muc_hash(),ensure_ascii=False)); sys.exit()
    print('ĐỒNG BỘ – mã phiên bản',check(*(sys.argv[1:3]+[None,None])[:2]))
