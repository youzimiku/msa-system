# -*- coding: utf-8 -*-
"""创建MSA计划弹窗布局调整：
1) 器具筛选（查询条件）置顶
2) 计划填写信息合并为一块（不分组），字段随页面宽度自适应列数（1/2/3/4列）"""
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

start_mark = '    {/* ① 计划信息（写入计划） */}'
end_mark = '    <div style={{marginBottom:8}}>{stdSel?'
i = s.find(start_mark)
j = s.find(end_mark)
assert i > 0 and j > i, (i, j)
print('segment len:', j - i)

new_block = r'''    {/* ⑥ 器具筛选（查询条件）——置顶 */}
    <div style={{border:'1px dashed #91caff', background:'#f0f9ff', borderRadius:6, padding:'6px 10px 8px', marginBottom:12}}>
      <div className="grp-label" style={{marginBottom:6}}>器具筛选（查询条件） <span className="tiny" style={{color:'#888'}}>（仅用于筛选下方器具清单，不写入计划）</span></div>
      <Row gutter={12}>
        <Col xs={24} sm={12} lg={6}><span className="flt-label">复评状态</span><Select size="small" allowClear style={{width:140}} placeholder="正常 / 0-15天 / 16-30天 / 超期" value={dueSel||undefined} options={[{value:'normal',label:'正常'},{value:'0-15',label:'0-15天'},{value:'16-30',label:'16-30天'},{value:'overdue',label:'超期'}]} onChange={v=>setDueSel(v||'')}/></Col>
        {curGroup==='all' && <>
          <Col xs={24} sm={12} lg={6}><span className="flt-label">厂商</span><Select size="small" allowClear style={{width:140}} placeholder="厂商" value={fVendor} options={[...new Set(d.instruments.map(i=>i.vendor).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFVendor}/></Col>
          <Col xs={24} sm={12} lg={6}><span className="flt-label">型号</span><Select size="small" allowClear style={{width:140}} placeholder="型号" value={fModel} options={[...new Set(d.instruments.map(i=>i.model).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFModel}/></Col>
          <Col xs={24} sm={12} lg={6}><span className="flt-label">产线</span><Select size="small" allowClear style={{width:140}} placeholder="产线" value={fProd} options={[...new Set(d.instruments.map(i=>i.prodLine).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProd}/></Col>
          <Col xs={24} sm={12} lg={6}><span className="flt-label">工序（用途）</span><Select size="small" allowClear style={{width:140}} placeholder="工序（用途）" value={fProcess} options={[...new Set(d.instruments.map(i=>i.process).filter(Boolean))].map(v=>({value:v,label:v}))} onChange={setFProcess}/></Col>
        </>}
      </Row>
      <div className="tiny mt4">说明：复评状态对全部器具生效；厂商 / 型号 / 产线 / 工序 仅在选「全部器具」时出现，辅助挑样。器具仅「在用 / 待校准」且「无未闭环计划」的可纳入（状态一致性校验：器具存在未闭环计划时禁止重复生成；周期复评需待上一计划闭环后重新发起）。</div>
    </div>
    {/* 计划填写信息（合并一块，字段随页面宽度自适应列数：1列/2列/3列/4列） */}
    <div style={{border:'1px solid #e3eaf3', borderRadius:6, padding:'8px 10px 10px', marginBottom:12, background:'#fafcff'}}>
      <div className="grp-label" style={{marginBottom:6}}>计划填写信息 <span className="tiny" style={{color:'#888'}}>（以下字段将写入创建的 MSA 计划；带 * 为必选）</span></div>
      <Row gutter={[12,10]}>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">零件/工序 <b style={{color:'#cf1322'}}>*</b></span><Select size="small" allowClear style={{width:140}} placeholder="先选零件" value={partSel||undefined} options={partOptions} onChange={v=>{ setPartSel(v||''); setStdSel(''); setCfg({}); setSelKeys([]); }}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">检验标准 <b style={{color:'#cf1322'}}>*</b></span><Select size="small" allowClear style={{width:140}} placeholder={partSel? '选择该零件检验标准':'请先选零件'} disabled={!partSel} options={stdOptions} value={stdSel||undefined} onChange={v=>{ setStdSel(v||''); setCfg(c=>({...c,_ops:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].ops,_trials:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].trials,_parts:TYPE_PARAMS[stdTypeOf(v||'GRR')||'GRR'].parts})); setMMethods(v? ((stdTypeOf(v)==='KAPPA')?['KAPPA']:['GRR']) : []); }}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">创建方式</span><div><Tag color="blue">逐个创建（一器一计划）</Tag></div></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">计划名称模板（{'{inst}'}=器具名）</span><Input size="small" style={{width:140}} value={nameTpl} onChange={e=>setNameTpl(e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">触发依据</span><Select size="small" style={{width:140}} value={trigger} options={['周期复评','新量具','新过程','过程变更','顾客要求','内审发现'].map(c=>({value:c,label:c}))} onChange={setTrigger}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">计划检期</span><Input size="small" style={{width:140}} value={planDate} onChange={e=>setPlanDate(e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">部门</span><Select size="small" style={{width:140}} value={meta.dept} options={ENUM.deptOptions.map(c=>({value:c,label:c}))} onChange={v=>setMetaK('dept',v)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">零件号</span><Input size="small" style={{width:140}} value={meta.partNo} onChange={e=>setMetaK('partNo',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">质检区划</span><Input size="small" style={{width:140}} value={meta.qcArea} onChange={e=>setMetaK('qcArea',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">工厂</span><Input size="small" style={{width:140}} value={meta.plant} onChange={e=>setMetaK('plant',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">分厂</span><Input size="small" style={{width:140}} value={meta.subplant} onChange={e=>setMetaK('subplant',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">观察员</span><Input size="small" style={{width:140}} placeholder="观察/记录人员" value={meta.observer} onChange={e=>setMetaK('observer',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">测量人员</span><Input size="small" style={{width:140}} placeholder="参与测量人员（如：操作员A·王强）" value={meta.measurers} onChange={e=>setMetaK('measurers',e.target.value)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">复评周期（月）</span><InputNumber size="small" min={1} max={60} style={{width:140}} value={reviewMonths} onChange={v=>setReviewMonths(v||12)}/></Col>
        <Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">复评提前提醒（天）</span><InputNumber size="small" min={1} max={90} style={{width:140}} value={reviewAdvance} onChange={v=>setReviewAdvance(v||20)}/></Col>
        <Col span={24}><span className="flt-label">分析方法（勾选本次要生成的分析计划；一器一计划一方法，GRR 与 KAPPA 不同时勾选）</span><Checkbox.Group size="small" value={mMethods} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'resolution',label:'分辨率'}]} onChange={setMMethods}/></Col>
      </Row>
      <div className="tiny mt6">取样策略（按分析方法固化）：{mMethods.length? mMethods.map(m=>ANAL_SHORT[m]+'：'+SAMPLING[m]).join('；') : '未勾选时仅生成「未定型」计划，可在列表勾选后转 GRR / 转 KAPPA 定型。'}；公共字段（部门/零件号/质检区划/工厂/分厂/观察员/测量人员）写入本次创建的所有 MSA 计划，台账录入时可再细化。</div>
    </div>
'''

s = s[:i] + new_block + s[j:]
io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
