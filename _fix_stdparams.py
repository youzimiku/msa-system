# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 1) stdsOf：优先从特性 methods 的 standardId 精确匹配
old1 = """  const stdsOf=(m,c)=>{
    const defStd = c? c['std_'+m] : '';
    const all=(d.standards||[]).filter(s=>s.status==='启用');
    const list=all.filter(s=> s.id===defStd || stdTypeOf(s.id)===m || s.method===m || (s.charIds&&s.charIds.length&&s.charIds.indexOf(c?c.id:'')>=0));
    return list.length? list : all;
  };"""
new1 = """  const stdsOf=(m,c)=>{
    const mm=(c&&c.methods)? (c.methods.find(x=>typeof x==='string'? x===m : x.method===m)||null) : null;
    const defStd = mm? (typeof mm==='string'? (c?c['std_'+m]:'') : (mm.standardId||'')) : (c?c['std_'+m]:'');
    const all=(d.standards||[]).filter(s=>s.status==='启用');
    const list=all.filter(s=> s.id===defStd || stdTypeOf(s.id)===m || s.method===m || (s.charIds&&s.charIds.length&&s.charIds.indexOf(c?c.id:'')>=0));
    return list.length? list : all;
  };"""
assert src.count(old1) == 1, ('old1', src.count(old1))
src = src.replace(old1, new1, 1)

# 2) pickChar：仅标准类型与方法一致时用标准取样参数，否则用方法默认（CGK 50次/线性 5×12）
old2 = "      const std=stds.find(s=>s.id===sid)||stds[0];\n      const sd=samplingDef(m);\n      cfg[m]={ std: std? std.id : '', ops: std&&Number(std.numOps)>0? Number(std.numOps) : sd.ops, trials: std&&Number(std.numTrials)>0? Number(std.numTrials) : sd.trials, parts: std&&Number(std.numParts)>0? Number(std.numParts) : sd.parts };"
new2 = "      const std=stds.find(s=>s.id===sid)||stds[0];\n      const sd=samplingDef(m);\n      const useStd = std && stdTypeOf(std.id)===m;\n      cfg[m]={ std: std? std.id : '', ops: useStd&&Number(std.numOps)>0? Number(std.numOps) : sd.ops, trials: useStd&&Number(std.numTrials)>0? Number(std.numTrials) : sd.trials, parts: useStd&&Number(std.numParts)>0? Number(std.numParts) : sd.parts };"
assert src.count(old2) == 1, ('old2', src.count(old2))
src = src.replace(old2, new2, 1)

open(p, 'w', encoding='utf-8').write(src)
print('ok')
