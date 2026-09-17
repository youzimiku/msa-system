# -*- coding: utf-8 -*-
"""Step1：需求2（'-'→文字）+ 需求5（.tiny 颜色统一）+ 结论空值→待采集"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s
R = []

def rep(old, new, expect=None, tag=''):
    global s
    n = s.count(old)
    if expect is not None and n != expect:
        R.append('FAIL[%s] %r x%d != %d' % (tag, old[:50], n, expect))
        return False
    s = s.replace(old, new)
    if tag: R.append('OK[%s] %r x%d' % (tag, old[:44], n))
    return True

# 1) 需求5：.tiny 颜色统一为正文色 #333333
rep('.tiny{font-size:14px;color:#666666}', '.tiny{font-size:14px;color:#333333}', 1, 'tiny统一')

# 2) fmt 返回 '暂无'
rep("function fmt(x, d=3){ return (x==null||isNaN(x))?'-':Number(x).toFixed(d); }",
    "function fmt(x, d=3){ return (x==null||isNaN(x))?'暂无':Number(x).toFixed(d); }", 1, 'fmt暂无')

# 3) 全局空值占位 '-' -> '暂无'（显示层）
n1 = s.count("||'-'"); s = s.replace("||'-'", "||'暂无'"); R.append('OK ||\'-\' x%d' % n1)
n2 = s.count("|| '-'"); s = s.replace("|| '-'", "|| '暂无'"); R.append('OK || \'-\' x%d' % n2)

# 4) 结论存储值与显示：'-' 改 '待采集'/空
rep("conclusion:'-'", "conclusion:''", None, 'conclusion存储')
rep("conclusion: '-'", "conclusion: ''", None, 'conclusion存储2')
rep("conclusion||'-'", "conclusion||'待采集'", None, 'conclusion显示')
rep("conclusion|| '-'", "conclusion|| '待采集'", None, 'conclusion显示2')

# 5) syncPlanFromRecord 汇总
rep("const cons = recs.map(r=>r.conclusion).filter(c=>c&&c!=='-');   p.result = recs.length>1 ? (cons.length? cons.join('；') : '-') : (recs[0].conclusion||'-'); }",
    "const cons = recs.map(r=>r.conclusion).filter(c=>c&&c!=='-'&&c!=='待采集');   p.result = recs.length>1 ? (cons.length? cons.join('；') : '待采集') : (recs[0].conclusion&&recs[0].conclusion!=='-'?recs[0].conclusion:'待采集'); }",
    1, 'syncPlan结论')

# 6) 计划 result 存储 '-' -> 空
n = s.count("result:'-'"); s = s.replace("result:'-'", "result:''"); R.append('OK result存储 x%d' % n)
n = s.count("result: '-'"); s = s.replace("result: '-'", "result: ''"); R.append('OK result存储2 x%d' % n)

# 7) 计划列表/详情 结论列 '-' -> '待采集'
rep("if(!recs.length) return r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:'-';",
    "if(!recs.length) return r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:'待采集';", 1, '计划列表结论')
rep("(plan.result&&plan.result!=='-'?<VerdictTag v={plan.result}/>:'-')",
    "(plan.result&&plan.result!=='-'?<VerdictTag v={plan.result}/>:'待采集')", 1, '计划详情结论')

# 8) 器具 lastMsa 默认 '-' -> '暂无'
rep("lastMsa:i.lastMsa||(msaDates.length?msaDates[msaDates.length-1]:'-'),",
    "lastMsa:i.lastMsa||(msaDates.length?msaDates[msaDates.length-1]:'暂无'),", 1, 'lastMsa默认')

# 9) Dashboard 空值 '-' -> '暂无'
n = s.count("grr.length?Math.round(100*grrOk.length/d.grr.length)+'%':'-'")
s = s.replace("grr.length?Math.round(100*grrOk.length/d.grr.length)+'%':'-'",
              "grr.length?Math.round(100*grrOk.length/d.grr.length)+'%':'暂无'")
n2 = s.count("kappa.length?Math.round(100*kpaOk.length/d.kappa.length)+'%':'-'")
s = s.replace("kappa.length?Math.round(100*kpaOk.length/d.kappa.length)+'%':'-'",
              "kappa.length?Math.round(100*kpaOk.length/d.kappa.length)+'%':'暂无'")
n3 = s.count("inUse.length/d.instruments.length)+'%':'-'")
s = s.replace("inUse.length/d.instruments.length)+'%':'-'",
              "inUse.length/d.instruments.length)+'%':'暂无'")
R.append('OK dashboard %d/%d/%d' % (n, n2, n3))

# 10) seed/applyFieldDefaults '—' 默认值 -> '暂无'
n = s.count("'—'"); 
rep("inspectItem:i.inspectItem||'—'", "inspectItem:i.inspectItem||'暂无'", 1, 'inspectItem')
rep("partName:(s.partName&&s.partName!=='—')?s.partName:pm[0], processName:(s.processName&&s.processName!=='—')?s.processName:pm[1],",
    "partName:(s.partName&&s.partName!=='—')?s.partName:(pm[0]==='—'?'暂无':pm[0]), processName:(s.processName&&s.processName!=='—')?s.processName:(pm[1]==='—'?'暂无':pm[1]),", 1, 'partName')
rep("res:s.res||'—'", "res:s.res||'暂无'", 1, 'standard res')
n = s.count("res:'—'"); s = s.replace("res:'—'", "res:''"); R.append('OK res存储 x%d' % n)
n = s.count("unit:'-'"); s = s.replace("unit:'-'", "unit:''"); R.append('OK unit存储 x%d' % n)
# PARTMAP 中 '—'
n = s.count("['—','—']"); s = s.replace("['—','—']", "['暂无','暂无']"); R.append('OK PARTMAP x%d' % n)

io.open(P, 'w', encoding='utf-8').write(s)
print('\n'.join(R))
print('saved delta:', len(s)-len(orig))
