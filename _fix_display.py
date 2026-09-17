# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

def rep(src, old, new, cnt_desc):
    n = src.count(old)
    print(f'{cnt_desc}: 出现 {n} 次', '-> 替换' if n else '!!未找到')
    return src.replace(old, new)

# ---- A. 卡帕人员组 -> kappa人员组（全部出现处统一替换） ----
src = rep(src, '卡帕人员组', 'kappa人员组', 'A 卡帕人员组->kappa人员组')

# ---- B. 全局 METHOD_NAME helper（插入到 TIPS 结束之后） ----
anchor = 'function verdictColor('
helper = ('/* 分析方法 code → 名称（大小写不敏感，被测参数维护页检验方法展示用） */\n'
          'const METHOD_NAME=(code)=>{ const d=Store.get(); const m=(d.anMethods||[]).find(x=>String(x.code).toLowerCase()===String(code||\'\').toLowerCase()); return m?m.name:code; };\n')
if 'const METHOD_NAME=' not in src:
    src = rep(src, anchor, helper + anchor, 'B 插入 METHOD_NAME helper')
else:
    print('B METHOD_NAME 已存在，跳过')

# ---- B1. 列表列 methodView ----
src = rep(src,
    'ms.map(m=><Tag key={m.method} color="blue" style={{marginRight:0}}>{m.method}</Tag>)',
    'ms.map(m=><Tag key={m.method} color="blue" style={{marginRight:0}}>{METHOD_NAME(m.method)}</Tag>)',
    'B1 列表检验方法列')

# ---- B2. 详情抽屉表格 ----
src = rep(src,
    "{title:'方法', dataIndex:'method', width:110, render:v=><Tag color=\"blue\">{v}</Tag>}",
    "{title:'方法', dataIndex:'method', width:150, render:v=><Tag color=\"blue\">{METHOD_NAME(v)}</Tag>}",
    'B2 详情抽屉检验方法表格')

# ---- B3. 编辑弹窗 Checkbox label ----
src = rep(src,
    "['GRR','KAPPA','linear','stability','cgcgk'].map(m=>({value:m,label:m}))",
    "['GRR','KAPPA','linear','stability','cgcgk'].map(m=>({value:m,label:METHOD_NAME(m)}))",
    'B3 编辑弹窗检验方法勾选')

# ---- B4. 编辑弹窗 Tag ----
src = rep(src,
    '<Tag color="blue" style={{width:90,textAlign:\'center\',marginRight:8}}>{m}</Tag>',
    '<Tag color="blue" style={{width:150,textAlign:\'center\',marginRight:8}}>{METHOD_NAME(m)}</Tag>',
    'B4 编辑弹窗方法Tag')

open(p, 'w', encoding='utf-8').write(src)
print('写入完成, 大小:', len(src))
