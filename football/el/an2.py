import json,math,statistics,datetime
fx=json.load(open('el/fm/fx.json')); AN=json.load(open('el/an.json')); od=json.load(open('el/odds.json'))
ev=[e for e in od if e['commence_time'].startswith('2026-11-26')]
def key(s): return s.lower().replace('olympiakos','olympiacos').replace('ofi crete','ofi').replace('tsg hoffenheim','hoffenheim').replace('ş','s').replace('ň','n').replace('á','a').replace('ø','o').split()[0][:5]
OM={}
for f in fx:
    for e in ev:
        if e['commence_time'][:16]==f['t'][:16] and (key(e['home_team'])==key(f['hn']) or key(e['away_team'])==key(f['an'])): OM[f['id']]=e
assert len(OM)==18, len(OM)
def alt(eid):
    try: d=json.load(open(f'el/odds/{eid}.json'))
    except: return {}
    if 'bookmakers' not in d: return {}
    o={}
    for b in d['bookmakers']:
        for m in b['markets']:
            if m['key'] in('alternate_totals_corners','alternate_totals_cards'):
                for x in m['outcomes']: o.setdefault((m['key'][17:],x['point']),{}).setdefault(x['name'],[]).append(x['price'])
    return {k:{n:statistics.median(v) for n,v in d2.items()} for k,d2 in o.items()}
def f1(x): return f"{x:.1f}".replace('.',',')
def pc(x): return f"{x*100:.0f}%"
def lg(x): return f"{x:g}".replace('.',',')
def odd(x): return f"{x:.2f}".replace('.',',')
def settle(v):
    if v>=0.5: return 1
    if abs(v-0.25)<1e-9: return .5
    if abs(v)<1e-9: return 0
    if abs(v+0.25)<1e-9: return -.5
    return -1
def rate(vals):
    W=sum(1 for s in vals if s==1);HW=sum(1 for s in vals if s==.5);HL=sum(1 for s in vals if s==-.5);L=sum(1 for s in vals if s==-1);P=sum(1 for s in vals if s==0)
    den=W+HW+HL+L
    return ((W+0.5*HW+0.5*HL*0)/den if den else 0),W+HW,den,P
