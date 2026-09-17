# -*- coding: utf-8 -*-
"""seed 清理：删除 4 组 defaultInstId；原默认器具补样机标记"""
import io
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:50], n, cnt)
    s = s.replace(old, new)

for iid in ['JJQ-2024-001', 'JJQ-2024-007', 'JJQ-2023-010', 'JJQ-2024-008']:
    rep(", defaultInstId:'" + iid + "'", '')

for iid in ['JJQ-2023-010', 'JJQ-2024-001', 'JJQ-2024-007', 'JJQ-2024-008']:
    rep("{id:'" + iid + "',", "{id:'" + iid + "', prototype:'是',")

io.open(p, 'w', encoding='utf-8').write(s)
print('seed patched, len', len(s))
print('残留 defaultInstId:', s.count('defaultInstId'))
print('样机标记(seed):', s.count("prototype:'是'"))
