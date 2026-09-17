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

anchor = "function GrrPage(){"
assert s.count(anchor)==1

component = """/* ============================================================================
 * 新增分析方法台账（2026-09-08 会议口径：特性-量具-方法；取样规则固化）
 *  线性/偏移性：5 标准件×10 次（覆盖量程）｜稳定性：25 子组×3~5 次（SPC 判异）
 *  Cg/Cgk(VDA Type1)：标准件 50 次｜分辨率：不取样直接录入
 * ==========================================================================*/
const ANA_PAGE = { linear:'anl_linear', stability:'anl_stability', cgcgk:'anl_cgcgk', resolution:'anl_resolution' };
const ANA_CFG = {
  linear:{ arr:'linear', idPref:'LIN', name:'线性/偏移性', params:(r)=> r.stds+' 个标准件 × '+r.per+' 次/件（覆盖量程）' },
  stability:{ arr:'stability', idPref:'STB', name:'稳定性', params:(r)=> r.groups+' 个子组 × '+r.per+' 次/组（跨 4 周~3 个月）' },
  cgcgk:{ arr:'cgcgk', idPref:'CG', name:'Cg/Cgk', params:(r)=> r.runs+' 次（标准件独立装夹）' },
  resolution:{ arr:'resolution', idPref:'RES', name:'分辨率', params:()=> '不取样，直接录入' }
};
let AnlOpen=null;
function anlOpenRec(kind,id){ AnlOpen={kind,id}; NavAPI.go(ANA_PAGE[kind]); }
function AnlPage({kind}){
  const CFG=ANA_CFG[kind];
  const d=Store.get();
  const [detail,setDetail]=useState(null);
  const [entryRec,setEntryRec]=useState(null);
  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);
  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});
  const rows=(d[CFG.arr]||[]).filter(r=>
    (!q.kw || (r.id+r.planId+r.instId+r.instName+r.object).toLowerCase().includes(q.kw.toLowerCase())) &&
    (!q.status || r.reviewStatus===q.status) &&
    (!q.concl || (r.conclusion||'').indexOf(q.concl)>=0));
  const resetQ=()=>{ setFkw('');setFstatus(undefined);setFconcl(undefined); setQ({kw:'',status:undefined,concl:undefined}); };
  useEffect(()=>{ if(AnlOpen && AnlOpen.kind===kind){ const rec=(d[CFG.arr]||[]).find(g=>g.id===AnlOpen.id); if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else setDetail(rec); } AnlOpen=null; } },[]);
  const cols=[
    {title:'操作', width:200, fixed:'left', render:(_,r)=><Space size={0}>
      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},
    {title:CFG.idPref+'编号', dataIndex:'id', width:115, render:(v,r)=><span className="row-link mono" onClick={()=>setDetail(r)}>{v}</span>},
    {title:'关联计划', dataIndex:'planId', width:110, render:(v)=><span className="row-link mono" onClick={()=>NavAPI.go('plan')}>{v||'-'}</span>},
    {title:'器具名称', width:150, render:(_,r)=>{ const it=d.instruments.find(i=>i.id===r.instId); return <span>{it?it.name:r.instName}</span>; }, ellipsis:true},
    {title:'测量对象', dataIndex:'object', width:160, ellipsis:true},
    {title:'取样规则', width:160, render:(_,r)=><span className="tiny">{CFG.params(r)}</span>},
    {title:'方法', dataIndex:'method', width:180, ellipsis:true},
    {title:'标准', dataIndex:'standard', width:105, render:v=><span className="mono tiny">{v||'-'}</span>},
    {title:'结论', width:130, render:(_,r)=>{ const c=recCalc(r); return <VerdictTag v={c?c.verdict:r.conclusion}/>; }},
    {title:'状态', width:90, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'分析人', dataIndex:'analyst', width:90},
    {title:'分析日期', dataIndex:'analysisDate', width:105}
  ];
  return <div>
    <Panel title="查询条件">
      <Space wrap>
        <Input.Search allowClear placeholder={CFG.idPref+'编号 / 关联计划 / 器具 / 测量对象'} style={{width:300}} value={fkw} onChange={e=>setFkw(e.target.value)}/>
        <Select allowClear placeholder="记录状态" style={{width:130}} value={fstatus} options={['待采集','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>
        <Select allowClear placeholder="结论" style={{width:130}} value={fconcl} options={['可接受','有条件','不可接受'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>
        <span className="tiny">共 {rows.length} 条</span>
      </Space>
    </Panel>
    <Panel title="操作">
      <Space wrap>
        <Button type="primary" onClick={()=>setQ({kw:fkw, status:fstatus, concl:fconcl})}>查询</Button>
        <Button onClick={resetQ}>重置</Button>
        <span className="tiny">查询 / 重置 在最前；{CFG.name}分析记录由 MSA 计划按分析方法自动生成（一器一计划一方法），取样规则固化：{CFG.params(rows[0]||{stds:5,per:10,groups:25,runs:50})}；录入表单按规则自动生成默认行数，可增减。</span>
      </Space>
    </Panel>
    <Panel title={CFG.name+'分析台账（'+rows.length+' 条）'}>
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:1580}} pagination={false}/>
    </Panel>
    {detail && <AnlDetail rec={detail} kind={kind} onClose={()=>setDetail(null)}/>}
    {entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s="待采集"/></Space>} width={kind==='stability'?1220:(kind==='cgcgk'?820:1000)} open onClose={()=>setEntryRec(null)}>
      <AnlEntry rec={entryRec} kind={kind} onClose={()=>setEntryRec(null)}/>
    </Drawer>}
  </div>;
}
function AnlActionForm({onChange}){
  const [form]=Form.useForm();
  useEffect(()=>{ form.setFieldsValue({type:'纠正措施', content:'', owner:'李工程师', planDate:TODAY}); },[]);
  return <Form form={form} layout="vertical" size="small" onValuesChange={(_,all)=>onChange&&onChange(all)}>
    <Form.Item name="type" label="措施类型"><Select options={['纠正措施','预防措施','培训/换人','量具维修/更换','标准更新'].map(c=>({value:c,label:c}))}/></Form.Item>
    <Form.Item name="content" label="措施内容" rules={[{required:true,message:'请填写'}]}><Input.TextArea rows={2}/></Form.Item>
    <Form.Item name="owner" label="责任人"><Input/></Form.Item>
    <Form.Item name="planDate" label="计划完成"><Input/></Form.Item>
  </Form>;
}
function AnlDetail({rec, kind, onClose}){
  const CFG=ANA_CFG[kind];
  const d=Store.get();
  const calc=recCalc(rec);
  const inst=d.instruments.find(i=>i.id===rec.instId);
  const me=d.me;
  const addAction=()=>{
    let v={type:'纠正措施',content:'',owner:me.name,planDate:TODAY};
    Modal.confirm({ title:'添加纠正措施 - '+rec.id, content:<AnlActionForm onChange={x=>v=x}/>, okText:'确认', cancelText:'取消',
      onOk:()=>{ mut(s=>{ const g=s[CFG.arr].find(x=>x.id===rec.id); g.actions=[...(g.actions||[]), {...v, status:'进行中'}]; logAction(s.me.name,'添加纠正措施',g.id,(v.content||'').slice(0,40)); }); toast.ok('已添加纠正措施'); } });
  };
  const reviewBtns=<Space wrap>
    {rec.reviewStatus==='待审核' && canDo(me.role,'review') && <Button size="small" type="primary" onClick={()=>{mut(s=>{const g=s[CFG.arr].find(x=>x.id===rec.id);g.reviewStatus='已批准';g.reviewer=me.name;g.reviewDate=TODAY;syncPlanFromRecord(s,g.planId);logAction(s.me.name,'审核通过',g.id,CFG.name+'分析审核通过，结论['+g.conclusion+']');}); toast.ok('已审核通过');}}>审核通过</Button>}
    {rec.reviewStatus==='待审核' && canDo(me.role,'review') && <Button size="small" danger onClick={()=>{mut(s=>{const g=s[CFG.arr].find(x=>x.id===rec.id);g.reviewStatus='需整改';g.reviewer=me.name;syncPlanFromRecord(s,g.planId);logAction(s.me.name,'退回整改',g.id,CFG.name+'分析退回：需制定纠正措施并复测');}); toast.warn('已退回整改');}}>退回整改</Button>}
    {rec.reviewStatus==='需整改' && canDo(me.role,'edit') && <Button size="small" onClick={addAction}>+ 添加纠正措施</Button>}
    {rec.reviewStatus==='需整改' && (rec.actions||[]).some(a=>a.status==='进行中') && canDo(me.role,'edit') && <Button size="small" type="primary" onClick={()=>{mut(s=>{const g=s[CFG.arr].find(x=>x.id===rec.id);g.actions.forEach(a=>{if(a.status==='进行中')a.status='已完成';});g.reviewStatus='已闭环';g.approver=me.name;g.approveDate=TODAY;syncPlanFromRecord(s,g.planId);logAction(s.me.name,'整改闭环',g.id,CFG.name+'纠正措施完成并复测验证，闭环归档');}); toast.ok('已闭环归档');}}>整改完成 · 复测验证 · 闭环</Button>}
  </Space>;
  const kpis = calc? (kind==='linear'? [{k:'最大偏移',v:fmt(calc.maxOff,3)},{k:'偏移%',v:fmt(calc.maxOffPct,1)+'%'},{k:'线性斜率',v:fmt(calc.slope,4)},{k:'R²',v:fmt(calc.r2,3)}]
    : kind==='stability'? [{k:'子组数',v:calc.xbars.length},{k:'X̄',v:fmt(calc.xbarBar,3)},{k:'R̄',v:fmt(calc.rbar,3)},{k:'UCL/LCL',v:fmt(calc.ucl,3)+'/'+fmt(calc.lcl,3)},{k:'出界点数',v:calc.out}]
    : kind==='cgcgk'? [{k:'均值',v:fmt(calc.m,4)},{k:'σ',v:fmt(calc.sd,4)},{k:'Cg',v:fmt(calc.Cg,2)},{k:'Cgk',v:fmt(calc.Cgk,2)},{k:'控制线',v:fmt(calc.usl,4)+'/'+fmt(calc.lsl,4)}]
    : [{k:'分辨率',v:rec.resValue||'-'},{k:'占公差',v:calc.pct!=null? fmt(calc.pct,1)+'%':'-'}]):[];
  return <Drawer title={<Space>{rec.id} · {rec.instName}<StatusTag s={rec.reviewStatus}/><VerdictTag v={rec.conclusion}/></Space>} width={980} open onClose={onClose} extra={reviewBtns}>
    {calc && <div className={"verdict-banner "+(calc.level===0?'verdict-accept':calc.level===1?'verdict-cond':'verdict-reject')}>
      <Space><b style={{fontSize:15}}>{CFG.name}分析 · {calc.verdict}</b><span className="tiny">判定依据：{calc.reasons.join('；')}</span></Space>
    </div>}
    <Descriptions column={3} size="small" bordered className="mt12" items={[
      {key:'关联计划', label:'关联计划', children:<span className="row-link mono" onClick={()=>NavAPI.go('plan')}>{rec.planId||'-'}</span>},
      {key:'器具编号', label:'器具编号', children:<span className="mono">{rec.instId||'-'}</span>},
      {key:'器具名称', label:'器具名称', children:inst?inst.name:'-'},
      {key:'测量对象', label:'测量对象', children:rec.object},
      {key:'分析方法', label:'分析方法', children:ANAL_SHORT[kind]},
      {key:'取样规则', label:'取样规则', children:CFG.params(rec)},
      {key:'检验标准', label:'检验标准', children:<span className="mono">{rec.standard||'-'}</span>},
      {key:'公差下限', label:'公差下限', children: rec.tolerance&&rec.tolerance.has? rec.tolerance.lsl:'-'},
      {key:'公差上限', label:'公差上限', children: rec.tolerance&&rec.tolerance.has? rec.tolerance.usl:'-'},
      {key:'分析人', label:'分析人', children:rec.analyst||'-'},
      {key:'分析日期', label:'分析日期', children:rec.analysisDate||'-'},
      {key:'单位', label:'单位', children:rec.unit||'-'}
    ]}/>
    {kpis.length>0 && <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>关键指标</span><div className="kpi-row" style={{gap:18}}>{kpis.map(x=><div key={x.k} className="kpi-item"><div className="k">{x.k}</div><div className="v">{x.v}</div></div>)}</div></div>
    </div>}
    {(rec.actions||[]).length>0 && <div className="mt12">{rec.actions.map((a,i)=><Alert key={i} type={a.status==='已完成'?'success':'warning'} showIcon style={{marginBottom:8}} message={<Space><Tag color={a.status==='已完成'?'green':'orange'}>{a.status}</Tag><b>{a.type}</b></Space>} description={<span>{a.content} ｜ 责任人：{a.owner} ｜ 计划完成：{a.planDate}</span>}/>)}</div>}
  </Drawer>;
}
function AnlEntry({rec, kind, onClose}){
  const CFG=ANA_CFG[kind];
  const d=Store.get();
  const me=d.me;
  const initState=()=>{
    if(kind==='linear') return {refs:Array.from({length:rec.stds||5},(_,i)=>rec.refs&&rec.refs[i]!==undefined?rec.refs[i]:''), raw:Array.from({length:rec.stds||5},()=>Array.from({length:rec.per||10},()=>''))};
    if(kind==='stability') return {raw:Array.from({length:rec.groups||25},()=>Array.from({length:rec.per||3},()=>''))};
    if(kind==='cgcgk') return {refValue:rec.refValue||'', raw:Array.from({length:rec.runs||50},()=>'')};
    return {resValue:rec.resValue||''};
  };
  const [st,setSt]=useState(initState);
  const [cnt,setCnt]=useState(kind==='stability'?(rec.groups||25):kind==='cgcgk'?(rec.runs||50):0);
  const setCell=(a,i,j,v)=>{ setSt(s=>{ const n={...s}; n[a]=s[a].map((r,ri)=>ri===i? (Array.isArray(r)? r.map((c,ci)=>ci===j?v:c): v):r); return n; }); };
  const regen=(n)=>{ if(kind==='stability'){ setSt(s=>({...s, raw:Array.from({length:n},()=>Array.from({length:rec.per||3},()=>''))})); } if(kind==='cgcgk'){ setSt(s=>({...s, raw:Array.from({length:n},()=>'')})); } };
  const submit=()=>{
    const check=(a)=>{ for(const r of st[a]){ for(const c of r){ if(c===''||c==null){ toast.warn('请完整录入数据'); return false; } } } return true; };
    let calc=null;
    if(kind==='linear'){ if(!check('raw')) return; if(st.refs.some(x=>!x)){ toast.warn('请填写每个标准件的参考值（真值）'); return; } calc=calcLinear({...rec, refs:st.refs, raw:st.raw}); }
    if(kind==='stability'){ if(!check('raw')) return; calc=calcStability({...rec, raw:st.raw}); }
    if(kind==='cgcgk'){ if(!st.refValue){ toast.warn('请填写标准件参考值（真值）'); return; } if(st.raw.some(x=>x===''||x==null)){ toast.warn('请完整录入 '+st.raw.length+' 次测量'); return; } calc=calcCgCgk({...rec, refValue:st.refValue, raw:st.raw}); }
    if(kind==='resolution'){ if(!st.resValue){ toast.warn('请填写分辨率值'); return; } calc=calcResolution({...rec, resValue:st.resValue}); }
    if(!calc){ toast.warn('数据不足，无法计算'); return; }
    mut(s=>{ const g=s[CFG.arr].find(x=>x.id===rec.id); Object.assign(g,{ raw:st.raw, refs:kind==='linear'?st.refs:g.refs, refValue:kind==='cgcgk'?st.refValue:g.refValue, resValue:kind==='resolution'?st.resValue:g.resValue,
      reviewStatus:'待审核', conclusion:calc.verdict, analyst:me.name, analysisDate:TODAY }); syncPlanFromRecord(s,g.planId); logAction(s.me.name,'数据提交',g.id,CFG.name+'分析样本录入提交，结论['+calc.verdict+']'); });
    toast.ok('已提交审核：结论 '+calc.verdict); onClose();
  };
  const cell=(i,j,v,onChange)=> <Input size="small" style={{width:78}} value={v} onChange={e=>onChange(e.target.value)}/>;
  const label=(txt,desc)=> <div style={{marginBottom:6}}><span className="flt-label">{txt}</span>{desc?<span className="tiny" style={{marginLeft:8}}>{desc}</span>:null}</div>;
  return <div>
    <Alert type="info" showIcon style={{marginBottom:12}} message={'取样规则（固化）：'+CFG.params(rec)} description={SAMPLING[kind]} />
    {(kind==='stability'||kind==='cgcgk') && <Space style={{marginBottom:12}}><span className="flt-label">数据行数（默认按规则生成，可增减）</span>
      <InputNumber size="small" min={1} max={200} value={cnt} onChange={v=>setCnt(v||1)}/>
      <Button size="small" onClick={()=>{ setCnt(cnt); regen(cnt); }}>重新生成 {cnt} 行</Button></Space>}
    {kind==='linear' && <div style={{maxHeight:430, overflow:'auto'}}>{label('标准件测量（每件 10 次，覆盖 0/25/50/75/100% 量程点）','参考值=鉴定证书/高等级量具真值')}
      <table className="mono-grid"><thead><tr><th>标准件</th><th>参考值</th>{Array.from({length:rec.per||10},(_,j)=><th key={j}>测{j+1}</th>)}</tr></thead>
      <tbody>{st.raw.map((row,i)=><tr key={i}><td>{'STD-'+String(i+1).padStart(2,'0')}（{(i*25)}%量程）</td>
        <td>{cell(i,0,st.refs[i],v=>setSt(s=>{const n={...s}; n.refs=s.refs.map((x,xi)=>xi===i?v:x); return n;}))}</td>
        {row.map((c,j)=><td key={j}>{cell(i,j,c,v=>setCell('raw',i,j,v))}</td>)}</tr>)}</tbody></table></div>}
    {kind==='stability' && <div style={{maxHeight:430, overflow:'auto'}}>{label('稳定性子组测量（25 子组 × 每期 3~5 次，跨 4 周~3 个月）','固定参照仪/工位，SPC 判异模型')}
      <table className="mono-grid"><thead><tr><th>子组</th>{Array.from({length:rec.per||3},(_,j)=><th key={j}>测{j+1}</th>)}<th>X̄</th><th>R</th></tr></thead>
      <tbody>{st.raw.map((row,i)=>{ const vals=row.map(Number).filter(v=>!isNaN(v)); const m=vals.length? vals.reduce((a,b)=>a+b,0)/vals.length:0; const rg=vals.length? (Math.max.apply(null,vals)-Math.min.apply(null,vals)):0;
        return <tr key={i}><td>{'G'+String(i+1).padStart(2,'0')}</td>{row.map((c,j)=><td key={j}>{cell(i,j,c,v=>setCell('raw',i,j,v))}</td>)}<td>{vals.length?fmt(m,3):'-'}</td><td>{vals.length?fmt(rg,3):'-'}</td></tr>; })}</tbody></table></div>}
    {kind==='cgcgk' && <div>{label('Cg/Cgk 测量（标准件连续 '+st.raw.length+' 次）','参考值 ±10% 公差控制线（VDA Type1）')}
      <Space style={{marginBottom:10}}><span className="flt-label">参考值（真值）</span><Input size="small" style={{width:120}} value={st.refValue} onChange={e=>setSt(s=>({...s, refValue:e.target.value}))}/></Space>
      <div style={{maxHeight:400, overflow:'auto'}}><table className="mono-grid"><thead><tr>{Array.from({length:Math.min(10,st.raw.length)},(_,i)=><th key={i}>测{i+1}</th>)}</tr></thead>
      <tbody>{Array.from({length:Math.ceil(st.raw.length/10)},(_,r0)=><tr key={r0}>{Array.from({length:Math.min(10,st.raw.length-r0*10)},(_,i)=>{ const idx=r0*10+i; return <td key={idx}>{cell(idx,0,st.raw[idx],v=>setCell('raw',idx,0,v))}</td>; })}</tr>)}</tbody></table></div></div>}
    {kind==='resolution' && <div>{label('分辨率（不取样，直接录入）','分辨率应 ≤ 过程公差的 1/10')}
      <Space><span className="flt-label">分辨率值{rec.unit?('（'+rec.unit+'）'):''}</span><Input size="small" style={{width:140}} value={st.resValue} onChange={e=>setSt(s=>({...s, resValue:e.target.value}))}/>
        {rec.tolerance&&rec.tolerance.has? <span className="tiny">过程公差：{rec.tolerance.lsl} ~ {rec.tolerance.usl}（自动解析自测量对象）</span>:<span className="tiny">未识别公差，请确认测量对象含公差（如 φ10±0.02）</span>}</Space></div>}
    <div style={{marginTop:18}}><Space><Button type="primary" onClick={submit}>提交分析（计算并判定）</Button><Button onClick={onClose}>取消</Button></Space></div>
  </div>;
}
"""

rep(anchor, component + anchor)

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
