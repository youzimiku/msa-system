# -*- coding: utf-8 -*-
"""multi4: seed 补一计划多方法演示计划"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

# 查看 seed plans 结尾（MSAP-2026-008 所在段后 1000 字符）
i = s.find('MSAP-2026-008')
print(s[i-260:i+1500])
