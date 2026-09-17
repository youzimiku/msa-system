# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
m = re.search(r'<script type="text/babel"[^>]*>(.*?)</script>', src, re.S)
print('script len', len(m.group(1)))
open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_compiled.js', 'w', encoding='utf-8').write(m.group(1))
print('saved')
