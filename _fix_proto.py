# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if "prototype:'是'" in l and 'JJQ-2024-001' in l:
        lines[i] = l.replace(", prototype:'是'", '', 1)
        print('fixed line', i + 1)
        break
open(p, 'w', encoding='utf-8').writelines(lines)
print('ok')
