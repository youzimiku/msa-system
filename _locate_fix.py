# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('=== 1) 卡帕/人员组 相关行 ===')
for i, l in enumerate(lines):
    if '卡帕' in l or ('人员组' in l and 'KAPPA' in l.upper()):
        print(i + 1, '|', l.rstrip()[:200])
print()
print('=== 2) 检验方法 code/name 渲染相关 ===')
kws = ['anMethods', 'methodCode', 'methodName', '检验方法', '方法代码', '方法名称']
for i, l in enumerate(lines):
    if any(k in l for k in kws) and ('render' in l or 'map' in l or 'label' in l or 'column' in l.lower() or 'title' in l):
        print(i + 1, '|', l.rstrip()[:200])
