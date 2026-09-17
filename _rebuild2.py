# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

old = """  const REBUILD=(key)=>{ const seen={}; d[key]=(d[key]||[]).filter(r=>{ if(seen[r.id]) return false; seen[r.id]=1; return SEED_IDS[key].indexOf(r.id)>=0; }); (d[key]||[]).forEach(r=>{ const f=SEED_F[r.id]; if(f) Object.assign(r,f); if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } }); };"""
new = """  const GEN_STB01=()=>{ const arr=[]; const base=[9.9979,9.9987,9.9996,10.0004,10.0013]; for(let g=0;g<25;g++){ const row=[]; for(let k=0;k<5;k++){ row.push(base[(g+k)%5]); } arr.push(row); } return arr; };
  const REBUILD=(key)=>{
    const seen={};
    d[key]=(d[key]||[]).filter(r=>{ if(seen[r.id]) return false; seen[r.id]=1; return SEED_IDS[key].indexOf(r.id)>=0; });
    SEED_IDS[key].forEach(id=>{ if(!seen[id]){ const f=SEED_F[id]||{}; const rec=Object.assign({id:id, method:'', analysisDate:'', analyst:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:'种子补录（演示数据）'}, f); if(id==='STB-2026-001'){ rec.raw=GEN_STB01(); rec.sampleNames=['轴径 φ10 标准件']; rec.opsNames=['赵磊','刘青']; rec.stations=['1号工位','2号工位']; } d[key].push(rec); } });
    (d[key]||[]).forEach(r=>{ const f=SEED_F[r.id]; if(f) Object.assign(r,f); if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } });
  };"""
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
