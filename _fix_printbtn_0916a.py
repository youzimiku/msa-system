# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_补打按钮移位前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. 操作列：移除补打，去掉 OpBtns 折叠（保存/日志/删除 平铺）
EDITS.append((
"""    {title:'操作', width:180, fixed:'left', render:(_,r)=><OpBtns items={[
      {label:'保存', onClick:()=>saveRow(r)},
      {label:'日志', onClick:()=>setLogOpen(r.id)},
      {label:'删除', danger:true, onClick:()=>delRow(r)},
      {label:'补打', onClick:()=>{}}
    ]}/>},""",
"""    {title:'操作', width:180, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveRow(r)}>保存</Button>
      <Button size="small" type="link" onClick={()=>setLogOpen(r.id)}>日志</Button>
      <Button size="small" type="link" danger onClick={()=>delRow(r)}>删除</Button>
    </Space>},""", 1))

# 2. 按钮板：新增样本按钮后加补打按钮
EDITS.append((
"""        <Button type="primary" onClick={addRow}>新增样本</Button>
        <ImportBtn title="样本库管理"/>""",
"""        <Button type="primary" onClick={addRow}>新增样本</Button>
        <Button onClick={()=>{}}>补打</Button>
        <ImportBtn title="样本库管理"/>""", 1))

fail = False
for i, (old, new, exp) in enumerate(EDITS):
    cnt = src.count(old)
    if cnt != exp:
        print(f"[FAIL] #{i} 期望 {exp} 实际 {cnt} | old[:70]={old[:70]!r}")
        fail = True
    else:
        src = src.replace(old, new)
        print(f"[OK] #{i} 替换 {cnt} 处")

if fail:
    print('存在未匹配项，未写回')
else:
    io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
    folder = os.path.join(BASE, 'backups', ts + '_补打按钮移位')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：样本库补打按钮移位（2026-09-16）

## 改动清单
1. 样本库管理页面 · 操作列：
   - 移除「补打」按钮
   - 去掉更多折叠，保存/日志/删除 三个按钮平铺显示
2. 样本库管理页面 · 按钮板：
   - 「新增样本」按钮后新增「补打」按钮（无点击事件）
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 样本库补打按钮移到按钮板新增样本后，操作列去折叠平铺\n")
    print('已写回 + 归档:', folder)
