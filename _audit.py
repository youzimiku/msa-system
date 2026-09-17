# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').readlines()

def show(kw, label, limit=45):
    print('==== ' + label + ' ====')
    n = 0
    for i, l in enumerate(lines):
        s = l.strip()
        if kw in s:
            print(i + 1, s[:230])
            n += 1
            if n >= limit:
                break
    print()

show('prototype', 'prototype字段')
show('样机', '样机')
show('特性编号', '特性编号')
show('特性名称', '特性名称')
show('质量特性', '质量特性(菜单/标题)')
show('instGroups', 'instGroups定义')
show('trigger', 'trigger任务来源')
show('charGroup', '器具组')
show('卡帕', '卡帕')
