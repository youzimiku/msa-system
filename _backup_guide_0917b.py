# -*- coding: utf-8 -*-
import io, os, shutil, subprocess, sys, datetime, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
TITLE = '页面说明按飞书修改回写'
now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir = os.path.join(BASE, 'backups', '%s_%s' % (now, TITLE))
os.makedirs(backup_dir, exist_ok=True)
src = os.path.join(BASE, 'index.html')
shutil.copy2(src, os.path.join(backup_dir, 'index.html'))

# diff 与最近一次备份
prev = None
dirs = sorted(glob.glob(os.path.join(BASE, 'backups', '*')), reverse=True)
for d in dirs:
    if os.path.isdir(d) and os.path.abspath(d) != os.path.abspath(backup_dir):
        if os.path.exists(os.path.join(d, 'index.html')):
            prev = os.path.join(d, 'index.html')
            break
diff_text = ''
if prev:
    r = subprocess.run(['git', 'diff', '--no-index', '--', prev, src], cwd=BASE,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    diff_text = r.stdout
io.open(os.path.join(backup_dir, '调整内容.diff.txt'), 'w', encoding='utf-8').write(diff_text or '(无差异)')

md = """# 调整内容：%s

- 时间：%s
- 触发：用户修改飞书在线表格「页面说明_20260917」后，按表格内容回写 index.html 的 PAGE_GUIDE 对象

## 本次改动
1. 页面说明文字按飞书表格修改全量回写（PAGE_GUIDE 对象）：
   - 器具组维护：页面说明精简为「维护测量器具组与人员组（岗位）。」；关键逻辑去掉行内编辑描述，人员组改为「（岗位）」、仅支持 KAPPA
   - 被测参数维护：删除「关键操作」段落
   - 抽样方法维护：删除「页面说明」段落；关键逻辑中判定结论改为「固定为可接受 / 有条件接受 / 不可接受」
   - 样本库管理：关键逻辑删去「判定状态下拉 / 补打」描述，仅保留零件号与被测参数关联
   - MSA 计划：页面说明删去「列表维度列跟踪」；关键逻辑人员弹窗改为「仅 支持KAPPA分析方式」、结尾改为「通过 / 不通过/有条件接受」；删除「关键操作」段落；状态表 3 行文字精简
   - 台账：删除「页面说明 / 关键逻辑 / 关键操作」，仅保留「权限说明」
   - 数据录入：删除「页面说明 / 关键操作」，仅保留「关键逻辑」（多操作员×多样本二维录入，每人只看/只改本人数据）
   - 计量器具台账 / 计量器具台账（设计稿）/ 分析结果：整页页面说明删除（不再显示）
2. 渲染函数适配：数据录入分支的关键操作改为条件渲染（g.ops 存在才显示）
3. 维度列状态表 3 行文字更新（未做 / 有条件接受 / 不通过）

## 状态
- 正式版 index.html 未发布；本次为备份。
""" % (TITLE, now)
io.open(os.path.join(backup_dir, '调整内容.md'), 'w', encoding='utf-8').write(md)

# 更新 CHANGELOG.md
cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
line = '| %s | %s | %s |' % (now, TITLE, backup_dir.replace(BASE, '.'))
if os.path.exists(cl):
    with io.open(cl, encoding='utf-8') as f:
        content = f.read()
    if not content.rstrip().endswith('|'):
        pass
    newc = content.rstrip() + '\n' + line + '\n'
else:
    newc = '# CHANGELOG\n\n| 时间 | 主题 | 路径 |\n|---|---|---|\n' + line + '\n'
io.open(cl, 'w', encoding='utf-8').write(newc)

# git 提交推送
subprocess.run(['git', 'add', '-A'], cwd=BASE, check=True)
subprocess.run(['git', 'commit', '-m', '备份：%s' % TITLE], cwd=BASE, check=True)
r = subprocess.run(['git', 'push', 'origin', 'HEAD'], cwd=BASE, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('备份目录:', backup_dir)
print('push:', 'OK' if r.returncode == 0 else r.stderr[-500:])
r2 = subprocess.run(['git', 'log', '-1', '--oneline'], cwd=BASE, capture_output=True, text=True, encoding='utf-8')
print('commit:', r2.stdout.strip())
