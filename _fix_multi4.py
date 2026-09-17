# -*- coding: utf-8 -*-
"""multi4: seed 补一计划多方法演示计划 MSAP-2026-009 + 3 条待采集记录"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'count=%d for: %s' % (c, old[:60])
    s = s.replace(old, new)

# 1) 计划 MSAP-2026-009（在 008 后）
rep("""     trigger:'顾客审核整改', status:'未定型', recordId:'', result:'', note:'待定型'}
  ];""",
"""     trigger:'顾客审核整改', status:'未定型', recordId:'', result:'', note:'待定型'},
    {id:'MSAP-2026-009', name:'数显千分表 0~12.7mm · GRR/稳定性/Cg-Cgk', instId:'JJQ-2024-004', instName:'数显千分表 0~12.7mm', cat:'千分表',
     type:'GRR', method:'均值-极差法(Xbar-R)', methods:['GRR','stability','cgcgk'], standard:'STD-MSA-001', params:{ops:3, trials:3, parts:10},
     object:'轴径 Φ12.5±0.05', feature:'直径', owner:'李工程师', editor:'李工程师', editorDate:'2026-09-08', planDate:'2026-10-15',
     trigger:'周期复评', status:'待采集', recordId:'', result:'', note:'一计划多方法：GRR + 稳定性 + Cg/Cgk（一个计划可触发多个分析任务）'}
  ];""")

# 2) GRR-2026-004（追加到 grr 数组尾）
i = s.find("{id:'GRR-2026-003'")
assert i > 0
j = s.find('\n  ];', i)
assert j > i
s = s[:j] + """
    {id:'GRR-2026-004', planId:'MSAP-2026-009', instId:'JJQ-2024-004', instName:'数显千分表 0~12.7mm', object:'轴径 Φ12.5±0.05', unit:'mm',
     method:'均值-极差法(Xbar-R)', standard:'STD-MSA-001', numOps:3, numTrials:3, numParts:10, sampleGroup:'',
     tolerance:{has:true, usl:12.55, lsl:12.45},
     operators:['操作员A','操作员B','操作员C'], raw:null, analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:'一计划多方法：GRR 任务（待采集）'}""" + s[j:]

# 3) STB-2026-003（stability 数组尾）
i = s.find("{id:'STB-2026-002'")
assert i > 0
j = s.find('\n  ];', i)
assert j > i
s = s[:j] + """
    {id:'STB-2026-003', planId:'MSAP-2026-009', instId:'JJQ-2024-004', instName:'数显千分表 0~12.7mm', object:'轴径 Φ12.5±0.05', unit:'mm',
     method:'均值-极差控制图（SPC判异模型）', standard:'STD-MSA-001', groups:25, per:5, span:'4周~3个月',
     raw:null, tolerance:{has:true, usl:12.55, lsl:12.45},
     reviewStatus:'待采集', conclusion:'', analyst:'', analysisDate:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:'一计划多方法：稳定性任务（待采集）'}""" + s[j:]

# 4) CG-2026-004（cgcgk 数组尾）
i = s.find("{id:'CG-2026-003'")
assert i > 0
j = s.find('\n  ];', i)
assert j > i
s = s[:j] + """
    {id:'CG-2026-004', planId:'MSAP-2026-009', instId:'JJQ-2024-004', instName:'数显千分表 0~12.7mm', object:'轴径 Φ12.5±0.05', unit:'mm',
     method:'Type1 能力指数（VDA 参考值±10%标准误）', standard:'STD-MSA-001', runs:50, refValue:'',
     raw:null, tolerance:{has:true, usl:12.55, lsl:12.45},
     reviewStatus:'待采集', conclusion:'', analyst:'', analysisDate:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[], note:'一计划多方法：Cg/Cgk 任务（待采集）'}""" + s[j:]

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('multi4 完成：MSAP-2026-009 + GRR-2026-004 + STB-2026-003 + CG-2026-004')
