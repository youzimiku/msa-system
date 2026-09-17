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

# 1) 查询条件：工厂后新增车间下拉
rep("""        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>工厂</span><Select allowClear style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>关键词</span>""",
"""        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>工厂</span><Select allowClear style={{width:140}} options={PLANTS_OPT} value={fPlant} onChange={setFPlant}/>
        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>车间</span><Select allowClear style={{width:120}} options={SUBPLANTS_OPT} value={fSub} onChange={setFSub}/>
        <span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>关键词</span>""",
"查询条件加车间下拉", cnt=1)

# 2) 抽样规则表格：按工厂/车间（查询生效值）过滤
rep("""          <Table rowKey="id" size="small" dataSource={(d.samplingRules||[]).filter(r=>!selMethod || String(r.method).toLowerCase()===String(selMethod).toLowerCase())} scroll={{x:1500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={samplingCols}/>""",
"""          <Table rowKey="id" size="small" dataSource={(d.samplingRules||[]).filter(r=>!selMethod || String(r.method).toLowerCase()===String(selMethod).toLowerCase()).filter(r=>!fQPlant || r.plant===fQPlant).filter(r=>!fQSub || r.subplant===fQSub)} scroll={{x:1500}} pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}} columns={samplingCols}/>""",
"抽样规则按工厂车间过滤", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('完成')
