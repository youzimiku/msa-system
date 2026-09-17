# -*- coding: utf-8 -*-
"""统一替换剩余 <span className="tiny">-</span>"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

n1 = s.count(' : <span className="tiny">-</span>')
s = s.replace(' : <span className="tiny">-</span>', ' : <span className="tiny">暂无</span>')
n2 = s.count('return <span className="tiny">-</span>')
s = s.replace('return <span className="tiny">-</span>', 'return <span className="tiny">暂无</span>')
n3 = s.count('> <span className="tiny">-</span>')
s = s.replace('> <span className="tiny">-</span>', '> <span className="tiny">暂无</span>')
n4 = s.count('<span className="tiny">-</span>')
print('剩余 tiny -:', n4)
import re
for m in re.finditer(r'<span className="tiny">-</span>', s):
    a = max(0, m.start()-60)
    print('@%d :: %s' % (m.start(), s[a:m.start()+30].replace('\n',' ')[-100:]))
io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
