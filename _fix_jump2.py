# -*- coding: utf-8 -*-
import io
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
# PlanTaskDrawer 内误删的 '['（定位在 PlanTaskDrawer 组件内第一个 'const cols='）
i = s.find('function PlanTaskDrawer')
j = s.find('const cols=', i)
assert j > 0
# 检查该处是否为 'const cols=\n    {'（缺 [）
if s[j:j+12] == 'const cols=\n':
    s = s[:j] + 'const cols=[\n' + s[j+12:]
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('fixed')
