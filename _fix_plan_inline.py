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

# state
rep("""  const [edit,setEdit]=useState(null);       // 编辑计划信息""",
"""  const [edit,setEdit]=useState(null);       // 编辑计划信息
  const [editingId,setEditingId]=useState(null); const [draft,setDraft]=useState({});
  const startEdit=(r)=>{ setEditingId(r.id); setDraft({...r}); };
  const saveEdit=()=>{ if(!editingId) return; mut(s=>{ const rec=s.plans.find(x=>x.id===editingId); if(rec) Object.assign(rec,draft); logAction(s.me.name,'编辑MSA计划',editingId,'行内编辑 '+editingId); }); setEditingId(null); setDraft({}); toast.ok('已保存'); };""",
'P1 state+saveEdit')

# PlanActions 编辑按钮
rep("""    <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={onEdit}>编辑</Button>""",
"""    {editingId===r.id
      ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
      : <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>startEdit(r)}>编辑</Button>}""",
'P2 计划编辑按钮')

# 可编辑列
rep("""    {title:'分析人', width:90, render:(_,r)=><span>{r.analyst||r.observer||'暂无'}</span>},""",
"""    {title:'分析人', width:110, render:(_,r)=>editingId===r.id?<Input size="small" defaultValue={r.analyst||r.observer||''} onChange={e=>setDraft(d=>({...d,analyst:e.target.value}))}/>:<span>{r.analyst||r.observer||'暂无'}</span>},""",
'P3 analyst')

rep("""    {title:'零件号', width:100, dataIndex:'partNo', render:v=><span className="mono">{v||'—'}</span>},""",
"""    {title:'零件号', width:100, dataIndex:'partNo', render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,partNo:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'P4 partNo')

rep("""    {title:'测量特性', width:160, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); return (r.instIds||[]).length>1? <span className="tiny">{recs.map(x=>x.object).filter(Boolean).join('、')}</span> : <span>{r.object||'暂无'}</span>; }},""",
"""    {title:'测量特性', width:160, ellipsis:true, render:(_,r)=>{ if(editingId===r.id) return <Input size="small" defaultValue={r.object||''} onChange={e=>setDraft(d=>({...d,object:e.target.value}))}/>; const recs=planRecords(d,r.id); return (r.instIds||[]).length>1? <span className="tiny">{recs.map(x=>x.object).filter(Boolean).join('、')}</span> : <span>{r.object||'暂无'}</span>; }},""",
'P5 object')

rep("""    {title:'数据类型', width:92, render:(_,r)=><Tag color={(r.dataType||'计量型')==='计数型'?'purple':'blue'}>{r.dataType||'计量型'}</Tag>},""",
"""    {title:'数据类型', width:100, render:(_,r)=>editingId===r.id?<Select size="small" defaultValue={r.dataType||'计量型'} style={{width:92}} options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]} onChange={x=>setDraft(d=>({...d,dataType:x}))}/>:<Tag color={(r.dataType||'计量型')==='计数型'?'purple':'blue'}>{r.dataType||'计量型'}</Tag>},""",
'P6 dataType')

rep("""    {title:'操作方法', width:150, render:(_,r)=><span>{r.opMethod||'《测量系统分析操作指导书》'}</span>},""",
"""    {title:'操作方法', width:160, render:(_,r)=>editingId===r.id?<Input size="small" defaultValue={r.opMethod||''} onChange={e=>setDraft(d=>({...d,opMethod:e.target.value}))}/>:<span>{r.opMethod||'《测量系统分析操作指导书》'}</span>},""",
'P7 opMethod')

rep("""    {title:'部门', dataIndex:'dept', width:100, render:v=><span className="tiny">{v||'暂无'}</span>},""",
"""    {title:'部门', dataIndex:'dept', width:100, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,dept:e.target.value}))}/>:<span className="tiny">{v||'暂无'}</span>},""",
'P8 dept')

rep("""    {title:'分厂', width:90, dataIndex:'subplant'},""",
"""    {title:'分厂', width:90, dataIndex:'subplant', render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,subplant:e.target.value}))}/>:<span>{v||'—'}</span>},""",
'P9 subplant')

rep("""    {title:'计划完成时间', dataIndex:'planDate', width:112},""",
"""    {title:'计划完成时间', dataIndex:'planDate', width:120, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,planDate:e.target.value}))}/>:<span className="mono tiny">{v||'暂无'}</span>},""",
'P10 planDate')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
