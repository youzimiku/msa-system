# -*- coding: utf-8 -*-
"""取样规则对齐业务速查表（默认值 + 可调参数化）— 第 1 步：常量/seed/spawnRecord/文案"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# 1) TYPE_PARAMS：业务默认值（KAPPA 3 次、线性每件 12 次+偏倚 15 次、稳定性每期 5 次）
rep("""const TYPE_PARAMS = { 'GRR':{ops:3,trials:3,parts:10}, 'KAPPA':{ops:3,trials:1,parts:50},
  'linear':{stds:5,per:10,points:5}, 'stability':{groups:25,per:3,span:'4周~3个月'}, 'cgcgk':{runs:50}, 'resolution':{none:1} };""",
"""const TYPE_PARAMS = { 'GRR':{ops:3,trials:3,parts:10}, 'KAPPA':{ops:3,trials:3,parts:50},
  'linear':{stds:5,per:12,points:5,biasRuns:15}, 'stability':{groups:25,per:5,span:'4周~3个月'}, 'cgcgk':{runs:50}, 'resolution':{none:1} };""")

# 2) SAMPLING 文案：对齐业务《取样数量规则速查》（默认规则 + 可调范围）
rep("""const SAMPLING = {
  'linear':'线性+偏倚合并取样：线性取 5 个标准件（鉴定证书/高等级量具真值）覆盖 0/25/50/75/100% 量程点、每件测 10~12 次；偏倚分析以标准件为对象重复测 15 次，先正态性检验（P>0.05）再判"0"是否落在 95% 置信区间',
  'stability':'稳定性单独取样：长周期跨 4 周~3 个月，固定参照仪/工位，每期 3~5 次，取 25 个子组，走 SPC 判异模型',
  'GRR':'重复性+再现性合并取样：10 个生产件 × 3 人 × 每件 2~3 次（60~90 组）；仅交叉表+方差分析法(ANOVA)，不做嵌套',
  'KAPPA':'KAPPA（计数型）取样：50 个零件 × 3 人盲测判定（业务报告样例 50 件/3 人/每件 3 次，系统演示为每件 1 次二分类判定），与参考值交叉表 + 检验员间交叉 + 有效性/错误率/错误警报率判定',
  'cgcgk':'Cg/Cgk 单独取样（VDA Type1）：标准件独立装夹连续测 50 次，参考值±10% 标准误控制线，输出 Cg/Cgk',
  'resolution':'分辨率不取样：直接录入分辨率值，与过程公差比对（分辨率应 ≤ 1/10 公差）'
};""",
"""const SAMPLING = {
  'linear':'线性+偏倚合并取样（业务速查默认）：线性 5 个标准件（鉴定证书/高等级量具真值）覆盖 0/25/50/75/100% 量程点 × 每件 12 次（10~12 次可调，读数 50~60）；偏倚 1 件标准件重复测 15 次（10~15 次可调，真值可追溯），先正态性检验（P>0.05）再判"0"是否落在 95% 置信区间',
  'stability':'稳定性单独取样（业务速查默认）：长周期跨 4 周~3 个月，固定参照仪/工位，每期 5 次（3~5 次可调）× 25 个子组（≥25，读数 75~125），走 SPC 判异模型',
  'GRR':'重复性+再现性合并取样（业务速查默认）：10 个生产件 × 3 人 × 每件 3 次（2~3 次可调，读数 60~90）；覆盖过程散差、重新装夹；盲测随机序，含 EV+AV+NDC；仅交叉表+方差分析法(ANOVA)，不做嵌套',
  'KAPPA':'KAPPA（计数型）取样（业务速查默认）：50 件 × 3 人 × 每件 3 次（20~50 件、2~5 人可调，读数 450；业务报告样例 50 件/3 人/每件 1 次判定），与参考值交叉表 + 检验员间交叉 + 有效性/错误率/错误警报率三档判定',
  'cgcgk':'Cg/Cgk 单独取样（VDA Type1，业务速查默认）：1 件标准件（中值）独立装夹连续测 50 次（≥50 次可调），参考值±10% 标准误控制线，输出 Cg/Cgk（偏倚打包进 Cgk）',
  'resolution':'分辨率不取样：直接录入分辨率值，与过程公差比对（分辨率应 ≤ 1/10 公差；NDC 由 GRR 验算）'
};""")

# 3) seed 默认：KAPPA 3 次、50 件
rep("numOps:s.numOps||3, numTrials:s.numTrials||(kappa?1:3), numParts:s.numParts||(kappa?30:10),",
    "numOps:s.numOps||3, numTrials:s.numTrials||3, numParts:s.numParts||(kappa?50:10),")

# 4) spawnRecord：KAPPA 增加 numTrials、partsN 默认 50
rep("""    const rid = 'KPA-'+TODAY.slice(0,4)+'-'+String(s.kappa.length+1).padStart(3,'0');
    const opsN=o.params?Number(o.params.ops)||3:3, partsN=o.params?Number(o.params.parts)||30:30;
    s.kappa.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, kind:'计数型(合格/不合格)',
      standard:o.standard||'', numApp:opsN, numSamples:partsN, sampleGroup:findSampleGroupForPlan(s,planId),""",
"""    const rid = 'KPA-'+TODAY.slice(0,4)+'-'+String(s.kappa.length+1).padStart(3,'0');
    const opsN=o.params?Number(o.params.ops)||3:3, partsN=o.params?Number(o.params.parts)||50:50, trialsN=o.params?Number(o.params.trials)||3:3;
    s.kappa.push({ id:rid, planId, instId:o.instId||p.instId, instName:o.instName||p.instName, object:o.object||p.object, kind:'计数型(合格/不合格)',
      standard:o.standard||'', numApp:opsN, numSamples:partsN, numTrials:trialsN, sampleGroup:findSampleGroupForPlan(s,planId),""")

# 5) spawnRecord：linear 从 params 读 stds/per/points/biasRuns
rep("      method:o.method||'线性回归+偏移t检验（5标准件覆盖量程）', standard:o.standard||'', stds:5, per:10, points:5,",
    "      method:o.method||'线性回归+偏移t检验（5标准件覆盖量程）', standard:o.standard||'', stds:o.params?Number(o.params.stds)||5:5, per:o.params?Number(o.params.per)||12:12, points:o.params?Number(o.params.points)||5:5, biasRuns:o.params?Number(o.params.biasRuns)||15:15,")

# 6) spawnRecord：stability 从 params 读 groups/per
rep("      method:o.method||'均值-极差控制图（SPC判异模型）', standard:o.standard||'', groups:25, per:3, span:'4周~3个月',",
    "      method:o.method||'均值-极差控制图（SPC判异模型）', standard:o.standard||'', groups:o.params?Number(o.params.groups)||25:25, per:o.params?Number(o.params.per)||5:5, span:'4周~3个月',")

# 7) spawnRecord：cgcgk 从 params 读 runs
rep("      method:o.method||'Type1 能力指数（VDA 参考值±10%标准误）', standard:o.standard||'', runs:50, refValue:'',",
    "      method:o.method||'Type1 能力指数（VDA 参考值±10%标准误）', standard:o.standard||'', runs:o.params?Number(o.params.runs)||50:50, refValue:'',")

# 8) 定型弹窗取样策略提示
rep("取样策略（会议固化）：{SAMPLING[type]||''}；GRR/KAPPA 建议操作员 3×试验 3×样本 ≥10（KAPPA 样本 ≥30）；线性/偏移 5 标准件×10 次；稳定性 25 子组；Cg/Cgk 50 次；分辨率不取样。检验标准定义在「零件/工序」上。",
    "取样策略（业务确认默认值，样品数/人数/次数可调节）：{SAMPLING[type]||''}。默认 GRR 10 件×3 人×3 次、KAPPA 50 件×3 人×3 次、线性 5 标准件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次；下方 人数/次数/样本数 可改，改后按新参数生成录入矩阵。检验标准定义在「零件/工序」上。")

# 9) AnlPage 操作区默认取样对象
rep("{CFG.params(rows[0]||{stds:5,per:10,groups:25,runs:50})}",
    "{CFG.params(rows[0]||{stds:5,per:12,points:5,groups:25,runs:50})}")

open(p, 'w', encoding='utf-8').write(s)
print('step1 OK, len:', len(s))
