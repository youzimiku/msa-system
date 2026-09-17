# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(old, new, desc, expect=1):
    global src
    n = src.count(old)
    ok = (n == expect)
    print(f'{desc}: 出现 {n} 次 (期望 {expect})', '-> 替换' if ok else '!!跳过')
    if ok:
        src = src.replace(old, new)

# ---- state ----
rep("""  const [stdDetail,setStdDetail]=useState(null);
  const [stdModal,setStdModal]=useState(null);""",
"""  const [stdDetail,setStdDetail]=useState(null);
  const [stdModal,setStdModal]=useState(null);
  const [editingId,setEditingId]=useState(null); const [draft,setDraft]=useState({});
  const [stdEditingId,setStdEditingId]=useState(null); const [stdDraft,setStdDraft]=useState({});""",
'C1 state')

# ---- saveEdit（特性）----
rep("""  const methodView=(r)=>{ const ms=r.methods||[]; return ms.length? <Space size={2} wrap>{ms.map(m=><Tag key={m.method} color="blue" style={{marginRight:0}}>{METHOD_NAME(m.method)}</Tag>)}</Space> : <span className="tiny">—</span>; };""",
"""  const methodView=(r)=>{ const ms=r.methods||[]; return ms.length? <Space size={2} wrap>{ms.map(m=><Tag key={m.method} color="blue" style={{marginRight:0}}>{METHOD_NAME(m.method)}</Tag>)}</Space> : <span className="tiny">—</span>; };
  const startEdit=(r)=>{ setEditingId(r.id); setDraft({...r}); };
  const saveEdit=()=>{ if(!editingId) return; mut(s=>{ const rec=s.characteristics.find(x=>x.id===editingId); if(rec) Object.assign(rec,draft); logAction(s.me.name,'编辑被测参数',editingId,'行内编辑 '+editingId+' '+(draft.name||'')); }); setEditingId(null); setDraft({}); toast.ok('已保存'); };
  const startStdEdit=(r)=>{ setStdEditingId(r.id); setStdDraft({...r}); };
  const saveStdEdit=()=>{ if(!stdEditingId) return; mut(s=>{ const rec=s.standards.find(x=>x.id===stdEditingId); if(rec) Object.assign(rec,stdDraft); logAction(s.me.name,'修订检验标准',stdEditingId,'行内修订 '+stdEditingId); }); setStdEditingId(null); setStdDraft({}); toast.ok('已保存'); };""",
'C2 saveEdit')

# ---- 特性列表 操作列 ----
rep("""      <Button size="small" type="link" onClick={()=>setDetail(r)}>查看</Button>
      <Button size="small" type="link" onClick={()=>setModal({record:r})}>编辑</Button>""",
"""      <Button size="small" type="link" onClick={()=>setDetail(r)}>查看</Button>
      {editingId===r.id
        ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
        : <Button size="small" type="link" onClick={()=>startEdit(r)}>编辑</Button>}""",
'C3 特性编辑按钮')

# ---- 特性列表 可编辑列 ----
rep("""    {title:'被测参数名称', dataIndex:'name', width:170, ellipsis:true},""",
"""    {title:'被测参数名称', dataIndex:'name', width:170, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},""",
'C4 name')

rep("""    {title:'特性类型', dataIndex:'type', width:90, render:v=><Tooltip title={TIPS.charType[v]||v}><Tag color={v==='SC'?'red':v==='CC'?'orange':'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
"""    {title:'特性类型', dataIndex:'type', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:100}} options={[{value:'SC',label:'SC'},{value:'CC',label:'CC'},{value:'普通',label:'普通'}]} onChange={x=>setDraft(d=>({...d,type:x}))}/>:<Tooltip title={TIPS.charType[v]||v}><Tag color={v==='SC'?'red':v==='CC'?'orange':'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
'C5 type')

