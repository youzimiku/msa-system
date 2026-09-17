# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "    d[key]=(d[key]||[]).filter(r=>{ if(seen[r.id]) return false; seen[r.id]=1; return SEED_IDS[key].indexOf(r.id)>=0; });"
new = "    d[key]=(d[key]||[]).filter(r=>{ if(seen[r.id]) return false; seen[r.id]=1; return true; });"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
