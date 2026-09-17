# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(P, encoding='utf-8').read()

# (old, new, expected_count)
EDITS = []

# A. 模拟数据常量（在 SUBPLANTS_OPT 行后追加）
EDITS.append((
"""const PLANTS_OPT = ['青岛工厂','烟台工厂'].map(v=>({value:v,label:v}));
const SUBPLANTS_OPT = ['一分厂','二分厂'].map(v=>({value:v,label:v}));""",
"""const PLANTS_OPT = ['青岛工厂','烟台工厂'].map(v=>({value:v,label:v}));
const SUBPLANTS_OPT = ['一分厂','二分厂'].map(v=>({value:v,label:v}));
/* 模拟数据下拉选项（前端演示用，非业务主数据） */
const PARTNO_OPT = ['PN-1000','PN-1001','PN-1002','PN-1003','PN-1004','PN-1005','PN-1006','PN-1007','PN-2001','PN-3001','PN-4001','PN-5001'].map(v=>({value:v,label:v}));
const PARTNAME_OPT = ['轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴'].map(v=>({value:v,label:v}));
const PROCESS_OPT = ['精加工','检验','装配','机加工','终检','总装'].map(v=>({value:v,label:v}));
const UNIT_OPT = ['mm','μm','N','N·m','kg','g','°C','MPa','件'].map(v=>({value:v,label:v}));
const DEPT_OPT = ['品质部','总装车间','电控车间','计量室','实验室','质量'].map(v=>({value:v,label:v}));
const ANALYST_OPT = ['王强','刘青','张伟','孙丽','赵磊','周敏','吴刚','郑芳','冯强','何静','李工程师','陈杰','吴芳','周军'].map(v=>({value:v,label:v}));""", 1))

# B. 页面名称 被测项目维护 -> 被测参数维护（5 处）
EDITS.append(("label:'被测项目维护', group:'基础数据'", "label:'被测参数维护', group:'基础数据'", 1))
EDITS.append(("'char':'被测项目维护',", "'char':'被测参数维护',", 1))
EDITS.append(("char:{label:'被测项目维护',", "char:{label:'被测参数维护',", 1))
EDITS.append(('<PageHead title="被测项目维护"/>', '<PageHead title="被测参数维护"/>', 1))
EDITS.append(('<ImportBtn title="被测项目维护"/>', '<ImportBtn title="被测参数维护"/>', 1))

# C. 被测参数列表：零件编号->零件号 且与零件名称互换位置；工序/特性类别改下拉
EDITS.append((
"""    {title:'零件名称', dataIndex:'partName', width:110, ellipsis:true, render:(_,r)=><Input size="small" value={r.partName||''} onChange={e=>setF(r,'partName',e.target.value)}/>},
    {title:'零件编号', dataIndex:'partNo', width:100, ellipsis:true, render:(_,r)=><Input size="small" className="mono" value={r.partNo||''} onChange={e=>setF(r,'partNo',e.target.value)}/>},
    {title:'工序', dataIndex:'processName', width:90, ellipsis:true, render:(_,r)=><Input size="small" value={r.processName||''} onChange={e=>setF(r,'processName',e.target.value)}/>},
    {title:'特性类别', dataIndex:'category', width:100, render:(_,r)=><Input size="small" value={r.category||''} onChange={e=>setF(r,'category',e.target.value)}/>},""",
"""    {title:'零件号', dataIndex:'partNo', width:110, render:(_,r)=><Select size="small" value={r.partNo||undefined} style={{width:100}} options={PARTNO_OPT} onChange={x=>setF(r,'partNo',x)}/>},
    {title:'零件名称', dataIndex:'partName', width:120, ellipsis:true, render:(_,r)=><Select size="small" value={r.partName||undefined} style={{width:110}} options={PARTNAME_OPT} onChange={x=>setF(r,'partName',x)}/>},
    {title:'工序', dataIndex:'processName', width:100, render:(_,r)=><Select size="small" value={r.processName||undefined} style={{width:90}} options={PROCESS_OPT} onChange={x=>setF(r,'processName',x)}/>},
    {title:'数据类型', dataIndex:'category', width:104, render:(_,r)=><Select size="small" value={r.category||'计量型'} style={{width:94}} options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]} onChange={x=>setF(r,'category',x)}/>},""", 1))

# D. 分析方法列表：方法组去掉 placeholder；默认适用->数据类型 下拉
EDITS.append((
"""    {title:'方法组', dataIndex:'mergeWith', width:120, render:(_,r)=><Input size="small" placeholder="如：尺寸类合并组" value={r.mergeWith||''} onChange={e=>setMF(r,'mergeWith',e.target.value)}/>},""",
"""    {title:'方法组', dataIndex:'mergeWith', width:120, render:(_,r)=><Input size="small" value={r.mergeWith||''} onChange={e=>setMF(r,'mergeWith',e.target.value)}/>},""", 1))
EDITS.append((
"""    {title:'默认适用', dataIndex:'defaultType', width:100, render:(_,r)=><Input size="small" value={r.defaultType||''} onChange={e=>setMF(r,'defaultType',e.target.value)}/>},""",
"""    {title:'数据类型', dataIndex:'defaultType', width:108, render:(_,r)=><Select size="small" value={r.defaultType||'计量型'} style={{width:98}} options={[{value:'计量型',label:'计量型'},{value:'计数型',label:'计数型'}]} onChange={x=>setMF(r,'defaultType',x)}/>},""", 1))

