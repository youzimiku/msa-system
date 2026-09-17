# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new, tag, cnt=1):
    global t
    n = t.count(old)
    assert n == cnt, '锚点数量不符 %s: 期望 %d 实际 %d' % (tag, cnt, n)
    t = t.replace(old, new)
    print('OK:', tag)

# 1) seed 数据加 verdict（两处 seed 相同，SPL-001~005 各替换 2 处）
seed_v = [
    ("{id:'SPL-001', name:'轴径 φ50 标准件', type:'标准件', partNo:'PN-1001', refValue:'50.000', nominal:'50.000', unit:'mm', charDim:'轴径 φ50±0.05', standardId:'STD-MSA-001', source:'计量校准中心', expireDate:'2027-03-31', plant:'青岛工厂', subplant:'一分厂', status:'启用', note:'高等级量具鉴定真值，用于 GRR/偏倚/线性参考'}",
     "{id:'SPL-001', name:'轴径 φ50 标准件', type:'标准件', partNo:'PN-1001', refValue:'50.000', nominal:'50.000', unit:'mm', charDim:'轴径 φ50±0.05', standardId:'STD-MSA-001', source:'计量校准中心', expireDate:'2027-03-31', plant:'青岛工厂', subplant:'一分厂', status:'启用', note:'高等级量具鉴定真值，用于 GRR/偏倚/线性参考', verdict:'合格'}", 'seed SPL-001'),
    ("{id:'SPL-002', name:'轴径 φ10 标准件', type:'标准件', partNo:'PN-1002', refValue:'10.000', nominal:'10.000', unit:'mm', charDim:'轴径 φ10±0.02', standardId:'STD-MSA-001', source:'计量校准中心', expireDate:'2027-06-30', plant:'青岛工厂', subplant:'一分厂', status:'启用', note:'用于 Cg/Cgk 参考值±10% 控制线'}",
     "{id:'SPL-002', name:'轴径 φ10 标准件', type:'标准件', partNo:'PN-1002', refValue:'10.000', nominal:'10.000', unit:'mm', charDim:'轴径 φ10±0.02', standardId:'STD-MSA-001', source:'计量校准中心', expireDate:'2027-06-30', plant:'青岛工厂', subplant:'一分厂', status:'启用', note:'用于 Cg/Cgk 参考值±10% 控制线', verdict:'合格'}", 'seed SPL-002'),
    ("{id:'SPL-003', name:'扭矩标准杆 25N·m', type:'标准件', partNo:'PN-1003', refValue:'25.000', nominal:'25.000', unit:'N·m', charDim:'螺栓拧紧力矩 25N·m', standardId:'STD-MSA-001', source:'第三方检定', expireDate:'2027-01-31', plant:'青岛工厂', subplant:'二分厂', status:'启用', note:'用于扭力扳手 Cg/Cgk 与稳定性分析'}",
     "{id:'SPL-003', name:'扭矩标准杆 25N·m', type:'标准件', partNo:'PN-1003', refValue:'25.000', nominal:'25.000', unit:'N·m', charDim:'螺栓拧紧力矩 25N·m', standardId:'STD-MSA-001', source:'第三方检定', expireDate:'2027-01-31', plant:'青岛工厂', subplant:'二分厂', status:'启用', note:'用于扭力扳手 Cg/Cgk 与稳定性分析', verdict:'合格'}", 'seed SPL-003'),
    ("{id:'SPL-004', name:'壳体成品件 003 批', type:'生产件', partNo:'PN-2001', refValue:'待维护', nominal:'待维护', unit:'mm', charDim:'壳体关键尺寸', standardId:'STD-MSA-003', source:'3号线当班抽取', expireDate:'待维护', plant:'烟台工厂', subplant:'一分厂', status:'启用', note:'生产件代表过程散差，用于 GRR 样本抽取'}",
     "{id:'SPL-004', name:'壳体成品件 003 批', type:'生产件', partNo:'PN-2001', refValue:'待维护', nominal:'待维护', unit:'mm', charDim:'壳体关键尺寸', standardId:'STD-MSA-003', source:'3号线当班抽取', expireDate:'待维护', plant:'烟台工厂', subplant:'一分厂', status:'启用', note:'生产件代表过程散差，用于 GRR 样本抽取', verdict:'不合格'}", 'seed SPL-004'),
    ("{id:'SPL-005', name:'外观判定样件 外观 A', type:'生产件', partNo:'PN-2002', refValue:'合格', nominal:'合格', unit:'—', charDim:'外观判定', standardId:'STD-MSA-004', source:'检验班留样', expireDate:'—', plant:'烟台工厂', subplant:'一分厂', status:'停用', note:'计数型 KAPPA 判定参考样件'}",
     "{id:'SPL-005', name:'外观判定样件 外观 A', type:'生产件', partNo:'PN-2002', refValue:'合格', nominal:'合格', unit:'—', charDim:'外观判定', standardId:'STD-MSA-004', source:'检验班留样', expireDate:'—', plant:'烟台工厂', subplant:'一分厂', status:'停用', note:'计数型 KAPPA 判定参考样件', verdict:'合格'}", 'seed SPL-005'),
]
for old, new, tag in seed_v:
    rep(old, new, tag, cnt=2)

