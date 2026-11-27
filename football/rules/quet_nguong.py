"""QUÉT NGƯỠNG (mục 0j): đổi lần lượt từng con số trong bộ máy (engine.grade/check16, model.tier) và xem ca kiểm ý nghĩa có bắt được không.
Chạy sau mỗi lần sửa đổi/bổ sung: python3 -B rules/quet_nguong.py → in các con số chưa có ca kiểm (LỌT) để bổ sung ca."""
import tokenize,io,subprocess,sys,os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
res=[]
for f,lo,hi in (('rules/engine.py','def pts5','def rank'),('model.py','def tier(sd','# ---------- mục 30')):
    src=open(f).read(); a=src.find(lo); b=src.find(hi)
    lines=src.splitlines(True); off=[0]
    for L in lines: off.append(off[-1]+len(L))
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type!=tokenize.NUMBER: continue
        p=off[tok.start[0]-1]+tok.start[1]
        if not (a<=p<b): continue
        v=float(tok.string)
        if v in(0,1) : continue
        for new in ([str(round(v*1.1+(0.01 if v<1 else 1),3)), str(round(v*0.9-(0.01 if v<1 else 1),3))]):
            mut=src[:p]+new+src[p+len(tok.string):]
            open(f,'w').write(mut)
            r=subprocess.run([sys.executable,'-B','rules/kiem_thu.py'],capture_output=True,text=True)
            open(f,'w').write(src)
            res.append((f,tok.start[0],tok.string,new,'BẮT' if r.returncode or 'LỖI' in r.stdout else 'LỌT',lines[tok.start[0]-1].strip()[:110]))
for r in res:
    if r[4]=='LỌT': print(*r[:5],'|',r[5])
print(sum(r[4]=='BẮT' for r in res),'/',len(res))
