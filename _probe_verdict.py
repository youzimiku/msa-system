# -*- coding: utf-8 -*-
"""探查结论列取值与生成逻辑"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# verdictTagColor / verdictColor
i = s.find('verdictTagColor')
print('--- verdictTagColor / verdictColor ---')
print(s[i-100:i+700])

# 所有结论字符串
cons = set(re.findall(r"'((?:优秀|良好|可接受|有条件接受|不可接受)[^']*)'", s))
print('\n结论取值集合:')
for c in sorted(cons):
    print('  ', c)

# VerdictTag / verdictColor 定义
j = s.find('function verdictColor')
print('\n--- verdictColor 定义 ---')
print(s[j:j+600] if j >= 0 else 'not found')
