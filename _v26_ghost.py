# -*- coding: utf-8 -*-
"""修复 L2106 ghost 按钮 + 全局扫 style 含 border 的 Button"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

OLD = """{recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size="small" type="primary" ghost disabled={!canDo(me.role,'edit')} onClick={()=>recJump(x)}>录入数据 {x.id}</Button>)}"""
NEW = """{recs.filter(x=>x.reviewStatus==='待采集').map(x=><Button key={x.id} size="small" type="link" disabled={!canDo(me.role,'edit')} onClick={()=>recJump(x)}>录入数据 {x.id}</Button>)}"""
assert s.count(OLD) == 1, 'ghost 定位失败 %d' % s.count(OLD)
s = s.replace(OLD, NEW, 1)
open(P, 'w', encoding='utf-8').write(s)
print('ghost fix OK')

# 检查所有 Button 内 style 含 border 的
for m in re.finditer(r'<Button[^>]*style=\{[^}]*border[^}]*\}[^>]*>', s):
    line = s.count('\n', 0, m.start()) + 1
    print('BORDER-BTN', line, m.group(0)[:130])
