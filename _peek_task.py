# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# recKindId 定义
i = s.find('function recKindId')
print('recKindId @', i)
print(s[i:i+400].replace('\n','⏎') if i>0 else '')
print()
# PlanTaskDrawer 组件
j = s.find('PlanTaskDrawer')
k = s.find('function PlanTaskDrawer')
print('PlanTaskDrawer def @', k)
if k > 0:
    # 输出组件体
    seg = s[k:k+2600]
    print(seg.replace('\n', '⏎'))
