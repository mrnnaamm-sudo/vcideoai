# J1 League – áp quy chuẩn chung (mục 1–29)
Chạy từ thư mục `football/`:
1. Tải dữ liệu: `j1/fm/lg.json` (FotMob leagues?id=223), `j1/fm/m_<id>.json` (10 trận gần nhất mỗi đội), `j1/fm/n_<id>.json` (trận sắp đá), `j1/odds.json` (Odds API soccer_japan_j_league, Pinnacle).
2. `python3 j1/run.py 28/11` → `j1/res_28-11.json` (mô hình Poisson/NB, mục 28 lối đá, mục 27 đội hình).
3. Danh sách vắng: `j1/abs_<ngày>.json` (Football LAB – FotMob không có cho J1).
4. `python3 j1/gen.py 28/11 && python3 j1/form.py 28/11` → `j1/sheet_28-11.json` (AQ:BL, khối phong độ BP2300+).
5. Giá góc/H1/thẻ người dùng: `j1/odds_user.json` = {"28/11": {"<dòng>": {"cor":[mốc,tài,xỉu], "h1":[...], "card":[...]}}} rồi chạy lại 2–4.
Khác biệt so với giải châu Âu: Elo ước tính từ BXH (1500 + 110 × hiệu số/trận), mẫu chỉ J1, trọng tài thường chưa công bố.
