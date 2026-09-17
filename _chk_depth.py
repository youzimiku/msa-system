# -*- coding: utf-8 -*-
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
start = s.find('<script type="text/babel">')
end = s.find('</script>', start)
code = s[start + len('<script type="text/babel">'):end]
lines = code.split('\n')
depth = 0
for i, ln in enumerate(lines, 1):
    for ch in ln:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                print('UNBALANCED at line', i, ':', ln[:100])
                break
print('final depth:', depth)
print('total lines:', len(lines))
