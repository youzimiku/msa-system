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

# CharPage 检验方法列
rep("""    {title:'检验方法', width:200, render:(_,r)=>editingId===r.id?<Select size="small" mode="multiple" defaultValue={(r.methods||[]).map(m=>m.method)} style={{width:190}} options={anMethods.map(m=>({value:m.code,label:METHOD_NAME(m.code)}))} onChange={x=>setDraft(d=>({...d,methods:x.map(v=>({method:v}))}))}/>:methodView(r)},""",
"""    {title:'检验方法', width:200, render:(_,r)=>editingId===r.id?<Select size="small" mode="multiple" defaultValue={(r.methods||[]).map(m=>m.method)} style={{width:190}} options={(d.anMethods||[]).map(m=>({value:m.code,label:METHOD_NAME(m.code)}))} onChange={x=>setDraft(d=>({...d,methods:x.map(v=>({method:v}))}))}/>:methodView(r)},""",
'F1 CharPage methods')

# SamplingPage 判断规则所属方法列
rep("""    {title:'所属方法', dataIndex:'method', width:130, render:(v,r)=>jEditingId===r.id?<Select size="small" defaultValue={v} style={{width:110}} options={anMethods.map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} onChange={x=>setJDraft(d=>({...d,method:x}))}/>:<span>{METHOD_NAME(v)}</span>},""",
"""    {title:'所属方法', dataIndex:'method', width:130, render:(v,r)=>jEditingId===r.id?<Select size="small" defaultValue={v} style={{width:110}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} onChange={x=>setJDraft(d=>({...d,method:x}))}/>:<span>{METHOD_NAME(v)}</span>},""",
'F2 SamplingPage judgeMethod')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
