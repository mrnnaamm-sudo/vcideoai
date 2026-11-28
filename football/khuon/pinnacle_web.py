"""NGUỒN GIÁ PINNACLE THAY THẾ khi Odds API hết lượt (mục 6: chấp/tài xỉu bàn = giá Pinnacle mới nhất).
Đọc dữ liệu công khai mà chính trang pinnacle.com dùng (guest.api.arcadia.pinnacle.com, không cần khóa),
đổi sang ĐÚNG định dạng Odds API (spreads/totals, giá thập phân) để bộ máy dùng y như cũ.

python3 khuon/pinnacle_web.py <mã giải> <tệp ra> [<tệp Odds API tham chiếu để khớp tên đội>]
mã giải: J1=2157, PL=1980, LL=2196, BL=1842 (tra thêm: /0.1/sports/29/leagues)."""
import json,sys,subprocess,re,unicodedata,datetime as dt
LID={'J1':2157,'PL':1980,'LL':2196,'BL':1842,'CL':2627,'EL':2630}
B='https://guest.api.arcadia.pinnacle.com/0.1'
def get(u):
    r=subprocess.run(['curl','-s','-m','40','-A','Mozilla/5.0',u],capture_output=True,text=True)
    return json.loads(r.stdout)
def dec(a): return round(1+a/100,3) if a>0 else round(1+100/abs(a),3)
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def toks(s): return {w for w in re.split(r'[^a-z0-9]+',norm(s)) if len(w)>=4 and w not in('club','united','city','real','borussia','sanga','purple')}
def main(ma,out,ref=None):
    lid=LID.get(ma,ma); M=get(f'{B}/leagues/{lid}/matchups'); K=get(f'{B}/leagues/{lid}/markets/straight')
    R=json.load(open(ref)) if ref else []
    now=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); ev=[]
    for m in M:
        if m.get('type')!='matchup' or m.get('parentId') or m.get('isLive'): continue
        p={x['alignment']:x['name'] for x in m['participants']}
        hn,an=p.get('home'),p.get('away')
        if not hn or not an: continue
        r=next((e for e in R if e['commence_time'][:13]==m['startTime'][:13] and (toks(hn)&toks(e['home_team']) or toks(an)&toks(e['away_team']))),None)
        H,A=(r['home_team'],r['away_team']) if r else (hn,an)
        mk=[]
        for k in K:
            if k['matchupId']!=m['id'] or k['period']!=0 or k.get('isAlternate') or k['type'] not in('spread','total'): continue
            pr={x['designation']:x for x in k['prices']}
            if k['type']=='spread':
                mk.append(dict(key='spreads',last_update=now,outcomes=[dict(name=H,price=dec(pr['home']['price']),point=pr['home']['points']),dict(name=A,price=dec(pr['away']['price']),point=pr['away']['points'])]))
            else:
                mk.append(dict(key='totals',last_update=now,outcomes=[dict(name='Over',price=dec(pr['over']['price']),point=pr['over']['points']),dict(name='Under',price=dec(pr['under']['price']),point=pr['under']['points'])]))
        ev.append(dict(id=str(m['id']),commence_time=m['startTime'],home_team=H,away_team=A,nguon='pinnacle.com (guest arcadia)',
                       bookmakers=[dict(key='pinnacle',title='Pinnacle',last_update=now,markets=mk)]))
    json.dump(ev,open(out,'w'),ensure_ascii=False,indent=1); print(len(ev),'trận →',out,'lúc',now)
if __name__=='__main__': main(*sys.argv[1:])
