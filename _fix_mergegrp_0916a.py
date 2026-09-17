# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

old = "  d.samplingRules=(d.samplingRules||[]).filter(r=>r.method!=='resolution');\n  d.resolution=[];"
new = "  d.samplingRules=(d.samplingRules||[]).filter(r=>r.method!=='resolution');\n  d.resolution=[];\n  /* 迁移：线性/偏倚方法组统一为 LIN_BIAS（2026-09-16 口径，兼容旧本地数据） */\n  (d.anMethods||[]).forEach(m=>{ if(m.code==='LINEAR'||m.code==='BIAS'){ if(m.canMerge==='是'||m.mergeWith){ m.mergeWith='LIN_BIAS'; } } });"
assert t.count(old) == 1, '锚点不唯一或不存在'
t = t.replace(old, new)

io.open(P, 'w', encoding='utf-8').write(t)
print('已加入方法组归一迁移逻辑')
