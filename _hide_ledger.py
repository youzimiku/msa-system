# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
old1 = "  {key:'ledger', icon:'⚙', label:'计量器具台账', group:'基础数据'},\n"
print('old1 found:', old1 in src)
old2 = "const [page,setPage]=useState('ledger');"
print('old2 found:', old2 in src)
new1 = "  /* 计量器具台账已按需求隐藏（保留页面组件与内部跳转，仅移除菜单入口） */\n"
new2 = "const [page,setPage]=useState('instgroup');"
if old1 in src:
    src = src.replace(old1, new1, 1)
if old2 in src:
    src = src.replace(old2, new2, 1)
open(p, 'w', encoding='utf-8').write(src)
print('done, sizes:', len(src))
