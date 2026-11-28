# Dự án kèo bóng đá (thư mục football/)
- Luôn trả lời người dùng bằng tiếng Việt.
- Mọi yêu cầu phân tích kèo / chốt kèo / chấm kết quả / rút bài học của BẤT KỲ giải nào, ngày nào: làm ĐÚNG theo `football/khuon/QUY_TRINH.md` (5 bước). Không tự nghĩ cách khác, không hỏi lại những gì quy trình đã quy định.
- Quy chuẩn phân tích = ghi chú A1 các tab = `football/rules/quy_chuan.md` = bộ máy (`football/rules/engine.py`, `football/model.py`). Không sửa quy chuẩn ngoài mục 0(i)(j)(k); A1 lệch bộ máy → dừng và báo.
- Google Sheet: "Make money online" (ID 1tsZy2D0UZ3xv0nt0xKVtpeFOLX1sNcVbAUgBjNY6ibE). Tab 'Tổng kết RR tuần' và 'Kèo đã vào' chỉ ghi kết quả. Tab 'Tổng kết RR tuần' chỉ cập nhật 1 lần/tuần ở buổi tổng kết cuối tuần, không cập nhật sau mỗi lượt chấm ngày (RR ngày ghi ở các tab kèo).
- Không đưa khóa API vào kho mã hay vào chat (Odds API: proxy tự gắn khóa, gọi không kèm apiKey).
- Tiết kiệm token (người dùng 28/11): lịch tự động CHỈ gồm chốt kèo trước trận và chấm kết quả RR ngày; không tự động làm việc khác (không tổng kết tuần, không rà soát thêm) trừ khi người dùng yêu cầu.
