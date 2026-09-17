# -*- coding: utf-8 -*-
"""清理 seed 与注释中的旧 KAPPA 判定文本，对齐业务三档口径"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:60], n, cnt))
    s = s.replace(old, new)

# STD-MSA-004 判定准则 → 业务三档表
rep("""    {id:'STD-MSA-004', name:'计数型有效性/漏判/误判判定准则', type:'有效性判定', version:'V1.2', effDate:'2025-07-01', status:'启用',
     instIds:['JJQ-2024-008'],
     basis:'AIAG MSA 第4版 §9；行业惯例',
     criteria:[
       {cond:'整体有效性 ≥ 90%', verdict:'可接受'},
       {cond:'漏判率 ≤ 2%', verdict:'满足（漏判风险直接影响顾客，从严）'},
       {cond:'误判率 ≤ 5%', verdict:'满足'},
       {cond:'任一超限', verdict:'不可接受，需培训并复测'}
     ],
     owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V1.2：漏判率从严至2%'},""",
"""    {id:'STD-MSA-004', name:'计数型三档判定准则', type:'有效性判定', version:'V2.0', effDate:'2025-07-01', status:'启用',
     instIds:['JJQ-2024-008'],
     basis:'AIAG MSA 第4版 §9；业务《计数型测量系统分析》三档判定表',
     criteria:[
       {cond:'Kappa≥0.75 且 有效性≥90% 且 错误率≤2% 且 错误警报率≤5%', verdict:'评价人可接受'},
       {cond:'Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10%', verdict:'可接受边缘-可能需改进'},
       {cond:'Kappa<0.40 或 有效性<80% 或 错误率>5% 或 错误警报率>10%', verdict:'不可接受-需改进（结论取最差档）'}
     ],
     owner:'质量部', editor:'李工程师', auditor:'张工', approver:'王经理', changeLog:'V2.0：按业务三档判定表对齐（有效性=正确决定次数/总决定次数）'},""")

# 校验标准 5：偏倚与线性判定准则 → 业务 4 条（先看现状再改）
rep("""    {id:'STD-MSA-005', name:'偏倚与线性判定准则', type:'偏倚/线性判定', version:'V1.0', effDate:'2025-01-01', status:'启用',
     instIds:[],
     basis:'AIAG MSA 第4版 §3、§4；基于过程变差或公差',
     criteria:[
       {cond:'偏倚% ≤ 10%（相对过程变差或公差）', verdict:'可接受'},""",
"""    {id:'STD-MSA-005', name:'偏倚与线性判定准则', type:'偏倚/线性判定', version:'V2.0', effDate:'2025-01-01', status:'启用',
     instIds:[],
     basis:'AIAG MSA 第4版 §3、§4；业务判定准则（"0"水平线 vs 95% 置信区间）',
     criteria:[
       {cond:'"0"水平线完全包围在 95% 置信区间内，且各点平均偏倚均落在区间内', verdict:'非常理想可接受'},
       {cond:'"0"出区间、常量显著≠0、斜率显著=0', verdict:'理想可接受（固定偏倚可修正）'},
       {cond:'"0"出区间、斜率显著≠0、平均偏倚在区间内', verdict:'较理想可接受（线性偏倚可修正）'},
       {cond:'"0"出区间、斜率≈0、出界点位于不同侧', verdict:'不可接受（有偏倚且无线性可修正）'},""")

# KAPPA seed 记录结论与备注措辞
rep("analysisDate:'2026-08-26', analyst:'李工程师', reviewStatus:'需整改', conclusion:'良好(有条件接受)',",
    "analysisDate:'2026-08-26', analyst:'李工程师', reviewStatus:'需整改', conclusion:'不可接受-需改进',")
rep("note:'零漏判（无顾客风险）；但误判率偏高（过严拒收），按顾客整改要求培训后复测'}",
    "note:'零漏判（无顾客风险）；但错误警报率偏高（过严拒收），按顾客整改要求培训后复测'}")

# 注释更新
rep(" *  KAPPA = (Po-Pe)/(1-Pe)，附有效性/漏判率/误判率",
    " *  KAPPA = (Po-Pe)/(1-Pe)，附有效性/错误率(漏判)/错误警报率(误判)，按业务三档表判定")

open(p, 'w', encoding='utf-8').write(s)
print('seed cleanup OK, len:', len(s))
