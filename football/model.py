import math
# ---------- distributions ----------
def pois(l,k): return math.exp(-l)*l**k/math.factorial(k)
def nb_pmf(mean,var,kmax=40):
    if var<=mean*1.001: return [pois(mean,k) for k in range(kmax)]
    p=mean/var; r=mean*p/(1-p)
    out=[]
    for k in range(kmax):
        out.append(math.exp(math.lgamma(k+r)-math.lgamma(r)-math.lgamma(k+1)+r*math.log(p)+k*math.log(1-p)))
    return out
def score_matrix(lh,la,n=11):
    return [[pois(lh,i)*pois(la,j) for j in range(n)] for i in range(n)]
# ---------- settlement EV for asian lines ----------
def split(line):
    f=line*4
    if abs(f-round(f))<1e-9 and int(round(f))%2!=0: return [line-0.25,line+0.25]
    return [line]
def ev_margin(dist,line,odds):
    """dist: dict margin->prob, bet wins if margin+line>0. returns EV per unit"""
    parts=split(line); ev=0
    for l in parts:
        e=0
        for m,p in dist.items():
            v=m+l
            e+=p*((odds-1) if v>0 else (0 if abs(v)<1e-9 else -1))
        ev+=e/len(parts)
    return ev
def ah_ev(M,line_home,odds,side):
    d={}
    for i,row in enumerate(M):
        for j,p in enumerate(row):
            m=(i-j) if side=='h' else (j-i)
            d[m]=d.get(m,0)+p
    return ev_margin(d,line_home if side=='h' else -line_home,odds)
def tot_ev(pmf,line,odds,over):
    d={}
    for k,p in enumerate(pmf):
        m=(k-line) if over else (line-k)
        d[round(m,2)]=d.get(round(m,2),0)+p
    # margin already includes line; ev_margin adds line, so pass 0 with split handled manually
    parts=split(line); ev=0
    for l in parts:
        e=0
        for k,p in enumerate(pmf):
            v=(k-l) if over else (l-k)
            e+=p*((odds-1) if v>0 else (0 if abs(v)<1e-9 else -1))
        ev+=e/len(parts)
    return ev
# ---------- sample hit rate (pooled 2 teams) ----------
def settle(v):
    if v>=0.5: return 1
    if abs(v-0.25)<1e-9: return .5
    if abs(v)<1e-9: return 0
    if abs(v+0.25)<1e-9: return -.5
    return -1
def rate(vals):
    W=sum(1 for s in vals if s==1);HW=sum(1 for s in vals if s==.5);HL=sum(1 for s in vals if s==-.5);L=sum(1 for s in vals if s==-1)
    den=W+HW+HL+L
    return ((W+0.5*HW)/den if den else 0),den
# ---------- venue blend ----------
def vblend(recs,key,home):
    A=[r[key] for r in recs if r.get(key) is not None]
    V=[r[key] for r in recs if r.get(key) is not None and r['home']==home]
    if not A: return None
    a=sum(A)/len(A)
    if not V: return a
    w=0.6*min(len(V),5)/5
    return w*sum(V)/len(V)+(1-w)*a
# ---------- league coefficient (UEFA 5y, kassiesa 26/27) ----------
COEF={'England':108.2,'Italy':92.6,'Spain':87.9,'Germany':85.4,'France':72.7,'Portugal':69.8,'Belgium':64.1,'Netherlands':56.4,
 'Turkey':53.9,'Greece':47.6,'Czechia':46.3,'Poland':45.7,'Norway':41.4,'Denmark':40.8,'Cyprus':35.4,'Switzerland':32.2,'Austria':29.7,
 'Hungary':29.3,'Croatia':27.9,'Sweden':27.0,'Scotland':26.9,'Romania':26.1,'Ukraine':24.8,'Israel':24.1,'Slovenia':23.6,'Serbia':19.0,
 'Bulgaria':22.1,'Armenia':15.8}
def lgf(ch,ca):
    if not ch or not ca: return 1.0
    return max(0.93,min(1.07,(ch/ca)**0.08))
