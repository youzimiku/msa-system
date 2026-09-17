# -*- coding: utf-8 -*-
"""探查：计划 result 显示、校准/样本状态 Tag、GrrPage/KappaPage/AnlPage 录入按钮"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) 计划 result 显示
print('=== 计划 result 显示 ===')
for m in re.finditer(r'\.result', s):
    a=max(0,m.start()-70); ctx=s[a:m.start()+40].replace('\n',' ')
    if 'p.result' in ctx or "r.result" in ctx or "plan.result" in ctx or "v.result" in ctx:
        print(' at', m.start(), '::', ctx[-110:])

# 2) 校准状态 Tag
print('\n=== 校准状态 Tag ===')
for m in re.finditer(r'正常.*临期|calibTag|calibStatus|class=".*calib', s):
    a=max(0,m.start()-80); print(' at', m.start(), '::', s[a:m.start()+120].replace('\n',' ')[-180:])

# 3) 样本状态 Tag
print('\n=== 样本状态 Tag ===')
for m in re.finditer(r'已测量|待测量', s):
    a=max(0,m.start()-60); print(' at', m.start(), '::', s[a:m.start()+80].replace('\n',' ')[-140:])
