# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_样本库补打按钮页面说明前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. 样本库操作列：改造为 OpBtns（保存/日志/删除在外，补打进更多），宽度 160 -> 180
EDITS.append((
"""    {title:'操作', width:160, fixed:'left', render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveRow(r)}>保存</Button>
      <Button size="small" type="link" onClick={()=>setLogOpen(r.id)}>日志</Button>
      <Button size="small" type="link" danger onClick={()=>delRow(r)}>删除</Button>
    </Space>},""",
"""    {title:'操作', width:180, fixed:'left', render:(_,r)=><OpBtns items={[
      {label:'保存', onClick:()=>saveRow(r)},
      {label:'日志', onClick:()=>setLogOpen(r.id)},
      {label:'删除', danger:true, onClick:()=>delRow(r)},
      {label:'补打', onClick:()=>{}}
    ]}/>},""", 1))

# 2. 页面说明：基础数据四页排除列表移除 samplelib
EDITS.append((
"  if(page==='instgroup'||page==='char'||page==='sampling'||page==='samplelib') return null; /* 基础数据四页不显示说明 */",
"  if(page==='instgroup'||page==='char'||page==='sampling') return null; /* 基础数据（样本库除外）不显示说明 */", 1))

# 3. 样本库页面说明内容
EDITS.append((
"  samplelib:{label:'样本库管理', text:'管理标准件 / 生产件样本及其真值（参考值），供各台账选件分析使用。', ops:'新增/修改为列表行内编辑；「日志查询」在样本行上。'},",
"  samplelib:{label:'样本库管理', text:'样本新增时，触发打印事件，打印样本编号二维码，支持补打。', ops:''},", 1))

fail = False
for i, (old, new, exp) in enumerate(EDITS):
    cnt = src.count(old)
    if cnt != exp:
        print(f"[FAIL] #{i} 期望 {exp} 实际 {cnt} | old[:80]={old[:80]!r}")
        fail = True
    else:
        src = src.replace(old, new)
        print(f"[OK] #{i} 替换 {cnt} 处")

if fail:
    print('存在未匹配项，未写回')
else:
    io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
    # 归档
    folder = os.path.join(BASE, 'backups', ts + '_样本库补打按钮页面说明')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：样本库补打按钮 + 页面说明（2026-09-16）

## 改动清单
1. 样本库管理 · 样本列表操作列：
   - 新增"补打"按钮（无点击事件）
   - 操作列改造为 OpBtns 折叠（最多显示 3 个：保存 / 日志 / 删除，补打收进「更多」悬停菜单）
   - 操作列宽度 160 → 180，避免拥挤
2. 样本库管理页面顶部新增页面说明（可折叠，浅黄色背景），内容：
   "样本新增时，触发打印事件，打印样本编号二维码，支持补打。"
   - 基础数据四页排除列表移除 samplelib（仅本页恢复说明，其余三页仍不显示）
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 样本库操作列新增补打按钮（收进更多）；页面顶部新增打印二维码说明\n")
    print('已写回 + 归档:', folder)
