# Quy chuẩn chung = bộ máy

| Tệp | Vai trò |
|---|---|
| `quy_chuan.md` | Văn bản A1 (giống hệt ghi chú ô A1 của mọi tab kèo bóng đá) |
| `engine.py` | Bộ máy chấm duy nhất (`grade`, `rank`) |
| `registry.py` | Bảng đối chiếu mục 0–30 ↔ nơi thực hiện; sinh danh sách bước kiểm bắt buộc |
| `run_day.py` | Nạp dữ liệu, chấm, sinh nội dung sheet theo khuôn chung |
| `audit.py` | Bước kiểm bắt buộc sau khi ghi sheet (chỉ báo kèo khi ĐẠT) |
| `derby.json`, `tinh_chat_<ngày>.json` | Đầu vào mục 23/24 |

Mọi thay đổi (bài học mới, quy chuẩn mới, tab mới) phải sửa cùng lúc: A1 các tab + `quy_chuan.md` + bộ máy + `registry.py` (mục 0f).

## Mục 0(i)(j) – A1 và bộ máy luôn giống hệt (từ 27/11 tối)
- `a1_sync.py`: mã phiên bản (cả văn bản) + MÃ TỪNG MỤC (registry.MUC_HASH) + chạy ca kiểm ý nghĩa; `require()` bắt buộc có mã A1 đọc từ sheet (A1_META) – thiếu/lệch → DỪNG PHÂN TÍCH, báo đúng tab/mục.
- `kiem_thu.py`: 91 ca kiểm ý nghĩa ("theo A1 thì kèo thế này phải ra kết quả gì"), có ca biên cho từng ngưỡng.
- `quet_nguong.py`: đổi từng con số trong bộ máy, kiểm ca nào bắt được (hiện 117/120; 3 số còn lại là định dạng hiển thị / điều kiện không thể xảy ra).
- `doi_chieu.py` → `DOI_CHIEU_A1_BO_MAY.md/.html`: bảng đối chiếu gửi người dùng sau mỗi lần sửa đổi/bổ sung/bài học.
Quy trình sửa: sửa quy_chuan.md + engine/model + ca kiểm của mục đó → `python3 rules/a1_sync.py --ma-muc` ghim mã vào registry → ghi A1 lên 6 tab + siêu dữ liệu → đọc ngược → `doi_chieu.py`.
Trước mỗi lần phân tích: đọc siêu dữ liệu 'quy_chuan_a1' 6 tab → results/a1_meta.json → `A1_META=results/a1_meta.json python3 rules/run_day.py`.
