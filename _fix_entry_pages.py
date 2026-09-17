# -*- coding: utf-8 -*-
"""按分析方法拆分取数/录入与结果展示：
1) 新增「取数录入」组 5 个独立页面（GRR/KAPPA/线性偏移/稳定性/CgCgk），复用 GrrEntry/KappaEntry/AnlEntry 页面内嵌
2) 原台账页转为「XX 分析结果」展示页（列表+详情+审核）
3) 转定型/详情分析单号跳转指向取数页（待采集自动开录入；已采集跳结果页详情）
4) 分辨率分析保留原样（不拆分）
"""
import io
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# 1) MENU：新增 5 个取数录入菜单 + 结果页改名
rep("""  {key:'sample', icon:'⬡', label:'样本管理', group:'MSA 管理'},
  {key:'grr', icon:'◔', label:'GRR 台账', group:'分析执行'},
  {key:'kappa', icon:'✓', label:'KAPPA 台账', group:'分析执行'},
  {key:'anl_linear', icon:'↗', label:'线性/偏移分析', group:'分析执行'},
  {key:'anl_stability', icon:'≋', label:'稳定性分析', group:'分析执行'},
  {key:'anl_cgcgk', icon:'⊞', label:'Cg/Cgk 分析', group:'分析执行'},
  {key:'anl_resolution', icon:'⊕', label:'分辨率分析', group:'分析执行'}
];""",
"""  {key:'sample', icon:'⬡', label:'样本管理', group:'MSA 管理'},
  {key:'entry_grr', icon:'⌗', label:'GRR 取数录入', group:'取数录入'},
  {key:'entry_kappa', icon:'⌗', label:'KAPPA 取数录入', group:'取数录入'},
  {key:'entry_linear', icon:'⌗', label:'线性/偏移取数录入', group:'取数录入'},
  {key:'entry_stability', icon:'⌗', label:'稳定性取数录入', group:'取数录入'},
  {key:'entry_cgcgk', icon:'⌗', label:'Cg/Cgk 取数录入', group:'取数录入'},
  {key:'grr', icon:'◔', label:'GRR 分析结果', group:'分析执行'},
  {key:'kappa', icon:'✓', label:'KAPPA 分析结果', group:'分析执行'},
  {key:'anl_linear', icon:'↗', label:'线性/偏移分析结果', group:'分析执行'},
  {key:'anl_stability', icon:'≋', label:'稳定性分析结果', group:'分析执行'},
  {key:'anl_cgcgk', icon:'⊞', label:'Cg/Cgk 分析结果', group:'分析执行'},
  {key:'anl_resolution', icon:'⊕', label:'分辨率分析', group:'分析执行'}
];""")

# 2) PAGE_TITLE
rep("""  'standard':'MSA 检验标准维护','sample':'样本管理','grr':'GRR 台账（计量型变差分析）',
  'kappa':'KAPPA 台账（计数型一致性分析）','anl_linear':'线性/偏移性分析台账','anl_stability':'稳定性分析台账','anl_cgcgk':'Cg/Cgk 分析台账（VDA Type1）','anl_resolution':'分辨率分析台账'};""",
"""  'standard':'MSA 检验标准维护','sample':'样本管理',
  'entry_grr':'GRR 取数录入','entry_kappa':'KAPPA 取数录入','entry_linear':'线性/偏移取数录入','entry_stability':'稳定性取数录入','entry_cgcgk':'Cg/Cgk 取数录入',
  'grr':'GRR 分析结果','kappa':'KAPPA 分析结果','anl_linear':'线性/偏移分析结果','anl_stability':'稳定性分析结果','anl_cgcgk':'Cg/Cgk 分析结果（VDA Type1）','anl_resolution':'分辨率分析'};""")

# 3) NavAPI 跳转：GRR/KAPPA/其他方法 -> 对应取数页（分辨率除外）
rep("""  NavAPI.openGrr = (id)=>{ GrrOpenId=id; setPage('grr'); };
  NavAPI.openKappa = (id)=>{ KpaOpenId=id; setPage('kappa'); };
  NavAPI.openAnl = (kind,id)=>{ AnlOpen={kind,id}; setPage(ANA_PAGE[kind]); };""",
"""  NavAPI.openGrr = (id)=>{ EntryOpen={kind:'grr',id}; setPage('entry_grr'); };
  NavAPI.openKappa = (id)=>{ EntryOpen={kind:'kappa',id}; setPage('entry_kappa'); };
  NavAPI.openAnl = (kind,id)=>{ if(kind==='resolution'){ AnlOpen={kind,id}; setPage('anl_resolution'); } else { EntryOpen={kind,id}; setPage(ENTRY_PAGE[kind]); } };""")

