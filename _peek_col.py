# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
i = c.find("title:'分析类型', width:84")
print(repr(c[i-8:i+160]))
