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

# 特性列表 unit（锚点：category 列已替换为 inline 版本）
rep("""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,category:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'单位', dataIndex:'unit', width:64, render:v=><span className="mono">{v||'—'}</span>},""",
"""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,category:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'单位', dataIndex:'unit', width:70, render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,unit:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},""",
'C11 unit(特性)')

# 特性列表 plant/subplant（锚点：lsl 列已替换）
rep("""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,lsl:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},
    {title:'工厂', dataIndex:'plant', width:90, ellipsis:true, render:v=><span>{v||'—'}</span>},
    {title:'车间', dataIndex:'subplant', width:80, ellipsis:true, render:v=><span>{v||'—'}</span>},""",
"""render:(v,r)=>editingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setDraft(d=>({...d,lsl:e.target.value}))}/>:<span className="mono">{v||'—'}</span>},
    {title:'工厂', dataIndex:'plant', width:110, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:100}} options={PLANTS_OPT} onChange={x=>setDraft(d=>({...d,plant:x}))}/>:<span>{v||'—'}</span>},
    {title:'车间', dataIndex:'subplant', width:100, render:(v,r)=>editingId===r.id?<Select size="small" defaultValue={v} style={{width:90}} options={SUBPLANTS_OPT} onChange={x=>setDraft(d=>({...d,subplant:x}))}/>:<span>{v||'—'}</span>},""",
'C15/16 plant/subplant(特性)')

# 标准列表 numOps/numTrials/numParts/分析类型/version（锚点：method 列已替换）
rep("""render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,method:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'测量人数', dataIndex:'numOps', width:80},
    {title:'测量次数', dataIndex:'numTrials', width:80},
    {title:'样本数量', dataIndex:'numParts', width:80},
    {title:'分析类型', width:84, render:(_,r)=><Tag color="blue">{r.type}</Tag>},""",
"""render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,method:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'测量人数', dataIndex:'numOps', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numOps:x}))}/>:<span>{v}</span>},
    {title:'测量次数', dataIndex:'numTrials', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numTrials:x}))}/>:<span>{v}</span>},
    {title:'样本数量', dataIndex:'numParts', width:80, render:(v,r)=>stdEditingId===r.id?<InputNumber size="small" min={1} defaultValue={v} style={{width:70}} onChange={x=>setStdDraft(d=>({...d,numParts:x}))}/>:<span>{v}</span>},
    {title:'分析类型', width:110, render:(_,r)=>stdEditingId===r.id?<Select size="small" defaultValue={r.type} style={{width:100}} options={['GRR判定','NDC判定','KAPPA判定','有效性判定','偏倚/线性判定','稳定性判定'].map(c=>({value:c,label:c}))} onChange={x=>setStdDraft(d=>({...d,type:x}))}/>:<Tag color="blue">{r.type}</Tag>},""",
'C22-25 标准取样参数(标准)')

# 标准列表 version（锚点：状态列已替换为 stdEditingId 版本）
rep("""{title:'版本', dataIndex:'version', width:70, render:v=><Tag color="purple">{v}</Tag>},
    {title:'状态', dataIndex:'status', width:100, render:(s,r)=>stdEditingId===r.id?<Select size="small" defaultValue={s} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setStdDraft(d=>({...d,status:x}))}/>:<StatusTag s={s}/>}
  ];""",
"""{title:'版本', dataIndex:'version', width:80, render:(v,r)=>stdEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setStdDraft(d=>({...d,version:e.target.value}))}/>:<Tag color="purple">{v}</Tag>},
    {title:'状态', dataIndex:'status', width:100, render:(s,r)=>stdEditingId===r.id?<Select size="small" defaultValue={s} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setStdDraft(d=>({...d,status:x}))}/>:<StatusTag s={s}/>}
  ];""",
'C26 version(标准)')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
