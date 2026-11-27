"""Mục 27 – Đội hình giả định mạnh nhất & chỉ số sức mạnh đội hình (tiêu chí phụ).
Dữ liệu: FotMob matchDetails của 10 trận gần nhất (đội hình ra sân, phút, điểm, giá trị) + trận sắp đá (vắng mặt, đội hình dự kiến)."""
import json, math, re
POS={0:'GK',1:'DEF',2:'MID',3:'FWD'}
def side_of(d,tid):
    g=d['general']; return 'homeTeam' if str(g['homeTeam']['id'])==str(tid) else 'awayTeam'
def mins_of(p,starter):
    ev=(p.get('performance') or {}).get('substitutionEvents') or []
    if starter:
        out=[e['time'] for e in ev if e.get('type')=='subOut']
        return min(out) if out else 90
    inn=[e['time'] for e in ev if e.get('type')=='subIn']
    return max(0,90-min(inn)) if inn else 0
def player_table(match_files,tid):
    P={}; XIs=[]
    for f in match_files:
        try: d=json.load(open(f))
        except Exception: continue
        lu=(d.get('content') or {}).get('lineup') or {}
        t=lu.get(side_of(d,tid)) or {}
        st=t.get('starters') or []
        if len(st)<11: continue
        xi=[]
        for starter,lst in ((True,st),(False,t.get('subs') or [])):
            for p in lst:
                pid=p['id']; m=mins_of(p,starter)
                r=P.setdefault(pid,dict(name=p['name'],pos=POS.get(p.get('usualPlayingPositionId'),'MID') if p.get('usualPlayingPositionId') is not None else ('GK' if p.get('positionId')==11 else 'MID'),
                                       mv=p.get('marketValue') or 0,mins=0,starts=0,rt=[]))
                if p.get('positionId')==11: r['pos']='GK'
                r['mins']+=m; r['starts']+=1 if starter else 0
                rt=(p.get('performance') or {}).get('rating')
                if rt and m>=20: r['rt'].append(rt)
                if p.get('marketValue'): r['mv']=p['marketValue']
                if starter: xi.append(pid)
        XIs.append(xi)
    n=max(1,len(XIs))
    mvmax=max([r['mv'] for r in P.values()]+[1])
    for r in P.values():
        rating=sum(r['rt'])/len(r['rt']) if r['rt'] else 6.5
        q=0.5*math.sqrt(r['mv']/mvmax)+0.5*min(1,max(0,(rating-5.5)/2.5))
        r['q']=q; r['share']=r['mins']/(90*n); r['I']=q*min(1,r['share']*1.25); r['rating']=rating
    return P,XIs
def shape(P,XIs):
    """Số cầu thủ mỗi tuyến hay dùng nhất (trung bình làm tròn của 10 trận)."""
    if not XIs: return {'GK':1,'DEF':4,'MID':4,'FWD':2}
    cnt={'DEF':0,'MID':0,'FWD':0}
    for xi in XIs:
        for p in xi:
            g=P[p]['pos']
            if g!='GK': cnt[g]+=1
    sh={g:round(v/len(XIs)) for g,v in cnt.items()}
    while sum(sh.values())>10: sh[max(sh,key=sh.get)]-=1
    while sum(sh.values())<10: sh['MID']+=1
    sh['GK']=1; return sh
def pick_xi(P,avail,sh=None):
    """Đội hình theo sơ đồ quen thuộc (sh), mỗi tuyến chọn cầu thủ có I×P cao nhất; thiếu người thì lấy tuyến bên cạnh."""
    sh=sh or {'GK':1,'DEF':4,'MID':4,'FWD':2}
    c=sorted(((r['I']*avail.get(pid,1.0),pid) for pid,r in P.items() if avail.get(pid,1.0)>=0.5),reverse=True)
    xi=[]
    for g in ('GK','DEF','MID','FWD'):
        xi+= [pid for s,pid in c if P[pid]['pos']==g][:sh[g]]
    rest=[pid for s,pid in c if pid not in xi and P[pid]['pos']!='GK']
    while len(xi)<11 and rest: xi.append(rest.pop(0))
    return xi