# 4) App renderPage 增加 5 个取数页分发
rep("""    if(page==='grr') return <GrrPage/>;
    if(page==='kappa') return <KappaPage/>;""",
"""    if(page==='entry_grr') return <EntryPage kind="grr"/>;
    if(page==='entry_kappa') return <EntryPage kind="kappa"/>;
    if(page==='entry_linear') return <EntryPage kind="linear"/>;
    if(page==='entry_stability') return <EntryPage kind="stability"/>;
    if(page==='entry_cgcgk') return <EntryPage kind="cgcgk"/>;
    if(page==='grr') return <GrrPage/>;
    if(page==='kappa') return <KappaPage/>;""")

# 5) anlOpenRec / recJump：非分辨率跳取数页
rep("""function anlOpenRec(kind,id){ AnlOpen={kind,id}; NavAPI.go(ANA_PAGE[kind]); }""",
"""function anlOpenRec(kind,id){ if(kind==='resolution'){ AnlOpen={kind,id}; NavAPI.go('anl_resolution'); } else { EntryOpen={kind,id}; NavAPI.go(ENTRY_PAGE[kind]); } }""")

# 6) doConvert 跳转：记录首条记录 id，跳对应取数页并自动打开录入
rep("""        let rid='';
        instIds.forEach(iid=>{
          const inst=s.instruments.find(i=>i.id===iid);
          rid=spawnRecord(s, p.id, { type:t, standard:std.id, method:ENUM.taskMethod[t][0], params,
            object:p.object, instId:iid, instName:inst?inst.name:'', owner:p.owner||s.me.name, note:'顶部按钮转 '+t+'，待台账内录入数据' });
        });""",
"""        let rid=''; if(!firstRid) firstRid='';
        instIds.forEach(iid=>{
          const inst=s.instruments.find(i=>i.id===iid);
          rid=spawnRecord(s, p.id, { type:t, standard:std.id, method:ENUM.taskMethod[t][0], params,
            object:p.object, instId:iid, instName:inst?inst.name:'', owner:p.owner||s.me.name, note:'顶部按钮转 '+t+'，待取数录入页录入数据' });
          if(!firstRid) firstRid=rid;
        });""")
rep("""    let done=0, skipped=0;
    mut(s=>{""",
"""    let done=0, skipped=0, firstRid='';
    mut(s=>{""")
rep("""    if(done) toast.ok('已转 '+t+' '+done+' 个计划（生成台账记录），跳转 '+(t==='GRR'?'GRR':'KAPPA')+' 台账');
    if(skipped) toast.warn(skipped+' 个计划已存在台账记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    NavAPI.go(t==='GRR'?'grr':'kappa');""",
"""    if(done) toast.ok('已转 '+t+' '+done+' 个计划（生成台账待采集记录），跳转 '+(t==='GRR'?'GRR':'KAPPA')+' 取数录入');
    if(skipped) toast.warn(skipped+' 个计划已存在台账记录或缺少匹配检验标准，未重复转换');
    setSelectedRowKeys([]);
    if(firstRid){ t==='GRR'? NavAPI.openGrr(firstRid) : NavAPI.openKappa(firstRid); }
    else NavAPI.go(t==='GRR'?'entry_grr':'entry_kappa');""")

