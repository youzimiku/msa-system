# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
i = c.find("title:'样品数范围'")
seg = c[i:i+6000]
j = seg.find('scroll')
cnt = 0
while j != -1 and cnt < 20:
    print('scroll@', j, ':', seg[max(0,j-30):j+50].replace('\n',' '))
    j = seg.find('scroll', j+1)
    cnt += 1
print('---done')
