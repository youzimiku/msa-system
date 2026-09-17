# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 1) charMethods 映射为方法代码
old1 = "  const charMethods = charObj&&charObj.methods&&charObj.methods.length? charObj.methods : (charObj? ((charObj.dataType==='计数型')?['KAPPA']:['GRR']) : []);"
new1 = "  const charMethods = charObj&&charObj.methods&&charObj.methods.length? charObj.methods.map(x=>typeof x==='string'?x:(x.method||'')).filter(Boolean) : (charObj? ((charObj.dataType==='计数型')?['KAPPA']:['GRR']) : []);"
assert src.count(old1) == 1, ('old1', src.count(old1))
src = src.replace(old1, new1, 1)

# 2) pickChar 中按特性 methods 的 standardId 带出标准
old2 = """      const stds=stdsOf(m,c);
      const std=stds.find(s=>s.id===(c['std_'+m]||''))||stds[0];"""
new2 = """      const stds=stdsOf(m,c);
      const mm=(c.methods||[]).find(x=>typeof x==='string'? x===m : x.method===m);
      const sid=mm?(typeof mm==='string'? (c['std_'+m]||'') : (mm.standardId||'')) : (c['std_'+m]||'');
      const std=stds.find(s=>s.id===sid)||stds[0];"""
assert src.count(old2) == 1, ('old2', src.count(old2))
src = src.replace(old2, new2, 1)

open(p, 'w', encoding='utf-8').write(src)
print('ok')
