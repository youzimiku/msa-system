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

# C1 NavAPI 声明加 openAnl
rep("const NavAPI = { go:()=>{}, openGrr:()=>{}, openKappa:()=>{}, openInst:()=>{}, openCalibInst:()=>{} };",
    "const NavAPI = { go:()=>{}, openGrr:()=>{}, openKappa:()=>{}, openAnl:()=>{}, openInst:()=>{}, openCalibInst:()=>{} };")

# C2 App 注入 openAnl
rep("  NavAPI.openKappa = (id)=>{ KpaOpenId=id; setPage('kappa'); };",
    "  NavAPI.openKappa = (id)=>{ KpaOpenId=id; setPage('kappa'); };\n  NavAPI.openAnl = (kind,id)=>{ AnlOpen={kind,id}; setPage(ANA_PAGE[kind]); };")

# C3 MENU 加 4 项
rep("  {key:'grr', icon:'◔', label:'GRR 台账', group:'分析执行'},\n  {key:'kappa', icon:'✓', label:'KAPPA 台账', group:'分析执行'}\n];",
    "  {key:'grr', icon:'◔', label:'GRR 台账', group:'分析执行'},\n  {key:'kappa', icon:'✓', label:'KAPPA 台账', group:'分析执行'},\n  {key:'anl_linear', icon:'↗', label:'线性/偏移分析', group:'分析执行'},\n  {key:'anl_stability', icon:'≋', label:'稳定性分析', group:'分析执行'},\n  {key:'anl_cgcgk', icon:'⊞', label:'Cg/Cgk 分析', group:'分析执行'},\n  {key:'anl_resolution', icon:'⊕', label:'分辨率分析', group:'分析执行'}\n];")

# C4 PAGE_TITLE 加 4 项
rep("  'kappa':'KAPPA 台账（计数型一致性分析）'};",
    "  'kappa':'KAPPA 台账（计数型一致性分析）','anl_linear':'线性/偏移性分析台账','anl_stability':'稳定性分析台账','anl_cgcgk':'Cg/Cgk 分析台账（VDA Type1）','anl_resolution':'分辨率分析台账'};")

# C5 renderPage 加 4 分支
rep("    if(page==='grr') return <GrrPage/>;\n    if(page==='kappa') return <KappaPage/>;\n    return <Dashboard/>;",
    "    if(page==='grr') return <GrrPage/>;\n    if(page==='kappa') return <KappaPage/>;\n    if(page==='anl_linear') return <AnlPage kind=\"linear\"/>;\n    if(page==='anl_stability') return <AnlPage kind=\"stability\"/>;\n    if(page==='anl_cgcgk') return <AnlPage kind=\"cgcgk\"/>;\n    if(page==='anl_resolution') return <AnlPage kind=\"resolution\"/>;\n    return <Dashboard/>;")

# C6 记录跳转 helper（放在 anlOpenRec 后）
rep("let AnlOpen=null;\nfunction anlOpenRec(kind,id){ AnlOpen={kind,id}; NavAPI.go(ANA_PAGE[kind]); }",
    "let AnlOpen=null;\nfunction anlOpenRec(kind,id){ AnlOpen={kind,id}; NavAPI.go(ANA_PAGE[kind]); }\nfunction recJump(x){ const k=recKindId(x); if(k==='GRR') return NavAPI.openGrr(x.id); if(k==='KAPPA') return NavAPI.openKappa(x.id); return anlOpenRec(k,x.id); }")

# C7 仪表盘分析单号跳转
rep("onClick={()=>x.id.indexOf('GRR')===0?NavAPI.openGrr(x.id):NavAPI.openKappa(x.id)}>{x.id}</span>)}",
    "onClick={()=>recJump(x)}>{x.id}</span>)}")

# C8 计划列表分析单号跳转
rep("        {title:'编号', dataIndex:'id', render:(v,r)=><span className=\"row-link mono\" onClick={()=>r.type==='GRR'?NavAPI.openGrr(v):NavAPI.openKappa(v)}>{v}</span>},",
    "        {title:'编号', dataIndex:'id', render:(v)=><span className=\"row-link mono\" onClick={()=>recJump({id:v})}>{v}</span>},")

# C9 PlanActions 台账按钮
rep("    <Button size=\"small\" type=\"link\" onClick={()=>{ if(!first){ toast.warn('该计划尚未定型生成台账记录'); return; } first.id.indexOf('GRR')===0?NavAPI.openGrr(first.id):NavAPI.openKappa(first.id); }}>台账</Button>",
    "    <Button size=\"small\" type=\"link\" onClick={()=>{ if(!first){ toast.warn('该计划尚未定型生成台账记录'); return; } recJump(first); }}>台账</Button>")

# C10 PlanDetail 录入数据/台账按钮
rep("      {recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size=\"small\" type=\"primary\" ghost disabled={!canDo(me.role,'edit')} onClick={()=>x.id.indexOf('GRR')===0?NavAPI.openGrr(x.id):NavAPI.openKappa(x.id)}>录入数据 {x.id}</Button>)}",
    "      {recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size=\"small\" type=\"primary\" ghost disabled={!canDo(me.role,'edit')} onClick={()=>recJump(x)}>录入数据 {x.id}</Button>)}")
rep("      {recs.map(x=><Button key={'t'+x.id} size=\"small\" type=\"link\" onClick={()=>x.id.indexOf('GRR')===0?NavAPI.openGrr(x.id):NavAPI.openKappa(x.id)}>台账 {x.id}</Button>)}",
    "      {recs.map(x=><Button key={'t'+x.id} size=\"small\" type=\"link\" onClick={()=>recJump(x)}>台账 {x.id}</Button>)}")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
