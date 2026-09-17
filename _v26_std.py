# -*- coding: utf-8 -*-
"""检验标准列：行内去重（同一计划多分计划同标准只显示一个）；全部计划同标准时仅首行显示"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

OLD = """  const stdAll=[...new Set(rows.map(r=>{ const rs=planRecords(d,r.id); return rs.length? rs.map(x=>x.standard).filter(Boolean).join('、') : (r.standard||''); }).filter(Boolean))];
  const stdSame = rows.length>1 && stdAll.length===1;"""
NEW = """  const stdOf=r=>{ const rs=planRecords(d,r.id); if(rs.length) return [...new Set(rs.map(x=>x.standard).filter(Boolean))].join('、'); return r.standard||''; };
  const stdAll=[...new Set(rows.map(stdOf).filter(Boolean))];
  const stdSame = rows.length>1 && stdAll.length===1;"""
assert s.count(OLD) == 1, 'stdOf 定位失败 %d' % s.count(OLD)
s = s.replace(OLD, NEW, 1)

OLD2 = """    {title:'检验标准', width:105, render:(_,r,idx)=>{ if(stdSame) return idx===0? <span className="mono tiny">{stdAll[0]}</span> : <span className="tiny">—</span>; const recs=planRecords(d,r.id); if(recs.length) return <span className="tiny">{recs.map(x=>x.standard).filter(Boolean).join('、')}</span>; return r.standard? <span className="mono tiny">{r.standard}</span> : <span className="tiny">暂无</span>; }},"""
NEW2 = """    {title:'检验标准', width:105, render:(_,r,idx)=>{ if(stdSame) return idx===0? <span className="mono tiny">{stdAll[0]}</span> : <span className="tiny">—</span>; const v=stdOf(r); return v? <span className="mono tiny">{v}</span> : <span className="tiny">暂无</span>; }},"""
assert s.count(OLD2) == 1, 'stdCol 定位失败 %d' % s.count(OLD2)
s = s.replace(OLD2, NEW2, 1)

open(P, 'w', encoding='utf-8').write(s)
print('std fix OK 长度', len(s))
