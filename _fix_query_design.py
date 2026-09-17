# -*- coding: utf-8 -*-
# 按各页数据结构统一设计查询条件（2026-09-11）
# 原则：工厂/车间保持最左；筛选字段对齐数据表实际字段；状态选项按页区分；不删数据字段
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(P, encoding='utf-8').read()
orig = src
def rep(old, new, tag):
    global src
    n = src.count(old)
    if n == 0:
        print('[MISS] ' + tag)
        return
    if n > 1:
        print('[MULTI x%d] %s' % (n, tag))
        return
    src = src.replace(old, new)
    print('[OK] ' + tag)

# ============ 1. 计量器具台账 LedgerPage：+器具类型(mcat) ============
rep(
"  const [fSub,setFSub]=useState(undefined);\n  const [q,setQ]=useState({kw:'',cat:undefined,status:undefined,due:undefined,dueN:'',plant:undefined,sub:undefined}); // 查询生效值",
"  const [fSub,setFSub]=useState(undefined);\n  const [fMcat,setFMcat]=useState(undefined);\n  const [q,setQ]=useState({kw:'',cat:undefined,mcat:undefined,status:undefined,due:undefined,dueN:'',plant:undefined,sub:undefined}); // 查询生效值",
"台账-状态声明+器具类型")

rep(
"(!q.cat || i.cat===q.cat) && (!q.status || i.status===q.status) &&",
"(!q.cat || i.cat===q.cat) && (!q.mcat || i.mcat===q.mcat) && (!q.status || i.status===q.status) &&",
"台账-过滤条件+器具类型")

rep(
'<Select allowClear placeholder="器具类别" style={{width:140}} value={fCat} options={ENUM.instCat.map(c=>({value:c,label:c}))} onChange={setFCat}/>',
'<Select allowClear placeholder="器具类别" style={{width:140}} value={fCat} options={ENUM.instCat.map(c=>({value:c,label:c}))} onChange={setFCat}/>\n        <Select allowClear placeholder="器具类型" style={{width:140}} value={fMcat} options={[...new Set(d.instruments.map(i=>i.mcat).filter(Boolean))].map(c=>({value:c,label:c}))} onChange={setFMcat}/>',
"台账-查询区插入器具类型")

rep(
"onClick={()=>setQ({kw, cat:fCat, status:fStatus, due:fDue, dueN, plant:fPlant, sub:fSub})}>查询",
"onClick={()=>setQ({kw, cat:fCat, mcat:fMcat, status:fStatus, due:fDue, dueN, plant:fPlant, sub:fSub})}>查询",
"台账-查询按钮")

rep(
"setKw('');setFCat(undefined);setFStatus(undefined);setFDue(undefined);setDueN('');setFPlant(undefined);setFSub(undefined); setQ({kw:'',cat:undefined,status:undefined,due:undefined,dueN:'',plant:undefined,sub:undefined});",
"setKw('');setFCat(undefined);setFMcat(undefined);setFStatus(undefined);setFDue(undefined);setDueN('');setFPlant(undefined);setFSub(undefined); setQ({kw:'',cat:undefined,mcat:undefined,status:undefined,due:undefined,dueN:'',plant:undefined,sub:undefined});",
"台账-重置")

# ============ 2. 器具组维护 InstGroupPage：+工厂/车间 ============
rep(
"  const [fType,setFType]=useState(undefined);\n  const [q,setQ]=useState({kw:'',cycle:undefined,type:undefined});",
"  const [fType,setFType]=useState(undefined);\n  const [fPlant,setFPlant]=useState(undefined);\n  const [fSub,setFSub]=useState(undefined);\n  const [q,setQ]=useState({kw:'',cycle:undefined,type:undefined,plant:undefined,sub:undefined});",
"器具组-状态声明+工厂车间")

