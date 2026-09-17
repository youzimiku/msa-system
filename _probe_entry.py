# -*- coding: utf-8 -*-
"""探查：Entry 组件签名与 Drawer 包裹、EntryPage 完整、'-'分布、openGrr 184731 上下文、planStatusView"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) GrrEntry / KappaEntry / AnlEntry 定义头
for fn in ['function GrrEntry', 'function KappaEntry', 'function AnlEntry']:
    i = s.find(fn)
    print('=== %s @ %d ===' % (fn, i))
    print(s[i:i+900])
    print()

# 2) '-' 分布
print('=== dash 分布（抽样前 60 处）===')
cnt = 0
for m in re.finditer(r"'\-'|\|\|'-'|\| '-'", s):
    a = max(0, m.start()-60)
    ctx = s[a:m.end()+40].replace('\n', ' ')
    print(m.group(0), '::', ctx[-100:])
    cnt += 1
    if cnt >= 45:
        break
print('total dash-ish matches:', len(re.findall(r"'\-'|\|\|'-'|\| '-'", s)))
