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

# B1 模块级 msaExcelMap（供 ConvertModal/编辑使用）
rep("const ANAL_COLOR = { 'GRR':'blue','KAPPA':'green','linear':'cyan','stability':'purple','cgcgk':'gold','resolution':'geekblue' };",
    "const ANAL_COLOR = { 'GRR':'blue','KAPPA':'green','linear':'cyan','stability':'purple','cgcgk':'gold','resolution':'geekblue' };\nconst msaExcelMap=(an)=> an==='GRR'?['重复性','再现性']: an==='KAPPA'?['kappa']: an==='linear'?['偏倚','线性']: an==='stability'?['稳定性']: an==='cgcgk'?['cg/cgk']: [];")

# B2 计划列表：分析关联类型 → 分析方法
rep("    {title:'分析关联类型', width:100, render:(_,r)=>{ const recs=planRecords(d,r.id); if((r.instIds||[]).length>1){ const ts=[...new Set(recs.map(x=>x.id.indexOf('GRR')===0?'GRR':'KAPPA'))]; return ts.length===1?<Tag color={ts[0]==='GRR'?'blue':'green'}>{ts[0]}</Tag>:<Tag color=\"purple\">GRR/KAPPA</Tag>; } return r.type? <Tag color={r.type==='GRR'?'blue':'green'}>{r.type}</Tag> : <Tag>未定型</Tag>; }},",
    "    {title:'分析方法', width:120, render:(_,r)=>{ const recs=planRecords(d,r.id); if((r.instIds||[]).length>1){ const ts=[...new Set(recs.map(x=>recKindId(x)))]; return ts.length? <Space size={2} wrap>{ts.map(t=>anTag(t))}</Space> : <Tag>未定型</Tag>; } return anTag(r.type); }},")

# B3 ConvertModal 支持 6 类分析类型
rep("  const typeStds=(t)=> (d.standards||[]).filter(s=>s.status==='启用'&&stdTypeOf(s.id)===t && (!plan.partName||plan.partName==='—'||s.partName===plan.partName));",
    "  const typeStds=(t)=> (d.standards||[]).filter(s=>s.status==='启用' && (stdTypeOf(s.id)===t || ['linear','stability','cgcgk','resolution'].indexOf(t)>=0) && (!plan.partName||plan.partName==='—'||s.partName===plan.partName));")
rep("  const changeType=(t)=>{\n    setType(t);\n    const s1=typeStds(t);\n    form.setFieldsValue({ type:t, method:ENUM.taskMethod[t][0], standard:s1[0]?s1[0].id:undefined,\n      ops:TYPE_PARAMS[t].ops, trials:TYPE_PARAMS[t].trials, parts:TYPE_PARAMS[t].parts });\n  };",
    "  const changeType=(t)=>{\n    setType(t);\n    const s1=typeStds(t);\n    const tp=TYPE_PARAMS[t]||{};\n    form.setFieldsValue({ type:t, method:(ENUM.taskMethod[t]||[''])[0], standard:s1[0]?s1[0].id:undefined,\n      ops:tp.ops||3, trials:tp.trials||3, parts:tp.parts||10 });\n  };")
rep("      Object.assign(p,{ type:v.type, method:v.method, standard:v.standard, dataType:(v.type==='KAPPA'?'计数型':'计量型'),\n        msaMethods:[...new Set([...(p.msaMethods||[]), (v.type==='KAPPA'?'kappa':'重复性'), (v.type==='KAPPA'?null:'再现性')].filter(Boolean))],\n        params:{ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},\n        object:v.object||p.object, owner:v.owner||p.owner, planDate:v.planDate||p.planDate, trigger:v.trigger||p.trigger, status:'待采集' });",
    "      const isGrrK=(v.type==='GRR'||v.type==='KAPPA');\n      Object.assign(p,{ type:v.type, method:v.method, standard:v.standard, dataType:(v.type==='KAPPA'?'计数型':'计量型'),\n        msaMethods:[...new Set([...(p.msaMethods||[]), ...msaExcelMap(v.type)].filter(Boolean))],\n        params: isGrrK? {ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10} : {...(TYPE_PARAMS[v.type]||{}), ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},\n        object:v.object||p.object, owner:v.owner||p.owner, planDate:v.planDate||p.planDate, trigger:v.trigger||p.trigger, status:'待采集' });")
