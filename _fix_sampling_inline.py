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
rep("""  const [selMethod,setSelMethod]=useState();""",
"""  const [selMethod,setSelMethod]=useState();
  const [mEditingId,setMEditingId]=useState(null); const [mDraft,setMDraft]=useState({});
  const [jEditingId,setJEditingId]=useState(null); const [jDraft,setJDraft]=useState({});
  const startMEdit=(r)=>{ setMEditingId(r.code); setMDraft({...r, rule: r.rule?{...r.rule}:null}); };
  const saveMEdit=()=>{ if(!mEditingId) return; mut(s=>{ const rec=s.anMethods.find(x=>x.code===mEditingId); if(rec) Object.assign(rec, mDraft, {rule:undefined}); if(mDraft.rule){ const rule=s.samplingRules.find(x=>String(x.method).toLowerCase()===String(mEditingId).toLowerCase()); if(rule) Object.assign(rule, mDraft.rule); } logAction(s.me.name,'编辑分析方法',mEditingId,'行内编辑 '+mEditingId+' '+(mDraft.name||'')); }); setMEditingId(null); setMDraft({}); toast.ok('已保存'); };
  const startJEdit=(r)=>{ setJEditingId(r.id); setJDraft({...r}); };
  const saveJEdit=()=>{ if(!jEditingId) return; mut(s=>{ const rec=s.judgeRules.find(x=>x.id===jEditingId); if(rec) Object.assign(rec,jDraft); logAction(s.me.name,'编辑判断规则',jEditingId,'行内编辑 '+jEditingId); }); setJEditingId(null); setJDraft({}); toast.ok('已保存'); };""",
'S1 state+saveEdit')

# 分析方法列表 编辑按钮
rep("""    {title:'操作', width:90, fixed:'left', render:(_,r)=><Button size="small" type="link" onClick={()=> r.rule? setRModal({record:r.rule}) : setMModal({record:r})}>编辑</Button>},""",
"""    {title:'操作', width:90, fixed:'left', render:(_,r)=>mEditingId===r.code
      ? <><Button size="small" type="link" onClick={saveMEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setMEditingId(null);setMDraft({});}}>取消</Button></>
      : <Button size="small" type="link" onClick={()=>startMEdit(r)}>编辑</Button>},""",
'S2 方法编辑按钮')

# 分析方法列表 可编辑列（方法字段）
rep("""    {title:'方法名称', dataIndex:'name', width:210, render:v=><span>{STRIP_PAREN(v)}</span>},""",
"""    {title:'方法名称', dataIndex:'name', width:220, render:(v,r)=>mEditingId===r.code?<Input size="small" defaultValue={v} onChange={e=>setMDraft(d=>({...d,name:e.target.value}))}/>:<span>{STRIP_PAREN(v)}</span>},""",
'S3 name')

rep("""    {title:'是否需要取样', dataIndex:'needSample', width:100},
    {title:'可否合并取样', dataIndex:'canMerge', width:100},""",
"""    {title:'是否需要取样', dataIndex:'needSample', width:110, render:(v,r)=>mEditingId===r.code?<Select size="small" defaultValue={v} style={{width:90}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setMDraft(d=>({...d,needSample:x}))}/>:<span>{v}</span>},
    {title:'可否合并取样', dataIndex:'canMerge', width:110, render:(v,r)=>mEditingId===r.code?<Select size="small" defaultValue={v} style={{width:90}} options={[{value:'是',label:'是'},{value:'否',label:'否'}]} onChange={x=>setMDraft(d=>({...d,canMerge:x}))}/>:<span>{v||'—'}</span>},""",
'S4 needSample/canMerge')

rep("""    {title:'合并对象', dataIndex:'mergeWith', width:90, render:v=><span>{v||'—'}</span>},
    {title:'默认适用', dataIndex:'defaultType', width:90},
    {title:'状态', dataIndex:'status', width:80, render:v=><Tag color={v==='启用'?'green':'default'} style={{marginRight:0}}>{v}</Tag>},""",
"""    {title:'合并对象', dataIndex:'mergeWith', width:100, render:(v,r)=>mEditingId===r.code?<Input size="small" defaultValue={v} onChange={e=>setMDraft(d=>({...d,mergeWith:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'默认适用', dataIndex:'defaultType', width:100, render:(v,r)=>mEditingId===r.code?<Input size="small" defaultValue={v} onChange={e=>setMDraft(d=>({...d,defaultType:e.target.value}))}/>:<span>{v||'—'}</span>},
    {title:'状态', dataIndex:'status', width:100, render:(v,r)=>mEditingId===r.code?<Select size="small" defaultValue={v} style={{width:90}} options={[{value:'启用',label:'启用'},{value:'停用',label:'停用'}]} onChange={x=>setMDraft(d=>({...d,status:x}))}/>:<Tag color={v==='启用'?'green':'default'} style={{marginRight:0}}>{v}</Tag>},""",
'S5 mergeWith/defaultType/status')

