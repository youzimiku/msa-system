# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new, tag, cnt=1):
    global t
    n = t.count(old)
    assert n == cnt, '锚点数量不符 %s: 期望 %d 实际 %d' % (tag, cnt, n)
    t = t.replace(old, new)
    print('OK:', tag)

# ============ 1) 查询条件：去掉状态 Radio ============
rep("""        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>方法名称</span><Select allowClear style={{width:140}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} value={fMethod2} onChange={setFMethod2}/>
        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>状态</span><Radio.Group size="small" value={fs2||''} onChange={e=>setFs2(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="启用">启用</Radio><Radio value="停用">停用</Radio></Radio.Group>""",
"""        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>方法名称</span><Select allowClear style={{width:140}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} value={fMethod2} onChange={setFMethod2}/>""",
"查询条件去状态", cnt=1)

# ============ 2) mergeCols 重构（方法固定代码表） ============
rep("""  const mergeCols=[
    {title:'操作', width:110, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveMRow(r)}>保存</Button>
      <Button size="small" type="link" danger disabled={mRef(r)} onClick={()=>delMRow(r)}>删除</Button>
    </Space>},
    {title:'方法代码', dataIndex:'code', width:110, render:v=><span className="mono">{v}</span>},
    {title:'方法名称', dataIndex:'name', width:190, render:(_,r)=><Input size="small" value={STRIP_PAREN(r.name)} onChange={e=>setMF(r,'name',e.target.value)}/>},
    {title:'是否需要取样', dataIndex:'needSample', width:104, render:(_,r)=><Select size="small" value={r.needSample||'是'} style={{width:92}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setMF(r,'needSample',x)}/>},
    {title:'方法组', dataIndex:'mergeWith', width:120, render:(_,r)=><Input size="small" value={r.mergeWith||''} onChange={e=>setMF(r,'mergeWith',e.target.value)}/>},
    {title:'数据类型', dataIndex:'defaultType', width:108, render:(_,r)=><Select size="small" value={r.defaultType||'计量型'} style={{width:98}} options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]} onChange={x=>setMF(r,'defaultType',x)}/>},
    {title:'状态', dataIndex:'status', width:86, render:(_,r)=><Switch size="small" checked={r.status==='启用'} onChange={x=>setMF(r,'status',x?'启用':'停用')}/>},
    {title:'默认样品数', width:92, render:(_,r)=><InputNumber size="small" min={0} value={r.rule?r.rule.sampleDefault:''} style={{width:82}} onChange={x=>setRF(r,'sampleDefault',x)}/>},
    {title:'默认人数', width:84, render:(_,r)=><InputNumber size="small" min={0} value={r.rule?r.rule.opsDefault:''} style={{width:74}} onChange={x=>setRF(r,'opsDefault',x)}/>},
    {title:'默认次数', width:84, render:(_,r)=><InputNumber size="small" min={0} value={r.rule?r.rule.trialsDefault:''} style={{width:74}} onChange={x=>setRF(r,'trialsDefault',x)}/>},
    {title:'样品数范围', width:140, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.rule?r.rule.sampleMin:''} style={{width:58}} onChange={x=>setRF(r,'sampleMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.rule?r.rule.sampleMax:''} style={{width:58}} onChange={x=>setRF(r,'sampleMax',x)}/></Space>},
    {title:'人数范围', width:132, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.rule?r.rule.opsMin:''} style={{width:54}} onChange={x=>setRF(r,'opsMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.rule?r.rule.opsMax:''} style={{width:54}} onChange={x=>setRF(r,'opsMax',x)}/></Space>},
    {title:'次数范围', width:132, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.rule?r.rule.trialsMin:''} style={{width:54}} onChange={x=>setRF(r,'trialsMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.rule?r.rule.trialsMax:''} style={{width:54}} onChange={x=>setRF(r,'trialsMax',x)}/></Space>},
    {title:'工厂', width:92, render:(_,r)=><Select size="small" value={r.rule?r.rule.plant:''} style={{width:82}} options={PLANTS_OPT} onChange={x=>setRF(r,'plant',x)}/>},
    {title:'方法备注', dataIndex:'note', width:180, ellipsis:true, render:(_,r)=><Input size="small" value={r.note||''} onChange={e=>setMF(r,'note',e.target.value)}/>}
  ];""",
"""  const mergeCols=[
    {title:'操作', width:70, fixed:'left', render:(_,r)=><Button size="small" type="link" onClick={()=>saveMRow(r)}>保存</Button>},
    {title:'方法代码', dataIndex:'code', width:110, render:v=><span className="mono">{v}</span>},
    {title:'方法名称', dataIndex:'name', width:230, render:v=><span>{STRIP_PAREN(v)}</span>},
    {title:'是否需要取样', dataIndex:'needSample', width:104, render:(_,r)=><Select size="small" value={r.needSample||'是'} style={{width:92}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setMF(r,'needSample',x)}/>},
    {title:'方法组', dataIndex:'mergeWith', width:130, render:(_,r)=><Input size="small" value={r.mergeWith||''} onChange={e=>setMF(r,'mergeWith',e.target.value)}/>},
    {title:'数据类型', dataIndex:'defaultType', width:108, render:(_,r)=><Select size="small" value={r.defaultType||'计量型'} style={{width:98}} options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]} onChange={x=>setMF(r,'defaultType',x)}/>},
    {title:'方法备注', dataIndex:'note', width:360, ellipsis:true, render:(_,r)=><Input size="small" value={r.note||''} onChange={e=>setMF(r,'note',e.target.value)}/>}
  ];""",
"mergeCols 重构", cnt=1)