# 7) 新增 ENTRY_PAGE / EntryOpen / EntryPage（插在 AnlEntry 结束、GrrPage 之前）
entry_block = r'''
/* ================= 取数录入页（5 套：按分析方法独立页面） ================= */
const ENTRY_PAGE = { grr:'entry_grr', kappa:'entry_kappa', linear:'entry_linear', stability:'entry_stability', cgcgk:'entry_cgcgk' };
let EntryOpen=null;
function EntryPage({kind}){
  const CFG=ENTRY_CFG[kind];
  const d=Store.get();
  const [entryRec,setEntryRec]=useState(null);
  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);
  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});
  const rows=(d[CFG.arr]||[]).filter(r=>
    (!q.kw || (r.id+r.planId+r.instId+r.instName+r.object).toLowerCase().includes(q.kw.toLowerCase())) &&
    (!q.status || r.reviewStatus===q.status) &&
    (!q.concl || (r.conclusion||'').indexOf(q.concl)>=0));
  const resetQ=()=>{ setFkw('');setFstatus(undefined);setFconcl(undefined); setQ({kw:'',status:undefined,concl:undefined}); };
  // 外部跳转（转定型 / 详情分析单号）：待采集 → 直接打开录入面板；已采集 → 跳结果页打开详情
  useEffect(()=>{ if(EntryOpen && EntryOpen.kind===kind){
    const rec=(d[CFG.arr]||[]).find(g=>g.id===EntryOpen.id);
    if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else goResult(rec); }
    EntryOpen=null;
  }},[]);
  const goResult=(r)=>{ if(kind==='grr'){ GrrOpenId=r.id; NavAPI.go('grr'); } else if(kind==='kappa'){ KpaOpenId=r.id; NavAPI.go('kappa'); } else { AnlOpen={kind,id:r.id}; NavAPI.go(CFG.result); } };
  const recParams=(r)=> kind==='grr'? (r.numOps+'人 × '+r.numTrials+'次 × '+r.numParts+'件') : kind==='kappa'? (r.numApp+'人 × '+r.numSamples+'件') : ANA_CFG[kind].params(r);
  const cols=[
    {title:'操作', width:200, fixed:'left', render:(_,r)=><Space size={0}>
      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>goResult(r)}>查看结果</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},
    {title:CFG.idPref+'编号', dataIndex:'id', width:115, render:(v,r)=><span className="row-link mono" onClick={()=>goResult(r)}>{v}</span>},
    {title:'关联计划', dataIndex:'planId', width:110, render:(v)=><span className="row-link mono" onClick={()=>NavAPI.go('plan')}>{v||'-'}</span>},
    {title:'器具名称', width:150, render:(_,r)=>{ const it=d.instruments.find(i=>i.id===r.instId); return <span>{it?it.name:r.instName}</span>; }, ellipsis:true},
    {title:'测量对象', dataIndex:'object', width:170, ellipsis:true},
    {title:'取样规则', width:170, render:(_,r)=><span className="tiny">{recParams(r)}</span>},
    {title:'标准', dataIndex:'standard', width:105, render:v=><span className="mono tiny">{v||'-'}</span>},
    {title:'结论', width:120, render:(_,r)=><VerdictTag v={r.conclusion||'-'}/>},
    {title:'状态', width:90, render:(_,r)=><StatusTag s={r.reviewStatus}/>},
    {title:'分析人', dataIndex:'analyst', width:90}
  ];
  return <div>
    <Panel title="查询条件">
      <Space wrap>
        <Input.Search allowClear placeholder={CFG.idPref+'编号 / 关联计划 / 器具 / 测量对象'} style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>
        <Select allowClear placeholder="记录状态" style={{width:140}} value={fstatus} options={['待采集','待审核','已批准','需整改','已闭环','已关闭'].map(c=>({value:c,label:c}))} onChange={setFstatus}/>
        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={['可接受','有条件','不可接受'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>
        <span className="tiny">共 {rows.length} 条</span>
      </Space>
    </Panel>
    <Panel title="操作">
      <Space wrap>
        <Button type="primary" onClick={()=>setQ({kw:fkw,status:fstatus,concl:fconcl})}>查询</Button>
        <Button onClick={resetQ}>重置</Button>
        <Button disabled={!canDo(d.me.role,'edit')}>导出</Button>
        <span className="tiny">查询 / 重置 在最前；{CFG.name}取数录入：{CFG.desc}；「待采集」记录在此录入，提交后自动计算分析项并跳转「{CFG.name}分析结果」审核闭环。</span>
      </Space>
    </Panel>
    {!entryRec && <Panel title={CFG.title+' · 记录列表（'+rows.length+' 条）'}>
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:1320}} pagination={false}/>
    </Panel>}
    {entryRec && <Panel title={<span>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s="待采集"/></span>}
      extra={<Button size="small" onClick={()=>setEntryRec(null)}>收起列表</Button>}>
      {CFG.entry(entryRec, ()=>{ setEntryRec(null); })}
    </Panel>}
  </div>;
}
const ENTRY_CFG = {
  grr:{arr:'grr', idPref:'GRR', name:'GRR', title:'GRR 取数录入', desc:'交叉型矩阵：操作员 × 样本 × 试验', entry:(r,c)=><GrrEntry rec={r} onClose={c}/>, result:'grr'},
  kappa:{arr:'kappa', idPref:'KAPPA', name:'KAPPA', title:'KAPPA 取数录入', desc:'检验员判定矩阵（合格/不合格，盲测）', entry:(r,c)=><KappaEntry rec={r} onClose={c}/>, result:'kappa'},
  linear:{arr:'linear', idPref:'LIN', name:'线性/偏移', title:'线性/偏移取数录入', desc:'标准件测量（覆盖量程 0/25/50/75/100%）', entry:(r,c)=><AnlEntry rec={r} kind="linear" onClose={c}/>, result:'anl_linear'},
  stability:{arr:'stability', idPref:'STB', name:'稳定性', title:'稳定性取数录入', desc:'子组测量（跨 4 周~3 个月，SPC 判异）', entry:(r,c)=><AnlEntry rec={r} kind="stability" onClose={c}/>, result:'anl_stability'},
  cgcgk:{arr:'cgcgk', idPref:'CG', name:'Cg/Cgk', title:'Cg/Cgk 取数录入', desc:'标准件连续测量（VDA Type1）', entry:(r,c)=><AnlEntry rec={r} kind="cgcgk" onClose={c}/>, result:'anl_cgcgk'},
};
'''
anchor = 'function GrrPage(){'
rep(anchor, entry_block + '\n' + anchor)

