# -*- coding: utf-8 -*-
"""探查：seed 数据量、EntryPage 结构、Entry 组件签名、'-'分布、planStatusView"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) seed 数据量：找 localStorage seed 定义
i = s.find('msa_demo_data')
print('=== seed 上下文（前 2500 字符）===')
seg = s[max(0,i-300): i+2500]
print(seg[:2500])
