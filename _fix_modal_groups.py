# -*- coding: utf-8 -*-
"""1) 全站输入控件统一 140（查询区/工具行/弹窗表单；表格格内控件保持 100%）
   2) 创建MSA计划弹窗上半部分分组：①计划信息 ②公共字段 ③检验标准 ④分析方法 ⑤复评配置（写入计划）⑥器具筛选（查询条件）"""
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'expect %d of [%s...] got %d' % (n, old[:70], c)
    s = s.replace(old, new, n)

# ============ A. 创建弹窗上半部分分组改造（按行号替换 1783-1814） ============
lines = s.split('\n')
assert lines[1782].strip().startswith('<Row gutter={12} style={{marginBottom:12}}>'), repr(lines[1782][:60])
assert lines[1813].strip() == '</div>', repr(lines[1813])

new_block = [
"    {/* ① 计划信息（写入计划） */}",
"    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'6px 10px 8px', marginBottom:10, background:'#fafcff'}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>① 计划信息 <span className=\"tiny\" style={{color:'#888'}}>（创建后写入计划）</span></div>",
"      <Row gutter={12}>",
"        <Col span={8}><span className=\"flt-label\">创建方式</span><div><Tag color=\"blue\">逐个创建（一器一计划）</Tag></div></Col>",
"        <Col span={8}><span className=\"flt-label\">计划名称模板（{'{inst}'}=器具名）</span><Input size=\"small\" style={{width:140}} value={nameTpl} onChange={e=>setNameTpl(e.target.value)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">触发依据</span><Select size=\"small\" style={{width:140}} value={trigger} options={['周期复评','新量具','新过程','过程变更','顾客要求','内审发现'].map(c=>({value:c,label:c}))} onChange={setTrigger}/></Col>",
"        <Col span={4}><span className=\"flt-label\">计划检期</span><Input size=\"small\" style={{width:140}} value={planDate} onChange={e=>setPlanDate(e.target.value)}/></Col>",
"      </Row>",
"    </div>",
"    {/* ② 公共字段（写入本次所有计划） */}",
"    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'6px 10px 8px', marginBottom:10, background:'#fafcff'}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>② 公共字段 <span className=\"tiny\" style={{color:'#888'}}>（写入本次创建的所有计划，台账录入时可再细化）</span></div>",
"      <Row gutter={12}>",
"        <Col span={4}><span className=\"flt-label\">部门</span><Select size=\"small\" style={{width:140}} value={meta.dept} options={ENUM.deptOptions.map(c=>({value:c,label:c}))} onChange={v=>setMetaK('dept',v)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">零件号</span><Input size=\"small\" style={{width:140}} value={meta.partNo} onChange={e=>setMetaK('partNo',e.target.value)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">质检区划</span><Input size=\"small\" style={{width:140}} value={meta.qcArea} onChange={e=>setMetaK('qcArea',e.target.value)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">工厂</span><Input size=\"small\" style={{width:140}} value={meta.plant} onChange={e=>setMetaK('plant',e.target.value)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">分厂</span><Input size=\"small\" style={{width:140}} value={meta.subplant} onChange={e=>setMetaK('subplant',e.target.value)}/></Col>",
"        <Col span={4}><span className=\"flt-label\">观察员</span><Input size=\"small\" style={{width:140}} placeholder=\"观察/记录人员\" value={meta.observer} onChange={e=>setMetaK('observer',e.target.value)}/></Col>",
"      </Row>",
"      <Row gutter={12} style={{marginTop:6}}>",
"        <Col span={12}><span className=\"flt-label\">测量人员</span><Input size=\"small\" style={{width:140}} placeholder=\"参与测量人员（如：操作员A·王强）\" value={meta.measurers} onChange={e=>setMetaK('measurers',e.target.value)}/></Col>",
"      </Row>",
"    </div>",
"    {/* ③ 检验标准（必选：先选零件 → 再选标准） */}",
"    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'6px 10px 8px', marginBottom:10, background:'#fafcff'}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>③ 检验标准 <span className=\"tiny\" style={{color:'#888'}}>（必选：先选零件 → 再选该零件下的一个检验标准；标准定义在零件/工序上，不直接绑器具）</span></div>",
"      <Row gutter={12}>",
"        <Col span={12}><span className=\"flt-label\">零件/工序</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"先选零件\" value={partSel||undefined} options={partOptions} onChange={v=>{ setPartSel(v||''); setStdSel(''); setCfg({}); setSelKeys([]); }}/></Col>",
"        <Col span={12}><span className=\"flt-label\">检验标准</span><Select size=\"small\" allowClear style={{width:140}} placeholder={partSel? '选择该零件检验标准':'请先选零件'} disabled={!partSel} options={stdOptions} value={stdSel||undefined} onChange={v=>{ setStdSel(v||''); setCfg(c=>({...c,_ops:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].ops,_trials:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].trials,_parts:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].parts})); setMMethods(v? ((stdTypeOf(v)==='KAPPA')?['KAPPA']:['GRR']) : []); }}/></Col>",
"      </Row>",
"    </div>",
"    {/* ④ 分析方法（勾选生成类型） */}",
"    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'6px 10px 8px', marginBottom:10, background:'#fafcff'}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>④ 分析方法 <span className=\"tiny\" style={{color:'#888'}}>（勾选本次要生成的分析计划；一器一计划一方法，GRR 与 KAPPA 不同时勾选）</span></div>",
"      <Checkbox.Group size=\"small\" value={mMethods} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'resolution',label:'分辨率'}]} onChange={setMMethods}/>",
"      <div className=\"tiny\" style={{marginTop:6}}>取样策略：{mMethods.length? mMethods.map(m=>ANAL_SHORT[m]+'：'+SAMPLING[m]).join('；') : '未勾选时仅生成「未定型」计划，可在列表勾选后转 GRR / 转 KAPPA 定型。'}</div>",
"    </div>",
"    {/* ⑤ 复评配置（写入计划） */}",
"    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'6px 10px 8px', marginBottom:10, background:'#fafcff'}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>⑤ 复评配置 <span className=\"tiny\" style={{color:'#888'}}>（写入计划：下次复评 = 上次MSA日期 + 复评周期；距复评 ≤ 提前提醒天数时预警）</span></div>",
"      <Row gutter={12}>",
"        <Col span={6}><span className=\"flt-label\">复评周期（月）</span><InputNumber size=\"small\" min={1} max={60} style={{width:140}} value={reviewMonths} onChange={v=>setReviewMonths(v||12)}/></Col>",
"        <Col span={6}><span className=\"flt-label\">复评提前提醒（天）</span><InputNumber size=\"small\" min={1} max={90} style={{width:140}} value={reviewAdvance} onChange={v=>setReviewAdvance(v||20)}/></Col>",
"      </Row>",
"    </div>",
"    {/* ⑥ 器具筛选（查询条件：仅筛选下方器具，不写入计划） */}",
"    <div style={{border:'1px dashed #91caff', background:'#f0f9ff', borderRadius:6, padding:'6px 10px 8px', marginBottom:12}}>",
"      <div className=\"grp-label\" style={{marginBottom:6}}>⑥ 器具筛选（查询条件） <span className=\"tiny\" style={{color:'#888'}}>（仅用于筛选下方器具清单，不写入计划）</span></div>",
"      <Row gutter={12}>",
"        <Col span={6}><span className=\"flt-label\">复评状态</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"正常 / 0-15天 / 16-30天 / 超期\" value={dueSel||undefined} options={[{value:'normal',label:'正常'},{value:'0-15',label:'0-15天'},{value:'16-30',label:'16-30天'},{value:'overdue',label:'超期'}]} onChange={v=>setDueSel(v||'')}/></Col>",
"        {curGroup==='all' && <>",
"          <Col span={6}><span className=\"flt-label\">厂商</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"厂商\" value={fVendor} options={[...new Set(d.instruments.map(i=>i.vendor).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFVendor}/></Col>",
"          <Col span={6}><span className=\"flt-label\">型号</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"型号\" value={fModel} options={[...new Set(d.instruments.map(i=>i.model).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFModel}/></Col>",
"          <Col span={6}><span className=\"flt-label\">产线</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"产线\" value={fProd} options={[...new Set(d.instruments.map(i=>i.prodLine).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProd}/></Col>",
"          <Col span={6}><span className=\"flt-label\">工序（用途）</span><Select size=\"small\" allowClear style={{width:140}} placeholder=\"工序（用途）\" value={fProcess} options={[...new Set(d.instruments.map(i=>i.process).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProcess}/></Col>",
"        </>}",
"      </Row>",
"      <div className=\"tiny mt4\">说明：复评状态对全部器具生效；厂商 / 型号 / 产线 / 工序 仅在选「全部器具」时出现，辅助挑样。器具仅「在用 / 待校准」且「无未闭环计划」的可纳入（状态一致性校验：器具存在未闭环计划时禁止重复生成；周期复评需待上一计划闭环后重新发起）。</div>",
"    </div>",
"    <div style={{marginBottom:8}}>{stdSel? <Tag color=\"blue\">本次创建：1 个检验标准 · 1 个质量特性 · 创建后类型为空，待「转 GRR / 转 KAPPA」定型（生成台账待采集记录）</Tag> : <Tag>请先选零件与检验标准</Tag>}</div>",
]
lines[1782:1814] = new_block