# 分析方法列表 可编辑列（取样规则字段）
rep("""    {title:'策略类别', width:90, render:(_,r)=>r.rule?r.rule.category:'—'},
    {title:'默认样品数', width:96, render:(_,r)=><span className="mono">{r.rule?r.rule.sampleDefault:'—'}</span>},
    {title:'默认人数', width:88, render:(_,r)=><span className="mono">{r.rule?r.rule.opsDefault:'—'}</span>},
    {title:'默认次数', width:88, render:(_,r)=><span className="mono">{r.rule?r.rule.trialsDefault:'—'}</span>},
    {title:'样品数范围', width:100, render:(_,r)=><span className="mono">{r.rule?r.rule.sampleMin+'~'+r.rule.sampleMax:'—'}</span>},
    {title:'人数范围', width:88, render:(_,r)=><span className="mono">{r.rule?r.rule.opsMin+'~'+r.rule.opsMax:'—'}</span>},
    {title:'次数范围', width:88, render:(_,r)=><span className="mono">{r.rule?r.rule.trialsMin+'~'+r.rule.trialsMax:'—'}</span>},
    {title:'读数建议', width:90, render:(_,r)=><span className="mono">{r.rule?(r.rule.readings||'—'):'—'}</span>},
    {title:'工厂', width:90, render:(_,r)=>r.rule?r.rule.plant:'—'},
    {title:'车间', width:80, render:(_,r)=>r.rule?r.rule.subplant:'—'},
    {title:'取样策略说明', width:300, ellipsis:true, render:(_,r)=>r.rule?r.rule.note:'—'},""",
"""    {title:'策略类别', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<Input size="small" defaultValue={r.rule.category} onChange={e=>setMDraft(d=>({...d,rule:{...(d.rule||{}),category:e.target.value}}))}/>:<span>{r.rule?r.rule.category:'—'}</span>},
    {title:'默认样品数', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<InputNumber size="small" min={0} defaultValue={r.rule.sampleDefault} style={{width:88}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),sampleDefault:x}}))}/>:<span className="mono">{r.rule?r.rule.sampleDefault:'—'}</span>},
    {title:'默认人数', width:90, render:(_,r)=>mEditingId===r.code&&r.rule?<InputNumber size="small" min={0} defaultValue={r.rule.opsDefault} style={{width:80}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),opsDefault:x}}))}/>:<span className="mono">{r.rule?r.rule.opsDefault:'—'}</span>},
    {title:'默认次数', width:90, render:(_,r)=>mEditingId===r.code&&r.rule?<InputNumber size="small" min={0} defaultValue={r.rule.trialsDefault} style={{width:80}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),trialsDefault:x}}))}/>:<span className="mono">{r.rule?r.rule.trialsDefault:'—'}</span>},
    {title:'样品数范围', width:110, render:(_,r)=>mEditingId===r.code&&r.rule?<Space size={2}><InputNumber size="small" min={0} defaultValue={r.rule.sampleMin} style={{width:50}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),sampleMin:x}}))}/><span>~</span><InputNumber size="small" min={0} defaultValue={r.rule.sampleMax} style={{width:50}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),sampleMax:x}}))}/></Space>:<span className="mono">{r.rule?r.rule.sampleMin+'~'+r.rule.sampleMax:'—'}</span>},
    {title:'人数范围', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<Space size={2}><InputNumber size="small" min={0} defaultValue={r.rule.opsMin} style={{width:46}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),opsMin:x}}))}/><span>~</span><InputNumber size="small" min={0} defaultValue={r.rule.opsMax} style={{width:46}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),opsMax:x}}))}/></Space>:<span className="mono">{r.rule?r.rule.opsMin+'~'+r.rule.opsMax:'—'}</span>},
    {title:'次数范围', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<Space size={2}><InputNumber size="small" min={0} defaultValue={r.rule.trialsMin} style={{width:46}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),trialsMin:x}}))}/><span>~</span><InputNumber size="small" min={0} defaultValue={r.rule.trialsMax} style={{width:46}} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),trialsMax:x}}))}/></Space>:<span className="mono">{r.rule?r.rule.trialsMin+'~'+r.rule.trialsMax:'—'}</span>},
    {title:'读数建议', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<Input size="small" defaultValue={r.rule.readings} onChange={e=>setMDraft(d=>({...d,rule:{...(d.rule||{}),readings:e.target.value}}))}/>:<span className="mono">{r.rule?(r.rule.readings||'—'):'—'}</span>},
    {title:'工厂', width:100, render:(_,r)=>mEditingId===r.code&&r.rule?<Select size="small" defaultValue={r.rule.plant} style={{width:90}} options={PLANTS_OPT} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),plant:x}}))}/>:<span>{r.rule?r.rule.plant:'—'}</span>},
    {title:'车间', width:90, render:(_,r)=>mEditingId===r.code&&r.rule?<Select size="small" defaultValue={r.rule.subplant} style={{width:80}} options={SUBPLANTS_OPT} onChange={x=>setMDraft(d=>({...d,rule:{...(d.rule||{}),subplant:x}}))}/>:<span>{r.rule?r.rule.subplant:'—'}</span>},
    {title:'取样策略说明', width:300, ellipsis:true, render:(_,r)=>mEditingId===r.code&&r.rule?<Input size="small" defaultValue={r.rule.note} onChange={e=>setMDraft(d=>({...d,rule:{...(d.rule||{}),note:e.target.value}}))}/>:<span>{r.rule?r.rule.note:'—'}</span>},""",
'S6 取样规则字段')