# ============ 3) 新增抽样规则函数 + 列表列（插在 mergeCols 之后、jRows 之前） ============
rep("""  const jRows=(d.judgeRules||[]).filter(r=>(!kw || (r.id+r.method+r.verdict).toLowerCase().includes(kw.toLowerCase())))
    .filter(r=>!selMethod || String(r.method).toLowerCase()===String(selMethod).toLowerCase());""",
"""  /* 抽样规则：方法+工厂+车间 唯一；同一组合重复时保存拦截 */
  const addRuleRow=()=>{ const id='SR-0'+(d.samplingRules.length+1); mut(s=>{ s.samplingRules.unshift({id, method:'', category:'其他', sampleDefault:'', sampleMin:'', sampleMax:'', opsDefault:'', opsMin:'', opsMax:'', trialsDefault:'', trialsMin:'', trialsMax:'', useOps:true, readingsMin:'', readingsMax:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, note:''}); logAction(s.me.name,'新增抽样规则',id,'列表新增空白行'); }); };
  const setRuleF=(r,k,v)=>{ mut(s=>{ const rec=s.samplingRules.find(x=>x.id===r.id); if(rec) rec[k]=v; }); };
  const saveRuleRow=(r)=>{ if(!r.method){ toast.warn('请先选择方法'); return; } const dup=(d.samplingRules||[]).some(x=>x.id!==r.id && String(x.method).toLowerCase()===String(r.method).toLowerCase() && x.plant===r.plant && x.subplant===r.subplant); if(dup){ toast.warn('同一方法 + 工厂 + 车间已存在抽样规则，不可重复'); return; } mut(s=>{ const rec=s.samplingRules.find(x=>x.id===r.id); if(rec){ rec.editor=s.me.name; rec.editorDate=NOW; } logAction(s.me.name,'编辑抽样规则',r.id,'方法 '+(r.method||'')); }); toast.ok('已保存'); };
  const delRuleRow=(r)=>{ Modal.confirm({title:'删除抽样规则 — '+(r.method||r.id), content:'确认删除该抽样规则？删除后不可恢复。', okText:'删除', okType:'danger', onOk:()=>{ mut(s=>{ s.samplingRules=s.samplingRules.filter(x=>x.id!==r.id); logAction(s.me.name,'删除抽样规则',r.id,'删除 '+(r.method||r.id)); }); toast.ok('已删除'); } }); };
  const samplingCols=[
    {title:'操作', width:110, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveRuleRow(r)}>保存</Button>
      <Button size="small" type="link" danger onClick={()=>delRuleRow(r)}>删除</Button>
    </Space>},
    {title:'方法', dataIndex:'method', width:120, render:(_,r)=><Select size="small" showSearch value={r.method||undefined} style={{width:108}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} placeholder="选择方法" onChange={x=>setRuleF(r,'method',x)}/>},
    {title:'工厂', dataIndex:'plant', width:110, render:(_,r)=><Select size="small" value={r.plant||''} style={{width:100}} options={PLANTS_OPT} onChange={x=>setRuleF(r,'plant',x)}/>},
    {title:'车间', dataIndex:'subplant', width:100, render:(_,r)=><Select size="small" value={r.subplant||''} style={{width:90}} options={SUBPLANTS_OPT} onChange={x=>setRuleF(r,'subplant',x)}/>},
    {title:'默认样品数', width:96, render:(_,r)=><InputNumber size="small" min={0} value={r.sampleDefault} style={{width:86}} onChange={x=>setRuleF(r,'sampleDefault',x)}/>},
    {title:'默认人数', width:88, render:(_,r)=><InputNumber size="small" min={0} value={r.opsDefault} style={{width:78}} onChange={x=>setRuleF(r,'opsDefault',x)}/>},
    {title:'默认次数', width:88, render:(_,r)=><InputNumber size="small" min={0} value={r.trialsDefault} style={{width:78}} onChange={x=>setRuleF(r,'trialsDefault',x)}/>},
    {title:'样品数范围', width:140, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.sampleMin} style={{width:58}} onChange={x=>setRuleF(r,'sampleMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.sampleMax} style={{width:58}} onChange={x=>setRuleF(r,'sampleMax',x)}/></Space>},
    {title:'人数范围', width:132, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.opsMin} style={{width:54}} onChange={x=>setRuleF(r,'opsMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.opsMax} style={{width:54}} onChange={x=>setRuleF(r,'opsMax',x)}/></Space>},
    {title:'次数范围', width:132, render:(_,r)=><Space size={2}><InputNumber size="small" min={0} value={r.trialsMin} style={{width:54}} onChange={x=>setRuleF(r,'trialsMin',x)}/><span style={{color:'#999999'}}>~</span><InputNumber size="small" min={0} value={r.trialsMax} style={{width:54}} onChange={x=>setRuleF(r,'trialsMax',x)}/></Space>},
    {title:'备注', dataIndex:'note', width:300, ellipsis:true, render:(_,r)=><Input size="small" value={r.note||''} onChange={e=>setRuleF(r,'note',e.target.value)}/>}
  ];
  const jRows=(d.judgeRules||[]).filter(r=>(!kw || (r.id+r.method+r.verdict).toLowerCase().includes(kw.toLowerCase())))
    .filter(r=>!selMethod || String(r.method).toLowerCase()===String(selMethod).toLowerCase());""",
"新增抽样规则函数与列", cnt=1)

