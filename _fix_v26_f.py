# -*- coding: utf-8 -*-
"""文案微调：转定型后跳录入数据页"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

n1 = s.count("toast.ok('已定型为 '+(ANAL_SHORT[v.type]||v.type)+'（'+v.standard+'），请在对应台账内录入数据');")
s = s.replace("toast.ok('已定型为 '+(ANAL_SHORT[v.type]||v.type)+'（'+v.standard+'），请在对应台账内录入数据');",
              "toast.ok('已定型为 '+(ANAL_SHORT[v.type]||v.type)+'（'+v.standard+'），已跳转对应「录入数据」页');")
print('toast x%d' % n1)

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
