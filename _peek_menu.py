# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('=== 1230-1345 区域 ===')
for i in range(1229, 1345):
    print(i + 1, '|', lines[i].rstrip()[:200])
