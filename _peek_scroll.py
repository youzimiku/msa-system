# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
i = c.find("title:'样品数范围'")
# 向后找 scroll 配置（在 mergeCols 数组结束后的 Table scroll 属性）
seg = c[i:i+3000]
j = seg.find('scroll')
while j != -1 and j < len(seg):
    print('scroll@', j, ':', seg[j:j+40])
    j = seg.find('scroll', j+1)
