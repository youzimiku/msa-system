# -*- coding: utf-8 -*-
"""Step2b：计划状态 Tag 加 Tooltip（列表 2 处）"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

old = "return <Tag color={v.color} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{v.text}</Tag>"
new = "return <Tooltip title={TIPS.plan[v.text]||v.text}><Tag color={v.color} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{v.text}</Tag></Tooltip>"
n = s.count(old)
print('计划状态 Tag: x%d' % n)
s = s.replace(old, new)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
