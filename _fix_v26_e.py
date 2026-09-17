# -*- coding: utf-8 -*-
"""anlOpenRec 智能分派与 openAnl 一致"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

old = "function anlOpenRec(kind,id){ if(kind==='resolution'){ AnlOpen={kind,id}; NavAPI.go('anl_resolution'); } else { EntryOpen={kind,id}; NavAPI.go(ENTRY_PAGE[kind]); } }"
new = "function anlOpenRec(kind,id){ if(kind==='resolution'){ AnlOpen={kind,id}; NavAPI.go('anl_resolution'); } else { const rec=(Store.data[ANA_CFG[kind].arr]||[]).find(g=>g.id===id); if(rec&&rec.reviewStatus==='待采集'){ DataOpen={kind,id}; NavAPI.go('data_'+kind); } else { AnlOpen={kind,id}; NavAPI.go(ANA_PAGE[kind]); } } }"
n = s.count(old)
print('anlOpenRec x%d' % n)
assert n == 1
s = s.replace(old, new)
io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
