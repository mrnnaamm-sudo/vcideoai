import json,math
G=json.load(open('g/games.json')); sel=json.load(open('d28/teams/sel.json'))
EV=json.load(open('d28/teams/evs.json'))
# match spec: tab,row,time,label,h,a,hn,an, hcap(line for home, oddH, oddA), tot(line,o,u), cor(line,o,u), card(line,o,u), ref(name,avg,lgavg) , out
M=[
('PL',150,'03:00','Nottingham Forest (Nhà) – Chelsea (Khách)','393','363','Nottingham','Chelsea',(0,1.87,2.07),(2.5,1.76,2.08),(10,1.95,1.88),(4,1.79,2.04),('Andy Madley',3.45,3.87,42),'5795533'),
('PL',155,'22:00','Leeds United (Nhà) – Coventry City (Khách)','357','388','Leeds','Coventry',(-1,1.77,2.08),(2.5,1.62,2.23),(9.5,1.96,1.86),(None,None,None),('Paul Tierney',3.65,3.87,17),'5795531'),
('PL',160,'22:00','Manchester United (Nhà) – Brentford (Khách)','360','337','MU','Brentford',(-0.5,2.12,1.71),(3,1.89,1.96),(10.5,2.00,1.83),(None,None,None),('Robert Jones',3.87,3.87,39),'5795532'),
('LL',150,'03:00','Levante (Nhà) – Racing Santander (Khách)','1538','87','Levante','Santander',(-0.5,2.09,1.75),(3.5,2.25,1.62),(10,1.92,1.92),(None,None,None),None,'5868146'),
('LL',155,'20:00','Real Betis (Nhà) – Rayo Vallecano (Khách)','244','101','Betis','Rayo',(-1,2.03,1.87),(3,1.93,1.95),(10,1.95,1.88),(None,None,None),None,'5868141'),
('LL',160,'22:15','Málaga (Nhà) – Athletic Club (Khách)','99','93','Málaga','Athletic',(0.5,2.12,1.74),(2.5,1.88,1.97),(9.5,1.82,2.01),(None,None,None),None,'5868147'),
('BL',150,'02:30','Werder Bremen (Nhà) – Mönchengladbach (Khách)','137','268','Bremen','Gladbach',(-0.5,1.70,2.10),(3.5,2.19,1.67),(10,2.01,1.80),(None,None,None),None,'5881241'),
('BL',155,'21:30','Paderborn (Nhà) – Schalke 04 (Khách)','3307','133','Paderborn','Schalke',(0,1.83,2.08),(2.5,1.75,2.05),(9.5,1.92,1.90),(None,None,None),None,'5881239'),
('BL',160,'21:30','Köln (Nhà) – Elversberg (Khách)','122','10388','Köln','Elversberg',(-0.5,2.02,1.85),(3,1.93,1.89),(10,1.93,1.88),(None,None,None),None,'5881234'),
('BL',165,'21:30','Hamburger SV (Nhà) – Bayern München (Khách)','127','132','HSV','Bayern',(2,1.78,2.04),(3.5,1.71,2.10),(10.5,1.99,1.82),(None,None,None),None,'5881236'),
('BL',170,'21:30','Mainz 05 (Nhà) – Union Berlin (Khách)','2950','598','Mainz','Union',(-1,1.80,2.05),(3,1.86,1.95),(10,1.91,1.91),(None,None,None),None,'5881238'),
]
REFS=json.load(open('d28/fm/refs.json'))
def rows(t):
    out=[]
    for d,gid,lg in sel[t]:
        g=G.get(gid)
        if not g: continue
        home=g['h']==t
        gf,ga=(g['fs'] if home else g['fs'][::-1])
        out.append(dict(gf=gf,ga=ga,tot=gf+ga,m=gf-ga,cor=sum(g['cor']) if g['cor'] else None,h1=sum(g['c1']) if g['ncom']>=30 else None,
            cards=(sum(g['yc'])+2*sum(g['rc'])) if g['yc'] else None,home=home,lg=lg))
    return out
def ou(vals,line):
    v=[x for x in vals if x is not None]
    return sum(x>line for x in v),sum(x<line for x in v),len(v)
