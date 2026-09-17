# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
anchor = """  /* 台账-计划锚点对齐（旧数据漂移修正）：以计划 recordId 为锚回写台账基础字段，状态/结论按种子口径对齐，保证演示数据跨页面一致 */
  const SEED_ST={'GRR-2026-001':'已批准','GRR-2026-002':'需整改','GRR-2026-003':'待采集','GRR-2026-004':'待采集','KPA-2026-001':'已批准','KPA-2026-002':'需整改','LIN-2026-001':'已批准','LIN-2026-002':'待采集','STB-2026-001':'已批准','STB-2026-002':'待采集','STB-2026-003':'待采集','CG-2026-001':'已批准','CG-2026-002':'待审核','CG-2026-003':'待采集'};
  const SEED_CON={'GRR-2026-001':'可接受','GRR-2026-002':'有条件接受','GRR-2026-003':'','GRR-2026-004':'','KPA-2026-001':'优秀(可接受)','KPA-2026-002':'不可接受-需改进','LIN-2026-001':'非常理想可接受','LIN-2026-002':'','STB-2026-001':'可接受','STB-2026-002':'','STB-2026-003':'','CG-2026-001':'可接受','CG-2026-002':'有条件接受','CG-2026-003':''};
  const ALIGN=(arr)=>{ (arr||[]).forEach(r=>{ if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } }); };
  ALIGN(d.grr); ALIGN(d.kappa); ALIGN(d.linear); ALIGN(d.stability); ALIGN(d.cgcgk);
  (d.plans||[]).forEach(p=>{
    if(!p.recordId) return;
    const rec=(d.grr||[]).find(x=>x.id===p.recordId)||(d.kappa||[]).find(x=>x.id===p.recordId);
    if(rec && rec.planId!==p.id){ rec.planId=p.id; rec.instId=p.instId; rec.instName=p.instName; rec.object=p.object||rec.object; rec.standard=p.standard||rec.standard; }
  });
  (d.plans||[]).forEach(p=>syncPlanFromRecord(d,p.id));
}
"""
needle = '}\n\n/* ---------------- 枚举字典 ---------------- */'
assert src.count(needle) == 1, src.count(needle)
src = src.replace(needle, anchor + '\n/* ---------------- 枚举字典 ---------------- */', 1)
open(p, 'w', encoding='utf-8').write(src)
print('reinserted ok')
