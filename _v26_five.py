# -*- coding: utf-8 -*-
"""5项调整：1)台账去器具组列表只留量具台账 2)MSA计划删分析方法列 3)详情抽屉extra移body顶部 4)抽屉label不换行 5)分析单操作列前置"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, tag):
    global s
    assert s.count(old) == 1, '%s 定位失败 %d' % (tag, s.count(old))
    s = s.replace(old, new, 1)

# ========== 1) 计量器具台账：去器具组列表 ==========
# 1a. 删 gModal / curGroup 状态
rep("""  const [gModal,setGModal]=useState(null);     // 器具组维护弹窗
  const [curGroup,setCurGroup]=useState(d.instGroups[0]?d.instGroups[0].id:''); // 当前器具组（明细列表按组过滤，默认第一组）
""", "", "gModal/curGroup状态")

# 1b. 删 gCols 定义
i0 = s.find('  const gCols=[', s.find('function LedgerPage'))
i1 = s.find('\n  ];', i0) + len('\n  ];')
rep(s[i0:i1], '', 'gCols定义')

# 1c. 删 effGroup 行
rep("""  const effGroup = curGroup==='ungrouped'? 'ungrouped' : (d.instGroups.find(g=>g.id===curGroup)? curGroup : (d.instGroups[0]?d.instGroups[0].id:''));
""", "", "effGroup")

# 1d. rows 去掉组过滤与组排序
rep("""    .filter(i=>{ if(effGroup==='ungrouped') return !d.instGroups.some(g=>(g.memberIds||[]).indexOf(i.id)>=0); const g=d.instGroups.find(x=>x.id===effGroup); if(!g) return true; return (g.memberIds||[]).indexOf(i.id)>=0; })
    .sort((a,b)=>{ const g=d.instGroups.find(x=>x.id===effGroup); if(!g) return 0; const aP=((d.instruments.find(x=>x.id===a.id)||{}).prototype==='是')?1:0; const bP=((d.instruments.find(x=>x.id===b.id)||{}).prototype==='是')?1:0; return bP-aP; });""",
""";""", "rows组过滤排序")

# 1e. 删器具组列表 Panel
rep("""    <Panel title={'器具组列表（'+d.instGroups.length+' 组）'}>
      <Space style={{marginBottom:12}} wrap>
        <Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={()=>setGModal({})}>+ 新增器具组</Button>
      </Space>
      <Table rowKey="id" size="middle" dataSource={d.instGroups} columns={gCols} pagination={false} scroll={{x:1050}}
        rowClassName={g=>g.id===effGroup?'ledger-group-active':''}
        onRow={g=>({ onClick:()=>setCurGroup(g.id) })}/>
    </Panel>
