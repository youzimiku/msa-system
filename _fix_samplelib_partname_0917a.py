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

# 1) 样本库过滤加入零件名称
rep("""  const rows=(d.sampleLib||[]).filter(r=>(!q.kw||(r.id+r.name+(r.partNo||'')+(r.charDim||'')).toLowerCase().includes(q.kw.toLowerCase())))""",
"""  const rows=(d.sampleLib||[]).filter(r=>(!q.kw||(r.id+r.name+(r.partNo||'')+(r.partName||'')+(r.charDim||'')).toLowerCase().includes(q.kw.toLowerCase())))""",
"样本库关键词加零件名称", cnt=1)

# 2) placeholder 加入零件名称
rep("placeholder=\"样本编号/样本名称/零件号/被测项目\"", "placeholder=\"样本编号/样本名称/零件号/零件名称/被测项目\"", "样本库placeholder加零件名称", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('完成')
