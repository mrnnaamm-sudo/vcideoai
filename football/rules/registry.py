"""BẢNG ĐỐI CHIẾU A1 ↔ BỘ MÁY. Mỗi mục trong A1 (rules/quy_chuan.md) phải có đúng 1 dòng ở đây và ngược lại.
loai: 'cham' = bộ máy chấm (engine.grade ghi bước kiểm có mã 'buoc'), 'mo_hinh' = model.py, 'du_lieu' = khâu nạp dữ liệu (run_day + kiểm đầu vào),
'xep' = engine.rank, 'trinh_bay' = khuôn ghi sheet (run_day), 'quy_trinh' = việc theo lịch (chốt kèo / chấm kết quả / tổng kết).
thi_truong: những thị trường bắt buộc phải có bước kiểm này trong dòng 'Đã kiểm quy chuẩn'."""
# Mục 0(h): DANH SÁCH THỊ TRƯỜNG. 'chinh_thuc' = đã tích hợp đủ 4 nơi, được chấm/xếp/báo; 'cho_tich_hop' = kèo mới đang thêm: chỉ lưu giá, KHÔNG chấm, KHÔNG Ưu tiên/TOP, KHÔNG tính RR.
MARKETS={'hc':('Chấp bàn FT','chinh_thuc'),'tot':('Tài/Xỉu bàn FT','chinh_thuc'),'cor':('Góc FT','chinh_thuc'),'h1':('Góc H1','chinh_thuc'),
         'card':('Thẻ FT','chinh_thuc'),'chc':('Chấp góc FT','chinh_thuc')}
def official(mk): return MARKETS.get(mk,(None,'cho_tich_hop'))[1]=='chinh_thuc'
ALL=('hc','tot','cor','h1','chc','card')
RR=('hc','tot','cor','h1','chc')
REG={
 0:dict(loai='quy_trinh',noi='rules/run_day.py → rules/audit.py (bắt buộc ĐẠT mới báo kèo)'),
 1:dict(loai='du_lieu',noi='run_day: mẫu 10 trận VĐQG + C1/EL (ACL với giải châu Á); audit kiểm đầu vào'),
 2:dict(loai='du_lieu',noi='run_day: bù số liệu từ trận C1/EL gần nhất'),
 3:dict(loai='trinh_bay',noi='khối phong độ BP2300+'),
 4:dict(loai='trinh_bay',noi='khối trọng tài BP2520+'),
 5:dict(loai='cham',buoc='5',thi_truong=('card',)),
 6:dict(loai='cham',buoc='6',thi_truong=ALL),
 7:dict(loai='cham',buoc='27',thi_truong=RR),
 8:dict(loai='cham',buoc='8',thi_truong=RR),
 9:dict(loai='xep',noi='engine.rank'),
 10:dict(loai='trinh_bay',noi='định dạng có điều kiện của tab'),
 11:dict(loai='du_lieu',noi='tái dùng tệp đã tải (g/, d28/fm, j1/fm)'),
 12:dict(loai='mo_hinh',noi='model / recs: thẻ = vàng + 2×đỏ'),
 13:dict(loai='quy_trinh',noi='lịch chấm kết quả sau trận'),
 14:dict(loai='cham',buoc=('14(8)','14(8b)','14(2)','14(1)'),thi_truong={'hc':('14(8)','14(8b)','14(2)','14(1)'),'tot':('14(8b)','14(1)'),'cor':('14(8b)',),'h1':('14(8b)',),'chc':('14(8)','14(8b)','14(2)')}),
 15:dict(loai='cham',buoc='15',thi_truong=ALL),
 16:dict(loai='cham',buoc='16',thi_truong=ALL),
 17:dict(loai='trinh_bay',noi='khung A5 6 khối'),
 18:dict(loai='cham',buoc='8',thi_truong=RR,noi='C+ trong model.tier; tổng kết tuần theo lịch'),
 19:dict(loai='mo_hinh',noi='model.evaluate, model.chc_eval'),
 20:dict(loai='cham',buoc='20(d)',thi_truong=('hc',),noi='(a)(b) trong model.vblend'),
 21:dict(loai='mo_hinh',noi='model.evaluate tham số coef (trận khác giải)'),
 22:dict(loai='mo_hinh',noi='model.evaluate tham số xg'),
 23:dict(loai='cham',buoc='23',thi_truong=RR),
 24:dict(loai='cham',buoc='24',thi_truong=('card',)),
 25:dict(loai='du_lieu',noi='ClubElo / Elo ước tính; dùng ở 14(2), 16, 23, 29'),
 26:dict(loai='quy_trinh',noi='review/ sau mỗi lượt chấm'),
 27:dict(loai='cham',buoc='27',thi_truong=RR),
 28:dict(loai='cham',buoc='28',thi_truong=('cor','h1')),
 29:dict(loai='cham',buoc='29',thi_truong=('card',)),
 30:dict(loai='cham',buoc='30(c)',thi_truong=('chc',)),
}
# Mục 0(h): PHẦN CHUNG mọi loại kèo (kể cả kèo mới) bắt buộc dùng: mẫu 10 trận (mục 1, khâu dữ liệu), giá (6), công thức tier (8),
# đủ số liệu (15), bất thường (16), xu hướng 5 trận (14(8b)), lịch (23), đội hình (27) và xếp Ưu tiên/TOP (9).
COMMON=('6','8','15','16','14(8b)','23','27')
EXTRA={}   # kèo mới: {'mã': ('mục riêng', ...)} – mục riêng của loại kèo mới (nếu có)
def need(mk):
    if mk not in ALL and mk!='card':                      # loại kèo mới: phần chung + mục riêng
        return list(dict.fromkeys(list(COMMON)+list(EXTRA.get(mk,()))))
    return _need_old(mk)
def _need_old(mk):
    """Các bước kiểm bắt buộc phải xuất hiện cho thị trường mk (lấy thẳng từ bảng đối chiếu)."""
    out=[]
    for m,r in REG.items():
        if r['loai']!='cham': continue
        tt=r.get('thi_truong',())
        if isinstance(tt,dict): out+=list(tt.get(mk,()))
        elif mk in tt: out+=[r['buoc']] if isinstance(r['buoc'],str) else list(r['buoc'])
    return list(dict.fromkeys(out))
