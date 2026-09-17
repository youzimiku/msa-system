# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_分辨力去单位前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. 新增 resClean 清洗函数（放在 applyFieldDefaults 定义之前）
EDITS.append((
"""/* 企业字段口径补全函数：对旧数据 / 新数据统一补齐新增字段默认值（本地已存数据加载时同样调用） */
function applyFieldDefaults(d){""",
"""/* 分辨力去单位：'0.01mm'→'0.01'、'0.02MPa'→'0.02'、'0.1N·m'→'0.1'、'0.1℃'→'0.1'；非"数字+单位"形态（如 计数型/暂无）原样保留 */
function resClean(v){
  const s=String(v==null?'':v).trim();
  const m=s.match(/^([0-9]+(?:\\.[0-9]+)?)\\s*[a-zA-Z°℃Ω%·]+$/);
  return m?m[1]:s;
}

/* 企业字段口径补全函数：对旧数据 / 新数据统一补齐新增字段默认值（本地已存数据加载时同样调用） */
function applyFieldDefaults(d){""", 1))

# 2. instruments 兜底处清洗 res（覆盖 seed + localStorage 旧缓存）
EDITS.append((
"""      nextReviewDate:i.nextReviewDate||(i.nextCal?i.nextCal:'暂无'), calAdvanceDays:i.calAdvanceDays||(i.calAdvance||15),""",
"""      nextReviewDate:i.nextReviewDate||(i.nextCal?i.nextCal:'暂无'), calAdvanceDays:i.calAdvanceDays||(i.calAdvance||15),
      res:i.res?resClean(i.res):i.res,""", 1))

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
    folder = os.path.join(BASE, 'backups', ts + '_分辨力去单位')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：所有分辨力字段去单位（2026-09-16）

## 改动清单
1. 新增 resClean 清洗函数：
   - '0.01mm'→'0.01'、'0.02MPa'→'0.02'、'0.1N·m'→'0.1'、'0.1℃'→'0.1'
   - 非"数字+单位"形态（如 计数型 / 暂无）原样保留
2. 器具数据兜底处统一清洗 instruments.res：
   - 覆盖种子数据与浏览器本地缓存旧数据，所有分辨力显示点（器具台账/详情/MSA计划列表/台账记录/分析结果等）自动无单位
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 所有分辨力字段值去单位（新增resClean清洗，覆盖缓存旧数据）\n")
    print('已写回 + 归档:', folder)
