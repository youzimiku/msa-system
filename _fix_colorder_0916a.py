# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

old = """          columns={[
            {title:'分析方法', width:120, render:(_,r)=><Tag color={ANAL_COLOR[r.method]} style={{marginRight:0,width:76,textAlign:'center'}}>{ANAL_SHORT[r.method]}</Tag>},
            {title:'人数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); if(!sd.useOps) return <span className="tiny">—</span>; return <InputNumber size="small" min={sd.opsMin} max={sd.opsMax} style={{width:88}} value={r.ops} onChange={v=>setRow(r.method,{ops:v})}/>; }},
            {title:'次数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.trialsMin} max={sd.trialsMax} style={{width:88}} value={r.trials} onChange={v=>setRow(r.method,{trials:v})}/>; }},
            {title:'样本数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.partsMin} max={sd.partsMax} style={{width:88}} value={r.parts} onChange={v=>setRow(r.method,{parts:v})}/>; }},
            {title:'操作', width:110, render:(_,r)=><Space size={0}>
              <Button size="small" type="link" onClick={()=>saveRow(r)}>保存</Button>
              <Button size="small" type="link" danger onClick={()=>delRow(r)}>删除</Button>
            </Space>}
          ]}/>"""
new = """          columns={[
            {title:'操作', width:110, render:(_,r)=><Space size={0}>
              <Button size="small" type="link" onClick={()=>saveRow(r)}>保存</Button>
              <Button size="small" type="link" danger onClick={()=>delRow(r)}>删除</Button>
            </Space>},
            {title:'分析方法', width:120, render:(_,r)=><Tag color={ANAL_COLOR[r.method]} style={{marginRight:0,width:76,textAlign:'center'}}>{ANAL_SHORT[r.method]}</Tag>},
            {title:'人数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); if(!sd.useOps) return <span className="tiny">—</span>; return <InputNumber size="small" min={sd.opsMin} max={sd.opsMax} style={{width:88}} value={r.ops} onChange={v=>setRow(r.method,{ops:v})}/>; }},
            {title:'次数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.trialsMin} max={sd.trialsMax} style={{width:88}} value={r.trials} onChange={v=>setRow(r.method,{trials:v})}/>; }},
            {title:'样本数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.partsMin} max={sd.partsMax} style={{width:88}} value={r.parts} onChange={v=>setRow(r.method,{parts:v})}/>; }},
          ]}/>"""
assert t.count(old) == 1, 'columns 锚点不唯一/不存在: ' + str(t.count(old))
t = t.replace(old, new)
io.open(P, 'w', encoding='utf-8').write(t)
print('操作列已移至最前')
