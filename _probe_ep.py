# -*- coding: utf-8 -*-
"""探查：EntryPage 全貌、GrrEntry return、.tiny/.mono 样式、planStatusView、openGrr 调用点、seed 六类记录"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()

# 1) EntryPage 定义到结束（找下一个顶层 function）
i = s.find('function EntryPage')
end = s.find('\nfunction ', i+10)
print('=== EntryPage @ %d ~ %d (%d chars) ===' % (i, end, end-i))
print(s[i:i+min(end-i, 6000)])
