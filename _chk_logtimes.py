# -*- coding: utf-8 -*-
import io
c = io.open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
for v in ["time:'2026-08-30 14:22'", "time:'2026-09-01 09:15'", "time:'2026-09-05 16:40'",
          "time:'2026-08-30", "2026-08-30 14:22", "2026-09-01 09:15", "2026-09-05 16:40"]:
    n = c.count(v)
    print(n, repr(v))