# 8) GrrPage：录入按钮 -> 去录入（跳取数页）；标题/说明更新（结尾 `</Space>}` 独立行）
rep("""      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button>
    </Space>},""",
"""      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>{ EntryOpen={kind:'grr',id:r.id}; NavAPI.go('entry_grr'); }}>去录入</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button>
    </Space>},""")
rep('<Panel title="GRR 台账列表">', '<Panel title="GRR 分析结果列表">')
rep("""<span className="tiny">查询 / 重置 在最前；GRR 记录由 MSA 计划定型自动生成，样本数据在台账行内录入并提交审核；不合格进入整改-复测-闭环。判定标准：%GRR&lt;10% 可接受；10%~30% 有条件；&gt;30% 不可接受；NDC≥5。</span>""",
"""<span className="tiny">查询 / 重置 在最前；GRR 记录由 MSA 计划定型自动生成，「待采集」记录在「GRR 取数录入」页录入并提交审核；不合格进入整改-复测-闭环。判定标准：%GRR&lt;10% 可接受；10%~30% 有条件；&gt;30% 不可接受；NDC≥5。</span>""")

# 9) KappaPage：录入按钮 -> 去录入；标题/说明更新（详情+器具同行）
rep("""      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button><Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},""",
"""      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>{ EntryOpen={kind:'kappa',id:r.id}; NavAPI.go('entry_kappa'); }}>去录入</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button><Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},""")
rep('<Panel title="KAPPA 台账列表">', '<Panel title="KAPPA 分析结果列表">')
rep("""<span className="tiny">查询 / 重置 在最前；KAPPA 记录由 MSA 计划定型自动生成，判定数据在台账行内录入并提交审核。判定标准：KAPPA&gt;0.75 优秀；0.40~0.75 良好（有条件）；&lt;0.40 不可接受；有效性≥90%、漏判≤2%、误判≤5%。</span>""",
"""<span className="tiny">查询 / 重置 在最前；KAPPA 记录由 MSA 计划定型自动生成，「待采集」记录在「KAPPA 取数录入」页录入并提交审核。判定标准：KAPPA&gt;0.75 优秀；0.40~0.75 良好（有条件）；&lt;0.40 不可接受；有效性≥90%、漏判≤2%、误判≤5%。</span>""")

# 10) AnlPage：非分辨率 录入按钮 -> 去录入（跳取数页）；标题/说明更新（`</Space>}` 与器具同行）
rep("""      {r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},""",
"""      {kind!=='resolution' && r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>{ EntryOpen={kind,id:r.id}; NavAPI.go(ENTRY_PAGE[kind]); }}>去录入</Button>}
      {kind==='resolution' && r.reviewStatus==='待采集' && <Button size="small" type="primary" ghost disabled={!canDo(d.me.role,'edit')} onClick={()=>setEntryRec(r)}>录入数据</Button>}
      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情/审核</Button>
      <Button size="small" type="link" onClick={()=>NavAPI.openInst(r.instId)}>器具</Button></Space>},""")
rep("<Panel title={CFG.name+'分析台账（'+rows.length+' 条）'}>", "<Panel title={CFG.name+'分析结果列表（'+rows.length+' 条）'}>")
rep("""<span className="tiny">查询 / 重置 在最前；{CFG.name}分析记录由 MSA 计划按分析方法自动生成（一器一计划一方法），取样规则固化：{CFG.params(rows[0]||{stds:5,per:10,groups:25,runs:50})}；录入表单按规则自动生成默认行数，可增减。</span>""",
"""<span className="tiny">查询 / 重置 在最前；{CFG.name}分析记录由 MSA 计划按分析方法自动生成（一器一计划一方法），取样规则固化：{CFG.params(rows[0]||{stds:5,per:10,groups:25,runs:50})}；{kind==='resolution'? '分辨率不取样，直接录入' : '「待采集」记录在对应「取数录入」页录入'}。</span>""")

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
