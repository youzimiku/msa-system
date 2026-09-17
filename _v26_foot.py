# -*- coding: utf-8 -*-
"""删除侧边栏底部'依据 AIAG MSA-4 / IATF 16949 ISO 10012 设计'"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()
OLD = '<div className="sider-foot">依据 AIAG MSA-4 / IATF 16949<br/>ISO 10012 设计</div>\n'
assert s.count(OLD) == 1, '定位失败 %d' % s.count(OLD)
s = s.replace(OLD, '', 1)
open(P, 'w', encoding='utf-8').write(s)
print('OK 长度', len(s))
