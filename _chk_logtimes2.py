# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for v in ["2026-08-30 14:22", "2026-09-01 09:15", "2026-09-05 16:40"]:
    print('==', v)
    start = 0
    while True:
        i = c.find(v, start)
        if i < 0:
            break
        print('  at', i, ':', repr(c[max(0,i-70):i+30]))
        start = i + 1
