# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()

print('=== 器具组维护 / 计量器具台账 出现处 ===')
for i, l in enumerate(lines):
    if '器具组维护' in l or '计量器具台账' in l:
        print(i + 1, '|', l.rstrip()[:200])
print()
print('=== key: ledger 出现处 ===')
for i, l in enumerate(lines):
    if "'ledger'" in l or '"ledger"' in l:
        print(i + 1, '|', l.rstrip()[:200])
