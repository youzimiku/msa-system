# -*- coding: utf-8 -*-
"""Step3：需求3 台账/录入拆页"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s
log = []

def rep(old, new, expect=None, tag=''):
    global s
    n = s.count(old)
    if expect is not None and n != expect:
        log.append('FAIL[%s] count=%d expect=%d :: %s' % (tag, n, expect, old[:60]))
        return
    s = s.replace(old, new)
    log.append('OK[%s] x%d' % (tag, n))

# ---- 1) EntryOpen 声明 -> DataOpen ----
rep("let EntryOpen=null;", "let DataOpen=null;", 1, 'DataOpen声明')

# ---- 2) NavAPI 注入（智能分派：待采集→录入数据页；已采集→结果页详情） ----
rep("NavAPI.openGrr = (id)=>{ EntryOpen={kind:'grr',id}; setPage('entry_grr'); };",
    "NavAPI.openGrr = (id)=>{ const rec=Store.data.grr.find(g=>g.id===id); if(rec&&rec.reviewStatus==='待采集'){ DataOpen={kind:'grr',id}; setPage('data_grr'); } else { GrrOpenId=id; setPage('grr'); } };", 1, 'openGrr')
rep("NavAPI.openKappa = (id)=>{ EntryOpen={kind:'kappa',id}; setPage('entry_kappa'); };",
    "NavAPI.openKappa = (id)=>{ const rec=Store.data.kappa.find(g=>g.id===id); if(rec&&rec.reviewStatus==='待采集'){ DataOpen={kind:'kappa',id}; setPage('data_kappa'); } else { KpaOpenId=id; setPage('kappa'); } };", 1, 'openKappa')
rep("NavAPI.openAnl = (kind,id)=>{ if(kind==='resolution'){ AnlOpen={kind,id}; setPage('anl_resolution'); } else { EntryOpen={kind,id}; setPage(ENTRY_PAGE[kind]); } };",
    "NavAPI.openAnl = (kind,id)=>{ if(kind==='resolution'){ AnlOpen={kind,id}; setPage('anl_resolution'); } else { const rec=(Store.data[ANA_CFG[kind].arr]||[]).find(g=>g.id===id); if(rec&&rec.reviewStatus==='待采集'){ DataOpen={kind,id}; setPage('data_'+kind); } else { AnlOpen={kind,id}; setPage(ANA_PAGE[kind]); } } };", 1, 'openAnl')

# ---- 3) EntryPage：去掉录入面板与 EntryOpen，行内跳录入数据页 ----
old_ep1 = """  const [entryRec,setEntryRec]=useState(null);
  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);"""
new_ep1 = """  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);"""
rep(old_ep1, new_ep1, 1, 'EntryPage state')

old_ep2 = """  // 外部跳转（转定型 / 详情分析单号）：待采集 → 直接打开录入面板；已采集 → 跳结果页打开详情
  useEffect(()=>{ if(EntryOpen && EntryOpen.kind===kind){
    const rec=(d[CFG.arr]||[]).find(g=>g.id===EntryOpen.id);
    if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else goResult(rec); }
    EntryOpen=null;
  }},[]);
