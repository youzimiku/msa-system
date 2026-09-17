# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
for k in ['grr','kappa','linear','stability','cgcgk']:
    old = "if(page==='data_"+k+"') return <DataEntryPage kind=\""+k+"\"/>;"
    new = "if(page==='data_"+k+"') return <DataEntryPage key=\""+k+"\" kind=\""+k+"\"/>;"
    assert src.count(old) == 1, (k, src.count(old))
    src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
