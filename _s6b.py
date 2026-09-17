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

rep("        <Col span={8}><Form.Item name=\"qcArea\" label=\"质检区划\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"plant\" label=\"工厂\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"subplant\" label=\"分厂\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"effDate\" label=\"生效日期\">",
    "        <Col span={8}><Form.Item name=\"qcArea\" label=\"质检区划\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"plant\" label=\"工厂\"><Input/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"subplant\" label=\"分厂\"><Input/></Form.Item></Col>\n        <Col span={24}><Form.Item name=\"groupIds\" label=\"绑定器具组（会议口径：为周期自动选样准备）\" tooltip=\"周期 MSA 校验时，系统按标准绑定的器具组自动筛选样机器具生成计划\"><Select mode=\"multiple\" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+' '+g.name}))}/></Form.Item></Col>\n        <Col span={8}><Form.Item name=\"effDate\" label=\"生效日期\">")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
