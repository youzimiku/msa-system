# -*- coding: utf-8 -*-
"""v2.6 第二批：MSA 计划创建引用 质量特性 + 抽样规则（samplingDef 数据驱动）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:80])
    s = s.replace(old, new, cnt)

# ---------- 1. samplingDef helper（插在 SMP_DEF 定义后） ----------
rep("""  const effMeth = mMethods.length===1? mMethods[0] : (stdTypeOf(stdSel)||'GRR');
  const effDef = SMP_DEF[effMeth]||SMP_DEF.GRR;""",
    """  const samplingDef=(m)=>{ const d0=Store.get(); const r=(d0.samplingRules||[]).find(x=>x.method===m); if(r) return {ops:r.opsDefault||3, opsMin:r.opsMin!==undefined?r.opsMin:1, opsMax:r.opsMax!==undefined?r.opsMax:5, useOps:!!r.useOps, trials:r.trialsDefault||3, trialsMin:r.trialsMin!==undefined?r.trialsMin:2, trialsMax:r.trialsMax!==undefined?r.trialsMax:5, parts:r.sampleDefault||10, partsMin:r.sampleMin!==undefined?r.sampleMin:1, partsMax:r.sampleMax!==undefined?r.sampleMax:30}; return SMP_DEF[m]||SMP_DEF.GRR; };
  const effMeth = mMethods.length===1? mMethods[0] : (stdTypeOf(stdSel)||'GRR');
  const effDef = samplingDef(effMeth);""",
    1, 'samplingDef-helper')

# ---------- 2. 质量特性 state（插在 partSel 状态行前） ----------
rep("  const [partSel,setPartSel]=useState('');",
    """  const [charSel,setCharSel]=useState('');            // 引用质量特性（基础数据页维护，SC/CC/普通）
  const charOptions=(d.characteristics||[]).filter(c=>c.status==='启用').map(c=>({value:c.id, label:c.name+(c.type?'（'+c.type+'）':''), type:c.type}));
  const charObj=charSel? (d.characteristics||[]).find(c=>c.id===charSel) : null;
  const [partSel,setPartSel]=useState('');""",
    1, 'char-state')

# ---------- 3. 计划填写信息区：加 质量特性 下拉（插在 检验标准 Col 后） ----------
rep("""        <Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">创建方式</span><div><Tag color="blue">逐个创建（一器一计划）</Tag></div></Col>""",
    """        <Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">质量特性</span><Select size="small" allowClear style={{width:140}} placeholder="选质量特性（自动带出测量对象）" options={charOptions} value={charSel||undefined} onChange={v=>setCharSel(v||'')}/></Col>
        <Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">创建方式</span><div><Tag color="blue">逐个创建（一器一计划）</Tag></div></Col>""",
    1, 'char-col')

# ---------- 4. 行内 测量对象 列：未手填时自动带出选中特性名 ----------
rep("""    {title:'测量对象（质量特性）', width:190, render:(_,i)=><Input size="small" placeholder="如：轴径 φ10±0.02" disabled={!i.selectable} value={cfg[i.id]?cfg[i.id].object:''} onChange={e=>setRow(i.id,{object:e.target.value})}/>},""",
    """    {title:'测量对象（质量特性）', width:190, render:(_,i)=><Input size="small" placeholder={charObj?charObj.name:'如：轴径 φ10±0.02'} disabled={!i.selectable} value={(cfg[i.id]&&cfg[i.id].object!==undefined)?cfg[i.id].object:(charObj?charObj.name:'')} onChange={e=>setRow(i.id,{object:e.target.value})}/>},""",
    1, 'object-col')

# ---------- 5. 提交：计划记录加 charId/feature ----------
rep("""          type:firstAn, method, methods:meths.slice(), standard:stdSel, params:meths.length? pParamsOf(firstAn) : {},
          object:c.object||'待定义', feature:'', owner:c.owner||s.me.name, editor:s.me.name, editorDate:TODAY,""",
    """          type:firstAn, method, methods:meths.slice(), standard:stdSel, params:meths.length? pParamsOf(firstAn) : {},
          object:c.object||(charObj?charObj.name:'待定义'), feature:charObj?charObj.type:'', charId:charSel, owner:c.owner||s.me.name, editor:s.me.name, editorDate:TODAY,""",
    1, 'plan-char')

rep("""        meths.forEach(an=>{ spawnRecord(s, pid, {type:an, instId:id, instName:fullName, object:c.object||'待定义', standard:stdSel, method:ENUM.taskMethod[an][0], params:pParamsOf(an), note:'创建时按分析方法 '+ANAL_SHORT[an]+' 生成'}); });""",
    """        meths.forEach(an=>{ spawnRecord(s, pid, {type:an, instId:id, instName:fullName, object:c.object||(charObj?charObj.name:'待定义'), standard:stdSel, method:ENUM.taskMethod[an][0], params:pParamsOf(an), feature:charObj?charObj.type:'', charId:charSel, note:'创建时按分析方法 '+ANAL_SHORT[an]+' 生成'}); });""",
    1, 'record-char')

# ---------- 6. SMP_DEF 引用替换为 samplingDef ----------
rep("""        const D0=SMP_DEF[(firstAn==='GRR'||firstAn==='KAPPA'||!firstAn)?(firstAn||'GRR'):(singleM?firstAn:'GRR')]||SMP_DEF.GRR;""",
    """        const D0=samplingDef((firstAn==='GRR'||firstAn==='KAPPA'||!firstAn)?(firstAn||'GRR'):(singleM?firstAn:'GRR'));""",
    1, 'D0')

rep("""    {title:'人数', width:64, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return !D.useOps?""",
    """    {title:'人数', width:64, render:(_,i)=>{ const D=samplingDef(effMeth); return !D.useOps?""",
    1, 'ops-col')

rep("""    {title:'次数', width:56, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return D.trialsMax===0?""",
    """    {title:'次数', width:56, render:(_,i)=>{ const D=samplingDef(effMeth); return D.trialsMax===0?""",
    1, 'trials-col')

rep("""    {title:'样本数', width:64, render:(_,i)=>{ const D=SMP_DEF[effMeth]||SMP_DEF.GRR; return D.partsMax===0?""",
    """    {title:'样本数', width:64, render:(_,i)=>{ const D=samplingDef(effMeth); return D.partsMax===0?""",
    1, 'parts-col')

open(P, 'w', encoding='utf-8').write(s)
print('batch2 OK 长度', len(s))