rep(
"(!q.cycle||String(g.calCycle||12)===q.cycle) &&\n    (!q.type||(g.type||'inst')===q.type));",
"(!q.cycle||String(g.calCycle||12)===q.cycle) &&\n    (!q.type||(g.type||'inst')===q.type) &&\n    (!q.plant||g.plant===q.plant) && (!q.sub||g.subplant===q.sub));",
"器具组-过滤条件+工厂车间")

rep(
'<Input.Search allowClear placeholder="组编码 / 组名称 / 说明" style={{width:140}} value={kw} onChange={e=>setKw(e.target.value)}/>',
'<Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>\n        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>\n        <Input.Search allowClear placeholder="组编码 / 组名称 / 说明" style={{width:140}} value={kw} onChange={e=>setKw(e.target.value)}/>',
"器具组-查询区工厂车间最左")

rep(
"onClick={()=>setQ({kw,cycle:fCycle,type:fType})}>查询",
"onClick={()=>setQ({kw,cycle:fCycle,type:fType,plant:fPlant,sub:fSub})}>查询",
"器具组-查询按钮")

rep(
"setKw('');setFCycle(undefined);setFType(undefined);setQ({kw:'',cycle:undefined,type:undefined});",
"setKw('');setFCycle(undefined);setFType(undefined);setFPlant(undefined);setFSub(undefined);setQ({kw:'',cycle:undefined,type:undefined,plant:undefined,sub:undefined});",
"器具组-重置")

# ============ 3. MSA 计划 PlanPage：+工厂/车间/任务来源 ============
rep(
"  const [qStatus,setQStatus]=useState();\n  const doQuery=()=>{ setQkw(fkw); setQType(ftype); setQStatus(fstatus); };\n  const resetQ=()=>{ setFkw('');setFtype();setFstatus(); setQkw('');setQType();setQStatus(); };",
"  const [qStatus,setQStatus]=useState();\n  const [fPlant,setFPlant]=useState(); const [fSub,setFSub]=useState(); const [fSource,setFSource]=useState();\n  const [qPlant,setQPlant]=useState(); const [qSub,setQSub]=useState(); const [qSource,setQSource]=useState();\n  const doQuery=()=>{ setQkw(fkw); setQType(ftype); setQStatus(fstatus); setQPlant(fPlant); setQSub(fSub); setQSource(fSource); };\n  const resetQ=()=>{ setFkw('');setFtype();setFstatus();setFPlant();setFSub();setFSource(); setQkw('');setQType();setQStatus();setQPlant();setQSub();setQSource(); };",
"MSA计划-状态声明+工厂车间任务来源")

rep(
"const statusMatch = !qStatus || planStatusView(p.status).text===qStatus;\n    return kwMatch && typeMatch && statusMatch;",
"const statusMatch = !qStatus || planStatusView(p.status).text===qStatus;\n    const plantMatch = !qPlant || p.plant===qPlant;\n    const subMatch = !qSub || p.subplant===qSub;\n    const sourceMatch = !qSource || (p.source||'临时任务')===qSource;\n    return kwMatch && typeMatch && statusMatch && plantMatch && subMatch && sourceMatch;",
"MSA计划-过滤条件+工厂车间任务来源")

rep(
"""    <Panel title="查询条件">
      <Space wrap>
        <Input.Search allowClear placeholder="计划号 / 量具号 / 器具名称 / 零件" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>
        <Select allowClear placeholder="分析关联类型" style={{width:140}} value={ftype} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'未定型',label:'未定型'}]} onChange={setFtype}/>""",
"""    <Panel title="查询条件">
      <Space wrap>
        <Select allowClear placeholder="工厂" style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <Select allowClear placeholder="车间" style={{width:140}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>
        <Select allowClear placeholder="分析关联类型" style={{width:140}} value={ftype} options={[{value:'GRR',label:'GRR'},{value:'KAPPA',label:'KAPPA'},{value:'linear',label:'线性/偏移'},{value:'stability',label:'稳定性'},{value:'cgcgk',label:'Cg/Cgk'},{value:'未定型',label:'未定型'}]} onChange={setFtype}/>
        <Select allowClear placeholder="任务来源" style={{width:140}} value={fSource} options={[{value:'周期任务',label:'周期任务'},{value:'临时任务',label:'临时任务'}]} onChange={setFSource}/>
        <Input.Search allowClear placeholder="计划号 / 量具号 / 器具名称 / 零件" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>""",
"MSA计划-查询区工厂车间任务来源")

