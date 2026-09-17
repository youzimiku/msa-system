# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = io.open(P, encoding='utf-8').read().splitlines()
targets = [1754, 2060, 2237, 2374, 2912, 3108, 3360, 3609, 3724, 3965, 4250, 4429, 4593]
for t in targets:
    owner = '?'
    for i in range(t-1, max(0, t-500), -1):
        m = re.search(r'function (\w+Page)\s*\(', lines[i])
        if m:
            owner = m.group(1)
            break
        m2 = re.search(r'<PageHead title="([^"]+)"', lines[i])
        if m2:
            owner = m2.group(1) + ' (PageHead)'
            break
    print(t, '->', owner)
