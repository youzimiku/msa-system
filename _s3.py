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

# T1 台账明细列表加"样机"列（是否做MSA 后）
rep("    {title:'是否做MSA', width:84, render:(_,r)=><span>{r.doMsa==='是'?<Tag color=\"blue\">是</Tag>:'否'}</span>},",
    "    {title:'是否做MSA', width:84, render:(_,r)=><span>{r.doMsa==='是'?<Tag color=\"blue\">是</Tag>:'否'}</span>},\n    {title:'样机', width:70, render:(_,r)=><span>{r.prototype==='是'?<Tag color=\"orange\">样机</Tag>:<span className=\"tiny\">—</span>}</span>},")

# T2 器具编辑表单加"样机"（是否做MSA 后）
rep("        <Col span={6}><Form.Item name=\"doMsa\" label=\"是否做MSA\"><Select options={[{value:'是',label:'是'},{value:'否',label:'否'}]}/></Form.Item></Col>\n        <Col span={6}><Form.Item name=\"status\"",
    "        <Col span={6}><Form.Item name=\"doMsa\" label=\"是否做MSA\"><Select options={[{value:'是',label:'是'},{value:'否',label:'否'}]}/></Form.Item></Col>\n        <Col span={6}><Form.Item name=\"prototype\" label=\"样机（周期校验自动筛选）\" tooltip=\"标记为样机的器具：周期性 MSA 校验时系统自动筛选带样机标记的器具生成计划，无需每次手动挑选\"><Select options={[{value:'是',label:'是（样机）'},{value:'否',label:'否'}]}/></Form.Item></Col>\n        <Col span={6}><Form.Item name=\"status\"")

# T3 详情抽屉加样机（是否做MSA 后）
rep("    {key:'是否做MSA', label:'是否做MSA', children:r.doMsa==='是'?<Tag color=\"blue\">是</Tag>:'否'},",
    "    {key:'是否做MSA', label:'是否做MSA', children:r.doMsa==='是'?<Tag color=\"blue\">是</Tag>:'否'},\n    {key:'样机', label:'样机标记', children:r.prototype==='是'?<Tag color=\"orange\">样机（周期校验自动筛选）</Tag>:'否'},")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
