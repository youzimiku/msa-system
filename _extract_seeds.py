# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 提取各台账数组块
def block(start_marker, end_marker):
    i = src.find(start_marker)
    j = src.find(end_marker, i)
    return src[i:j]

blocks = {
    'grr': block('const grr = [', '\n  ];'),
    'kappa': block('const kappa = [', '\n  ];'),
    'linear': block('const linear = [', '\n  ];'),
    'stability': block('const stability = [', '\n  ];'),
    'cgcgk': block('const cgcgk = [', '\n  ];'),
}
for k, v in blocks.items():
    print('=====', k, '=====')
    # 打印每条记录的 id 行及后续字段（简单打印前1200字符）
    print(v[:1600])
    print('...len', len(v))
