# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

label = '<span style={{marginRight:4,color:\'#666666\',fontSize:14,whiteSpace:\'nowrap\'}}>状态</span>'
pat = r'(<Radio\.Group size="small" value=)'
n = len(re.findall(pat, src))
print('Radio.Group 数量:', n)
# 只在前面没有 状态 标签的 Radio.Group 前插入
src = re.sub(pat, label + r'\1', src)
# 防止重复插入（如果某处已带标签）
src = src.replace(label + label, label)
open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
