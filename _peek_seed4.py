# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for rid in ['GRR-2026-003', 'STB-2026-002', 'CG-2026-003', 'LIN-2026-002']:
    i = s.find("id:'"+rid+"'")
    if i < 0:
        print(rid, 'NOT FOUND'); continue
    # 找对象边界：从 {id 到 }
    j = s.find('}', i)
    print('===', rid, '===')
    print(s[i-60:j+1])
    print()
# standards id
for m in re.finditer(r"id:'([^']*标准[^']*)'", s[:80000]):
    print('std:', m.group(1))
