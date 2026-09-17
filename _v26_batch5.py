# -*- coding: utf-8 -*-
"""v2.6 第五批：全站清理剩余说明性文字（副标题/tooltip/括号内说明/placeholder文案）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:100])
    s = s.replace(old, new, cnt)

# 1. 质量特性维护页副标题
rep('<PageHead title="质量特性维护" sub="质量特性基础数据（SC/CC/普通），MSA 计划创建时引用"/>',
    '<PageHead title="质量特性维护"/>', 1, 'char-sub')
# 2. 抽样方法维护页副标题
rep('<PageHead title="抽样方法维护" sub="七大检测分析方法代码表 + 取样规则（默认值可调，计划创建时引用）"/>',
    '<PageHead title="抽样方法维护"/>', 1, 'sampling-sub')
# 3. 器具台账 样机 tooltip
rep('<Form.Item name="prototype" label="样机" tooltip="标记为样机的器具：周期性 MSA 校验时系统自动筛选带样机标记的器具生成计划，无需每次手动挑选">',
    '<Form.Item name="prototype" label="样机">', 1, 'proto-tooltip')
# 4. 器具台账详情 样机 Tag
rep("{key:'样机', label:'样机', children:r.prototype==='是'?<Tag color=\"orange\">样机（周期校验自动筛选）</Tag>:'否'},",
    "{key:'样机', label:'样机', children:r.prototype==='是'?<Tag color=\"orange\">样机</Tag>:'否'},", 1, 'proto-tag')
# 5. 检验标准 modal groupIds label/tooltip
rep('<Col span={24}><Form.Item name="groupIds" label="绑定器具组（会议口径：为周期自动选样准备）" tooltip="周期 MSA 校验时，系统按标准绑定的器具组自动筛选样机器具生成计划"><Select mode="multiple" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+\' \'+g.name}))}/></Form.Item></Col>',
    '<Col span={24}><Form.Item name="groupIds" label="绑定器具组"><Select mode="multiple" allowClear options={(d.instGroups||[]).map(g=>({value:g.id,label:g.id+\' \'+g.name}))}/></Form.Item></Col>', 1, 'std-group')
# 6. 校准登记 Modal 标题
rep('<Modal title="登记校准记录（自动更新台账下次校准日期与状态）" open width={640}',
    '<Modal title="登记校准记录" open width={640}', 1, 'calib-modal')
# 7. 修订检验标准标题
rep('title={revise?\'修订检验标准（自动升版）\':\'新增检验标准\'}',
    'title={revise?\'修订检验标准\':\'新增检验标准\'}', 1, 'std-modal-title')
# 8. 计划创建弹窗 质量特性 placeholder
rep('placeholder="选质量特性（自动带出测量对象）"',
    'placeholder="选质量特性"', 1, 'char-ph')
# 9. 计划创建弹窗 测量对象 label
rep('label="测量对象（含公差，GRR 自动解析公差）"',
    'label="测量对象"', 1, 'object-label')
# 10. 适用器具 grp-label
rep('<div className="grp-label">适用器具（按工序自动匹配，只读）</div>',
    '<div className="grp-label">适用器具</div>', 1, 'app-inst')
# 11. 覆盖范围说明 placeholder
rep('<Input placeholder="覆盖过程变差（低/中/高）"/>',
    '<Input placeholder=""/>', 1, 'cover-ph')

open(P, 'w', encoding='utf-8').write(s)
print('batch5 OK 长度', len(s))
