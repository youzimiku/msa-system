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

# A1 mMethods 语义：分析方法（会议口径）
rep("  const [mMethods,setMMethods]=useState([]);          // 勾选的 MSA 方法（默认按数据类型：计量型=重复性/再现性，计数型=kappa）",
    "  const [mMethods,setMMethods]=useState([]);          // 勾选的分析方法（会议口径：特性-量具-方法；默认按数据类型 GRR/KAPPA）")

# A2 stdSel onChange 联动分析方法
rep("onChange={v=>{ setStdSel(v||''); setCfg(c=>({...c,_ops:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].ops,_trials:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].trials,_parts:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].parts})); setMMethods(v? ((stdTypeOf(v)==='KAPPA')?['kappa']:['重复性','再现性']) : []); }}/></Col>",
    "onChange={v=>{ setStdSel(v||''); setCfg(c=>({...c,_ops:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].ops,_trials:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].trials,_parts:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].parts})); setMMethods(v? ((stdTypeOf(v)==='KAPPA')?['KAPPA']:['GRR']) : []); }}/></Col>")

# A3 submit 整段重写（去掉 merge，按分析方法逐器具生成）
old_submit = """  const submit=()=>{
    if(!partSel){ toast.warn('请先选择零件/工序（检验标准定义在零件上）'); return; }
    if(!stdSel){ toast.warn('请为该零件选择检验标准（一个计划一个检验标准）'); return; }
    if(!selKeys.length){ toast.warn('请至少选择一个计量器具'); return; }
    const t=stdTypeOf(stdSel);
    const baseParams={ops:cfg._ops||TYPE_PARAMS[t].ops, trials:cfg._trials||TYPE_PARAMS[t].trials, parts:cfg._parts||TYPE_PARAMS[t].parts};
    if(mode==='merge'){
      mut(s=>{
        let skipped=0;
        const okIds=selKeys.filter(id=>{ if(instHasActivePlan(s,id)){ skipped++; return false; } return true; });
        if(!okIds.length){ if(skipped) toast.warn('所选器具均已存在未闭环计划，未创建新计划'); return; }
        const it0=s.instruments.find(i=>i.id===okIds[0]);
        const pid=nextPlanId(s);
        const fullNames=okIds.map(id=>{ const it=s.instruments.find(i=>i.id===id); return (it.range&&it.range!=='-'&&it.range!=='计数型'&&it.range!=='通端/止端')?(it.name+' '+it.range):it.name; });
        s.plans.unshift({ id:pid, name:(nameTpl||'{inst} MSA 分析计划').replace('{inst}','多器具合并计划'), instId:okIds[0], instName:'多器具合并计划（'+okIds.length+'台）', instIds:okIds, cat:it0?it0.cat:'',
          type:'', method:'', standard:stdSel, params:baseParams,
          object:'', feature:'', owner:d.me.name, editor:s.me.name, editorDate:TODAY,
          planDate, trigger, status:'未定型', recordId:'', result:'-', note:'合并创建：同一检验标准 '+stdSel+'，创建后类型为空，待顶部「转 GRR / 转 KAPPA」定型后按器具生成分析记录',
          partNo:meta.partNo, partName:partSel.split(' / ')[0], qcArea:meta.qcArea, plant:meta.plant, subplant:meta.subplant, observer:meta.observer, measurers:meta.measurers,
          dept:meta.dept, dataType:(stdTypeOf(stdSel)==='KAPPA'?'计数型':'计量型'), msaMethods:mMethods.length?mMethods:(stdTypeOf(stdSel)==='KAPPA'?['kappa']:['重复性','再现性']), opMethod:'《测量系统分析操作指导书》' });
        logAction(s.me.name,'计划编制',pid,'多器具合并创建 MSA 计划：'+okIds.length+' 台器具，待定型'+(skipped?'，跳过 '+skipped+' 台':''));
        toast.ok('已创建合并计划 '+pid+'（'+okIds.length+' 台器具，单一检验标准 '+stdSel+'），创建后类型为空，请在列表勾选后「转 GRR / 转 KAPPA」定型'+(skipped?('；跳过 '+skipped+' 台（已有未闭环计划）'):''));
      });
      onClose(); return;
    }
    // 逐个创建（一器一计划，全部使用同一检验标准）
    let created=0, skipped=0;
    mut(s=>{
      selKeys.forEach(id=>{
        if(instHasActivePlan(s, id)){ skipped++; return; }
        const it=s.instruments.find(i=>i.id===id); if(!it) return;
        const fullName=(it.range&&it.range!=='-'&&it.range!=='计数型'&&it.range!=='通端/止端')?(it.name+' '+it.range):it.name;
        const c=cfg[id]||{};
        const params={ops:Number(c.ops)||baseParams.ops, trials:Number(c.trials)||baseParams.trials, parts:Number(c.parts)||baseParams.parts};
        const pid=nextPlanId(s);
        s.plans.unshift({ id:pid, name:(nameTpl||'{inst} MSA 分析计划').replace('{inst}',fullName), instId:id, instName:fullName, instIds:[id], cat:it.cat,
          type:'', method:'', standard:stdSel, params:params,
          object:c.object||'待定义', feature:'', owner:c.owner||s.me.name, editor:s.me.name, editorDate:TODAY,
          planDate, trigger, status:'未定型', recordId:'', result:'-', note:'创建时选定零件 '+partSel.split(' / ')[0]+'、检验标准 '+stdSel+'，创建后类型为空，待定型（转 GRR / 转 KAPPA）',
          partNo:meta.partNo, partName:partSel.split(' / ')[0], qcArea:meta.qcArea, plant:meta.plant, subplant:meta.subplant, observer:meta.observer, measurers:meta.measurers,
          dept:meta.dept, dataType:(stdTypeOf(stdSel)==='KAPPA'?'计数型':'计量型'), msaMethods:mMethods.length?mMethods:(stdTypeOf(stdSel)==='KAPPA'?['kappa']:['重复性','再现性']), opMethod:'《测量系统分析操作指导书》' });
        created++;
      });
      logAction(s.me.name,'计划编制','MSAP-批量','按器具批量创建 '+created+' 个 MSA 计划（待定型，单一标准 '+stdSel+'）'+(skipped?('，跳过 '+skipped+' 台（已有未闭环计划）'):''));
    });
    if(created) toast.ok('已创建 '+created+' 个 MSA 计划（类型为空待定型，单一检验标准 '+stdSel+'），请在列表勾选后「转 GRR / 转 KAPPA」定型'+(skipped?('；跳过 '+skipped+' 台（已有未闭环计划）'):''));
    else toast.warn('所选器具均已存在未闭环计划，未创建新计划');
    onClose();
  };"""

