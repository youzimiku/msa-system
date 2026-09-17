# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
a = """  (d.plans||[]).forEach(p=>{
    if(!p.recordId) return;
    const rec=(d.grr||[]).find(x=>x.id===p.recordId)||(d.kappa||[]).find(x=>x.id===p.recordId);
    if(rec && rec.planId!==p.id){ rec.planId=p.id; rec.instId=p.instId; rec.instName=p.instName; rec.object=p.object||rec.object; rec.standard=p.standard||rec.standard; }
  });"""
b = """  (d.plans||[]).forEach(p=>{
    if(!p.recordId) return;
    const rec=(d.grr||[]).find(x=>x.id===p.recordId)||(d.kappa||[]).find(x=>x.id===p.recordId);
    if(rec){
      rec.planId=p.id; rec.instId=p.instId; rec.instName=p.instName; rec.object=p.object||rec.object; rec.standard=p.standard||rec.standard;
      const pr=p.params||{};
      if(rec.id.indexOf('GRR-')===0 && pr.ops!==undefined){ rec.numOps=pr.ops; rec.numTrials=pr.trials!==undefined?pr.trials:rec.numTrials; rec.numParts=pr.parts!==undefined?pr.parts:rec.numParts; }
    }
  });"""
assert src.count(a) == 1, src.count(a)
src = src.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
