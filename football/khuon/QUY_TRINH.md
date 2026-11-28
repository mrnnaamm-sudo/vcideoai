# QUY TRÌNH CHUẨN – PHÂN TÍCH KÈO BÓNG ĐÁ (mọi giải, mọi ngày)

Một quy trình duy nhất, chạy đúng thứ tự, không sửa tay. **Quy trình này KHÔNG chứa quy chuẩn phân tích**: quy chuẩn nằm ở A1 = `rules/quy_chuan.md` và bộ máy `rules/engine.py` + `model.py`. Khuôn chỉ nạp dữ liệu, gọi bộ máy, ghi sheet, chấm kết quả. Sửa quy chuẩn chỉ theo mục 0(i)(j)(k) của A1.

Yêu cầu dạng: *"phân tích kèo <giải> ngày <dd/mm>"* (có thể thêm *"trận <đội>"*) → làm 5 bước dưới đây.
Mã giải: PL, LL, BL, J1, CL, EL (khai báo ở `khuon/giai.py`; giải mới chỉ thêm 1 dòng ở đây, mục 0g).

## Bước 0 – Kiểm A1 = bộ máy (bắt buộc, mục 0i)
1. Đọc siêu dữ liệu `quy_chuan_a1` 6 tab (get_spreadsheet, fields `sheets.properties.sheetId`, `sheets.developerMetadata`) → `results/a1_meta.json` dạng `{"100": "<mã>", ...}`.
2. Mọi lệnh dưới đây chạy với `A1_META=results/a1_meta.json`. Lệch → bộ chạy tự DỪNG và báo; báo ngay người dùng, không phân tích.

## Bước 1 – Lên kế hoạch
0. Elo (mục 25): `python3 khuon/elo_moi.py` – cập nhật ClubElo mỗi ngày phân tích (đọc bảng toàn cầu trên clubelo.com vì api.clubelo.com bị ngắt ở proxy). Đội chưa khớp tên → bộ chạy dừng và chỉ tên cần thêm vào `khuon/elo_alias.json`.
1. Giá: chấp/tài xỉu bàn chỉ lấy **Pinnacle** (Odds API, mục 6) → lưu `khuon/gia/<YYYY-MM-DD>/pinnacle_<mã odds>.json`; lần lấy trước (nếu có) đổi tên `..._truoc.json` (mục 14(1)). Odds API có hạn mức – kiểm `x-requests-remaining` (gọi /v4/sports không tốn lượt).
   **HẾT LƯỢT / MẤT NGUỒN → TỰ CHUYỂN NGUỒN THAY THẾ, KHÔNG DỪNG, KHÔNG CHỜ HỎI (người dùng 28/11).** Thứ tự nguồn giá Pinnacle: (1) Odds API; (2) trang Pinnacle công khai – `python3 khuon/pinnacle_web.py <PL|LL|BL|J1|CL|EL> khuon/gia/<ngày>/pinnacle_<mã odds>_web.json <tệp Odds API cũ để khớp tên>` (cùng định dạng Odds API, không cần khóa); (3) chỉ khi cả hai hỏng mới để 'chờ giá' (mục 6). Ghi rõ nguồn và giờ lấy ở cột AX. Áp dụng tương tự cho mọi nguồn khác: FotMob lỗi → ESPN/SofaScore; ClubElo API lỗi → bảng clubelo.com (khuon/elo_moi.py); đội hình chính thức → FotMob matchDetails (lineupType 'standard'). Luôn báo người dùng đã chuyển sang nguồn nào.
2. Giá người dùng gửi (góc FT, góc H1, thẻ, chấp góc) → `khuon/gia/<ngày>/nguoi_dung.json`:
   `{"PL": {"Arsenal – Manchester City": {"cor": [10.5, 1.90, 1.90], "h1": [4.5, 1.85, 1.95], "card": [4.5, 1.80, 2.00], "chc": [-1.5, 1.95, 1.85]}}}` (mốc chấp góc theo đội nhà; cách đọc kèo người dùng theo mục 30a).
3. Sơ đồ dòng: đọc `AQ150:AR399` của tab giải → lưu `{mã: values}` → `python3 khuon/doc_sheet.py so-do <vào> <so_do.json>`.
4. Tính chất trận (nếu có thông tin rõ, mục 23c/24): `rules/tinh_chat_<dd-mm>.json`.