USR={0:((9.5,1.97,1.75),(4.5,2.04,1.69),(4,1.99,1.71)),7:((9.5,1.82,1.88),(4.5,1.97,1.74),(3.5,1.666,2.08)),
2:((9.5,1.84,1.86),(4.5,2.02,1.71),(3,1.9,1.78)),4:((9,1.82,1.88),(4.5,2.13,1.62),(4.5,1.96,1.75)),
3:((9,1.96,1.75),(4.5,2.23,1.56),(4,1.97,1.727)),1:((9.5,1.98,1.7),(4.5,2.12,1.62),(4,1.94,1.75)),
5:((9.5,1.83,1.88),(4.5,1.98,1.74),(4,1.71,1.99)),6:((9.5,1.95,1.76),(4.5,1.96,1.75),(4,1.98,1.72)),
8:((9.5,1.86,1.84),(4.5,1.98,1.74),(4.5,1.83,1.87)),12:((10.5,1.99,1.7),(4.5,1.8,1.9),(3.5,1.9,1.8)),
13:((10,1.99,1.92),(4.5,1.9,1.81),(3.5,1.78,2.0)),14:((9.5,1.84,1.86),(4.5,1.96,1.75),(4.5,2.1,1.65)),
16:((9.5,1.81,1.9),(4.5,1.95,1.76),(4.5,2.45,1.49)),15:((10,1.9,1.8),(4.5,1.85,1.85),(4.5,1.96,1.75)),
17:((10,1.83,1.87),(4.5,1.82,1.88),(4.5,2.4,1.5)),9:((9.5,1.8,1.91),(4.5,1.95,1.76),(3.5,1.96,1.75)),
10:((10.5,1.94,1.77),(4.5,1.75,1.96),(3.5,1.7,2.03)),11:((9.5,1.87,1.83),(4.5,2.0,1.72),(4.5,2.5,1.47))}
REF={}
OUT=[];REFROWS=[]
for fi,f in enumerate(fx):
    e=OM[f['id']]; h=AN[str(f['h'])]; a=AN[str(f['a'])]
    hn,an=h['name'],a['name']; lab=h['lab']; time=lab[:5]; match=lab[8:]
    nh,na=len(h['vals']),len(a['vals'])
    d=json.load(open(f"el/fm/n_{f['id']}.json")); c=d['content']
    r=c['matchFacts']['infoBox'].get('Referee') or {}
    st={s['type']:(s.get('value'),s.get('average')) for s in r.get('stats',[])}
    un=c.get('lineup',{}) or {}
    def unav(side):
        t=un.get(side) or {}
        return [p.get('name') for p in (t.get('unavailable') or [])][:6]
    uh,ua=unav('homeTeam'),unav('awayTeam')
    inj=f"Vắng: {hn} – {', '.join(uh) or 'không có thông tin'}; {an} – {', '.join(ua) or 'không có thông tin'}."
    ryc,ravg=st.get('yellowCards',(None,None)); rm=st.get('matches',(0,None))[0] or 0; rred=st.get('redCards',(0,None))[0]; rfo=st.get('fouls',(None,None))[0]
    rdir=0;rv='TRUNG BÌNH'
    if ryc and ravg and rm>=10:
        if ryc-ravg>=0.3: rdir=1; rv='CHẶT TAY' if ryc-ravg>=0.6 else 'TRÊN TRUNG BÌNH'
        elif ryc-ravg<=-0.3: rdir=-1; rv='NHẸ TAY'
    elif rm<10: rv='MẪU MỎNG'
    REF[f['id']]=(r.get('text'),r.get('country'),rm,ryc,ravg,rred,rfo,rv,rdir)
    mk=e['bookmakers'][0]['markets']; M={m['key']:m['outcomes'] for m in mk}
    sp=M['spreads']; hs=[o for o in sp if o['name']==e['home_team']][0]; as_=[o for o in sp if o['name']!=e['home_team']][0]
    L=hs['point']; oh,oa=hs['price'],as_['price']
    to=M['totals']; tl=to[0]['point']; tov=[o for o in to if o['name']=='Over'][0]['price']; tun=[o for o in to if o['name']=='Under'][0]['price']
    AL=alt(e['id'])
    res=[]
    mh=[v['gf']-v['ga'] for v in h['vals']]; ma=[v['gf']-v['ga'] for v in a['vals']]
    sh=[settle(x+L) for x in mh]+[settle(-x+L) for x in ma]
    sa=[-s for s in sh]
    ph,wh,dh,P=rate(sh); pa,wa,da,_=rate(sa)
    eh=ph-1/oh; ea=pa-1/oa
    if eh>=ea: side,line,o,p,w,dn,e_=hn,L,oh,ph,wh,dh,eh
    else: side,line,o,p,w,dn,e_=an,-L,oa,pa,wa,da,ea
    sgn=lambda x:('+' if x>0 else '')+lg(x) if x!=0 else '0'
    under=(side==hn and L>0) or (side==an and L<0)
    blow=min(mh if side==hn else ma) if True else 0
    res.append(dict(k='hc',cua=f"{side} {sgn(line)} FT",od=o,p=p,e=e_,n=f"{w}/{dn}"+(f", hoàn {P}" if P else ''),
        ar=f"Hiệu số 10 trận – {hn}: {', '.join(sgn(x) for x in mh)}; {an}: {', '.join(sgn(x) for x in ma)}.",line=(L,hn,oh,an,oa),psv=(under and abs(line)>=1.5 and blow<=-4)))
    def tot(key,i,name,line,oo,uu):
        v1=[v['row'][i] for v in h['vals'] if v['row'][i]!='']; v2=[v['row'][i] for v in a['vals'] if v['row'][i]!='']
        if line is None:
            allv=v1+v2; line=math.floor(sum(allv)/max(1,len(allv)))+0.5
        so=[settle(x-line) for x in v1+v2]; su=[-s for s in so]
        po,wo,do,Po=rate(so); pu,wu,du,_=rate(su)
        if oo:
            eo=po-1/oo; eu=pu-1/uu
            sd=('Tài',oo,po,eo,wo,do) if eo>=eu else ('Xỉu',uu,pu,eu,wu,du)
        else:
            sd=('Tài',None,po,None,wo,do) if po>=pu else ('Xỉu',None,pu,None,wu,du)
        o1=sum(x>line for x in v1); o2=sum(x>line for x in v2)
        ar=f"Mẫu 10 trận (mốc {lg(line)}): {hn} TB {f1(sum(v1)/max(1,len(v1)))}, Tài {o1}/{len(v1)}; {an} TB {f1(sum(v2)/max(1,len(v2)))}, Tài {o2}/{len(v2)}."
        cua=f"{sd[0]} {lg(line)} {name}"
        return dict(k=key,cua=cua,od=sd[1],p=sd[2],e=sd[3],n=f"{sd[4]}/{sd[5]}"+(f", hoàn {Po}" if Po else ''),ar=ar,line=(line,'Tài',oo,'Xỉu',uu),side=sd[0])
    res.append(tot('tot',None,'bàn FT',tl,tov,tun) if False else None)
    # goals need gf+ga totals
    for v in h['vals']+a['vals']: v['row'].append(v['gf']+v['ga'])
    res[-1]=tot('tot',24,'bàn FT',tl,tov,tun)
    def pick(kind,i,name,lines):
        if lines:
            v=[x for x in h['vals']+a['vals'] if x['row'][i]!='']; m=sum(x['row'][i] for x in v)/max(1,len(v))
            best=min(lines,key=lambda k:abs(lines[k].get('Over',9)-lines[k].get('Under',0)) if 'Over' in lines[k] and 'Under' in lines[k] else 99)
            return tot(kind,i,name,best,lines[best].get('Over'),lines[best].get('Under'))
        return tot(kind,i,name,None,None,None)
    cl={k[1]:v for k,v in AL.items() if k[0]=='corners' and 'Over' in v and 'Under' in v}
    kl={k[1]:v for k,v in AL.items() if k[0]=='cards' and 'Over' in v and 'Under' in v}
    U=USR[fi]
    res.append(tot('cor',9,'góc FT',*U[0]))
    res.append(tot('h1',7,'góc H1',*U[1]))
    res.append(tot('card',17,'thẻ FT',*U[2]))
    for v in h['vals']+a['vals']: v['row'].pop()
    OUT.append(dict(id=f['id'],time=time,lab=lab,match=match,hn=hn,an=an,nh=nh,na=na,inj=inj,res=res,ref=REF[f['id']]))
json.dump(OUT,open('el/out2.json','w'),ensure_ascii=False)
for m in OUT:
    print('##',m['time'],m['match'],m['nh'],m['na'],'| ref',m['ref'][0],m['ref'][3],m['ref'][4],m['ref'][7])
    print('  ',m['inj'][:200])
    for r in m['res']:
        print('   ',r['k'],r['cua'],r['od'],pc(r['p']),r['n'],'edge' ,None if r['e'] is None else round(r['e']*100),'PSV' if r.get('psv') else '')
