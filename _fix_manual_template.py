# -*- coding: utf-8 -*-
"""更新手册模板：第7章改为「取数录入与分析结果」，图片占位符指向新截图"""
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_gen_manual.py'
s = open(p, encoding='utf-8').read()

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:60], n, cnt))
    s = s.replace(old, new)

# 侧边栏
rep('<a href="#s7">七、分析台账（六类）</a>', '<a href="#s7">七、取数录入与分析结果</a>')

# 章节标题与副标题
rep('<h2><span class="no">7</span>分析台账（六类）</h2>',
    '<h2><span class="no">7</span>取数录入与分析结果</h2>')
rep('<p class="sub">GRR / KAPPA / 线性·偏移 / 稳定性 / Cg·Cgk / 分辨率 六类台账共用同一闭环：<b>待采集 → 录入数据 → 提交判定（待审核）→ 审核通过（已批准）｜ 退回整改（需整改）→ 纠正措施 → 整改完成·复测 → 已闭环</b>。</p>',
    '<p class="sub">取数/录入与结果展示按分析方法拆分为 5 套独立页面（GRR / KAPPA / 线性·偏移 / 稳定性 / Cg·Cgk），分辨率分析保留原样。闭环：<b>计划定型生成「待采集」→ 在对应「取数录入」页录入并提交 → 在对应「分析结果」页审核通过（已批准）｜ 退回整改（需整改）→ 纠正措施 → 整改完成·复测 → 已闭环</b>。</p>')

# 7.1 通用操作流程
rep('<div class="step"><div class="n">1</div><div class="t"><b>录入数据</b><span>「待采集」记录行点「录入数据」，按固化取样策略生成默认行数（可增减），填写测量值；GRR 为操作员×样本×试验的交叉矩阵，完整性校验不通过会被拦截。</span></div></div>',
    '<div class="step"><div class="n">1</div><div class="t"><b>进入取数录入页</b><span>菜单「取数录入」下按分析方法分 5 个独立页面（GRR / KAPPA / 线性偏移 / 稳定性 / Cg·Cgk）；「待采集」记录行点「录入数据」，按固化取样策略生成默认行数（可增减），填写测量值；GRR 为操作员×样本×试验的交叉矩阵，完整性校验不通过会被拦截。</span></div></div>')
rep('<div class="step"><div class="n">2</div><div class="t"><b>提交分析</b><span>点击「提交分析」，系统按标准自动计算并给出结论（如 %GRR / NDC / KAPPA / Cg·Cgk / 线性 R² / 控制图出界点数），记录进入「待审核」。</span></div></div>',
    '<div class="step"><div class="n">2</div><div class="t"><b>提交分析</b><span>点击「提交分析」，系统按标准自动计算并给出结论（如 %GRR / NDC / KAPPA / Cg·Cgk / 线性 R² / 控制图出界点数），记录进入「待审核」并跳转对应「分析结果」页。</span></div></div>')
rep('<div class="step"><div class="n">3</div><div class="t"><b>审核</b><span>审核员「审核通过」→ 已批准（一次通过）；「退回整改」→ 需整改。</span></div></div>',
    '<div class="step"><div class="n">3</div><div class="t"><b>审核</b><span>在「分析结果」页（GRR / KAPPA / 线性偏移 / 稳定性 / Cg·Cgk 各为独立页面）打开「详情/审核」：审核员「审核通过」→ 已批准（一次通过）；「退回整改」→ 需整改。</span></div></div>')
rep('<div class="step"><div class="n">4</div><div class="t"><b>整改闭环</b><span>「需整改」记录添加纠正措施（类型 / 内容 / 责任人 / 计划完成）→ 复测验证后点「整改完成 · 复测验证 · 闭环」→ 已闭环。</span></div></div>',
    '<div class="step"><div class="n">4</div><div class="t"><b>整改闭环</b><span>「需整改」记录在「分析结果」页添加纠正措施（类型 / 内容 / 责任人 / 计划完成）→ 复测验证后点「整改完成 · 复测验证 · 闭环」→ 已闭环。</span></div></div>')