new_submit = """  const methodExcelMap=(an)=> an==='GRR'?['重复性','再现性']: an==='KAPPA'?['kappa']: an==='linear'?['偏倚','线性']: an==='stability'?['稳定性']: an==='cgcgk'?['cg/cgk']: [];
  const submit=()=>{
    if(!partSel){ toast.warn('请先选择零件/工序（检验标准定义在零件上）'); return; }
    if(!stdSel){ toast.warn('请为该零件选择检验标准（一个计划一个检验标准）'); return; }
    if(!selKeys.length){ toast.warn('请至少选择一个计量器具'); return; }
    const t=stdTypeOf(stdSel);
    const baseParams={ops:cfg._ops||TYPE_PARAMS[t].ops, trials:cfg._trials||TYPE_PARAMS[t].trials, parts:cfg._parts||TYPE_PARAMS[t].parts};
    // 会议口径：一器一计划一方法。勾选 N 个分析方法 → 每台器具生成 N 个计划（各对应 1 个方法 + 1 条台账待采集记录）；未勾选 → 生成 1 个「未定型」计划（待转）
    const meths = mMethods.length? mMethods : [null];
    let created=0, skipped=0;
    mut(s=>{
      selKeys.forEach(id=>{
        if(instHasActivePlan(s, id)){ skipped++; return; }
        const it=s.instruments.find(i=>i.id===id); if(!it) return;
        const fullName=(it.range&&it.range!=='-'&&it.range!=='计数型'&&it.range!=='通端/止端')?(it.name+' '+it.range):it.name;
        const c=cfg[id]||{};
        meths.forEach(an=>{
          const pid=nextPlanId(s);
          const tp=an||'';
          const method=an? ENUM.taskMethod[an][0] : '';
          const tparams=TYPE_PARAMS[an||'GRR']||{};
          // GRR/KAPPA/未定型：人数/次数/样本数取行输入；linear/stability/cgcgk/resolution 用固化取样参数
          const pParams=(an==='GRR'||an==='KAPPA'||!an)
            ? {ops:Number(c.ops)||tparams.ops||baseParams.ops, trials:Number(c.trials)||tparams.trials||baseParams.trials, parts:Number(c.parts)||tparams.parts||baseParams.parts}
            : {ops:tparams.ops||1, trials:tparams.trials||1, parts:tparams.parts||1, stds:tparams.stds, per:tparams.per, points:tparams.points, groups:tparams.groups, runs:tparams.runs, span:tparams.span};
          const dataType = (an==='KAPPA'||stdTypeOf(stdSel)==='KAPPA')?'计数型':'计量型';
          s.plans.unshift({ id:pid, name:(nameTpl||'{inst} MSA 分析计划').replace('{inst}', an? fullName+'·'+ANAL_SHORT[an] : fullName), instId:id, instName:fullName, instIds:[id], cat:it.cat,
            type:tp, method, standard:stdSel, params:pParams,
            object:c.object||'待定义', feature:'', owner:c.owner||s.me.name, editor:s.me.name, editorDate:TODAY,
            planDate, trigger, status: an? '待采集':'未定型', recordId:'', result:'-',
            note: an? ('创建时勾选分析方法 '+ANAL_SHORT[an]+'（'+SAMPLING[an]+'），已生成台账待采集记录') : ('创建时选定零件 '+partSel.split(' / ')[0]+'、检验标准 '+stdSel+'，未勾选分析方法，可在列表勾选后转 GRR / 转 KAPPA 定型'),
            partNo:meta.partNo, partName:partSel.split(' / ')[0], qcArea:meta.qcArea, plant:meta.plant, subplant:meta.subplant, observer:meta.observer, measurers:meta.measurers,
            dept:meta.dept, dataType, msaMethods:an? methodExcelMap(an) : [], opMethod:'《测量系统分析操作指导书》' });
          if(an){ const rid=spawnRecord(s, pid, {type:an, instId:id, instName:fullName, object:c.object||'待定义', standard:stdSel, method, params:pParams, note:'创建时按分析方法 '+ANAL_SHORT[an]+' 生成'}); syncPlanFromRecord(s,pid); }
          created++;
        });
      });
      logAction(s.me.name,'计划编制','MSAP-批量','按器具批量创建 '+created+' 个 MSA 计划（勾选分析方法：'+(mMethods.length?mMethods.map(x=>ANAL_SHORT[x]).join('、'):'未定型')+'，单一标准 '+stdSel+'）'+(skipped?('，跳过 '+skipped+' 台（已有未闭环计划）'):''));
    });
    if(created) toast.ok('已创建 '+created+' 个 MSA 计划'+(mMethods.length?('（'+mMethods.map(x=>ANAL_SHORT[x]).join('/')+'，已生成台账待采集记录）'):'（未定型，待转）')+',单一检验标准 '+stdSel+(skipped?('；跳过 '+skipped+' 台（已有未闭环计划）'):''));
    else toast.warn('所选器具均已存在未闭环计划，未创建新计划');
    onClose();
  };"""

