# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
folder = os.path.join(BASE, 'backups', '20260916_180304_零件号联动下拉')

# 找到快照（修改前）
snaps = [f for f in os.listdir(BASE) if f.startswith('index_备份_') and '零件号联动下拉前' in f]
snap = os.path.join(BASE, sorted(snaps)[-1]) if snaps else None

# 更新归档 index.html
shutil.copy2(CUR, os.path.join(folder, 'index.html'))

# 重新生成 diff
if snap:
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    print('diff 已更新, 共', len(diff), '行')

# 更新调整内容.md 补充修复说明
md = io.open(os.path.join(folder, '调整内容.md'), encoding='utf-8').read()
md += """
## 修复记录
- 修复命名冲突：applyFieldDefaults 内新增映射改名 PARTNAME_MAP（原文件已有 PARTMAP 检验标准映射）
- 修复组件缺失：antd 解构列表补充 Popover（PartSelect 下拉使用）
"""
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
print('归档已同步')