# ============ 4) judgeCols 加工厂车间 + verdict 下拉 ============
rep("""  const judgeCols=[
    {title:'操作', width:110, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveJRow(r)}>保存</Button>
      <Button size="small" type="link" danger onClick={()=>delJRow(r)}>删除</Button>
    </Space>},
    {title:'规则编号', dataIndex:'id', width:100, render:v=><span className="mono">{v}</span>},
    {title:'所属方法', dataIndex:'method', width:130, render:(_,r)=><Select size="small" value={r.method||undefined} style={{width:110}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} onChange={x=>setJF(r,'method',x)}/>},
    {title:'判定条件', dataIndex:'condition', width:320, ellipsis:true, render:(_,r)=><Input size="small" value={r.condition||''} onChange={e=>setJF(r,'condition',e.target.value)}/>},
    {title:'判定结论', dataIndex:'verdict', width:150, render:(_,r)=><Input size="small" value={r.verdict||''} onChange={e=>setJF(r,'verdict',e.target.value)}/>},
    {title:'说明', dataIndex:'note', width:460, ellipsis:true, render:(_,r)=><Input size="small" value={r.note||''} onChange={e=>setJF(r,'note',e.target.value)}/>}
  ];""",
"""  const judgeCols=[
    {title:'操作', width:110, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveJRow(r)}>保存</Button>
      <Button size="small" type="link" danger onClick={()=>delJRow(r)}>删除</Button>
    </Space>},
    {title:'规则编号', dataIndex:'id', width:100, render:v=><span className="mono">{v}</span>},
    {title:'所属方法', dataIndex:'method', width:130, render:(_,r)=><Select size="small" value={r.method||undefined} style={{width:110}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} onChange={x=>setJF(r,'method',x)}/>},
    {title:'工厂', dataIndex:'plant', width:100, render:(_,r)=><Select size="small" value={r.plant||''} style={{width:90}} options={PLANTS_OPT} onChange={x=>setJF(r,'plant',x)}/>},
    {title:'车间', dataIndex:'subplant', width:92, render:(_,r)=><Select size="small" value={r.subplant||''} style={{width:82}} options={SUBPLANTS_OPT} onChange={x=>setJF(r,'subplant',x)}/>},
    {title:'判定条件', dataIndex:'condition', width:300, ellipsis:true, render:(_,r)=><Input size="small" value={r.condition||''} onChange={e=>setJF(r,'condition',e.target.value)}/>},
    {title:'判定结论', dataIndex:'verdict', width:130, render:(_,r)=><Select size="small" value={r.verdict||undefined} style={{width:110}} options={[{value:'可接受',label:'可接受'},{value:'有条件接受',label:'有条件接受'},{value:'不可接受',label:'不可接受'}]} onChange={x=>setJF(r,'verdict',x)}/>},
    {title:'说明', dataIndex:'note', width:360, ellipsis:true, render:(_,r)=><Input size="small" value={r.note||''} onChange={e=>setJF(r,'note',e.target.value)}/>}
  ];""",
"judgeCols 加工厂车间与结论下拉", cnt=1)

