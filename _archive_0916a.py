# -*- coding: utf-8 -*-
import io, os, datetime, shutil, subprocess

base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder = ts + '_删三列分号方法日期控件去检验标准'
bk = os.path.join(base, 'backups', folder)
os.makedirs(bk, exist_ok=True)

# 1. 页面快照
shutil.copy2(os.path.join(base, 'index.html'), os.path.join(bk, 'index.html'))

# 2. diff（对比本轮改前快照）
snap = os.path.join(base, 'index_备份_20260916_140021_四条调整前.html')
r = subprocess.run(['git', 'diff', '--no-index', '--', snap, os.path.join(base, 'index.html')],
                   cwd=base, capture_output=True, encoding='utf-8', errors='replace')
diff = (r.stdout or '') + (r.stderr or '')
io.open(os.path.join(bk, '调整内容.diff.txt'), 'w', encoding='utf-8').write(diff)

# 3. 调整说明
md = '''# 调整内容 — 2026-09-16 14:1x（四条调整）

## 1. 抽样方法维护 · 分析方法列表：删除 3 个字段
- 删除列「可否合并取样」（字段 canMerge）
- 删除列「车间」（取样规则的车间字段 subplant）
- 删除列「取样策略说明」（取样规则备注 note）
- 仅删列表列；遗留弹窗（无触发入口的死代码）字段保留不动

## 2. 被测项目维护 · 被测参数列表：检验方法展示改「；」连接的方法名称
- 已选项展示由标签堆叠改为 `GRR；KAPPA；稳定性` 纯文本形式，用「；」分隔
- 显示方法名称（不含括弧内容），不显示方法代码
- 编辑时仍为多选下拉框；新增 CSS `.msa-method-select` 控制展示

## 3. 所有页面：日期/时间字段输入框改为日期选择器
- 新增公共组件 FDate / FDateTime（内部完成 dayjs ↔ 字符串转换，存储格式不变）
- 日期字段（YYYY-MM-DD）→ 日期选择器（共 14 处）：
  - 器具台账新增弹窗：购置年月日、年月日、校准时间、下次校准日期
  - 登记校准弹窗：校准日期
  - 器具组列表行内（新增/编辑）：上次执行时间、下次计划日期、下次提醒时间
  - 器具组弹窗：上次执行时间、下次计划日期、下次提醒时间
  - MSA计划创建弹窗：计划完成日期；计划详情弹窗：实际检期；按人员创建弹窗：计划完成日期
  - 检验标准弹窗：生效日期
  - 样本库列表行内 + 新增弹窗：有效期至
  - 台账弹窗：选取日期
- 时间字段（YYYY-MM-DD HH:mm:ss）→ 日期时间选择器（1 处）：
  - 器具台账新增弹窗：入账时间
- 已存数据不动（原字符串值保留，控件显示为空时不覆盖）

## 4. 样本库管理：查询条件去掉「检验标准」
- 删除查询条件「检验标准」下拉框
- 删除对应筛选逻辑（q.std / 过滤条件 / 查询按钮参数 / 重置参数）
- 样本列表内「关联检验标准」字段不动

## 验证
- shot.py 渲染无 console 错误
- 无头 Chrome 依次渲染 被测项目维护 / 抽样方法维护 / 样本库管理 / MSA计划 四个页面，均正常出数据
'''
io.open(os.path.join(bk, '调整内容.md'), 'w', encoding='utf-8').write(md)

# 4. CHANGELOG 追加
cl = os.path.join(base, 'backups', 'CHANGELOG.md')
c = io.open(cl, encoding='utf-8').read()
row = '| ' + ts[:4] + '-' + ts[4:6] + '-' + ts[6:8] + ' ' + ts[8:10] + ':' + ts[10:12] + ' | ' + folder + ' | 删分析方法三字段；检验方法分号连接展示；日期/时间改选择器；样本库查询去检验标准 |\n'
c = c.replace('| 2026-09-16 13:27 | 20260916_132711_时间到秒状态列移动范围合并 | 时间字段统一到秒；检验标准状态列前移；范围字段合并、读数下限/上限删除 |\n',
              '| 2026-09-16 13:27 | 20260916_132711_时间到秒状态列移动范围合并 | 时间字段统一到秒；检验标准状态列前移；范围字段合并、读数下限/上限删除 |\n' + row)
io.open(cl, 'w', encoding='utf-8').write(c)

print('ARCHIVED:', folder)
