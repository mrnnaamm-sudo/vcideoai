import json,sys
sys.path.insert(0,'.')
from model import tier
f2=lambda x:('%.2f'%x).replace('.',',')
pc=lambda x:'%.0f%%'%(x*100)
sg=lambda x:('+' if x>=0 else '')+('%.1f'%(x*100)).replace('.',',')+'%'
lg=lambda x:(f"{x:g}").replace('.',',')
def best(x):
    return max(x['sides'],key=lambda s:(s['ev'] if s['ev'] is not None else s['pe']-0.6))
def cua(mk,x,s,hn,an):
    L=x['line']
    if mk=='hc':
        l=L if s['side']==0 else -L
        t=hn if s['side']==0 else an
        return f"{t} {('+' if l>0 else '')+lg(l) if l!=0 else '0'} FT"
    nm={'tot':'bàn FT','cor':'góc FT','h1':'góc H1','card':'thẻ FT'}[mk]
    return f"{'Tài' if s['side']==0 else 'Xỉu'} {lg(L)} {nm}"
def line_text(mk,x,s,hn,an,kv):
    c=cua(mk,x,s,hn,an)
    kvs={'hc':f"mô hình {f2(kv['lh'])}–{f2(kv['la'])} bàn",'tot':f"kỳ vọng {lg(round(kv['tot'],1))} bàn",'cor':f"kỳ vọng {lg(round(kv['cor'],1))} góc",
         'h1':f"kỳ vọng {lg(round(kv['h1'],1))} góc H1",'card':f"kỳ vọng {lg(round(kv['card'],1))} thẻ"}[mk]
    if s['odds']:
        return c,f"{c} @{f2(s['odds'])} • mẫu {pc(s['ps'])} / hòa vốn {pc(1/s['odds'])} • EV {sg(s['ev'])} (mô hình {pc((s['evm']+1)/s['odds'])}) • {kvs}"
    return c,f"{c} (chờ giá) • mẫu {pc(s['ps'])} • mô hình {pc(s['pm'])} • {kvs}"
