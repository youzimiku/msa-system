# -*- coding: utf-8 -*-
"""录入页可调节：KappaEntry 每件多判（多数裁决）+ AnlEntry 线性/稳定性参数可调 + calc 行数自适应"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# ---- A. calcLinear / calcStability 行数自适应 ----
rep("  for(let i=0;i<rec.stds;i++){\n    const row=rec.raw[i]; if(!row||!row.length) return null;",
    "  for(let i=0;i<rec.raw.length;i++){\n    const row=rec.raw[i]; if(!row||!row.length) return null;")
rep("  const n=rec.per||3, A2=SPC_A2[n]||1.023, D4=SPC_D4[n]||2.574;",
    "  const n=(rec.raw[0]||[]).length||rec.per||5, A2=SPC_A2[n]||1.023, D4=SPC_D4[n]||2.574;")

# ---- B. KappaEntry：默认 3 人×50 件×3 判/件（多数裁决） ----
rep("  const numApp=Number(rec.numApp)||2, numSamples= items.length || Number(rec.numSamples)||30;",
    "  const numApp=Number(rec.numApp)||3, numSamples= items.length || Number(rec.numSamples)||50, numTrials=Number(rec.numTrials)||3;")
rep("  const [judg,setJudg]=useState(()=>Array.from({length:numApp},()=>Array.from({length:numSamples},()=>'')));",
    "  const [judg,setJudg]=useState(()=>Array.from({length:numApp},()=>Array.from({length:numSamples},()=>Array.from({length:numTrials},()=>''))));")
rep("  const setCell=(a,s,v)=>{ setJudg(judg.map((x,ia)=>ia===a?x.map((y,is)=>is===s?v:y):x)); };",
    "  const setCell=(a,s,t,v)=>{ setJudg(judg.map((x,ia)=>ia===a?x.map((y,is)=>is===s?y.map((z,it)=>it===t?v:z):y):x)); };")
rep("  const complete = judg.every(a=>a.every(v=>v===0||v===1));",
    "  const complete = judg.every(a=>a.every(s=>s.length&&s.every(v=>v===0||v===1)));")
rep("""    const ref = Array.from({length:numSamples},(_,i)=> i<Math.round(numSamples*0.6)?1:0);
    setJudg(appNames.map((_,ia)=> ref.map((v,i)=>(i%(7+ia*3)===0&&i>0)?(v===1?0:1):v)));""",
"""    const ref = Array.from({length:numSamples},(_,i)=> i<Math.round(numSamples*0.6)?1:0);
    setJudg(appNames.map((_,ia)=> ref.map((v,i)=>Array.from({length:numTrials},(_,t)=>(i%(7+ia*3+t)===0&&i>0)?(v===1?0:1):v))));""")
rep("""    const ref = items.length? items.map(s=>s.refVerdict): Array.from({length:numSamples},(_,i)=> i<Math.round(numSamples*0.6)?1:0);
    const calc=calcKappaRec(Object.assign({}, rec, {reference:ref, appData:judg, appNames, numApp, numSamples}));""",
"""    const ref = items.length? items.map(s=>s.refVerdict): Array.from({length:numSamples},(_,i)=> i<Math.round(numSamples*0.6)?1:0);
    const majority=(arr)=>{ if(!arr||!arr.length) return 0; const ones=arr.filter(v=>v===1).length; return ones>arr.length/2?1:0; };
    const appData=judg.map(a=>a.map(s=>majority(s))); // 每件多次判定 → 多数裁决
    const calc=calcKappaRec(Object.assign({}, rec, {reference:ref, appData, appNames, numApp, numSamples, numTrials}));""")
rep("""  for(let a=0;a<numApp;a++) cols.push({title:appNames[a]||('检验员'+a), dataIndex:'a'+a, width:150,
    render:(v,row)=><Select size="small" style={{width:'100%'}} value={row.j[a]===''?undefined:row.j[a]}
      options={[{value:1,label:'合格'},{value:0,label:'不合格'}]} onChange={v=>setCell(a,row.i,v)} placeholder="判定"/>});""",
"""  for(let a=0;a<numApp;a++) cols.push({title:(appNames[a]||('检验员'+a))+(numTrials>1?('（'+numTrials+'判/件）'):''), dataIndex:'a'+a, width:numTrials*70+16,
    render:(v,row)=><Space size={2}>{Array.from({length:numTrials},(_,tt)=><Select size="small" style={{width:64}} value={row.j[a][tt]===''?undefined:row.j[a][tt]}
      options={[{value:1,label:'合格'},{value:0,label:'不合格'}]} onChange={v=>setCell(a,row.i,tt,v)} placeholder={String(tt+1)}/>)}</Space>});""")
rep("""        <div className="form-hint">每行首列为样本参考判定（专家/标准件仲裁）。<br/>检验员须在不知晓参考判定情况下独立完成判定（盲测）。<br/>检验标准：<span className="mono">{rec.standard||'-'}</span></div>""",
"""        <div className="form-hint">每行首列为样本参考判定（专家/标准件仲裁）。<br/>检验员须在不知晓参考判定情况下独立完成判定（盲测）；每件判定 {numTrials} 次，按多数裁决为该件结论。<br/>取样默认：{numApp} 人 × {numSamples} 件 × {numTrials} 次（业务速查默认 50 件×3 人×3 次，件数/人数/次数可调）。<br/>检验标准：<span className="mono">{rec.standard||'-'}</span></div>""")
rep('<div className="grp-label">判定矩阵（合格/不合格）</div>',
    '<div className="grp-label">判定矩阵（合格/不合格，每件 {numTrials} 判 · 多数裁决）</div>')
rep("        <Table size=\"small\" rowKey=\"i\" dataSource={ds} columns={cols} pagination={false} scroll={{x:numApp*160+130}}/>",
    "        <Table size=\"small\" rowKey=\"i\" dataSource={ds} columns={cols} pagination={false} scroll={{x:numApp*(numTrials*70+16)+140}}/>")

# ---- C. AnlEntry：线性/稳定性参数可调（默认 5×12、25×5），Cg/Cgk 次数可调 ----
rep("""    if(kind==='linear') return {refs:Array.from({length:rec.stds||5},(_,i)=>rec.refs&&rec.refs[i]!==undefined?rec.refs[i]:''), raw:Array.from({length:rec.stds||5},()=>Array.from({length:rec.per||10},()=>''))};
    if(kind==='stability') return {raw:Array.from({length:rec.groups||25},()=>Array.from({length:rec.per||3},()=>''))};""",
"""    if(kind==='linear') return {refs:Array.from({length:rec.stds||5},(_,i)=>rec.refs&&rec.refs[i]!==undefined?rec.refs[i]:''), raw:Array.from({length:rec.stds||5},()=>Array.from({length:rec.per||12},()=>''))};
    if(kind==='stability') return {raw:Array.from({length:rec.groups||25},()=>Array.from({length:rec.per||5},()=>''))};""")
rep("  const [cnt,setCnt]=useState(kind==='stability'?(rec.groups||25):kind==='cgcgk'?(rec.runs||50):0);",
    "  const [cnt,setCnt]=useState(kind==='linear'?(rec.stds||5):kind==='stability'?(rec.groups||25):kind==='cgcgk'?(rec.runs||50):0);\n  const [perN,setPerN]=useState(kind==='linear'?(rec.per||12):kind==='stability'?(rec.per||5):0);")
rep("  const regen=(n)=>{ if(kind==='stability'){ setSt(s=>({...s, raw:Array.from({length:n},()=>Array.from({length:rec.per||3},()=>''))})); } if(kind==='cgcgk'){ setSt(s=>({...s, raw:Array.from({length:n},()=>'')})); } };",
    "  const regen=()=>{ if(kind==='linear'){ setSt(s=>({...s, raw:Array.from({length:cnt||5},()=>Array.from({length:perN||12},()=>'')), refs:Array.from({length:cnt||5},(_,i)=>s.refs&&s.refs[i]!==undefined?s.refs[i]:'')})); } if(kind==='stability'){ setSt(s=>({...s, raw:Array.from({length:cnt||25},()=>Array.from({length:perN||5},()=>''))})); } if(kind==='cgcgk'){ setSt(s=>({...s, raw:Array.from({length:cnt||50},()=>'')})); } };")
rep("""    {(kind==='stability'||kind==='cgcgk') && <Space style={{marginBottom:12}}><span className="flt-label">数据行数（默认按规则生成，可增减）</span>
      <InputNumber size="small" min={1} max={200} value={cnt} onChange={v=>setCnt(v||1)}/>
      <Button size="small" onClick={()=>{ setCnt(cnt); regen(cnt); }}>重新生成 {cnt} 行</Button></Space>}""",
"""    {(kind==='linear'||kind==='stability'||kind==='cgcgk') && <Space style={{marginBottom:12}} wrap>
      <span className="flt-label">{kind==='linear'?'标准件数':kind==='stability'?'子组数':'测量次数'}</span>
      <InputNumber size="small" min={kind==='stability'?25:1} max={kind==='cgcgk'?200:100} value={cnt} onChange={v=>setCnt(v||1)}/>
      {kind!=='cgcgk' && <><span className="flt-label">{kind==='linear'?'每件次数':'每期次数'}</span>
      <InputNumber size="small" min={1} max={20} value={perN} onChange={v=>setPerN(v||1)}/></>}
      <Button size="small" onClick={regen}>重新生成（默认 {kind==='linear'?'5 件 × 12 次':kind==='stability'?'25 子组 × 5 次':'50 次'}）</Button>
      <span className="tiny">（业务速查默认值，可调整后重新生成录入矩阵）</span></Space>}""")
rep("""    {kind==='linear' && <div style={{maxHeight:430, overflow:'auto'}}>{label('标准件测量（每件 10 次，覆盖 0/25/50/75/100% 量程点）','参考值=鉴定证书/高等级量具真值')}
      <table className="mono-grid"><thead><tr><th>标准件</th><th>参考值</th>{Array.from({length:rec.per||10},(_,j)=><th key={j}>测{j+1}</th>)}</tr></thead>
      <tbody>{st.raw.map((row,i)=><tr key={i}><td>{'STD-'+String(i+1).padStart(2,'0')}（{(i*25)}%量程）</td>""",
"""    {kind==='linear' && <div style={{maxHeight:430, overflow:'auto'}}>{label('标准件测量（每件 '+perN+' 次可调，覆盖 0~100% 量程）','参考值=鉴定证书/高等级量具真值')}
      <table className="mono-grid"><thead><tr><th>标准件</th><th>参考值</th>{Array.from({length:perN||12},(_,j)=><th key={j}>测{j+1}</th>)}</tr></thead>
      <tbody>{st.raw.map((row,i)=><tr key={i}><td>{'STD-'+String(i+1).padStart(2,'0')}（{Math.round(100*i/(Math.max(1,(cnt||5)-1)))}%量程）</td>""")
rep("""    {kind==='stability' && <div style={{maxHeight:430, overflow:'auto'}}>{label('稳定性子组测量（25 子组 × 每期 3~5 次，跨 4 周~3 个月）','固定参照仪/工位，SPC 判异模型')}
      <table className="mono-grid"><thead><tr><th>子组</th>{Array.from({length:rec.per||3},(_,j)=><th key={j}>测{j+1}</th>)}<th>X̄</th><th>R</th></tr></thead>""",
"""    {kind==='stability' && <div style={{maxHeight:430, overflow:'auto'}}>{label('稳定性子组测量（'+cnt+' 子组 × 每期 '+perN+' 次可调，跨 4 周~3 个月）','固定参照仪/工位，SPC 判异模型')}
      <table className="mono-grid"><thead><tr><th>子组</th>{Array.from({length:perN||5},(_,j)=><th key={j}>测{j+1}</th>)}<th>X̄</th><th>R</th></tr></thead>""")

open(p, 'w', encoding='utf-8').write(s)
print('step3 OK, len:', len(s))