rep(old_submit, new_submit)

# A4 创建方式 Radio → 静态 Tag（会议：仅逐个创建，一器一计划）
rep("      <Col span={8}><span className=\"flt-label\">创建方式</span><Radio.Group size=\"small\" value={mode} onChange={e=>setMode(e.target.value)} options={[{value:'single',label:'逐个创建（一器一计划）'},{value:'merge',label:'合并创建（多器一计划）'}]} optionType=\"button\" buttonStyle=\"solid\"/></Col>",
    "      <Col span={8}><span className=\"flt-label\">创建方式</span><Tag color=\"blue\">逐个创建（一器一计划，1 计划 = 1 器具 × 1 特性 × 1 方法）</Tag></Col>")

# A5 Alert 文案（去掉合并创建）
rep("message=\"创建流程：先选零件 → 选该零件的一个检验标准（一个 MSA 计划只针对一个质量特性 / 一个检验标准）→ 选择器具组（左侧）→ 在右侧组内器具中勾选本次测量器具（默认选中该组「默认器具」）。支持逐个创建（一器一计划）/ 合并创建（多器一计划，每台器具一条独立分析记录）。\"",
    "message=\"创建流程：先选零件 → 选该零件的一个检验标准（一个 MSA 计划只针对一个质量特性 / 一个检验标准）→ 勾选分析方法（会议口径：特性-量具-方法，一器一计划一方法；GRR 与 KAPPA 不会同时勾选）→ 选择器具组（左侧）→ 在右侧组内器具中勾选本次测量器具（默认选中该组「默认器具」）。勾选 N 个方法即按器具生成 N 个计划，并自动生成对应台账待采集记录。\"")

