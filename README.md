# Phân tích kèo bóng đá – mô hình chung 5 tab

Mã và dữ liệu phục vụ bộ quy chuẩn chung (mục 1–25) cho các tab bóng đá trong Google Sheet
"Make money online": Champions League, Europa League, Ngoại hạng Anh, La Liga, Bundesliga
(không áp dụng cho tab NBA và "Kèo đã vào").

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `football/rules/quy_chuan_chung.md` | Bộ quy chuẩn đầy đủ mục 1–25 (bản đang ghi ở ô A1 của 5 tab) |
| `football/model.py` | Mô hình: Poisson (bàn), nhị thức âm (góc, góc H1, thẻ), tách sân nhà/khách, xG, hệ số giải, Elo, EV%, xếp Tier |
| `football/gen3.py` | Hàm định dạng câu kết luận (cột AY) |
| `football/el/run3.py` | Chạy mô hình cho Europa League 27/11 → `el/res3.json` |
| `football/d28/run3.py` | Chạy mô hình cho các trận 28/11 (PL/LL/BL) → `d28/res3.json` |
| `football/elo/` | Bảng ClubElo (lấy từ clubelo.com) và bảng ánh xạ tên đội |
| `football/xg/` | xG ghi/lọt TB 10 trận gần nhất (FotMob) |
| `football/g/games.json`, `football/el/an.json` | Số liệu 10 trận mỗi đội (ESPN / FotMob) |
| `football/results/` | Kết quả mô hình và nội dung cột AY đã ghi lên sheet |

## Chạy lại

```bash
cd football
python3 el/run3.py
python3 d28/run3.py
```

Chỉ cần Python 3, không cần thư viện ngoài. Không có khoá API nào trong repo.
