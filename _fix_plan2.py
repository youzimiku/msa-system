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

# 1) PlanActions 签名加 props
rep("""function PlanActions({r, onDetail, onEdit}){""",
"""function PlanActions({r, onDetail, onEdit, editingId, startEdit, saveEdit, cancelEdit}){""",
'PA1 签名')

# 2) 取消按钮用 props（避免引用 PlanPage 局部变量）
rep("""      ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setEditingId(null);setDraft({});}}>取消</Button></>
      : <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>startEdit(r)}>编辑</Button>}""",
"""      ? <><Button size="small" type="link" onClick={saveEdit}>保存</Button><Button size="small" type="link" onClick={cancelEdit}>取消</Button></>
      : <Button size="small" type="link" disabled={!canDo(d.me.role,'edit')} onClick={()=>startEdit(r)}>编辑</Button>}""",
'PA2 取消props')

# 3) 操作列调用处传 props
rep("""    {title:'操作', width:150, fixed:'left', render:(_,r)=><PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)}/>},""",
"""    {title:'操作', width:150, fixed:'left', render:(_,r)=><PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)} editingId={editingId} startEdit={startEdit} saveEdit={saveEdit} cancelEdit={()=>{setEditingId(null);setDraft({});}}/>},""",
'PA3 调用处props')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
