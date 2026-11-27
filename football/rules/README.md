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