## Bước 2 – Phân tích (bộ máy chung)
```
A1_META=results/a1_meta.json python3 -B khuon/chay.py --ngay <YYYY-MM-DD> --giai PL,LL --so-do <so_do.json> [--tran <đội>]
```
Ra: `results/engine_<dd-mm>.json`, `results/sheet_engine_<dd-mm>.json`, `results/ke_hoach_ghi_<dd-mm>.json`.

## Bước 3 – Ghi sheet + bước kiểm + báo kèo
1. Ghi đúng từng vùng trong `ke_hoach_ghi_<dd-mm>.json` (update_values; ô `null` bỏ qua). Không ghi cột AZ:BA, không ghi khung A–H.
   **Tab J1 – khối phong độ 10 trận (cột L lọc theo B1):** `python3 -B khuon/phong_do.py J1 <YYYY-MM-DD> results/phong_do_J1_<dd-mm>.json` → ghi nối tiếp vào `BP2300:CO2519` ngay sau dòng cuối đã có (BP = số ngày); khối trọng tài ghi nối tiếp `BP2520:BZ2560` (chưa công bố → 'Chưa công bố', kèo thẻ tối đa C). Đầy vùng → nới phạm vi FILTER ở L5, không ghi đè ngày cũ.
   **Ô chọn ngày B1 (mọi tab):** ngày mới phân tích phải có trong danh sách thả xuống của B1 (setDataValidation ONE_OF_LIST, dạng dd/mm/yyyy, giữ các ngày cũ) – thiếu thì thêm ngay khi ghi sheet.
2. Đọc ngược `AW150:AW399` → `python3 khuon/doc_sheet.py aw <vào> <aw.json>` → `A1_META=results/a1_meta.json python3 -B rules/audit.py results/sheet_engine_<dd-mm>.json <aw.json>`.
3. **Chỉ báo kèo khi ĐẠT 0 lỗi**: TOP 1–2 mỗi khung giờ, Ưu tiên mỗi trận, kèo KHÔNG VÀO; nói rõ kèo nào đang chờ giá.
4. Chốt 1 tiếng trước mỗi khung giờ (mục 6, 27f): lấy đội hình chính thức (FotMob tự cập nhật) + giá mới → chạy lại Bước 2–3 cho khung đó (`--tran`). Không chỉnh tier tay.

## Bước 4 – Sau trận: kết quả + RR
```
python3 -B khuon/ket_qua.py --ngay <YYYY-MM-DD> [--giai PL]
```
1. Ghi `results/ke_hoach_ket_qua_<dd-mm>.json` (cột AZ 'Thực tế', BA 'Kết quả'). Trận chưa đủ số liệu → 'Chờ số liệu', đặt lịch kiểm lại.
2. Kèo người dùng đã vào thật (tab 'Kèo đã vào'): ghi J (Kết quả), K (diễn biến), L (giờ cập nhật).
3. Cập nhật bản tóm tắt tab 'Tổng kết RR tuần' (vùng N200, 7 phần, ngắn gọn; thẻ RR riêng – mục 29).

## Bước 5 – Rút bài học (mục 0k)
1. Xem `ung_vien_bai_hoc` trong `results/ket_qua_<dd-mm>.json` (nhóm |z| ≥ 1,5; kèo Ưu tiên/TOP thua).
2. Có nguyên nhân rõ, có số liệu → **cập nhật ngay** theo mục 0(j): mục 14 `rules/quy_chuan.md` + bộ máy + ca kiểm `rules/kiem_thu.py` + `python3 rules/a1_sync.py --ma-muc` (ghim registry) + `python3 -B rules/quet_nguong.py` + ghi A1 lên 6 tab + siêu dữ liệu + đọc ngược toàn văn + `python3 -B rules/doi_chieu.py` + commit. Áp từ lần phân tích kế tiếp, không chấm lại kèo đã đá. Dao động ngẫu nhiên → chỉ ghi nhận.
3. **Cuối tuần** (Tổng kết RR tuần): gộp bài học đã cập nhật + RR tuần thành danh sách review **CHỜ NGƯỜI DÙNG DUYỆT**; chỉ sửa sau khi người dùng báo.

## Không được
- Sửa quy chuẩn ngoài mục 0(j)(k); chỉnh tier bằng tay; dùng giá quy đổi/tự đoán; báo kèo khi bước kiểm chưa ĐẠT; ghi đè cột kết quả hoặc khung công thức A–H.