# ============ 5) addJudgeRow 空行补 plant/subplant ============
rep("const addJudgeRow=()=>{ const id='JR-0'+(d.judgeRules.length+1); mut(s=>{ s.judgeRules.unshift({id, method:'', condition:'', verdict:'', note:''}); logAction(s.me.name,'新增判断规则',id,'列表新增空白行'); }); };",
"const addJudgeRow=()=>{ const id='JR-0'+(d.judgeRules.length+1); mut(s=>{ s.judgeRules.unshift({id, method:'', condition:'', verdict:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, note:''}); logAction(s.me.name,'新增判断规则',id,'列表新增空白行'); }); };",
"addJudgeRow 补工厂车间", cnt=1)

# ============ 6) 方法列表 Panel：去新增按钮；Tabs 三个页签 ============
rep("""    <Panel title="分析方法列表">
      <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addMethodRow}>新增分析方法</Button></div>
      <Table rowKey="code" size="small" dataSource={mRows} onRow={r=>({onClick:()=>setSelMethod(r.code), style: selMethod===r.code? {background:'#e6f4ff'} : undefined})} scroll={{x:2500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={mergeCols}/>
    </Panel>
    <Panel title="判断规则 / 计算参数">
      <Tabs defaultActiveKey="judge" items={[
        {key:'judge', label:'判断规则', children:<>
          <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addJudgeRow}>新增判断规则</Button></div>
          <Table rowKey="id" size="small" dataSource={jRows} scroll={{x:1250}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={judgeCols}/>
        </>},
        {key:'cal', label:'计算参数', children:<>
          <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addParamRow}>新增计算参数</Button></div>
          <Table rowKey="id" size="small" dataSource={d.calParams||[]} scroll={{x:700}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={calCols}/>
        </>}
      ]}/>
    </Panel>""",
"""    <Panel title="分析方法（固定代码表）">
      <Table rowKey="code" size="small" dataSource={mRows} onRow={r=>({onClick:()=>setSelMethod(r.code), style: selMethod===r.code? {background:'#e6f4ff'} : undefined})} scroll={{x:1100}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={mergeCols}/>
    </Panel>
    <Panel title="抽样规则 / 判断规则 / 计算参数">
      <Tabs defaultActiveKey="sample" items={[
        {key:'sample', label:'抽样规则', children:<>
          <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addRuleRow}>新增抽样规则</Button></div>
          <Table rowKey="id" size="small" dataSource={d.samplingRules||[]} scroll={{x:1500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={samplingCols}/>
        </>},
        {key:'judge', label:'判断规则', children:<>
          <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addJudgeRow}>新增判断规则</Button></div>
          <Table rowKey="id" size="small" dataSource={jRows} scroll={{x:1350}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={judgeCols}/>
        </>},
        {key:'cal', label:'计算参数', children:<>
          <div style={{marginBottom:8, textAlign:'left'}}><Button type="primary" onClick={addParamRow}>新增计算参数</Button></div>
          <Table rowKey="id" size="small" dataSource={d.calParams||[]} scroll={{x:700}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={calCols}/>
        </>}
      ]}/>
    </Panel>""",
"方法列表与三页签", cnt=1)

# ============ 7) 页面说明文案 ============
rep("  sampling:{label:'抽样方法维护', text:'维护分析方法（方法代码 / 名称 / 方法组合并配置）与取样参数（样品数 / 人数 / 次数 / 读数上下限）、判断规则与计算参数。', ops:'新增/修改为列表行内编辑；范围字段在编辑模式下拆为上下限两个输入框；判断规则、计算参数按页签维护。'},",
"  sampling:{label:'抽样方法维护', text:'分析方法为固定代码表（名称只读，其余可编辑）；抽样规则按「方法 + 工厂 + 车间」维护（同一组合唯一），判断规则 / 计算参数按页签维护。', ops:'方法固定不可增删；抽样规则 / 判断规则 / 计算参数三个页签均行内编辑，行首保存按钮常驻；抽样规则同一方法 + 工厂 + 车间不可重复。'},",
"页面说明文案", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('页面重构完成')
