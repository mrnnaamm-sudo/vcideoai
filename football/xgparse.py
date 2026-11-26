import json,re
def xg(path):
    try: s=open(path).read()
    except: return None
    m=re.search(r'"key":"expected_goals","stats":\[([^\],]+),([^\]]+)\]',s)
    if not m: return None
    try: return float(m.group(1).strip('"')),float(m.group(2).strip('"'))
    except: return None
