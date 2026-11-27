"""Mục 28 – Lối đá & tỷ lệ chuyển đổi ra góc (tiêu chí cho kèo góc).
Đọc chi tiết trận FotMob (matchDetails) của 10 trận mẫu mỗi đội."""
import json,re,math,os,sys

def _num(v):
    if v is None: return None
    if isinstance(v,(int,float)): return float(v)
    m=re.match(r'\s*([\d.]+)',str(v)); return float(m.group(1)) if m else None
def _att(v):
    """'3 (33%)' -> (acc=3, attempts=9)"""
    if v is None: return None,None
    m=re.match(r'\s*(\d+)\s*\((\d+)%\)',str(v))
    if not m: return _num(v),None
    a,p=int(m.group(1)),int(m.group(2))
    return a,(round(a*100/p) if p>0 else (0 if a==0 else None))

def stats_of(content,period='All'):
    out={}
    for grp in ((content.get('stats') or {}).get('Periods') or {}).get(period,{}).get('stats',[]) or []:
        for s in grp.get('stats',[]):
            if s.get('stats') and s['stats'][0] is not None: out.setdefault(s['key'],s['stats'])
    return out

def match_row(path,tid):
    d=json.load(open(path)); c=d['content']; g=d['general']
    home=str(g['homeTeam']['id'])==str(tid); i,j=(0,1) if home else (1,0)
    S=stats_of(c); S1=stats_of(c,'FirstHalf')
    if 'corners' not in S: return None
    r=dict(home=home)
    r['poss']=_num(S.get('BallPossesion',[None,None])[i])
    r['cf']=_num(S['corners'][i]); r['ca']=_num(S['corners'][j])
    r['c1f']=_num(S1.get('corners',[None,None])[i]); r['c1a']=_num(S1.get('corners',[None,None])[j])
    ca=S.get('accurate_crosses')
    r['xf']=_att(ca[i])[1] if ca else None; r['xa']=_att(ca[j])[1] if ca else None
    r['tbf']=_num(S.get('touches_opp_box',[None,None])[i]); r['tba']=_num(S.get('touches_opp_box',[None,None])[j])
    r['shf']=_num(S.get('total_shots',[None,None])[i]); r['sha']=_num(S.get('total_shots',[None,None])[j])
    r['blf']=_num(S.get('blocked_shots',[None,None])[i])   # cú sút của đội bị chặn (hay ra góc)
    r['clr_opp']=_num(S.get('clearances',[None,None])[j])  # đối thủ phá bóng
    aw=S.get('aerials_won'); r['aer']=(_att(aw[i])[0]/max(1,(_att(aw[i])[0] or 0)+(_att(aw[j])[0] or 0))) if aw else None
    z=c.get('attackingZones') or {}
    zz=(z.get('home' if home else 'away') or {}).get('total')
    if zz: r['wide']=(zz['left']+zz['right'])/100; r['center']=zz['center']/100
    sh=[s for s in (c.get('shotmap') or {}).get('shots',[]) if str(s.get('teamId'))==str(tid)]
    r['head']=sum(1 for s in sh if s.get('shotType')=='Header')
    r['fromcorner']=sum(1 for s in sh if s.get('situation')=='FromCorner')
    r['xg_corner']=sum(s.get('expectedGoals') or 0 for s in sh if s.get('situation')=='FromCorner')
    return r

def avg(R,k):
    v=[x[k] for x in R if x.get(k) is not None]
    return sum(v)/len(v) if v else None

