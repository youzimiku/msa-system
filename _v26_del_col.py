# -*- coding: utf-8 -*-
"""1) MSA计划列表去掉分计划列 2) 操作列去掉台账按钮，清理taskPlan抽屉"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

# 1) 删除分计划列整行
OLD_COL = """    {title:'分计划', width:130, render:(_,r)=>{ const recs=planRecords(d,r.id); return recs.length? <Space size={2} wrap>{recs.map(x=><Tag key={x.id} color={ANAL_COLOR[recKindId(x)]||'default'}>{ANAL_SHORT[recKindId(x)]||recKindId(x)}</Tag>)}</Space> : <span className="tiny">未定型</span>; }},
"""
assert s.count(OLD_COL) == 1, '分计划列定位失败 %d' % s.count(OLD_COL)
s = s.replace(OLD_COL, '', 1)

# 2) 操作列去掉台账按钮（PlanActions）
OLD_ACT = """function PlanActions({r, onDetail, onEdit, onTasks}){
  return <Space size={0}>
    <Button size="small" type="link" onClick={onTasks}>台账</Button>
    <Button size="small" type="link" disabled={!canDo(Store.get().me.role,'edit')} onClick={onEdit}>编辑</Button>
    <Button size="small" type="link" onClick={onDetail}>详情</Button>
  </Space>;
}"""
NEW_ACT = """function PlanActions({r, onDetail, onEdit}){
  return <Space size={0}>
    <Button size="small" type="link" disabled={!canDo(Store.get().me.role,'edit')} onClick={onEdit}>编辑</Button>
    <Button size="small" type="link" onClick={onDetail}>详情</Button>
  </Space>;
}"""
assert s.count(OLD_ACT) == 1, 'PlanActions 定位失败 %d' % s.count(OLD_ACT)
s = s.replace(OLD_ACT, NEW_ACT, 1)

# 3) 调用处去掉 onTasks 传参
OLD_CALL = """<PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)} onTasks={()=>setTaskPlan(r)}/>"""
NEW_CALL = """<PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)}/>"""
assert s.count(OLD_CALL) == 1, '调用处定位失败 %d' % s.count(OLD_CALL)
s = s.replace(OLD_CALL, NEW_CALL, 1)

# 4) 删除 taskPlan 状态声明
OLD_ST = """const [taskPlan,setTaskPlan]=useState(null); // 计划分析任务抽屉（一计划多任务）"""
assert s.count(OLD_ST) == 1, 'taskPlan状态定位失败 %d' % s.count(OLD_ST)
s = s.replace(OLD_ST, '', 1)

# 5) 删除 taskPlan 抽屉渲染行
OLD_REN = """    {taskPlan && <PlanTaskDrawer plan={taskPlan} onClose={()=>setTaskPlan(null)}/>}"""
assert s.count(OLD_REN) == 1, 'taskPlan渲染定位失败 %d' % s.count(OLD_REN)
s = s.replace(OLD_REN, '', 1)

# 6) 删除 PlanTaskDrawer 组件定义（整段）
import re
i = s.find('/* 计划分计划抽屉：一个 MSA 总计划下挂多个分析方法的分计划（取样计划 → 录入 → 分析） */')
j = s.find('function nextPlanId(s){', i)
assert i > 0 and j > i, 'PlanTaskDrawer定义定位失败 %d %d' % (i, j)
s = s[:i] + s[j:]

open(P, 'w', encoding='utf-8').write(s)
print('OK 长度', len(s))
