"""Mục 25: cập nhật ClubElo trước mỗi ngày phân tích. api.clubelo.com bị ngắt kết nối ở proxy → đọc bảng Elo trên trang quốc gia clubelo.com/<mã>.
  python3 khuon/elo_moi.py → ghi elo/elo_all.json (khuôn {tên ClubElo: [quốc gia, Elo, 1]}) + elo/ngay_cap_nhat.txt"""
import json,os,re,subprocess,datetime as dt,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P=os.path.join(ROOT,'elo','elo_all.json')
QG={'ENG':'England','ESP':'Spain','GER':'Germany','ITA':'Italy','FRA':'France','POR':'Portugal','NED':'Netherlands','BEL':'Belgium','TUR':'Turkey',
    'GRE':'Greece','CZE':'Czech Republic','POL':'Poland','NOR':'Norway','DEN':'Denmark','CYP':'Cyprus','SUI':'Switzerland','AUT':'Austria','HUN':'Hungary',
    'CRO':'Croatia','SWE':'Sweden','SCO':'Scotland','ISR':'Israel','SVN':'Slovenia','BUL':'Bulgaria','ARM':'Armenia','SRB':'Serbia','UKR':'Ukraine',
    'AZE':'Azerbaijan','SVK':'Slovakia','ROU':'Romania','KAZ':'Kazakhstan','MDA':'Moldova','IRL':'Ireland','FIN':'Finland'}
old=json.load(open(P)) if os.path.exists(P) else {}
new={}; loi=[]; h=''
for i in range(3):
    r=subprocess.run(['curl','-s','-m','40','-o','-','-w','\n%{http_code}','https://clubelo.com/ENG'],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition('\n')
    if code.strip()=='200' and 'class="Ast"' in body: h=body; break
    time.sleep(3)
# bảng xếp hạng toàn cầu: mỗi dòng có cờ quốc gia (alt), tên (span Ast) và Elo (td class r)
for cc,name,elo in re.findall(r'alt="([A-Z]{3})"(?:(?!</tr>).)*?<span class="Ast">([^<]+)</span></a></td><td class="r">(\d{3,4})</td>',h,re.S):
    new.setdefault(name.strip(),[QG.get(cc,cc),int(elo),1])
need=['Arsenal','Man City','Barcelona','Werder','Gladbach']
if len(new)<300 or any(k not in new for k in need):
    raise SystemExit(f'DỪNG – chỉ đọc được {len(new)} đội (lỗi trang: {loi}) – giữ bảng Elo cũ, báo người dùng')
ch=sum(1 for k in new if k in old and old[k][1]!=new[k][1])
json.dump(new,open(P,'w'),ensure_ascii=False)
open(os.path.join(ROOT,'elo','ngay_cap_nhat.txt'),'w').write(dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).strftime('%d/%m/%Y %H:%M')+'\n')
print(f'ClubElo: {len(new)} đội (bảng cũ {len(old)}), đổi Elo {ch} đội; trang lỗi: {loi or "không"}; đội cũ không còn: {sorted(set(old)-set(new))[:10]}')
