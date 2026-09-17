# -*- coding: utf-8 -*-
"""v2.6 计划层级改造：总计划 → 分计划（取样计划）
① 创建弹窗：勾选分析方法后显示「将生成 N 个分计划（取样计划）」预览条
② 计划列表：分析单号列→分计划标签列 + 行展开显示分计划表
③ 计划详情：新增「分计划列表」面板
④ 计划分析任务抽屉：正名为「计划分计划」，复用公共分计划表格
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:110])
    s = s.replace(old, new, cnt)

# ---------- ① 创建弹窗：分析方法勾选后显示分计划预览条 ----------
rep("""        <Col span={24}><span className="flt-label">分析方法</span><Checkbox.Group size="small" value={mMethods} options={[{value:'GRR',label:'GRR（重复性+再现性）'},{value:'KAPPA',label:'KAPPA（计数型一致性）'},{value:'linear',label:'线性/偏移（线性+偏倚）'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk（能力）'},{value:'resolution',label:'分辨率（分辨力）'}]} onChange={setMMethods}/></Col>""",
    """        <Col span={24}><span className="flt-label">分析方法</span><Checkbox.Group size="small" value={mMethods} options={[{value:'GRR',label:'GRR（重复性+再现性）'},{value:'KAPPA',label:'KAPPA（计数型一致性）'},{value:'linear',label:'线性/偏移（线性+偏倚）'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk（能力）'},{value:'resolution',label:'分辨率（分辨力）'}]} onChange={setMMethods}/></Col>
        {mMethods.length>0 && <Col span={24}><Alert type="info" showIcon message={'将生成 '+mMethods.length+' 个分计划（取样计划）：'+mMethods.map(an=>ANAL_SHORT[an]+'（'+subRuleBrief(an)+'）').join(' / ')} style={{marginTop:8}}/></Col>}""",
    1, 'create-preview')

# 在 BatchPlanModal 内（effDef 定义后）插入 subRuleBrief
rep("""  const effMeth = mMethods.length===1? mMethods[0] : (stdTypeOf(stdSel)||'GRR');
  const effDef = samplingDef(effMeth);""",
    """  const effMeth = mMethods.length===1? mMethods[0] : (stdTypeOf(stdSel)||'GRR');
  const effDef = samplingDef(effMeth);
  const subRuleBrief=(an)=>{ const sd=samplingDef(an); if(an==='GRR'||an==='KAPPA') return sd.parts+'件×'+sd.ops+'人×'+sd.trials+'次'; if(an==='linear') return sd.parts+'标准件×'+sd.trials+'次'; if(an==='stability') return sd.parts+'子组×'+sd.trials+'次'; if(an==='cgcgk') return sd.trials+'次'; return '不取样'; };""",
    1, 'subrule-brief')

# ---------- ② 公共分计划表格 + PlanTaskDrawer 正名 ----------
OLD_DRAWER = """/* 计划分析任务抽屉：一计划多任务（一个计划可挂多个分析方法的台账记录） */
const ENTRY_MAP={GRR:'entry_grr', KAPPA:'entry_kappa', linear:'entry_linear', stability:'entry_stability', cgcgk:'entry_cgcgk', resolution:'entry_resolution'};
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
      <Button size="small" type="link" onClick={()=>NavAPI.go(ENTRY_MAP[recKindId(r)]||'entry_grr')}>台账</Button>
    </Space>}
  ];
  return <Drawer title={'计划分析任务：'+plan.id+(plan.instName?' '+plan.instName:'')} open width={980} onClose={onClose}>
    <div style={{marginBottom:12}}>
      <Space wrap>
        <Tag color="blue">{plan.id}</Tag>
        {recs.length? <span className="tiny">共 {recs.length} 个分析任务</span> : <span className="tiny">该计划尚未定型</span>}
      </Space>
    </div>
    <Table rowKey="id" size="middle" dataSource={recs} columns={cols} scroll={{x:900}} pagination={false}/>
  </Drawer>;
}"""
NEW_DRAWER = """/* 分计划（取样计划）公共表格：一个 MSA 总计划下按分析方法生成的分计划列表 */
const ENTRY_MAP={GRR:'entry_grr', KAPPA:'entry_kappa', linear:'entry_linear', stability:'entry_stability', cgcgk:'entry_cgcgk', resolution:'entry_resolution'};
const subRuleText=(r)=>{ const k=recKindId(r); const P=r.params||{};
  if(k==='GRR'||k==='KAPPA') return (r.numParts||r.numSamples||P.parts||'-')+' 件 × '+(r.numOps||r.numApp||P.ops||'-')+' 人 × '+(r.numTrials||P.trials||'-')+' 次';
  if(k==='linear') return (P.stds||r.stds||5)+' 标准件 × '+(P.per||r.per||12)+' 次';
  if(k==='stability') return (P.groups||r.groups||25)+' 子组 × '+(P.per||r.per||5)+' 次';
  if(k==='cgcgk') return (P.runs||r.runs||50)+' 次连续测量';
  return '不取样，直接录入'; };
function subPlanCols(){
  return [
    {title:'分计划号', dataIndex:'id', width:150, render:v=><span className="mono">{v}</span>},
    {title:'分析方法', width:110, render:(_,r)=><Tag color={ANAL_COLOR[recKindId(r)]||'default'}>{ANAL_SHORT[recKindId(r)]||recKindId(r)}</Tag>},
    {title:'取样规则', width:230, render:(_,r)=><span className="tiny">{subRuleText(r)}</span>},
    {title:'状态', width:100, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'结论', width:130, render:(_,r)=><VerdictTag v={r.conclusion}/>},
    {title:'操作', width:180, fixed:'right', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>recJump(r)}>{r.reviewStatus==='待采集'?'录入数据':'查看结果'}</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.go(ENTRY_MAP[recKindId(r)]||'entry_grr')}>台账</Button>
    </Space>}
  ];
}
/* 计划分计划抽屉：一个 MSA 总计划下挂多个分析方法的分计划（取样计划 → 录入 → 分析） */
function PlanTaskDrawer({plan, onClose}){
  const d=Store.get();
  const recs=planRecords(d, plan.id);
  return <Drawer title={'计划分计划：'+plan.id+(plan.instName?' '+plan.instName:'')} open width={980} onClose={onClose}>
    <div style={{marginBottom:12}}>
      <Space wrap>
        <Tag color="blue">{plan.id}</Tag>
        {recs.length? <span className="tiny">共 {recs.length} 个分计划（取样计划）</span> : <span className="tiny">该计划尚未定型，无分计划</span>}
      </Space>
    </div>
    <Table rowKey="id" size="middle" dataSource={recs} columns={subPlanCols()} scroll={{x:960}} pagination={false}/>
  </Drawer>;
}"""
rep(OLD_DRAWER, NEW_DRAWER, 1, 'drawer')

# ---------- ③ 计划列表：分析单号列 → 分计划标签列 + 行展开 ----------
rep("""    {title:'分析单号', width:120, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <Space size={2} wrap>{recs.map(x=><span key={x.id} className="mono tiny">{x.id}</span>)}</Space> : <span className="tiny">暂无</span>; }},""",
    """    {title:'分计划', width:130, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <Space size={2} wrap>{recs.map(x=><Tag key={x.id} color={ANAL_COLOR[recKindId(x)]||'default'}>{ANAL_SHORT[recKindId(x)]||recKindId(x)}</Tag>)}</Space> : <span className="tiny">未定型</span>; }},""",
    1, 'plan-col')
rep("""      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:4400}} pagination={false}
        rowSelection={{ selectedRowKeys, onChange:setSelectedRowKeys }}/>""",
    """      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:4400}} pagination={false}
        rowSelection={{ selectedRowKeys, onChange:setSelectedRowKeys }}
        expandable={{ expandedRowRender:(r)=>{ const recs=planRecords(d,r.id); return recs.length? <Table rowKey="id" size="small" dataSource={recs} columns={subPlanCols()} pagination={false} scroll={{x:960}}/> : <span className="tiny">该计划尚未定型，无分计划</span>; } }}/>""",
    1, 'plan-expand')

# ---------- ④ 计划详情：新增「分计划列表」面板 ----------
rep("""    {recs.filter(r=>r.reviewStatus==='待采集').length>0 && <Alert className="mt12" type="warning" showIcon message="存在待采集记录，请在对应台账中点击「录入数据」完成样本数据采集并提交审核。" />}""",
    """    <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>分计划列表（取样计划 → 录入 → 分析 → 结论归集）</span>{recs.length? <span className="tiny">共 {recs.length} 个分计划，任一不合格则总计划不合格</span> : <span className="tiny">未定型，无分计划</span>}</div>
      <Table rowKey="id" size="small" dataSource={recs} columns={subPlanCols()} pagination={false} scroll={{x:960}}/>
    </div>
    {recs.filter(r=>r.reviewStatus==='待采集').length>0 && <Alert className="mt12" type="warning" showIcon message="存在待采集分计划，请点击「录入数据」完成样本采集并提交审核。" />}""",
    1, 'detail-panel')

open(P, 'w', encoding='utf-8').write(s)
print('hierarchy OK 长度', len(s))
