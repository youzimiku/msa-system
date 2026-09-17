# -*- coding: utf-8 -*-
"""v2.6 第六批：addMonths 空值/非法日期守卫（修复创建弹窗 Invalid time value 白屏）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

old = "function addMonths(dateStr, m){const d=new Date(dateStr);d.setMonth(d.getMonth()+m);return d.toISOString().slice(0,10)}"
new = "function addMonths(dateStr, m){ if(!dateStr) return ''; const d=new Date(dateStr); if(isNaN(d.getTime())) return ''; d.setMonth(d.getMonth()+(m||0)); return d.toISOString().slice(0,10); }"
assert s.count(old) == 1, 'addMonths 命中 %d' % s.count(old)
s = s.replace(old, new)

open(P, 'w', encoding='utf-8').write(s)
print('batch6 OK 长度', len(s))
