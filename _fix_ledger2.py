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

# L3 编辑按钮（LedgerPage 上下文：查看按钮后）
rep("""      <Button size="small" type="link" onClick={()=>setDetail(r)}>查看</Button>
      {canDo(d.me.role,'edit')&&<Button size="small" type="link" onClick={()=>openEdit(r)}>编辑</Button>}""",
"""      <Button size="small" type="link" onClick={()=>setDetail(r)}>查看</Button>
      {canDo(d.me.role,'edit')&&(editingId===r.id
        ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
        : <Button size="small" type="link" onClick={()=>startEdit(r)}>编辑</Button>)}""",
'L3 编辑按钮(台账)')

# L5 model 列（LedgerPage：name 列后）
rep("""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},
    {title:'型号', dataIndex:'model', width:100, ellipsis:true},""",
"""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,name:e.target.value}))}/>:<span>{v}</span>},
    {title:'型号', dataIndex:'model', width:100, ellipsis:true, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,model:e.target.value}))}/>:<span>{v}</span>},""",
'L5 model(台账)')

# L17 status 列（LedgerPage：所属器具组列后 + 数组结尾）
rep("""    {title:'所属器具组', width:130, render:(_,r)=>{ const gs=d.instGroups.filter(g=>(g.memberIds||[]).indexOf(r.id)>=0); return gs.length? <span className="tiny">{gs.map(g=>g.name).join('、')}</span> : <span className="tiny">未分组</span>; }},
    {title:'状态', dataIndex:'status', width:90, render:s=><StatusTag s={s}/>}
  ];""",
"""    {title:'所属器具组', width:130, render:(_,r)=>{ const gs=d.instGroups.filter(g=>(g.memberIds||[]).indexOf(r.id)>=0); return gs.length? <span className="tiny">{gs.map(g=>g.name).join('、')}</span> : <span className="tiny">未分组</span>; }},
    {title:'状态', dataIndex:'status', width:110, render:(s,r)=>editingId===r.id?<Select size="small" defaultValue={s} style={{width:100}} options={ENUM.instStatus.map(c=>({value:c,label:c}))} onChange={x=>setDraft(d=>({...d,status:x}))}/>:<StatusTag s={s}/>}
  ];""",
'L17 status(台账)')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
