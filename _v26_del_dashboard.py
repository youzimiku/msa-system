# -*- coding: utf-8 -*-
"""删除仪表盘功能：菜单/标题/初始页/分发/铃铛/组件整体移除"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:100])
    s = s.replace(old, new, cnt)

# 1. 菜单移除仪表盘
rep("  {key:'dashboard', icon:'◈', label:'仪表盘', group:null},\n", "", 1, 'menu')
# 2. PAGE_TITLE 移除
rep("'dashboard':'MSA 测量系统分析 · 总览',", "", 1, 'title')
# 3. 初始页改计量器具台账
rep("const [page,setPage]=useState('dashboard');", "const [page,setPage]=useState('ledger');", 1, 'init')
# 4. 分发移除 dashboard
rep("    if(page==='dashboard') return <Dashboard/>;\n", "", 1, 'dispatch')
# 5. fallback 改 LedgerPage
rep("    return <Dashboard/>;\n  };", "    return <LedgerPage/>;\n  };", 1, 'fallback')
# 6. 铃铛跳转改校准管理
rep("onClick={()=>setPage('dashboard')}", "onClick={()=>setPage('calib')}", 1, 'bell')
# 7. 删除整个 Dashboard 组件（含注释，保留计量器具台账注释）
i = s.find('/* ================= 仪表盘 ================= */')
j = s.find('/* ================= 计量器具台账 ================= */')
assert i > 0 and j > i, '组件定位失败 %d %d' % (i, j)
s = s[:i] + s[j:]
# 8. 顶部注释去仪表盘
rep(" *  应用框架 / 通用组件 / 仪表盘 / 计量器具台账", " *  应用框架 / 通用组件 / 计量器具台账", 1, 'hdr-comment')

open(P, 'w', encoding='utf-8').write(s)
print('del-dashboard OK 长度', len(s))
