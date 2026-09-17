# -*- coding: utf-8 -*-
"""v2.6 第三批 c：KappaDetail 重构为业务报告式（报告头/逐样本两两一致/列联表/交叉表/逐对Kappa/自评/审批栏）+ KappaPage 加逐对KAPPA列"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

NEW_DETAIL = """function KappaDetail({rec,onClose}){
  const d=Store.get();
  const calc=calcKappaRec(rec);
  const inst=d.instruments.find(i=>i.id===rec.instId);
  const plan=(d.plans||[]).find(p=>p.id===rec.planId);
  const me=d.me;
  const [actionModal,setActionModal]=useState(false);
  const level = calc.level;
  const banner = {0:{t:'测量系统一致性可接受',c:'accept',desc:'总体 KAPPA≥0.75，有效性≥90%、错误率≤2%、错误警报率≤5%，满足要求'},1:{t:'可接受边缘-可能需改进',c:'cond',desc:'存在单项落入边缘区间（Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10%），需加强培训并复测验证'},2:{t:'不可接受-需改进',c:'reject',desc:'存在单项不可接受（Kappa<0.40 / 有效性<80% / 错误率>5% / 错误警报率>10%），须重新培训/更换判定标准后复测'}}[level];
  const reviewBtns=<Space wrap>
    {rec.reviewStatus==='待审核'&&canDo(me.role,'review')&&<Button size="small" type="primary" onClick={()=>{mut(s=>{const g=s.kappa.find(x=>x.id===rec.id);g.reviewStatus='已批准';g.reviewer=me.name;g.reviewDate=TODAY;syncPlanFromRecord(s,g.planId);backfillMsa(s,g.planId);logAction(s.me.name,'审核通过',g.id,'KAPPA分析审核通过，结论['+g.conclusion+']');}); toast.ok('已审核通过');}}>审核通过</Button>}
    {rec.reviewStatus==='待审核'&&canDo(me.role,'review')&&<Button size="small" danger onClick={()=>{mut(s=>{const g=s.kappa.find(x=>x.id===rec.id);g.reviewStatus='需整改';g.reviewer=me.name;syncPlanFromRecord(s,g.planId);logAction(s.me.name,'退回整改',g.id,'审核退回');}); toast.warn('已退回整改');}}>退回整改</Button>}
    {rec.reviewStatus==='需整改'&&canDo(me.role,'edit')&&<Button size="small" onClick={()=>setActionModal(true)}>+ 添加纠正措施</Button>}
    {rec.reviewStatus==='需整改'&&rec.actions.some(a=>a.status==='进行中')&&canDo(me.role,'edit')&&<Button size="small" type="primary" onClick={()=>{mut(s=>{const g=s.kappa.find(x=>x.id===rec.id);g.actions.forEach(a=>{if(a.status==='进行中')a.status='已完成';});g.reviewStatus='已闭环';g.approver=me.name;g.approveDate=TODAY;syncPlanFromRecord(s,g.planId);backfillMsa(s,g.planId);logAction(s.me.name,'整改闭环',g.id,'KAPPA整改完成并复测验证，闭环');}); toast.ok('已闭环');}}>整改完成 · 复测 · 闭环</Button>}
  </Space>;
  const hasRaw = !!(rec.rawData && rec.rawData.length && rec.rawData[0] && Array.isArray(rec.rawData[0][0]));
  const finalData = hasRaw? rec.rawData.map(app=>app.map(s=>majority1(s))) : (rec.appData||[]);
  const ref = rec.reference||[];
  const N = ref.length;
  const srows = Array.from({length:N},(_,i)=>({
    i, ref:ref[i], a:finalData[0]?finalData[0][i]:'—', b:finalData[1]?finalData[1][i]:'—', c:finalData[2]?finalData[2][i]:'—'
  }));
  const pairMark=(x,y)=> (x==='—'||y==='—')?'—': (x===y?'D':(x===0?'A':'B'));
  const selfMark=(ai)=> hasRaw? (()=>{ const app=rec.rawData[ai]; const first=app&&app[0]; if(!first) return '—'; const all=app.every(s=>s.every((v,t)=>v===first[t])); return all?'D':majority1(first); })() : '—';
  const sampleCols=[
    {title:'样本', width:56, render:(_,r)=><span className="mono">{r.i+1}</span>},
    {title:'Ref', width:52, render:(_,r)=><span className="mono">{r.ref}</span>},
    {title:'A', width:44, render:(_,r)=><span className="mono">{r.a}</span>},
    {title:'B', width:44, render:(_,r)=><span className="mono">{r.b}</span>},
    {title:'C', width:44, render:(_,r)=><span className="mono">{r.c}</span>},
    {title:'A*B', width:52, render:(_,r)=><span className="mono">{pairMark(r.a,r.b)}</span>},
    {title:'A*C', width:52, render:(_,r)=><span className="mono">{pairMark(r.a,r.c)}</span>},
    {title:'B*C', width:52, render:(_,r)=><span className="mono">{pairMark(r.b,r.c)}</span>},
    {title:'Self-A', width:60, render:(_,r)=><span className="mono">{selfMark(0)}</span>},
    {title:'Self-B', width:60, render:(_,r)=><span className="mono">{selfMark(1)}</span>},
    {title:'Self-C', width:60, render:(_,r)=><span className="mono">{selfMark(2)}</span>}
  ];
  // 2×2 列联表（Data Summary）：A*B / A*C / B*C / A*REF / B*REF / C*REF
  const pairs6 = [];
  const labels6 = ['A*B','A*C','B*C','A*REF','B*REF','C*REF'];
  const crosstab = [];
  labels6.forEach(lb=>{
    const [x,y]= lb==='A*B'?[0,1]: lb==='A*C'?[0,2]: lb==='B*C'?[1,2]: lb==='A*REF'?[0,'r']: lb==='B*REF'?[1,'r']:[2,'r'];
    const X = x==='r'? ref : (finalData[x]||ref);
    const Y = y==='r'? ref : (finalData[y]||ref);
    let a=0,b=0,c=0,d=0;
    for(let k=0;k<N;k++){ const xv=X[k]||0, yv=Y[k]||0; if(xv===1&&yv===1)a++; else if(xv===1&&yv===0)b++; else if(xv===0&&yv===1)c++; else d++; }
    const n=N, po=(a+d)/n;
    const cX1=X.filter(v=>v===1).length, cX0=n-cX1, cY1=Y.filter(v=>v===1).length, cY0=n-cY1;
    const pe=((a+b)*(a+c)+(c+d)*(b+d))/(n*n);
    const kappa=(1-pe===0)?1:(po-pe)/(1-pe);
    pairs6.push({label:lb, d00:d, d10:b, d01:c, d11:a, n});
    crosstab.push({label:lb, c0:cY0, c1:cY1, e0:(cX0*cY0)/n, e1:(cX1*cY1)/n, po, pe, kappa});
  });
  const kappaTag=(k)=><Tag color={k>=0.75?'green':k>=0.4?'orange':'red'}>{k>=0.75?'好':k>=0.4?'边缘':'差'}</Tag>;
  const perCols=[
    {title:'检验员', dataIndex:'name', width:150},
    {title:'一致数', width:80, render:(_,r)=> <span className="mono">{r.a+r.d}</span>},
    {title:'总样本数', width:90, render:(_,r)=> <span className="mono">{rec.numSamples}</span>},
    {title:'有效性', width:90, render:(_,r)=>fmt(r.effectiveness,1)+'%'},
    {title:'错误率(漏判)', width:100, render:(_,r)=><span style={{color:r.missRate>5?'#dc2626':r.missRate>2?'#d97706':'inherit'}}>{fmt(r.missRate,1)}%</span>},
    {title:'错误警报率(误判)', width:120, render:(_,r)=><span style={{color:r.falseAlarm>10?'#dc2626':r.falseAlarm>5?'#d97706':'inherit'}}>{fmt(r.falseAlarm,1)}%</span>},
    {title:'与Ref判定', width:100, render:(_,r)=><Tag color={r.effectiveness>=90?'green':r.effectiveness>=80?'orange':'red'}>{r.effectiveness>=90?'可接受':r.effectiveness>=80?'边缘':'不可接受'}</Tag>}
  ];
  const pairCols=[
    {title:'检验员对', dataIndex:'label', width:180},
    {title:'一致数', width:80, render:(_,r)=> <span className="mono">{r.a+r.d}</span>},
    {title:'总样本数', width:90, render:(_,r)=> <span className="mono">{rec.numSamples}</span>},
    {title:'KAPPA', dataIndex:'kappa', width:90, render:v=>fmt(v,2)},
    {title:'一致性%', width:90, render:(_,r)=>fmt(100*r.po,1)+'%'},
    {title:'判定', width:80, render:(_,r)=>kappaTag(r.kappa)}
  ];
  const selfCols=[
    {title:'检验员', dataIndex:'name', width:150},
    {title:'试验次数', dataIndex:'trials', width:90, render:v=><span className="mono">{v}</span>},
    {title:'两两一致对', width:100, render:(_,r)=><span className="mono">{r.pairs.length} 对</span>},
    {title:'匹配样本', width:90, render:(_,r)=> <span className="mono">{r.pairs.reduce((m,p)=>m+(p.a+p.d),0)}</span>},
    {title:'总样本', width:80, render:(_,r)=> <span className="mono">{rec.numSamples}</span>},
    {title:'%重复性一致', width:110, render:(_,r)=>{ const v=100*r.pairs.reduce((m,p)=>m+(p.a+p.d),0)/(r.pairs.length*rec.numSamples); return fmt(v,1)+'%'; }},
    {title:'判定', width:90, render:(_,r)=>{ const v=100*r.pairs.reduce((m,p)=>m+(p.a+p.d),0)/(r.pairs.length*rec.numSamples); return <Tag color={v>=90?'green':v>=80?'orange':'red'}>{v>=90?'可接受':v>=80?'边缘':'不可接受'}</Tag>; }}
  ];
  const table2x2Cols=[
    {title:'交叉组', dataIndex:'label', width:110, render:v=><b>{v}</b>},
    {title:'0*0', dataIndex:'d00', width:80, render:v=><span className="mono">{v}</span>},
    {title:'1*0', dataIndex:'d10', width:80, render:v=><span className="mono">{v}</span>},
    {title:'0*1', dataIndex:'d01', width:80, render:v=><span className="mono">{v}</span>},
    {title:'1*1', dataIndex:'d11', width:80, render:v=><span className="mono">{v}</span>},
    {title:'合计', width:80, render:(_,r)=><span className="mono">{r.n}</span>}
  ];
  const ctCols=[
    {title:'交叉组', dataIndex:'label', width:110, render:v=><b>{v}</b>},
    {title:'Count-0', dataIndex:'c0', width:80, render:v=><span className="mono">{v}</span>},
    {title:'Count-1', dataIndex:'c1', width:80, render:v=><span className="mono">{v}</span>},
    {title:'Expected-0', width:100, render:(_,r)=><span className="mono">{fmt(r.e0,2)}</span>},
    {title:'Expected-1', width:100, render:(_,r)=><span className="mono">{fmt(r.e1,2)}</span>},
    {title:'Po', width:80, render:(_,r)=><span className="mono">{fmt(100*r.po,1)}%</span>},
    {title:'Pe', width:80, render:(_,r)=><span className="mono">{fmt(100*r.pe,1)}%</span>},
    {title:'KAPPA', width:90, render:(_,r)=><b className="mono">{fmt(r.kappa,2)}</b>}
  ];
  return <Drawer title={<Space>{rec.id} · {rec.instName}<StatusTag s={rec.reviewStatus}/><VerdictTag v={rec.conclusion}/></Space>} width={1100} open onClose={onClose} extra={reviewBtns}>
    <div className={"verdict-banner "+(level===0?'verdict-accept':level===1?'verdict-cond':'verdict-reject')}>
      <Space><b style={{fontSize:16}}>{banner.t}</b><span className="tiny">判定依据：{calc.reasons.join('；')}</span></Space>
    </div>
    <Descriptions column={4} size="small" bordered className="mt12" items={[
      {key:'表单编号', label:'表单编号', children:<span className="mono">GJZ-MSA-KPA-{rec.id}</span>},
      {key:'关联计划', label:'关联计划', children:<span className="row-link mono" onClick={()=>NavAPI.go('plan')}>{rec.planId||'暂无'}</span>},
      {key:'料号/产品代码', label:'料号/产品代码', children:<span className="mono">{plan?plan.partNo:'暂无'}</span>},
      {key:'品名规格', label:'品名规格', children:plan?plan.partName:'暂无'},
      {key:'器具编号', label:'器具编号', children:<span className="mono">{rec.instId||'暂无'}</span>},
      {key:'器具名称', label:'器具名称', children:inst?inst.name:'暂无'},
      {key:'量具类型', label:'量具类型', children:inst?inst.cat:'暂无'},
      {key:'测量对象', label:'测量对象', children:rec.object},
      {key:'特性说明', label:'特性说明', children:'判定值 1=合格 / 0=不合格，盲测独立判定'},
      {key:'检验标准', label:'检验标准', children:<span className="mono">{rec.standard||'暂无'}</span>},
      {key:'样本组', label:'样本组', children:<span className="mono">{rec.sampleGroup||'暂无'}</span>},
      {key:'人数', label:'人数', children:rec.numApp+' 人'},
      {key:'零件数', label:'零件数', children:rec.numSamples+' 件'},
      {key:'次数', label:'次数', children:(rec.numTrials||3)+' 次/件'},
      {key:'检验员', label:'检验员', children:(rec.appNames||[]).join('、')},
      {key:'测量者A·B·C', label:'测量者A·B·C', children:(rec.appNames||[]).map((n,i)=>(i>0?' / ':'')+n)},
      {key:'分析人', label:'分析人', children:rec.analyst||'暂无'},
      {key:'分析日期', label:'分析日期', children:rec.analysisDate||'暂无'}
    ]}/>
    <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>逐样本两两一致性（D=一致，字母=不一致方；Self=该检验员多次判定一致性）</span></div>
      <Table size="small" rowKey="i" dataSource={srows} columns={sampleCols} pagination={false} scroll={{x:640,y:280}}/>
    </div>
    {calc && <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>汇总评估</span>
        <div className="kpi-row">
          <div className="kpi-item"><div className="k">总体 KAPPA</div><div className="v" style={{color:calc.overall.kappa>=0.75?'#16a34a':calc.overall.kappa>=0.4?'#d97706':'#dc2626'}}>{fmt(calc.overall.kappa,2)}</div><div className="tiny">≥0.75 可接受</div></div>
          <div className="kpi-item"><div className="k">总体有效性</div><div className="v" style={{color:calc.overall.effectiveness>=90?'inherit':calc.overall.effectiveness>=80?'#d97706':'#dc2626'}}>{fmt(calc.overall.effectiveness,1)}%</div><div className="tiny">≥90% 可接受</div></div>
          <div className="kpi-item"><div className="k">错误率(漏判)</div><div className="v" style={{color:calc.overall.missRate>5?'#dc2626':calc.overall.missRate>2?'#d97706':'inherit'}}>{fmt(calc.overall.missRate,1)}%</div><div className="tiny">≤2% 可接受</div></div>
          <div className="kpi-item"><div className="k">错误警报率(误判)</div><div className="v" style={{color:calc.overall.falseAlarm>10?'#dc2626':calc.overall.falseAlarm>5?'#d97706':'inherit'}}>{fmt(calc.overall.falseAlarm,1)}%</div><div className="tiny">≤5% 可接受</div></div>
        </div>
      </div>
      <div className="grp-label">各检验员 vs 参照判定（有效性/漏判/误判）</div>
      <Table size="small" rowKey="name" dataSource={calc.per} columns={perCols} pagination={false}/>
      {calc.self && calc.self.length>0 && <div className="grp-label">重复性 %Appraiser（自评：多次试验两两一致性）</div>}
      {calc.self && calc.self.length>0 && <Table size="small" rowKey="name" dataSource={calc.self} columns={selfCols} pagination={false}/>}
      <div className="grp-label">检验员间两两一致性（逐对 Kappa）</div>
      <Table size="small" rowKey="label" dataSource={calc.pairs} columns={pairCols} pagination={false}/>
    </div>}
    <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>2×2 列联表（Data Summary：0=不合格 1=合格，行×列）</span></div>
      <Table size="small" rowKey="label" pagination={false} dataSource={pairs6} columns={table2x2Cols}/>
    </div>
    <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>交叉表 Crosstabulation（Count / Expected / Po / Pe）</span></div>
      <Table size="small" rowKey="label" pagination={false} dataSource={crosstab} columns={ctCols}/>
    </div>
    {calc && <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>判定准则（业务计数型三档表）</span></div>
      <Table size="small" rowKey="d" pagination={false} dataSource={[
        {d:'评价人可接受', k:'Kappa ≥0.75', e:'有效性 ≥90%', m:'错误率 ≤2%', f:'错误警报率 ≤5%'},
        {d:'可接受边缘-可能需改进', k:'Kappa 0.40~0.75', e:'有效性 80%~90%', m:'错误率 2%~5%', f:'错误警报率 5%~10%'},
        {d:'不可接受-需改进', k:'Kappa <0.40', e:'有效性 <80%', m:'错误率 >5%', f:'错误警报率 >10%'}
      ]} columns={[
        {title:'判定档位', dataIndex:'d', width:220},
        {title:'Kappa', dataIndex:'k', width:140},
        {title:'有效性', dataIndex:'e', width:130},
        {title:'错误率(漏判)', dataIndex:'m', width:120},
        {title:'错误警报率(误判)', dataIndex:'f', width:140}
      ]}/>
    </div>}
    <div className="panel mt12" style={{marginBottom:0}}>
      <div className="panel-title"><span className="t"><span className="bar"/>审批栏</span></div>
      <Table size="small" rowKey="r" pagination={false} dataSource={[
        {r:'拟制', name:rec.analyst||'—', date:rec.analysisDate||'—'},
        {r:'审核', name:rec.reviewer||'待审核', date:rec.reviewDate||'—'},
        {r:'批准', name:rec.approver||'待批准', date:rec.approveDate||'—'}
      ]} columns={[
        {title:'签署', dataIndex:'r', width:120, render:v=><b>{v}</b>},
        {title:'姓名', dataIndex:'name', width:220},
        {title:'日期', dataIndex:'date', width:160}
      ]}/>
    </div>
    {rec.actions && rec.actions.length>0 && <div className="grp-label">纠正措施 / 整改跟踪</div>}
    {rec.actions && rec.actions.map((a,i)=><Alert key={i} type={a.status==='已完成'?'success':'warning'} showIcon style={{marginBottom:8}}
      message={<Space><Tag color={a.status==='已完成'?'green':'orange'}>{a.status}</Tag><b>{a.type}</b></Space>}
      description={<span>{a.content} ｜ 责任人：{a.owner} ｜ 计划完成：{a.planDate}{a.note?' ｜ '+a.note:''}</span>}/>)}

    {actionModal && <Modal title="添加纠正措施" open onCancel={()=>setActionModal(false)} footer={null} destroyOnClose>
      <ActionForm onSubmit={(vals)=>{ mut(s=>{const g=s.kappa.find(x=>x.id===rec.id); g.actions.push({...vals,status:'进行中'}); logAction(s.me.name,'添加纠正措施',g.id,vals.content); }); setActionModal(false); toast.ok('措施已登记'); }}/>
    </Modal>}
  </Drawer>;
}
"""

i = s.find('function KappaDetail({rec,onClose}){')
j = s.find('/* ================= 设计说明（评审依据） ================= */')
assert i > 0 and j > i, '定位失败 %d %d' % (i, j)
s = s[:i] + NEW_DETAIL + '\n' + s[j:]

# ---------- KappaPage 列表加「逐对KAPPA」列 ----------
old_col = "{title:'总体KAPPA', width:100, render:(_,r)=>{const c=calcKappaRec(r);return c?<b>{fmt(c.overall.kappa,2)}</b>:'暂无'}},"
new_col = """{title:'总体KAPPA', width:100, render:(_,r)=>{const c=calcKappaRec(r);return c?<b>{fmt(c.overall.kappa,2)}</b>:'暂无'}},
    {title:'逐对KAPPA', width:170, render:(_,r)=>{const c=calcKappaRec(r); if(!c||!c.pairs.length) return '暂无'; return <span className="tiny">{c.pairs.map(p=>p.label.replace(' ↔ ','×')+' '+fmt(p.kappa,2)).join(' / ')}</span>;}},"""
assert s.count(old_col) == 1, 'kappa-page col 命中 %d' % s.count(old_col)
s = s.replace(old_col, new_col)

open(P, 'w', encoding='utf-8').write(s)
print('batch3c OK 长度', len(s))
