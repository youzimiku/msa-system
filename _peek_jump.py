# -*- coding: utf-8 -*-
import io
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for key in ["'entry_'", "entry_grr", "recJump", "openAnl", "entry_linear"]:
    i = s.find(key)
    print('==', key, '@', i)
    if i >= 0:
        print(s[max(0,i-260):i+380].replace('\n', '⏎'))
    print()
