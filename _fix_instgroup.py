# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(src, old, new, desc, expect=1):
    n = src.count(old)
    ok = n == expect
    print(f'{desc}: 出现 {n} 次 (期望 {expect})', '-> 替换' if ok else '!!不匹配跳过')
    return src.replace(old, new) if ok else src

# A. 菜单恢复 计量器具台账
src = rep(src,
"""  /* 基础数据（按操作顺序：器具 → 器具组 → 特性 → 抽样 → 样本库） */
  /* 计量器具台账已按需求隐藏（保留页面组件与内部跳转，仅移除菜单入口） */
  {key:'instgroup', icon:'▦', label:'器具组维护', group:'基础数据'},""",
"""  /* 基础数据（按操作顺序：器具 → 器具组 → 特性 → 抽样 → 样本库） */
  {key:'ledger', icon:'☑', label:'计量器具台账', group:'基础数据'},
  {key:'instgroup', icon:'▦', label:'器具组维护', group:'基础数据'},""",
'A 菜单恢复计量器具台账')

# B. 初始化逻辑：补 下次计划日期 / 提醒周期 / 联动后的下次提醒时间
src = rep(src,
"""    if(!g.calCycle) g.calCycle=(ix%2===0?12:6);
    if(!g.lastExec) g.lastExec='暂无';
    if(!g.nextRemind) g.nextRemind=(g.lastExec&&g.lastExec!=='暂无')?g.lastExec:'暂无';
    if(!g.records) g.records=[];""",
"""    if(!g.calCycle) g.calCycle=(ix%2===0?12:6);
    if(!g.lastExec) g.lastExec='暂无';
    if(!g.remindAdvance) g.remindAdvance=20;
    if(!g.nextPlanDate) g.nextPlanDate=(g.lastExec&&g.lastExec!=='暂无')?dayjs(g.lastExec).add(g.calCycle||12,'month').format('YYYY-MM-DD'):'暂无';
    if(!g.nextRemind) g.nextRemind=(g.nextPlanDate&&g.nextPlanDate!=='暂无')?dayjs(g.nextPlanDate).subtract(g.remindAdvance||20,'day').format('YYYY-MM-DD'):'暂无';
    if(!g.records) g.records=[];""",
'B 初始化补字段')

# C. 列表列：加 下次计划日期 / 提醒周期
src = rep(src,
"""    {title:'上次执行时间', dataIndex:'lastExec', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'下次提醒时间', dataIndex:'nextRemind', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'组成员', width:170, render:(_,r)=>memberText(r)},""",
"""    {title:'上次执行时间', dataIndex:'lastExec', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'下次计划日期', dataIndex:'nextPlanDate', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'提醒周期(天)', width:105, render:(_,r)=><span className="mono">{r.remindAdvance||20}</span>},
    {title:'下次提醒时间', dataIndex:'nextRemind', width:115, render:v=><span className="mono tiny">{v||'暂无'}</span>},
    {title:'组成员', width:170, render:(_,r)=>memberText(r)},""",
'C 列表加列')

# D1. 表单加 onValuesChange
src = rep(src,
'    <Form form={form} layout="vertical" size="small">',
'    <Form form={form} layout="vertical" size="small" onValuesChange={onValuesChange}>',
'D1 表单挂联动')

# D2. 表单字段：加 下次计划日期 / 提醒周期
src = rep(src,
"""        <Col span={6}><Form.Item name="calCycle" label="检验周期(月)" rules={[{required:true}]}><Input type="number"/></Form.Item></Col>
        <Col span={6}><Form.Item name="lastExec" label="上次执行时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>
        <Col span={6}><Form.Item name="nextRemind" label="下次提醒时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>""",
"""        <Col span={6}><Form.Item name="calCycle" label="检验周期(月)" rules={[{required:true}]}><Input type="number"/></Form.Item></Col>
        <Col span={6}><Form.Item name="lastExec" label="上次执行时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>
        <Col span={6}><Form.Item name="nextPlanDate" label="下次计划日期"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>
        <Col span={6}><Form.Item name="remindAdvance" label="提醒周期(天)"><Input type="number" placeholder="如 20"/></Form.Item></Col>
        <Col span={6}><Form.Item name="nextRemind" label="下次提醒时间"><Input placeholder="YYYY-MM-DD"/></Form.Item></Col>""",
'D2 表单加字段')

# D3. onValuesChange 逻辑定义（插入 onOk 之前）
src = rep(src,
"""  const onOk=async()=>{
    const vals=await form.validateFields();
    if((vals.type||'inst')==='kappa' && !((vals.members||[]).length) && !(vals.posts&&vals.posts.length)){ toast.warn('kappa人员组请至少维护岗位或成员'); return; }""",
"""  /* 联动：上次执行时间+检验周期 -> 下次计划日期 -> 下次提醒时间（提醒周期=提前天数） */
  const onValuesChange=(ch)=>{
    const fv=(k)=>form.getFieldValue(k);
    if('lastExec' in ch || 'calCycle' in ch){
      const le=('lastExec' in ch)?ch.lastExec:fv('lastExec');
      const cc=('calCycle' in ch)?ch.calCycle:fv('calCycle');
      if(le && cc){ const nd=dayjs(le).add(Number(cc),'month').format('YYYY-MM-DD'); const ra=('remindAdvance' in ch)?ch.remindAdvance:fv('remindAdvance')||20; form.setFieldsValue({nextPlanDate:nd, nextRemind:dayjs(nd).subtract(Number(ra),'day').format('YYYY-MM-DD')}); }
    }
    if('nextPlanDate' in ch || 'remindAdvance' in ch){
      const nd=('nextPlanDate' in ch)?ch.nextPlanDate:fv('nextPlanDate');
      const ra=('remindAdvance' in ch)?ch.remindAdvance:fv('remindAdvance');
      if(nd && ra){ form.setFieldsValue({nextRemind:dayjs(nd).subtract(Number(ra),'day').format('YYYY-MM-DD')}); }
    }
  };
  const onOk=async()=>{
    const vals=await form.validateFields();
    if((vals.type||'inst')==='kappa' && !((vals.members||[]).length) && !(vals.posts&&vals.posts.length)){ toast.warn('kappa人员组请至少维护岗位或成员'); return; }""",
'D3 联动逻辑')

# E. 详情抽屉加字段
src = rep(src,
"""      {key:'上次执行时间', label:'上次执行时间', children:rec.lastExec||'暂无'},
      {key:'下次提醒时间', label:'下次提醒时间', children:rec.nextRemind||'暂无'},""",
"""      {key:'上次执行时间', label:'上次执行时间', children:rec.lastExec||'暂无'},
      {key:'下次计划日期', label:'下次计划日期', children:rec.nextPlanDate||'暂无'},
      {key:'提醒周期', label:'提醒周期', children:rec.remindAdvance?rec.remindAdvance+' 天':'20 天'},
      {key:'下次提醒时间', label:'下次提醒时间', children:rec.nextRemind||'暂无'},""",
'E 详情加字段')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