# ============ 4. 被测参数维护 CharPage：+特性类别/工序 ============
rep(
"const [kw,setKw]=useState(''); const [fType,setFType]=useState(); const [fStatus,setFStatus]=useState(); const [fQPlant,setFQPlant]=useState(); const [fQSub,setFQSub]=useState();",
"const [kw,setKw]=useState(''); const [fType,setFType]=useState(); const [fStatus,setFStatus]=useState(); const [fQPlant,setFQPlant]=useState(); const [fQSub,setFQSub]=useState(); const [fCat2,setFCat2]=useState(); const [fProc2,setFProc2]=useState();",
"被测参数-状态声明+特性类别工序")

rep(
"const doQuery=()=>{ setKw(fkw2); setFType(ft2); setFStatus(fs2); setFQPlant(fPlant); setFQSub(fSub); };\n  const doReset=()=>{ setFkw2(''); setFt2(); setFs2(); setFPlant(); setFSub(); setKw(''); setFType(); setFStatus(); setFQPlant(); setFQSub(); };",
"const doQuery=()=>{ setKw(fkw2); setFType(ft2); setFStatus(fs2); setFQPlant(fPlant); setFQSub(fSub); setFCat2(fCat2); setFProc2(fProc2); };\n  const doReset=()=>{ setFkw2(''); setFt2(); setFs2(); setFPlant(); setFSub(); setKw(''); setFType(); setFStatus(); setFQPlant(); setFQSub(); setFCat2(); setFProc2(); };",
"被测参数-查询重置")

rep(
".filter(r=>!fType || r.type===fType).filter(r=>!fStatus || r.status===fStatus)\n    .filter(r=>!fQPlant || r.plant===fQPlant).filter(r=>!fQSub || r.subplant===fQSub);",
".filter(r=>!fType || r.type===fType).filter(r=>!fStatus || r.status===fStatus)\n    .filter(r=>!fCat2 || r.category===fCat2).filter(r=>!fProc2 || r.processName===fProc2)\n    .filter(r=>!fQPlant || r.plant===fQPlant).filter(r=>!fQSub || r.subplant===fQSub);",
"被测参数-过滤条件+特性类别工序")

rep(
'<Input allowClear placeholder="被测参数编号 / 名称 / 零件 / 工序" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>\n        <Select allowClear placeholder="特性类型" style={{width:140}} options={[{value:\'SC\',label:\'SC\'},{value:\'CC\',label:\'CC\'},{value:\'普通\',label:\'普通\'}]} value={ft2} onChange={setFt2}/>',
'<Input allowClear placeholder="被测参数编号 / 名称 / 零件 / 工序" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>\n        <Select allowClear placeholder="特性类型" style={{width:140}} options={[{value:\'SC\',label:\'SC\'},{value:\'CC\',label:\'CC\'},{value:\'普通\',label:\'普通\'}]} value={ft2} onChange={setFt2}/>\n        <Select allowClear placeholder="特性类别" style={{width:140}} options={[{value:\'计量型\',label:\'计量型\'},{value:\'计数型\',label:\'计数型\'}]} value={fCat2} onChange={setFCat2}/>\n        <Select allowClear placeholder="工序" style={{width:140}} options={[...new Set((d.characteristics||[]).map(r=>r.processName).filter(Boolean))].map(c=>({value:c,label:c}))} value={fProc2} onChange={setFProc2}/>',
"被测参数-查询区特性类别工序")

