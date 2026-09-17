# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. 本地快照
snap = os.path.join(BASE, f'index_备份_{ts}_删操作方法列前.html')
shutil.copy2(CUR, snap)

# 2. 删除列表列
src = io.open(CUR, encoding='utf-8').read()
old = "    {title:'操作方法', width:170, render:(_,r)=><Input size=\"small\" value={r.opMethod||'《测量系统分析操作指导书》'} onChange={e=>setF(r,'opMethod',e.target.value)}/>},\n"
cnt = src.count(old)
assert cnt == 1, f'期望 1 处，实际 {cnt}'
src = src.replace(old, '')
io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
print('已删除 MSA计划列表 操作方法列')

# 3. 归档
folder = os.path.join(BASE, 'backups', ts + '_删操作方法列')
os.makedirs(folder, exist_ok=True)
shutil.copy2(CUR, os.path.join(folder, 'index.html'))
md = """# 调整内容：MSA计划列表去掉操作方法列（2026-09-16）

## 改动清单
- MSA计划 · 计划列表：删除列"操作方法"（opMethod，原为行内输入框，默认《测量系统分析操作指导书》）
- 未改动：老数据补全逻辑（opMethod 默认值）、详情抽屉"操作方法"、创建/编辑弹窗"操作方法"输入框

## 说明
- 仅删除列表展示列，不影响数据字段与其余入口。
"""
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
a = io.open(snap, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
io.open(cl, 'a', encoding='utf-8').write(f"- {ts} MSA计划列表去掉操作方法列（详情/弹窗保留）\n")
print('归档完成:', folder)
