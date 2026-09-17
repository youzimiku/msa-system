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

# state + saveEdit
rep("""  const [modal,setModal]=useState(null);
  const [logOpen,setLogOpen]=useState(false);""",
"""  const [modal,setModal]=useState(null);
  const [logOpen,setLogOpen]=useState(false);
  const [editingId,setEditingId]=useState(null); const [draft,setDraft]=useState({});
  const startEdit=(r)=>{ setEditingId(r.id); setDraft({...r}); };
  const saveEdit=()=>{ if(!editingId) return; mut(s=>{ const rec=s.sampleLib.find(x=>x.id===editingId); if(rec) Object.assign(rec,draft); logAction(s.me.name,'编辑样本',editingId,'行内编辑 '+editingId+' '+(draft.name||'')); }); setEditingId(null); setDraft({}); toast.ok('已保存'); };""",
'B1 state+saveEdit')

# 编辑按钮
rep("""      <Button size="small" type="link" onClick={()=>setModal({record:r,revise:true})}>编辑</Button>""",
"""      {editingId===r.id
        ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
        : <Button size="small" type="link" onClick={()=>startEdit(r)}>编辑</Button>}""",
'B2 编辑按钮')

# 可编辑列
rep("""    {title:'样本名称', dataIndex:'name', width:190, ellipsis:true},""",
"""    {title:'样本名称', dataIndex:'name', width:190, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},""",
'B3 name')

rep("""    {title:'样本类型', dataIndex:'type', width:100, render:v=><Tag color={v==='标准件'?'blue':'green'}>{v}</Tag>},""",
"""    {title:'样本类型', dataIndex:'type', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:92}} options={[{value:'标准件',label:'标准件'},{value:'生产件',label:'生产件'}]} onChange={x=>setDraft(d=>({...d,type:x}))}/>:<Tag color={v==='标准件'?'blue':'green'}>{v}</Tag>},""",
'B4 type')

rep("""    {title:'零件号', dataIndex:'partNo', width:100, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'零件号', dataIndex:'partNo', width:100, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,partNo:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'B5 partNo')

rep("""    {title:'对应被测项目', dataIndex:'charDim', width:150, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'对应被测项目', dataIndex:'charDim', width:150, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,charDim:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'B6 charDim')

rep("""    {title:'名义值', dataIndex:'nominal', width:90, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'名义值', dataIndex:'nominal', width:100, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,nominal:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'B7 nominal')

rep("""    {title:'参考值（真值）', dataIndex:'refValue', width:120, render:v=><span className="mono">{v||'暂无'}</span>},""",
"""    {title:'参考值（真值）', dataIndex:'refValue', width:120, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,refValue:e.target.value}))}/>:<span className="mono">{v||'暂无'}</span>},""",
'B8 refValue')

rep("""    {title:'单位', dataIndex:'unit', width:64, render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'单位', dataIndex:'unit', width:70, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,unit:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'B9 unit')

rep("""    {title:'关联检验标准', dataIndex:'standardId', width:110, render:(v)=>{ const st=(d.standards||[]).find(s=>s.id===v); return <span className="mono">{st?(st.id):(v||'—')}</span>; }},""",
"""    {title:'关联检验标准', dataIndex:'standardId', width:120, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:110}} options={[{value:'',label:'—'},...(d.standards||[]).map(s=>({value:s.id,label:s.id}))]} onChange={x=>setDraft(d=>({...d,standardId:x||undefined}))}/>:<span className="mono">{(()=>{ const st=(d.standards||[]).find(s=>s.id===v); return st?(st.id):(v||'—'); })()}</span>},""",
'B10 standardId')

rep("""    {title:'来源', dataIndex:'source', width:150, ellipsis:true},""",
"""    {title:'来源', dataIndex:'source', width:150, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,source:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'B11 source')

rep("""    {title:'有效期至', dataIndex:'expireDate', width:105, render:v=><span className="mono tiny">{v}</span>},""",
"""    {title:'有效期至', dataIndex:'expireDate', width:110, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,expireDate:e.target.value}))}/>:<span className="mono tiny">{v}</span>},""",
'B12 expireDate')

rep("""    {title:'工厂', dataIndex:'plant', width:90, ellipsis:true, render:v=><span>{v||'—'}</span>},
    {title:'车间', dataIndex:'subplant', width:80, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""    {title:'工厂', dataIndex:'plant', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:100}} options={PLANTS_OPT} onChange={x=>setDraft(d=>({...d,plant:x}))}/>:<span>{v||'—'}</span>},
    {title:'车间', dataIndex:'subplant', width:100, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:90}} options={SUBPLANTS_OPT} onChange={x=>setDraft(d=>({...d,subplant:x}))}/>:<span>{v||'—'}</span>},""",
'B13 plant/subplant')

rep("""    {title:'状态', dataIndex:'status', width:90, render:v=><Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
"""    {title:'状态', dataIndex:'status', width:100, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setDraft(d=>({...d,status:x}))}/>:<Tooltip title={TIPS.status2[v]||v}><Tag color={ENUM.statusColor[v]||'default'} style={{minWidth:56,display:'inline-flex',justifyContent:'center',marginRight:0}}>{v}</Tag></Tooltip>},""",
'B14 status')

rep("""    {title:'说明', dataIndex:'note', width:240, ellipsis:true}
  ];""",
"""    {title:'说明', dataIndex:'note', width:240, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,note:e.target.value}))}/>:<span>{v||'—'}</span>}
  ];""",
'B15 note')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
