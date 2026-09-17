# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()
print('=== 1360-1390 区域（铃铛按钮等） ===')
for i in range(1359, 1390):
    print(i + 1, '|', lines[i].rstrip()[:180])
print()
print('=== openInst / openCalibInst 调用方 ===')
for i, l in enumerate(lines):
    if 'openInst' in l or 'openCalibInst' in l:
        print(i + 1, '|', l.rstrip()[:180])
