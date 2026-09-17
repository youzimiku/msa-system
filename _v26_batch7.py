# -*- coding: utf-8 -*-
"""v2.6 第七批：修复 KAPPA 表单编号重复前缀（GJZ-MSA-KPA-KPA-… → GJZ-MSA-KPA-…）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

old = "children:<span className=\"mono\">GJZ-MSA-KPA-{rec.id}</span>}"
new = "children:<span className=\"mono\">GJZ-MSA-{rec.id}</span>}"
assert s.count(old) == 1, '表单编号命中 %d' % s.count(old)
s = s.replace(old, new)

open(P, 'w', encoding='utf-8').write(s)
print('batch7 OK 长度', len(s))
