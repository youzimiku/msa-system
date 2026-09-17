# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
SNAP = os.path.join(BASE, 'index_备份_20260916_150700_下拉框改造前.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder = os.path.join(BASE, 'backups', ts + '_下拉框改造')
os.makedirs(folder, exist_ok=True)

# 1. 页面快照
shutil.copy2(CUR, os.path.join(folder, 'index.html'))

# 2. 调整内容.md
md = """# 调整内容：下拉框改造（2026-09-16）

## 本次改动清单（精确到字段）

### ① 被测项目维护 → 页面名称改"被测参数维护"
- 菜单 label：被测项目维护 → 被测参数维护
- 页面标题映射（PAGE_TITLE）'char'：被测项目维护 → 被测参数维护
- 页面说明（PAGE_DESC.char.label）：被测项目维护 → 被测参数维护
- 页面头部（PageHead title）：被测项目维护 → 被测参数维护
- 导入按钮标题（ImportBtn title）：被测项目维护 → 被测参数维护

### ② 样本库管理 · 样本列表
- 列"对应被测项目"（charDim）→ 列名改"被测参数"，控件 Input → Select 下拉框，选项 = 被测参数维护页面的被测参数名称（d.characteristics[].name）
- 列"零件号"（partNo）控件 Input → Select 下拉框（模拟数据 PARTNO_OPT）
- 列"零件名称"（partName）控件 Input → Select 下拉框（模拟数据 PARTNAME_OPT）
- 列"单位"（unit）控件 Input → Select 下拉框（模拟数据 UNIT_OPT）

### ③ 抽样方法维护 · 分析方法列表
- 列"方法组"（mergeWith）去掉占位文字"如：尺寸类合并组"（只留空输入框）
- 列"默认适用"（defaultType）→ 列名改"数据类型"，控件 Input → Select 下拉框（选项：计量型/计数型）

### ④ 被测参数维护 · 被测参数列表
- 列"零件编号"（partNo）→ 列名改"零件号"，与"零件名称"列互换位置（零件号在前、零件名称在后）
- 列"零件号"控件 Input → Select 下拉框（模拟数据 PARTNO_OPT）
- 列"零件名称"（partName）控件 Input → Select 下拉框（模拟数据 PARTNAME_OPT）
- 列"工序"（processName）控件 Input → Select 下拉框（模拟数据 PROCESS_OPT）
- 列"特性类别"（category）→ 列名改"数据类型"，控件 Input → Select 下拉框（选项：计量型/计数型）
- 列"单位"（unit）控件 Input → Select 下拉框（模拟数据 UNIT_OPT）
- 未改动：列"特性类型"（type：SC/CC/普通）

### ⑤ MSA计划 · 计划列表
- 列"零件号"（partNo）控件 Input → Select 下拉框（模拟数据 PARTNO_OPT）
- "零件号"列后新增列"零件名称"（partName），控件 Select 下拉框（模拟数据 PARTNAME_OPT）
- 删除列"检验标准"（原按台账记录 standard 字段聚合显示）
- 列"分析人"（analyst||observer）控件 Input → Select 下拉框（模拟数据 ANALYST_OPT）
- 列"部门"（dept）控件 Input → Select 下拉框（模拟数据 DEPT_OPT）
- 列"分厂"（subplant）→ 列名改"工厂"，控件 Input → Select 下拉框，绑定字段改为 plant（工厂名），选项 PLANTS_OPT
- 列"测量特性"（object）→ 列名改"被测参数"，控件 Input → 纯文本只读（不可编辑）
  - 取值逻辑不变：创建计划时选择的被测参数 → 台账记录 object → 列表聚合读回（多器具用"、"连接）

### ⑥ 新增模拟数据下拉常量（全局）
- PARTNO_OPT：PN-1000 ~ PN-5001（12 项）
- PARTNAME_OPT：轴类件 / 孔类件 / 标准件 / 轴端盖 / 壳体 / 齿轮轴
- PROCESS_OPT：精加工 / 检验 / 装配 / 机加工 / 终检 / 总装
- UNIT_OPT：mm / μm / N / N·m / kg / g / °C / MPa / 件
- DEPT_OPT：品质部 / 总装车间 / 电控车间 / 计量室 / 实验室 / 质量
- ANALYST_OPT：王强 / 刘青 / 张伟 / 孙丽 / 赵磊 / 周敏 / 吴刚 / 郑芳 / 冯强 / 何静 / 李工程师 / 陈杰 / 吴芳 / 周军

## 说明
- 仅改前端展示与控件类型，不改数据交互逻辑、不做数据校验。
- 未改动范围（按用户要求只改点名内容）：被测参数详情抽屉/编辑弹窗中的"零件编号"字样保留原样。
"""
io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)

# 3. diff
a = io.open(SNAP, encoding='utf-8').read().splitlines()
b = io.open(CUR, encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(a, b, fromfile='index_备份_20260916_150700_下拉框改造前.html', tofile='index.html', lineterm=''))
io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))

# 4. CHANGELOG 追加
cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
line = f"- {ts} 下拉框改造：①页面名被测项目维护→被测参数维护(5处) ②样本库:对应被测项目→被测参数下拉/零件号·零件名称·单位改下拉 ③抽样方法:默认适用→数据类型下拉/方法组去placeholder ④被测参数列表:零件编号→零件号并与零件名称换位/零件号·零件名称·工序·单位下拉/特性类别→数据类型下拉 ⑤MSA计划:零件号后加零件名称列/零件号·分析人·部门下拉/删检验标准列/分厂→工厂下拉/测量特性→被测参数只读 ⑥新增6组模拟下拉常量\n"
io.open(cl, 'a', encoding='utf-8').write(line)

print('归档完成:', folder)
print('CHANGELOG 已追加')