rep("      const rid=spawnRecord(s, p.id, { type:v.type, standard:v.standard, method:v.method,\n        params:{ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},\n        object:p.object, instId:p.instId, instName:p.instName, owner:v.owner||p.owner, note:'计划定型为 '+v.type+'，待台账内录入数据' });",
    "      const rid=spawnRecord(s, p.id, { type:v.type, standard:v.standard, method:v.method,\n        params: isGrrK? {ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10} : {...(TYPE_PARAMS[v.type]||{}), ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},\n        object:p.object, instId:p.instId, instName:p.instName, owner:v.owner||p.owner, note:'计划定型为 '+v.type+'，待台账内录入数据' });")
rep("    toast.ok('已定型为 '+v.type+'（'+v.standard+'），请在 '+(v.type==='GRR'?'GRR':'KAPPA')+' 台账内录入数据'); onClose();",
    "    toast.ok('已定型为 '+(ANAL_SHORT[v.type]||v.type)+'（'+v.standard+'），请在对应台账内录入数据'); onClose();")
rep("      <Alert style={{marginBottom:12}} type=\"info\" showIcon message=\"定型后将在对应台账中建立「待采集」记录，样本数据需在 GRR / KAPPA 台账内录入并提交审核；计划状态与台账记录自动联动。一个 MSA 计划只能选择一个检验标准（一个质量特性）。\" />",
    "      <Alert style={{marginBottom:12}} type=\"info\" showIcon message=\"定型后将在对应分析台账中建立「待采集」记录，样本数据在台账内录入并提交审核；计划状态与台账记录自动联动。一个 MSA 计划只能选择一个检验标准（一个质量特性）、一个分析方法（会议口径：特性-量具-方法）。\" />")
rep("        <Col span={8}><Form.Item name=\"type\" label=\"分析类型\" rules={[{required:true}]}><Select options={ENUM.taskType.map(c=>({value:c,label:c}))} onChange={changeType}/></Form.Item></Col>",
    "        <Col span={8}><Form.Item name=\"type\" label=\"分析方法\" rules={[{required:true}]}><Select options={ENUM.analysisTypes.map(c=>({value:c,label:ANAL_SHORT[c]}))} onChange={changeType}/></Form.Item></Col>")
rep("      <div className=\"form-hint\">GRR 建议：操作员 3 × 试验 3 × 样本 ≥10（覆盖过程变差）；KAPPA 建议：检验员 3 × 样本 ≥30（含合格/不合格及临界样本）。检验标准定义在「零件/工序」上，此处仅列该零件且类型匹配的启用标准。</div>",
    "      <div className=\"form-hint\">取样策略（会议固化）：{SAMPLING[type]||''}；GRR/KAPPA 建议操作员 3×试验 3×样本 ≥10（KAPPA 样本 ≥30）；线性/偏移 5 标准件×10 次；稳定性 25 子组；Cg/Cgk 50 次；分辨率不取样。检验标准定义在「零件/工序」上。</div>")

# B4 PlanDetail 分析关联类型 → 分析方法
rep("      {key:'分析关联类型', label:'分析关联类型', children: multi? (recs.length?<Tag color=\"purple\">{[...new Set(recs.map(x=>x.id.indexOf('GRR')===0?'GRR':'KAPPA'))].join(' / ')}</Tag>:<Tag>未定型</Tag>) : (plan.type? <Tag color={plan.type==='GRR'?'blue':'green'}>{plan.type}</Tag>:<Tag>未定型</Tag>)},",
    "      {key:'分析方法', label:'分析方法', children: multi? (recs.length?<Space size={2} wrap>{[...new Set(recs.map(x=>recKindId(x)))].map(t=>anTag(t))}</Space>:<Tag>未定型</Tag>) : anTag(plan.type)},")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
