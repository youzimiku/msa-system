# -*- coding: utf-8 -*-
"""desc: 全站说明性文字删除 v2"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'FAIL count=%d for: %s' % (c, old[:60])
    s = s.replace(old, new)

def del_block(start_marker, end_marker='</div>'):
    """从 start_marker 起（含）到 end_marker 止（含）删除，并吃掉前面空白"""
    global s
    i = s.find(start_marker)
    assert i > 0, 'del_block not found: ' + start_marker[:50]
    j = s.find(end_marker, i) + len(end_marker)
    assert j > i, 'end not found'
    k = i
    while k > 0 and s[k-1] in ' \n\t':
        k -= 1
    s = s[:k] + s[j:]

# ========== A. 操作区整行说明删除 ==========
rep('\n        <span className="tiny">查询 / 重置 对所有列表生效；一级按钮在下方各自列表区。台账页分为上「器具组列表」、下「器具明细列表」：器具组维护组与成员；器具明细维护每台器具，并标注所属器具组 / 样机标记。</span>', '')
rep('\n        <span className="tiny">为组配置成员器具；创建 MSA 计划时先选器具组，系统拉出该组全部器具并默认选中样机器具。</span>', '')
rep('\n        <span className="tiny">增删改：新增器具 / 登记校准 在此；行内 编辑 / 删除 / 状态变更 亦在此。删除器具会同步清理其 MSA 计划、校准与 GRR/KAPPA 记录，并移出所属器具组。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；检验标准定义在「零件/工序」上（不绑定器具），适用器具按工序自动匹配，另可按「绑定器具组」为周期自动选样准备；创建 MSA 计划时先选零件 → 选该零件的一个检验标准 → 勾选分析方法 → 再勾选器具。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；样本覆盖过程变差（低/中/高），参考值须由更高等级测量设备测定并记录来源，保证 MSA 可溯源。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；{CFG.name}分析记录由 MSA 计划按分析方法自动生成（一器一计划一方法），取样规则固化：{CFG.params(rows[0]||{stds:5,per:12,points:5,groups:25,runs:50})}；{kind===\'resolution\'? \'分辨率不取样，直接录入\' : \'「待采集」记录在对应「录入数据」页录入\'}。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；{CFG.name}台账：{CFG.desc}；「待采集」记录请到「{CFG.name}录入数据」页录入，提交后自动计算分析项并跳转「{CFG.name}分析结果」审核闭环。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；GRR 记录由 MSA 计划定型自动生成，「待采集」记录在「GRR 台账」页录入并提交审核；不合格进入整改-复测-闭环。判定标准：%GRR&lt;10% 可接受；10%~30% 有条件；&gt;30% 不可接受；NDC≥5。</span>', '')
rep('\n        <span className="tiny">查询 / 重置 在最前；KAPPA 记录由 MSA 计划定型自动生成，「待采集」记录在「KAPPA 台账」页录入并提交审核。判定标准（业务三档）：Kappa≥0.75 且有效性≥90%、错误率≤2%、错误警报率≤5% → 可接受；Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10% → 边缘；Kappa&lt;0.40 或有效性&lt;80% 或错误率&gt;5% 或错误警报率&gt;10% → 不可接受-需改进。</span>', '')

# 校准页：拆出统计保留
rep('\n        <span className="tiny">查询 / 重置 在最前；登记校准按校准周期自动生成到期计划，校准记录回写台账，不合格自动停用。统计：90天内到期 {due90.length} 台 ｜ 逾期 {overdue.length} 台 ｜ 本月已登记 {monthCount} 条。</span>',
    '\n        <span className="tiny">统计：90天内到期 {due90.length} 台 ｜ 逾期 {overdue.length} 台 ｜ 本月已登记 {monthCount} 条。</span>')

# ========== B. 创建弹窗 ==========
rep('\n    <Alert style={{marginBottom:12}} type="success" showIcon message="创建流程：先选零件 → 选该零件的一个检验标准（一个 MSA 计划只针对一个质量特性 / 一个检验标准）→ 勾选分析方法（会议口径：特性-量具-方法，一器一计划一方法；GRR 与 KAPPA 不会同时勾选）→ 选择器具组（左侧）→ 在右侧组内器具中勾选本次测量器具（默认选中该组「样机」器具）。勾选 N 个方法即按器具生成 N 个计划，并自动生成对应台账待采集记录。" />', '')
rep('>器具筛选（查询条件） <span className="tiny" style={{color:\'#666666\'}}>（仅用于筛选下方器具清单，不写入计划）</span>', '>器具筛选（查询条件）')
rep('>计划填写信息 <span className="tiny" style={{color:\'#666666\'}}>（以下字段将写入创建的 MSA 计划；带 * 为必选）</span>', '>计划填写信息')
rep('<span className="flt-label">分析方法（五性一力 + Cg/Cgk：重复性、再现性、线性、偏倚、稳定性、分辨力、能力；勾选后按器具批量生成分析任务，一个计划可触发多个任务，计划未完成期间同器具禁止新建计划）</span>',
    '<span className="flt-label">分析方法</span>')
del_block('\n      <div className="tiny mt6">取样策略（按分析方法固化）')
rep('\n    {stdSel && <div style={{marginBottom:8}}><Tag color="blue">本次创建：1 个检验标准 · 1 个质量特性 · 创建后类型为空，待「转 GRR / 转 KAPPA」定型（生成台账待采集记录）</Tag></div>}', '')
rep('（可用下方筛选辅助挑样）', '')
rep('（已默认勾选，可改）', '')
del_block('\n    <div className="tiny mt8">仅「在用 / 待校准」且「无未闭环计划」的器具可纳入')
rep('>未勾选（定型时按分析类型自动带出：GRR=重复性/再现性，KAPPA=kappa）</span>', '>未勾选</span>')

# ========== C. 详情/抽屉 ==========
rep('\n      <div className="tiny mt4">该标准按工序「{detail.processName}」自动匹配以上器具；如需限定到更具体器具，请在计量器具台账维护器具的「工序/检测项目」字段。</div>', '')
rep('{tol&&tol.has?<>公差 {tol.lsl} ~ {tol.usl} <span className="tiny">（自动从测量对象解析）</span></>:<span className="tiny">未识别公差</span>}',
    '{tol&&tol.has?<>公差 {tol.lsl} ~ {tol.usl}</>:<span className="tiny">未识别公差</span>}')
rep('{rec.tolerance&&rec.tolerance.has? <span className="tiny">过程公差：{rec.tolerance.lsl} ~ {rec.tolerance.usl}（自动解析自测量对象）</span>:<span className="tiny">未识别公差，请确认测量对象含公差（如 φ10±0.02）</span>}',
    '{rec.tolerance&&rec.tolerance.has? <span className="tiny">过程公差：{rec.tolerance.lsl} ~ {rec.tolerance.usl}</span>:<span className="tiny">未识别公差</span>}')
rep('\n        <div className="form-hint mt8">固定为「操作员×样本×试验」矩阵（{numOps}×{numParts}×{numTrials}={numOps*numParts*numTrials} 行），每名操作员测量全部样本，禁止自由增/减行；提交前强制校验每一格均有数值，缺失即拦截。验厂/常规检验仅允许交叉型。</div>', '')
rep('<span className="tiny">（业务速查默认值，可调整后重新生成录入矩阵）</span>', '')
rep('\n    <Alert type="info" showIcon style={{marginBottom:12}} message={\'取样规则（固化）：\'+CFG.params(rec)} description={SAMPLING[kind]} />', '')
rep("label('标准件测量（每件 '+perN+' 次可调，覆盖 0~100% 量程）','参考值=鉴定证书/高等级量具真值')",
    "label('标准件测量（每件 '+perN+' 次可调，覆盖 0~100% 量程）')")
rep("label('分辨率（不取样，直接录入）','分辨率应 ≤ 过程公差的 1/10')", "label('分辨率（不取样，直接录入）')")
rep('\n      <div className="tiny mt8">EV=K1·R̄，AV=√((K2·X̄diff)²−EV²/(n·r))，PV=Rp·K3；K1/K2/K3 为 AIAG 常量（按试验/操作员/样本数查表）。</div>', '')
rep('\n      <div className="tiny mt8">{banner.desc}</div>', '', n=2)
rep('\n      <div className="tiny mt8">结论取最差档：任一项落入不可接受区间即整体「不可接受-需改进」；Kappa&gt;0.75 满足一致性要求（业务《MCU6焊接KAPPA报告》样例：Kappa=1.00/0.94，判定「好」）。</div>', '')
del_block('\n          <div className="tiny mt8">评审修正后的业务规则')
rep('\n      <div className="tiny mt8">演示版通过右上角「角色」切换验证权限差异；生产系统建议对接统一身份认证(SSO)与电子签名。</div>', '')
rep('\n      <Alert style={{marginBottom:12}} type="info" showIcon message="定型后将在对应分析台账中建立「待采集」记录，样本数据在台账内录入并提交审核；计划状态与台账记录自动联动。一个 MSA 计划只能选择一个检验标准（一个质量特性）、一个分析方法（会议口径：特性-量具-方法）。" />', '')

# ========== D. DataEntryPage ==========
rep('<span className="tiny">共 {pending.length} 条待采集记录；提交后自动计算分析项并跳转「{CFG.name}分析结果」审核。</span>',
    '<span className="tiny">共 {pending.length} 条待采集记录</span>')
rep('<Panel title="暂无待采集记录"><span>当前没有待采集的{CFG.name}记录。可先在「MSA 计划」页创建计划并转定型生成，或到「{CFG.name}台账」页查看已有记录。</span></Panel>',
    '<Panel title="暂无待采集记录"/>')

# ========== E. PlanTaskDrawer 说明简短化 ==========
rep('{recs.length? <span className="tiny">共 {recs.length} 个分析任务（一个计划可支持多个分析方法）</span> : <span className="tiny">该计划尚未定型生成分析任务，可在列表勾选后转分析方法生成</span>}',
    '{recs.length? <span className="tiny">共 {recs.length} 个分析任务</span> : <span className="tiny">该计划尚未定型</span>}')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('desc v2 删除全部成功')
