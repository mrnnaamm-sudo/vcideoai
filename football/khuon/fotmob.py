"""Tải FotMob có bộ nhớ đệm (football/data/fm). Trận đã kết thúc giữ cố định; trận sắp đá và trang đội/giải tải lại khi quá hạn."""
import json,os,time,subprocess
D=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','fm'); os.makedirs(D,exist_ok=True)
def _get(url,path,max_age):
    if os.path.exists(path) and (max_age is None or time.time()-os.path.getmtime(path)<max_age):
        try: return json.load(open(path))
        except Exception: pass
    for i in range(3):
        r=subprocess.run(['curl','-s','-m','40','-A','Mozilla/5.0',url,'-o',path+'.tmp','-w','%{http_code}'],capture_output=True,text=True)
        if r.stdout.strip()=='200':
            os.replace(path+'.tmp',path); return json.load(open(path))
        time.sleep(2*(i+1))
    raise RuntimeError(f'FotMob lỗi {url} (mã {r.stdout})')
def giai(lid,max_age=3*3600): return _get(f'https://www.fotmob.com/api/data/leagues?id={lid}',f'{D}/l_{lid}.json',max_age)
def doi(tid,max_age=6*3600): return _get(f'https://www.fotmob.com/api/data/teams?id={tid}',f'{D}/t_{tid}.json',max_age)
def tran(mid,da_xong=True,max_age=1800):
    """da_xong=True: trận đã đá → lưu vĩnh viễn; False: trận sắp đá/đang đá → tải lại sau max_age giây (đội hình, trọng tài)."""
    p=f'{D}/m_{mid}.json'; u=f'https://www.fotmob.com/api/data/matchDetails?matchId={mid}'
    d=_get(u,p,None if da_xong else max_age)
    if da_xong and not ((d.get('header') or {}).get('status') or {}).get('finished'):   # tệp cũ lưu khi trận chưa xong → tải lại
        os.remove(p); d=_get(u,p,0)
    return d
def duong_dan_tran(mid): return f'{D}/m_{mid}.json'