# ============ 5. 抽样方法维护 SamplingPage：+方法名称/可否合并取样 ============
rep(
"const [kw,setKw]=useState(''); const [fNeed,setFNeed]=useState(); const [fSt,setFSt]=useState(); const [fQPlant,setFQPlant]=useState(); const [fQSub,setFQSub]=useState();",
"const [kw,setKw]=useState(''); const [fNeed,setFNeed]=useState(); const [fSt,setFSt]=useState(); const [fQPlant,setFQPlant]=useState(); const [fQSub,setFQSub]=useState(); const [fMethod2,setFMethod2]=useState(); const [fMerge2,setFMerge2]=useState(); const [fMethod,setFMethod]=useState(); const [fMerge,setFMerge]=useState();",
"抽样方法-状态声明+方法合并")

rep(
"const doQuery=()=>{ setKw(fkw2); setFNeed(fn2); setFSt(fs2); setFQPlant(fPlant); setFQSub(fSub); };\n  const doReset=()=>{ setFkw2(''); setFn2(); setFs2(); setFPlant(); setFSub(); setKw(''); setFNeed(); setFSt(); setFQPlant(); setFQSub(); };",
"const doQuery=()=>{ setKw(fkw2); setFNeed(fn2); setFSt(fs2); setFQPlant(fPlant); setFQSub(fSub); setFMethod(fMethod2); setFMerge(fMerge2); };\n  const doReset=()=>{ setFkw2(''); setFn2(); setFs2(); setFPlant(); setFSub(); setKw(''); setFNeed(); setFSt(); setFQPlant(); setFQSub(); setFMethod(); setFMerge(); setFMethod2(); setFMerge2(); };",
"抽样方法-查询重置")

rep(
".filter(m=>!fNeed || m.needSample===fNeed)\n    .filter(m=>!fSt || m.status===fSt)",
".filter(m=>!fNeed || m.needSample===fNeed)\n    .filter(m=>!fMethod || m.code===fMethod)\n    .filter(m=>!fMerge || (m.canMerge||'否')===fMerge)\n    .filter(m=>!fSt || m.status===fSt)",
"抽样方法-过滤条件+方法合并")

rep(
'<Input allowClear placeholder="规则编号 / 方法 / 说明" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>\n        <Select allowClear placeholder="是否需要取样" style={{width:140}} options={[{value:\'是\',label:\'是\'},{value:\'否\',label:\'否\'}]} value={fn2} onChange={setFn2}/>',
'<Input allowClear placeholder="规则编号 / 方法 / 说明" style={{width:140}} value={fkw2} onChange={e=>setFkw2(e.target.value)}/>\n        <Select allowClear placeholder="方法名称" style={{width:140}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} value={fMethod2} onChange={setFMethod2}/>\n        <Select allowClear placeholder="是否需要取样" style={{width:140}} options={[{value:\'是\',label:\'是\'},{value:\'否\',label:\'否\'}]} value={fn2} onChange={setFn2}/>\n        <Select allowClear placeholder="可否合并取样" style={{width:140}} options={[{value:\'是\',label:\'是\'},{value:\'否\',label:\'否\'}]} value={fMerge2} onChange={setFMerge2}/>',
"抽样方法-查询区方法合并")

# ============ 6. 样本库管理 SampleLibPage：+关联检验标准 ============
rep(
"  const [q,setQ]=useState({kw:'',type:undefined,st:undefined,plant:undefined,sub:undefined});",
"  const [fStd,setFStd]=useState();\n  const [q,setQ]=useState({kw:'',type:undefined,st:undefined,std:undefined,plant:undefined,sub:undefined});",
"样本库-状态声明+检验标准")

rep(
".filter(r=>!q.type||r.type===q.type).filter(r=>!q.st||r.status===q.st)\n    .filter(r=>!q.plant||r.plant===q.plant).filter(r=>!q.sub||r.subplant===q.sub);",
".filter(r=>!q.type||r.type===q.type).filter(r=>!q.st||r.status===q.st)\n    .filter(r=>!q.std||r.standardId===q.std)\n    .filter(r=>!q.plant||r.plant===q.plant).filter(r=>!q.sub||r.subplant===q.sub);",
"样本库-过滤条件+检验标准")

