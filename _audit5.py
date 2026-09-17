# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if "id:'GRR-2026-003'" in l or "id:'GRR-2026-004'" in l:
        print('---', i + 1)
        print(l.rstrip()[:300])
        if i + 1 < len(lines):
            print(lines[i + 1].rstrip()[:300])
