# RÀ SOÁT QUY CHUẨN CHUNG 28/11 – CHỈ ĐỀ XUẤT (CHỜ NGƯỜI DÙNG DUYỆT)
Không sửa A1, bộ máy, tier. Dữ liệu kiểm chứng: 84 kèo đã chấm có đủ xác suất (72 kèo EL 27/11 + 12 kèo rạng sáng 28/11, trừ thẻ, bỏ kèo hoàn). Kết quả EL 27/11 dựng lại từ RR nên có sai số nhỏ. **Mẫu nhỏ – mọi số liệu chỉ để định hướng.**

## A. A1 và bộ máy lệch nhau (bước kiểm chưa bắt)
1. **Mục 9 – ưu tiên kèo góc khi EV chênh ≤ 2 điểm**: A1 ghi áp cho cả "Ưu tiên/TOP"; bộ máy (engine.rank) chỉ áp khi xếp TOP khung giờ, KHÔNG áp khi chọn Ưu tiên 1/2 trong trận. Ảnh hưởng: có thể chọn kèo bàn làm Ưu tiên 1 thay vì kèo góc cùng tier. Đề xuất: (a) sửa bộ máy cho đúng A1, hoặc (b) sửa chữ A1 cho đúng bộ máy; thêm ca kiểm. CHỜ DUYỆT.
2. **Mục 8 – dòng '[Thử mục 8 (a)(b); tier cách cũ: …]'**: A1 yêu cầu ghi trong kết luận, bộ máy không ghi. Ảnh hưởng: tổng kết tuần 30/11 không so được bản thử với cách cũ trên kèo 28–29/11 (chỉ còn results/d28_AY_cachcu.json cho 28/11). Đề xuất: bộ máy ghi thêm tier cách cũ (model.tier_old), hoặc bỏ câu này khỏi A1. CHỜ DUYỆT.
3. **Mục 8 – C+ cần "mẫu ≥ 8"**: bộ máy không kiểm riêng điều kiện này (chỉ có mục 15 cho góc/thẻ). Ảnh hưởng nhỏ (mẫu bàn luôn đủ 10). Đề xuất: thêm điều kiện vào bộ máy + ca kiểm, hoặc ghi rõ trong A1 là đã thay bằng mục 15. CHỜ DUYỆT.
4. **Trọng số 40/30/30 (mục 8b) chưa có ca kiểm** – đã ghi nhận 28/11, lịch tổng kết tuần sẽ kiểm. Đề xuất: thêm ca kiểm khi duyệt. CHỜ DUYỆT.

## B. Mâu thuẫn chữ trong A1
5. Mục 18(a)(b)(c), 26(b) ghi "cả 5 tab" trong khi đã có 6 tab (J1). Đề xuất: đổi thành "mọi tab kèo bóng đá". CHỜ DUYỆT.

## C. Phương pháp – kiểm chứng trên 84 kèo
6. **Hiệu chuẩn (Brier, thấp = tốt)**: thị trường 0,2434 • mẫu đã co 0,2486 • mô hình 0,2553 • mẫu thô 0,2632. Trộn 40/30/30 (hiện tại) 0,2473; 30/20/50 0,2455; 20/20/60 0,2446. → Thị trường hiệu chuẩn tốt nhất, mô hình kém nhất. Chọn kèo EV ≥ 5%: 40/30/30 → 25 kèo RR +2,28; 30/20/50 → 16 kèo RR +2,82; 20/20/60 → 9 kèo RR +0,14. Đề xuất: cân nhắc 30/20/50 (bản thử 2) – nhưng 84 kèo là quá ít, nên chờ tổng kết tuần 30/11 với thêm kèo 28–29/11 rồi quyết. CHỜ DUYỆT.
7. **Chọn ngược theo mức lệch thị trường (ước tính − công bằng)**: lệch > 8 điểm: 12 kèo RR −2,86 (ROI −23,8%; dự báo thắng 63%, thực tế 40%); lệch 4–8 điểm: 26 kèo RR +6,11 (ROI +23,5%); lệch 0–4 điểm: 38 kèo RR −4,91. → Kèo lệch thị trường nhiều nhất là nhóm tự tin quá mức. A1 hiện chỉ chặn lệch > 12 điểm ở tier A. Đề xuất theo dõi: tier B lệch > 8 điểm thì tối đa C+ – mẫu 12 kèo quá nhỏ, CHỜ DUYỆT sau tổng kết tuần.
8. **Mẫu 10 trận không điều chỉnh sức mạnh đối thủ** (trận C1/EL/ACL gặp đội yếu, ví dụ Kyoto 4T–1H ở ACL): chưa kiểm chứng được (cần Elo đối thủ từng trận mẫu – nay khuôn đã có ClubElo 1.700 đội). Đề xuất: thử hệ số điều chỉnh theo Elo đối thủ trên dữ liệu tuần sau. CHỜ DUYỆT.
9. **Trọng số đều 10 trận** (không giảm dần): chưa kiểm chứng; mục 14(8)(8b) đang bù phần phong độ ngắn hạn. Đề xuất: thử trọng số giảm dần khi đủ dữ liệu. CHỜ DUYỆT.
10. **Chấp góc – giả định góc hai đội độc lập**: mới 3 kèo đã chấm (2T–1B) – chưa đủ để đánh giá. Theo dõi.
11. **Elo ước tính J1 (1500 + 110 × hiệu số/trận)**: chưa có dữ liệu kết quả J1 để kiểm; kiểm sau lượt chấm J1 16:35.
12. **Tách sân 60%**: chưa kiểm chứng riêng. Theo dõi.

## Đã kiểm, không vấn đề
- Phép tính bàn H1 J1 đúng (113/113 trận); mục 6/17 đủ 6 thị trường; trọng số 40/30/30 trong bộ máy khớp EV đã lưu 89/89 kèo ngày 28/11.
