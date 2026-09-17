# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()
n = t.count('placeholder="支持：')
assert n == 13, '期望 13 处，实际 %d' % n
t = t.replace('placeholder="支持：', 'placeholder="')
io.open(P, 'w', encoding='utf-8').write(t)
print('完成，共去掉 %d 处' % n)
