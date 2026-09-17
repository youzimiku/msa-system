# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for arr in ['grr', 'kappa', 'linear', 'stability', 'cgcgk', 'resolution']:
    i = s.find('const ' + arr + ' = [')
    k = s.find('];', i)
    seg = s[i:k]
    ids = re.findall(r"id:'([A-Z]+-[\w-]+)'", seg)
    print(arr, '顺序:', ids)
    print('  尾150:', s[k-130:k+5].replace(chr(10), ' '))
    print()
