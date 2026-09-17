# -*- coding: utf-8 -*-
import io

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
c = io.open(path, encoding='utf-8').read()

def must_replace(old, new, tag):
    global c
    n = c.count(old)
    assert n == 1, f'{tag}: found {n}'
    c = c.replace(old, new)
    print('OK', tag)

# ===== 改动1：删除 mergeCols 三列 =====
must_replace("""    {title:'可否合并取样', dataIndex:'canMerge', width:104, render:(_,r)=><Select size="small" value={r.canMerge||'否'} style={{width:92}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setMF(r,'canMerge',x)}/>},
""", "", 'del 可否合并取样列')

must_replace("""    {title:'车间', width:86, render:(_,r)=><Select size="small" value={r.rule?r.rule.subplant:''} style={{width:76}} options={SUBPLANTS_OPT} onChange={x=>setRF(r,'subplant',x)}/>},
""", "", 'del 车间列(mergeCols)')

must_replace("""    {title:'取样策略说明', width:220, ellipsis:true, render:(_,r)=><Input size="small" value={r.rule?r.rule.note:''} onChange={e=>setRF(r,'note',e.target.value)}/>},
""", "", 'del 取样策略说明列')

# ===== 改动4：样本库查询条件去掉检验标准 =====
must_replace("  const [fStd,setFStd]=useState();\n", "", 'del fStd state')
must_replace("  const [q,setQ]=useState({kw:'',type:undefined,st:undefined,std:undefined,plant:undefined,sub:undefined});",
             "  const [q,setQ]=useState({kw:'',type:undefined,st:undefined,plant:undefined,sub:undefined});", 'del q.std')
must_replace("    .filter(r=>!q.std||r.standardId===q.std)\n", "", 'del std filter')
must_replace("  const resetQ=()=>{ setFkw('');setFtype();setFst();setFStd();setFPlant();setFSub(); setQ({kw:'',type:undefined,st:undefined,std:undefined,plant:undefined,sub:undefined}); };",
             "  const resetQ=()=>{ setFkw('');setFtype();setFst();setFPlant();setFSub(); setQ({kw:'',type:undefined,st:undefined,plant:undefined,sub:undefined}); };", 'resetQ 清理 std')
must_replace("        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>检验标准</span><Select allowClear style={{width:140}} options={(d.standards||[]).map(s=>({value:s.id,label:s.id}))} value={fStd} onChange={setFStd}/>\n", "", 'del 查询条件检验标准')
must_replace("onClick={()=>setQ({kw:fkw,type:ftype,st:fst,std:fStd,plant:fPlant,sub:fSub})}", "onClick={()=>setQ({kw:fkw,type:ftype,st:fst,plant:fPlant,sub:fSub})}", '查询按钮去 std')

# ===== 改动2：被测参数列表检验方法列，改为分号连接的方法名称展示 =====
old_col = """    {title:'检验方法', width:210, render:(_,r)=><Select size="small" mode="multiple" value={(r.methods||[]).map(m=>m.method)} style={{width:200}} options={(d.anMethods||[]).map(m=>({value:m.code,label:METHOD_NAME(m.code)}))} onChange={x=>setF(r,'methods',x.map(v=>({method:v})))}/>},"""
new_col = """    {title:'检验方法', width:230, render:(_,r)=><Select size="small" className="msa-method-select" mode="multiple" value={(r.methods||[]).map(m=>m.method)} style={{width:220}} options={(d.anMethods||[]).map(m=>({value:m.code,label:METHOD_NAME(m.code)}))} tagRender={(p)=><span>{p.label}</span>} onChange={x=>setF(r,'methods',x.map(v=>({method:v})))}/>},"""
must_replace(old_col, new_col, '检验方法列改分号连接展示')

io.open(path, 'w', encoding='utf-8').write(c)
print('ALL DONE')
