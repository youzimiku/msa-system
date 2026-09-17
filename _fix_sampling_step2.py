# -*- coding: utf-8 -*-
"""创建 MSA 计划弹窗：人数/次数/样本数按分析方法可调（业务速查默认值 + 可调范围）"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# 1) 组件内插入 SMP_DEF（方法→人数/次数/样本数默认与可调范围）
rep("""  const methodExcelMap=(an)=> an==='GRR'?['重复性','再现性']: an==='KAPPA'?['kappa']: an==='linear'?['偏倚','线性']: an==='stability'?['稳定性']: an==='cgcgk'?['cg/cgk']: [];
  const submit=()=>{""",
"""  const methodExcelMap=(an)=> an==='GRR'?['重复性','再现性']: an==='KAPPA'?['kappa']: an==='linear'?['偏倚','线性']: an==='stability'?['稳定性']: an==='cgcgk'?['cg/cgk']: [];
  /* 业务《取样数量规则速查》默认值 + 可调范围：单方法勾选时 人数/次数/样本数 直接映射到该方法（GRR/KAPPA=操作员×试验×样本；线性=标准件数×每件次数；稳定性=子组数×每期次数；Cg/Cgk=连续测量次数） */
  const SMP_DEF = {
    GRR:{ops:3,opsMin:1,opsMax:5,useOps:true, trials:3,trialsMin:2,trialsMax:5, parts:10,partsMin:1,partsMax:30},
    KAPPA:{ops:3,opsMin:2,opsMax:5,useOps:true, trials:3,trialsMin:1,trialsMax:5, parts:50,partsMin:20,partsMax:50},
    linear:{useOps:false, trials:12,trialsMin:10,trialsMax:20, parts:5,partsMin:1,partsMax:10},
    stability:{useOps:false, trials:5,trialsMin:3,trialsMax:10, parts:25,partsMin:25,partsMax:100},
    cgcgk:{useOps:false, trials:50,trialsMin:50,trialsMax:200, parts:1,partsMin:1,partsMax:1},
    resolution:{useOps:false, trials:0, trialsMin:0, trialsMax:0, parts:0, partsMin:0, partsMax:0}
  };
  const effMeth = mMethods.length===1? mMethods[0] : (stdTypeOf(stdSel)||'GRR');
  const effDef = SMP_DEF[effMeth]||SMP_DEF.GRR;
  const submit=()=>{""")

# 2) 提交 pParams：单方法时行输入映射全部方法；多方法时 GRR/KAPPA 用行输入、五性/Cg/Cgk 取方法默认
rep("""          const tparams=TYPE_PARAMS[an||'GRR']||{};
          // GRR/KAPPA/未定型：人数/次数/样本数取行输入；linear/stability/cgcgk/resolution 用固化取样参数
          const pParams=(an==='GRR'||an==='KAPPA'||!an)
            ? {ops:Number(c.ops)||tparams.ops||baseParams.ops, trials:Number(c.trials)||tparams.trials||baseParams.trials, parts:Number(c.parts)||tparams.parts||baseParams.parts}
            : {ops:tparams.ops||1, trials:tparams.trials||1, parts:tparams.parts||1, stds:tparams.stds, per:tparams.per, points:tparams.points, groups:tparams.groups, runs:tparams.runs, span:tparams.span};""",
"""          const tparams=TYPE_PARAMS[an||'GRR']||{};
          const singleM=mMethods.length===1; // 单一方法勾选 → 行参数映射到该方法；多方法时五性/Cg/Cgk 取方法默认
          const D0=SMP_DEF[(an==='GRR'||an==='KAPPA'||!an)?(an||effMeth):(singleM?an:'GRR')]||SMP_DEF.GRR;
          const rowOps=Number(c.ops)||D0.ops, rowTrials=Number(c.trials)||D0.trials, rowParts=Number(c.parts)||D0.parts;
          const pParams=(an==='GRR'||an==='KAPPA'||!an)
            ? {ops:rowOps, trials:rowTrials, parts:rowParts}
            : (an==='linear')
              ? (singleM? {stds:rowParts||5, per:rowTrials||12, points:rowParts||5, biasRuns:tparams.biasRuns||15} : {stds:tparams.stds||5, per:tparams.per||12, points:tparams.points||5, biasRuns:tparams.biasRuns||15})
              : (an==='stability')
                ? (singleM? {groups:rowParts||25, per:rowTrials||5, span:'4周~3个月'} : {groups:tparams.groups||25, per:tparams.per||5, span:'4周~3个月'})
                : (an==='cgcgk')
                  ? (singleM? {runs:rowTrials||50, parts:1} : {runs:tparams.runs||50, parts:1})
                  : {none:1};""")

# 3) 行参数三列 → 方法感知（人数按方法禁用；次数/样本数按方法范围与默认）
rep("""    {title:'人数', width:64, render:(_,i)=><InputNumber size="small" min={1} max={10} style={{width:'100%'}} placeholder="—" disabled={!i.selectable||!stdSel} value={cfg[i.id]?cfg[i.id].ops:(stdSel?TYPE_PARAMS[stdTypeOf(stdSel)||'GRR'].ops:undefined)} onChange={v=>setRow(i.id,{ops:v})}/>},
    {title:'次数', width:56, render:(_,i)=><InputNumber size="small" min={1} max={10} style={{width:'100%'}} placeholder="—" disabled={!i.selectable||!stdSel} value={cfg[i.id]?cfg[i.id].trials:(stdSel?TYPE_PARAMS[stdTypeOf(stdSel)||'GRR'].trials:undefined)} onChange={v=>setRow(i.id,{trials:v})}/>},
    {title:'样本数', width:64, render:(_,i)=><InputNumber size="small" min={1} max={60} style={{width:'100%'}} placeholder="—" disabled={!i.selectable||!stdSel} value={cfg[i.id]?cfg[i.id].parts:(stdSel?TYPE_PARAMS[stdTypeOf(stdSel)||'GRR'].parts:undefined)} onChange={v=>setRow(i.id,{parts:v})}/>},""",
"""    {title:'人数', width:64, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return !D.useOps? <span className="tiny" style={{color:'#bbb'}}>—</span> : <InputNumber size="small" min={D.opsMin} max={D.opsMax} style={{width:'100%'}} placeholder={String(D.ops)} disabled={!i.selectable||!stdSel} value={cfg[i.id]&&cfg[i.id].ops!==undefined?cfg[i.id].ops:D.ops} onChange={v=>setRow(i.id,{ops:v})}/>; }},
    {title:'次数', width:56, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return D.trialsMax===0? <span className="tiny" style={{color:'#bbb'}}>—</span> : <InputNumber size="small" min={D.trialsMin} max={D.trialsMax} style={{width:'100%'}} placeholder={String(D.trials)} disabled={!i.selectable||!stdSel} value={cfg[i.id]&&cfg[i.id].trials!==undefined?cfg[i.id].trials:D.trials} onChange={v=>setRow(i.id,{trials:v})}/>; }},
    {title:'样本数', width:64, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return D.partsMax===0? <span className="tiny" style={{color:'#bbb'}}>—</span> : <InputNumber size="small" min={D.partsMin} max={D.partsMax} style={{width:'100%'}} placeholder={String(D.parts)} disabled={!i.selectable||!stdSel} value={cfg[i.id]&&cfg[i.id].parts!==undefined?cfg[i.id].parts:D.parts} onChange={v=>setRow(i.id,{parts:v})}/>; }},""")

# 4) 提示列：映射说明（放在"将生成"提示前）
rep("""    {title:'提示', width:200, render:(_,i)=> i.active? <Tag color="volcano">已有未闭环计划</Tag> : i.overdue? <Tag color="red">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span className="tiny">{stdSel? (mMethods.length? '将生成 '+mMethods.length+' 个计划（'+mMethods.map(x=>ANAL_SHORT[x]).join('、')+'）':'将生成未定型计划（待转）'):'请先选零件与标准'}</span> : <span className="tiny">停用/报废不可选</span>}""",
"""    {title:'提示', width:210, render:(_,i)=> i.active? <Tag color="volcano">已有未闭环计划</Tag> : i.overdue? <Tag color="red">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span className="tiny">{stdSel? (mMethods.length? '将生成 '+mMethods.length+' 个计划（'+mMethods.map(x=>ANAL_SHORT[x]).join('、')+'），按['+ANAL_SHORT[effMeth]+']默认取样，可改上方 人数/次数/样本数' : '将生成未定型计划（待转），取样按['+ANAL_SHORT[effMeth]+']默认'):'请先选零件与标准'}</span> : <span className="tiny">停用/报废不可选</span>}""")

# 5) 底部说明：补充业务默认与可调口径
rep("一个 MSA 计划 = 一个零件 + 一个检验标准（一个质量特性）；本次创建的所有计划共用所选标准，选定标准自动带出 测量人数/测量次数/样本数量 建议值（每台可再细化）；创建后类型为空（未定型），由列表顶部「转 GRR / 转 KAPPA」或计划详情定型，生成对应台账「待采集」记录后再录入样本。",
    "一个 MSA 计划 = 一个零件 + 一个检验标准（一个质量特性）；本次创建的所有计划共用所选标准。取样默认按业务《取样数量规则速查》：GRR 10 件×3 人×3 次、KAPPA 50 件×3 人×3 次、线性 5 标准件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次；每行 人数/次数/样本数 可调，按勾选方法映射（单方法时生效；多方法时五性/Cg/Cgk 取方法默认）。创建后类型为空（未定型），由列表顶部「转 GRR / 转 KAPPA」或计划详情定型，生成对应台账「待采集」记录后再录入样本。")

open(p, 'w', encoding='utf-8').write(s)
print('step2 OK, len:', len(s))
