# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old = """    (d[key]||[]).forEach(r=>{ const f=SEED_F[r.id]; if(f) Object.assign(r,f); if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } });"""
new = """    (d[key]||[]).forEach(r=>{ const f=SEED_F[r.id]; if(f) Object.assign(r,f); if(key==='grr'&&r.operators) r.opsNames=r.operators.map(n=>String(n).split('·').pop()).filter(n=>!/^(操作员[ABCDE]|检验员[甲乙丙丁戊])$/.test(n)); if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } });"""
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
