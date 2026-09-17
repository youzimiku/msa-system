# -*- coding: utf-8 -*-
"""查看 buildSeed 的 return 对象与六类台账 seed 记录"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

i = s.find('function buildSeed')
# 找 buildSeed 结束（下一个 function 或 return 块）
seg = s[i:i+200000]
# 找 return { 的位置
mret = re.search(r'return\s*\{', seg)
print('return at', mret.start() if mret else None)
if mret:
    seg2 = seg[mret.start(): mret.start()+40000]
    print(seg2[:3500])