rep("""    {title:'方法备注', dataIndex:'note', width:200, ellipsis:true}
  ];""",
"""    {title:'方法备注', dataIndex:'note', width:200, ellipsis:true, render:(v,r)=>mEditingId===r.code?<Input size="small" defaultValue={v} onChange={e=>setMDraft(d=>({...d,note:e.target.value}))}/>:<span>{v||'—'}</span>}
  ];""",
'S7 note')

# 判断规则列表 编辑按钮 + 可编辑列
rep("""    {title:'操作', width:90, fixed:'left', render:(_,r)=><Button size="small" type="link" onClick={()=>setJModal({record:r})}>编辑</Button>},""",
"""    {title:'操作', width:90, fixed:'left', render:(_,r)=>jEditingId===r.id
      ? <><Button size="small" type="link" onClick={saveJEdit}>保存</Button><Button size="small" type="link" onClick={()=>{setJEditingId(null);setJDraft({});}}>取消</Button></>
      : <Button size="small" type="link" onClick={()=>startJEdit(r)}>编辑</Button>},""",
'S8 判断编辑按钮')

rep("""    {title:'所属方法', dataIndex:'method', width:120, render:v=><span>{METHOD_NAME(v)}</span>},
    {title:'判定条件', dataIndex:'condition', width:320, ellipsis:true},
    {title:'判定结论', dataIndex:'verdict', width:150},
    {title:'说明', dataIndex:'note', width:460, ellipsis:true}
  ];""",
"""    {title:'所属方法', dataIndex:'method', width:130, render:(v,r)=>jEditingId===r.id?<Select size="small" defaultValue={v} style={{width:110}} options={anMethods.map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} onChange={x=>setJDraft(d=>({...d,method:x}))}/>:<span>{METHOD_NAME(v)}</span>},
    {title:'判定条件', dataIndex:'condition', width:320, ellipsis:true, render:(v,r)=>jEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setJDraft(d=>({...d,condition:e.target.value}))}/>:<span>{v}</span>},
    {title:'判定结论', dataIndex:'verdict', width:150, render:(v,r)=>jEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setJDraft(d=>({...d,verdict:e.target.value}))}/>:<span>{v}</span>},
    {title:'说明', dataIndex:'note', width:460, ellipsis:true, render:(v,r)=>jEditingId===r.id?<Input size="small" defaultValue={v} onChange={e=>setJDraft(d=>({...d,note:e.target.value}))}/>:<span>{v||'—'}</span>}
  ];""",
'S9 判断规则列')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