rep(
"const resetQ=()=>{ setFkw('');setFtype();setFst();setFPlant();setFSub(); setQ({kw:'',type:undefined,st:undefined,plant:undefined,sub:undefined}); };",
"const resetQ=()=>{ setFkw('');setFtype();setFst();setFStd();setFPlant();setFSub(); setQ({kw:'',type:undefined,st:undefined,std:undefined,plant:undefined,sub:undefined}); };",
"样本库-重置")

rep(
'<Select allowClear placeholder="样本类型" style={{width:140}} options={[{value:\'标准件\',label:\'标准件\'},{value:\'生产件\',label:\'生产件\'}]} value={ftype} onChange={setFtype}/>',
'<Select allowClear placeholder="样本类型" style={{width:140}} options={[{value:\'标准件\',label:\'标准件\'},{value:\'生产件\',label:\'生产件\'}]} value={ftype} onChange={setFtype}/>\n        <Select allowClear placeholder="关联检验标准" style={{width:140}} options={(d.standards||[]).map(s=>({value:s.id,label:s.id}))} value={fStd} onChange={setFStd}/>',
"样本库-查询区检验标准")

rep(
"onClick={()=>setQ({kw:fkw,type:ftype,st:fst,plant:fPlant,sub:fSub})}>查询",
"onClick={()=>setQ({kw:fkw,type:ftype,st:fst,std:fStd,plant:fPlant,sub:fSub})}>查询",
"样本库-查询按钮")

# ============ 7. 五类台账 EntryPage：+分析人 +结论动态 ============
rep(
"const CFG=ENTRY_CFG[kind];\n  const d=Store.get();\n  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});",
"const CFG=ENTRY_CFG[kind];\n  const d=Store.get();\n  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined); const [fanl,setFanl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined,anl:undefined});\n  const conclOpts=[...new Set((d[CFG.arr]||[]).map(r=>r.conclusion).filter(Boolean))];\n  const anlOpts=[...new Set((d[CFG.arr]||[]).map(r=>r.analyst).filter(Boolean))];",
"台账页-状态声明+分析人")

rep(
"const rows=(d[CFG.arr]||[]).filter(r=>\n    (!q.kw || (r.id+r.planId+r.instId+r.instName+r.object).toLowerCase().includes(q.kw.toLowerCase())) &&\n    (!q.status || r.reviewStatus===q.status) &&\n    (!q.concl || (r.conclusion||'').indexOf(q.concl)>=0));\n  const resetQ=()=>{ setFkw('');setFstatus(undefined);setFconcl(undefined); setQ({kw:'',status:undefined,concl:undefined}); };\n  const goResult=",
"const rows=(d[CFG.arr]||[]).filter(r=>\n    (!q.kw || (r.id+r.planId+r.instId+r.instName+r.object).toLowerCase().includes(q.kw.toLowerCase())) &&\n    (!q.status || r.reviewStatus===q.status) &&\n    (!q.concl || (r.conclusion||'').indexOf(q.concl)>=0) &&\n    (!q.anl || r.analyst===q.anl));\n  const resetQ=()=>{ setFkw('');setFstatus(undefined);setFconcl(undefined);setFanl(undefined); setQ({kw:'',status:undefined,concl:undefined,anl:undefined}); };\n  const goResult=",
"台账页-过滤条件+分析人")

rep(
'<Input.Search allowClear placeholder={CFG.idPref+\'编号 / 关联计划 / 器具 / 测量对象\'} style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={[\'可接受\',\'有条件\',\'不可接受\'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
'<Input.Search allowClear placeholder={CFG.idPref+\'编号 / 关联计划 / 器具 / 测量对象\'} style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={conclOpts.map(c=>({value:c,label:c}))} onChange={setFconcl}/>\n        <Select allowClear placeholder="分析人" style={{width:140}} value={fanl} options={anlOpts.map(c=>({value:c,label:c}))} onChange={setFanl}/>',
"台账页-查询区结论动态+分析人")

