# -*- coding: utf-8 -*-
"""修正 AnlPage useEffect：resolution 待采集 → 打开内嵌录入；其他 → data 页"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

old = "if(rec.reviewStatus==='待采集'){ if(kind==='resolution') setDetail(rec); else { DataOpen={kind,id:rec.id}; NavAPI.go('data_'+kind); } } else setDetail(rec); }"
new = "if(rec.reviewStatus==='待采集'){ if(kind==='resolution') setEntryRec(rec); else { DataOpen={kind,id:rec.id}; NavAPI.go('data_'+kind); } } else setDetail(rec); }"
n = s.count(old)
print('AnlPage useEffect fix x%d' % n)
s = s.replace(old, new)
io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
