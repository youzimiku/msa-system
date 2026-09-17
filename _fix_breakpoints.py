# -*- coding: utf-8 -*-
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig_len = len(s)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'expect %d of [%s...] got %d' % (n, old[:60], c)
    s = s.replace(old, new, n)

# ---------- A：新增 backfillMsa（闭环终态回写器具 lastMsa，滚动复评周期） ----------
anchor = '''  p.status = agg;
  const cons = recs.map(r=>r.conclusion).filter(c=>c&&c!=='-');
  p.result = recs.length>1 ? (cons.length? cons.join('；') : '-') : (recs[0].conclusion||'-');
}'''
backfill = anchor + '''
/* 分析闭环终态（已批准/已闭环）回写器具「上次MSA」，复评周期随之滚动（会议口径：汇总到器具并更新周期） */
function backfillMsa(s, planId){
  const p = s.plans.find(x=>x.id===planId); if(!p) return;
  (p.instIds||[p.instId]).forEach(iid=>{ const it=s.instruments.find(i=>i.id===iid); if(it) it.lastMsa=TODAY; });
}'''
rep(anchor, backfill, 1)

# 6 个终态操作点回写 lastMsa（审核通过 3 处 + 整改闭环 3 处）
rep('g.reviewDate=TODAY;syncPlanFromRecord(s,g.planId);logAction(',
    'g.reviewDate=TODAY;syncPlanFromRecord(s,g.planId);backfillMsa(s,g.planId);logAction(', 3)
rep('g.approveDate=TODAY;syncPlanFromRecord(s,g.planId);logAction(',
    'g.approveDate=TODAY;syncPlanFromRecord(s,g.planId);backfillMsa(s,g.planId);logAction(', 3)

# ---------- B：已批准（结论已出）不再拦截新计划；仪表盘 active/closed 口径同步 ----------
rep("['未定型','待采集','待审核','已批准','需整改']", "['未定型','待采集','待审核','需整改']", 2)
rep("const closed = plans.filter(p=>p.status==='已闭环'||p.status==='已关闭');",
    "const closed = plans.filter(p=>['已批准','已闭环','已关闭'].indexOf(p.status)>=0);", 1)

# ---------- C：关闭计划同步覆盖 6 类分析台账记录 ----------
rep("(s.grr.concat(s.kappa)).forEach(r=>{ if(r.planId===p.id) r.reviewStatus='已关闭'; });",
    "[s.grr,s.kappa,s.linear,s.stability,s.cgcgk,s.resolution].forEach(arr=>arr.forEach(r=>{ if(r.planId===p.id) r.reviewStatus='已关闭'; }));", 1)

# ---------- D：转 GRR/KAPPA 全部跳过时给出提示并中止跳转 ----------
rep("""    if(done) toast.ok('已转 '+t+' '+done+' 个计划（生成台账记录），跳转 '+(t==='GRR'?'GRR':'KAPPA')+' 台账');
    if(skipped) toast.warn(skipped+' 个计划已存在台账记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    NavAPI.go(t==='GRR'?'grr':'kappa');""",
"""    if(!done){ toast.warn('所选计划均未定型或缺少匹配的 '+t+' 检验标准，未执行转换'); setSelectedRowKeys([]); return; }
    if(done) toast.ok('已转 '+t+' '+done+' 个计划（生成台账记录），跳转 '+(t==='GRR'?'GRR':'KAPPA')+' 台账');
    if(skipped) toast.warn(skipped+' 个计划已存在台账记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    NavAPI.go(t==='GRR'?'grr':'kappa');""", 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig_len, ')')
