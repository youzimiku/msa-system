# -*- coding: utf-8 -*-
"""v2.6 第一批：新增 质量特性维护 / 抽样方法维护 两个基础数据页面"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:80])
    s = s.replace(old, new, cnt)

# ---------- 1. seed 增补：质量特性 / 分析方法代码 / 取样规则 ----------
SEED_ADD = """  /* ---------------- 质量特性基础数据（业务口径：特性≠七大检测方法；特性计划模块本次不做，字典先行） ---------------- */
  const characteristics = [
    {id:'CHAR-2026-001', name:'轴径 φ50±0.05', type:'SC', partName:'轴类件', processName:'精加工', category:'计量型', unit:'mm', target:'50', usl:'50.05', lsl:'49.95', source:'CP-轴类控制计划', standardId:'STD-MSA-001', status:'启用', note:'关键尺寸，配数显卡尺，GRR+线性+Cg/Cgk', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-002', name:'轴径 φ10±0.02', type:'CC', partName:'轴类件', processName:'精加工', category:'计量型', unit:'mm', target:'10', usl:'10.02', lsl:'9.98', source:'CP-轴类控制计划', standardId:'STD-MSA-001', status:'启用', note:'外径千分尺测量，稳定性分析', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-003', name:'孔径 φ8H7 通/止', type:'CC', partName:'孔类件', processName:'检验', category:'计数型', unit:'', target:'', usl:'', lsl:'', source:'CP-孔类控制计划', standardId:'STD-MSA-003', status:'启用', note:'光滑塞规通止判定，KAPPA 分析', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-004', name:'螺栓拧紧力矩 25N·m', type:'SC', partName:'轴类件', processName:'装配', category:'计量型', unit:'N·m', target:'25', usl:'27.5', lsl:'22.5', source:'CP-装配控制计划', standardId:'STD-MSA-001', status:'启用', note:'安全相关扭矩，GRR+偏倚', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-005', name:'称量 100g', type:'普通', partName:'标准件', processName:'检验', category:'计量型', unit:'g', target:'100', usl:'100.1', lsl:'99.9', source:'CP-实验室控制计划', standardId:'STD-MSA-001', status:'启用', note:'电子天平', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-006', name:'烘箱温度 120℃', type:'普通', partName:'标准件', processName:'检验', category:'计量型', unit:'℃', target:'120', usl:'122', lsl:'118', source:'CP-实验室控制计划', standardId:'STD-MSA-001', status:'启用', note:'数字温度计', editor:'李工程师', editorDate:'2026-09-09'},
    {id:'CHAR-2026-007', name:'液压试验压力 1.0MPa', type:'SC', partName:'轴类件', processName:'检验', category:'计量型', unit:'MPa', target:'1.0', usl:'1.05', lsl:'0.95', source:'CP-液压控制计划', standardId:'STD-MSA-001', status:'启用', note:'精密压力表，Cg/Cgk', editor:'李工程师', editorDate:'2026-09-09'}
  ];

  /* ---------------- 抽样方法基础数据（业务口径：七大检测方法代码 + 合并取样配置 + 取样规则一张表） ---------------- */
  const anMethods = [
    {code:'GRR', name:'GRR（重复性+再现性）', needSample:'是', canMerge:'是', mergeWith:'', defaultType:'计量型', status:'启用', note:'10 件×3 人×3 次'},
    {code:'KAPPA', name:'KAPPA（计数型一致性）', needSample:'是', canMerge:'否', mergeWith:'', defaultType:'计数型', status:'启用', note:'50 件×3 人×3 次'},
    {code:'LINEAR', name:'线性', needSample:'是', canMerge:'是', mergeWith:'BIAS', defaultType:'计量型', status:'启用', note:'5 标准件×12 次，覆盖量程'},
    {code:'BIAS', name:'偏倚性', needSample:'是', canMerge:'是', mergeWith:'LINEAR', defaultType:'计量型', status:'启用', note:'1 标准件×15 次'},
    {code:'STABILITY', name:'稳定性', needSample:'是', canMerge:'否', mergeWith:'', defaultType:'计量型', status:'启用', note:'25 子组×5 次，跨 4 周~3 个月'},
    {code:'CGCGK', name:'Cg/Cgk（Type1）', needSample:'是', canMerge:'否', mergeWith:'', defaultType:'计量型', status:'启用', note:'标准件 50 次'},
    {code:'RES', name:'分辨率', needSample:'否', canMerge:'否', mergeWith:'', defaultType:'计量型', status:'启用', note:'不取样，直接录入'}
  ];
  const samplingRules = [
    {id:'SR-001', method:'GRR', category:'其他', sampleDefault:10, sampleMin:1, sampleMax:30, opsDefault:3, opsMin:1, opsMax:5, trialsDefault:3, trialsMin:2, trialsMax:5, useOps:true, readings:'60~90', note:'重复性+再现性合并取样：10 个生产件×3 人×每件 3 次，覆盖过程散差、重新装夹；盲测随机序'},
    {id:'SR-002', method:'KAPPA', category:'其他', sampleDefault:50, sampleMin:20, sampleMax:50, opsDefault:3, opsMin:2, opsMax:5, trialsDefault:3, trialsMin:1, trialsMax:5, useOps:true, readings:'450', note:'50 件×3 人×每件 3 次（业务报告样例 50 件/3 人/每件 1 次判定），与参考值交叉表+检验员间交叉+三档判定'},
    {id:'SR-003', method:'linear', category:'线性类', sampleDefault:5, sampleMin:1, sampleMax:10, opsDefault:1, opsMin:1, opsMax:3, trialsDefault:12, trialsMin:10, trialsMax:20, useOps:false, readings:'50~60', note:'线性+偏倚合并取样：线性 5 个标准件覆盖 0/25/50/75/100% 量程×每件 12 次；偏倚 1 件×15 次'},
    {id:'SR-004', method:'stability', category:'稳定性类', sampleDefault:25, sampleMin:25, sampleMax:100, opsDefault:1, opsMin:1, opsMax:3, trialsDefault:5, trialsMin:3, trialsMax:10, useOps:false, readings:'75~125', note:'稳定性单独取样：25 个子组×每期 5 次，跨 4 周~3 个月，SPC 判异'},
    {id:'SR-005', method:'cgcgk', category:'其他', sampleDefault:1, sampleMin:1, sampleMax:1, opsDefault:1, opsMin:1, opsMax:1, trialsDefault:50, trialsMin:50, trialsMax:200, useOps:false, readings:'50', note:'Cg/Cgk 单独取样：1 件标准件独立装夹连续测 50 次，参考值±10% 标准误控制线'},
    {id:'SR-006', method:'resolution', category:'其他', sampleDefault:0, sampleMin:0, sampleMax:0, opsDefault:0, opsMin:0, opsMax:0, trialsDefault:0, trialsMin:0, trialsMax:0, useOps:false, readings:'—', note:'分辨率不取样：直接录入分辨率值，与过程公差比对（≤1/10 公差）'}
  ];

  /* ---------------- 审计日志（初始几条） ---------------- */"""
rep('  /* ---------------- 审计日志（初始几条） ---------------- */', SEED_ADD, 1, 'seed-add')

# ---------- 2. buildSeed return ----------
rep("return { me:{ name:'李工程师', role:'quality', roleName:'质量工程师' },\n           instruments, calibrations, standards, plans, samples, sampleItems, grr, kappa, linear, stability, cgcgk, resolution, logs, extrapolations:[], instGroups };",
    "return { me:{ name:'李工程师', role:'quality', roleName:'质量工程师' },\n           instruments, calibrations, standards, plans, samples, sampleItems, grr, kappa, linear, stability, cgcgk, resolution, logs, extrapolations:[], instGroups, characteristics, anMethods, samplingRules };",
    1, 'seed-return')

# ---------- 3. applyFieldDefaults 默认数组 ----------
rep("  if(!d.linear) d.linear=[]; if(!d.stability) d.stability=[]; if(!d.cgcgk) d.cgcgk=[]; if(!d.resolution) d.resolution=[]; // 新增分析方法台账（线性/偏移、稳定性、Cg/Cgk、分辨率）",
    "  if(!d.linear) d.linear=[]; if(!d.stability) d.stability=[]; if(!d.cgcgk) d.cgcgk=[]; if(!d.resolution) d.resolution=[]; // 新增分析方法台账（线性/偏移、稳定性、Cg/Cgk、分辨率）\n  if(!d.characteristics) d.characteristics=[]; if(!d.anMethods) d.anMethods=[]; if(!d.samplingRules) d.samplingRules=[]; // 新增基础数据（质量特性 / 抽样方法）",
    1, 'apply-defaults')

# ---------- 4. init 合并新数组 ----------
rep("      ['linear','stability','cgcgk','resolution'].forEach(k=>{ if(!Store.data[k] || !Store.data[k].length) Store.data[k]=(Store.data[k]||[]).concat(sd[k].slice()); });",
    "      ['linear','stability','cgcgk','resolution','characteristics','anMethods','samplingRules'].forEach(k=>{ if(!Store.data[k] || !Store.data[k].length) Store.data[k]=(Store.data[k]||[]).concat(sd[k].slice()); });",
    1, 'init-merge')

# ---------- 5. MENU ----------
rep("  {key:'standard', icon:'▥', label:'检验标准维护', group:'MSA 管理'},\n  {key:'sample', icon:'⬡', label:'样本管理', group:'MSA 管理'},",
    "  {key:'standard', icon:'▥', label:'检验标准维护', group:'MSA 管理'},\n  {key:'char', icon:'♯', label:'质量特性维护', group:'MSA 管理'},\n  {key:'sampling', icon:'∿', label:'抽样方法维护', group:'MSA 管理'},\n  {key:'sample', icon:'⬡', label:'样本管理', group:'MSA 管理'},",
    1, 'menu')

# ---------- 6. PAGE_TITLE ----------
rep("'standard':'MSA 检验标准维护','sample':'样本管理',",
    "'standard':'MSA 检验标准维护','char':'质量特性维护','sampling':'抽样方法维护','sample':'样本管理',",
    1, 'page-title')

# ---------- 7. renderPage ----------
rep("    if(page==='standard') return <StandardPage/>;\n    if(page==='sample') return <SamplePage/>;",
    "    if(page==='standard') return <StandardPage/>;\n    if(page==='char') return <CharPage/>;\n    if(page==='sampling') return <SamplingPage/>;\n    if(page==='sample') return <SamplePage/>;",
    1, 'render-page')

open(P, 'w', encoding='utf-8').write(s)
print('batch1 OK 长度', len(s))