"""
rep(old_ep2, "", 1, 'EntryPage useEffect')

rep("onClick={()=>setEntryRec(r)}>录入数据</Button>}",
    "onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>录入数据</Button>}", 1, 'EntryPage录入按钮')

old_ep3 = """    {!entryRec && <Panel title={CFG.title+' · 记录列表（'+rows.length+' 条）'}>
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:1320}} pagination={false}/>
    </Panel>}
    {entryRec && <Panel title={<span>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s="待采集"/></span>}
      extra={<Button size="small" onClick={()=>setEntryRec(null)}>收起列表</Button>}>
      {CFG.entry(entryRec, ()=>{ setEntryRec(null); })}
    </Panel>}"""
new_ep3 = """    <Panel title={CFG.title+' · 记录列表（'+rows.length+' 条）'}>
      <Table rowKey="id" size="middle" dataSource={rows} columns={cols} scroll={{x:1320}} pagination={false}/>
    </Panel>"""
rep(old_ep3, new_ep3, 1, 'EntryPage列表')

rep("「待采集」记录在此录入，提交后自动计算分析项并跳转「{CFG.name}分析结果」审核闭环。",
    "「待采集」记录请到「{CFG.name}录入数据」页录入，提交后自动计算分析项并跳转「{CFG.name}分析结果」审核闭环。", 1, 'EntryPage说明')

# EntryPage 结论列：VerdictTag 兜底
rep("<VerdictTag v={r.conclusion||'暂无'}/>", "<VerdictTag v={r.conclusion}/>", 1, 'EntryPage结论列')

# ---- 4) DataEntryPage 新增（插在 EntryPage 结束与 ENTRY_CFG 之间） ----
data_page = '''
function DataEntryPage({kind}){
  const CFG=ENTRY_CFG[kind];
  const d=Store.get();
  const [rec,setRec]=useState(()=>{
    if(DataOpen && DataOpen.kind===kind){ const r=(d[CFG.arr]||[]).find(g=>g.id===DataOpen.id); DataOpen=null; if(r) return r; }
    return (d[CFG.arr]||[]).find(g=>g.reviewStatus==='待采集')||null;
  });
  const pending=(d[CFG.arr]||[]).filter(r=>r.reviewStatus==='待采集');
  const [selId,setSelId]=useState(rec?rec.id:null);
  const cur=rec || (d[CFG.arr]||[]).find(g=>g.id===selId) || null;
  const gotoList=()=>NavAPI.go('entry_'+kind);
  const onPicked=(id)=>{ const r=(d[CFG.arr]||[]).find(g=>g.id===id); if(r){ setRec(r); setSelId(id); } };
  return <div>
    <PageHead title={CFG.title+' · 数据录入'} sub={'台账列表在「'+CFG.name+'台账」页；此处选择待采集记录录入样本并提交分析'} extra={<Space><Button onClick={gotoList}>返回台账</Button></Space>}/>
    <Panel title="选择待采集记录">
      <Space wrap>
        <Select style={{width:300}} value={cur?cur.id:undefined} placeholder={'选择要录入的'+CFG.name+'记录'} options={pending.map(r=>({value:r.id,label:r.id+' · '+r.instName+' · '+r.object}))} onChange={onPicked}/>
        <span className="tiny">共 {pending.length} 条待采集记录；提交后自动计算分析项并跳转「{CFG.name}分析结果」审核。</span>
      </Space>
    </Panel>
    {cur ? <Panel title={<span>{cur.id} · {cur.instName} · {CFG.name} 数据录入<StatusTag s="待采集"/></span>} extra={<Button size="small" onClick={gotoList}>返回台账</Button>}>
      {CFG.entry(cur, ()=>{ toast.ok('已提交，请在「'+CFG.name+'分析结果」页审核'); NavAPI.go(CFG.result); })}
    </Panel> : <Panel title="暂无待采集记录"><span>当前没有待采集的{CFG.name}记录。可先在「MSA 计划」页创建计划并转定型生成，或到「{CFG.name}台账」页查看已有记录。</span></Panel>}
  </div>;
}
'''
anchor = "\nconst ENTRY_CFG = {"
rep(anchor, data_page + anchor, 1, 'DataEntryPage')

# ---- 5) GrrPage ----
rep("const [detail,setDetail]=useState(null);   const [entryRec,setEntryRec]=useState(null); // 待采集记录 → 台账内录入   const [fkw,setFkw]=useState",
    "const [detail,setDetail]=useState(null);   const [fkw,setFkw]=useState", 1, 'GrrPage state')
rep("if(GrrOpenId){ const rec=d.grr.find(g=>g.id===GrrOpenId); if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else setDetail(rec); } GrrOpenId=null; }",
    "if(GrrOpenId){ const rec=d.grr.find(g=>g.id===GrrOpenId); if(rec){ if(rec.reviewStatus==='待采集'){ DataOpen={kind:'grr',id:rec.id}; NavAPI.go('data_grr'); } else setDetail(rec); } GrrOpenId=null; }", 1, 'GrrPage useEffect')
rep("onClick={()=>{ EntryOpen={kind:'grr',id:r.id}; NavAPI.go('entry_grr'); }}>去录入</Button>",
    "onClick={()=>{ DataOpen={kind:'grr',id:r.id}; NavAPI.go('data_grr'); }}>去录入</Button>", 1, 'GrrPage录入按钮')
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · GRR 数据录入<StatusTag s=\"待采集\"/></Space>} width={1000} open onClose={()=>setEntryRec(null)}>       <GrrEntry rec={entryRec} onClose={()=>setEntryRec(null)}/>     </Drawer>}",
    "", 1, 'GrrPage删Drawer')

# ---- 6) KappaPage ----
rep("const [detail,setDetail]=useState(null);   const [entryRec,setEntryRec]=useState(null); // 待采集记录 → 台账内录入   const [fkw,setFkw]=useState",
    "const [detail,setDetail]=useState(null);   const [fkw,setFkw]=useState", 1, 'KappaPage state')
rep("if(KpaOpenId){ const rec=d.kappa.find(k=>k.id===KpaOpenId); if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else setDetail(rec); } KpaOpenId=null; }",
    "if(KpaOpenId){ const rec=d.kappa.find(k=>k.id===KpaOpenId); if(rec){ if(rec.reviewStatus==='待采集'){ DataOpen={kind:'kappa',id:rec.id}; NavAPI.go('data_kappa'); } else setDetail(rec); } KpaOpenId=null; }", 1, 'KappaPage useEffect')
rep("onClick={()=>{ EntryOpen={kind:'kappa',id:r.id}; NavAPI.go('entry_kappa'); }}>去录入</Button>",
    "onClick={()=>{ DataOpen={kind:'kappa',id:r.id}; NavAPI.go('data_kappa'); }}>去录入</Button>", 1, 'KappaPage录入按钮')
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · KAPPA 判定数据录入<StatusTag s=\"待采集\"/></Space>} width={1000} open onClose={()=>setEntryRec(null)}>       <KappaEntry rec={entryRec} onClose={()=>setEntryRec(null)}/>     </Drawer>}",
    "", 1, 'KappaPage删Drawer')

# ---- 7) AnlPage ----
rep("const [detail,setDetail]=useState(null);   const [entryRec,setEntryRec]=useState(null);   const [fkw,setFkw]=useState",
    "const [detail,setDetail]=useState(null);   const [fkw,setFkw]=useState", 1, 'AnlPage state')
rep("if(AnlOpen && AnlOpen.kind===kind){ const rec=(d[CFG.arr]||[]).find(g=>g.id===AnlOpen.id); if(rec){ if(rec.reviewStatus==='待采集') setEntryRec(rec); else setDetail(rec); } AnlOpen=null; }",
    "if(AnlOpen && AnlOpen.kind===kind){ const rec=(d[CFG.arr]||[]).find(g=>g.id===AnlOpen.id); if(rec){ if(rec.reviewStatus==='待采集'){ if(kind==='resolution') setDetail(rec); else { DataOpen={kind,id:rec.id}; NavAPI.go('data_'+kind); } } else setDetail(rec); } AnlOpen=null; }", 1, 'AnlPage useEffect')
rep("onClick={()=>{ EntryOpen={kind,id:r.id}; NavAPI.go(ENTRY_PAGE[kind]); }}>去录入</Button>",
    "onClick={()=>{ DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind); }}>去录入</Button>", 1, 'AnlPage去录入')
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s=\"待采集\"/></Space>} width={kind==='stability'?1220:(kind==='cgcgk'?820:1000)} open onClose={()=>setEntryRec(null)}>       <AnlEntry rec={entryRec} kind={kind} onClose={()=>setEntryRec(null)}/>     </Drawer>}",
    "{kind==='resolution' && entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s=\"待采集\"/></Space>} width={kind==='stability'?1220:(kind==='cgcgk'?820:1000)} open onClose={()=>setEntryRec(null)}>       <AnlEntry rec={entryRec} kind={kind} onClose={()=>setEntryRec(null)}/>     </Drawer>}", 1, 'AnlPage Drawer')
# AnlPage 操作区说明
rep("「待采集」记录在对应「台账」页录入", "「待采集」记录在对应「录入数据」页录入", 1, 'AnlPage说明')
# AnlPage 仍保留 entryRec state（resolution 用）
# 恢复 entryRec state（上面删了，resolution 需要）
old_anl_state = "const [detail,setDetail]=useState(null);   const [fkw,setFkw]=useState"
rep(old_anl_state, "const [detail,setDetail]=useState(null);   const [entryRec,setEntryRec]=useState(null);   const [fkw,setFkw]=useState", 1, 'AnlPage恢复entryRec')

# ---- 8) MENU / PAGE_TITLE / renderPage ----
old_menu = """  {key:'entry_cgcgk', icon:'⌗', label:'Cg/Cgk 台账', group:'台账'},"""
new_menu = old_menu + """
  {key:'data_grr', icon:'⌗', label:'GRR 录入数据', group:'录入数据'},
  {key:'data_kappa', icon:'⌗', label:'KAPPA 录入数据', group:'录入数据'},
  {key:'data_linear', icon:'⌗', label:'线性/偏移录入数据', group:'录入数据'},
  {key:'data_stability', icon:'⌗', label:'稳定性录入数据', group:'录入数据'},
  {key:'data_cgcgk', icon:'⌗', label:'Cg/Cgk 录入数据', group:'录入数据'},"""
rep(old_menu, new_menu, 1, 'MENU录入组')

old_pt = "'entry_cgcgk':'Cg/Cgk 台账',"
new_pt = "'entry_cgcgk':'Cg/Cgk 台账','data_grr':'GRR 录入数据','data_kappa':'KAPPA 录入数据','data_linear':'线性/偏移录入数据','data_stability':'稳定性录入数据','data_cgcgk':'Cg/Cgk 录入数据',"
rep(old_pt, new_pt, 1, 'PAGE_TITLE')

old_rp = "if(page==='entry_cgcgk') return <EntryPage kind=\"cgcgk\"/>;"
new_rp = old_rp + """
    if(page==='data_grr') return <DataEntryPage kind="grr"/>;
    if(page==='data_kappa') return <DataEntryPage kind="kappa"/>;
    if(page==='data_linear') return <DataEntryPage kind="linear"/>;
    if(page==='data_stability') return <DataEntryPage kind="stability"/>;
    if(page==='data_cgcgk') return <DataEntryPage kind="cgcgk"/>;"""
rep(old_rp, new_rp, 1, 'renderPage')

io.open(P, 'w', encoding='utf-8').write(s)
print('\n'.join(log))
print('saved delta:', len(s)-len(orig))
