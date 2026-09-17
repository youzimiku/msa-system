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

# 1) state + saveEdit
rep("""  const openAdd=()=>setModal({mode:'add',record:{}});
  const openEdit=(r)=>setModal({mode:'edit',record:r});""",
"""  const openAdd=()=>setModal({mode:'add',record:{}});
  const openEdit=(r)=>setModal({mode:'edit',record:r});
  const [editingId,setEditingId]=useState(null); const [draft,setDraft]=useState({});
  const startEdit=(r)=>{ setEditingId(r.id); setDraft({...r}); };
  const saveEdit=()=>{ if(!editingId) return; mut(s=>{ const rec=s.instGroups.find(x=>x.id===editingId); if(rec) Object.assign(rec,draft); logAction(s.me.name,'编辑器具组',editingId,'行内编辑器具组 '+editingId+' '+(draft.name||'')); }); setEditingId(null); setDraft({}); toast.ok('已保存'); };""",
'I1 state+saveEdit')

# 2) 编辑按钮
rep("""      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情</Button>
      {canDo(d.me.role,'edit')&&<Button size="small" type="link" onClick={()=>openEdit(r)}>编辑</Button>}""",
"""      <Button size="small" type="link" onClick={()=>setDetail(r)}>详情</Button>
      {canDo(d.me.role,'edit')&&(editingId===r.id
        ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
        : <Button size="small" type="link" onClick={()=>startEdit(r)}>编辑</Button>)}""",
'I2 编辑按钮')

# 3) 可编辑列
rep("""    {title:'组名称', dataIndex:'name', width:180, ellipsis:true},""",
"""    {title:'组名称', dataIndex:'name', width:180, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},""",
'I3 name')

rep("""    {title:'组类型', width:110, render:(_,r)=><Tag color={(r.type||'inst')==='kappa'?'purple':'blue'} style={{marginRight:0}}>{(r.type||'inst')==='kappa'?'kappa人员组':'测量器具组'}</Tag>},""",
"""    {title:'组类型', width:130, render:(_,r)=>editingId===r.id?<Select size="small" defaultValue={r.type||'inst'} style={{width:120}} options={[{value:'inst',label:'测量器具组'},{value:'kappa',label:'kappa人员组'}]} onChange={x=>setDraft(d=>({...d,type:x}))}/>:<Tag color={(r.type||'inst')==='kappa'?'purple':'blue'} style={{marginRight:0}}>{(r.type||'inst')==='kappa'?'kappa人员组':'测量器具组'}</Tag>},""",
'I4 type')

rep("""    {title:'检验周期(月)', width:110, render:(_,r)=><span className="mono">{r.calCycle||12}</span>},""",
"""    {title:'检验周期(月)', width:110, render:(_,r)=>editingId===r.id?<InputNumber size="small" min={1} defaultValue={r.calCycle||12} style={{width:92}} onChange={x=>setDraft(d=>({...d,calCycle:x}))}/>:<span className="mono">{r.calCycle||12}</span>},""",
'I5 calCycle')

rep("""    {title:'上次执行时间', dataIndex:'lastExec', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},""",
"""    {title:'上次执行时间', dataIndex:'lastExec', width:115, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,lastExec:e.target.value}))}/>:<span className="mono tiny">{v||'暂无'}</span>},""",
'I6 lastExec')

rep("""    {title:'下次计划日期', dataIndex:'nextPlanDate', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},""",
"""    {title:'下次计划日期', dataIndex:'nextPlanDate', width:115, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,nextPlanDate:e.target.value}))}/>:<span className="mono tiny">{v||'暂无'}</span>},""",
'I7 nextPlanDate')

rep("""    {title:'提醒周期(天)', width:105, render:(_,r)=><span className="mono">{r.remindAdvance||20}</span>},""",
"""    {title:'提醒周期(天)', width:115, render:(_,r)=>editingId===r.id?<InputNumber size="small" min={0} defaultValue={r.remindAdvance||20} style={{width:96}} onChange={x=>setDraft(d=>({...d,remindAdvance:x}))}/>:<span className="mono">{r.remindAdvance||20}</span>},""",
'I8 remindAdvance')

rep("""    {title:'下次提醒时间', dataIndex:'nextRemind', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},""",
"""    {title:'下次提醒时间', dataIndex:'nextRemind', width:115, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,nextRemind:e.target.value}))}/>:<span className="mono tiny">{v||'暂无'}</span>},""",
'I9 nextRemind')

rep("""    {title:'说明', dataIndex:'note', ellipsis:true},""",
"""    {title:'说明', dataIndex:'note', ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,note:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'I10 note')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