# 图片区：07/08/09 图注 + 新增 11
rep('<img class="img" src="{{IMG_07}}" alt="GRR台账">\n      <div class="imgcap">▲ GRR 台账：5 条记录，待采集行有「录入数据」，已分析行可「详情/审核」</div>',
    '<img class="img" src="{{IMG_07}}" alt="GRR取数录入">\n      <div class="imgcap">▲ GRR 取数录入页：待采集记录展开录入面板（操作员×样本×试验交叉矩阵），提交后自动计算并跳转「GRR 分析结果」</div>')
rep('<img class="img" src="{{IMG_08}}" alt="KAPPA台账">\n      <div class="imgcap">▲ KAPPA 台账：计数型一致性，展示总体 KAPPA、有效性、漏判/误判</div>',
    '<img class="img" src="{{IMG_08}}" alt="KAPPA取数录入">\n      <div class="imgcap">▲ KAPPA 取数录入页：检验员判定矩阵（合格/不合格，盲测）；结果在「KAPPA 分析结果」页展示总体 KAPPA、有效性、漏判/误判</div>')
rep('<img class="img" src="{{IMG_09}}" alt="CgCgk分析台账">\n      <div class="imgcap">▲ Cg/Cgk 分析台账（VDA Type1）：固化 50 次取样规则，结论「可接受」，状态已批准</div>',
    '<img class="img" src="{{IMG_09}}" alt="CgCgk取数录入">\n      <div class="imgcap">▲ Cg/Cgk 取数录入页（VDA Type1）：固化取样规则；结果在「Cg/Cgk 分析结果」页展示</div>\n      <img class="img" src="{{IMG_11}}" alt="GRR分析结果">\n      <div class="imgcap">▲ GRR 分析结果页：展示 %GRR / NDC / 公差%GRR / 变差分解与判定；「待采集」行提供「去录入」快捷跳转取数页</div>')

# 11.2 速查表（更新入口）
rep('<tr><td>维护器具组 / 默认器具</td><td>计量器具台账 → 上方器具组列表</td></tr>',
    '<tr><td>维护器具组 / 样机属性</td><td>计量器具台账 → 上方器具组列表 / 下方器具明细（样机列）</td></tr>')
rep('<tr><td>录入 GRR 样本</td><td>GRR 台账 → 待采集行「录入数据」</td></tr>',
    '<tr><td>录入 GRR 样本</td><td>取数录入 → GRR 取数录入 → 待采集行「录入数据」</td></tr>')
rep('<tr><td>录入 KAPPA 判定</td><td>KAPPA 台账 → 待采集行「录入数据」</td></tr>',
    '<tr><td>录入 KAPPA 判定</td><td>取数录入 → KAPPA 取数录入 → 待采集行「录入数据」</td></tr>')
rep('<tr><td>审核一条分析</td><td>对应分析台账 → 详情/审核 → 审核通过 / 退回整改</td></tr>',
    '<tr><td>审核一条分析</td><td>分析执行 → 对应分析结果页 → 详情/审核 → 审核通过 / 退回整改</td></tr>')
if 'GRR 台账' in s:
    s = s.replace('GRR 台账', 'GRR 分析结果')
if 'KAPPA 台账' in s:
    s = s.replace('KAPPA 台账', 'KAPPA 分析结果')
if 'Cg/Cgk 分析台账' in s:
    s = s.replace('Cg/Cgk 分析台账', 'Cg/Cgk 分析结果')
if '线性/偏移性分析台账' in s:
    s = s.replace('线性/偏移性分析台账', '线性/偏移分析结果')
if '稳定性分析台账' in s:
    s = s.replace('稳定性分析台账', '稳定性分析结果')

open(p, 'w', encoding='utf-8').write(s)
print('manual template patched')
