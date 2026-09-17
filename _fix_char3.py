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

# unit 列锚点：检验方法(methods inline) 后
rep("""onChange={x=>setDraft(d=>({...d,methods:x.map(v=>({method:v}))}))}/>:methodView(r)},
    {title:'单位', dataIndex:'unit', width:64, render:v=><span className="mono">{v||'—'}</span>},""",
"""onChange={x=>setDraft(d=>({...d,methods:x.map(v=>({method:v}))}))}/>:methodView(r)},
    {title:'单位', dataIndex:'unit', width:70, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,unit:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C11 unit(特性)')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
