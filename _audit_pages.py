# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
lines = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').readlines()
print('总行数:', len(lines))

# 1) 菜单项
print('===== 菜单 =====')
in_menu = False
for i, l in enumerate(lines):
    if 'const MENU' in l: in_menu = True
    if in_menu and '];' in l: in_menu = False; break
    if in_menu and '{key:' in l:
        print(i+1, '|', l.strip()[:150])

# 2) 每个 Page 的 查询条件 Panel 内容
print()
print('===== 查询条件 Panel =====')
pgs = [(1394,'LedgerPage'),(1729,'InstGroupPage'),(1913,'CalibPage'),(1994,'PlanPage'),(2526,'StandardPage'),(2689,'CharPage'),(2901,'SamplingPage'),(3152,'SampleLibPage'),(3276,'SamplePage'),(3916,'GrrPage'),(4090,'KappaPage'),(4342,'DesignPage'),(4418,'LogPage')]
for start, name in pgs:
    # 找该页面的 Panel title="查询条件"
    for i in range(start, start+260 if start+260 < len(lines) else len(lines)):
        if '查询条件' in lines[i] and 'Panel' in lines[i]:
            print(f'-- {name} (L{i+1})')
            # 打印下面直到 Panel title="操作" 或 列表 Panel
            for j in range(i, min(i+30, len(lines))):
                s = lines[j].rstrip()
                if j > i and ('Panel title' in s or 'Panel' in s and 'title' in s):
                    print('    ...', s.strip()[:80]); break
                if j > i and s.strip():
                    print('    ', s.strip()[:160])
            break
