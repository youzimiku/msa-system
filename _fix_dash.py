# -*- coding: utf-8 -*-
import io
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
old = '<span className="tiny">-</span>'
print('count:', s.count(old))
s = s.replace(old, '<span className="tiny">未绑定</span>')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('done')
