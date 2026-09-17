# -*- coding: utf-8 -*-
"""补充：其他状态类 Tag 宽度统一（计划状态 planStatusView、校准状态、样本状态）"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

TAGW = "{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}"

# 1) planStatusView 生成的 Tag（计划状态 待开始/进行中/已完成）
m = re.findall(r"return <Tag color=\{v\.color\}", s)
print('planStatusView Tag count:', len(m))
s = s.replace("return <Tag color={v.color} className=\"spec-tag\"", "return <Tag color={v.color} className=\"spec-tag\" style={" + TAGW + "}")
s = s.replace("return <Tag color={v.color}>", "return <Tag color={v.color} style={" + TAGW + "}>")

# 2) 校准状态 Tag（正常/临期/超期，两处：台账与创建弹窗）
m = re.findall(r"return <Tag>正常</Tag>; const dd=daysBetween\(TODAY,r\.nextCal\)", s)
print('calib status Tag pattern A:', len(m))
s = s.replace("return <Tag>正常</Tag>; const dd=daysBetween(TODAY,r.nextCal); ret", "return <Tag style={" + TAGW + "}>正常</Tag>; const dd=daysBetween(TODAY,r.nextCal); ret")
s = s.replace("return <Tag>正常</Tag>; const dd=daysBetween(TODAY,i.nextCal); ret", "return <Tag style={" + TAGW + "}>正常</Tag>; const dd=daysBetween(TODAY,i.nextCal); ret")

# 3) 样本状态 Tag（已测量/待测量、已测/未测）
s = s.replace("render:s=><Tag color={s==='已测量'?'green':s==='待测量'?'orange':'default'}", "render:s=><Tag color={s==='已测量'?'green':s==='待测量'?'orange':'default'} style={" + TAGW + "}")
s = s.replace("render:s=><Tag color={s==='已测'?'green':'orange'}", "render:s=><Tag color={s==='已测'?'green':'orange'} style={" + TAGW + "}")

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s) - len(orig))
