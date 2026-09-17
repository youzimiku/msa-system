# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
# 找 '已完成定型并建立台账记录' 上下文
for m in re.finditer('已完成定型并建立台账记录', s):
    print('@', m.start())
    print(s[m.start()-500:m.start()+300].replace('\n', '⏎'))
    print('-----')
