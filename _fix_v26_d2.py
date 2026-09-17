# -*- coding: utf-8 -*-
"""Step4b：用占位符替换避免 % 冲突"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

def gen_lin(ref, n=12, amp=0.004, seed=0):
    return [round(ref + (-amp + amp*2*((i*3+seed) % 5)/5.0), 4) for i in range(n)]

def gen_stab(n=25, per=5, ref=10.0, amp=0.003, seed=0):
    return [[round(ref + (-amp + amp*2*((g*2+i+seed) % 7)/7.0), 4) for i in range(per)] for g in range(n)]

def gen_cg(n=50, ref=50.0, amp=0.002, bias=0.0, seed=0):
    return [round(ref + bias + (-amp + amp*2*((i*5+seed) % 9)/9.0), 4) for i in range(n)]

lin1_raw = str([gen_lin(r, 12, 0.004, idx) for idx, r in enumerate([10, 40, 80, 120, 150])])
stb1_raw = str(gen_stab(25, 5, 10.0, 0.003, 1))
cg1_raw = str(gen_cg(50, 50.0, 0.002, 0.0, 2))
cg2_raw = str(gen_cg(50, 25.0, 0.05, 0.05, 3))

lin_rec = """{id:'LIN-2026-001', planId:'MSAP-2026-001', instId:'JJQ-2024-001', instName:'数显卡尺 0~150mm', object:'轴径 φ50±0.05', unit:'mm',
     method:'线性回归+偏移t检验（5标准件覆盖量程）', standard:'STD-MSA-001', stds:5, per:12, points:5, biasRuns:15,
     refs:['10','40','80','120','150'], raw:@LIN1@, tolerance:{has:true, usl:50.05, lsl:49.95},
     analysisDate:'2026-03-18', analyst:'李工程师', reviewStatus:'已批准', conclusion:'非常理想可接受',
     reviewer:'张工', reviewDate:'2026-03-20', approver:'王经理', approveDate:'2026-03-22', actions:[],
     note:'偏倚为0的水平线完全包围在置信区间内，各点平均偏倚均落在区间内（示例数据）'},
    {id:'LIN-2026-002', planId:'MSAP-2026-004', instId:'JJQ-2024-002', instName:'外径千分尺 0~25mm', object:'轴径 φ10±0.02', unit:'mm',
     method:'线性回归+偏移t检验（5标准件覆盖量程）', standard:'STD-MSA-001', stds:5, per:12, points:5, biasRuns:15,
     refs:['','','','',''], raw:null, tolerance:{has:true, usl:10.02, lsl:9.98},
     analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[],
     note:'已建立台账记录，待录入 5 标准件×12 次测量数据后自动完成线性回归与偏倚判定'}"""

stb_rec = """{id:'STB-2026-001', planId:'MSAP-2026-004', instId:'JJQ-2024-002', instName:'外径千分尺 0~25mm', object:'轴径 φ10±0.02', unit:'mm',
     method:'均值-极差控制图（SPC判异模型）', standard:'STD-MSA-001', groups:25, per:5, span:'4周~3个月',
     raw:@STB1@, tolerance:{has:true, usl:10.02, lsl:9.98},
     analysisDate:'2026-04-10', analyst:'李工程师', reviewStatus:'已批准', conclusion:'可接受',
     reviewer:'张工', reviewDate:'2026-04-12', approver:'王经理', approveDate:'2026-04-15', actions:[],
     note:'25 子组×5 次，Xbar-R 控制图无出界点，过程稳定（示例数据）'},
    {id:'STB-2026-002', planId:'MSAP-2026-003', instId:'JJQ-2024-007', instName:'数显扭力扳手 5~50N·m', object:'螺栓拧紧力矩 25N·m', unit:'N·m',
     method:'均值-极差控制图（SPC判异模型）', standard:'STD-MSA-001', groups:25, per:5, span:'4周~3个月',
     raw:null, tolerance:{has:true, usl:27.5, lsl:22.5},
     analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[],
     note:'已建立台账记录，待按子组录入测量数据后自动绘制控制图并判异'}"""

cg_rec = """{id:'CG-2026-001', planId:'MSAP-2026-001', instId:'JJQ-2024-001', instName:'数显卡尺 0~150mm', object:'轴径 φ50±0.05', unit:'mm',
     method:'Type1 能力指数（VDA 参考值±10%标准误）', standard:'STD-MSA-001', runs:50, refValue:'50',
     raw:@CG1@, tolerance:{has:true, usl:50.05, lsl:49.95},
     analysisDate:'2026-03-18', analyst:'李工程师', reviewStatus:'已批准', conclusion:'可接受',
     reviewer:'张工', reviewDate:'2026-03-20', approver:'王经理', approveDate:'2026-03-22', actions:[],
     note:'Cg、Cgk 均 ≥1.33，量具能力充足，可用于日常检验与量产判定（示例数据）'},
    {id:'CG-2026-002', planId:'MSAP-2026-003', instId:'JJQ-2024-007', instName:'数显扭力扳手 5~50N·m', object:'螺栓拧紧力矩 25N·m', unit:'N·m',
     method:'Type1 能力指数（VDA 参考值±10%标准误）', standard:'STD-MSA-001', runs:50, refValue:'25',
     raw:@CG2@, tolerance:{has:true, usl:27.5, lsl:22.5},
     analysisDate:'2026-06-12', analyst:'李工程师', reviewStatus:'待审核', conclusion:'有条件接受',
     reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[],
     note:'存在系统性偏倚，Cgk 处于边缘，需评估是否需要重新校准（示例数据）'},
    {id:'CG-2026-003', planId:'MSAP-2026-004', instId:'JJQ-2024-002', instName:'外径千分尺 0~25mm', object:'轴径 φ10±0.02', unit:'mm',
     method:'Type1 能力指数（VDA 参考值±10%标准误）', standard:'STD-MSA-001', runs:50, refValue:'',
     raw:null, tolerance:{has:true, usl:10.02, lsl:9.98},
     analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[],
     note:'已建立台账记录，待录入 50 次连续测量并填写参考值后自动计算 Cg/Cgk'}"""

res_rec = """{id:'RES-2026-001', planId:'MSAP-2026-001', instId:'JJQ-2024-001', instName:'数显卡尺 0~150mm', object:'轴径 φ50±0.05', unit:'mm',
     method:'直接录入（不取样）', standard:'STD-MSA-001', resValue:'0.01', tolerance:{has:true, usl:50.05, lsl:49.95},
     analysisDate:'2026-03-18', analyst:'李工程师', reviewStatus:'已批准', conclusion:'可接受',
     reviewer:'张工', reviewDate:'2026-03-20', approver:'王经理', approveDate:'2026-03-22', actions:[],
     note:'分辨率 0.01mm ≤ 1/10 过程公差，分辨率满足要求（示例数据）'},
    {id:'RES-2026-002', planId:'MSAP-2026-004', instId:'JJQ-2024-002', instName:'外径千分尺 0~25mm', object:'轴径 φ10±0.02', unit:'mm',
     method:'直接录入（不取样）', standard:'STD-MSA-001', resValue:'', tolerance:{has:true, usl:10.02, lsl:9.98},
     analysisDate:'', analyst:'', reviewStatus:'待采集', conclusion:'', reviewer:'', reviewDate:'', approver:'', approveDate:'', actions:[],
     note:'已建立台账记录，待填写分辨率值后自动判定'}"""

lin_rec = lin_rec.replace('@LIN1@', lin1_raw)
stb_rec = stb_rec.replace('@STB1@', stb1_raw)
cg_rec = cg_rec.replace('@CG1@', cg1_raw).replace('@CG2@', cg2_raw)

old = "  const linear=[], stability=[], cgcgk=[], resolution=[];"
new = ("  const linear = [\n" + lin_rec + "\n  ];\n"
       "  const stability = [\n" + stb_rec + "\n  ];\n"
       "  const cgcgk = [\n" + cg_rec + "\n  ];\n"
       "  const resolution = [\n" + res_rec + "\n  ];")
n = s.count(old)
print('seed 空数组替换 x%d' % n)
assert n == 1
s = s.replace(old, new)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