# E. 样本库列表：零件号/零件名称/单位 下拉；对应被测项目->被测参数 下拉
EDITS.append((
"""    {title:'零件号', dataIndex:'partNo', width:100, render:(_,r)=><Input size="small" className="mono" value={r.partNo||''} onChange={e=>setF(r,'partNo',e.target.value)}/>},""",
"""    {title:'零件号', dataIndex:'partNo', width:110, render:(_,r)=><Select size="small" value={r.partNo||undefined} style={{width:100}} options={PARTNO_OPT} onChange={x=>setF(r,'partNo',x)}/>},""", 1))
EDITS.append((
"""    {title:'零件名称', dataIndex:'partName', width:110, ellipsis:true, render:(_,r)=><Input size="small" value={r.partName||''} onChange={e=>setF(r,'partName',e.target.value)}/>},""",
"""    {title:'零件名称', dataIndex:'partName', width:120, ellipsis:true, render:(_,r)=><Select size="small" value={r.partName||undefined} style={{width:110}} options={PARTNAME_OPT} onChange={x=>setF(r,'partName',x)}/>},""", 1))
EDITS.append((
"""    {title:'对应被测项目', dataIndex:'charDim', width:150, ellipsis:true, render:(_,r)=><Input size="small" value={r.charDim||''} onChange={e=>setF(r,'charDim',e.target.value)}/>},""",
"""    {title:'被测参数', dataIndex:'charDim', width:170, render:(_,r)=><Select size="small" showSearch value={r.charDim||undefined} style={{width:160}} options={(d.characteristics||[]).map(c=>({value:c.name,label:c.name}))} onChange={x=>setF(r,'charDim',x)}/>},""", 1))
# 单位列（被测参数列表 + 样本库列表，两处相同，统一替换）
EDITS.append((
"""    {title:'单位', dataIndex:'unit', width:70, render:(_,r)=><Input size="small" className="mono" value={r.unit||''} onChange={e=>setF(r,'unit',e.target.value)}/>},""",
"""    {title:'单位', dataIndex:'unit', width:86, render:(_,r)=><Select size="small" value={r.unit||undefined} style={{width:76}} options={UNIT_OPT} onChange={x=>setF(r,'unit',x)}/>},""", 2))

# F. MSA计划列表
# F1 分析人下拉
EDITS.append((
"""    {title:'分析人', width:110, render:(_,r)=><Input size="small" value={r.analyst||r.observer||''} onChange={e=>setF(r,'analyst',e.target.value)}/>},""",
"""    {title:'分析人', width:116, render:(_,r)=><Select size="small" value={r.analyst||r.observer||undefined} style={{width:106}} options={ANALYST_OPT} onChange={x=>setF(r,'analyst',x)}/>},""", 1))
# F2 零件号下拉 + 新增零件名称列
EDITS.append((
"""    {title:'零件号', width:100, dataIndex:'partNo', render:(_,r)=><Input size="small" className="mono" value={r.partNo||''} onChange={e=>setF(r,'partNo',e.target.value)}/>},""",
"""    {title:'零件号', width:110, dataIndex:'partNo', render:(_,r)=><Select size="small" value={r.partNo||undefined} style={{width:100}} options={PARTNO_OPT} onChange={x=>setF(r,'partNo',x)}/>},
    {title:'零件名称', width:120, dataIndex:'partName', render:(_,r)=><Select size="small" value={(r.partName&&r.partName!=='—')?r.partName:undefined} style={{width:110}} options={PARTNAME_OPT} onChange={x=>setF(r,'partName',x)}/>},""", 1))
# F3 测量特性 -> 被测参数（只读纯文本）
EDITS.append((
"""    {title:'测量特性', width:170, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); const cur=(r.instIds||[]).length>1? recs.map(x=>x.object).filter(Boolean).join('、') : (r.object||''); return <Input size="small" value={cur} onChange={e=>setF(r,'object',e.target.value)}/>; }},""",
"""    {title:'被测参数', width:190, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); const cur=(r.instIds||[]).length>1? recs.map(x=>x.object).filter(Boolean).join('、') : (r.object||''); return <span>{cur||'—'}</span>; }},""", 1))
# F4 去掉检验标准列（整行删除）
EDITS.append((
"""    {title:'检验标准', width:110, render:(_,r,idx)=>{ if(stdSame) return idx===0? <span className="mono">{stdAll[0]}</span> : <span>—</span>; const v=stdOf(r); return <span className="mono">{v}</span>; }},
""", "", 1))
# F5 部门下拉
EDITS.append((
"""    {title:'部门', dataIndex:'dept', width:100, render:(_,r)=><Input size="small" value={r.dept||''} onChange={e=>setF(r,'dept',e.target.value)}/>},""",
"""    {title:'部门', dataIndex:'dept', width:104, render:(_,r)=><Select size="small" value={r.dept||undefined} style={{width:94}} options={DEPT_OPT} onChange={x=>setF(r,'dept',x)}/>},""", 1))
# F6 分厂 -> 工厂（下拉，绑定 plant 字段）
EDITS.append((
"""    {title:'分厂', width:90, dataIndex:'subplant', render:(_,r)=><Input size="small" value={r.subplant||''} onChange={e=>setF(r,'subplant',e.target.value)}/>},""",
"""    {title:'工厂', width:100, dataIndex:'plant', render:(_,r)=><Select size="small" value={r.plant||undefined} style={{width:90}} options={PLANTS_OPT} onChange={x=>setF(r,'plant',x)}/>},""", 1))

fail = False
for i, (old, new, exp) in enumerate(EDITS):
    cnt = src.count(old)
    if cnt != exp:
        print(f"[FAIL] #{i} 期望 {exp} 实际 {cnt} | old[:60]={old[:60]!r}")
        fail = True
    else:
        src = src.replace(old, new)
        print(f"[OK] #{i} 替换 {cnt} 处")

if fail:
    print("存在未匹配项，未写回文件")
else:
    open(P, 'w', encoding='utf-8', newline='').write(src)
    print("全部替换成功，已写回 index.html")
