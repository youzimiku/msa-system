# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

new_block = """  /* 台账种子权威重建（演示数据一致性）：按种子 id 集合过滤旧数据残留、去重、锚定基础字段与状态/结论，保证台账与计划跨页面一致 */
  const SEED_IDS={'grr':['GRR-2026-001','GRR-2026-002','GRR-2026-003','GRR-2026-004'],'kappa':['KPA-2026-001','KPA-2026-002'],'linear':['LIN-2026-001','LIN-2026-002'],'stability':['STB-2026-001','STB-2026-002','STB-2026-003'],'cgcgk':['CG-2026-001','CG-2026-002','CG-2026-003','CG-2026-004']};
  const SEED_F={
    'GRR-2026-001':{planId:'MSAP-2026-001',instId:'JJQ-2024-001',instName:'数显卡尺 0~150mm',object:'轴径 φ50±0.05',standard:'STD-MSA-001',numOps:3,numTrials:3,numParts:10,operators:['操作员A·王强','操作员B·刘青','操作员C·陈杰']},
    'GRR-2026-002':{planId:'MSAP-2026-003',instId:'JJQ-2024-007',instName:'数显扭力扳手 5~50N·m',object:'螺栓拧紧力矩 25N·m',standard:'STD-MSA-001',numOps:3,numTrials:3,numParts:10,operators:['操作员A·王强','操作员B·刘青','操作员C·陈杰']},
    'GRR-2026-003':{planId:'MSAP-2026-004',instId:'JJQ-2024-002',instName:'外径千分尺 0~25mm',object:'轴径 φ10±0.02',standard:'STD-MSA-001',numOps:3,numTrials:3,numParts:10,operators:['操作员A·赵磊','操作员B·刘青','操作员C·陈杰']},
    'GRR-2026-004':{planId:'MSAP-2026-009',instId:'JJQ-2024-004',instName:'数显千分表 0~12.7mm',object:'轴径 Φ12.5±0.05',standard:'STD-MSA-001',numOps:3,numTrials:3,numParts:10},
    'KPA-2026-001':{planId:'MSAP-2026-002',instId:'JJQ-2024-008',instName:'光滑塞规 φ8H7',object:'孔径 φ8H7 通/止判定',standard:'STD-MSA-003',numApp:3,numSamples:30,numTrials:3,appNames:['检验员甲·孙丽','检验员乙·周燕','检验员丙·吴敏']},
    'KPA-2026-002':{planId:'MSAP-2026-005',instId:'JJQ-2024-008',instName:'光滑塞规 φ8H7',object:'孔径 φ8H7 通/止判定（二期复评）',standard:'STD-MSA-003',numApp:2,numSamples:30,numTrials:3,appNames:['检验员甲·孙丽','检验员乙·周燕']},
    'LIN-2026-001':{planId:'MSAP-2026-001',instId:'JJQ-2024-001',instName:'数显卡尺 0~150mm',object:'轴径 φ50±0.05',standard:'STD-MSA-001',stds:5,per:12,points:5},
    'LIN-2026-002':{planId:'MSAP-2026-004',instId:'JJQ-2024-002',instName:'外径千分尺 0~25mm',object:'轴径 φ10±0.02',standard:'STD-MSA-001',stds:5,per:12,points:5},
    'STB-2026-001':{planId:'MSAP-2026-004',instId:'JJQ-2024-002',instName:'外径千分尺 0~25mm',object:'轴径 φ10±0.02',standard:'STD-MSA-001',groups:25,per:5},
    'STB-2026-002':{planId:'MSAP-2026-003',instId:'JJQ-2024-007',instName:'数显扭力扳手 5~50N·m',object:'螺栓拧紧力矩 25N·m',standard:'STD-MSA-001',groups:25,per:5},
    'STB-2026-003':{planId:'MSAP-2026-009',instId:'JJQ-2024-004',instName:'数显千分表 0~12.7mm',object:'轴径 Φ12.5±0.05',standard:'STD-MSA-001',groups:25,per:5},
    'CG-2026-001':{planId:'MSAP-2026-001',instId:'JJQ-2024-001',instName:'数显卡尺 0~150mm',object:'轴径 φ50±0.05',standard:'STD-MSA-001',runs:50},
    'CG-2026-002':{planId:'MSAP-2026-003',instId:'JJQ-2024-007',instName:'数显扭力扳手 5~50N·m',object:'螺栓拧紧力矩 25N·m',standard:'STD-MSA-001',runs:50},
    'CG-2026-003':{planId:'MSAP-2026-004',instId:'JJQ-2024-002',instName:'外径千分尺 0~25mm',object:'轴径 φ10±0.02',standard:'STD-MSA-001',runs:50},
    'CG-2026-004':{planId:'MSAP-2026-009',instId:'JJQ-2024-004',instName:'数显千分表 0~12.7mm',object:'轴径 Φ12.5±0.05',standard:'STD-MSA-001',runs:50}
  };
  const SEED_ST={'GRR-2026-001':'已批准','GRR-2026-002':'需整改','GRR-2026-003':'待采集','GRR-2026-004':'待采集','KPA-2026-001':'已批准','KPA-2026-002':'需整改','LIN-2026-001':'已批准','LIN-2026-002':'待采集','STB-2026-001':'已批准','STB-2026-002':'待采集','STB-2026-003':'待采集','CG-2026-001':'已批准','CG-2026-002':'待审核','CG-2026-003':'待采集','CG-2026-004':'待采集'};
  const SEED_CON={'GRR-2026-001':'可接受','GRR-2026-002':'有条件接受','GRR-2026-003':'','GRR-2026-004':'','KPA-2026-001':'优秀(可接受)','KPA-2026-002':'不可接受-需改进','LIN-2026-001':'非常理想可接受','LIN-2026-002':'','STB-2026-001':'可接受','STB-2026-002':'','STB-2026-003':'','CG-2026-001':'可接受','CG-2026-002':'有条件接受','CG-2026-003':'','CG-2026-004':''};
  const REBUILD=(key)=>{ const seen={}; d[key]=(d[key]||[]).filter(r=>{ if(seen[r.id]) return false; seen[r.id]=1; return SEED_IDS[key].indexOf(r.id)>=0; }); (d[key]||[]).forEach(r=>{ const f=SEED_F[r.id]; if(f) Object.assign(r,f); if(SEED_ST[r.id]){ r.reviewStatus=SEED_ST[r.id]; r.conclusion=SEED_CON[r.id]!==undefined?SEED_CON[r.id]:r.conclusion; } }); };
  REBUILD('grr'); REBUILD('kappa'); REBUILD('linear'); REBUILD('stability'); REBUILD('cgcgk');
  (d.plans||[]).forEach(p=>syncPlanFromRecord(d,p.id));
}
"""

# 替换从锚点注释到函数结束的整个块
pat = re.compile(r'  /\* 台账-计划锚点对齐.*?\(d\.plans\|\|\[\]\)\.forEach\(p=>syncPlanFromRecord\(d,p\.id\)\);\n\}\n', re.S)
m = pat.search(src)
if not m:
    print('PATTERN NOT FOUND')
    sys.exit(1)
print('found at', m.start(), m.end())
src = src[:m.start()] + new_block + src[m.end():]
open(p, 'w', encoding='utf-8').write(src)
print('replaced ok, new len', len(src))
