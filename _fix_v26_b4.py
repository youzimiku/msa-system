# -*- coding: utf-8 -*-
"""修 CalBadge '-' + 扫描残留显示 '-'"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# CalBadge 无校准日期
n = s.count("if(!nextCal) return <span className=\"tiny\">-</span>;")
s = s.replace("if(!nextCal) return <span className=\"tiny\">-</span>;", "if(!nextCal) return <span className=\"tiny\">暂无</span>;")
print('CalBadge: x%d' % n)

# 扫描剩余显示 '-'：'>-<' 与 '>'-'<' 与 'tiny">-' 等
pat = re.compile(r">'-'<|>-'<|tiny\">-\s*<|return '-';|:'-'")
for m in pat.finditer(s):
    a = max(0, m.start()-55)
    print('@%d :: %s' % (m.start(), s[a:m.start()+40].replace('\n', ' ')[-100:]))

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
