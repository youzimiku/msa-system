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

# D1 标准兜底加 groupIds（绑定器具组：为周期自动选样准备）
rep("      note:s.note||'', qcArea:s.qcArea||'质检科', plant:s.plant||PLANTS[0], subplant:s.subplant||SUBPLANTS[0]\n    });",
    "      note:s.note||'', qcArea:s.qcArea||'质检科', plant:s.plant||PLANTS[0], subplant:s.subplant||SUBPLANTS[0],\n      groupIds:s.groupIds||(s.id==='STD-MSA-001'?['G-01']:(s.id==='STD-MSA-003'?['G-04']:[])) // 绑定器具组（会议口径：为周期自动选样准备）\n    });")

# D2 标准列表加"绑定器具组"列
rep("    {title:'适用器具数量', width:100, render:(_,r)=>{ const app=applicableInstruments(d,r); return <span className=\"mono\">{app.length} 台</span>; }},",
    "    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className=\"tiny\">{gs.map(g=>g.name).join('、')}</span> : <span className=\"tiny\">-</span>; }},")
rep("    {title:'适用器具数量', width:100, render:(_,r)=>{ const app=applicableInstruments(d,r); return <span className=\"mono\">{app.length} 台</span>; }},\n    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className=\"tiny\">{gs.map(g=>g.name).join('、')}</span> : <span className=\"tiny\">-</span>; }},",
    "    {title:'适用器具数量', width:100, render:(_,r)=>{ const app=applicableInstruments(d,r); return <span className=\"mono\">{app.length} 台</span>; }},\n    {title:'绑定器具组', width:130, render:(_,r)=>{ const gs=(r.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? <span className=\"tiny\">{gs.map(g=>g.name).join('、')}</span> : <span className=\"tiny\">-</span>; }},")

# D3 标准详情加绑定器具组
rep("        {key:'检验标准', label:'检验标准', children:detail.basis, span:2},",
    "        {key:'检验标准', label:'检验标准', children:detail.basis, span:2},\n        {key:'绑定器具组', label:'绑定器具组', children: (()=>{ const gs=(detail.groupIds||[]).map(gid=>(d.instGroups||[]).find(g=>g.id===gid)).filter(Boolean); return gs.length? gs.map(g=>g.name).join('、') : <span className=\"tiny\">-（为周期自动选样准备）</span>; })()},")

# D4 标准表单加绑定器具组多选
rep("        <Col span={8}><Form.Item name=\"qcArea\" label=\"质检区划\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"plant\" label=\"工厂\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"subplant\" label=\"分厂\"><Input/></Form.Item></Col>",
    "        <Col span={8}><Form.Item name=\"qcArea\" label=\"质检区划\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"plant\" label=\"工厂\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"subplant\" label=\"分厂\"><Input/></Form.Item></Col>\n        <Col span={24}><Form.Item name=\"groupIds\" label=\"绑定器具组（会议口径：为周期自动选样准备）\" tooltip=\"周期 MSA 校验时，系统按标准绑定的器具组自动筛选样机器具生成计划\"><Select mode=\"multiple\" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+' '+g.name}))}/></Form.Item></Col>")

# D5 onOk 保留 groupIds
rep("    ['partName','processName','method','numOps','numTrials','numParts','res','unit','target','usl','lsl','note','qcArea','plant','subplant','editor','editorDate']",
    "    ['partName','processName','method','numOps','numTrials','numParts','res','unit','target','usl','lsl','note','qcArea','plant','subplant','editor','editorDate','groupIds']")

# D6 标准维护页操作区提示更新
rep("        <span className=\"tiny\">查询 / 重置 在最前；检验标准定义在「零件/工序」上（不绑定器具），适用器具按工序自动匹配；创建 MSA 计划时先选零件 → 选该零件的一个检验标准 → 再勾选器具。</span>",
    "        <span className=\"tiny\">查询 / 重置 在最前；检验标准定义在「零件/工序」上（不绑定器具），适用器具按工序自动匹配，另可按「绑定器具组」为周期自动选样准备；创建 MSA 计划时先选零件 → 选该零件的一个检验标准 → 勾选分析方法 → 再勾选器具。</span>")

# D7 仪表盘 planTypes 按新方法体系
rep("  const planTypes = p => { const recs=planRecords(d,p.id); if(p.type==='GRR'||p.type==='KAPPA') return [p.type]; if(!recs.length) return ['未定型']; const ts=[...new Set(recs.map(x=>x.id.indexOf('GRR')===0?'GRR':'KAPPA'))]; return ts.length? ts : ['未定型']; };",
    "  const planTypes = p => { if(p.type) return [p.type]; const recs=planRecords(d,p.id); if(!recs.length) return ['未定型']; const ts=[...new Set(recs.map(x=>recKindId(x)))]; return ts.length? ts : ['未定型']; };")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
