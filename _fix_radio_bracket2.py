# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "options={[{value:'',label:'全部'}].concat(ENUM.instStatus.map(c=>({value:c,label:c}))))/"
new = "options={[{value:'',label:'全部'}].concat(ENUM.instStatus.map(c=>({value:c,label:c})))}/"
print('命中:', src.count(old))
src = src.replace(old, new)
open(p, 'w', encoding='utf-8').write(src)
print('OK')
