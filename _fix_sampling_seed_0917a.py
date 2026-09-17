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

# ============ 1) samplingRules seed：SR-005 后补 3 条（不同工厂车间） ============
rep("    {id:'SR-005', method:'cgcgk', category:'其他', sampleDefault:1, sampleMin:1, sampleMax:1, opsDefault:1, opsMin:1, opsMax:1, trialsDefault:50, trialsMin:50, trialsMax:200, useOps:false, readingsMin:'50', readingsMax:'50', plant:'青岛工厂', subplant:'二分厂', note:'Cg/Cgk 单独取样：1 件标准件独立装夹连续测 50 次，参考值±10% 标准误控制线'}\n  ];",
    "    {id:'SR-005', method:'cgcgk', category:'其他', sampleDefault:1, sampleMin:1, sampleMax:1, opsDefault:1, opsMin:1, opsMax:1, trialsDefault:50, trialsMin:50, trialsMax:200, useOps:false, readingsMin:'50', readingsMax:'50', plant:'青岛工厂', subplant:'二分厂', note:'Cg/Cgk 单独取样：1 件标准件独立装夹连续测 50 次，参考值±10% 标准误控制线'},\n    {id:'SR-006', method:'GRR', category:'其他', sampleDefault:10, sampleMin:3, sampleMax:15, opsDefault:3, opsMin:2, opsMax:4, trialsDefault:3, trialsMin:2, trialsMax:5, useOps:true, readingsMin:'60', readingsMax:'90', plant:'烟台工厂', subplant:'一分厂', note:'烟台工厂 GRR 抽样规则（示例）：10 件×3 人×3 次'},\n    {id:'SR-007', method:'KAPPA', category:'其他', sampleDefault:50, sampleMin:20, sampleMax:50, opsDefault:3, opsMin:2, opsMax:4, trialsDefault:3, trialsMin:1, trialsMax:5, useOps:true, readingsMin:'450', readingsMax:'450', plant:'烟台工厂', subplant:'一分厂', note:'烟台工厂 KAPPA 抽样规则（示例）：50 件×3 人×3 次'},\n    {id:'SR-008', method:'stability', category:'稳定性类', sampleDefault:25, sampleMin:25, sampleMax:100, opsDefault:1, opsMin:1, opsMax:3, trialsDefault:5, trialsMin:3, trialsMax:10, useOps:false, readingsMin:'75', readingsMax:'125', plant:'青岛工厂', subplant:'一分厂', note:'青岛工厂稳定性抽样规则（示例）：25 子组×5 次'}\n  ];",
    "samplingRules 新增 3 条", cnt=1)

