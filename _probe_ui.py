# -*- coding: utf-8 -*-
"""探查 StatusTag/VerdictTag 定义与内联样式分布"""
import io, re
from collections import Counter

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function StatusTag')
print('--- StatusTag ---')
print(s[i:i+900] if i >= 0 else 'not found')
j = s.find('function VerdictTag')
print('--- VerdictTag ---')
print(s[j:j+900] if j >= 0 else 'not found')

print('inline fontSize:', len(re.findall(r'fontSize\s*:', s)))
print('inline color:', len(re.findall(r'color\s*:\s*[\'\"#]', s)))
cs = Counter(re.findall(r'color\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|white|#fff|inherit)', s))
print('color value counts (top 25):')
for k, v in cs.most_common(25):
    print('  ', k, v)
