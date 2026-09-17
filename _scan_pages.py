# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('TOTAL', len(lines))
keys = ['MSA','台账','计划','器具','质量','特性','抽样','样本','校准','维护','录入','数据','仪表','GRR','KAPPA','被测','看板','分析','检验','分辨','精度']
for i, l in enumerate(lines):
    s = l.strip()
    if re.search(r'(label:|key:)\s*[\'"]', s):
        if any(k in s for k in keys):
            print(i+1, s[:160])
print('---TAB/页面标题---')
for i, l in enumerate(lines):
    s = l.strip()
    if re.search(r'(title:|name:)\s*[\'"]', s) and any(k in s for k in keys):
        print(i+1, s[:160])