# ============ 2) judgeRules seed（两处相同，各替换 2 处）：补 plant/subplant + 规范化 verdict ============
judge_patch = [
    ("{id:'JR-001', method:'GRR', condition:'NDC ≥ 5', verdict:'可接受', note:'可区分类别数达标，测量系统分辨力与变差可接受'}",
     "{id:'JR-001', method:'GRR', condition:'NDC ≥ 5', verdict:'可接受', plant:'青岛工厂', subplant:'一分厂', note:'可区分类别数达标，测量系统分辨力与变差可接受'}"),
    ("{id:'JR-002', method:'GRR', condition:'%GRR < 10%', verdict:'可接受', note:'测量系统重复性+再现性占比小于 10%，可接受'}",
     "{id:'JR-002', method:'GRR', condition:'%GRR < 10%', verdict:'可接受', plant:'青岛工厂', subplant:'一分厂', note:'测量系统重复性+再现性占比小于 10%，可接受'}"),
    ("{id:'JR-003', method:'GRR', condition:'10% ≤ %GRR ≤ 30%', verdict:'有条件接受', note:'处于有条件区间，需结合过程能力评审后批准'}",
     "{id:'JR-003', method:'GRR', condition:'10% ≤ %GRR ≤ 30%', verdict:'有条件接受', plant:'青岛工厂', subplant:'一分厂', note:'处于有条件区间，需结合过程能力评审后批准'}"),
    ("{id:'JR-004', method:'GRR', condition:'%GRR > 30%', verdict:'不可接受', note:'测量系统不能接受，必须整改后重新分析'}",
     "{id:'JR-004', method:'GRR', condition:'%GRR > 30%', verdict:'不可接受', plant:'青岛工厂', subplant:'一分厂', note:'测量系统不能接受，必须整改后重新分析'}"),
    ("{id:'JR-005', method:'KAPPA', condition:'Kappa > 0.75', verdict:'可接受', note:'检验员判定与参考值高度一致，满足要求'}",
     "{id:'JR-005', method:'KAPPA', condition:'Kappa > 0.75', verdict:'可接受', plant:'青岛工厂', subplant:'一分厂', note:'检验员判定与参考值高度一致，满足要求'}"),
    ("{id:'JR-006', method:'KAPPA', condition:'0.40 ≤ Kappa ≤ 0.75', verdict:'有条件接受', note:'一致性处于边缘区间，需结合有效性/错误率评估'}",
     "{id:'JR-006', method:'KAPPA', condition:'0.40 ≤ Kappa ≤ 0.75', verdict:'有条件接受', plant:'青岛工厂', subplant:'一分厂', note:'一致性处于边缘区间，需结合有效性/错误率评估'}"),
    ("{id:'JR-007', method:'KAPPA', condition:'Kappa < 0.40', verdict:'不可接受', note:'一致性不足，需培训或整改后重新分析'}",
     "{id:'JR-007', method:'KAPPA', condition:'Kappa < 0.40', verdict:'不可接受', plant:'青岛工厂', subplant:'一分厂', note:'一致性不足，需培训或整改后重新分析'}"),
    ("{id:'JR-008', method:'linear', condition:'偏倚0水平线完全包围在置信区间内', verdict:'非常理想可接受', note:'各点平均偏倚均落在置信区间内'}",
     "{id:'JR-008', method:'linear', condition:'偏倚0水平线完全包围在置信区间内', verdict:'可接受', plant:'青岛工厂', subplant:'一分厂', note:'各点平均偏倚均落在置信区间内'}"),
    ("{id:'JR-009', method:'linear', condition:'固定偏倚（常量显著≠0、斜率不显著）', verdict:'理想可接受', note:'量程范围内固定偏倚，可通过纠偏修正'}",
     "{id:'JR-009', method:'linear', condition:'固定偏倚（常量显著≠0、斜率不显著）', verdict:'可接受', plant:'青岛工厂', subplant:'一分厂', note:'量程范围内固定偏倚，可通过纠偏修正'}"),
    ("{id:'JR-010', method:'linear', condition:'线性偏倚（斜率显著≠0）且平均偏倚在区间内', verdict:'较理想可接受', note:'可按回归结果对偏倚加以修正'}",
     "{id:'JR-010', method:'linear', condition:'线性偏倚（斜率显著≠0）且平均偏倚在区间内', verdict:'有条件接受', plant:'青岛工厂', subplant:'一分厂', note:'可按回归结果对偏倚加以修正'}"),
    ("{id:'JR-011', method:'linear', condition:'斜率不显著且有偏倚点位于区间外不同侧', verdict:'不可接受', note:'测量系统有偏倚且无法修正，不能接受'}",
     "{id:'JR-011', method:'linear', condition:'斜率不显著且有偏倚点位于区间外不同侧', verdict:'不可接受', plant:'青岛工厂', subplant:'一分厂', note:'测量系统有偏倚且无法修正，不能接受'}"),
    ("{id:'JR-012', method:'stability', condition:'Xbar-R 控制图无出界点', verdict:'可接受', note:'过程稳定，无异常波动'}",
     "{id:'JR-012', method:'stability', condition:'Xbar-R 控制图无出界点', verdict:'可接受', plant:'烟台工厂', subplant:'一分厂', note:'过程稳定，无异常波动'}"),
    ("{id:'JR-013', method:'cgcgk', condition:'Cg ≥ 1.33 且 Cgk ≥ 1.33', verdict:'可接受', note:'量具重复性、偏倚满足要求，能力充足'}",
     "{id:'JR-013', method:'cgcgk', condition:'Cg ≥ 1.33 且 Cgk ≥ 1.33', verdict:'可接受', plant:'青岛工厂', subplant:'二分厂', note:'量具重复性、偏倚满足要求，能力充足'}"),
    ("{id:'JR-014', method:'cgcgk', condition:'Cg < 1.33', verdict:'不可接受', note:'量具重复性差，需检修/清洁/更换量具或提升装夹稳定性'}",
     "{id:'JR-014', method:'cgcgk', condition:'Cg < 1.33', verdict:'不可接受', plant:'青岛工厂', subplant:'二分厂', note:'量具重复性差，需检修/清洁/更换量具或提升装夹稳定性'}"),
    ("{id:'JR-015', method:'cgcgk', condition:'Cg 合格、Cgk < 1.33', verdict:'有条件接受', note:'存在系统性偏倚，需重新校准、修正补偿、核对标准件真值'}",
     "{id:'JR-015', method:'cgcgk', condition:'Cg 合格、Cgk < 1.33', verdict:'有条件接受', plant:'青岛工厂', subplant:'二分厂', note:'存在系统性偏倚，需重新校准、修正补偿、核对标准件真值'}"),
    ("{id:'JR-016', method:'cgcgk', condition:'Cgk < 0', verdict:'不可接受', note:'偏倚超出 10% 公差，量具不可使用，立即整改复测'}",
     "{id:'JR-016', method:'cgcgk', condition:'Cgk < 0', verdict:'不可接受', plant:'青岛工厂', subplant:'二分厂', note:'偏倚超出 10% 公差，量具不可使用，立即整改复测'}"),
    ("{id:'JR-017', method:'cgcgk', condition:'6σ/T ≤ 15%', verdict:'优秀', note:'重复性误差占比优秀'}",
     "{id:'JR-017', method:'cgcgk', condition:'6σ/T ≤ 15%', verdict:'可接受', plant:'青岛工厂', subplant:'二分厂', note:'重复性误差占比优秀'}"),
    ("{id:'JR-018', method:'cgcgk', condition:'6σ/T ≤ 20%', verdict:'可接受', note:'重复性误差占比可接受'}",
     "{id:'JR-018', method:'cgcgk', condition:'6σ/T ≤ 20%', verdict:'可接受', plant:'青岛工厂', subplant:'二分厂', note:'重复性误差占比可接受'}"),
]
for old, new in judge_patch:
    rep(old, new, 'judgeRules seed ' + old[old.find('JR-')+3:old.find('JR-')+8], cnt=2)

# 新增 2 条演示（GRR/KAPPA @ 烟台工厂一分厂）——加在两处 seed 的 JR-018 后
rep("    {id:'JR-018', method:'cgcgk', condition:'6σ/T ≤ 20%', verdict:'可接受', plant:'青岛工厂', subplant:'二分厂', note:'重复性误差占比可接受'}\n  ];",
    "    {id:'JR-018', method:'cgcgk', condition:'6σ/T ≤ 20%', verdict:'可接受', plant:'青岛工厂', subplant:'二分厂', note:'重复性误差占比可接受'},\n    {id:'JR-019', method:'GRR', condition:'NDC ≥ 5 且 %GRR < 10%', verdict:'可接受', plant:'烟台工厂', subplant:'一分厂', note:'烟台工厂 GRR 判定（示例）'},\n    {id:'JR-020', method:'KAPPA', condition:'Kappa > 0.75', verdict:'可接受', plant:'烟台工厂', subplant:'一分厂', note:'烟台工厂 KAPPA 判定（示例）'}\n  ];",
    "judgeRules 新增 2 条", cnt=2)

io.open(P, 'w', encoding='utf-8').write(t)
print('seed 修改完成')
