# -*- coding: utf-8 -*-
"""查 AnlDetail / GrrDetail 数据来源（kpis 字段？），以及已批准 seed 记录 GRR-2026-001 的完整字段"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function AnlDetail')
j = s.find('\nfunction ', i+10)
print('=== AnlDetail @ %d ~ %d ===' % (i, j))
print(s[i:i+min(j-i, 3200)])
