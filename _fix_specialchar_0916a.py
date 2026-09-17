# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new, tag):
    global t
    assert t.count(old) == 1, '锚点不唯一/不存在: ' + tag + ' (count=' + str(t.count(old)) + ')'
    t = t.replace(old, new)
    print('OK:', tag)

# A. applyFieldDefaults：特殊特性主数据 seed + 被测参数迁移 specialCharId
rep(
"    if(!c.plant) c.plant=PLANTS[ix%2];\n    if(!c.subplant) c.subplant=SUBPLANTS[ix%2];\n  });",
"    if(!c.plant) c.plant=PLANTS[ix%2];\n    if(!c.subplant) c.subplant=SUBPLANTS[ix%2];\n  });\n  /* 特殊特性主数据（业务口径：特殊特性清单由 CP/研发下发，前端模拟；被测参数按顺序绑定） */\n  if(!d.specialChars) d.specialChars=[\n    {id:'SC-001', name:'轴径 φ50', type:'SC', category:'关键特性'},\n    {id:'SC-002', name:'轴径 φ10', type:'SC', category:'关键特性'},\n    {id:'SC-003', name:'拧紧力矩 25N·m', type:'CC', category:'重要特性'},\n    {id:'SC-004', name:'壳体关键尺寸', type:'CC', category:'重要特性'},\n    {id:'SC-005', name:'外观判定', type:'普通', category:'一般特性'}\n  ];\n  (d.characteristics||[]).forEach((c,ix)=>{ if(!c.specialCharId){ const scs=d.specialChars||[]; if(scs.length) c.specialCharId=scs[ix%scs.length].id; } });",
"A")

# B. 被测参数列表：特性类型后加「特殊特性」列（行内下拉，显示 编号+名称）
rep(
"    {title:'特性类型', dataIndex:'type', width:110, render:(_,r)=><Select size=\"small\" value={r.type||'普通'} style={{width:100}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} onChange={x=>setF(r,'type',x)}/>},\n    {title:'零件号', dataIndex:'partNo', width:110,",
"    {title:'特性类型', dataIndex:'type', width:110, render:(_,r)=><Select size=\"small\" value={r.type||'普通'} style={{width:100}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} onChange={x=>setF(r,'type',x)}/>},\n    {title:'特殊特性', width:176, render:(_,r)=><Select size=\"small\" showSearch optionFilterProp=\"label\" placeholder=\"选择特殊特性\" value={r.specialCharId||undefined} style={{width:166}} options={(d.specialChars||[]).map(s=>({value:s.id,label:s.id+' '+s.name}))} onChange={x=>setF(r,'specialCharId',x)}/>},\n    {title:'零件号', dataIndex:'partNo', width:110,",
"B")

# C. CharDetail 详情：特性类别后加「特殊特性」行
rep(
"      {key:'category',label:'特性类别',children:rec.category},\n      {key:'partName',label:'零件名称',children:rec.partName||'—'},",
"      {key:'category',label:'特性类别',children:rec.category},\n      {key:'specialChar',label:'特殊特性',children:(()=>{ const s=(d.specialChars||[]).find(x=>x.id===rec.specialCharId); return s? (s.id+' '+s.name) : '—'; })()},\n      {key:'partName',label:'零件名称',children:rec.partName||'—'},",
"C")

# D1. 被测参数维护页：新增 groupView state
rep(
"  const [stdDetail,setStdDetail]=useState(null);\n  const [stdModal,setStdModal]=useState(null);",
"  const [stdDetail,setStdDetail]=useState(null);\n  const [stdModal,setStdModal]=useState(null);\n  const [groupView,setGroupView]=useState(null);",
"D1")

# D2. 检验标准列表操作列：新增「器具组」按钮
rep(
"    {title:'操作', width:110, render:(_,r)=><Space size={0}>\n      <Button size=\"small\" type=\"link\" onClick={()=>saveStdRow(r)}>保存</Button>\n      <Button size=\"small\" type=\"link\" danger disabled={stdRef(r)} onClick={()=>delStd(r)}>删除</Button>\n    </Space>},",
"    {title:'操作', width:170, render:(_,r)=><Space size={0}>\n      <Button size=\"small\" type=\"link\" onClick={()=>setGroupView(r)}>器具组</Button>\n      <Button size=\"small\" type=\"link\" onClick={()=>saveStdRow(r)}>保存</Button>\n      <Button size=\"small\" type=\"link\" danger disabled={stdRef(r)} onClick={()=>delStd(r)}>删除</Button>\n    </Space>},",
"D2")

