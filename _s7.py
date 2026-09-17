# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    cnt = s.count(old)
    if cnt != 1:
        print('WARN count=%d for: %s' % (cnt, old[:60])); return
    s = s.replace(old, new)
    print('OK:', old[:46])

# E1 CSS：mono-grid 数据录入表格
rep(".kpi-item .v{font-size:20px;font-weight:700;color:#0f172a;margin-top:2px}",
    ".kpi-item .v{font-size:20px;font-weight:700;color:#0f172a;margin-top:2px}\n.mono-grid{border-collapse:collapse;font-size:12px;font-family:'JetBrains Mono',Consolas,monospace}\n.mono-grid th,.mono-grid td{border:1px solid #e2e8f0;padding:3px 6px;text-align:center;white-space:nowrap}\n.mono-grid th{background:#f1f5f9;color:#334155;font-weight:600}")

# E2 仪表盘方法分布（6 类 + 未定型）
rep("            {['GRR','KAPPA','未定型'].map(k=><div className=\"kpi-item\" key={k}><div className=\"k\">{k}</div><div className=\"v\">{typeCount[k]}</div></div>)}",
    "            {['GRR','KAPPA','线性/偏移','稳定性','Cg/Cgk','分辨率','未定型'].map(k=><div className=\"kpi-item\" key={k}><div className=\"k\">{k}</div><div className=\"v\">{typeCount[k]}</div></div>)}")
rep("          <Alert className=\"mt8\" type=\"info\" showIcon message={'计划定型率：'+Math.round(100*typed.length/plans.length)+'%（'+typed.length+'/'+plans.length+' 已定型为 GRR / KAPPA）。'} />",
    "          <Alert className=\"mt8\" type=\"info\" showIcon message={'计划定型率：'+Math.round(100*typed.length/plans.length)+'%（'+typed.length+'/'+plans.length+' 已定型为分析方法）。'} />")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
