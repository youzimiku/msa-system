# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
# 找 instrument seed 定义
i = s.find("id:'JJQ-2024-001'")
print('seed hit at', i)
print(s[i-200:i+800])
