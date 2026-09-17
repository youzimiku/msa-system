# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    cnt = s.count(old)
    if cnt != 1:
        print('WARN count=%d for: %s' % (cnt, old[:60])); return
    s = s.replace(old, new)
    print('OK:', old[:46])

# S1 seed 返回增加新分析台账数组
rep("  return { me:{ name:'李工程师', role:'quality', roleName:'质量工程师' },\n           instruments, calibrations, standards, plans, samples, sampleItems, grr, kappa, logs, extrapolations:[], instGroups };",
    "  return { me:{ name:'李工程师', role:'quality', roleName:'质量工程师' },\n           instruments, calibrations, standards, plans, samples, sampleItems, grr, kappa, linear, stability, cgcgk, resolution, logs, extrapolations:[], instGroups };")

# S2 applyFieldDefaults 兜底新数组 + 器具样机标记
rep("  if(!d.extrapolations) d.extrapolations=[];\n  if(!d.instGroups) d.instGroups=[];",
    "  if(!d.extrapolations) d.extrapolations=[];\n  if(!d.instGroups) d.instGroups=[];\n  if(!d.linear) d.linear=[]; if(!d.stability) d.stability=[]; if(!d.cgcgk) d.cgcgk=[]; if(!d.resolution) d.resolution=[]; // 新增分析方法台账（线性/偏移、稳定性、Cg/Cgk、分辨率）")

rep("      lastMsa:i.lastMsa||(msaDates.length?msaDates[msaDates.length-1]:'-'),\n      extrapolatedFrom:i.extrapolatedFrom||''\n    });",
    "      lastMsa:i.lastMsa||(msaDates.length?msaDates[msaDates.length-1]:'-'),\n      extrapolatedFrom:i.extrapolatedFrom||'',\n      prototype:i.prototype||((i.id==='JJQ-2024-001'||i.id==='JJQ-2024-007'||i.id==='JJQ-2023-010'||i.id==='JJQ-2024-008')?'是':'否') // 样机标记：周期性校验自动筛选\n    });")

# S3 ENUM 扩展：分析方法全量 + 方法默认 + 取样策略
rep("  taskType: ['GRR','KAPPA'],",
    "  taskType: ['GRR','KAPPA'], // 兼容旧定型按钮\n  analysisTypes: ['GRR','KAPPA','linear','stability','cgcgk','resolution'], // 会议口径：特性-量具-方法，一器一计划一方法\n  analysisNames: { 'GRR':'GRR（重复性+再现性）','KAPPA':'KAPPA（计数型一致性）','linear':'线性/偏移性','stability':'稳定性','cgcgk':'Cg/Cgk（Type1）','resolution':'分辨率' },")

rep("  taskMethod: { 'GRR':['均值-极差法(Xbar-R)','方差分析法(ANOVA)'], 'KAPPA':['计数型一致性(KAPPA)'] },",
    "  taskMethod: { 'GRR':['均值-极差法(Xbar-R)','方差分析法(ANOVA)'], 'KAPPA':['计数型一致性(KAPPA)'],\n    'linear':['线性回归+偏移t检验（5标准件覆盖量程）'], 'stability':['均值-极差控制图（SPC判异模型）'], 'cgcgk':['Type1 能力指数（VDA 参考值±10%标准误）'], 'resolution':['直接录入（不取样）'] },")

# S4 TYPE_STDS/TYPE_PARAMS 扩展
rep("const TYPE_STDS = { 'GRR':['STD-MSA-001','STD-MSA-002'], 'KAPPA':['STD-MSA-003','STD-MSA-004'] };\nconst TYPE_PARAMS = { 'GRR':{ops:3,trials:3,parts:10}, 'KAPPA':{ops:3,trials:1,parts:30} };",
    "const TYPE_STDS = { 'GRR':['STD-MSA-001','STD-MSA-002'], 'KAPPA':['STD-MSA-003','STD-MSA-004'] };\nconst TYPE_PARAMS = { 'GRR':{ops:3,trials:3,parts:10}, 'KAPPA':{ops:3,trials:1,parts:30},\n  'linear':{stds:5,per:10,points:5}, 'stability':{groups:25,per:3,span:'4周~3个月'}, 'cgcgk':{runs:50}, 'resolution':{none:1} };\n/* 会议确认的取样策略（固化展示；线性+偏移合并取样、GRR/Kappa合并取样、稳定性单独、Cg/Cgk单独、分辨率不取样） */\nconst SAMPLING = {\n  'linear':'线性+偏移性合并取样：5 个标准件（具鉴定证书/高等级量具真值）覆盖 0/25/50/75/100% 量程点，每件测 10~12 次（共 50~60 组）',\n  'stability':'稳定性单独取样：长周期跨 4 周~3 个月，固定参照仪/工位，每期 3~5 次，取 25 个子组，走 SPC 判异模型',\n  'GRR':'重复性+再现性合并取样：10 个生产件 × 3 人 × 每件 2~3 次（60~90 组）；仅交叉表+方差分析法(ANOVA)，不做嵌套',\n  'KAPPA':'与 GRR 相同取样（计数型）：检验员×参考值交叉表 + 检验员间交叉 + 漏发/误发判定 + 有效性（报告格式待万工确认）',\n  'cgcgk':'Cg/Cgk 单独取样（VDA Type1）：标准件独立装夹连续测 50 次，参考值±10% 标准误控制线，输出 Cg/Cgk',\n  'resolution':'分辨率不取样：直接录入分辨率值，与过程公差比对（分辨率应 ≤ 1/10 公差）'\n};")

# S5 planRecords 扩展全部 6 类台账
rep("function planRecords(s, planId){\n  return (s.grr.concat(s.kappa)).filter(r=>r.planId===planId);\n}",
    "function planRecords(s, planId){\n  return (s.grr||[]).concat(s.kappa||[],s.linear||[],s.stability||[],s.cgcgk||[],s.resolution||[]).filter(r=>r.planId===planId);\n}")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
