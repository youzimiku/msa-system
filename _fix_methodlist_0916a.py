# -*- coding: utf-8 -*-
import datetime, io, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
P = ROOT + r'\index.html'
t = io.open(P, encoding='utf-8').read()

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
snap = ROOT + r'\index_备份_' + ts + '_分析方法列表化前.html'
shutil.copy2(P, snap)
print('快照:', snap)

def rep(old, new, tag):
    global t
    assert t.count(old) == 1, '锚点不唯一/不存在: ' + tag + ' (count=' + str(t.count(old)) + ')'
    t = t.replace(old, new)
    print('OK:', tag)

# 1) 新增 methodRows state
rep(
"  const [qualityChar,setQualityChar]=useState('');",
"  const [qualityChar,setQualityChar]=useState('');\n  const [methodRows,setMethodRows]=useState([]);",
"methodRows state")

# 2) pickChar：不自动勾选（删 setChecked(ms)），切换被测参数清空列表
rep(
"    const ms = c.methods&&c.methods.length? c.methods.map(x=>typeof x==='string'?x:(x.method||'')).filter(Boolean) : ((c.dataType==='计数型')?['KAPPA']:['GRR']);\n    setChecked(ms);",
"    const ms = c.methods&&c.methods.length? c.methods.map(x=>typeof x==='string'?x:(x.method||'')).filter(Boolean) : ((c.dataType==='计数型')?['KAPPA']:['GRR']);\n    setMethodRows([]);",
"pickChar 不自动勾选+清列表")

# 3) pickGroup：切换器具组清空列表
rep(
"  const pickGroup=(gid)=>{\n    setCurGroup(gid);\n    setSelKeys([]);\n  };",
"  const pickGroup=(gid)=>{\n    setCurGroup(gid);\n    setSelKeys([]);\n    setMethodRows([]);\n  };",
"pickGroup 清列表")

# 4) subRuleText 后新增 methodList + 确定/行编辑/保存/删除函数
rep(
"    if(an==='cgcgk') return trials+' 次';\n    return '不取样，直接录入'; };",
"    if(an==='cgcgk') return trials+' 次';\n    return '不取样，直接录入'; };\n  const methodList = isPersonGroup? ['KAPPA'] : charMethods;\n  /* 确定：把勾选中且未入列表的方法加入配置列表（不允许重复添加） */\n  const addMethods=()=>{\n    const list=methodList.filter(m=>checked.indexOf(m)>=0 && !methodRows.some(r=>r.method===m));\n    if(!list.length){ toast.warn('请先勾选未加入列表的分析方法'); return; }\n    const rows=list.map(m=>{ const sd=samplingDef(m); const c=mCfg[m]||{};\n      return {method:m, std:(c.std||''), ops:sd.useOps?(c.ops!==undefined?c.ops:sd.ops):undefined, trials:(c.trials!==undefined?c.trials:sd.trials), parts:(c.parts!==undefined?c.parts:sd.parts), saved:false}; });\n    setMethodRows(rs=>rs.concat(rows));\n  };\n  /* 行内编辑受控更新 */\n  const setRow=(m,patch)=>setMethodRows(rs=>rs.map(r=>r.method===m?{...r,...patch}:r));\n  /* 保存当前行配置 */\n  const saveRow=(r)=>{ setMethodRows(rs=>rs.map(x=>x.method===r.method?{...x,saved:true}:x)); toast.ok(ANAL_SHORT[r.method]+' 配置已保存'); };\n  /* 删除行：联动取消勾选（无二次确认） */\n  const delRow=(r)=>{ setMethodRows(rs=>rs.filter(x=>x.method!==r.method)); setChecked(c=>c.filter(x=>x!==r.method)); };",
"方法列表函数")

