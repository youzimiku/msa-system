# -*- coding: utf-8 -*-
"""desc2: 残留说明删除"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'FAIL count=%d for: %s' % (c, old[:60])
    s = s.replace(old, new)

# 1) 器具筛选区"说明：复评状态对全部器具生效"整块
old1 = '<div className="tiny mt4">说明：复评状态对全部器具生效；厂商 / 型号 / 产线 / 工序 仅在选「全部器具」时出现，辅助挑样。器具仅「在用 / 待校准」且「无未闭环计划」的可纳入（状态一致性校验：器具存在未闭环计划时禁止重复生成；周期复评需待上一计划闭环后重新发起）。</div>'
i = s.find(old1)
assert i > 0, 'mt4 block not found'
# 吃掉前面空白
k = i
while k > 0 and s[k-1] in ' \n\t':
    k -= 1
s = s[:k] + s[i+len(old1):]

# 2) 器具表格提示列说明简化（去 tiny、去取样说明）
rep("""{title:'提示', width:210, render:(_,i)=> i.active? <Tag color="volcano">已有未闭环计划</Tag> : i.overdue? <Tag color="red">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span className="tiny">{stdSel? (mMethods.length? '将生成 '+mMethods.length+' 个计划（'+mMethods.map(x=>ANAL_SHORT[x]).join('、')+'），按['+ANAL_SHORT[effMeth]+']默认取样，可改上方 人数/次数/样本数' : '将生成未定型计划（待转），取样按['+ANAL_SHORT[effMeth]+']默认'):'请先选零件与标准'}</span> : <span className="tiny">停用/报废不可选</span>}""",
"""{title:'提示', width:210, render:(_,i)=> i.active? <Tag color="volcano">已有未闭环计划</Tag> : i.overdue? <Tag color="red">检定已过期</Tag> : (i.status==='在用'||i.status==='待校准')? <span>{stdSel? (mMethods.length? '将生成 '+mMethods.length+' 个计划（'+mMethods.map(x=>ANAL_SHORT[x]).join('、')+'）' : '将生成未定型计划') : '未就绪'}</span> : <span>停用/报废不可选</span>}""")

# 3) -（为周期自动选样准备）
rep('gs.length? gs.map(g=>g.name).join(\'、\') : <span className="tiny">-（为周期自动选样准备）</span>',
    'gs.length? gs.map(g=>g.name).join(\'、\') : <span className="tiny">-</span>')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('desc2 完成')