def strength(P,xi,part):
    grp={'att':('MID','FWD'),'def':('GK','DEF'),'all':('GK','DEF','MID','FWD')}[part]
    return sum(P[p]['q'] for p in xi if p in P and P[p]['pos'] in grp)
def availability(next_file,tid,rotation=0.0):
    """Xác suất ra sân: vắng chắc chắn (chấn thương/treo giò có ngày trở lại sau trận) = 0; 'Doubtful'/'A few days' = 0,5;
       rotation (0–0,3): giảm xác suất của cầu thủ trụ cột khi lịch dày/trận sau quan trọng hơn."""
    d=json.load(open(next_file)); lu=(d.get('content') or {}).get('lineup') or {}
    t=lu.get(side_of(d,tid)) or {}
    av={}; outs=[]
    for p in t.get('unavailable') or []:
        u=p.get('unavailability') or {}; er=str(u.get('expectedReturn') or '')
        pr=0.5 if re.search(r'Doubtful|few days|Questionable',er,re.I) else 0.0
        av[p['id']]=pr; outs.append((p['name'],u.get('type'),er,pr))
    pred=[p['id'] for p in (t.get('starters') or [])]
    return av,outs,pred,lu.get('lineupType')
def team_report(match_files,tid,next_file,rotation=0.0):
    P,XIs=player_table(match_files,tid)
    if not P: return None
    sh=shape(P,XIs); best=pick_xi(P,{},sh)
    av,outs,fm_pred,ltype=availability(next_file,tid,rotation)
    if rotation:
        top=sorted(P,key=lambda p:-P[p]['I'])[:6]
        for p in top: av[p]=min(av.get(p,1.0),1-rotation)
    mine=pick_xi(P,av,sh)
    res={}
    for part in ('att','def','all'):
        b=strength(P,best,part) or 1
        samp=[strength(P,x,part)/b for x in XIs] or [1]
        sm=sum(samp)/len(samp)
        res[part]=dict(best=1.0,sample=sm,mine=strength(P,mine,part)/b,fm=(strength(P,fm_pred,part)/b if len(fm_pred)==11 else None))
        res[part]['rel']=res[part]['mine']/sm if sm else 1
        if res[part]['fm'] is not None: res[part]['rel_fm']=res[part]['fm']/sm
    agree=len(set(mine)&set(fm_pred)) if len(fm_pred)==11 else None
    key=[P[p]['name'] for p in sorted(P,key=lambda p:-P[p]['I'])[:6]]
    missing=[P[p]['name'] for p in best if p not in mine]
    return dict(shape=sh,best=[P[p]['name'] for p in best],mine=[P[p]['name'] for p in mine],fm_pred_type=ltype,agree=agree,key=key,missing=missing,outs=outs,idx=res,n=len(XIs))
def compare_official(match_files,tid,next_file,mine_names):
    """Khi có đội hình chính thức: so với đội hình giả định, tính lại chỉ số."""
    P,XIs=player_table(match_files,tid); best=pick_xi(P,{},shape(P,XIs))
    av,outs,off,ltype=availability(next_file,tid)
    if ltype not in ('standard',) or len(off)<11: return None
    names={P[p]['name']:p for p in P}
    diff_in=[P[p]['name'] if p in P else str(p) for p in off if p in P and P[p]['name'] not in mine_names]
    diff_out=[n for n in mine_names if names.get(n) not in off]
    res={}
    for part in ('att','def','all'):
        b=strength(P,best,part) or 1; sm=sum(strength(P,x,part)/b for x in XIs)/max(1,len(XIs))
        res[part]=strength(P,off,part)/b/sm if sm else 1
    return dict(vao=diff_in,ra=diff_out,rel=res)