# 5) submit：改用已保存行
rep(
"  const submit=()=>{\n    if(!charSel){ toast.warn('请选择被测参数'); return; }\n    const effMethods=isPersonGroup?['KAPPA']:charMethods;\n    const effChecked=isPersonGroup?['KAPPA']:checked;\n    const acts=effMethods.filter(m=>effChecked.indexOf(m)>=0);\n    if(!acts.length){ toast.warn('请至少勾选一个分析方法'); return; }\n    for(const m of acts){\n      const sd=samplingDef(m); const c=mCfg[m]||{};\n      const ops=c.ops!==undefined?c.ops:sd.ops, trials=c.trials!==undefined?c.trials:sd.trials, parts=c.parts!==undefined?c.parts:sd.parts;\n      if(ops<sd.opsMin||ops>sd.opsMax||trials<sd.trialsMin||trials>sd.trialsMax||parts<sd.partsMin||parts>sd.partsMax){ toast.warn('分析方法 '+ANAL_SHORT[m]+' 取样参数超出允许范围（人数 '+sd.opsMin+'~'+sd.opsMax+'、次数 '+sd.trialsMin+'~'+sd.trialsMax+'、样本数 '+sd.partsMin+'~'+sd.partsMax+'），请调整'); return; }\n    }",
"  const submit=()=>{\n    if(!charSel){ toast.warn('请选择被测参数'); return; }\n    const savedRows=methodRows.filter(r=>r.saved);\n    const acts=savedRows.map(r=>r.method);\n    if(!acts.length){ toast.warn('请先在上方勾选分析方法并点击「确定」加入列表，然后在列表中保存至少一个方法的配置'); return; }\n    for(const r of savedRows){\n      const m=r.method; const sd=samplingDef(m);\n      const ops=r.ops, trials=r.trials, parts=r.parts;\n      if((sd.useOps&&(ops<sd.opsMin||ops>sd.opsMax))||trials<sd.trialsMin||trials>sd.trialsMax||parts<sd.partsMin||parts>sd.partsMax){ toast.warn('分析方法 '+ANAL_SHORT[m]+' 取样参数超出允许范围（人数 '+sd.opsMin+'~'+sd.opsMax+'、次数 '+sd.trialsMin+'~'+sd.trialsMax+'、样本数 '+sd.partsMin+'~'+sd.partsMax+'），请调整'); return; }\n    }",
"submit 改用已保存行")

# 6) mkP 改用列表行
rep(
"        const mkP=(an)=>{ const c=mCfg[an]||{}; const ops=Number(c.ops)||3, trials=Number(c.trials)||3, parts=Number(c.parts)||10;",
"        const mkP=(an)=>{ const r=savedRows.find(x=>x.method===an); const ops=Number(r?r.ops:undefined)||3, trials=Number(r?r.trials:undefined)||3, parts=Number(r?r.parts:undefined)||10;",
"mkP 用列表行")

# 7) standard 字段（计划主行 + 台账行）
rep(
"methods:acts.slice(), standard:mCfg[acts[0]].std, params:mkP(acts[0]),",
"methods:acts.slice(), standard:(savedRows.find(r=>r.method===acts[0])||{}).std||'', params:mkP(acts[0]),",
"standard 主行")
rep(
"        acts.forEach(an=>{ spawnRecord(s, pid, {type:an, instId:skey, instName:fullName, object:charObj?charObj.name:'', standard:mCfg[an].std, method:ENUM.taskMethod[an][0], params:mkP(an), feature:charObj?charObj.type:'', charId:charSel, note:''}); });",
"        acts.forEach(an=>{ spawnRecord(s, pid, {type:an, instId:skey, instName:fullName, object:charObj?charObj.name:'', standard:(savedRows.find(r=>r.method===an)||{}).std||'', method:ENUM.taskMethod[an][0], params:mkP(an), feature:charObj?charObj.type:'', charId:charSel, note:''}); });",
"standard 台账行")

