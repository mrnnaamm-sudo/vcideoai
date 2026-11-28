"""Chuyển dữ liệu đọc từ sheet (công cụ Google Sheets get_values) sang tệp cho khuôn.
  python3 khuon/doc_sheet.py so-do <vao.json> <ra.json>   vào: {mã giải: giá trị AQ150:AR399}  → ra: {mã: [[dòng, serial, nhãn trận], ...]}
  python3 khuon/doc_sheet.py aw    <vao.json> <ra.json>   vào: {mã giải: giá trị AW150:AW399} → ra: {mã: {dòng: tier}} (cho rules/audit.py)"""
import json,sys
kieu,vao,ra=sys.argv[1:4]; V=json.load(open(vao)); out={}
for ma,vals in V.items():
    if isinstance(vals,dict): vals=vals.get('values',[])
    if kieu=='so-do': out[ma]=[[150+i,(v[0] if len(v)>0 else ''),(v[1] if len(v)>1 else '')] for i,v in enumerate(vals) if v and any(v)]
    else: out[ma]={str(150+i):(v[0] if v else None) for i,v in enumerate(vals)}
json.dump(out,open(ra,'w'),ensure_ascii=False); print('đã ghi',ra,{k:len(v) for k,v in out.items()})
