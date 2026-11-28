"""CẤU HÌNH GIẢI – nơi DUY NHẤT phải sửa khi thêm giải mới (mục 0g: tab mới chỉ thêm phần nạp dữ liệu).
Mỗi giải: id FotMob, tab sheet (sheetId), mã Odds API (giá Pinnacle chấp/tài xỉu), tên giải dùng cho mục 1 (registry.MAU_GIAI),
Elo: 'clubelo' (bảng elo/elo_all.json) hoặc 'bxh' (1500 + 110 × hiệu số/trận, mục 25), thị trường (J1 bỏ thẻ – mục 29g)."""
GIAI={
 'PL':dict(ten='Ngoại hạng Anh',fotmob=47,sheet=200,tab='Ngoại hạng Anh',odds='soccer_epl',mau='English Premier League',elo='clubelo',
           tt=('hc','tot','cor','h1','card','chc'),tra_ve=5),
 'LL':dict(ten='La Liga',fotmob=87,sheet=201,tab='La Liga',odds='soccer_spain_la_liga',mau='Spanish LALIGA',elo='clubelo',
           tt=('hc','tot','cor','h1','card','chc'),tra_ve=5),
 'BL':dict(ten='Bundesliga',fotmob=54,sheet=202,tab='Bundesliga',odds='soccer_germany_bundesliga',mau='German Bundesliga',elo='clubelo',
           tt=('hc','tot','cor','h1','card','chc'),tra_ve=5),
 'J1':dict(ten='J1 League',fotmob=223,sheet=207,tab='J1 League',odds='soccer_japan_j_league',mau='J1 League',elo='bxh',
           tt=('hc','tot','cor','h1','chc'),tra_ve=5),
 'CL':dict(ten='Champions League',fotmob=42,sheet=100,tab='Champions League',odds='soccer_uefa_champs_league',mau='UEFA Champions League',elo='clubelo',
           tt=('hc','tot','cor','h1','card','chc'),tra_ve=5),
 'EL':dict(ten='Europa League',fotmob=73,sheet=203,tab='Europa League',odds='soccer_uefa_europa_league',mau='UEFA Europa League',elo='clubelo',
           tt=('hc','tot','cor','h1','card','chc'),tra_ve=5),
}
# Mục 1: giải được lấy vào mẫu 10 trận. leagueId FotMob của VĐQG + C1/EL (kể cả vòng loại) + ACL; KHÔNG cúp quốc nội, giao hữu, Conference League.
VDQG={47:'English Premier League',87:'Spanish LALIGA',54:'German Bundesliga',55:'Italian Serie A',53:'French Ligue 1',223:'J1 League'}
def ten_mau(tour):
    """→ tên giải theo registry.MAU_GIAI, hoặc None nếu giải không được lấy (mục 1)."""
    lid=tour.get('leagueId'); nm=tour.get('name','')
    if lid in VDQG: return VDQG[lid]
    if 'Conference' in nm or 'Youth' in nm or 'Women' in nm: return None
    if nm.startswith('Champions League'): return 'UEFA Champions League'
    if nm.startswith('Europa League'): return 'UEFA Europa League'
    if nm.startswith('AFC Champions League'): return 'ACL'
    return None
CUP_CHAU_LUC=('UEFA Champions League','UEFA Europa League','ACL')
