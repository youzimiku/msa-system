# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "  REBUILD('grr'); REBUILD('kappa'); REBUILD('linear'); REBUILD('stability'); REBUILD('cgcgk');\n  (d.plans||[]).forEach(p=>syncPlanFromRecord(d,p.id));"
new = "  REBUILD('grr'); REBUILD('kappa'); REBUILD('linear'); REBUILD('stability'); REBUILD('cgcgk');\n  /* 被测参数（质量特性）锚定种子：覆盖旧数据 methods 结构（字符串数组→对象数组）与字段口径 */\n  const SEED_CHARS={}; (typeof characteristics!=='undefined'?characteristics:[]).forEach(c=>{ SEED_CHARS[c.id]=c; });\n  (d.characteristics||[]).forEach(c=>{ const f=SEED_CHARS[c.id]; if(f) Object.assign(c,f); });\n  (d.plans||[]).forEach(p=>syncPlanFromRecord(d,p.id));"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