# 8) 分析方法模块 JSX 整体替换
rep(
"""      {charSel && <>
        <div style={{marginBottom:8}}><Checkbox.Group size="small" disabled={isPersonGroup} value={isPersonGroup?['KAPPA']:checked} options={(isPersonGroup?['KAPPA']:charMethods).map(m=>({value:m,label:ANAL_SHORT[m]+'（'+subRuleText(m)+'）'}))} onChange={setChecked}/></div>
        {(isPersonGroup?['KAPPA']:charMethods).filter(m=>(isPersonGroup?['KAPPA']:checked).indexOf(m)>=0).map(m=>{
          const c=mCfg[m]||{};
          const sd=samplingDef(m);
          const ops=c.ops!==undefined?c.ops:sd.ops, trials=c.trials!==undefined?c.trials:sd.trials, parts=c.parts!==undefined?c.parts:sd.parts;
          return <div key={m} style={{display:'flex', gap:12, alignItems:'center', flexWrap:'wrap', padding:'6px 0', borderTop:'1px solid #f0f0f0'}}>
            <Tag color={ANAL_COLOR[m]} style={{marginRight:0,width:66,textAlign:'center'}}>{ANAL_SHORT[m]}</Tag>
            {sd.useOps && <><span className="flt-label">人数</span><InputNumber size="small" min={sd.opsMin} max={sd.opsMax} style={{width:70}} value={ops} onChange={v=>setM(m,{ops:v})}/></>}
            <span className="flt-label">次数</span><InputNumber size="small" min={sd.trialsMin} max={sd.trialsMax} style={{width:70}} value={trials} onChange={v=>setM(m,{trials:v})}/>
            <span className="flt-label">样本数</span><InputNumber size="small" min={sd.partsMin} max={sd.partsMax} style={{width:70}} value={parts} onChange={v=>setM(m,{parts:v})}/>
          </div>;
        })}
      </>}""",
"""      {charSel && <>
        <div style={{marginBottom:8, display:'flex', alignItems:'center', gap:12, flexWrap:'wrap'}}>
          <Checkbox.Group size="small" value={checked} options={methodList.map(m=>({value:m,label:ANAL_SHORT[m]+'（'+subRuleText(m)+'）', disabled:methodRows.some(r=>r.method===m)}))} onChange={setChecked}/>
          <Button size="small" type="primary" onClick={addMethods}>确定</Button>
        </div>
        <Table size="small" rowKey="method" pagination={false} dataSource={methodRows}
          locale={{emptyText:'未添加分析方法，请在上方勾选后点击「确定」'}}
          columns={[
            {title:'分析方法', width:120, render:(_,r)=><Tag color={ANAL_COLOR[r.method]} style={{marginRight:0,width:76,textAlign:'center'}}>{ANAL_SHORT[r.method]}</Tag>},
            {title:'人数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); if(!sd.useOps) return <span className="tiny">—</span>; return <InputNumber size="small" min={sd.opsMin} max={sd.opsMax} style={{width:88}} value={r.ops} onChange={v=>setRow(r.method,{ops:v})}/>; }},
            {title:'次数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.trialsMin} max={sd.trialsMax} style={{width:88}} value={r.trials} onChange={v=>setRow(r.method,{trials:v})}/>; }},
            {title:'样本数', width:100, render:(_,r)=>{ const sd=samplingDef(r.method); return <InputNumber size="small" min={sd.partsMin} max={sd.partsMax} style={{width:88}} value={r.parts} onChange={v=>setRow(r.method,{parts:v})}/>; }},
            {title:'操作', width:110, render:(_,r)=><Space size={0}>
              <Button size="small" type="link" onClick={()=>saveRow(r)}>保存</Button>
              <Button size="small" type="link" danger onClick={()=>delRow(r)}>删除</Button>
            </Space>}
          ]}/>
      </>}""",
"分析方法模块 JSX")

io.open(P, 'w', encoding='utf-8').write(t)
print('全部修改完成')