def f1(x): return f"{x:.1f}".replace('.',',')
def pc(x): return f"{x*100:.0f}%"
def odd(x): return ("%.2f"%x).replace('.',',') if x else ""
OUT=[]
for tab,row,time,lab,h,a,hn,an,hc,tt,cr,cd,ref,fid in M:
    R1,R2=rows(h),rows(a)
    un=REFS[fid]['un']
    inj=f"Vắng: {hn} – {', '.join(n for n,_ in un['homeTeam'][:5]) or 'không'}; {an} – {', '.join(n for n,_ in un['awayTeam'][:6]) or 'không'}."
    res=[]
    # handicap
    L,oh,oa=hc
    mh=[r['m'] for r in R1]; ma=[r['m'] for r in R2]
    hw=sum(x+L>0 for x in mh)+sum(-x+L>0 for x in ma); hp=sum(x+L==0 for x in mh)+sum(-x+L==0 for x in ma); hl=len(mh)+len(ma)-hw-hp
    ph=hw/max(1,hw+hl); pa=1-ph
    eh=ph-1/oh; ea=pa-1/oa
    side=(hn,L,oh,ph,eh,hw,hl,hp) if eh>=ea else (an,-L,oa,pa,ea,hl,hw,hp)
    ls=lambda x:('+' if x>0 else '')+(f"{x:g}".replace('.',',')) if x!=0 else '0'
    res.append(dict(k='hc',cua=f"{side[0]} {ls(side[1])} FT",od=side[2],p=side[3],e=side[4],n=f"{side[5]}/{side[5]+side[6]}"+(f", hoàn {side[7]}" if side[7] else ""),
        ar=f"Hiệu số 10 trận – {hn}: {', '.join(('+' if x>0 else '')+str(x) for x in mh)}; {an}: {', '.join(('+' if x>0 else '')+str(x) for x in ma)}.",line=(L,hn,oh,an,oa)))
    # totals etc
    for k,key,spec,name in (('tot','tot',tt,'bàn'),('cor','cor',cr,'góc'),('h1','h1',(4.5,None,None),'góc H1'),('card','cards',cd,'thẻ')):
        line,oo,uu=spec
        v1=[r[key] for r in R1]; v2=[r[key] for r in R2]
        if line is None:
            allv=[x for x in v1+v2 if x is not None]; mean=sum(allv)/max(1,len(allv)); line=math.floor(mean)+0.5
        o1,u1,n1=ou(v1,line); o2,u2,n2=ou(v2,line)
        O,U=o1+o2,u1+u2; p_o=O/max(1,O+U); p_u=1-p_o
        if oo:
            eo=p_o-1/oo; eu=p_u-1/uu
            sd=('Tài',oo,p_o,eo,O,U) if eo>=eu else ('Xỉu',uu,p_u,eu,U,O)
        else:
            sd=('Tài',None,p_o,p_o-0.526,O,U) if p_o>=p_u else ('Xỉu',None,p_u,p_u-0.526,U,O)
        m1=[x for x in v1 if x is not None]; m2=[x for x in v2 if x is not None]
        ar=f"Mẫu 10 trận (mốc {f'{line:g}'.replace('.',',')}): {hn} TB {f1(sum(m1)/max(1,len(m1)))}, Tài {o1}/{n1}; {an} TB {f1(sum(m2)/max(1,len(m2)))}, Tài {o2}/{n2}."
        cua=f"{sd[0]} {f'{line:g}'.replace('.',',')} {name} {'H1' if k=='h1' else 'FT'}".replace('góc H1 H1','góc H1')
        res.append(dict(k=k,cua=cua,od=sd[1],p=sd[2],e=sd[3],n=f"{sd[4]}/{sd[4]+sd[5]}",ar=ar,line=(line,'Tài',oo,'Xỉu',uu)))
    OUT.append(dict(tab=tab,row=row,time=time,lab=lab,hn=hn,an=an,ref=ref,inj=inj,res=res))
json.dump(OUT,open('d28/out.json','w'),ensure_ascii=False)
for m in OUT:
    print('\n##',m['tab'],m['time'],m['lab'],'| ref',m['ref'])
    print('  ',m['inj'])
    for r in m['res']: print(f"   {r['cua']:32s} odd {odd(r['od']):5s} p {pc(r['p'])} edge {r['e']*100:+.0f} n {r['n']}")
