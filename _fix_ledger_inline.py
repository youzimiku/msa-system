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

# 1) state
rep("""  const [modal,setModal]=useState(null); // {mode:'add'|'edit', record}
  const [detail,setDetail]=useState(null);""",
"""  const [modal,setModal]=useState(null); // {mode:'add'|'edit', record}
  const [detail,setDetail]=useState(null);
  const [editingId,setEditingId]=useState(null); const [draft,setDraft]=useState({});""",
'L1 state')

# 2) saveEdit
rep("""  const openAdd = ()=>setModal({mode:'add', record:{}});
  const openEdit = (r)=>setModal({mode:'edit', record:r});""",
"""  const openAdd = ()=>setModal({mode:'add', record:{}});
  const openEdit = (r)=>setModal({mode:'edit', record:r});
  const startEdit=(r)=>{ setEditingId(r.id); setDraft({...r}); };
  const saveEdit=()=>{ if(!editingId) return; mut(s=>{ const rec=s.instruments.find(x=>x.id===editingId); if(rec) Object.assign(rec,draft); logAction(s.me.name,'编辑器具',editingId,'行内编辑 '+editingId+' '+(draft.name||'')); }); setEditingId(null); setDraft({}); toast.ok('已保存'); };""",
'L2 saveEdit')

# 3) 操作列编辑按钮
rep("""      {canDo(d.me.role,'edit')&&<Button size="small" type="link" onClick={()=>openEdit(r)}>编辑</Button>}""",
"""      {canDo(d.me.role,'edit')&&(editingId===r.id
        ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
        : <Button size="small" type="link" onClick={()=>startEdit(r)}>编辑</Button>)}""",
'L3 编辑按钮')

# 4) 可编辑列
def inp(field):
    return f'render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={{v}} onChange={{e=>setDraft(d=>({{...d,{field}:e.target.value}}))}}/>:<span>{{v||"—"}}</span>'

rep("""    {title:'计量器具名称', dataIndex:'name', width:160, ellipsis:true},""",
"""    {title:'计量器具名称', dataIndex:'name', width:160, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},""",
'L4 name')

rep("""    {title:'型号', dataIndex:'model', width:100, ellipsis:true},""",
"""    {title:'型号', dataIndex:'model', width:100, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,model:e.target.value}))}/>:<span>{v}</span>},""",
'L5 model')

rep("""    {title:'器具类型', dataIndex:'cat', width:86, render:(v)=><Tag>{v}</Tag>},""",
"""    {title:'器具类型', dataIndex:'cat', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:100}} options={ENUM.instCat.map(c=>({value:c,label:c}))} onChange={x=>setDraft(d=>({...d,cat:x}))}/>:<Tag>{v}</Tag>},""",
'L6 cat')

rep("""    {title:'线别', dataIndex:'line', width:70, ellipsis:true},""",
"""    {title:'线别', dataIndex:'line', width:70, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,line:e.target.value}))}/>:<span>{v||"—"}</span>},""",
'L7 line')

rep("""    {title:'生产线', dataIndex:'prodLine', width:90, ellipsis:true},""",
"""    {title:'生产线', dataIndex:'prodLine', width:90, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,prodLine:e.target.value}))}/>:<span>{v||"—"}</span>},""",
'L8 prodLine')

rep("""    {title:'规格', dataIndex:'spec', width:105, ellipsis:true, render:(v)=><span className="mono">{v||'暂无'}</span>},""",
"""    {title:'规格', dataIndex:'spec', width:105, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,spec:e.target.value}))}/>:<span className="mono">{v||'暂无'}</span>},""",
'L9 spec')

rep("""    {title:'分辨力', dataIndex:'res', width:92, render:(v)=><span className="mono">{v}</span>},""",
"""    {title:'分辨力', dataIndex:'res', width:100, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,res:e.target.value}))}/>:<span className="mono">{v}</span>},""",
'L10 res')

rep("""    {title:'使用部门', dataIndex:'dept', width:100, ellipsis:true},""",
"""    {title:'使用部门', dataIndex:'dept', width:100, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,dept:e.target.value}))}/>:<span>{v||"—"}</span>},""",
'L11 dept')

rep("""    {title:'复评周期(月)', width:100, render:(_,r)=><span className="mono">{r.calCycle||12}</span>},""",
"""    {title:'复评周期(月)', width:100, render:(_,r)=>editingId===r.id?<InputNumber size="small" min={1} defaultValue={r.calCycle||12} style={{width:90}} onChange={x=>setDraft(d=>({...d,calCycle:x}))}/>:<span className="mono">{r.calCycle||12}</span>},""",
'L12 calCycle')

rep("""    {title:'复评提前提醒(天)', width:130, render:(_,r)=><span className="mono">{r.calAdvance||20}</span>},""",
"""    {title:'复评提前提醒(天)', width:130, render:(_,r)=>editingId===r.id?<InputNumber size="small" min={0} defaultValue={r.calAdvance||20} style={{width:110}} onChange={x=>setDraft(d=>({...d,calAdvance:x}))}/>:<span className="mono">{r.calAdvance||20}</span>},""",
'L13 calAdvance')

rep("""    {title:'领用人', dataIndex:'owner', width:74},""",
"""    {title:'领用人', dataIndex:'owner', width:80, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,owner:e.target.value}))}/>:<span>{v||"—"}</span>},""",
'L14 owner')

rep("""    {title:'校准方式', dataIndex:'calMode', width:72, render:(v)=>v==='外校'?<Tag color="blue">外校</Tag>:<Tag color="cyan">内校</Tag>},""",
"""    {title:'校准方式', dataIndex:'calMode', width:86, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:78}} options={['外校','内校'].map(c=>({value:c,label:c}))} onChange={x=>setDraft(d=>({...d,calMode:x}))}/>:(v==='外校'?<Tag color="blue">外校</Tag>:<Tag color="cyan">内校</Tag>)},""",
'L15 calMode')

rep("""    {title:'是否做MSA', width:84, render:(_,r)=><span>{r.doMsa==='是'?<Tag color="blue">是</Tag>:'否'}</span>},""",
"""    {title:'是否做MSA', width:100, render:(_,r)=>editingId===r.id?<Select size="small" defaultValue={r.doMsa||'否'} style={{width:84}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setDraft(d=>({...d,doMsa:x}))}/>:<span>{r.doMsa==='是'?<Tag color="blue">是</Tag>:'否'}</span>},""",
'L16 doMsa')

rep("""    {title:'状态', dataIndex:'status', width:90, render:s=><StatusTag s={s}/>}
  ];""",
"""    {title:'状态', dataIndex:'status', width:110, render:(s,r)=>editingId===r.id?<Select size="small" defaultValue={s} style={{width:100}} options={ENUM.instStatus.map(c=>({value:c,label:c}))} onChange={x=>setDraft(d=>({...d,status:x}))}/>:<StatusTag s={s}/>}
  ];""",
'L17 status')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
