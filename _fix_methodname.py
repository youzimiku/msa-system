# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = "const METHOD_NAME=(code)=>{ const d=Store.get(); const m=(d.anMethods||[]).find(x=>String(x.code).toLowerCase()===String(code||'').toLowerCase()); return m?m.name:code; };"
new = "const METHOD_NAME=(code)=>{ const d=Store.get(); const m=(d.anMethods||[]).find(x=>String(x.code).toLowerCase()===String(code||'').toLowerCase()); const n=m?m.name:code; return String(n).replace(/（[^）]*）/g,'').replace(/\\([^)]*\\)/g,''); };"
print('found:', old in src)
if old in src:
    src = src.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(src)
    print('done')
else:
    print('NOT FOUND')
