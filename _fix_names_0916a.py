# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global t
    assert t.count(old) == 1, ('锚点不唯一或不存在: %s...' % old[:80])
    t = t.replace(old, new)

# 1) 被测参数列表：检验方法 列名 → 分析方法
rep("{title:'检验方法', width:230, render:(_,r)=><Select size=\"small\" className=\"msa-method-select\"",
    "{title:'分析方法', width:230, render:(_,r)=><Select size=\"small\" className=\"msa-method-select\"")

# 2) 线性 / 偏倚性 方法组统一为 LIN_BIAS
rep("    {code:'LINEAR', name:'线性', needSample:'是', canMerge:'是', mergeWith:'BIAS', defaultType:'计量型', status:'启用', note:'5 标准件×12 次，覆盖量程'},",
    "    {code:'LINEAR', name:'线性', needSample:'是', canMerge:'是', mergeWith:'LIN_BIAS', defaultType:'计量型', status:'启用', note:'5 标准件×12 次，覆盖量程'},")
rep("    {code:'BIAS', name:'偏倚性', needSample:'是', canMerge:'是', mergeWith:'LINEAR', defaultType:'计量型', status:'启用', note:'1 标准件×15 次'},",
    "    {code:'BIAS', name:'偏倚性', needSample:'是', canMerge:'是', mergeWith:'LIN_BIAS', defaultType:'计量型', status:'启用', note:'1 标准件×15 次'},")

# 3) 菜单：线性/偏移台账 → 线性/偏倚台账
rep("{key:'entry_linear', icon:'⌗', label:'线性/偏移台账', group:'台账'},",
    "{key:'entry_linear', icon:'⌗', label:'线性/偏倚台账', group:'台账'},")

# 4) 菜单：线性/偏移录入数据 → 线性/偏倚录入数据
rep("{key:'data_linear', icon:'⌗', label:'线性/偏移录入数据', group:'数据录入'},",
    "{key:'data_linear', icon:'⌗', label:'线性/偏倚录入数据', group:'数据录入'},")

# 5) 页面标题映射
rep("'entry_linear':'线性/偏移台账','entry_stability':'稳定性台账'",
    "'entry_linear':'线性/偏倚台账','entry_stability':'稳定性台账'")
rep("'data_linear':'线性/偏移录入数据','data_stability':'稳定性录入数据'",
    "'data_linear':'线性/偏倚录入数据','data_stability':'稳定性录入数据'")

# 6) 操作人弹窗标题
rep("kindTitle={grr:'GRR 台账',kappa:'KAPPA 台账',linear:'线性/偏移台账',stability:'稳定性台账',cgcgk:'Cg/Cgk 台账'}[kind]||kind;",
    "kindTitle={grr:'GRR 台账',kappa:'KAPPA 台账',linear:'线性/偏倚台账',stability:'稳定性台账',cgcgk:'Cg/Cgk 台账'}[kind]||kind;")

# 7) ENTRY_CFG linear：name + title
rep("linear:{arr:'linear', idPref:'LIN', name:'线性/偏移', title:'线性/偏移台账', desc:'标准件测量（覆盖量程 0/25/50/75/100%）',",
    "linear:{arr:'linear', idPref:'LIN', name:'线性/偏倚', title:'线性/偏倚台账', desc:'标准件测量（覆盖量程 0/25/50/75/100%）',")

io.open(P, 'w', encoding='utf-8').write(t)
print('替换完成', len(t))
