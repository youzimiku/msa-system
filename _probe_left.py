# -*- coding: utf-8 -*-
"""列出残留 '-' 占位上下文"""
import io, re

s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
pat = re.compile(r"return '-';\|\? '-'|:'-'|>'-'<|'-'</span>|: '-'")
for m in pat.finditer(s):
    a = max(0, m.start()-70)
    print(m.start(), '::', s[a:m.start()+50].replace('\n', ' ')[-120:])