rep("""    {title:'零件名称', dataIndex:'partName', width:110, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'零件名称', dataIndex:'partName', width:110, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,partName:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C6 partName')

rep("""    {title:'零件编号', dataIndex:'partNo', width:100, ellipsis:true, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'零件编号', dataIndex:'partNo', width:100, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,partNo:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C7 partNo')

rep("""    {title:'工序', dataIndex:'processName', width:90, ellipsis:true},""",
"""    {title:'工序', dataIndex:'processName', width:90, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,processName:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C8 processName')

rep("""    {title:'特性类别', dataIndex:'category', width:90},""",
"""    {title:'特性类别', dataIndex:'category', width:100, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,category:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C9 category')

rep("""    {title:'检验方法', width:150, render:(_,r)=>methodView(r)},""",
"""    {title:'检验方法', width:200, render:(_,r)=>editingId===r.id?<Select size="small" mode="multiple" defaultValue={(r.methods||[]).map(m=>m.method)} style={{width:190}} options={anMethods.map(m=>({value:m.code,label:METHOD_NAME(m.code)}))} onChange={x=>setDraft(d=>({...d,methods:x.map(v=>({method:v}))}))}/>:methodView(r)},""",
'C10 methods')

rep("""    {title:'单位', dataIndex:'unit', width:64, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'单位', dataIndex:'unit', width:70, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,unit:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C11 unit')

rep("""    {title:'标准值', dataIndex:'target', width:80, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'标准值', dataIndex:'target', width:90, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,target:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C12 target')

rep("""    {title:'上限USL', dataIndex:'usl', width:80, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'上限USL', dataIndex:'usl', width:90, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,usl:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C13 usl')

rep("""    {title:'下限LSL', dataIndex:'lsl', width:80, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'下限LSL', dataIndex:'lsl', width:90, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,lsl:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C14 lsl')

rep("""    {title:'工厂', dataIndex:'plant', width:90, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'工厂', dataIndex:'plant', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:100}} options={PLANTS_OPT} onChange={x=>setDraft(d=>({...d,plant:x}))}/>:<span>{v||'—'}</span>},""",
'C15 plant')

rep("""    {title:'车间', dataIndex:'subplant', width:80, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'车间', dataIndex:'subplant', width:100, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:90}} options={SUBPLANTS_OPT} onChange={x=>setDraft(d=>({...d,subplant:x}))}/>:<span>{v||'—'}</span>},""",
'C16 subplant')

rep("""    {title:'来源', dataIndex:'source', width:140, ellipsis:true},""",
"""    {title:'来源', dataIndex:'source', width:140, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,source:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C17 source')

rep("""    {title:'状态', dataIndex:'status', width:80, render:v=><Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
"""    {title:'状态', dataIndex:'status', width:100, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setDraft(d=>({...d,status:x}))}/>:<Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
'C18 status')

# ---- 标准列表 操作列（详情/修订）----
rep("""    {title:'操作', width:120, render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>setStdDetail(r)}>详情</Button>
      <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>setStdModal({record:r, revise:true})}>修订</Button>
    </Space>},""",
"""    {title:'操作', width:120, render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>setStdDetail(r)}>详情</Button>
      {stdEditingId===r.id
        ? <><Button size="small" type="link" onClick={saveStdEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setStdEditingId(null);setStdDraft({});}}>取消</Button></>
        : <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>startStdEdit(r)}>修订</Button>}
    </Space>},""",
'C19 标准修订按钮')

# ---- 标准列表 可编辑列 ----
rep("""    {title:'检验标准', dataIndex:'basis', width:180, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'检验标准', dataIndex:'basis', width:180, ellipsis:true, render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,basis:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C20 basis')

rep("""    {title:'检验方法', dataIndex:'method', width:150, ellipsis:true},""",
"""    {title:'检验方法', dataIndex:'method', width:150, ellipsis:true, render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,method:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'C21 method')

rep("""    {title:'测量人数', dataIndex:'numOps', width:80},""",
"""    {title:'测量人数', dataIndex:'numOps', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numOps:x}))}/>:<span>{v}</span>},""",
'C22 numOps')

rep("""    {title:'测量次数', dataIndex:'numTrials', width:80},""",
"""    {title:'测量次数', dataIndex:'numTrials', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numTrials:x}))}/>:<span>{v}</span>},""",
'C23 numTrials')

rep("""    {title:'样本数量', dataIndex:'numParts', width:80},""",
"""    {title:'样本数量', dataIndex:'numParts', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numParts:x}))}/>:<span>{v}</span>},""",
'C24 numParts')

rep("""    {title:'分析类型', width:84, render:(_,r)=><Tag color="blue">{r.type}</Tag>},""",
"""    {title:'分析类型', width:110, render:(_,r)=>stdEditingId===r.id?<Select size="small" defaultValue={r.type} style={{width:100}} options={['GRR判定','NDC判定','KAPPA判定','有效性判定','偏倚/线性判定','稳定性判定'].map(c=>({value:c,label:c}))} onChange={x=>setStdDraft(d=>({...d,type:x}))}/>:<Tag color="blue">{r.type}</Tag>},""",
'C25 stdType')

rep("""    {title:'版本', dataIndex:'version', width:70, render:v=><Tag color="purple">{v}</Tag>},""",
"""    {title:'版本', dataIndex:'version', width:80, render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,version:e.target.value}))}/>:<Tag color="purple">{v}</Tag>},""",
'C26 version')

rep("""    {title:'状态', dataIndex:'status', width:90, render:s=><StatusTag s={s}/>}
  ];""",
"""    {title:'状态', dataIndex:'status', width:100, render:(s,r)=>stdEditingId===r.id?<Select size="small" defaultValue={s} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setStdDraft(d=>({...d,status:x}))}/>:<StatusTag s={s}/>}
  ];""",
'C27 stdStatus')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