# D3. 检验标准列表：去掉「绑定器具组」列（stdCols 内，用 setStdF 状态列作上下文区分）
rep(
"    {title:'状态', dataIndex:'status', width:100, render:(_,r)=><Switch size=\"small\" checked={r.status==='启用'} onChange={x=>setStdF(r,'status',x?'启用':'停用')}/>},\n    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className=\"tiny\">{gs.map(g=>g.name).join('、')}</span> : <span className=\"tiny\">暂无</span>; }},\n    {title:'备注', dataIndex:'note', width:160,",
"    {title:'状态', dataIndex:'status', width:100, render:(_,r)=><Switch size=\"small\" checked={r.status==='启用'} onChange={x=>setStdF(r,'status',x?'启用':'停用')}/>},\n    {title:'备注', dataIndex:'note', width:160,",
"D3")

# D4. 检验标准「器具组」弹窗（Modal 查看绑定的器具组列表）
rep(
"    {stdModal && <StandardModal value={stdModal} onClose={()=>setStdModal(null)}/>}",
"    {stdModal && <StandardModal value={stdModal} onClose={()=>setStdModal(null)}/>}\n    {groupView && <Modal cancelText=\"取消\" title={'检验标准 '+groupView.id+' · 绑定的器具组'} open width={800} onCancel={()=>setGroupView(null)} footer={<Button type=\"primary\" onClick={()=>setGroupView(null)}>关闭</Button>}>\n      {(groupView.groupIds||[]).length===0 ? <div style={{color:'#666666',padding:'22px 0',textAlign:'center',fontSize:14}}>未绑定器具组</div> :\n      <Table rowKey=\"id\" size=\"small\" pagination={false} dataSource={(groupView.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean)}\n        columns={[\n          {title:'组编号', dataIndex:'id', width:90, render:v=><span className=\"mono\">{v}</span>},\n          {title:'组名称', dataIndex:'name', width:170, ellipsis:true},\n          {title:'组类型', width:110, render:(_,g)=><Tag color={isPersonGroupType(g.type||'inst')?'purple':'blue'} style={{marginRight:0}}>{isPersonGroupType(g.type||'inst')?'人员组':'测量器具组'}</Tag>},\n          {title:'成员数', width:90, render:(_,g)=>{ const isP=isPersonGroupType(g.type||'inst'); const n=isP? (d.personnel||[]).filter(x=>x.postCode===(g.postCode||'')).length : (g.memberIds||[]).length; return n+' '+(isP?'人':'台'); }},\n          {title:'说明', dataIndex:'note', ellipsis:true}\n        ]}/>}\n    </Modal>}",
"D4")

# E1. 创建MSA计划弹窗：新增 qualityChar state
rep(
"  const setMetaK=(k,v)=>setMeta(m=>({...m,[k]:v}));",
"  const setMetaK=(k,v)=>setMeta(m=>({...m,[k]:v}));\n  const [qualityChar,setQualityChar]=useState('');",
"E1")

# E2. 计划填写信息模块：零件名称后加「质量特性」下拉（特性编号+特性名称）
rep(
"        <Col xs={24} sm={12} md={8} lg={4}><span className=\"flt-label\">零件名称</span><Input size=\"small\" style={{width:140}} disabled placeholder={charObj&&charObj.partName? charObj.partName : '由特性带出'}/></Col>",
"        <Col xs={24} sm={12} md={8} lg={4}><span className=\"flt-label\">零件名称</span><Input size=\"small\" style={{width:140}} disabled placeholder={charObj&&charObj.partName? charObj.partName : '由特性带出'}/></Col>\n        <Col xs={24} sm={12} md={8} lg={4}><span className=\"flt-label\">质量特性</span><Select size=\"small\" style={{width:140}} showSearch optionFilterProp=\"label\" placeholder=\"选择质量特性\" options={(d.specialChars||[]).map(s=>({value:s.id,label:s.id+' '+s.name}))} value={qualityChar||undefined} onChange={setQualityChar}/></Col>",
"E2")

io.open(P, 'w', encoding='utf-8').write(t)
print('全部修改完成')
