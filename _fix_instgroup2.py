# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(old, new, desc, expect=1):
    global src
    n = src.count(old)
    ok = (n == expect)
    print(f'{desc}: 出现 {n} 次 (期望 {expect})', '-> 替换' if ok else '!!跳过')
    if ok:
        src = src.replace(old, new)

# 1) 列表去掉 组成员 列（含换行）
rep(
"    {title:'组成员', width:170, render:(_,r)=>memberText(r)},\n",
"",
'1 列表去组成员列')

# 2) 弹窗去掉 成员器具（多选）下拉（inst 分支）
rep(
"""        : <Row gutter={12}>
            <Col span={24}><Form.Item name="memberIds" label="成员器具（多选）"><Select mode="multiple" allowClear optionFilterProp="label"
              options={d.instruments.map(i=>({value:i.id,label:i.id+' '+i.name}))}/></Form.Item></Col>
          </Row>}""",
"        : null}",
'2 弹窗去成员器具下拉')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
