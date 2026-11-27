"""Lập BẢNG ĐỐI CHIẾU A1 ↔ BỘ MÁY (mục 0j-5): từng mục A1, mã mục, chỗ bộ máy thực hiện, ca kiểm ý nghĩa + kết quả, mã từng tab.
python3 rules/doi_chieu.py [a1_meta.json] [a1_notes.json] → rules/DOI_CHIEU_A1_BO_MAY.md + .html"""
import json,sys,os,re,html,datetime,hashlib
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import a1_sync, registry, kiem_thu
D=os.path.dirname(os.path.abspath(__file__))
meta=json.load(open(sys.argv[1])) if len(sys.argv)>1 else {}
notes=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
t=a1_sync.text(); v=a1_sync.version(); S=a1_sync.sections(); MH=a1_sync.muc_hash()
res={}
for m,y,f in kiem_thu.CASES:
    try: ok=bool(f())
    except Exception: ok=False
    res.setdefault(m,[]).append((y,ok))
nca=len(kiem_thu.CASES); ndat=sum(ok for L in res.values() for _,ok in L)
LOAI={'cham':'Bộ máy chấm (engine.grade)','mo_hinh':'Mô hình xác suất (model.py)','du_lieu':'Khâu nạp dữ liệu (run_day) + kiểm đầu vào (audit)',
      'xep':'Xếp Ưu tiên/TOP (engine.rank)','trinh_bay':'Khuôn ghi sheet','quy_trinh':'Quy trình theo lịch'}
TT={'hc':'Chấp bàn','tot':'Tài/Xỉu bàn','cor':'Góc FT','h1':'Góc H1','card':'Thẻ','chc':'Chấp góc'}
def cases_for(m):
    r=registry.REG.get(int(m)) if m.isdigit() else None
    keys=[m]
    if r and r['loai']=='cham': keys+=[r['buoc']] if isinstance(r['buoc'],str) else list(r['buoc'])
    if m=='14': keys+=['14(8c)']
    if m=='29': keys+=['29(g)']
    if m=='0': keys+=['0(h)']
    return [c for k in dict.fromkeys(keys) for c in res.get(k,[])]
def impl(m):
    if not m.isdigit(): return 'Phần mở đầu – phạm vi áp dụng (mọi tab bóng đá, trừ NBA, RR tuần, Kèo đã vào)'
    r=registry.REG[int(m)]; s=LOAI[r['loai']]
    if r.get('buoc'): s+=f" • bước kiểm '{r['buoc'] if isinstance(r['buoc'],str) else ', '.join(r['buoc'])}'"
    tt=r.get('thi_truong')
    if tt: s+=' • áp cho: '+', '.join(TT[k] for k in (tt.keys() if isinstance(tt,dict) else tt))
    if r.get('noi'): s+=' • '+r['noi']
    return s
tab_rows=[]
for sid,name in a1_sync.TABS.items():
    mv=meta.get(str(sid)); nt=notes.get(str(sid))
    tab_rows.append((name,mv or '—','KHỚP' if mv==v else 'LỆCH','TRÙNG TỪNG KÝ TỰ' if nt==t else ('chưa đọc' if nt is None else 'KHÁC')))
rows=[]
for k in S:
    a=MH[k]; b=registry.MUC_HASH.get(k)
    title=S[k].split('\n')[0]; title=re.sub(r'^\d+\. ','',title)
    title=(title.split(':')[0] if ':' in title[:90] else title[:80]).strip()
    rows.append(dict(m=k,title=title,a=a,b=b,ok=a==b,impl=impl(k),cases=cases_for(k),text=S[k].strip()))
allok=all(r['ok'] for r in rows) and ndat==nca and all(x[2]=='KHỚP' for x in tab_rows) and registry.A1_VERSION==v
now=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=7)
# ---------- Markdown ----------
L=[f"# BẢNG ĐỐI CHIẾU QUY CHUẨN CHUNG: A1 ↔ BỘ MÁY",f"Lập lúc {now:%d/%m/%Y %H:%M} (giờ VN) • Mã phiên bản quy chuẩn: **{v}** • Bộ máy ghim: **{registry.A1_VERSION}**",
   f"**KẾT LUẬN: {'ĐỒNG BỘ – A1 và bộ máy giống hệt nhau' if allok else 'LỆCH – DỪNG PHÂN TÍCH'}**","",
   "## 1. A1 trên từng tab","| Tab | Mã A1 trên tab | So với bộ máy | Toàn văn A1 so với bộ máy |","|---|---|---|---|"]
L+=[f"| {a} | {b} | {c} | {d} |" for a,b,c,d in tab_rows]
L+=["",f"## 2. Ca kiểm ý nghĩa: {ndat}/{nca} ĐẠT","",
    "## 3. Từng mục: mã A1 = mã bộ máy","| Mục | Nội dung | Mã A1 | Mã bộ máy | Khớp | Bộ máy thực hiện | Ca kiểm |","|---|---|---|---|---|---|---|"]