# ---------- main evaluation ----------
def evaluate(H,A,od,ref=None,elo=(None,None),coef=(None,None),xg=(None,None),char=1.0):
    """H,A: list of match recs with gf,ga,cf,ca,cor,h1,cards,home.
       od: dict market-> (line, o_first, o_second) ; hc line is for home.
       returns list of dicts per market with both sides evaluated."""
    atk_h=vblend(H,'gf',True); def_h=vblend(H,'ga',True); atk_a=vblend(A,'gf',False); def_a=vblend(A,'ga',False)
    xh,xa=xg
    if xh and xh['n']>=6: atk_h=0.5*atk_h+0.5*xh['xgf']; def_h=0.5*def_h+0.5*xh['xga']
    if xa and xa['n']>=6: atk_a=0.5*atk_a+0.5*xa['xgf']; def_a=0.5*def_a+0.5*xa['xga']
    f=lgf(*coef)
    lh=(atk_h+def_a)/2*f; la=(atk_a+def_h)/2/f
    T=lh+la; S=lh-la
    if elo[0] and elo[1]:
        Se=(elo[0]-elo[1]+65)/220
        S=0.75*S+0.25*Se
    lh=max(0.15,(T+S)/2); la=max(0.15,(T-S)/2)
    M=score_matrix(lh,la)
    tot_pmf=[0]*21
    for i,row in enumerate(M):
        for j,p in enumerate(row): tot_pmf[i+j]+=p
    kv={'tot':T,'sup':lh-la,'lh':lh,'la':la}
    cf_h=vblend(H,'cf',True); ca_h=vblend(H,'ca',True); cf_a=vblend(A,'cf',False); ca_a=vblend(A,'ca',False)
    if None not in (cf_h,ca_h,cf_a,ca_a): kv['cor']=(cf_h+ca_a)/2+(cf_a+ca_h)/2
    else: kv['cor']=((vblend(H,'cor',True) or 0)+(vblend(A,'cor',False) or 0))/2
    kv['h1']=((vblend(H,'h1',True) or 0)+(vblend(A,'h1',False) or 0))/2
    rf=1.0
    if ref and ref.get('ryc') and ref.get('ravg') and (ref.get('rm') or 0)>=10: rf=ref['ryc']/ref['ravg']
    kv['rf']=rf; kv['char']=char
    kv['card']=((vblend(H,'cards',True) or 0)+(vblend(A,'cards',False) or 0))/2*rf*char
    out={}
    for mk,(line,o1,o2) in od.items():
        if line is None: continue
        if mk=='hc':
            sh=[settle(r['gf']-r['ga']+line) for r in H]+[settle(-(r['gf']-r['ga'])+line) for r in A]
            sa=[-s for s in sh]
            ps1,n=rate(sh); ps2,_=rate(sa)
            ev1=ah_ev(M,line,o1,'h') if o1 else None; ev2=ah_ev(M,line,o2,'a') if o2 else None
            pm1=None if o1 is None else (ev1+1)/o1; pm2=None if o2 is None else (ev2+1)/o2
            # model prob without price: win prob equiv at even odds
            pw1=ah_ev(M,line,2.0,'h')/2+0.5; pw2=ah_ev(M,line,2.0,'a')/2+0.5
        else:
            key={'tot':'tot','cor':'cor','h1':'h1','card':'cards'}[mk]
            vals=[(r['gf']+r['ga']) if mk=='tot' else r.get(key) for r in H+A]
            vals=[v for v in vals if v is not None]
            so=[settle(v-line) for v in vals]; su=[-s for s in so]
            ps1,n=rate(so); ps2,_=rate(su)
            if mk=='tot': pmf=tot_pmf
            elif mk=='cor': pmf=nb_pmf(kv['cor'],kv['cor']*1.35)
            elif mk=='h1': pmf=nb_pmf(kv['h1'],kv['h1']*1.3)
            else: pmf=nb_pmf(kv['card'],kv['card']*1.6)
            ev1=tot_ev(pmf,line,o1,True) if o1 else None; ev2=tot_ev(pmf,line,o2,False) if o2 else None
            pm1=None if o1 is None else (ev1+1)/o1; pm2=None if o2 is None else (ev2+1)/o2
            pw1=tot_ev(pmf,line,2.0,True)/2+0.5; pw2=tot_ev(pmf,line,2.0,False)/2+0.5
        sides=[]
        for s,(o,oo,ps,pm,pw) in enumerate(((o1,o2,ps1,pm1,pw1),(o2,o1,ps2,pm2,pw2))):
            pf=None
            if o and oo: pf=(1/o)/(1/o+1/oo)
            if o:
                pe=0.4*pm+0.3*ps+0.3*pf if pf else 0.55*pm+0.45*ps
                ev=pe*o-1; evm=pm*o-1
            else:
                pe=0.55*pw+0.45*ps; ev=None; evm=None
            sides.append(dict(side=s,odds=o,ps=ps,pm=pw,pf=pf,pe=pe,ev=ev,evm=evm,edge=(ps-1/o) if o else None,n=n))
        out[mk]=dict(line=line,sides=sides)
    return kv,out
def tier(sd,mk,n_ok=True,ref_ok=None,card_dev=None,refdev=None):
    """new mục 8 (+EV) and mục 18b"""
    o=sd['odds']; ps=sd['ps']
    if o is None:
        if ps>=0.65 and sd['pm']>=0.58: return 'B?'
        return 'C'
    e=sd['edge']; ev=sd['ev']; evm=sd['evm']
    if mk=='card':
        if ps>=0.70 and refdev is not None and refdev>=0.5 and card_dev is not None and card_dev>=0.6 and ev>=0.05 and evm>0: return 'B'
        if e>=0.05 and ev>=0.02 and o>=1.65 and evm>0 and ref_ok and n_ok: return 'C+'
        return 'C'
    if e>=0.25 and ev>=0.12 and evm>0: return 'A'
    if e>=0.09 and ps>=0.55 and ev>=0.05 and evm>0: return 'B'
    if e>=0.05 and ev>=0.02 and o>=1.65 and evm>0 and n_ok: return 'C+'
    return 'C'
