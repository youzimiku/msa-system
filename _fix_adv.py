# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "else { const n=d.instGroups.filter(g=>g.id.startsWith('G-')).length+1; form.setFieldsValue({id:'G-'+String(n).padStart(2,'0'), calCycle:12, type:'inst'}); }"
new = "else { const n=d.instGroups.filter(g=>g.id.startsWith('G-')).length+1; form.setFieldsValue({id:'G-'+String(n).padStart(2,'0'), calCycle:12, type:'inst', remindAdvance:20}); }"
n = src.count(old)
print('新增默认值优化:', n, '次', '-> 替换' if n==1 else '!!跳过')
if n == 1:
    src = src.replace(old, new)
    open(p, 'w', encoding='utf-8').write(src)
    print('写入完成, 大小:', len(src))
