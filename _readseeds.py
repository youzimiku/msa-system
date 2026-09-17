# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
targets = ["id:'STB-2026-002'", "id:'STB-2026-003'", "id:'CG-2026-003'", "id:'LIN-2026-002'"]
for t in targets:
    for i, l in enumerate(lines):
        if t in l:
            print('=====', t, '@', i + 1)
            for j in range(i, min(i + 10, len(lines))):
                print('   ', lines[j].rstrip()[:230])
            break
