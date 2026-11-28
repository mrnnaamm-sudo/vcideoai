---
name: phan-tich-keo
description: Phân tích kèo bóng đá theo quy trình chuẩn của dự án (mọi giải PL, LL, BL, J1, C1, EL; mọi ngày) – lên kế hoạch, chạy bộ máy quy chuẩn chung, ghi sheet, bước kiểm, báo kèo; sau trận chấm kết quả, tính RR, rút bài học. Dùng khi người dùng nói "phân tích kèo", "chốt kèo", "chấm kết quả", "tính RR", "rút bài học" cho trận/ngày/giải bất kỳ.
---
Đọc và làm đúng từng bước trong `football/khuon/QUY_TRINH.md` (Bước 0 → 5), chạy từ thư mục `football/`.
- Bước 0 luôn đọc mã A1 từ sheet và chạy với `A1_META`; lệch → dừng, báo người dùng.
- Không sửa quy chuẩn (A1, `rules/`, `model.py`) ngoài mục 0(j)(k) của A1; không chỉnh tier tay; chỉ báo kèo khi `rules/audit.py` ĐẠT 0 lỗi.
- Trả lời người dùng bằng tiếng Việt, ngắn gọn: TOP/Ưu tiên/KHÔNG VÀO, kèo chờ giá, kết quả bước kiểm.