def profile(rows):
    P={k:avg(rows,k) for k in ('poss','cf','ca','c1f','c1a','xf','xa','tbf','tba','shf','sha','blf','clr_opp','aer','wide','center','head','fromcorner','xg_corner')}
    P['n']=len(rows)
    sx=sum(x['cf'] for x in rows if x.get('xf')); sxx=sum(x['xf'] for x in rows if x.get('xf'))
    P['c_per_cross']=sx/sxx if sxx else None                       # góc / 1 quả tạt (chuyển đổi)
    st=sum(x['cf'] for x in rows if x.get('tbf')); stt=sum(x['tbf'] for x in rows if x.get('tbf'))
    P['c_per_box']=st/stt if stt else None                         # góc / 1 chạm bóng vòng cấm
    ax=sum(x['ca'] for x in rows if x.get('xa')); axx=sum(x['xa'] for x in rows if x.get('xa'))
    P['ca_per_cross']=ax/axx if axx else None                      # góc thủng / 1 quả tạt đối thủ
    at=sum(x['ca'] for x in rows if x.get('tba')); att=sum(x['tba'] for x in rows if x.get('tba'))
    P['ca_per_box']=at/att if att else None
    return P

def style_label(P):
    L=[]
    if P['poss'] is not None:
        L.append('kiểm soát bóng' if P['poss']>=55 else ('nhường bóng/phản công' if P['poss']<=45 else 'cầm bóng trung bình'))
    if P.get('wide') is not None:
        L.append('đá cánh' if P['wide']>=0.72 else ('trung lộ' if P['wide']<=0.66 else 'cánh–trung lộ cân bằng'))
    if P['xf'] is not None:
        L.append('tạt nhiều' if P['xf']>=20 else ('ít tạt' if P['xf']<=13 else 'tạt vừa'))
    if P['head'] is not None and P['xf'] is not None and P['head']>=2.5 and P['xf']>=17: L.append('tạt cánh đánh đầu')
    elif P['head'] is not None and P['head']>=2.5: L.append('mạnh đánh đầu')
    return ', '.join(L)

def side_corners(A,B):
    """Kỳ vọng góc của đội A theo lối đá (A tấn công, B phòng ngự)."""
    parts=[]
    if A['xf'] and B['xa'] and A['c_per_cross'] and B['ca_per_cross']:
        parts.append((A['xf']+B['xa'])/2*(A['c_per_cross']+B['ca_per_cross'])/2)
    if A['tbf'] and B['tba'] and A['c_per_box'] and B['ca_per_box']:
        parts.append((A['tbf']+B['tba'])/2*(A['c_per_box']+B['ca_per_box'])/2)
    return sum(parts)/len(parts) if parts else None

def matchup(PH,PA,home_adj=0.0):
    eh=side_corners(PH,PA); ea=side_corners(PA,PH)
    if eh is None or ea is None: return None
    eh*=1+home_adj; ea*=1-home_adj
    poss_h=((PH['poss'] or 50)+(100-(PA['poss'] or 50)))/2
    h1=None
    if PH['c1f'] and PA['c1f'] and PH['cf'] and PA['cf']:
        h1=eh*PH['c1f']/PH['cf']*0.5+eh*PA['c1a']/max(PA['ca'],0.1)*0.5 + ea*PA['c1f']/PA['cf']*0.5+ea*PH['c1a']/max(PH['ca'],0.1)*0.5
    return dict(eh=eh,ea=ea,tot=eh+ea,h1=h1,poss_h=poss_h)

def verdict(pick,line,E,kv):
    """pick: 'Tài'/'Xỉu'; E: kỳ vọng theo lối đá; kv: kỳ vọng mô hình.  ±0,5 góc quanh mốc."""
    d=E-line
    if (pick=='Tài' and d>=0.5) or (pick=='Xỉu' and d<=-0.5): return 'ủng hộ'
    if (pick=='Tài' and d<=-0.5) or (pick=='Xỉu' and d>=0.5): return 'phản bác'
    return 'trung tính'

def profile_venue(rows,home):
    """Mục 20: 60% cùng sân khi có ≥5 trận cùng sân (ít hơn giảm theo tỷ lệ)."""
    allp=profile(rows); same=[r for r in rows if r['home']==home]
    if not same: return allp
    sp=profile(same); w=0.6*min(1,len(same)/5)
    out={}
    for k,v in allp.items():
        s=sp.get(k)
        out[k]=v if (s is None or v is None or k=='n') else w*s+(1-w)*v
    out['n_same']=len(same)
    return out

