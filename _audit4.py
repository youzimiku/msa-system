# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
for i, l in enumerate(lines):
    ll = l.lower()
    if 'cgcgk' in ll and ('id:' in l or 'const' in l or 'dataIndex' in l or 'kind:' in l or 'keys:' in l):
        print(i + 1, l.rstrip()[:200])
