# -*- coding: utf-8 -*-
"""multi3: PlanPage 挂载任务抽屉 + ConvertModal 追加语义 + PlanDetail 文案"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'count=%d for: %s...' % (c, old[:70])
    s = s.replace(old, new)

# 1) 清理 PlanPage 残留旧注释
rep("""  // 转 GRR / KAPPA：将勾选计划的分析关联类型改为对应类型，生成台账「待采集」记录，并跳转对应台账
    // 转分析方法（GRR / KAPPA / 线性偏移 / 稳定性 / CgCgk）：将勾选计划的分析关联类型改为对应方法，生成台账「待采集」记录，并跳转对应录入数据页；一个计划可追加多个方法（一计划""",
    """  // 转分析方法（GRR / KAPPA / 线性偏移 / 稳定性 / CgCgk）：将勾选计划的分析关联类型改为对应方法，生成台账「待采集」记录，并跳转对应录入数据页；一个计划可追加多个方法（一计划""")

# 2) PlanPage state 加 taskPlan
rep("""  const [edit,setEdit]=useState(null);       // 编辑计划信息
  const [selectedRowKeys,setSelectedRowKeys]=useState([]); // 勾选用于 转GRR/转KAPPA""",
    """  const [edit,setEdit]=useState(null);       // 编辑计划信息
  const [taskPlan,setTaskPlan]=useState(null); // 计划分析任务抽屉（一计划多任务）
  const [selectedRowKeys,setSelectedRowKeys]=useState([]); // 勾选用于转分析方法""")

# 3) PlanActions 调用传 onTasks
rep("""<PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)}/>""",
    """<PlanActions r={r} onDetail={()=>setDetail(r)} onEdit={()=>setEdit(r)} onTasks={()=>setTaskPlan(r)}/>""")

# 4) 挂载 PlanTaskDrawer
rep("""    {batchModal && <BatchPlanModal value={batchModal} onClose={()=>setBatchModal(null)}/>}
    {convert && <ConvertModal plan={convert} onClose={()=>setConvert(null)}/>}
    {detail && <PlanDetail plan={detail} onClose={()=>setDetail(null)} onConvert={()=>{ setDetail(null); setConvert(detail); }}/>}
    {edit && <PlanEditModal plan={edit} onClose={()=>setEdit(null)}/>}""",
    """    {batchModal && <BatchPlanModal value={batchModal} onClose={()=>setBatchModal(null)}/>}
    {convert && <ConvertModal plan={convert} onClose={()=>setConvert(null)}/>}
    {detail && <PlanDetail plan={detail} onClose={()=>setDetail(null)} onConvert={()=>{ setDetail(null); setConvert(detail); }}/>}
    {edit && <PlanEditModal plan={edit} onClose={()=>setEdit(null)}/>}
    {taskPlan && <PlanTaskDrawer plan={taskPlan} onClose={()=>setTaskPlan(null)}/>}""")

# 5) ConvertModal：已定型类型 disabled + 追加语义
rep("""        <Col span={8}><Form.Item name="type" label="分析方法" rules={[{required:true}]}><Select options={ENUM.analysisTypes.map(c=>({value:c,label:ANAL_SHORT[c]}))} onChange={changeType}/></Form.Item></Col>""",
    """        <Col span={8}><Form.Item name="type" label="分析方法" rules={[{required:true}]}><Select options={ENUM.analysisTypes.map(c=>({value:c,label:ANAL_SHORT[c], disabled: planRecords(d,plan.id).some(r=>recKindId(r)===c)}))} onChange={changeType}/></Form.Item></Col>""")

rep("""      const rid=spawnRecord(s, p.id, { type:v.type, standard:v.standard, method:v.method,
        params: isGrrK? {ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10} : {...(TYPE_PARAMS[v.type]||{}), ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},
        object:p.object, instId:p.instId, instName:p.instName, owner:v.owner||p.owner, note:'计划定型为 '+v.type+'，待台账内录入数据' });
      p.recordId=rid;
      logAction(s.me.name,'计划定型',p.id,'定型为 '+v.type+' · '+v.standard+'，生成台账记录 '+rid);""",
    """      const rid=spawnRecord(s, p.id, { type:v.type, standard:v.standard, method:v.method,
        params: isGrrK? {ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10} : {...(TYPE_PARAMS[v.type]||{}), ops:Number(v.ops)||3, trials:Number(v.trials)||3, parts:Number(v.parts)||10},
        object:p.object, instId:p.instId, instName:p.instName, owner:v.owner||p.owner, note:'计划定型为 '+v.type+'，待台账内录入数据' });
      p.recordId=rid;
      p.methods=[...new Set([...(p.methods||[]), v.type])];
      syncPlanFromRecord(s,p.id);
      logAction(s.me.name,'计划定型',p.id,'定型为 '+v.type+' · '+v.standard+'，生成台账记录 '+rid);""")

# 6) PlanDetail 定型按钮文案 + 创建方式文案
rep(">定型（转 GRR / KAPPA）</Button>", ">转分析方法</Button>")
rep("""{key:'创建方式', label:'创建方式', children: multi? <Tag color="purple">多器具合并计划（1 计划 = 1 分析任务，每台器具各 1 条分析记录）</Tag>:<Tag>一器具一计划</Tag>},""",
    """{key:'创建方式', label:'创建方式', children: multi? <Tag color="purple">多器具合并计划</Tag>:<Tag>一器具一计划</Tag>},""")

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('multi3 全部替换成功')