L+=[f"| {r['m']} | {r['title']} | {r['a']} | {r['b']} | {'✔' if r['ok'] else '✘'} | {r['impl']} | {sum(o for _,o in r['cases'])}/{len(r['cases'])} |" for r in rows]
L+=["","## 4. Chi tiết từng mục (văn bản A1 nguyên văn + bộ máy)"]
for r in rows:
    L+=["",f"### Mục {r['m']} — {'✔ khớp' if r['ok'] else '✘ LỆCH'} (mã {r['a']})","**A1:**","",r['text'],"",f"**Bộ máy:** {r['impl']}"]
    if r['cases']: L+=["","**Ca kiểm ý nghĩa (theo A1 thì phải ra):**"]+[f"- {'✔ ĐẠT' if o else '✘ KHÔNG ĐẠT'} — {y}" for y,o in r['cases']]
open(os.path.join(D,'DOI_CHIEU_A1_BO_MAY.md'),'w').write('\n'.join(L)+'\n')
# ---------- HTML ----------
e=html.escape
H=[f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Đối chiếu A1 – bộ máy</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#ddd;--ok:#1b7f3b;--bad:#c62828;--card:#f6f7f9}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8e8e8;--mut:#9aa;--line:#333;--ok:#4cc36f;--bad:#ff6b6b;--card:#1f2227}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,sans-serif;margin:0;padding:16px;max-width:1100px;margin:auto}}
h1{{font-size:22px}}h2{{font-size:18px;margin-top:28px}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}}
.wrap{{overflow-x:auto}}.ok{{color:var(--ok);font-weight:700}}.bad{{color:var(--bad);font-weight:700}}.big{{font-size:18px;padding:10px 14px;border-radius:8px;background:var(--card);border:1px solid var(--line)}}
details{{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:8px 12px}}summary{{cursor:pointer;font-weight:600}}.a1{{white-space:pre-wrap;font-size:13.5px}}.mut{{color:var(--mut)}}code{{font-size:12px}}
</style></head><body><h1>Bảng đối chiếu quy chuẩn chung: A1 ↔ bộ máy</h1>
<p class="mut">Lập lúc {now:%d/%m/%Y %H:%M} (giờ VN) • Mã phiên bản quy chuẩn <code>{v}</code> • Bộ máy ghim <code>{registry.A1_VERSION}</code></p>
<p class="big {'ok' if allok else 'bad'}">{'ĐỒNG BỘ – A1 trên cả 6 tab và bộ máy giống hệt nhau' if allok else 'LỆCH – DỪNG PHÂN TÍCH'}</p>
<h2>1. A1 trên từng tab</h2><div class="wrap"><table><tr><th>Tab</th><th>Mã A1 trên tab</th><th>So với bộ máy</th><th>Toàn văn A1 so với bộ máy</th></tr>"""]
H+=[f"<tr><td>{e(a)}</td><td><code>{b}</code></td><td class='{'ok' if c=='KHỚP' else 'bad'}'>{c}</td><td class='{'ok' if d.startswith('TRÙNG') else 'bad'}'>{d}</td></tr>" for a,b,c,d in tab_rows]
H+=[f"</table></div><h2>2. Ca kiểm ý nghĩa: <span class='{'ok' if ndat==nca else 'bad'}'>{ndat}/{nca} ĐẠT</span></h2><p class='mut'>Mỗi ca là một kèo dựng sẵn ghi rõ “theo A1 thì phải ra kết quả gì”; bộ máy chạy thử và phải ra đúng như vậy.</p>",
    "<h2>3. Từng mục: mã A1 = mã bộ máy</h2><div class='wrap'><table><tr><th>Mục</th><th>Nội dung</th><th>Mã A1</th><th>Mã bộ máy</th><th>Khớp</th><th>Bộ máy thực hiện</th><th>Ca kiểm</th></tr>"]
H+=[f"<tr><td>{r['m']}</td><td>{e(r['title'])}</td><td><code>{r['a']}</code></td><td><code>{r['b']}</code></td><td class='{'ok' if r['ok'] else 'bad'}'>{'✔' if r['ok'] else '✘'}</td><td>{e(r['impl'])}</td><td>{sum(o for _,o in r['cases'])}/{len(r['cases'])}</td></tr>" for r in rows]
H+=["</table></div><h2>4. Chi tiết từng mục</h2><p class='mut'>Bấm vào từng mục để xem văn bản A1 nguyên văn, chỗ bộ máy thực hiện và các ca kiểm.</p>"]
for r in rows:
    H+=[f"<details><summary>Mục {r['m']} – {e(r['title'])} <span class='{'ok' if r['ok'] else 'bad'}'>{'✔' if r['ok'] else '✘'}</span></summary><p><b>A1:</b></p><div class='a1'>{e(r['text'])}</div><p><b>Bộ máy:</b> {e(r['impl'])}</p>"]
    if r['cases']: H+=["<p><b>Ca kiểm ý nghĩa:</b></p><ul>"]+[f"<li><span class='{'ok' if o else 'bad'}'>{'ĐẠT' if o else 'KHÔNG ĐẠT'}</span> — {e(y)}</li>" for y,o in r['cases']]+["</ul>"]
    H+=["</details>"]
H+=["</body></html>"]
open(os.path.join(D,'DOI_CHIEU_A1_BO_MAY.html'),'w').write('\n'.join(H))
print('ĐỒNG BỘ' if allok else 'LỆCH', v, f'{ndat}/{nca} ca', [x[2]+'/'+x[3] for x in tab_rows])
