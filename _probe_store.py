# -*- coding: utf-8 -*-
"""探查：Store 初始化/applyFieldDefaults 时机、EntryPage 全貌、Entry 组件签名、'-'分布、planStatusView"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) Store 初始化
i = s.find('const Store =')
print('=== Store 定义 ===')
print(s[i:i+900] if i>=0 else 'not found')
j = s.find('applyFieldDefaults(')
print('\n=== applyFieldDefaults 调用点 ===')
for m in re.finditer('applyFieldDefaults', s):
    print(' at', m.start(), '::', s[max(0,m.start()-80):m.start()+60].replace('\n',' ')[-140:])