# A6 测量人员 + 分析方法勾选行（替换原 MSA 方法行）
rep("""    <Row gutter={12} style={{marginBottom:8}}>
      <Col span={9}><span className="flt-label">测量人员</span><Input size="small" placeholder="参与测量人员（如：操作员A·王强）" value={meta.measurers} onChange={e=>setMetaK('measurers',e.target.value)}/></Col>
      <Col span={15}><span className="flt-label">MSA 方法（勾选本次要开展的分析，对应《测量系统分析计划》表）</span><Checkbox.Group size="small" value={mMethods} options={ENUM.msaMethods.map(m=>({value:m,label:m}))} onChange={setMMethods}/></Col>
    </Row>
    <div className="tiny" style={{marginBottom:12}}>说明：部门 / 零件号 / 质检区划 / 工厂 / 分厂 / 观察员 / 测量人员 为公共字段，将写入本次创建的所有 MSA 计划；MSA 方法勾选按检验标准的数据类型默认给出（计量型=重复性/再现性，计数型=kappa），可增删；台账内录入时可再按记录细化测量人员/观察员。</div>""",
    """    <Row gutter={12} style={{marginBottom:8}}>
      <Col span={6}><span className="flt-label">测量人员</span><Input size="small" placeholder="参与测量人员（如：操作员A·王强）" value={meta.measurers} onChange={e=>setMetaK('measurers',e.target.value)}/></Col>
      <Col span={18}><span className="flt-label">分析方法（勾选本次要生成的分析计划；一器一计划一方法，GRR 与 KAPPA 不会同时勾选）</span><Checkbox.Group size="small" value={mMethods} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'resolution',label:'分辨率'}]} onChange={setMMethods}/></Col>
    </Row>
    <div className="tiny" style={{marginBottom:12}}>取样策略（按分析方法固化，勾选后生成对应取样计划）：{mMethods.length? mMethods.map(m=>ANAL_SHORT[m]+'：'+SAMPLING[m]).join('；') : '未勾选时仅生成「未定型」计划，可在列表勾选后转 GRR / 转 KAPPA 定型。'}</div>
    <div className="tiny" style={{marginBottom:12}}>说明：部门 / 零件号 / 质检区划 / 工厂 / 分厂 / 观察员 / 测量人员 为公共字段，将写入本次创建的所有 MSA 计划；台账内录入时可再按记录细化测量人员/观察员。</div>""")

# A7 提示列（按勾选方法提示生成数量）
rep("    {title:'提示', width:150, render:(_,i)=> i.active? <Tag color=\"volcano\">已有未闭环计划</Tag> : i.overdue? <Tag color=\"red\">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span className=\"tiny\">{stdSel? '将生成 '+stdTypeOf(stdSel)+' 记录':(mode==='merge'?'合并创建(须选标准)':'可创建')}</span> : <span className=\"tiny\">停用/报废不可选</span>}",
    "    {title:'提示', width:200, render:(_,i)=> i.active? <Tag color=\"volcano\">已有未闭环计划</Tag> : i.overdue? <Tag color=\"red\">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span className=\"tiny\">{stdSel? (mMethods.length? '将生成 '+mMethods.length+' 个计划（'+mMethods.map(x=>ANAL_SHORT[x]).join('、')+'）':'将生成未定型计划（待转）'):'请先选零件与标准'}</span> : <span className=\"tiny\">停用/报废不可选</span>}")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
