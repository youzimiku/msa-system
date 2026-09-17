# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(old, new, desc, expect=1):
    n = src.count(old)
    print(f'{desc}: 出现 {n} 次', '-> 替换' if n else '!!未找到')
    return src.replace(old, new)

# 1) METHOD_NAME 重构 + STRIP_PAREN 新增
old1 = "const METHOD_NAME=(code)=>{ const d=Store.get(); const m=(d.anMethods||[]).find(x=>String(x.code).toLowerCase()===String(code||'').toLowerCase()); const n=m?m.name:code; return String(n).replace(/（[^）]*）/g,'').replace(/\\([^)]*\\)/g,''); };"
new1 = ("const STRIP_PAREN=(s)=>String(s||'').replace(/（[^）]*）/g,'').replace(/\\([^)]*\\)/g,'');\n"
        "const METHOD_NAME=(code)=>{ const d=Store.get(); const m=(d.anMethods||[]).find(x=>String(x.code).toLowerCase()===String(code||'').toLowerCase()); return STRIP_PAREN(m?m.name:code); };")
src = rep(old1, new1, '1 METHOD_NAME 重构 + STRIP_PAREN')

# 2) 抽样方法页 方法名称列 去括弧
old2 = "{title:'方法名称', dataIndex:'name', width:210},"
new2 = "{title:'方法名称', dataIndex:'name', width:210, render:v=><span>{STRIP_PAREN(v)}</span>},"
src = rep(old2, new2, '2 方法名称列去括弧')

# 3) 判断规则列表 所属方法列 显示名称
old3 = "{title:'所属方法', dataIndex:'method', width:110, render:v=><span className=\"mono\">{v}</span>},"
new3 = "{title:'所属方法', dataIndex:'method', width:120, render:v=><span>{METHOD_NAME(v)}</span>},"
src = rep(old3, new3, '3 所属方法列显示名称')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
