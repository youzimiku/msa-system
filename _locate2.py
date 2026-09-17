# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('=== 所属方法 相关 ===')
for i, l in enumerate(lines):
    if '所属方法' in l:
        print(i + 1, '|', l.rstrip()[:230])
print()
print('=== 方法名称列 ===')
for i, l in enumerate(lines):
    if "title:'方法名称'" in l or 'title: "方法名称"' in l:
        print(i + 1, '|', l.rstrip()[:230])
print()
print('=== judgeRules 列定义区域（判断规则列表） ===')
for i, l in enumerate(lines):
    if 'judgeRules' in l and ('title' in l or 'dataIndex' in l):
        print(i + 1, '|', l.rstrip()[:230])
