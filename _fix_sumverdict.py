# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = """  const sumVerdict=(recs)=>{ // 按分计划结论汇总：任一不合格则不合格
    if(!recs.length) return '待采集';
    const v=recs.map(x=>x.conclusion).filter(Boolean);
    if(v.some(x=>x==='不可接受')) return '不可接受';
    if(v.some(x=>x==='有条件接受')) return '有条件接受';
    if(v.every(x=>x==='可接受'||x==='非常理想可接受')) return '可接受';
    return v.length? v[0] : '待采集';
  };"""
new = """  const sumVerdict=(recs)=>{ // 按分计划结论汇总：任一不合格则不合格；无结论按待采集
    if(!recs.length) return '待采集';
    const v=recs.map(x=>x.conclusion).filter(Boolean);
    if(!v.length) return '待采集';
    if(v.some(x=>x==='不可接受')) return '不可接受';
    if(v.some(x=>x==='有条件接受')) return '有条件接受';
    if(v.every(x=>x==='可接受'||x==='非常理想可接受')) return '可接受';
    return v[0];
  };"""
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
