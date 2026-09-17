# -*- coding: utf-8 -*-
import io
path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
c = io.open(path, encoding='utf-8').read()

status_col = "{title:'状态', dataIndex:'status', width:90, render:s=><StatusTag s={s}/>},"
type_col = "{title:'分析类型', width:84, render:(_,r)=><Tag color=\"blue\">{r.type}</Tag>},"

# 1) 从原位置删除状态列（原位置：版本行之后、录入人行之前）
old_block = "{title:'版本', dataIndex:'version', width:70, render:v=><Tag color=\"purple\">{v}</Tag>},\n    " + status_col + "\n    {title:'录入人', dataIndex:'editor', width:90, ellipsis:true},"
new_block = "{title:'版本', dataIndex:'version', width:70, render:v=><Tag color=\"purple\">{v}</Tag>},\n    {title:'录入人', dataIndex:'editor', width:90, ellipsis:true},"
assert c.count(old_block) == 1, ('remove status', c.count(old_block))
c = c.replace(old_block, new_block)

# 2) 在分析类型列之后插入状态列
old2 = type_col + "\n    {title:'关联被测参数',"
new2 = type_col + "\n    " + status_col + "\n    {title:'关联被测参数',"
assert c.count(old2) == 1, ('insert status', c.count(old2))
c = c.replace(old2, new2)

io.open(path, 'w', encoding='utf-8').write(c)
print('STATUS COL MOVED OK')
