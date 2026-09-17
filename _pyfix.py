# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 修复更名脚本残留的 "},children" 逗号
fixes = [
    ("{key:'id',label:'被测参数编号'},children:", "{key:'id',label:'被测参数编号',children:"),
    ("{key:'name',label:'被测参数名称'},children:", "{key:'name',label:'被测参数名称',children:"),
]
for a, b in fixes:
    n = src.count(a)
    print('fix', a[:40], 'count', n)
    src = src.replace(a, b)

open(p, 'w', encoding='utf-8').write(src)
print('done')