""", "", "器具组列表Panel")

# 1f. 明细 Panel：标题改计量器具台账，去当前器具组下拉
rep("""    <Panel title={'器具明细列表（'+rows.length+' 台）'}>
      <Space style={{marginBottom:12}} wrap>
        <span className="tiny">当前器具组：</span>
        <Select size="small" style={{width:140}} value={effGroup} onChange={setCurGroup} options={[
          ...(d.instGroups.map(g=>({value:g.id,label:g.id+' '+g.name}))),
          {value:'',label:'（无器具组）'},
          {value:'ungrouped',label:'未分组（不属于任何组）'}
        ]}/>
        <Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={openAdd}>+ 新增器具</Button>""",
"""    <Panel title={'计量器具台账（'+rows.length+' 台）'}>
      <Space style={{marginBottom:12}} wrap>
        <Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={openAdd}>+ 新增器具</Button>""", "明细Panel头")

# 1g. 删 gModal 渲染行
rep("""    {gModal && <InstGroupModal value={gModal} onClose={()=>setGModal(null)}/>}
""", "", "gModal渲染")

# 1h. 删 InstGroupModal 定义
i0 = s.find('function InstGroupModal({value, onClose}){')
i1 = s.find('\nfunction ', i0 + 10)
rep(s[i0:i1], '', 'InstGroupModal定义')

# ========== 2) MSA计划删分析方法列 ==========
m = re.search(r"^    \{title:'分析方法', width:150, render:\(_,r\)=>.*\},\n", s, re.M)
assert m, '分析方法列定位失败'
rep(m.group(0), '', '分析方法列')

# ========== 3) PlanDetail：extra 移到 body 顶部 ==========
# 3a. actBtns 定义
rep("""  const [edit,setEdit]=useState(false);
  return <Drawer title={<Space>{plan.id} {plan.instName}<StatusTag s={plan.status}/>{multi? <Tag color="purple">多器具合并</Tag> : (plan.type?<Tag color={plan.type==='GRR'?'blue':'green'}>{plan.type}</Tag>:<Tag>未定型</Tag>)}</Space>} width={900} open onClose={onClose}
    extra={<Space wrap>
      <Button size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={()=>setEdit(true)}>编辑信息</Button>
      {plan.status==='未定型' && <Button size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={onConvert}>转分析方法</Button>}
      {recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={()=>recJump(x)}>录入数据 {x.id}</Button>)}
      {recs.map(x=><Button key={'t'+x.id} size="small" type="link" onClick={()=>recJump(x)}>台账 {x.id}</Button>)}
      {plan.status!=='已关闭' && canDo(me.role,'approve') && <Button size="small" type="link" danger onClick={()=>act((p,s)=>{ p.status='已关闭'; [s.grr,s.kappa,s.linear,s.stability,s.cgcgk,s.resolution].forEach(arr=>arr.forEach(r=>{ if(r.planId===p.id) r.reviewStatus='已关闭'; })); },'关闭计划')}>关闭</Button>}
    </Space>}>""",
"""  const [edit,setEdit]=useState(false);
  const actBtns=<Space wrap>
    <Button size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={()=>setEdit(true)}>编辑信息</Button>
    {plan.status==='未定型' && <Button size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={onConvert}>转分析方法</Button>}
    {recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={()=>recJump(x)}>录入数据 {x.id}</Button>)}
    {recs.map(x=><Button key={'t'+x.id} size="small" type="link" onClick={()=>recJump(x)}>台账 {x.id}</Button>)}
    {plan.status!=='已关闭' && canDo(me.role,'approve') && <Button size="small" type="link" danger onClick={()=>act((p,s)=>{ p.status='已关闭'; [s.grr,s.kappa,s.linear,s.stability,s.cgcgk,s.resolution].forEach(arr=>arr.forEach(r=>{ if(r.planId===p.id) r.reviewStatus='已关闭'; })); },'关闭计划')}>关闭</Button>}
  </Space>;
  return <Drawer title={<Space>{plan.id} {plan.instName}<StatusTag s={plan.status}/>{multi? <Tag color="purple">多器具合并</Tag> : (plan.type?<Tag color={plan.type==='GRR'?'blue':'green'}>{plan.type}</Tag>:<Tag>未定型</Tag>)}</Space>} width={900} open onClose={onClose}>
    <div style={{marginBottom:12}}>{actBtns}</div>""", "PlanDetail extra")

# ========== 4) 抽屉内 Descriptions 字段名不换行（全局 CSS） ==========
OLD_CSS = """.ant-btn-text{background:transparent;border:none;color:#1677ff;border-radius:4px}"""
NEW_CSS = """.ant-btn-text{background:transparent;border:none;color:#1677ff;border-radius:4px}
.ant-drawer .ant-descriptions-item-label{white-space:nowrap;word-break:keep-all}"""
rep(OLD_CSS, NEW_CSS, '抽屉label不换行CSS')

# ========== 5) 当前计划分析单：操作列移到最前 ==========
OLD_SUB = """  return [
    {title:'分计划号', dataIndex:'id', width:150, render:v=><span className="mono">{v}</span>},
    {title:'分析方法', width:110, render:(_,r)=><Tag color={ANAL_COLOR[recKindId(r)]||'default'}>{ANAL_SHORT[recKindId(r)]||recKindId(r)}</Tag>},
    {title:'取样规则', width:230, render:(_,r)=><span className="tiny">{subRuleText(r)}</span>},
    {title:'状态', width:100, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'结论', width:130, render:(_,r)=><VerdictTag v={r.conclusion}/>},
    {title:'操作', width:180, fixed:'right', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>recJump(r)}>{r.reviewStatus==='待采集'?'录入数据':'查看结果'}</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.go(ENTRY_MAP[recKindId(r)]||'entry_grr')}>台账</Button>
    </Space>}
  ];"""
NEW_SUB = """  return [
    {title:'操作', width:180, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>recJump(r)}>{r.reviewStatus==='待采集'?'录入数据':'查看结果'}</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.go(ENTRY_MAP[recKindId(r)]||'entry_grr')}>台账</Button>
    </Space>},
    {title:'分计划号', dataIndex:'id', width:150, render:v=><span className="mono">{v}</span>},
    {title:'分析方法', width:110, render:(_,r)=><Tag color={ANAL_COLOR[recKindId(r)]||'default'}>{ANAL_SHORT[recKindId(r)]||recKindId(r)}</Tag>},
    {title:'取样规则', width:230, render:(_,r)=><span className="tiny">{subRuleText(r)}</span>},
    {title:'状态', width:100, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'结论', width:130, render:(_,r)=><VerdictTag v={r.conclusion}/>}
  ];"""
rep(OLD_SUB, NEW_SUB, 'subPlanCols操作列前置')

open(P, 'w', encoding='utf-8').write(s)
print('OK 长度', len(s))