# 删除原「全部器具」筛选 Row（已并入 ⑥ 组）
old_sel = [
"        {curGroup==='all' && <Row gutter={12} style={{marginBottom:6}}>",
"          <Col span={6}><Select size=\"small\" allowClear style={{width:'100%'}} placeholder=\"厂商\" value={fVendor} options={[...new Set(d.instruments.map(i=>i.vendor).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFVendor}/></Col>",
"          <Col span={6}><Select size=\"small\" allowClear style={{width:'100%'}} placeholder=\"型号\" value={fModel} options={[...new Set(d.instruments.map(i=>i.model).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFModel}/></Col>",
"          <Col span={6}><Select size=\"small\" allowClear style={{width:'100%'}} placeholder=\"产线\" value={fProd} options={[...new Set(d.instruments.map(i=>i.prodLine).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProd}/></Col>",
"          <Col span={6}><Select size=\"small\" allowClear style={{width:'100%'}} placeholder=\"工序（用途）\" value={fProcess} options={[...new Set(d.instruments.map(i=>i.process).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProcess}/></Col>",
"        </Row>}",
]
# 找到并删除（删除后保证后续行对齐）
joined = '\n'.join(lines)
cnt = joined.count('\n'.join(old_sel))
assert cnt == 1, 'old_sel block found %d' % cnt
joined = joined.replace('\n'.join(old_sel), '')
lines = joined.split('\n')
s = '\n'.join(lines)

# ============ B. 查询区 / 工具行输入控件统一 140 ============
rep('style={{width:280}}', 'style={{width:140}}', 8)
rep('style={{width:280,marginBottom:14}}', 'style={{width:140,marginBottom:14}}', 1)
rep('style={{width:180}}', 'style={{width:140}}', 1)   # 台账「当前器具组」选择器

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
