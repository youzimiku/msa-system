# -*- coding: utf-8 -*-
"""修复 PlanTaskDrawer 台账按钮跳转映射"""
import io
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

old = """function PlanTaskDrawer({plan, onClose}){
  const d=Store.get();
  const recs=planRecords(d, plan.id);
  const cols=["""
new = """const ENTRY_MAP={GRR:'entry_grr', KAPPA:'entry_kappa', linear:'entry_linear', stability:'entry_stability', cgcgk:'entry_cgcgk', resolution:'entry_resolution'};
function PlanTaskDrawer({plan, onClose}){
  const d=Store.get();
  const recs=planRecords(d, plan.id);
  const cols="""
assert s.count(old) == 1
s = s.replace(old, new)

old2 = """<Button size="small" type="link" onClick={()=>NavAPI.go('entry_'+recKindId(r))}>台账</Button>"""
new2 = """<Button size="small" type="link" onClick={()=>NavAPI.go(ENTRY_MAP[recKindId(r)]||'entry_grr')}>台账</Button>"""
assert s.count(old2) == 1
s = s.replace(old2, new2)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('PlanTaskDrawer 跳转已修复')
