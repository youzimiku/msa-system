# -*- coding: utf-8 -*-
"""找 linear/stability/cgcgk/resolution 在 buildSeed 的生成方式"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function buildSeed')
j = s.find('function applyFieldDefaults')
seg = s[i:j]

print('=== buildSeed 段内 LIN-/STB-/CG-2026/RES- 出现 ===')
for pref in ["'LIN-", "'STB-", "'CG-", "'RES-", 'LIN-', 'STB-', 'CG-2026', 'RES-']:
    ms = [m.start() for m in re.finditer(re.escape(pref), seg)]
    print(pref, '->', len(ms), '处', ms[:8])

# linear 数组生成：搜索 "linear" 在 buildSeed 内
print('\n=== linear 关键词上下文 ===')
for m in re.finditer(r'linear', seg):
    a = max(0, m.start()-50)
    print(' at', m.start(), '::', seg[a:m.start()+70].replace('\n',' ')[-120:])