# 2) 迁移：已有 sampleLib 记录补 verdict（锚点用 judgeRules 前一行，避免依赖 SPL-005 原文）
rep("  ];\n  if(!d.judgeRules.length)",
    "  ];\n  (d.sampleLib||[]).forEach(o=>{ if(o.verdict===undefined) o.verdict=''; });\n  if(!d.judgeRules.length)",
    "字段迁移", cnt=1)

# 3) cleanV 函数
rep("  /* 行内字段即时写 store；保存常驻操作列；启用/停用用 Switch；日志按钮保留在行上 */",
    "  const cleanV=(v)=>(v&&v!=='—'&&v!=='待维护'&&v!=='合格')?v:'';\n  /* 行内字段即时写 store；保存常驻操作列；启用/停用用 Switch；日志按钮保留在行上 */",
    "cleanV 函数", cnt=1)

# 4) addRow 空行加 verdict
rep("s.sampleLib.unshift({id, name:'', type:'标准件', partNo:'', partName:'', charDim:'', nominal:'', refValue:'', unit:'mm', standardId:'', source:'', expireDate:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, status:'启用', note:''});",
    "s.sampleLib.unshift({id, name:'', type:'标准件', partNo:'', partName:'', charDim:'', verdict:'', nominal:'', refValue:'', unit:'mm', standardId:'', source:'', expireDate:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, status:'启用', note:''});",
    "addRow 空行", cnt=1)

# 5) 列表列：被测参数后加判定状态列；标准值/真值去待维护/合格
rep(
"""    {title:'被测参数', dataIndex:'charDim', width:170, render:(_,r)=><Select size="small" showSearch value={r.charDim||undefined} style={{width:160}} options={(d.characteristics||[]).map(c=>({value:c.name,label:c.name}))} onChange={x=>setF(r,'charDim',x)}/>},
    {title:'标准值', dataIndex:'nominal', width:100, render:(_,r)=><Input size="small" className="mono" value={(r.nominal&&r.nominal!=='—')?r.nominal:''} placeholder="待维护" onChange={e=>setF(r,'nominal',e.target.value)}/>},
    {title:'真值', dataIndex:'refValue', width:110, render:(_,r)=><Input size="small" className="mono" value={(r.refValue&&r.refValue!=='—')?r.refValue:''} placeholder="待维护" onChange={e=>setF(r,'refValue',e.target.value)}/>},""",
"""    {title:'被测参数', dataIndex:'charDim', width:170, render:(_,r)=><Select size="small" showSearch value={r.charDim||undefined} style={{width:160}} options={(d.characteristics||[]).map(c=>({value:c.name,label:c.name}))} onChange={x=>setF(r,'charDim',x)}/>},
    {title:'判定状态', dataIndex:'verdict', width:104, render:(_,r)=><Select size="small" value={r.verdict||undefined} style={{width:92}} options={[{value:'合格',label:'合格'},{value:'不合格',label:'不合格'}]} onChange={x=>setF(r,'verdict',x)}/>},
    {title:'标准值', dataIndex:'nominal', width:100, render:(_,r)=><Input size="small" className="mono" value={cleanV(r.nominal)} onChange={e=>setF(r,'nominal',e.target.value)}/>},
    {title:'真值', dataIndex:'refValue', width:110, render:(_,r)=><Input size="small" className="mono" value={cleanV(r.refValue)} onChange={e=>setF(r,'refValue',e.target.value)}/>},""",
"样本列表列", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('全部完成')
