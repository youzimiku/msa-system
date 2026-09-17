# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "    const ms = c.methods&&c.methods.length? c.methods : ((c.dataType==='计数型')?['KAPPA']:['GRR']);"
new = "    const ms = c.methods&&c.methods.length? c.methods.map(x=>typeof x==='string'?x:(x.method||'')).filter(Boolean) : ((c.dataType==='计数型')?['KAPPA']:['GRR']);"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
