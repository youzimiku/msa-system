# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_台账编号统一前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()

old = """    {title:CFG.idPref+'编号', dataIndex:'id', width:115, render:(v,r)=><span className="row-link mono" onClick={()=>goResult(r)}>{v}</span>},"""
new = """    {title:'台账编号', dataIndex:'id', width:115, render:(v,r)=><span className="row-link mono" onClick={()=>goResult(r)}>{v}</span>},"""

cnt = src.count(old)
if cnt != 1:
    print(f'[FAIL] 期望 1 处，实际 {cnt}')
else:
    src = src.replace(old, new)
    io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
    folder = os.path.join(BASE, 'backups', ts + '_台账编号统一')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：五个台账页面编号列改名（2026-09-16）

## 改动清单
1. 台账层级下的五个台账页面（GRR/KAPPA/线性偏移/稳定性/CgCgk，共用 EntryPage 组件）：
   - 操作列后面的编号列，列标题由「GRR 编号 / KAPPA 编号 / LIN 编号 / STB 编号 / CG 编号」统一改为「台账编号」
   - 数据内容不变（仍显示原台账记录编号）
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 五个台账页面编号列统一改为「台账编号」\n")
    print('已写回 + 归档:', folder)
