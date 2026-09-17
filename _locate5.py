# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('=== 组成员 列 ===')
for i, l in enumerate(lines):
    if '组成员' in l and 'title' in l:
        print(i + 1, '|', l.rstrip()[:250])
print()
print('=== 成员器具（多选） ===')
for i, l in enumerate(lines):
    if '成员器具' in l:
        print(i + 1, '|', l.rstrip()[:250])
