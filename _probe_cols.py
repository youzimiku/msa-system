# -*- coding: utf-8 -*-
"""探查 JSX 内联 style 中的 color，以及状态列 width 分布"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 找 style={{ ... }} 内的 color
print('--- JSX style color ---')
for m in re.finditer(r'style=\{\{[^}]*?\}\}', s):
    if 'color' in m.group(0):
        print(m.group(0)[:160])
print()
print('--- title 状态 列 width ---')
for m in re.finditer(r"\{title:'状态'[^}]*\}", s):
    print(m.group(0))
print()
print('--- title 含 状态/结论 width ---')
for m in re.finditer(r"\{title:'(状态|结论|校准状态|复评提醒)'[^}]*\}", s):
    print(m.group(0)[:120])
