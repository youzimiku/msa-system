# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

old = "      {pickedMap[r.id]&&<Tooltip title={'样本：'+((pickedMap[r.id].samples||[]).map(s=>s.id).join('、')||'—')+'；人员：'+((pickedMap[r.id].ops||[]).join('、')||'—')}><Tag color=\"blue\">{(pickedMap[r.id].samples||[]).length}样本/{(pickedMap[r.id].ops||[]).length}人</Tag></Tooltip>}\n"
assert t.count(old) == 1, '锚点不唯一或不存在'
t = t.replace(old, '')

io.open(P, 'w', encoding='utf-8').write(t)
print('已移除操作列已选回显标签')
