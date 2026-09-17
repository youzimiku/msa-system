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

# 1) 抽样规则：方法列改只读纯文本
rep("""    {title:'方法', dataIndex:'method', width:120, render:(_,r)=><Select size="small" showSearch value={r.method||undefined} style={{width:108}} options={(d.anMethods||[]).map(m=>({value:m.code,label:STRIP_PAREN(m.name)}))} placeholder="选择方法" onChange={x=>setRuleF(r,'method',x)}/>},""",
"""    {title:'方法', dataIndex:'method', width:150, render:(_,r)=><span>{r.method?STRIP_PAREN(((d.anMethods||[]).find(m=>m.code===r.method)||{}).name||r.method):''}</span>},""",
"方法列只读", cnt=1)

# 2) addRuleRow：必须先选中方法，新增行方法取当前选中方法
rep("""  const addRuleRow=()=>{ const id='SR-0'+(d.samplingRules.length+1); mut(s=>{ s.samplingRules.unshift({id, method:'', category:'其他', sampleDefault:'', sampleMin:'', sampleMax:'', opsDefault:'', opsMin:'', opsMax:'', trialsDefault:'', trialsMin:'', trialsMax:'', useOps:true, readingsMin:'', readingsMax:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, note:''}); logAction(s.me.name,'新增抽样规则',id,'列表新增空白行'); }); };""",
"""  const addRuleRow=()=>{ if(!selMethod){ toast.warn('请先在分析方法列表中选择一个方法'); return; } const id='SR-0'+(d.samplingRules.length+1); mut(s=>{ s.samplingRules.unshift({id, method:selMethod, category:'其他', sampleDefault:'', sampleMin:'', sampleMax:'', opsDefault:'', opsMin:'', opsMax:'', trialsDefault:'', trialsMin:'', trialsMax:'', useOps:true, readingsMin:'', readingsMax:'', plant:PLANTS_OPT[0].value, subplant:SUBPLANTS_OPT[0].value, note:''}); logAction(s.me.name,'新增抽样规则',id,'方法 '+selMethod); }); };""",
"addRuleRow 带选中方法", cnt=1)

# 3) 抽样规则表格按当前选中方法过滤
rep("""          <Table rowKey="id" size="small" dataSource={d.samplingRules||[]} scroll={{x:1500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={samplingCols}/>""",
"""          <Table rowKey="id" size="small" dataSource={(d.samplingRules||[]).filter(r=>!selMethod || String(r.method).toLowerCase()===String(selMethod).toLowerCase())} scroll={{x:1500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={samplingCols}/>""",
"抽样规则按方法过滤", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('完成')