# ============ 8. GRR 分析结果 GrrPage：去待采集 +结论动态 ============
rep(
"  const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});\n  const rows = d.grr.filter(r=>",
"  const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});\n  const conclOpts=[...new Set(d.grr.map(r=>r.conclusion).filter(Boolean))];\n  const rows = d.grr.filter(r=>",
"GRR结果-状态声明+结论动态")

rep(
'<Input.Search allowClear placeholder="GRR编号 / 关联计划 / 器具 / 测量对象" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={[\'可接受\',\'有条件\',\'不可接受\'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
'<Input.Search allowClear placeholder="GRR编号 / 关联计划 / 器具 / 测量对象" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={conclOpts.map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
"GRR结果-查询区状态去待采集+结论动态")

# ============ 9. KAPPA 分析结果 KappaPage：去待采集 +结论动态 ============
rep(
"  const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});\n  const rows = d.kappa.filter(r=>",
"  const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});\n  const conclOpts=[...new Set(d.kappa.map(r=>r.conclusion).filter(Boolean))];\n  const rows = d.kappa.filter(r=>",
"KAPPA结果-状态声明+结论动态")

rep(
'<Input.Search allowClear placeholder="KAPPA编号 / 关联计划 / 器具 / 测量对象" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={[\'可接受\',\'有条件\',\'不可接受\'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
'<Input.Search allowClear placeholder="KAPPA编号 / 关联计划 / 器具 / 测量对象" style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={conclOpts.map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
"KAPPA结果-查询区状态去待采集+结论动态")

# ============ 10. 线性/稳定性/CgCgk 分析结果 AnlPage：去待采集 +结论动态 ============
rep(
"const CFG=ANA_CFG[kind];\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [entryRec,setEntryRec]=useState(null);\n  const [anlRec,setAnlRec]=useState(null);\n  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});",
"const CFG=ANA_CFG[kind];\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [entryRec,setEntryRec]=useState(null);\n  const [anlRec,setAnlRec]=useState(null);\n  const [fkw,setFkw]=useState(''); const [fstatus,setFstatus]=useState(undefined); const [fconcl,setFconcl]=useState(undefined);\n  const [q,setQ]=useState({kw:'',status:undefined,concl:undefined});\n  const conclOpts=[...new Set((d[CFG.arr]||[]).map(r=>r.conclusion).filter(Boolean))];",
"Anl结果-状态声明+结论动态")

rep(
'<Input.Search allowClear placeholder={CFG.idPref+\'编号 / 关联计划 / 器具 / 测量对象\'} style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待采集">待采集</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={[\'可接受\',\'有条件\',\'不可接受\'].map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
'<Input.Search allowClear placeholder={CFG.idPref+\'编号 / 关联计划 / 器具 / 测量对象\'} style={{width:140}} value={fkw} onChange={e=>setFkw(e.target.value)}/>\n        <span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span><Radio.Group size="small" value={fstatus||\'\'} onChange={e=>setFstatus(e.target.value||undefined)}><Radio value="">全部</Radio><Radio value="待分析">待分析</Radio><Radio value="待审核">待审核</Radio><Radio value="已批准">已批准</Radio><Radio value="需整改">需整改</Radio><Radio value="已闭环">已闭环</Radio><Radio value="已关闭">已关闭</Radio></Radio.Group>\n        <Select allowClear placeholder="结论" style={{width:140}} value={fconcl} options={conclOpts.map(c=>({value:c,label:c}))} onChange={setFconcl}/>',
"Anl结果-查询区状态去待采集+结论动态")

open(P, 'w', encoding='utf-8').write(src)
print('---- done. changed=%s ----' % (src != orig))
