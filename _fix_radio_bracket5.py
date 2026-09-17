# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
n = src.count('}]}]}/>')
print('命中 }]}]}/>:', n)
src = src.replace('}]}]}/>', '}]}/>')
open(p, 'w', encoding='utf-8').write(src)
print('OK')
