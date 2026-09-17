# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

new_guide = """const PAGE_GUIDE = {
  instgroup:{label:'器具组维护', text:'维护测量器具组与人员组（岗位）。', logic:'组类型决定用途：测量器具组供「创建MSA计划-器具」选择；人员组（岗位）供「创建MSA计划-人员」选择（仅支持 KAPPA）。被计划引用的器具组不可删除。'},
  char:{label:'被测参数维护', text:'维护质量特性（被测项目）主数据，一个项目可关联多种检验方法（GRR / KAPPA / 线性 / 稳定性 / Cg/Cgk），每种方法关联对应检验标准；检验标准在本页统一维护。', logic:'维护被测项目（质量特性）主数据：每个项目对应零件 + 工序 + 检验方法（多选，下拉按方法名称展示），检验标准号系统自动生成不可修改。创建 MSA 计划时选中被测参数会自动带出该特性支持的分析方法。'},
  sampling:{label:'抽样方法维护', logic:'分析方法为固定代码表：名称只读、不可增删，其余字段可编辑；抽样规则按「方法 + 工厂 + 车间」唯一维护（默认样品数/人数/次数及范围），列表随上方选中的分析方法联动过滤；判断规则在同一方法 + 工厂 + 车间下可有多条，判定结论固定为可接受 / 有条件接受 / 不可接受；计算参数按方法维护。', ops:'方法固定不可增删；抽样规则 / 判断规则 / 计算参数三个页签均行内编辑，行首保存按钮常驻；抽样规则同一方法 + 工厂 + 车间不可重复。'},
  samplelib:{label:'样本库管理', text:'样本新增时，触发打印事件，打印样本编号二维码，支持补打。', logic:'零件号下拉支持按「零件号-零件名称」检索，选中后仅显示零件号并自动带出零件名称（名称只读）；被测参数下拉取「被测参数维护」中的参数名称；'},
  plan:{label:'MSA 计划', text:'创建 MSA 计划（按器具 / 按人员），计划下自动生成对应台账分析单；', logic:'创建计划：先选器具（组）/ 人员（组），再选被测参数（自动带出该特性支持的分析方法，需手动勾选后点「确定」加入下方方法列表，同一方法不可重复添加，删除列表行会联动取消勾选，切换器具/参数时清空列表）；人员弹窗仅 支持KAPPA分析方式。维度列状态按计划勾选的方法范围与台账结论判定：不做（未勾选）/ 未做（勾选未分析）/ 通过 / 不通过/有条件接受', status:true},
  entry:{label:'台账', perm:true}
};
"""
old_guide_m = s.index('const PAGE_GUIDE = {')
old_guide_end = s.index('};\n', old_guide_m) + 3
s = s[:old_guide_m] + new_guide + s[old_guide_end:]

# 渲染函数：data 分支 ops 条件化（用户删除了 data 关键操作）
old_data = "if(kind==='data'){ if(g.logic) body.push(<div key=\"l\" style={{marginBottom:6}}><b>关键逻辑：</b>{g.logic}</div>); body.push(<div key=\"o\"><b>关键操作：</b>{g.ops}</div>); }"
new_data = "if(kind==='data'){ if(g.logic) body.push(<div key=\"l\" style={{marginBottom:6}}><b>关键逻辑：</b>{g.logic}</div>); if(g.ops) body.push(<div key=\"o\"><b>关键操作：</b>{g.ops}</div>); }"
assert old_data in s, 'data branch not found'
s = s.replace(old_data, new_data)

# 状态表文字更新（按表格修改）
repl = [
 ("<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>未做（灰色虚线圆圈）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>属于计划范围，但尚未完成对应台账分析</td></tr>",
  "<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>未做（灰色虚线圆圈）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>属于计划范围，但未完成对应台账分析</td></tr>"),
 ("<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>有条件接受（黄色感叹号）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为有条件接受（可接受但需关注）；多个分计划以最差结论为准</td></tr>",
  "<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>有条件接受（黄色感叹号）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为有条件接受</td></tr>"),
 ("<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>不通过（红色叉）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为不可接受，需整改；多个分计划以最差结论为准</td></tr>",
  "<tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>不通过（红色叉）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为不可接受</td></tr>"),
]
for a, b in repl:
    assert a in s, 'status row not found: ' + a[:50]
    s = s.replace(a, b)

io.open(P, 'w', encoding='utf-8').write(s)
print('done, new len =', len(s))