def flags(PH,PA,m,hn,an):
    F=[]
    for nm,P,Q,ps in ((hn,PH,PA,m['poss_h']),(an,PA,PH,100-m['poss_h'])):
        if ps>=57 and ((P['wide'] or 0)>=0.70 or (P['xf'] or 0)>=17) and (Q['tba'] or 0)>=27:
            F.append(f'{nm} dự kiến cầm bóng {ps:.0f}% + đá cánh/tạt, đối thủ để chạm vòng cấm {Q["tba"]:.0f}/trận → DỒN ÉP TẠO GÓC (bất lợi Xỉu góc, bài học EL 27/11)')
        side=m['eh'] if P is PH else m['ea']
        if (Q['xa'] or 0)>=21 and (P['xf'] or 0)>=17 and side>=5.8:
            F.append(f'{nm} tạt {P["xf"]:.0f}/trận gặp đối thủ cho tạt {Q["xa"]:.0f}/trận, dự kiến {side:.1f} góc → NHIỀU GÓC CHO {nm} (bất lợi Xỉu góc)')
        if P['c_per_cross'] and P['c_per_cross']>=0.33: F.append(f'{nm} chuyển đổi tạt→góc cao ({P["c_per_cross"]:.2f})')
        if P['c_per_cross'] and P['c_per_cross']<=0.20 and (P['xf'] or 0)>=17: F.append(f'{nm} tạt nhiều nhưng ít ra góc ({P["c_per_cross"]:.2f})')
    if (PH['xf'] or 99)<=15 and (PA['xf'] or 99)<=15: F.append('HAI ĐỘI ÍT TẠT → bất lợi Tài góc')
    if (PH['wide'] or 0)>=0.72 and (PA['wide'] or 0)>=0.72 and (PH['xf'] or 0)>=17 and (PA['xf'] or 0)>=17: F.append('HAI ĐỘI ĐÁ CÁNH + TẠT NHIỀU → bất lợi Xỉu góc')
    cv=[x for x in (PH['c_per_cross'],PA['c_per_cross']) if x]
    if len(cv)==2 and max(cv)<=0.22: F.append('HAI ĐỘI CHUYỂN ĐỔI RA GÓC THẤP → bất lợi Tài góc')
    if (PH['wide'] or 1)<=0.66 and (PA['wide'] or 1)<=0.66: F.append('HAI ĐỘI ĐÁ TRUNG LỘ → bất lợi Tài góc')
    return F

def summary(hn,an,PH,PA,m):
    f=lambda v,d=1: '–' if v is None else (f'{v:.{d}f}').replace('.',',')
    def one(nm,P):
        return (f'{nm}: {style_label(P)} (cầm bóng {f(P["poss"],0)}%, cánh {f((P["wide"] or 0)*100,0)}%/trung lộ {f((P["center"] or 0)*100,0)}%, '
                f'tạt {f(P["xf"])}/trận, chạm vòng cấm {f(P["tbf"],0)}, đánh đầu {f(P["head"])} cú, góc {f(P["cf"])}–{f(P["ca"])}, '
                f'góc/tạt {f(P["c_per_cross"],2)})')
    s=one(hn,PH)+' | '+one(an,PA)
    s+=f' | Kỳ vọng góc theo lối đá: {f(m["eh"])} + {f(m["ea"])} = {f(m["tot"])} FT, {f(m["h1"])} H1; cầm bóng dự kiến {f(m["poss_h"],0)}–{f(100-m["poss_h"],0)}'
    F=flags(PH,PA,m,hn,an)
    if F: s+=' | Cờ: '+'; '.join(F)
    return s

def verdict_flags(pick,F):
    """pick 'Tài'/'Xỉu' → ('phản bác'|'ủng hộ'|'trung tính', lý do)."""
    bad=[f for f in F if ('bất lợi Xỉu' in f and pick=='Xỉu') or ('bất lợi Tài' in f and pick=='Tài')]
    good=[f for f in F if ('bất lợi Xỉu' in f and pick=='Tài') or ('bất lợi Tài' in f and pick=='Xỉu')]
    if bad: return 'phản bác',bad
    if good: return 'ủng hộ',good
    return 'trung tính',[]
