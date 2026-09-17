# -*- coding: utf-8 -*-
"""multi2: PlanPage 多方法改造"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'count=%d for: %s...' % (c, old[:70])
    s = s.replace(old, new)

# 1) doConvert 整体替换（5 方法追加语义）
old_conv_start = s.find('const doConvert=(t)=>{')
old_conv_end = s.find("else NavAPI.go(t==='GRR'?'entry_grr':'entry_kappa');", old_conv_start)
assert old_conv_start > 0 and old_conv_end > old_conv_start
conv_body_end = s.find('\n  };', old_conv_end) + 4
new_conv = '''  // 转分析方法（GRR / KAPPA / 线性偏移 / 稳定性 / CgCgk）：将勾选计划的分析关联类型改为对应方法，生成台账「待采集」记录，并跳转对应录入数据页；一个计划可追加多个方法（一计划多任务）
  const doConvert=(t)=>{
    if(!selectedRowKeys.length){ toast.warn('请先在列表中勾选要转 '+ANAL_SHORT[t]+' 的 MSA 计划'); return; }
    let done=0, skipped=0, firstRid='';
    mut(s=>{
      selectedRowKeys.forEach(id=>{
        const p=s.plans.find(x=>x.id===id); if(!p) return;
        if(planRecords(s,id).some(r=>recKindId(r)===t)){ skipped++; return; } // 已存在该方法记录的不重复转换
        const std=(d.standards||[]).find(st=>st.status==='启用'&&(stdTypeOf(st.id)===t || ['linear','stability','cgcgk'].indexOf(t)>=0) && (!p.partName||p.partName==='—'||st.partName===p.partName));
        if(!std){ skipped++; return; } // 该零件无匹配类型标准
        const params=TYPE_PARAMS[t]? {...TYPE_PARAMS[t], ops:TYPE_PARAMS[t].ops, trials:TYPE_PARAMS[t].trials, parts:TYPE_PARAMS[t].parts} : {ops:3, trials:3, parts:10};
        const had=p.type||planRecords(s,id).length;
        if(!had) p.type=t;
        p.method=ENUM.taskMethod[t][0]; p.standard=std.id; p.params=params;
        p.dept=p.dept||'质量'; p.dataType=(t==='KAPPA'?'计数型':'计量型'); p.opMethod=p.opMethod||'《测量系统分析操作指导书》';
        p.msaMethods=[...new Set([...(p.msaMethods||[]), ...msaExcelMap(t)].filter(Boolean))];
        p.methods=[...new Set([...(p.methods||[]), t])];
        const instIds = (p.instIds&&p.instIds.length)? p.instIds : [p.instId];
        let rid='';
        instIds.forEach(iid=>{
          const inst=s.instruments.find(i=>i.id===iid);
          rid=spawnRecord(s, p.id, { type:t, standard:std.id, method:ENUM.taskMethod[t][0], params,
            object:p.object, instId:iid, instName:inst?inst.name:'', owner:p.owner||s.me.name, note:'顶部按钮转 '+ANAL_SHORT[t]+'，待台账页录入数据' });
          if(!firstRid) firstRid=rid;
        });
        p.recordId=rid;
        syncPlanFromRecord(s,p.id);
        logAction(s.me.name,'计划定型',p.id,'批量转 '+ANAL_SHORT[t]+' · '+std.id+'，生成台账记录');
        done++;
      });
    });
    if(!done){ toast.warn('所选计划均缺少匹配的 '+ANAL_SHORT[t]+' 检验标准或已存在该方法记录，未执行转换'); setSelectedRowKeys([]); return; }
    if(done) toast.ok('已转 '+ANAL_SHORT[t]+' '+done+' 个计划（生成台账待采集记录），跳转对应「录入数据」页');
    if(skipped) toast.warn(skipped+' 个计划已存在该方法记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    if(firstRid){ if(t==='GRR') NavAPI.openGrr(firstRid); else if(t==='KAPPA') NavAPI.openKappa(firstRid); else NavAPI.openAnl(t, firstRid); }
    else NavAPI.go(t==='GRR'?'entry_grr': t==='KAPPA'?'entry_kappa':'entry_'+t);
  };'''
s = s[:old_conv_start] + new_conv + s[conv_body_end:]

# 2) typeShow 聚合
rep("""    const typeShow = recs.length? [...new Set(recs.map(x=>x.id.indexOf('GRR')===0?'GRR':'KAPPA'))].join('/') : (p.type||'未定型');""",
    """    const typeShow = recs.length? [...new Set(recs.map(x=>recKindId(x)))].join('/') : ((p.methods&&p.methods.length)? p.methods.join('/') : (p.type||'未定型'));""")

# 3) 查询下拉 ftype options
rep("""options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'未定型',label:'未定型'}]} onChange={setFtype}/>""",
    """options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'未定型',label:'未定型'}]} onChange={setFtype}/>""")

# 4) 操作区按钮 5 方法
rep("""        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('GRR')}>转 GRR</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('KAPPA')}>转 KAPPA</Button>
        <span className="tiny">查询 / 重置 在最前；一级：创建 MSA 计划；二级：勾选计划后批量定型并跳转对应台账。</span>""",
    """        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('GRR')}>转 GRR</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('KAPPA')}>转 KAPPA</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('linear')}>转线性偏移</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('stability')}>转稳定性</Button>
        <Button disabled={!canDo(d.me.role,'edit')} onClick={()=>doConvert('cgcgk')}>转 Cg/Cgk</Button>""")

# 5) 面板标题
rep('<Panel title="MSA 计划列表（1 计划 = 1 分析任务）">', '<Panel title="MSA 计划列表">')

# 6) 列表"分析方法"列：单器具也按记录聚合
rep("""    {title:'分析方法', width:120, render:(_,r)=>{ const recs=planRecords(d,r.id); if((r.instIds||[]).length>1){ const ts=[...new Set(recs.map(x=>recKindId(x)))]; return ts.length? <Space size={2} wrap>{ts.map(t=>anTag(t))}</Space> : <Tag>未定型</Tag>; } return anTag(r.type); }},""",
    """    {title:'分析方法', width:150, render:(_,r)=>{ const recs=planRecords(d,r.id); const ts=[...new Set(recs.map(x=>recKindId(x)))]; if(ts.length) return <Space size={2} wrap>{ts.map(t=>anTag(t))}</Space>; if(r.methods&&r.methods.length) return <Space size={2} wrap>{r.methods.map(t=>anTag(t))}</Space>; return <Tag>未定型</Tag>; }},""")

# 7) PlanActions 台账按钮 → onTasks
rep("""function PlanActions({r, onDetail, onEdit}){
  const d=Store.get();
  const recs=planRecords(d, r.id);
  const first=recs[0];
  return <Space size={0}>
    <Button size="small" type="link" onClick={()=>{ if(!first){ toast.warn('该计划尚未定型生成台账记录'); return; } recJump(first); }}>台账</Button>
    <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={onEdit}>编辑</Button>
    <Button size="small" type="link" onClick={onDetail}>详情</Button>
  </Space>;
}""",
"""function PlanActions({r, onDetail, onEdit, onTasks}){
  return <Space size={0}>
    <Button size="small" type="link" onClick={onTasks}>台账</Button>
    <Button size="small" type="link" disabled={!canDo(Store.get().me.role,'edit')} onClick={onEdit}>编辑</Button>
    <Button size="small" type="link" onClick={onDetail}>详情</Button>
  </Space>;
}
/* 计划分析任务抽屉：一计划多任务（一个计划可挂多个分析方法的台账记录） */
function PlanTaskDrawer({plan, onClose}){
  const d=Store.get();
  const recs=planRecords(d, plan.id);
  const cols=[
    {title:'分析方法', width:120, render:(_,r)=><Tag color={ANAL_COLOR[recKindId(r)]||'default'}>{ANAL_SHORT[recKindId(r)]||recKindId(r)}</Tag>},
    {title:'分析单号', dataIndex:'id', width:150, render:v=><span className="mono">{v}</span>},
    {title:'取样参数', width:220, render:(_,r)=>{ const k=recKindId(r); const p=k==='GRR'||k==='KAPPA'? ('人数 '+(r.numOps||r.numApp||'-')+' / 次数 '+(r.numTrials||'-')+' / 样本 '+(r.numParts||r.numSamples||'-')) : (k==='linear'?('标准件 '+(r.stds||5)+' / 每件 '+(r.per||12)+' 次') : k==='stability'?('子组 '+(r.groups||25)+' / 每子组 '+(r.per||5)+' 次') : k==='cgcgk'?('次数 '+(r.runs||50)) : '—'); return <span className="tiny">{p}</span>; }},
    {title:'状态', width:100, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'结论', width:130, render:(_,r)=><VerdictTag v={r.conclusion}/>},
    {title:'操作', width:170, fixed:'right', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>recJump(r)}>{r.reviewStatus==='待采集'?'录入数据':'查看结果'}</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.go('entry_'+recKindId(r))}>台账</Button>
    </Space>}
  ];
  return <Drawer title={'计划分析任务：'+plan.id+(plan.instName?' '+plan.instName:'')} open width={980} onClose={onClose}>
    <div style={{marginBottom:12}}>
      <Space wrap>
        <Tag color="blue">{plan.id}</Tag>
        {recs.length? <span className="tiny">共 {recs.length} 个分析任务（一个计划可支持多个分析方法）</span> : <span className="tiny">该计划尚未定型生成分析任务，可在列表勾选后转分析方法生成</span>}
      </Space>
    </div>
    <Table rowKey="id" size="middle" dataSource={recs} columns={cols} scroll={{x:900}} pagination={false}/>
  </Drawer>;
}""")

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('multi2 全部替换成功')
