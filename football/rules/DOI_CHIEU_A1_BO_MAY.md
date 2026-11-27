# BẢNG ĐỐI CHIẾU QUY CHUẨN CHUNG: A1 ↔ BỘ MÁY
Lập lúc 27/11/2026 23:38 (giờ VN) • Mã phiên bản quy chuẩn: **3cbba536afd6** • Bộ máy ghim: **3cbba536afd6**
**KẾT LUẬN: ĐỒNG BỘ – A1 và bộ máy giống hệt nhau**

## 1. A1 trên từng tab
| Tab | Mã A1 trên tab | So với bộ máy | Toàn văn A1 so với bộ máy |
|---|---|---|---|
| Champions League | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |
| Ngoại hạng Anh | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |
| La Liga | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |
| Bundesliga | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |
| Europa League | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |
| J1 League | 3cbba536afd6 | KHỚP | TRÙNG TỪNG KÝ TỰ |

## 2. Ca kiểm ý nghĩa: 91/91 ĐẠT

## 3. Từng mục: mã A1 = mã bộ máy
| Mục | Nội dung | Mã A1 | Mã bộ máy | Khớp | Bộ máy thực hiện | Ca kiểm |
|---|---|---|---|---|---|---|
| đầu | QUY CHUẨN CHUNG – ÁP DỤNG GIỐNG NHAU CHO MỌI TAB BÓNG ĐÁ (trừ tab NBA), MỌI GIẢI | cdec39c938ac | cdec39c938ac | ✔ | Phần mở đầu – phạm vi áp dụng (mọi tab bóng đá, trừ NBA, RR tuần, Kèo đã vào) | 0/0 |
| 0 | A1 = BỘ MÁY (bắt buộc, từ 27/11 tối) | c701ba9131ea | c701ba9131ea | ✔ | Quy trình theo lịch • rules/run_day.py → rules/audit.py (bắt buộc ĐẠT mới báo kèo) | 2/2 |
| 1 | Dữ liệu | 041eb27e2e03 | 041eb27e2e03 | ✔ | Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • run_day: mẫu 10 trận VĐQG + C1/EL (ACL với giải châu Á); audit kiểm đầu vào | 1/1 |
| 2 | Bù số liệu | e27ad41f5a68 | e27ad41f5a68 | ✔ | Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • run_day: bù số liệu từ trận C1/EL gần nhất | 0/0 |
| 3 | Bảng phong độ (cột L trở đi) | d2a2163b7d65 | d2a2163b7d65 | ✔ | Khuôn ghi sheet • khối phong độ BP2300+ | 0/0 |
| 4 | Khối 'TRỌNG TÀI CÁC TRẬN' ngay dưới bảng phong độ | eb31f57853de | eb31f57853de | ✔ | Khuôn ghi sheet • khối trọng tài BP2520+ | 0/0 |
| 5 | Kèo thẻ BẮT BUỘC xét trọng tài và tính chất trận (mục 24) (SIẾT sau RR kỳ 0 | 7e7d5bb8fbdd | 7e7d5bb8fbdd | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '5' • áp cho: Thẻ | 11/11 |
| 6 | Trước trận | 87970b0e64ec | 87970b0e64ec | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '6' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ | 1/1 |
| 7 | Tin lực lượng | 88a54636765c | 88a54636765c | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '27' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc | 5/5 |
| 8 | Chấm kèo (BẢN THỬ từ 28/11 – (a)(b), so sánh với cách cũ ở tổng kết tuần 30/11) | e08386d5cddd | e08386d5cddd | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '8' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc | 15/15 |
| 9 | Mỗi trận tối đa 2 kèo ưu tiên ('Ưu tiên 1 • …', 'Ưu tiên 2 • …') và CHỈ chọn từ | 378f413cce2e | 378f413cce2e | ✔ | Xếp Ưu tiên/TOP (engine.rank) • engine.rank | 3/3 |
| 10 | Trình bày thống nhất | 67a5260315d9 | 67a5260315d9 | ✔ | Khuôn ghi sheet • định dạng có điều kiện của tab | 0/0 |
| 11 | Tái sử dụng dữ liệu đã có trong file trước, chỉ tra web phần mới/thiếu. | 1ce05d97aac1 | 1ce05d97aac1 | ✔ | Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • tái dùng tệp đã tải (g/, d28/fm, j1/fm) | 0/0 |
| 12 | Cách đếm thẻ | 200d821f672a | 200d821f672a | ✔ | Mô hình xác suất (model.py) • model / recs: thẻ = vàng + 2×đỏ | 0/0 |
| 13 | Sau trận | 07765d7683e0 | 07765d7683e0 | ✔ | Quy trình theo lịch • lịch chấm kết quả sau trận | 0/0 |
| 14 | Bài học đã rút (C1 25–26/11) | 8e33aaa35f86 | 8e33aaa35f86 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '14(8), 14(8b), 14(2), 14(1)' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc | 14/14 |
| 15 | TRẬN KHÔNG ĐỦ SỐ LIỆU | c95c08d3b43d | c95c08d3b43d | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '15' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ | 3/3 |
| 16 | KIỂM TRA KÈO BẤT THƯỜNG (bắt buộc trước khi chấm tier) | cf37705765d5 | cf37705765d5 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '16' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ | 16/16 |
| 17 | BỐ CỤC BẮT BUỘC MỖI TAB (mọi giải, mọi ngày, giống hệt tab Champions League) | d5d60086fa69 | d5d60086fa69 | ✔ | Khuôn ghi sheet • khung A5 6 khối | 0/0 |
| 18 | RR LÀ THƯỚC ĐO HIỆU QUẢ PHÂN TÍCH | 49c86f641233 | 49c86f641233 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '8' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc • C+ trong model.tier; tổng kết tuần theo lịch | 15/15 |
| 19 | MÔ HÌNH XÁC SUẤT (mẫu tối đa 10 trận/đội) | 7e7d6be2a5b5 | 7e7d6be2a5b5 | ✔ | Mô hình xác suất (model.py) • model.evaluate, model.chc_eval | 0/0 |
| 20 | SÂN NHÀ / SÂN KHÁCH (bắt buộc tách) | c7c4b84d609e | c7c4b84d609e | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '20(d)' • áp cho: Chấp bàn • (a)(b) trong model.vblend | 4/4 |
| 21 | HỆ SỐ GIẢI (thông số PHỤ, chỉ dùng khi hai đội khác giải – cúp châu Âu) | 2c6531a1a9dc | 2c6531a1a9dc | ✔ | Mô hình xác suất (model.py) • model.evaluate tham số coef (trận khác giải) | 0/0 |
| 22 | xG (khi tra được) | 81e2e0001bfd | 81e2e0001bfd | ✔ | Mô hình xác suất (model.py) • model.evaluate tham số xg | 0/0 |
| 23 | ĐỘNG LỰC & LỊCH THI ĐẤU (bắt buộc ghi) | 200634f1b072 | 200634f1b072 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '23' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc | 2/2 |
| 24 | TÍNH CHẤT TRẬN CHO KÈO THẺ (nhân vào kỳ vọng thẻ) | 0a40c7974de7 | 0a40c7974de7 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '24' • áp cho: Thẻ | 4/4 |
| 25 | RANKING SỨC MẠNH & ĐỊNH NGHĨA ĐỘI LỚN | 06f00223529f | 06f00223529f | ✔ | Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • ClubElo / Elo ước tính; dùng ở 14(2), 16, 23, 29 | 0/0 |
| 26 | RÀ SOÁT RR SAU MỖI TRẬN/MỖI LƯỢT CHẤM (bắt buộc) | da6339b745f4 | da6339b745f4 | ✔ | Quy trình theo lịch • review/ sau mỗi lượt chấm | 0/0 |
| 27 | ĐỘI HÌNH GIẢ ĐỊNH MẠNH NHẤT (tiêu chí phụ, áp dụng từ 28/11). (a) Vài giờ trước | 5a2e0fc9d366 | 5a2e0fc9d366 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '27' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc | 4/4 |
| 28 | LỐI ĐÁ & TỶ LỆ CHUYỂN ĐỔI RA GÓC (tiêu chí bắt buộc cho kèo góc FT và góc H1, áp | c4cbb5e5ae76 | c4cbb5e5ae76 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '28' • áp cho: Góc FT, Góc H1 | 2/2 |
| 29 | KÈO THẺ – RR RIÊNG & ƯU TIÊN THEO TÍNH CHẤT TRẬN (áp dụng từ 28/11, theo người d | e799394475f8 | e799394475f8 | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '29' • áp cho: Thẻ | 7/7 |
| 30 | CHẤP GÓC FT (thị trường thứ 6, mọi giải, từ 28/11 theo người dùng). (a) CÁCH NGƯ | 6b62412dd08a | 6b62412dd08a | ✔ | Bộ máy chấm (engine.grade) • bước kiểm '30(c)' • áp cho: Chấp góc | 1/1 |

## 4. Chi tiết từng mục (văn bản A1 nguyên văn + bộ máy)

### Mục đầu — ✔ khớp (mã cdec39c938ac)
**A1:**

QUY CHUẨN CHUNG – ÁP DỤNG GIỐNG NHAU CHO MỌI TAB BÓNG ĐÁ (trừ tab NBA), MỌI GIẢI, MỌI NGÀY (bản 27/11/2026 23:59 – A1 = BỘ MÁY). Đây là bộ quy chuẩn CHUẨN, BẮT BUỘC áp đủ mục 0–30 cho mọi kèo, mọi giải, mọi ngày; không được bỏ sót mục nào. Bổ sung quy chuẩn ở tab nào thì áp ngay cho tất cả các tab bóng đá và các ngày sau; ngày cũ không chỉnh lại.

**Bộ máy:** Phần mở đầu – phạm vi áp dụng (mọi tab bóng đá, trừ NBA, RR tuần, Kèo đã vào)

### Mục 0 — ✔ khớp (mã c701ba9131ea)
**A1:**

0. A1 = BỘ MÁY (bắt buộc, từ 27/11 tối): (a) Văn bản A1 này giống hệt tệp rules/quy_chuan.md trong kho mã; mọi kèo chỉ được chấm bằng bộ máy chung rules/engine.py (không giải nào cài quy tắc riêng, KHÔNG chỉnh tier bằng tay); bảng đối chiếu rules/registry.py ghi mỗi mục 0–30 được thực hiện ở đâu (bộ máy chấm, mô hình, nạp dữ liệu, xếp ưu tiên, trình bày hay lịch chạy). (b) Thứ tự chấm cố định: mục 6 (giá) → 15 (đủ số liệu) → 16 (bất thường) → 8 (tier; thẻ theo 5, 24, 29) → 28 (góc) → 30(c) (chấp góc) → 14(8) → 14(8b) → 14(2) → 20(d) → 27 (đội hình) → 14(1) (giá đi ngược) → 23 (lịch) → 9 (Ưu tiên/TOP). (c) Mỗi kèo ghi cuối cột kết luận dòng 'Đã kiểm quy chuẩn: …' liệt kê từng mục đã kiểm và kết quả. (d) Sau khi ghi sheet: đọc ngược sheet và chạy rules/audit.py – chỉ báo kèo cho người dùng khi ĐẠT 0 lỗi (đủ mục bắt buộc cho từng thị trường theo bảng đối chiếu, tier trên sheet = bộ máy, Ưu tiên/TOP chỉ từ tier B trở lên, tối đa 2 Ưu tiên/trận, A1 ↔ bảng đối chiếu khớp). (e) PHẠM VI: mọi tab kèo bóng đá – Champions League, Ngoại hạng Anh, La Liga, Bundesliga, Europa League, J1 League và MỌI TAB GIẢI MỚI; KHÔNG áp cho tab 'Tổng kết RR tuần' và 'Kèo đã vào'. (f) MỌI THAY ĐỔI – rút bài học mới (ghi mục 14), cập nhật/bổ sung quy chuẩn phân tích, thêm tab kèo mới – đều phải sửa CÙNG LÚC và GIỐNG HỆT ở HAI PHÍA: (1) A1 của TẤT CẢ các tab kèo bóng đá (Champions League, Ngoại hạng Anh, La Liga, Bundesliga, Europa League, J1 League và mọi tab giải mới – cùng một văn bản, không tab nào khác tab nào); (2) BỘ MÁY, gồm văn bản gốc rules/quy_chuan.md (= A1), bộ chấm rules/engine.py + model.py, bảng đối chiếu rules/registry.py và ca kiểm ý nghĩa rules/kiem_thu.py. Bài học chỉ ghi chữ mà chưa vào bộ máy thì CHƯA có hiệu lực. Thiếu ở bất kỳ tab hay thành phần nào thì bước kiểm báo lỗi và không được báo kèo. (g) TAB KÈO MỚI: chỉ thêm phần nạp dữ liệu (nguồn mẫu 10 trận theo mục 1, khớp tên đội với giá Pinnacle, vị trí dòng); dùng nguyên bộ máy, khuôn ghi sheet và bước kiểm chung; A1 chép nguyên văn từ tab Champions League. (h) KÈO MỚI HOÀN TOÀN (loại kèo chưa có trong danh sách thị trường) – PHÂN TÍCH ĐÚNG BẰNG QUY CHUẨN CHUNG, KHÔNG ẢNH HƯỞNG KÈO ĐANG CÓ. MÃ THỊ TRƯỜNG: hc = Chấp bàn FT; tot = Tài/Xỉu bàn FT; cor = Góc FT; h1 = Góc H1; card = Thẻ FT; chc = Chấp góc FT. (1) PHẢI PHÂN TÍCH: loại kèo mới bắt buộc dùng PHẦN CHUNG của quy chuẩn như mọi kèo – mẫu 10 trận VĐQG + C1/EL/ACL (mục 1), tách sân (20), giá nhà cái thật (6), công thức xác suất ước tính/EV/tier A–B–C+–C (8, 18b), đủ số liệu (15), kèo bất thường (16), xu hướng 5 trận (14(8b)), lịch thi đấu (23), đội hình (27), Elo (25), xếp Ưu tiên/TOP (9) – cộng thêm mô hình xác suất riêng cho loại kèo đó (theo cách mục 19) và mục riêng nếu cần (ví dụ cờ lối đá mục 28 cho kèo góc). Kèo mới được chấm tier, được xét Ưu tiên/TOP và tính RR chung như kèo khác. (2) KHÔNG ẢNH HƯỞNG: thêm kèo mới KHÔNG được sửa bất kỳ ngưỡng, trọng số, thứ tự chấm hay danh sách mục bắt buộc nào của các thị trường đang có; danh sách mục bắt buộc của thị trường đang có được KHÓA (rules/khoa_thi_truong.json) – lệch là lỗi. Bước kiểm HỒI QUY: tier của mọi kèo cũ (giá không đổi) phải giữ nguyên như trước khi thêm kèo mới; Ưu tiên/TOP chỉ được thay đổi do kèo mới đủ điều kiện cạnh tranh theo mục 9. (3) CÁCH THÊM: làm cùng lúc cho TẤT CẢ các tab – A1 (thêm mã vào danh sách trên + cách người dùng ghi kèo, mô hình, mục riêng, vị trí ghi) + bộ máy (mô hình + đưa vào đường chấm chung) + bảng đối chiếu (phần chung + mục riêng) + khuôn sheet. Trạng thái 'CHỜ TÍCH HỢP' chỉ dùng tạm trong lúc đang dựng mô hình (chỉ lưu giá, chưa chấm, chưa báo, chưa tính RR); dựng xong phải chuyển ngay sang chính thức và chạy bước kiểm. (4) Bổ sung giá cho kèo còn thiếu của thị trường đã có KHÔNG phải thay đổi quy chuẩn: chỉ nhập giá rồi chạy lại bộ máy và bước kiểm. (i) A1 VÀ BỘ MÁY LUÔN GIỐNG HỆT – LỆCH LÀ DỪNG: bộ máy là đường phân tích DUY NHẤT cho mọi tab kèo bóng đá; bộ máy chỉ được thay đổi CÙNG LÚC và GIỐNG HỆT A1 (sửa đổi, bổ sung quy chuẩn, kèo mới hoàn toàn, bài học rút ra). Mỗi bản quy chuẩn có MÃ PHIÊN BẢN (12 ký tự đầu SHA-256 của văn bản A1 = rules/quy_chuan.md); bộ máy ghim mã này (registry.A1_VERSION) và mỗi tab kèo mang mã này trong siêu dữ liệu 'quy_chuan_a1' ghi cùng lúc với ô A1; ô A1 có cảnh báo khi sửa tay. TRƯỚC MỖI LẦN PHÂN TÍCH và trong bước kiểm, bộ chạy (rules/a1_sync.py) đối chiếu: mã của văn bản A1 = mã bộ máy = mã trên TẤT CẢ các tab; khi cần kiểm toàn văn thì so ghi chú A1 từng tab với quy_chuan.md từng ký tự. Lệch bất kỳ chỗ nào → NGỪNG PHÂN TÍCH NGAY, không chấm, không ghi sheet, không báo kèo, báo người dùng tab/nơi lệch; chỉ phân tích tiếp khi đã đồng bộ lại đủ A1 mọi tab + bộ máy. (j) SỬA ĐỔI – BỔ SUNG – BÀI HỌC PHẢI ĐỦ VÀ ĐÚNG Ý Ở CẢ A1 LẪN BỘ MÁY: (1) SỬA ĐỔI một quy chuẩn: nội dung mới phải giống nhau ở A1 và bộ máy – sửa ngưỡng, điều kiện, cách hạ tier, thị trường áp dụng trong A1 thì sửa đúng chỗ đó trong bộ máy, không bên nào còn giữ bản cũ. (2) BỔ SUNG quy chuẩn mới: thêm ĐẦY ĐỦ và ĐÚNG Ý ở cả hai – A1 ghi rõ điều kiện, tác động (hạ mấy bậc / tối đa tier nào / chỉ ghi chú, không nâng) và thị trường áp dụng; bộ máy cài đúng điều kiện và tác động đó, có bước kiểm hiện trong dòng 'Đã kiểm quy chuẩn'. (3) BÀI HỌC RÚT RA (mục 14) làm y như bổ sung quy chuẩn: chỉ có hiệu lực khi đã vào cả A1 lẫn bộ máy. (4) CÁCH KIỂM: mỗi mục 0–30 có MÃ MỤC riêng (12 ký tự đầu SHA-256 của chính văn bản mục đó) ghim trong bộ máy (registry.MUC_HASH) → sửa chữ mục nào trong A1 mà bộ máy chưa cập nhật mục đó (hoặc ngược lại) thì bộ chạy báo ĐÚNG MỤC bị lệch và DỪNG. Mỗi quy chuẩn do bộ máy chấm có CA KIỂM Ý NGHĨA (rules/kiem_thu.py): ví dụ dựng sẵn ghi rõ 'theo A1 thì kèo như thế này phải ra kết quả gì' – mọi ca phải ĐẠT trước mỗi lần phân tích; sửa đổi/bổ sung/bài học ở mục nào thì phải sửa/thêm ca kiểm của mục đó theo đúng ý mới; mục bộ máy chấm mà không có ca kiểm, hoặc có ca không đạt → DỪNG. (5) Sau mỗi lần sửa đổi/bổ sung/bài học: lập lại bảng đối chiếu A1 ↔ bộ máy (rules/DOI_CHIEU_A1_BO_MAY.md: từng mục A1, chỗ bộ máy thực hiện, ca kiểm ý nghĩa và kết quả, mã từng tab) và gửi người dùng xem.

**Bộ máy:** Quy trình theo lịch • rules/run_day.py → rules/audit.py (bắt buộc ĐẠT mới báo kèo)

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Kèo mới hoàn toàn thiếu hàm xu hướng 5 trận → bộ máy dừng, không chấm
- ✔ ĐẠT — Kèo mới hoàn toàn được chấm bằng phần chung (6, 8, 15, 16, 14(8b), 23, 27)

### Mục 1 — ✔ khớp (mã 041eb27e2e03)
**A1:**

1. Dữ liệu: 8–10 TRẬN GẦN NHẤT (mặc định 10, TỐI ĐA 10 – không lấy thêm để bám sát phong độ hiện tại) mỗi đội theo ngày đá thực tế, gồm giải VĐQG (giải cao nhất của nước đó) + C1 (Champions League) + Europa League (kể cả vòng loại). Không lấy cúp quốc nội, giao hữu, Conference League. Giải châu Á (J1 League…): cúp châu lục = AFC Champions League Elite/Two, tính như cúp châu Âu (bỏ sót ACL là sai mục 1 – lỗi J1 27/11).

**Bộ máy:** Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • run_day: mẫu 10 trận VĐQG + C1/EL (ACL với giải châu Á); audit kiểm đầu vào

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Mẫu chỉ VĐQG + C1/EL (+ACL); không cúp quốc nội

### Mục 2 — ✔ khớp (mã e27ad41f5a68)
**A1:**

2. Bù số liệu: trận thiếu góc/góc H1/thẻ → lấy trận cúp châu Âu gần nhất của đội đó (lùi dần theo thời gian) cho đủ 10 trận có số liệu; ghi '• BÙ SỐ LIỆU' ở cột Giải. Lấy số liệu từ TẤT CẢ các nguồn, nguồn nào đủ số liệu thì dùng (ESPN, FotMob, SofaScore, The Odds API, football-data.org, DFB/RFEF/PGMOL, web); không để trống nếu còn nguồn. Không dùng số liệu giả (toàn 0).

**Bộ máy:** Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • run_day: bù số liệu từ trận C1/EL gần nhất

### Mục 3 — ✔ khớp (mã d2a2163b7d65)
**A1:**

3. Bảng phong độ (cột L trở đi): 10 trận/đội + dòng 'TB 10 TRẬN' (T-H-B, bàn H1/FT, góc H1/H2/FT, góc đội/đối thủ, vàng, đỏ, thẻ quy đổi, cầm bóng, sút, sút trúng, phạm lỗi, cứu thua).

**Bộ máy:** Khuôn ghi sheet • khối phong độ BP2300+

### Mục 4 — ✔ khớp (mã eb31f57853de)
**A1:**

4. Khối 'TRỌNG TÀI CÁC TRẬN' ngay dưới bảng phong độ: tên, nguồn, số trận, vàng TB 12 tháng (FotMob) so với TB giải, đỏ, lỗi/trận, đánh giá (NHẸ TAY / TRUNG BÌNH / CHẶT TAY / MẪU MỎNG / CHỜ CÔNG BỐ) và ảnh hưởng tới kèo thẻ.

**Bộ máy:** Khuôn ghi sheet • khối trọng tài BP2520+

### Mục 5 — ✔ khớp (mã 7e7d5bb8fbdd)
**A1:**

5. Kèo thẻ BẮT BUỘC xét trọng tài và tính chất trận (mục 24) (SIẾT sau RR kỳ 0: thẻ 6T–12B = −7,47R): chỉ lên Tier B khi mẫu đội ≥ 70% VÀ trọng tài cùng chiều rõ (lệch ≥ ±0,5 vàng/trận so với TB giải, mẫu ≥ 10 trận) VÀ kỳ vọng thẻ (TB hai đội × hệ số trọng tài) lệch mốc ≥ 0,6; thiếu một điều kiện → Tier C; không vào Tài thẻ mốc thấp giá cao. Kèo thẻ tính RR RIÊNG và chỉ được ưu tiên theo mục 29.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '5' • áp cho: Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Thẻ: mẫu ≥ 70%, trọng tài cùng chiều ≥ 0,5, kỳ vọng lệch mốc ≥ 0,6, EV ≥ 5% → B
- ✔ ĐẠT — Thẻ: trọng tài thiếu mẫu (< 10 trận) → không lên B
- ✔ ĐẠT — Biên: trọng tài lệch +0,51 → B; +0,49 → không B
- ✔ ĐẠT — Biên: kỳ vọng thẻ lệch mốc 0,61 → B; 0,59 → không B
- ✔ ĐẠT — Biên: mẫu thẻ 70% → B; 69% → không B
- ✔ ĐẠT — Biên: trọng tài đủ 10 trận → xét B; 9 trận → không B
- ✔ ĐẠT — Biên: Thẻ EV 5,01% → B; 4,99% → không B
- ✔ ĐẠT — Thẻ C+: trọng tài ngược −0,49 → C+; −0,51 → C
- ✔ ĐẠT — Thẻ C+: mẫu co ≥ hòa vốn +3 → C+; +2,9 → C
- ✔ ĐẠT — Thẻ C+: EV 2,01% → C+; 1,99% → C
- ✔ ĐẠT — Thẻ C+: odds 1,65 → C+; 1,64 → C

### Mục 6 — ✔ khớp (mã 87970b0e64ec)
**A1:**

6. Trước trận: cập nhật liên tục; chốt 1 tiếng trước mỗi khung giờ (trọng tài, đội hình, odds, chấn thương), phân tích lại đủ 6 thị trường (chấp bàn, tài xỉu bàn, góc FT, góc H1, thẻ, chấp góc FT; J1 bỏ thẻ theo mục 29g), xếp lại tier, gửi người dùng 2 kèo tự tin nhất mỗi khung. Kèo/mốc/odds KHÔNG tìm được thì BỎ TRỐNG (không tự đoán, không bịa), người dùng sẽ tự điền; khi có giá thì chấm lại ngay theo đủ mục 8, 15, 16. Nguồn giá: chấp bàn và tài xỉu bàn lấy Pinnacle (Odds API) mới nhất; góc FT, góc H1, thẻ, chấp góc lấy giá người dùng gửi; KHÔNG dùng giá quy đổi từ 1X2 hay giá tự ước tính (có giá quy đổi → coi như chờ giá, tier C).

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '6' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Giá quy đổi từ 1X2 (không phải giá nhà cái) → coi như chờ giá, C

### Mục 7 — ✔ khớp (mã 88a54636765c)
**A1:**

7. Tin lực lượng: chấn thương, treo giò, đội hình dự kiến. Nhiều nguồn; không bịa số.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '27' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Tin lực lượng phản bác (hạ) → hạ 1 bậc
- ✔ ĐẠT — Đội hình giả định phản bác (tấn công đội mình theo ≤ 0,90) → hạ 1 bậc
- ✔ ĐẠT — Đội hình ủng hộ → chỉ điểm cộng, KHÔNG nâng (B giữ B)
- ✔ ĐẠT — Hai nguồn đội hình lệch (⚠) → chưa hạ
- ✔ ĐẠT — Biên: chỉ số đội hình 0,90 → hạ; 0,91 → không

### Mục 8 — ✔ khớp (mã e08386d5cddd)
**A1:**

8. Chấm kèo (BẢN THỬ từ 28/11 – (a)(b), so sánh với cách cũ ở tổng kết tuần 30/11): (a) mẫu = tỷ lệ đạt trong 10 trận hai đội (gộp, tính hoàn/thắng-thua nửa); MẪU CO VỀ THỊ TRƯỜNG = (mẫu + xác suất công bằng nhà cái)/2 trước khi tính EV và lợi thế; hòa vốn = 1/odds (giá người dùng nếu có). (b) Xác suất mô hình theo mục 19. Xác suất công bằng = (1/odds cửa chọn) ÷ (1/odds cửa chọn + 1/odds cửa kia). Xác suất ước tính = 40% mô hình + 30% mẫu đã co + 30% công bằng (thiếu giá cửa kia: 55% mô hình + 45% mẫu); EV% = xác suất ước tính × odds − 1. Tier A: EV ≥ 10%, EV mô hình ≥ 10%, lệch so với thị trường (ước tính − công bằng) ≤ 12 điểm %, mẫu thô nghiêng hơn thị trường, mẫu đã co ≥ hòa vốn, tin tức/trọng tài không phản bác. Kèo lệch thị trường > 12 điểm tối đa B trừ khi tin lực lượng giải thích được. Tier B: EV ≥ 5%, EV mô hình > 0, mẫu thô nghiêng hơn thị trường, mẫu đã co ≥ hòa vốn. C+ (mục 18b): EV ≥ 2%, mẫu đã co ≥ hòa vốn +3 điểm, odds ≥ 1,65, mô hình cùng chiều, mẫu ≥ 8. Mô hình NGƯỢC CHIỀU → tối đa C. Kèo thẻ vẫn theo mục 5. Chờ giá: kèo chưa có giá thật luôn tier C (không vào); nếu mẫu ≥ 65% và mô hình ≥ 58% thì ghi 'đủ B chờ giá' để chấm lại ngay khi có giá. Kết luận ghi 'mẫu x% / hòa vốn y% • EV +z% (mô hình w%) • kỳ vọng …' và '[Thử mục 8 (a)(b); tier cách cũ: …]'. Cách cũ (để so sánh): A = mẫu ≥ hòa vốn +25 điểm & EV ≥ 12%; B = mẫu ≥ hòa vốn +9 điểm, mẫu ≥ 55%, EV ≥ 5%.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '8' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Kèo chuẩn đủ điều kiện (EV ≥ 10%, EV mô hình ≥ 10%, lệch thị trường ≤ 12, mẫu nghiêng hơn thị trường) → A
- ✔ ĐẠT — EV 6% (≥ 5%), mô hình > 0 → B
- ✔ ĐẠT — Lệch thị trường > 12 điểm → tối đa B
- ✔ ĐẠT — Mẫu thô KHÔNG nghiêng hơn thị trường → không A/B
- ✔ ĐẠT — Mô hình ngược chiều (EV mô hình < 0) → tối đa C
- ✔ ĐẠT — C+: EV 3%, mẫu co ≥ hòa vốn +3, odds ≥ 1,65, mô hình cùng chiều → C+
- ✔ ĐẠT — Chưa có giá thật → luôn C (đủ B ghi "B chờ giá")
- ✔ ĐẠT — Biên A: EV 10,01% → A; EV 9,99% → B
- ✔ ĐẠT — Biên A: EV mô hình 10,01% → A; 9,99% → B
- ✔ ĐẠT — Biên A: lệch thị trường 11,99 điểm → A; 12,01 → B
- ✔ ĐẠT — Biên B: EV 5,01% → B; 4,99% → C+
- ✔ ĐẠT — Biên C+: odds 1,65 → C+; 1,64 → C
- ✔ ĐẠT — Biên C+: mẫu co ≥ hòa vốn + 3 điểm → C+; + 2 điểm → C
- ✔ ĐẠT — Biên "B chờ giá": mẫu 65% + mô hình 58% → ghi đủ B chờ giá; 64,9% hoặc 57,9% → không
- ✔ ĐẠT — Biên C+: EV 2,01% → C+; 1,99% → C

### Mục 9 — ✔ khớp (mã 378f413cce2e)
**A1:**

9. Mỗi trận tối đa 2 kèo ưu tiên ('Ưu tiên 1 • …', 'Ưu tiên 2 • …') và CHỈ chọn từ tier B trở lên; trận không có kèo B ghi 'KHÔNG VÀO'. Mỗi khung giờ '★ TOP 1 khung hh:mm' và '★ TOP 2 khung hh:mm' cũng chỉ từ tier B trở lên, xếp theo Tier (A trước) rồi EV% cao nhất; khi hai kèo cùng tier chênh EV ≤ 2 điểm thì ưu tiên kèo góc (góc FT, góc H1, chấp góc) (bài học RR kỳ 0); kèo ⚠ bất thường không được Ưu tiên; cửa đội có nguy cơ xoay tua (mục 23b) không được làm TOP; KÈO THẺ KHÔNG chiếm Ưu tiên 1/2/TOP (Ưu tiên thẻ 25–27/11: 1T–5B, −4,25R) – kèo thẻ có nhãn riêng 'Thẻ ưu tiên' theo mục 29; kèo GÓC H1 được ưu tiên khi chọn Ưu tiên/TOP nếu EV chênh ≤ 2 điểm (Ưu tiên góc H1 25–27/11: 6T–1B, +3,99R).

**Bộ máy:** Xếp Ưu tiên/TOP (engine.rank) • engine.rank

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Mỗi trận tối đa 2 Ưu tiên, chỉ tier A/B
- ✔ ĐẠT — Cùng tier, EV kém ≤ 2 điểm → kèo góc xếp TOP trên kèo bàn
- ✔ ĐẠT — Cửa có nguy cơ xoay tua không làm TOP

### Mục 10 — ✔ khớp (mã 67a5260315d9)
**A1:**

10. Trình bày thống nhất: Tier A nền xanh lá chữ trắng, B xanh dương chữ trắng, C nền xám chữ đen đậm (KHÔNG làm mờ chữ dòng tier C); Ưu tiên 1 vàng đậm, Ưu tiên 2 vàng nhạt; TOP 1 đỏ, TOP 2 cam; KHÔNG VÀO chữ đỏ; KHÔNG ĐỦ SỐ LIỆU và ⚠ KÈO BẤT THƯỜNG nền hồng chữ đỏ đậm; dòng TB xanh nhạt chữ đậm; KQ Thắng xanh/Thua đỏ/Hòa xám; trọng tài NHẸ TAY xanh, CHẶT TAY đỏ, TRUNG BÌNH vàng; BÙ SỐ LIỆU nghiêng xám; tiêu đề nền xanh đậm chữ trắng; mốc 1 số lẻ, odds 2 số lẻ. Câu chữ dạng 'Kèo @odds • mẫu x% / hòa vốn y% • kết luận'; không dán link.

**Bộ máy:** Khuôn ghi sheet • định dạng có điều kiện của tab

### Mục 11 — ✔ khớp (mã 1ce05d97aac1)
**A1:**

11. Tái sử dụng dữ liệu đã có trong file trước, chỉ tra web phần mới/thiếu.

**Bộ máy:** Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • tái dùng tệp đã tải (g/, d28/fm, j1/fm)

### Mục 12 — ✔ khớp (mã 200d821f672a)
**A1:**

12. Cách đếm thẻ: vàng = 1; đỏ trực tiếp = 2; 1 vàng rồi đỏ trực tiếp = 3; 2 vàng → đỏ = 2.

**Bộ máy:** Mô hình xác suất (model.py) • model / recs: thẻ = vàng + 2×đỏ

### Mục 13 — ✔ khớp (mã 07765d7683e0)
**A1:**

13. Sau trận: cập nhật kết quả liên tục (H1/FT, góc H1/FT, thẻ theo đội), chấm mọi kèo; chưa đủ số liệu ghi 'Chờ số liệu' và hẹn kiểm tra lại đến khi đủ; tính RR (TOP, Ưu tiên, Tier A/B/C, toàn bộ), chốt vé ở tab 'Kèo đã vào'.

**Bộ máy:** Quy trình theo lịch • lịch chấm kết quả sau trận

### Mục 14 — ✔ khớp (mã 8e33aaa35f86)
**A1:**

14. Bài học đã rút (C1 25–26/11): Tier C lỗ −7,67 RR → không vào Tier C; kèo thẻ thua nhiều → quy tắc mục 5; Tài góc/Tài bàn khi đội vắng mũi nhọn (Gala–Villa) → nay xử lý theo mục 27 (tối đa hạ 1 bậc, không hạ thẳng C); kèo chấp cho đội dưới cơ có trận thua ≤ −4 trong mẫu (PSV +2,5 thua 1–5) → ĐÃ BỎ hạ C từ 27/11, chỉ ghi lưu ý (xem (2)); Tài thẻ mốc thấp giá cao: Atlético–Viking Tài 3,5 thẻ @2,62 (từng chấm A, Ưu tiên 2) THUA – chỉ 3 thẻ; PSG–Roma Tài 3,5 thẻ @2,55 THUA – 2 thẻ → nhà cái đã định giá ít thẻ, mẫu đội không thắng được giá. RR kỳ 0 (25–26/11): Tier A +0,93R, Tier B +6,37R (giữ cách chọn B), Tier C −7,67R (áp mục 18b), thẻ −7,47R (siết mục 5), góc H1/góc FT ROI tốt nhất (13,6%/10,8%) → ưu tiên góc khi chọn TOP. KỲ 1 – EUROPA LEAGUE 27/11 (90 kèo): TOP 2T–2B −0,09R; 2 kèo ưu tiên 7T–11B −5,25R; Tier A 1T–1B −0,06R; Tier B 7T–10B −4,24R; Tier C 40T–28B–3H +6,71R; C+ ½R 4T–1H (+1,83R thực tế); toàn bộ +2,41R. Bài học: (1) KÈO BỊ THỊ TRƯỜNG ĐI NGƯỢC TRƯỚC GIỜ ĐÁ: Pinnacle dịch mốc chấp ngược cửa mình ≥ ¼ trái hoặc giá cửa mình tăng ≥ 5% kèm tin lực lượng (Sturm +1,5 khi Hoffenheim lên −1,75; Real Sociedad +0,5 khi Mateta trở lại) → cả 2 thua → từ nay hạ thẳng xuống C, bỏ khỏi Ưu tiên/TOP (không chỉ hạ 1 bậc). (2) Cửa dưới nhận chấp trước đội lớn hơn ≥ 150 Elo thua 2/3 (Sturm, Omonia; Jagiellonia thắng) trong khi 5 kèo cửa dưới bị hạ C theo bài học PSV (Hapoel, Levski, Lech, Celje, Lillestrøm) thắng cả 5 → ĐÃ BỎ hạ C theo bài học PSV từ 27/11 (bỏ lỡ +4,51R), chỉ ghi lưu ý trong kết luận. (3) Hai kèo ưu tiên cùng kịch bản trong 1 trận (cửa dưới nhận chấp + Xỉu bàn: Sturm/Omonia) thua cùng lúc −4R → ghi chú tương quan, ĐỀ XUẤT chờ người dùng duyệt. (4) Xỉu góc FT ưu tiên thua 3/4 (Celta, Dinamo, Sunderland – đội mạnh hơn dồn ép tạo góc) → theo dõi (mục 28 cờ DỒN ÉP TẠO GÓC). (5) Tier C dương kỳ này, âm kỳ 0 → dao động lớn, chưa đổi ngưỡng. (6) TÁCH KÈO THẺ (mục 29, tuần 23–29/11): bỏ thẻ ra thì RR chung +8,93R (ROI 6,2%), 2 kèo ưu tiên B+ +5,61R (ROI 14,0%) > tổng kèo; nhóm yếu nhất còn lại là CHẤP A/B 7T–8B–2H −1,46R → kèo chấp A/B bắt buộc qua kiểm tra đội hình (mục 27) và giá Pinnacle lúc chốt, tuần sau vẫn âm thì siết B chấp. (7) RÀ SOÁT SÂU 27/11 (trừ thẻ): ưu tiên đã chốt 7T–11B −5,25R vì chọn theo MẪU THÔ (mẫu dự báo 67%, thực tế 42%, thị trường 51% sát nhất); chấm lại bằng bản thử mục 8 thì ưu tiên 13T–8B–2H +3,69R, thêm quy tắc giá đi ngược thì +5,69R → giữ bản thử; 4 kèo Xỉu góc ưu tiên thua đều bị bản thử chấm C/C+ → kèo góc chỉ ưu tiên khi bản thử chấm B trở lên. (8) PHONG ĐỘ 5 TRẬN GẦN NHẤT (từ 27/11, người dùng chất vấn Shimizu +0,5 J1): mẫu 10 trận + tách sân có thể che mất sa sút ngắn hạn. Đội được chọn ở kèo chấp bàn/chấp góc (hoặc đội mình theo) có ≤ 2 điểm VÀ ghi ≤ 2 bàn trong 5 trận gần nhất, trong khi đối thủ ≥ 4 điểm → kèo theo đội đó tối đa C+ (½R), không Ưu tiên/TOP; ghi rõ số điểm/bàn 5 trận trong kết luận. (8b) XU HƯỚNG 5 TRẬN CỦA CHÍNH KÈO: với mọi kèo đạt B trở lên, tính tỷ lệ đạt của kèo đó trong 5 trận gần nhất của hai đội (gộp); ≤ 40% trong khi mẫu 10 trận nghiêng cửa mình → hạ 1 bậc (A → B, B → C+), ghi 'Mục 14(8b): 5 trận gần nhất x/y'. Rà soát 27/11 tối: MU–Brentford Xỉu 4,5 góc H1 (4/10) hạ A → B. (8c) Tin lực lượng/Agent Reach ỦNG HỘ kèo chỉ ghi điểm cộng, KHÔNG nâng tier (mục 27e) – đã sửa 2 kèo J1 bị nâng sai C → C+. Bài học mới sau mỗi ngày được thêm vào mục này và áp cho mọi tab.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '14(8), 14(8b), 14(2), 14(1)' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Đội được chọn ≤ 2 điểm và ≤ 2 bàn trong 5 trận, đối thủ ≥ 4 điểm → tối đa C+
- ✔ ĐẠT — Biên: đội chọn 2 điểm/2 bàn, đối thủ 4 điểm → tối đa C+
- ✔ ĐẠT — Biên: đội chọn 3 điểm → không áp 14(8)
- ✔ ĐẠT — Biên: đối thủ 3 điểm → không áp 14(8)
- ✔ ĐẠT — Biên: đội chọn ghi 3 bàn (2 điểm) → không áp 14(8)
- ✔ ĐẠT — Xu hướng 5 trận gần nhất của chính kèo ≤ 40% → hạ 1 bậc (A → B)
- ✔ ĐẠT — Biên: 5 trận gần nhất đạt đúng 40% (4/10) → hạ 1 bậc
- ✔ ĐẠT — Biên: đạt 50% (5/10) → không hạ
- ✔ ĐẠT — Biên: 4/9 (44%, có 1 trận hoàn) → không hạ
- ✔ ĐẠT — Cửa dưới nhận chấp trước đội mạnh hơn ≥ 150 Elo → chỉ ghi lưu ý, KHÔNG hạ
- ✔ ĐẠT — Biên: chênh đúng 150 Elo (tính +65 sân nhà) → ghi lưu ý; 149 → không
- ✔ ĐẠT — Biên: đội NHÀ nhận chấp trước khách mạnh hơn đúng 150 Elo → lưu ý; 149 → không
- ✔ ĐẠT — Giá Pinnacle đi ngược cửa chọn trước giờ đá → hạ thẳng C
- ✔ ĐẠT — Tin lực lượng ỦNG HỘ kèo chỉ ghi điểm cộng, KHÔNG nâng tier

### Mục 15 — ✔ khớp (mã c95c08d3b43d)
**A1:**

15. TRẬN KHÔNG ĐỦ SỐ LIỆU: đội nào có dưới 8 trận đủ số liệu góc/thẻ (J1 bỏ thẻ nên chỉ xét góc) (đã bù hết trận cúp châu Âu tìm được) → TOÀN BỘ kèo của trận đó xếp Tier C và cột kết luận ghi đầu dòng 'KHÔNG ĐỦ SỐ LIỆU PHÂN TÍCH (đội … chỉ có n trận có số liệu)'.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '15' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Đội có dưới 8 trận đủ số liệu góc/thẻ → cả trận C, ghi KHÔNG ĐỦ SỐ LIỆU
- ✔ ĐẠT — J1 chỉ xét số liệu góc (thiếu thẻ vẫn đủ)
- ✔ ĐẠT — Biên: đúng 8 trận đủ số liệu → vẫn chấm; 7 trận → C

### Mục 16 — ✔ khớp (mã cf37705765d5)
**A1:**

16. KIỂM TRA KÈO BẤT THƯỜNG (bắt buộc trước khi chấm tier): odds ảnh hưởng rất lớn tới kèo. Đánh dấu '⚠ KÈO BẤT THƯỜNG' khi: (a) kèo chấp sâu (+2,5/+3/+4 trở lên) mà odds cửa dưới ≥ 2,3–2,4 – TÙY ĐỐI THỦ: đội lớn theo ranking sức mạnh mục 25 (ClubElo ≥ 1800: Arsenal, Barca, Bayern, Real, Man City, PSG, Inter, Liverpool…) gặp đội cửa dưới quá yếu, ít tên tuổi thì chấp sâu và odds cao là BÌNH THƯỜNG; chỉ BẤT THƯỜNG khi hai đội sức mạnh gần nhau mà nhà cái vẫn cho chấp sâu với odds cao; (b) mốc rất thấp/rất dễ ăn (ví dụ Tài 0,5–1,5 bàn, Xỉu mốc rất cao, Tài góc/thẻ mốc thấp) mà odds lại cao; (c) KIỂM TRA GIÁ: (1) odds cao hơn giá Pinnacle/mặt bằng các nhà cái khác từ 15% trở lên (ví dụ Pinnacle 1,90 mà nhà cái cho 2,20 → +16%) → nghi giá cũ chưa cập nhật tin lực lượng, giá sai hoặc giá mồi – chỉ kiểm tra được khi có giá Pinnacle/nhà cái khác; (2) tổng 1/odds hai cửa: 1,02–1,10 là bình thường (1,90–1,90 → 1,053); dưới 1,00 là giá lỗi/giá cũ (2,10–2,05 → 0,964) → bất thường; trên 1,12 là giá quá xấu (1,60–1,60 → 1,25) → không bất thường nhưng không đáng vào; (d) odds/mốc biến động mạnh trong ngày mà không có tin lực lượng giải thích; (e) KÈO NGƯỢC PHONG ĐỘ RÕ RỆT: xem giá cả hai cửa cùng phong độ, đối chiếu công–thủ hai đội (bàn: A ghi với B lọt và ngược lại; góc: đánh giá cả hai đội; thẻ: TB thẻ hai đội × hệ số trọng tài). CHỈ coi là bất thường khi chênh lệch RÕ RỆT: phong độ nghiêng rất mạnh một cửa (mẫu ≥ 70% hoặc kỳ vọng vượt mốc từ 1,5 trở lên) mà giá cửa đó vẫn rất cao (≥ 2,30) – kiểu Atlético–Viking Tài 3,5 thẻ @2,62 (mẫu 70%) → thua. (f) KHÔNG coi là bất thường: giá 1,60–2,15 ở các mốc cơ bản (góc H1 4,5; thẻ 3,5–4,5; bàn 2,5–3,5; góc FT 9–10,5); mốc nhà cái cho sát kỳ vọng (kèo thẻ còn phụ thuộc diễn biến, tính cách trận); đội ghi nhiều gặp đội thủ chắc với giá cân bằng; giá lệch nhưng cùng chiều phong độ (Juventus Xỉu thẻ 1,47; Real Sociedad +0,5 @1,83); đội lớn châu Âu gặp đội nhỏ hơn được nhà cái tôn trọng (Olympiacos–Milan đồng banh @2,08 dù Olympiacos phong độ tốt) – CHỈ áp cho đội lớn gặp đội nhỏ (định nghĩa ở mục 25); hai đội lớn gặp nhau thì phải xét thêm nhiều yếu tố (lực lượng, động lực, sân nhà, đối đầu, vị trí bảng xếp hạng) rồi mới kết luận. Khi lệch nhẹ chỉ ghi 'lưu ý', không hạ tier. Bộ máy tự kiểm: (a) chấp ≥ 2,5 mà cửa dưới ≥ 2,30 khi hai đội chênh < 150 Elo; (b) Tài bàn mốc ≤ 1,5 mà giá ≥ 1,70; (c2) tổng 1/odds hai cửa < 1,00; (e) mẫu ≥ 70% hoặc kỳ vọng vượt mốc ≥ 1,5 theo cửa chọn mà giá ≥ 2,30; (g) đội mạnh hơn ≥ 200 Elo (tính sân nhà) chỉ chấp ≤ 1 mà giá đội mạnh ≥ 2,10; (c1)(d) kiểm qua mục 14(1) khi có 2 lần giá Pinnacle. (g) ĐỘI MẠNH GẶP ĐỘI YẾU MÀ KÈO CHẤP QUÁ NÔNG: đội mạnh (cả vị thế lẫn phong độ) gặp đội yếu/phong độ kém, đáng lẽ phải chấp sâu nhưng nhà cái chỉ cho chấp 0,5–1 mà giá đội mạnh lại cao bất thường → bất thường, không theo đội mạnh. Lưu ý so sánh trình độ giải. Kèo bất thường: tối đa Tier C, không chọn Ưu tiên/TOP; ghi đầu cột kết luận '⚠ KÈO BẤT THƯỜNG (lý do)', kiểm tra lại tin lực lượng, đội hình, giá các nhà cái khác trước khi kết luận và báo người dùng.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '16' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc, Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — (c2) Tổng 1/odds hai cửa < 1,00 → ⚠ bất thường, tối đa C
- ✔ ĐẠT — (b) Tài bàn mốc ≤ 1,5 mà giá ≥ 1,70 → bất thường, C
- ✔ ĐẠT — (e) Mẫu ≥ 70% mà giá ≥ 2,30 → bất thường, C
- ✔ ĐẠT — (a) Chấp ≥ 2,5 giữa hai đội chênh < 150 Elo mà cửa dưới ≥ 2,30 → bất thường, C
- ✔ ĐẠT — (g) Đội mạnh hơn ≥ 200 Elo chỉ chấp ≤ 1 mà giá ≥ 2,10 → bất thường, C
- ✔ ĐẠT — Kèo bất thường không được Ưu tiên/TOP
- ✔ ĐẠT — Biên (e): mẫu 70% @2,30 → bất thường; mẫu 69% @2,30 → không
- ✔ ĐẠT — Biên (e): mẫu 72% @2,29 → không bất thường
- ✔ ĐẠT — Biên (b): Tài 1,5 @1,70 → bất thường; @1,69 → không
- ✔ ĐẠT — Biên (g): chênh 200 Elo, chấp 1 @2,10 → bất thường; chênh 199 → không; @2,09 → không
- ✔ ĐẠT — Biên (a): chấp 2,5, cửa dưới @2,30, chênh 149 Elo → bất thường; 150 → không
- ✔ ĐẠT — Biên (c2): tổng 1/odds = 1,00 trở lên → không bất thường
- ✔ ĐẠT — (a) chỉ áp khi chấp từ 2,5: chấp 2,25 cửa dưới @2,30 chênh 149 → không bất thường
- ✔ ĐẠT — (a) cửa dưới @2,29 → không bất thường
- ✔ ĐẠT — (e) Tài: kỳ vọng vượt mốc 1,5 mà giá @2,30 → bất thường; vượt 1,4 → không
- ✔ ĐẠT — (e) Xỉu: kỳ vọng thấp hơn mốc 1,5 mà giá @2,30 → bất thường; 1,4 → không

### Mục 17 — ✔ khớp (mã d5d60086fa69)
**A1:**

17. BỐ CỤC BẮT BUỘC MỖI TAB (mọi giải, mọi ngày, giống hệt tab Champions League): khung hiển thị A5 gồm đủ 6 khối theo thứ tự: (1) DANH SÁCH KÈO • GIỜ VIỆT NAM (6 thị trường/trận – J1 5, ô thiếu để trống); (2) NHẬN ĐỊNH & TIER (trận, cửa, odds, tier, nguồn, mẫu 10 trận, cột TOP khung giờ, cột Ưu tiên); (3) ★ KÈO ƯU TIÊN MỖI KHUNG GIỜ (TOP 1 – TOP 2 của từng khung, kèm kết quả và thực tế); (4) 2 KÈO / HƯỚNG ƯU TIÊN MỖI TRẬN (kèm kết quả, TOP, thực tế); (5) KẾT QUẢ CÁC TRẬN • RR: mỗi trận ghi tỷ số H1|FT, Ưu tiên 1 → KQ, Ưu tiên 2 → KQ, RR 2 kèo ưu tiên, góc FT, thẻ FT, TOP → KQ; trận không có kèo B ghi 'Không vào'; (6) BẢNG RR THEO NHÓM: ★ TOP khung giờ, 2 kèo ưu tiên/trận, Tier A, Tier B, Tier C, toàn bộ kèo có odds (tất cả TRỪ THẺ) và dòng 'KÈO THẺ • RR RIÊNG (mục 29)' – cột Thắng/Thua/Hoàn/Chờ số liệu/Đã chốt/Tổng RR/ROI. Quy ước RR: 1R/kèo; thắng = odds−1; thắng nửa = (odds−1)/2; hoàn = 0; thua nửa = −0,5; thua = −1; ROI = tổng RR / số kèo đã chốt. Sau trận ghi cột Thực tế (H1 x–y | FT x–y | Góc H1 n | Góc FT a–b = n | Vàng a–b = n thẻ | Đỏ…) và cột Kết quả (Thắng/Thua/Hoàn/Thắng nửa/Thua nửa/Chờ số liệu) để bảng RR tự tính. Tab mới hoặc ngày mới phải dựng đủ 6 khối này trước khi phân tích; thiếu khối nào là sai quy chuẩn.

**Bộ máy:** Khuôn ghi sheet • khung A5 6 khối

### Mục 18 — ✔ khớp (mã 49c86f641233)
**A1:**

18. RR LÀ THƯỚC ĐO HIỆU QUẢ PHÂN TÍCH: RR cao trên mọi nhóm kèo = cách phân tích đang tốt; RR thấp/âm = BẮT BUỘC đổi cách phân tích. (a) TỔNG KẾT TUẦN: mỗi tuần 1 lần gộp RR của cả 5 tab bóng đá (theo giải, theo nhóm TOP/Ưu tiên/Tier A/B/C, theo thị trường chấp/bàn/góc FT/góc H1, theo lý do chọn; kèo thẻ tổng kết RIÊNG theo mục 29), ghi vào tab 'Tổng kết RR tuần', rút bài học vào mục 14 và chỉnh ngưỡng/quy tắc nếu nhóm nào RR âm 2 tuần liên tiếp. (b) NÂNG RR TIER C cho CẢ 5 TAB BÓNG ĐÁ (không chỉ khuyên bỏ): số liệu đầu tiên đã có kết quả (C1 25–26/11; Europa, Ngoại hạng Anh, La Liga, Bundesliga cộng dồn ngay khi có kết quả) – Tier C 25T–28B = −7,67R (thẻ −3,24; bàn −1,67; góc FT −1,32; góc H1 −1,10; chấp −0,34; lý do 'không lợi thế' −2,64, 'mẫu mỏng' −2,18, 'trọng tài ngược' −1,50) vì kèo C chỉ nhỉnh hòa vốn nên ra kết quả như tung đồng xu. Cách nâng: (1) TÌM MỐC TỐI ƯU: với mỗi kèo C, thử các mốc/cửa thay thế (mốc ¼, mốc ±1, cửa ngược, chấp châu Á thay 1X2) và chọn mốc có lợi thế lớn nhất so với giá – chỉ giữ nếu lợi thế ≥ +5 điểm; (2) ĐỐI CHIẾU KÉP: mẫu tỷ lệ + kỳ vọng công–thủ (mục 16e) + trọng tài (kèo thẻ) phải CÙNG CHIỀU mới được xét C+; lệch chiều thì loại hẳn, không để C tham khảo; (3) LOẠI GIÁ THẤP: không chọn cửa C có odds < 1,65 (biên nhà cái nuốt hết lợi thế); (4) MẪU ĐỦ: kèo C do mẫu mỏng chỉ xét lại khi đã bù đủ ≥ 8 trận; (5) PHÂN HẠNG C+ / C: C+ = lợi thế +5 đến +9 điểm, đủ (2)(3)(4), ghi 'C+ • ½R' trong kết luận (khuyến nghị nửa vốn); C còn lại ghi 'C • không vào'. Bảng RR tính riêng C+ và C để theo dõi; nếu C+ RR dương 2 tuần liên tiếp thì nâng ngưỡng B xuống tương ứng, nếu âm thì siết điều kiện C+. (c) Mọi thay đổi cách phân tích do RR tuần đều ghi rõ vào mục 14 và áp ngay cho cả 5 tab.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '8' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc • C+ trong model.tier; tổng kết tuần theo lịch

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Kèo chuẩn đủ điều kiện (EV ≥ 10%, EV mô hình ≥ 10%, lệch thị trường ≤ 12, mẫu nghiêng hơn thị trường) → A
- ✔ ĐẠT — EV 6% (≥ 5%), mô hình > 0 → B
- ✔ ĐẠT — Lệch thị trường > 12 điểm → tối đa B
- ✔ ĐẠT — Mẫu thô KHÔNG nghiêng hơn thị trường → không A/B
- ✔ ĐẠT — Mô hình ngược chiều (EV mô hình < 0) → tối đa C
- ✔ ĐẠT — C+: EV 3%, mẫu co ≥ hòa vốn +3, odds ≥ 1,65, mô hình cùng chiều → C+
- ✔ ĐẠT — Chưa có giá thật → luôn C (đủ B ghi "B chờ giá")
- ✔ ĐẠT — Biên A: EV 10,01% → A; EV 9,99% → B
- ✔ ĐẠT — Biên A: EV mô hình 10,01% → A; 9,99% → B
- ✔ ĐẠT — Biên A: lệch thị trường 11,99 điểm → A; 12,01 → B
- ✔ ĐẠT — Biên B: EV 5,01% → B; 4,99% → C+
- ✔ ĐẠT — Biên C+: odds 1,65 → C+; 1,64 → C
- ✔ ĐẠT — Biên C+: mẫu co ≥ hòa vốn + 3 điểm → C+; + 2 điểm → C
- ✔ ĐẠT — Biên "B chờ giá": mẫu 65% + mô hình 58% → ghi đủ B chờ giá; 64,9% hoặc 57,9% → không
- ✔ ĐẠT — Biên C+: EV 2,01% → C+; 1,99% → C

### Mục 19 — ✔ khớp (mã 7e7d6be2a5b5)
**A1:**

19. MÔ HÌNH XÁC SUẤT (mẫu tối đa 10 trận/đội): (a) Bàn thắng – Poisson: tấn công/phòng ngự mỗi đội lấy theo mục 20 (sân nhà/sân khách), trộn xG theo mục 22, nhân hệ số giải mục 21; λ đội nhà = (tấn công nhà + phòng ngự khách)/2, λ đội khách = (tấn công khách + phòng ngự nhà)/2; hiệu số kỳ vọng = 75% từ số liệu + 25% từ Elo (mục 25): (Elo nhà − Elo khách + 65)/220 bàn. Tính đủ kèo châu Á ¼ (thắng/thua nửa, hoàn). (b) Góc FT: kỳ vọng = (góc đội nhà được hưởng + góc đội khách để đối thủ hưởng)/2 + (góc đội khách được hưởng + góc đội nhà để đối thủ hưởng)/2; phân phối nhị thức âm (phương sai 1,35 × TB). (c) Góc H1: TB góc H1 hai đội (tách sân), phương sai 1,3 × TB. (d) Thẻ: TB thẻ trận hai đội (tách sân) × hệ số trọng tài (vàng TB trọng tài ÷ TB giải, khi ≥ 10 trận) × hệ số tính chất trận (mục 24), phương sai 1,6 × TB. (e) Mô hình chỉ là một thành phần của EV (mục 8), không thay thế mẫu và tin tức.

**Bộ máy:** Mô hình xác suất (model.py) • model.evaluate, model.chc_eval

### Mục 20 — ✔ khớp (mã c7c4b84d609e)
**A1:**

20. SÂN NHÀ / SÂN KHÁCH (bắt buộc tách): (a) Trong 10 trận gần nhất, đội nhà lấy các trận SÂN NHÀ, đội khách lấy các trận SÂN KHÁCH; số liệu dùng = trọng số cùng sân × TB cùng sân + phần còn lại × TB cả 10 trận, trọng số cùng sân = 60% khi có ≥ 5 trận cùng sân (ít hơn giảm theo tỷ lệ: 4 trận 48%, 3 trận 36%…). (b) Lợi thế sân nhà ≈ +65 Elo (≈ 0,3 bàn) đã tính trong mô hình; sân trung lập bỏ lợi thế này. (c) Bảng phong độ ghi thêm thành tích sân nhà của đội nhà và sân khách của đội khách (T-H-B, bàn ghi/lọt). (d) Đội khách chấp từ 1 trái trở lên mà thắng cách biệt ≥ mốc chấp ở dưới 50% trận sân khách → hạ 1 bậc; đội nhà nhận chấp mà thua ≤ 1 bàn ở ≥ 70% trận sân nhà → ghi điểm cộng cho cửa dưới.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '20(d)' • áp cho: Chấp bàn • (a)(b) trong model.vblend

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Đội khách chấp ≥ 1 mà thắng cách biệt ≥ mốc < 50% trận sân khách → hạ 1 bậc
- ✔ ĐẠT — Biên: khách chấp 1 thắng cách biệt đúng 50% trận sân khách → không hạ; 33% → hạ
- ✔ ĐẠT — Biên: khách chấp 1 thắng cách biệt 4/9 trận sân khách (44%) → hạ
- ✔ ĐẠT — Nhà nhận chấp thua ≤ 1 bàn ở 70% trận sân nhà → điểm cộng; 6/9 (67%) → không

### Mục 21 — ✔ khớp (mã 2c6531a1a9dc)
**A1:**

21. HỆ SỐ GIẢI (thông số PHỤ, chỉ dùng khi hai đội khác giải – cúp châu Âu): hệ số riêng theo bảng UEFA 5 năm (kassiesa, mùa 26/27): Anh 108,2; Ý 92,6; TBN 87,9; Đức 85,4; Pháp 72,7; BĐN 69,8; Bỉ 64,1; Hà Lan 56,4; Thổ 53,9; Hy Lạp 47,6; Séc 46,3; Ba Lan 45,7; Na Uy 41,4; Đan Mạch 40,8; Síp 35,4; Thụy Sĩ 32,2; Áo 29,7; Hungary 29,3; Croatia 27,9; Thụy Điển 27,0; Scotland 26,9; Israel 24,1; Slovenia 23,6; Bulgaria 22,1; Armenia 15,8. Hệ số điều chỉnh = (hệ số giải đội A ÷ hệ số giải đội B)^0,08, giới hạn 0,93–1,07, nhân vào kỳ vọng bàn của đội A và chia cho đội B. Chỉ là thông số phụ: ở cúp châu Âu mỗi đội có toan tính và sức mạnh riêng, không dùng hệ số giải để lật kết luận khi mẫu, mô hình và tin tức cùng chiều. Cập nhật bảng hệ số mỗi tháng.

**Bộ máy:** Mô hình xác suất (model.py) • model.evaluate tham số coef (trận khác giải)

### Mục 22 — ✔ khớp (mã 81e2e0001bfd)
**A1:**

22. xG (khi tra được): lấy xG ghi/lọt của từng trận trong 10 trận mẫu (FotMob/SofaScore); đội có ≥ 6 trận có xG thì tấn công = 50% bàn thực tế + 50% xG ghi, phòng ngự = 50% bàn lọt + 50% xG lọt; dưới 6 trận không dùng. Ghi xG TB vào bảng phong độ.

**Bộ máy:** Mô hình xác suất (model.py) • model.evaluate tham số xg

### Mục 23 — ✔ khớp (mã 200634f1b072)
**A1:**

23. ĐỘNG LỰC & LỊCH THI ĐẤU (bắt buộc ghi): số ngày nghỉ từ trận trước, trận kế tiếp (đối thủ, giải, cách mấy ngày), vị trí bảng xếp hạng/mục tiêu (đua vô địch, suất châu Âu, trụ hạng, đã chắc đi tiếp/bị loại). Lịch chỉ xét VĐQG + C1/EL (ACL với giải châu Á), bỏ cúp quốc nội. (a) Nghỉ < 3 ngày hoặc vừa đá C1/EL/ACL cách ≤ 4,5 ngày → đội đó mệt, ghi lưu ý; (b) trận kế tiếp cách ≤ 4 ngày lịch là C1/EL/ACL, hoặc gặp đội Elo ≥ 1800, hoặc derby (danh sách rules/derby.json) → NGUY CƠ XOAY TUA: không chọn cửa đội đó (chấp bàn/chấp góc) làm TOP, kèo theo cửa đối thủ được ghi điểm cộng; (c) đội hết động lực (đã chắc suất/đã bị loại/giữa bảng cuối mùa – ghi vào rules/tinh_chat_<ngày>.json) mà phải chấp từ 1 trái trở lên → không theo, tối đa C; (d) mục 23 chỉ hạ hoặc cộng điểm khi có thông tin rõ, không tự đoán đội hình.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '23' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Đội được chọn có nguy cơ xoay tua (trận C1/EL/ACL, Elo ≥ 1800 hoặc derby ≤ 4 ngày) → không làm TOP, tier giữ nguyên
- ✔ ĐẠT — (c) Đội hết động lực mà phải chấp ≥ 1 → tối đa C

### Mục 24 — ✔ khớp (mã 0a40c7974de7)
**A1:**

24. TÍNH CHẤT TRẬN CHO KÈO THẺ (nhân vào kỳ vọng thẻ): derby/kình địch ×1,15; trận quyết định (đua vô địch, trụ hạng, phải thắng mới đi tiếp, loại trực tiếp) ×1,10; hai đội phạm lỗi nhiều (TB ≥ 13 lỗi/trận mỗi đội) ×1,05; trận chênh lệch lớn (Elo chênh ≥ 250) ×0,92; trận hết động lực ×0,92. Tài thẻ chỉ xét B khi hệ số ≥ 1,0; derby/trận quyết định thì không vào Xỉu thẻ. Ghi hệ số đã dùng trong cột kết luận kèo thẻ (derby lấy từ rules/derby.json; trận quyết định, phạm lỗi nhiều, hết động lực ghi vào rules/tinh_chat_<ngày>.json khi phân tích). Bộ máy: Tài thẻ có hệ số < 1,0 tối đa C+; derby/trận quyết định → Xỉu thẻ tier C.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '24' • áp cho: Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Tài thẻ khi hệ số tính chất < 1,0 (hết động lực) → tối đa C+
- ✔ ĐẠT — Derby / trận quyết định → không vào Xỉu thẻ (C)
- ✔ ĐẠT — Biên: Tài thẻ hệ số đúng 1,0 → được B
- ✔ ĐẠT — Hệ số: derby ×1,15; trận quyết định ×1,10; phạm lỗi nhiều ×1,05; hết động lực ×0,92

### Mục 25 — ✔ khớp (mã 06f00223529f)
**A1:**

25. RANKING SỨC MẠNH & ĐỊNH NGHĨA ĐỘI LỚN: dùng ClubElo (clubelo.com, cập nhật trước mỗi ngày phân tích; Opta Power Rankings để đối chiếu khi tra được). ĐỘI LỚN = Elo ≥ 1800 (khoảng top 45 châu Âu). ĐỘI LỚN GẶP ĐỘI NHỎ = đội lớn hơn đối thủ ≥ 150 Elo → chấp sâu/odds cao cửa dưới là bình thường (mục 16a, 16f). Hai đội chênh < 150 Elo = sức mạnh gần nhau → chấp sâu với odds cao là BẤT THƯỜNG; hai đội đều ≥ 1800 = đội lớn gặp nhau → xét thêm lực lượng, động lực, sân nhà, đối đầu, bảng xếp hạng. Ghi Elo hai đội trong kết luận kèo chấp. Giải không có ClubElo (J1…): Elo ước tính = 1500 + 110 × hiệu số bàn/trận theo bảng xếp hạng.

**Bộ máy:** Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit) • ClubElo / Elo ước tính; dùng ở 14(2), 16, 23, 29

### Mục 26 — ✔ khớp (mã da6339b745f4)
**A1:**

26. RÀ SOÁT RR SAU MỖI TRẬN/MỖI LƯỢT CHẤM (bắt buộc): (a) Với từng nhóm (TOP, 2 kèo ưu tiên, Tier A, B, C+, C, toàn bộ – đều TRỪ THẺ; thêm theo thị trường chấp/bàn/góc FT/góc H1; kèo thẻ rà soát RIÊNG theo mục 29) so RR THỰC TẾ với RR KỲ VỌNG = tổng EV lúc chốt; độ lệch chuẩn = √Σ[p(odds−1)² + (1−p) − EV²]; z = (thực tế − kỳ vọng)/độ lệch chuẩn. (b) |z| < 1,5: dao động bình thường, ghi nhận. |z| ≥ 1,5: BẤT THƯỜNG → bắt buộc tìm nguyên nhân. |z| ≥ 2: bắt buộc sửa cách phân tích ngay (ghi mục 14, áp cho cả 5 tab), không chờ tổng kết tuần. Áp cho cả RR tăng bất thường (tìm xem có phải may mắn hay quy tắc đang loại nhầm kèo tốt, ví dụ nhóm bị hạ C nhưng thắng nhiều). (c) Cách tìm nguyên nhân: hiệu chuẩn (tỷ lệ thắng dự báo của mẫu/mô hình/thị trường so với thực tế, Brier); RR theo mức lệch so với thị trường; theo thị trường; theo lý do hạ/nâng tier (PSV, Gala–Villa, thẻ, thiếu số liệu); từng kèo thua lớn: tin lực lượng, xoay tua, giá đi ngược trước giờ đá, diễn biến (thẻ đỏ, phạt đền) hay ngẫu nhiên. (d) Ghi bảng 'RÀ SOÁT RR SAU TRẬN' vào tab 'Tổng kết RR tuần' (nhóm, số kèo, RR thực tế, kỳ vọng, chênh lệch, độ lệch chuẩn, z, đánh giá; hiệu chuẩn; nguyên nhân; xử lý) và báo người dùng ngay sau mỗi lượt chấm. (e) KIỂM SOÁT KÈO ƯU TIÊN (bắt buộc, theo yêu cầu người dùng): kèo Ưu tiên/TOP là kèo trọng tâm, phải tốt hơn tổng kèo. Sau mỗi ngày so ROI '2 kèo ưu tiên' với ROI 'tổng kèo' và 'kèo không ưu tiên'; Ưu tiên ROI thấp hơn tổng kèo hoặc âm → bắt buộc rà soát TỪNG kèo ưu tiên thua (vì sao chọn, mẫu/mô hình/thị trường nói gì, tin lực lượng, giá đi ngược, diễn biến) và ghi nguyên nhân, cách sửa vào mục 14. Cộng dồn 25–27/11: Ưu tiên B+ 24T–19B–2H +2,36R (ROI +5,2%) vs tổng kèo +2,04R (ROI +1,1%), kèo không ưu tiên +3,17R (ROI +2,5%); ngày 27/11 Ưu tiên −5,25R trong khi tổng +2,41R → chưa đạt. Mỗi kèo Ưu tiên khi chốt phải qua bảng kiểm tra kép: đội hình chính thức/dự kiến không phản bác (mục 27); lối đá không phản bác với kèo góc (mục 28); giá Pinnacle không đi ngược (mục 14); mô hình và mẫu đã co cùng chiều, EV ≥ 5%; không phải kèo thẻ; lý do chọn ghi rõ trong kết luận.

**Bộ máy:** Quy trình theo lịch • review/ sau mỗi lượt chấm

### Mục 27 — ✔ khớp (mã 5a2e0fc9d366)
**A1:**

27. ĐỘI HÌNH GIẢ ĐỊNH MẠNH NHẤT (tiêu chí phụ, áp dụng từ 28/11). (a) Vài giờ trước trận, dựng cho mỗi đội 1 đội hình 11 người mạnh nhất có thể ra sân, dựa trên 10 trận mẫu (mục 1): số phút, số trận đá chính, điểm FotMob, giá trị cầu thủ, các trận quan trọng (C1/EL, đại chiến) → chỉ số chất lượng từng cầu thủ; giữ sơ đồ quen thuộc (số hậu vệ/tiền vệ/tiền đạo hay dùng nhất). (b) Xác suất ra sân: vắng chắc chắn (chấn thương, treo giò được xác nhận) = 0; tin nghi ngờ/chưa xác thực xếp theo % độ tin tưởng (mặc định 50%); xoay tua do lịch dày (mục 23), trận ít quan trọng hoặc trước trận lớn → giảm 10–30% cho trụ cột. (c) Đối chiếu với đội hình dự kiến của FotMob (độ trùng x/11) và lấy trung bình hai nguồn. (d) Tính chỉ số TẤN CÔNG (tiền vệ + tiền đạo), PHÒNG NGỰ (thủ môn + hậu vệ) và TỔNG so với đội hình trung bình trong 10 trận mẫu: ≤ 0,90 = YẾU HƠN mẫu (mẫu đang đánh giá cao đội này), ≥ 1,10 = MẠNH HƠN mẫu. Ghi vào cột BK 'Đội hình giả định (mục 27)' và vào kết luận AY của kèo liên quan. (e) Ảnh hưởng tối đa ±1 bậc tier: đội hình phản bác kèo → hạ 1 bậc (A → B, B → C+, C+ → C). Bộ máy áp: chấp bàn – đội mình theo có tấn công hoặc phòng ngự ≤ 0,90; chấp góc – đội mình theo có tấn công ≤ 0,90; Tài bàn/góc/góc H1 – một trong hai đội tấn công ≤ 0,90; Xỉu bàn – một trong hai đội phòng ngự ≤ 0,90 (chỉ số = trung bình đội hình giả định và FotMob dự kiến); đội hình ủng hộ kèo → chỉ ghi 'điểm cộng', không nâng tier. Hai nguồn lệch nhau (trùng ≤ 6/11 hoặc chênh ngược chiều > 0,2) → chưa hạ, ghi ⚠ và chờ đội hình chính thức. (f) Khi có đội hình chính thức (khoảng 1 giờ trước trận, lúc chốt): so với đội hình giả định (ai vào/ra), tính lại chỉ số; nếu xác nhận yếu hơn mẫu ≥ 10% ở phần phản bác kèo → hạ 1 bậc, bỏ khỏi Ưu tiên/TOP; ghi kết quả đối chiếu vào AY. (g) Đây chỉ là 1 tiêu chí phụ bên cạnh mẫu, mô hình, thị trường; không tự tạo kèo và không dùng một mình để phán đoán. Sau mỗi tuần rà soát RR các kèo có/không có cờ đội hình để đánh giá tiêu chí.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '27' • áp cho: Chấp bàn, Tài/Xỉu bàn, Góc FT, Góc H1, Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Đội hình giả định phản bác (tấn công đội mình theo ≤ 0,90) → hạ 1 bậc
- ✔ ĐẠT — Đội hình ủng hộ → chỉ điểm cộng, KHÔNG nâng (B giữ B)
- ✔ ĐẠT — Hai nguồn đội hình lệch (⚠) → chưa hạ
- ✔ ĐẠT — Biên: chỉ số đội hình 0,90 → hạ; 0,91 → không

### Mục 28 — ✔ khớp (mã c4cbb5e5ae76)
**A1:**

28. LỐI ĐÁ & TỶ LỆ CHUYỂN ĐỔI RA GÓC (tiêu chí bắt buộc cho kèo góc FT và góc H1, áp dụng từ 28/11; kèo góc đang có RR tốt nhất). (a) Từ 10 trận mẫu (FotMob, tách sân theo mục 20), ghi cho mỗi đội: cầm bóng %; hướng tấn công cánh trái + phải / trung lộ % (≥ 72% cánh = ĐÁ CÁNH, ≤ 66% = TRUNG LỘ); số quả tạt/trận (≥ 20 tạt nhiều, ≤ 13 ít tạt) và số quả tạt đối thủ được phép thực hiện; chạm bóng trong vòng cấm đối thủ (ghi/để lọt); số cú đánh đầu (≥ 2,5 cú + tạt ≥ 17 = TẠT CÁNH ĐÁNH ĐẦU); cú sút bị chặn; góc được hưởng/để đối thủ hưởng FT và H1. (b) TỶ LỆ CHUYỂN ĐỔI RA GÓC: góc/quả tạt (≥ 0,33 cao, ≤ 0,20 thấp), góc/chạm bóng vòng cấm; và chiều ngược lại cho phòng ngự (góc thủng/quả tạt của đối thủ). (c) KỲ VỌNG GÓC THEO LỐI ĐÁ mỗi đội = trung bình của [(tạt của đội + tạt đối thủ cho phép)/2 × (chuyển đổi của đội + chuyển đổi đối thủ để thủng)/2] và cách tính tương tự với chạm bóng vòng cấm; cộng hai đội = kỳ vọng FT; H1 theo tỷ lệ góc H1 của hai đội. Cầm bóng dự kiến = (cầm bóng đội nhà + 100 − cầm bóng đội khách)/2. (d) CỜ LỐI ĐÁ: DỒN ÉP TẠO GÓC (một đội dự kiến cầm bóng ≥ 57%, đá cánh/tạt nhiều, đối thủ để chạm vòng cấm ≥ 27/trận) → bất lợi Xỉu góc (bài học EL 27/11: đội mạnh dồn ép làm thua Xỉu góc); TẠT GẶP ĐỐI THỦ CHO TẠT (đội tạt ≥ 17 gặp đối thủ cho tạt ≥ 21 và dự kiến ≥ 5,8 góc) → bất lợi Xỉu góc; HAI ĐỘI ĐÁ CÁNH + TẠT NHIỀU (cánh ≥ 72% và tạt ≥ 17 cả hai) → bất lợi Xỉu góc; HAI ĐỘI ÍT TẠT (≤ 15), HAI ĐỘI ĐÁ TRUNG LỘ (≤ 66%) hoặc HAI ĐỘI CHUYỂN ĐỔI THẤP (góc/tạt ≤ 0,22) → bất lợi Tài góc. (e) Ảnh hưởng (giống mục 27): cờ phản bác kèo đang chọn → hạ 1 bậc (A → B, B → C+, C+ → C) và bỏ khỏi Ưu tiên/TOP nếu xuống dưới B; cờ ủng hộ → chỉ ghi 'điểm cộng', không nâng tier; kỳ vọng theo lối đá gần như trùng mô hình mục 19 nên KHÔNG dùng riêng con số kỳ vọng để đổi tier, chỉ dùng cờ. Ghi vào cột BL 'Lối đá & góc (mục 28)' ở dòng Góc FT và Góc H1 của mỗi trận, và tóm tắt trong kết luận AY của kèo góc ưu tiên. (f) Kiểm chứng ban đầu trên 18 trận EL 27/11: cờ lối đá đúng 6 – sai 3 – hoàn 1 (mẫu rất nhỏ); 3 kèo Xỉu góc FT thua (Beşiktaş, Celta, Dinamo) không bị cờ nào bắt → tiếp tục theo dõi, tổng kết tuần 30/11 so RR kèo góc có cờ ủng hộ / phản bác / trung tính để chỉnh ngưỡng.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '28' • áp cho: Góc FT, Góc H1

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Góc: cờ lối đá PHẢN BÁC cửa chọn → hạ 1 bậc (A → B)
- ✔ ĐẠT — Góc: cờ lối đá ỦNG HỘ → chỉ điểm cộng, không nâng

### Mục 29 — ✔ khớp (mã e799394475f8)
**A1:**

29. KÈO THẺ – RR RIÊNG & ƯU TIÊN THEO TÍNH CHẤT TRẬN (áp dụng từ 28/11, theo người dùng). (a) Kèo thẻ phụ thuộc nhiều vào diễn biến trên sân (thẻ đỏ, tỷ số, cách điều hành) nên không đòi hỏi RR cao như các kèo khác, nhưng KHÔNG được bỏ qua: mọi trận vẫn phân tích đủ mục 4, 5, 24 (trọng tài, mẫu đội, tính chất trận). (b) TÁCH RR: kèo thẻ KHÔNG tính vào khung RR chung (TOP, 2 kèo ưu tiên, Tier A/B/C, toàn bộ kèo, rà soát mục 26, tổng kết tuần mục 18); có bảng 'KÈO THẺ • RR RIÊNG' ở mỗi tab và ở tab 'Tổng kết RR tuần' (theo tier, Tài/Xỉu, loại trận). Các kèo còn lại (chấp, bàn, góc FT, góc H1) phải phân tích chuẩn xác và được đánh giá bằng RR chung. (c) PHÂN LOẠI TRẬN cho kèo thẻ theo Elo (mục 25), chênh = |Elo nhà + 65 − Elo khách|: CÂN BẰNG < 100; CHÊNH VỪA 100–199; QUÁ LỆCH ≥ 200. TRẬN LỚN = hai đội ≥ 1800, derby/kình địch, trận quyết định (mục 24). NGOẠI HẠNG ANH = giải tranh chấp quyết liệt. Ghi loại trận ở cột BL dòng kèo thẻ. (d) ƯU TIÊN THẺ: chỉ ở trận CÂN BẰNG, TRẬN LỚN hoặc Ngoại hạng Anh (chênh < 200); mỗi trận tối đa 1 kèo nhãn 'Thẻ ưu tiên' (nhãn riêng, không chiếm chỗ Ưu tiên 1/2 và TOP khung giờ), phải đạt tier B theo mục 5. Trận QUÁ LỆCH: kèo thẻ tối đa C, không ưu tiên (nhất là Tài thẻ). Trận CHÊNH VỪA ngoài PL/trận lớn: tối đa B, không ưu tiên. (e) Số liệu nền tuần 23–29/11 (36 kèo thẻ C1 + EL): toàn bộ −6,89R; trận cân bằng 7T–4B +1,93R (Tài thẻ 6T–2B +3,18R); chênh vừa 6T–6B −0,75R; quá lệch 3T–10B −8,07R (Tài thẻ 1T–7B −6,29R) → xác nhận quy tắc. Khi tách thẻ, RR chung tuần từ +2,04R lên +8,93R (ROI 6,2%), 2 kèo ưu tiên B+ +5,61R (ROI 14,0%). (f) Tổng kết tuần so RR thẻ theo loại trận để chỉnh ngưỡng chênh Elo. (g) J1 LEAGUE: kèo thẻ khó đoán → TẠM BỎ QUA kèo thẻ ở tab J1 theo người dùng (27/11); dòng thứ 5 mỗi trận J1 dùng cho chấp góc FT (mục 30).

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '29' • áp cho: Thẻ

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Trận QUÁ LỆCH (chênh ≥ 200 Elo) → thẻ tối đa C
- ✔ ĐẠT — Trận CHÊNH VỪA ngoài PL/trận lớn → thẻ tối đa B
- ✔ ĐẠT — Biên: chênh 200 Elo → QUÁ LỆCH (C); 199 → CHÊNH VỪA (PL giữ B)
- ✔ ĐẠT — Biên: CHÊNH VỪA ngoài PL/trận lớn bị giới hạn B (không lên A)
- ✔ ĐẠT — Biên: chênh 99 Elo = CÂN BẰNG → Thẻ ưu tiên; 100 = CHÊNH VỪA (ngoài PL) → không ưu tiên
- ✔ ĐẠT — Biên: Ngoại hạng Anh chênh 190 Elo vẫn được Thẻ ưu tiên (chênh < 200)
- ✔ ĐẠT — J1 bỏ kèo thẻ

### Mục 30 — ✔ khớp (mã 6b62412dd08a)
**A1:**

30. CHẤP GÓC FT (thị trường thứ 6, mọi giải, từ 28/11 theo người dùng). (a) CÁCH NGƯỜI DÙNG GỬI: 'Đội X -1,5 góc ft - 1,90 - 1,92' = kèo Chấp/Được chấp (dấu −/+) – giá của chính cửa đó – giá cửa ngược lại (ví dụ 'Kobe -2,5 góc ft - 1,90 - 1,92' → Kobe −2,5 @1,90, Chiba +2,5 @1,92). Viết tắt KHÔNG có dấu ('A 0,5 góc - 1,98 - 2,11') = đội A CHẤP: A −0,5 @1,98, đội B +0,5 @2,11; có dấu '+' = A được chấp. Ghi mốc theo đội nhà ở cột BF (nhà −1,5 → '-1,5'). (b) MÔ HÌNH: góc mỗi đội ~ nhị thức âm (phương sai 1,3 × TB), TB = (góc đội được hưởng + góc đối thủ để thủng)/2 theo mẫu tách sân mục 20; mẫu = hiệu số góc (đội – đối thủ) 10 trận gần nhất của hai đội; tier theo mục 8 bản thử (a)(b) như các kèo khác; tính vào RR chung (không phải kèo thẻ). (c) MỤC 28 áp cho chấp góc: kỳ vọng góc theo lối đá từng đội ghi ở cột BL; cờ 'NHIỀU GÓC CHO đội X' / DỒN ÉP TẠO GÓC của đội X phản bác cửa đối thủ của X được chấp → hạ 1 bậc (A → B, B → C+, C+ → C); ủng hộ → chỉ ghi điểm cộng. Mục 27: đội vắng cầu thủ chạy cánh/tạt chính → điểm trừ cho cửa đội đó chấp. (d) VỊ TRÍ GHI: tab châu Âu (EL, PL, LL, BL; tab C1 lệch 3 cột sang trái: AN:BI) khối 'CHẤP GÓC FT' ở dòng 200–249, cùng cột AQ:BL (AQ ngày, AR trận, AS kèo, AT odds, AU hiệu số góc 10 trận, AV căn cứ, AW tier, AX nguồn, AY kết luận, AZ/BA kết quả; BB–BJ danh sách kèo, BE = 'Chấp góc FT'); tab J1 dùng dòng thứ 5 mỗi trận. Kèo chấp góc được xét Ưu tiên/TOP như kèo khác (mỗi trận tối đa 2 Ưu tiên). (e) CHẤM: hiệu số góc FT (nhà – khách) + mốc; mốc ¼ chia đôi như chấp bàn.

**Bộ máy:** Bộ máy chấm (engine.grade) • bước kiểm '30(c)' • áp cho: Chấp góc

**Ca kiểm ý nghĩa (theo A1 thì phải ra):**
- ✔ ĐẠT — Chấp góc: cờ NHIỀU GÓC CHO / DỒN ÉP của đối thủ → hạ 1 bậc
