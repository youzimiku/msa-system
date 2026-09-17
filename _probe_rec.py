# -*- coding: utf-8 -*-
"""探查：seed 六类台账记录内容 + openGrr 调用点 + spawnRecord 字段"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) openGrr / openKappa 调用点
print('=== openGrr / openKappa / openAnl 调用点 ===')
for m in re.finditer(r'openGrr|openKappa', s):
    ctx = s[max(0,m.start()-90):m.start()+30].replace('\n',' ')
    print(' at', m.start(), '::', ctx[-120:])

# 2) spawnRecord 形状（转换函数）
i = s.find("const rid = 'GRR-'")
print('\n=== 转换创建记录模板（前 2600）===')
print(s[max(0,i-900):i+2600])
