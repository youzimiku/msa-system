# -*- coding: utf-8 -*-
"""补修 syncPlan 汇总（filter 与 :'-'）"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

old = "const cons = recs.map(r=>r.conclusion).filter(c=>c&&c!=='-');\n  p.result = recs.length>1 ? (cons.length? cons.join('；') : '-') : (recs[0].conclusion||'暂无');"
new = "const cons = recs.map(r=>r.conclusion).filter(c=>c&&c!=='-'&&c!=='待采集');\n  p.result = recs.length>1 ? (cons.length? cons.join('；') : '待采集') : (recs[0].conclusion&&recs[0].conclusion!=='-'?recs[0].conclusion:'待采集');"
n = s.count(old)
assert n == 1, n
s = s.replace(old, new)

# 检查剩余可见 '-' 占位（渲染层常见模式）
import re
left = re.findall(r"return '-';|\? '-'|:'-'|:'-'|'-'</span>|>'-'<", s)
print('剩余疑似占位:', left[:20])

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
