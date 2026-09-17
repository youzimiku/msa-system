# -*- coding: utf-8 -*-
"""seed 演示数据验证：MSAP-2026-009 多方法计划"""
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

plan = s[s.find("id:'MSAP-2026-009'"):]
plan = plan[:plan.find('};')+2]
print('== MSAP-2026-009 ==')
print(plan.replace('\n', '⏎'))
print()

# 三条记录存在性
for rid in ['GRR-2026-004', 'STB-2026-003', 'CG-2026-004']:
    i = s.find("id:'" + rid + "'")
    seg = s[i:i+420].replace('\n', ' ')
    ok = ('planId:\'MSAP-2026-009\'' in seg) and ('reviewStatus:\'待采集\'' in seg)
    print(rid, 'OK' if ok else 'CHECK', '::', seg[:150])
    print()

# 计划记录聚合函数存在
for fn in ['function planRecords', 'function syncPlanFromRecord', 'function spawnRecord', 'function instHasActivePlan']:
    print(fn, ':', 'OK' if fn in s else 'MISSING')
