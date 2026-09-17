# -*- coding: utf-8 -*-
"""7 项 UI 调整：
1 全站列表操作列按钮去边框（type=link 文字按钮）
2 质量特性维护/抽样方法维护 改三面板（查询条件/操作/列表）+查询重置
3 抽样方法维护：新增取样规则按钮移到取样规则表上方
4 MSA计划列表：检验标准全部相同则只显示一个
5 MSA计划列表：判定结果汇总为一个（按分计划结论总结）
6 MSA计划列表字段按重要性重排
7 创建MSA计划按钮去闪电图标
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:90])
    s = s.replace(old, new, cnt)

# ========== 1. 全站操作列按钮 link 化 ==========
pat1 = re.compile(r'<Button size="small"(?![^>]*type=)(?=[^>]*>)')
n1 = len(pat1.findall(s))
s = pat1.sub('<Button size="small" type="link"', s)
pat2 = re.compile(r'<Button size="small" type="primary"( ghost)?')
n2 = len(pat2.findall(s))
s = pat2.sub('<Button size="small" type="link"', s)
print('link 化: no-type', n1, 'primary', n2)

# ========== 7. 创建按钮去闪电 ==========
rep("""<Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={()=>setBatchModal({})}>⚡ 创建MSA计划</Button>""",
    """<Button type="primary" disabled={!canDo(d.me.role,'edit')} onClick={()=>setBatchModal({})}>创建MSA计划</Button>""",
    1, 'no-flash')

# ========== 4/5/6. MSA计划 cols：检验标准列、判定结果列、重排 ==========
OLD_COLS = """  const cols=[
    {title:'操作', width:180, fixed:'left', render:(_,r)=><PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)} onTasks={()=>setTaskPlan(r)}/>},
    {title:'MSA计划号', dataIndex:'id', width:130, render:v=><span className="mono">{v}</span>},
    {title:'部门', dataIndex:'dept', width:100, render:v=><span className="tiny">{v||'暂无'}</span>},
    {title:'仪器/设备名称', width:160, render:(_,r)=>instCell(r,it=>it?it.name:'')},
    {title:'量具编号', width:110, render:(_,r)=>instCell(r,it=>it?<span className="mono">{it.id}</span>:'')},
    {title:'分辨率', width:86, render:(_,r)=>instCell(r,it=>it?<span className="mono tiny">{it.res||'暂无'}</span>:'')},
    {title:'工序', width:84, render:(_,r)=>instCell(r,it=>it?<span className="tiny">{it.process||'暂无'}</span>:'')},
    {title:'测量特性', width:160, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); return (r.instIds||[]).length>1? <span className="tiny">{recs.map(x=>x.object).filter(Boolean).join('、')}</span> : <span>{r.object||'暂无'}</span>; }},
    {title:'数据类型', width:92, render:(_,r)=><Tag color={(r.dataType||'计量型')==='计数型'?'purple':'blue'}>{r.dataType||'计量型'}</Tag>},
    ...ENUM.msaMethods.map(m=>msaM(m)),
    {title:'操作方法', width:150, render:(_,r)=><span className="tiny">{r.opMethod||'《测量系统分析操作指导书》'}</span>},
    {title:'计划完成时间', dataIndex:'planDate', width:112},
    {title:'实际完成时间', dataIndex:'actualDate', width:112, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'状态', width:90, render:(_,r)=>{ const v=planStatusView(r.status); return <Tooltip title={TIPS.plan[v.text]||v.text}><Tag color={v.color} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{v.text}</Tag></Tooltip>; }},
    {title:'分析方法', width:150, render:(_,r)=>{ const recs=planRecords(d,r.id); const ts=[...new Set(recs.map(x=>recKindId(x)))]; if(ts.length) return <Space size={2} wrap>{ts.map(t=>anTag(t))}</Space>; if(r.methods&&r.methods.length) return <Space size={2} wrap>{r.methods.map(t=>anTag(t))}</Space>; return <Tag>未定型</Tag>; }},
    {title:'分计划', width:130, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <Space size={2} wrap>{recs.map(x=><Tag key={x.id} color={ANAL_COLOR[recKindId(x)]||'default'}>{ANAL_SHORT[recKindId(x)]||recKindId(x)}</Tag>)}</Space> : <span className="tiny">未定型</span>; }},
    {title:'零件号', width:100, dataIndex:'partNo', render:v=><span className="mono">{v}</span>},
    {title:'分厂', width:90, dataIndex:'subplant'},
    {title:'测量人数', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numOps}</span> : (r.params? <span className="mono tiny">{r.params.ops}</span> : <span className="tiny">待定型</span>); }},
    {title:'测量次数', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numTrials}</span> : (r.params? <span className="mono tiny">{r.params.trials}</span> : <span className="tiny">待定型</span>); }},
    {title:'样本数量', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numParts}</span> : (r.params? <span className="mono tiny">{r.params.parts}</span> : <span className="tiny">待定型</span>); }},
    {title:'检验标准', width:105, render:(_,r)=>{ const recs=planRecords(d,r.id); if(recs.length) return <span className="tiny">{recs.map(x=>x.standard).filter(Boolean).join('、')}</span>; return r.standard? <span className="mono tiny">{r.standard}</span> : <span className="tiny">暂无</span>; }},
    {title:'判定结果', width:110, render:(_,r)=>{ const recs=planRecords(d,r.id); if(!recs.length) return r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:'待采集'; return <Space size={2} wrap>{recs.map(x=><VerdictTag key={x.id} v={x.conclusion}/>)}</Space>; }},
    {title:'录入人', dataIndex:'editor', width:90, ellipsis:true}
  ];"""

NEW_COLS = """  const stdAll=[...new Set(rows.map(r=>{ const rs=planRecords(d,r.id); return rs.length? rs.map(x=>x.standard).filter(Boolean).join('、') : (r.standard||''); }).filter(Boolean))];
  const stdSame = rows.length>1 && stdAll.length===1;
  const sumVerdict=(recs)=>{ // 按分计划结论汇总：任一不合格则不合格
    if(!recs.length) return '待采集';
    const v=recs.map(x=>x.conclusion).filter(Boolean);
    if(v.some(x=>x==='不可接受')) return '不可接受';
    if(v.some(x=>x==='有条件接受')) return '有条件接受';
    if(v.every(x=>x==='可接受'||x==='非常理想可接受')) return '可接受';
    return v.length? v[0] : '待采集';
  };
  const cols=[
    {title:'操作', width:180, fixed:'left', render:(_,r)=><PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)} onTasks={()=>setTaskPlan(r)}/>},
    {title:'MSA计划号', dataIndex:'id', width:130, render:v=><span className="mono">{v}</span>},
    {title:'仪器/设备名称', width:160, render:(_,r)=>instCell(r,it=>it?it.name:'')},
    {title:'量具编号', width:110, render:(_,r)=>instCell(r,it=>it?<span className="mono">{it.id}</span>:'')},
    {title:'测量特性', width:160, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); return (r.instIds||[]).length>1? <span className="tiny">{recs.map(x=>x.object).filter(Boolean).join('、')}</span> : <span>{r.object||'暂无'}</span>; }},
    {title:'检验标准', width:105, render:(_,r,idx)=>{ if(stdSame) return idx===0? <span className="mono tiny">{stdAll[0]}</span> : <span className="tiny">—</span>; const recs=planRecords(d,r.id); if(recs.length) return <span className="tiny">{recs.map(x=>x.standard).filter(Boolean).join('、')}</span>; return r.standard? <span className="mono tiny">{r.standard}</span> : <span className="tiny">暂无</span>; }},
    {title:'判定结果', width:110, render:(_,r)=>{ const recs=planRecords(d,r.id); const sv=sumVerdict(recs); return recs.length? <VerdictTag v={sv}/> : (r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:<span className="tiny">待采集</span>); }},
    {title:'状态', width:90, render:(_,r)=>{ const v=planStatusView(r.status); return <Tooltip title={TIPS.plan[v.text]||v.text}><Tag color={v.color} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{v.text}</Tag></Tooltip>; }},
    {title:'分析方法', width:150, render:(_,r)=>{ const recs=planRecords(d,r.id); const ts=[...new Set(recs.map(x=>recKindId(x)))]; if(ts.length) return <Space size={2} wrap>{ts.map(t=>anTag(t))}</Space>; if(r.methods&&r.methods.length) return <Space size={2} wrap>{r.methods.map(t=>anTag(t))}</Space>; return <Tag>未定型</Tag>; }},
    {title:'分计划', width:130, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <Space size={2} wrap>{recs.map(x=><Tag key={x.id} color={ANAL_COLOR[recKindId(x)]||'default'}>{ANAL_SHORT[recKindId(x)]||recKindId(x)}</Tag>)}</Space> : <span className="tiny">未定型</span>; }},
    ...ENUM.msaMethods.map(m=>msaM(m)),
    {title:'测量人数', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numOps}</span> : (r.params? <span className="mono tiny">{r.params.ops}</span> : <span className="tiny">待定型</span>); }},
    {title:'测量次数', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numTrials}</span> : (r.params? <span className="mono tiny">{r.params.trials}</span> : <span className="tiny">待定型</span>); }},
    {title:'样本数量', width:90, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <span className="mono tiny">{recs[0].numParts}</span> : (r.params? <span className="mono tiny">{r.params.parts}</span> : <span className="tiny">待定型</span>); }},
    {title:'工序', width:84, render:(_,r)=>instCell(r,it=>it?<span className="tiny">{it.process||'暂无'}</span>:'')},
    {title:'分辨率', width:86, render:(_,r)=>instCell(r,it=>it?<span className="mono tiny">{it.res||'暂无'}</span>:'')},
    {title:'数据类型', width:92, render:(_,r)=><Tag color={(r.dataType||'计量型')==='计数型'?'purple':'blue'}>{r.dataType||'计量型'}</Tag>},
    {title:'操作方法', width:150, render:(_,r)=><span className="tiny">{r.opMethod||'《测量系统分析操作指导书》'}</span>},
    {title:'部门', dataIndex:'dept', width:100, render:v=><span className="tiny">{v||'暂无'}</span>},
    {title:'零件号', width:100, dataIndex:'partNo', render:v=><span className="mono">{v}</span>},
    {title:'分厂', width:90, dataIndex:'subplant'},
    {title:'计划完成时间', dataIndex:'planDate', width:112},
    {title:'实际完成时间', dataIndex:'actualDate', width:112, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'录入人', dataIndex:'editor', width:90, ellipsis:true}
  ];"""
assert s.count(OLD_COLS) == 1, 'cols 定位失败 %d' % s.count(OLD_COLS)
s = s.replace(OLD_COLS, NEW_COLS, 1)

# ========== 2/3. CharPage 三面板 ==========
OLD_CHAR = """  return <div>
    <PageHead title="质量特性维护"/>
    <Panel>
      <Space wrap size={10}>
        <Input.Search allowClear placeholder="特性编号 / 名称 / 零件 / 工序" style={{width:220}} onSearch={setKw} onChange={e=>!e.target.value&&setKw('')}/>
        <Select allowClear placeholder="特性类型" style={{width:140}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} value={fType} onChange={setFType}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fStatus} onChange={setFStatus}/>
        <Button type="primary" onClick={()=>setModal({})}>新增特性</Button>
      </Space>
    </Panel>
    <Panel>
      <Table rowKey="id" size="small" dataSource={rows} scroll={{x:1500}} pagination={{pageSize:10,showTotal:t=>'共 '+t+' 条'}} columns={cols}/>
    </Panel>"""
NEW_CHAR = """  return <div>
    <PageHead title="质量特性维护"/>
    <Panel title="查询条件">
      <Space wrap size={10}>
        <Input allowClear placeholder="特性编号 / 名称 / 零件 / 工序" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>
        <Select allowClear placeholder="特性类型" style={{width:140}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} value={ft2} onChange={setFt2}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fs2} onChange={setFs2}/>
      </Space>
    </Panel>
    <Panel title="操作">
      <Space wrap size={10}>
        <Button type="primary" onClick={doQuery}>查询</Button>
        <Button onClick={doReset}>重置</Button>
        <Button type="primary" onClick={()=>setModal({})}>新增特性</Button>
      </Space>
    </Panel>
    <Panel title="质量特性列表">
      <Table rowKey="id" size="small" dataSource={rows} scroll={{x:1500}} pagination={{pageSize:10,showTotal:t=>'共 '+t+' 条'}} columns={cols}/>
    </Panel>"""
assert s.count(OLD_CHAR) == 1, 'CharPage 定位失败 %d' % s.count(OLD_CHAR)
s = s.replace(OLD_CHAR, NEW_CHAR, 1)

# CharPage state：草稿+生效分离
OLD_CHAR_ST = """function CharPage(){
  const d=Store.get();
  const [kw,setKw]=useState('');
  const [fType,setFType]=useState();
  const [fStatus,setFStatus]=useState();
  const [detail,setDetail]=useState(null);
  const [modal,setModal]=useState(null);
  const rows=(d.characteristics||[]).filter(r=>(!kw || (r.id+r.name+r.partName+r.processName).includes(kw)))
    .filter(r=>!fType || r.type===fType).filter(r=>!fStatus || r.status===fStatus);"""
NEW_CHAR_ST = """function CharPage(){
  const d=Store.get();
  const [fkw2,setFkw2]=useState(''); const [ft2,setFt2]=useState(); const [fs2,setFs2]=useState();
  const [kw,setKw]=useState(''); const [fType,setFType]=useState(); const [fStatus,setFStatus]=useState();
  const [detail,setDetail]=useState(null);
  const [modal,setModal]=useState(null);
  const doQuery=()=>{ setKw(fkw2); setFType(ft2); setFStatus(fs2); };
  const doReset=()=>{ setFkw2(''); setFt2(); setFs2(); setKw(''); setFType(); setFStatus(); };
  const rows=(d.characteristics||[]).filter(r=>(!kw || (r.id+r.name+r.partName+r.processName).includes(kw)))
    .filter(r=>!fType || r.type===fType).filter(r=>!fStatus || r.status===fStatus);"""
assert s.count(OLD_CHAR_ST) == 1, 'CharPage state 定位失败 %d' % s.count(OLD_CHAR_ST)
s = s.replace(OLD_CHAR_ST, NEW_CHAR_ST, 1)

# ========== 2/3. SamplingPage 三面板 + 新增取样规则移位 ==========
OLD_SAM = """  return <div>
    <PageHead title="抽样方法维护"/>
    <Panel>
      <Space wrap size={10}>
        <Input.Search allowClear placeholder="方法代码 / 名称" style={{width:220}} onSearch={setKw} onChange={e=>!e.target.value&&setKw('')}/>
        <Select allowClear placeholder="是否需要取样" style={{width:140}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} value={fNeed} onChange={setFNeed}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fSt} onChange={setFSt}/>
        <Button type="primary" onClick={()=>setMModal({})}>新增方法</Button>
        <Button onClick={()=>setRModal({})}>新增取样规则</Button>
      </Space>
    </Panel>
    <Panel title="分析方法代码表">
      <Table rowKey="code" size="small" dataSource={mRows} scroll={{x:1200}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={methodCols}/>
    </Panel>
    <Panel title="取样规则表">
      <Table rowKey="id" size="small" dataSource={rRows} scroll={{x:1700}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={ruleCols}/>
    </Panel>"""
NEW_SAM = """  return <div>
    <PageHead title="抽样方法维护"/>
    <Panel title="查询条件">
      <Space wrap size={10}>
        <Input allowClear placeholder="方法代码 / 名称" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>
        <Select allowClear placeholder="是否需要取样" style={{width:140}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} value={fn2} onChange={setFn2}/>
        <Select allowClear placeholder="状态" style={{width:140}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} value={fs2} onChange={setFs2}/>
      </Space>
    </Panel>
    <Panel title="操作">
      <Space wrap size={10}>
        <Button type="primary" onClick={doQuery}>查询</Button>
        <Button onClick={doReset}>重置</Button>
        <Button type="primary" onClick={()=>setMModal({})}>新增方法</Button>
      </Space>
    </Panel>
    <Panel title="分析方法代码表">
      <Table rowKey="code" size="small" dataSource={mRows} scroll={{x:1200}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={methodCols}/>
    </Panel>
    <Panel title="取样规则表">
      <div style={{marginBottom:8}}><Button type="primary" onClick={()=>setRModal({})}>新增取样规则</Button></div>
      <Table rowKey="id" size="small" dataSource={rRows} scroll={{x:1700}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={ruleCols}/>
    </Panel>"""
assert s.count(OLD_SAM) == 1, 'SamplingPage 定位失败 %d' % s.count(OLD_SAM)
s = s.replace(OLD_SAM, NEW_SAM, 1)

# SamplingPage state
OLD_SAM_ST = """function SamplingPage(){
  const d=Store.get();
  const [kw,setKw]=useState('');
  const [fNeed,setFNeed]=useState();
  const [fSt,setFSt]=useState();
  const [mModal,setMModal]=useState(null);
  const [rModal,setRModal]=useState(null);
  const mRows=(d.anMethods||[]).filter(r=>(!kw || (r.code+r.name).toLowerCase().includes(kw.toLowerCase())))
    .filter(r=>!fNeed || r.needSample===fNeed).filter(r=>!fSt || r.status===fSt);"""
NEW_SAM_ST = """function SamplingPage(){
  const d=Store.get();
  const [fkw2,setFkw2]=useState(''); const [fn2,setFn2]=useState(); const [fs2,setFs2]=useState();
  const [kw,setKw]=useState(''); const [fNeed,setFNeed]=useState(); const [fSt,setFSt]=useState();
  const [mModal,setMModal]=useState(null);
  const [rModal,setRModal]=useState(null);
  const doQuery=()=>{ setKw(fkw2); setFNeed(fn2); setFSt(fs2); };
  const doReset=()=>{ setFkw2(''); setFn2(); setFs2(); setKw(''); setFNeed(); setFSt(); };
  const mRows=(d.anMethods||[]).filter(r=>(!kw || (r.code+r.name).toLowerCase().includes(kw.toLowerCase())))
    .filter(r=>!fNeed || r.needSample===fNeed).filter(r=>!fSt || r.status===fSt);"""
assert s.count(OLD_SAM_ST) == 1, 'SamplingPage state 定位失败 %d' % s.count(OLD_SAM_ST)
s = s.replace(OLD_SAM_ST, NEW_SAM_ST, 1)

open(P, 'w', encoding='utf-8').write(s)
print('ui7 OK 长度', len(s))
