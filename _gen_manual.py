# -*- coding: utf-8 -*-
"""生成 MSA 系统操作手册 HTML（Ant Design 风格，图片 base64 内嵌）"""
import io, json, os

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
b64 = json.load(io.open(os.path.join(BASE, 'manual-img', 'b64.json'), encoding='utf-8'))
IM = lambda k: b64.get(k, '')

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MSA 测量系统分析管理系统 · 操作手册</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/antd@5.21.6/dist/reset.css">
<style>
  :root{--primary:#1677ff;--bg:#f5f5f5;--card:#fff;}
  *{box-sizing:border-box;}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif;background:var(--bg);color:#1a1a1a;font-size:14px;line-height:1.7;}
  .layout{display:flex;min-height:100vh;}
  .sider{width:240px;background:#001529;color:rgba(255,255,255,.75);position:fixed;top:0;left:0;bottom:0;overflow-y:auto;padding:16px 0;z-index:10;}
  .sider .logo{color:#fff;font-size:17px;font-weight:600;padding:8px 24px 16px;border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:8px;white-space:nowrap;}
  .sider .logo small{display:block;font-size:11px;font-weight:400;color:rgba(255,255,255,.45);margin-top:2px;}
  .sider a{display:block;color:rgba(255,255,255,.7);text-decoration:none;padding:9px 24px;font-size:13px;border-left:3px solid transparent;}
  .sider a:hover{color:#fff;background:rgba(255,255,255,.06);}
  .sider a.on{color:#fff;background:#1677ff;border-left-color:#69b1ff;}
  .main{flex:1;margin-left:240px;padding:24px 32px 64px;min-width:0;}
  .hero{background:linear-gradient(120deg,#0b3b8c,#1677ff 55%,#4096ff);color:#fff;border-radius:16px;padding:32px 36px;margin-bottom:24px;}
  .hero h1{margin:0 0 6px;font-size:26px;font-weight:600;}
  .hero p{margin:0;opacity:.85;font-size:13px;}
  .hero .tags{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;}
  .tag{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:2px 12px;font-size:12px;}
  .card{background:#fff;border-radius:14px;padding:24px 28px;margin-bottom:22px;box-shadow:0 1px 3px rgba(0,0,0,.05);}
  .card h2{font-size:19px;margin:0 0 4px;color:#0b3b8c;font-weight:600;}
  .card h2 .no{display:inline-block;background:#1677ff;color:#fff;border-radius:8px;font-size:14px;width:26px;height:26px;line-height:26px;text-align:center;margin-right:8px;vertical-align:2px;}
  .card h3{font-size:15px;color:#333;margin:18px 0 8px;border-left:4px solid #1677ff;padding-left:10px;}
  .card h4{font-size:14px;margin:14px 0 6px;color:#1677ff;}
  .sub{color:#888;font-size:12px;margin:0 0 12px;}
  .step{display:flex;gap:12px;margin:10px 0;}
  .step .n{flex-shrink:0;width:24px;height:24px;border-radius:50%;background:#e6f4ff;color:#0958d9;font-weight:600;font-size:13px;display:flex;align-items:center;justify-content:center;margin-top:2px;}
  .step .t{flex:1;min-width:0;}
  .step .t b{display:block;font-size:13.5px;}
  .step .t span{font-size:13px;color:#555;}
  .img{width:100%;max-width:1280px;border:1px solid #e8e8e8;border-radius:10px;margin:8px 0 4px;display:block;}
  .imgcap{font-size:12px;color:#888;margin:2px 0 10px;}
  .tbl{width:100%;border-collapse:collapse;margin:8px 0;font-size:13px;}
  .tbl th,.tbl td{border:1px solid #e8e8e8;padding:7px 10px;text-align:left;}
  .tbl th{background:#fafafa;font-weight:600;white-space:nowrap;}
  .tbl tr:nth-child(even) td{background:#fcfcfc;}
  .ok{color:#389e0d;font-weight:600;}
  .bad{color:#cf1322;font-weight:600;}
  .warn{color:#d46b08;font-weight:600;}
  .flow{display:flex;gap:6px;flex-wrap:wrap;align-items:stretch;margin:12px 0;}
  .flow .node{flex:1 1 120px;min-width:0;border-radius:10px;padding:10px 12px;font-size:12.5px;background:#e6f4ff;border:1px solid #91caff;}
  .flow .node b{display:block;font-size:13px;color:#0958d9;margin-bottom:2px;}
  .flow .node.green{background:#f6ffed;border-color:#b7eb8f;}
  .flow .node.green b{color:#389e0d;}
  .flow .arrow{align-self:center;color:#91caff;font-size:16px;flex-shrink:0;}
  .note{background:#fffbe6;border:1px solid #ffe58f;border-radius:8px;padding:10px 14px;font-size:13px;margin:10px 0;}
  .note.red{background:#fff2f0;border-color:#ffccc7;}
  .note.blue{background:#e6f4ff;border-color:#91caff;}
  .kbd{background:#f5f5f5;border:1px solid #d9d9d9;border-radius:4px;padding:0 6px;font-size:12px;font-family:Consolas,monospace;}
  .toTop{position:fixed;right:24px;bottom:24px;background:#1677ff;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-size:13px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15);z-index:20;}
  @media (max-width:900px){ .sider{display:none;} .main{margin-left:0;padding:14px;} .hero{padding:22px;} .card{padding:16px;} }
</style>
</head>
<body>
<div class="layout">

  <nav class="sider">
    <div class="logo">MSA 测量系统分析<br><small>管理系统操作手册</small></div>
    <a href="#s1">一、系统概述与闭环</a>
    <a href="#s2">二、角色与权限</a>
    <a href="#s3">三、计量器具台账</a>
    <a href="#s4">四、校准管理</a>
    <a href="#s5">五、检验标准维护</a>
    <a href="#s6">六、MSA 计划</a>
    <a href="#s7">七、台账与分析结果</a>
    <a href="#s8">八、样本管理</a>
    <a href="#s9">九、仪表盘总览</a>
    <a href="#s10">十、业务规则与防漏洞</a>
    <a href="#s11">十一、速查表</a>
  </nav>

  <main class="main">

    <div class="hero">
      <h1>MSA 测量系统分析管理系统 · 操作手册</h1>
      <p>版本 V2.5 ｜ 朴素化 UI 与台账命名版（AIAG 五性 vs VDA Cgk 业务速查表：样品数/人数/次数可调）｜ 设计依据：AIAG MSA 第4版 / IATF 16949 / ISO 10012</p>
      <div class="tags">
        <span class="tag">计量器具台账</span><span class="tag">校准管理</span><span class="tag">检验标准</span>
        <span class="tag">MSA 计划</span><span class="tag">GRR</span><span class="tag">KAPPA</span>
        <span class="tag">线性/偏移</span><span class="tag">稳定性</span><span class="tag">Cg/Cgk</span><span class="tag">分辨率</span>
      </div>
    </div>

    <!-- 一、系统概述 -->
    <div class="card" id="s1">
      <h2><span class="no">1</span>系统概述与业务闭环</h2>
      <p class="sub">本系统以「测量系统能力分析」为核心，计量台账 / 校准 / 检验标准为数据基础，MSA 计划即分析任务，样本录入与判定闭环在各分析台账内完成。</p>
      <div class="flow">
        <div class="node"><b>计量器具台账</b>器具组＋样机标记·校准状态</div>
        <div class="arrow">→</div>
        <div class="node"><b>检验标准</b>绑零件/工序·绑器具组</div>
        <div class="arrow">→</div>
        <div class="node"><b>MSA 计划</b>选零件→选标准→勾方法→器具组→勾器具（一器一计划一方法）</div>
        <div class="arrow">→</div>
        <div class="node"><b>六类分析台账</b>录入→提交判定→待审核</div>
        <div class="arrow">→</div>
        <div class="node green"><b>审核/整改闭环</b>已批准 / 需整改→纠正措施→已闭环</div>
      </div>
      <div class="flow">
        <div class="node green"><b>闭环回写</b>计划状态联动·器具「上次MSA」更新·复评周期滚动</div>
        <div class="arrow">→</div>
        <div class="node green"><b>可重新发起</b>已批准/已闭环/已关闭器具可再建计划（周期复评）</div>
        <div class="arrow">→</div>
        <div class="node">仪表盘/审计日志全程可追溯</div>
      </div>
      <div class="note blue">核心原则：<b>1 个 MSA 计划 = 1 台器具 × 1 个质量特性 × 1 个分析方法</b>；一个计划只对应一个检验标准；GRR 与 KAPPA 不会在同一器具同时开展（KAPPA 是计数型分支）。</div>
    </div>

    <!-- 二、角色与权限 -->
    <div class="card" id="s2">
      <h2><span class="no">2</span>角色与权限</h2>
      <p class="sub">右上角可切换角色，用于演示不同岗位的操作边界。</p>
      <table class="tbl">
        <tr><th>角色</th><th>查看</th><th>创建/编辑</th><th>样本录入/提交</th><th>审核通过/退回</th><th>关闭计划</th></tr>
        <tr><td>浏览者 viewer</td><td>✔</td><td>✘</td><td>✘</td><td>✘</td><td>✘</td></tr>
        <tr><td>质量工程师 quality</td><td>✔</td><td>✔</td><td>✔</td><td>✔</td><td>✘</td></tr>
        <tr><td>审核员 auditor</td><td>✔</td><td>✔</td><td>✔</td><td>✔</td><td>✔</td></tr>
        <tr><td>管理员 admin</td><td>✔</td><td>✔</td><td>✔</td><td>✔</td><td>✔</td></tr>
      </table>
    </div>

    <!-- 三、计量器具台账 -->
    <div class="card" id="s3">
      <h2><span class="no">3</span>计量器具台账</h2>
      <p class="sub">台账页为上下两个列表：上方「器具组列表」、下方「器具明细列表」，均按「查询条件 / 操作 / 列表」三面板布局。</p>

      <h3>3.1 器具组维护（上方列表）</h3>
      <div class="step"><div class="n">1</div><div class="t"><b>新增器具组</b><span>点击「＋新增器具组」，填写组编号、组名称，勾选组内成员器具并标记「样机」（样机器具在创建 MSA 计划时默认选中）。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>编辑 / 删除</b><span>行内「编辑」可调整成员与样机标记；「删除」移除整组（组内器具本身保留在台账）。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>作用</b><span>创建 MSA 计划时先选器具组 → 系统拉出该组全部器具并默认选中默认器具，便于同组快速批量建档。</span></div></div>

      <h3>3.2 器具明细维护（下方列表）</h3>
      <div class="step"><div class="n">1</div><div class="t"><b>按组查看</b><span>明细列表按当前选中的器具组过滤；默认器具优先显示；列含校准时间、校准状态（正常/临期/超期）、复评提醒。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>新增 / 编辑 / 删除</b><span>「＋新增器具」登记新量具（含样机标记）；行内「编辑」维护档案；「删除」会同步清理其 MSA 计划、校准与台账记录并移出所属组，请谨慎操作。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>登记校准 / 状态变更</b><span>「登记校准」跳转校准登记；「状态变更」调整 在用/停用/报废/封存/待校准（校准逾期应停用）。</span></div></div>
      <div class="note">样机标记：被标记为「样机」的器具参与周期自动选样，是周期校验时筛出待建计划的依据。</div>
      <img class="img" src="{{IMG_02}}" alt="计量器具台账">
      <div class="imgcap">▲ 计量器具台账：上器具组列表（4 组）、下器具明细（当前组 G-01），操作列均在列表最前</div>
    </div>

    <!-- 四、校准管理 -->
    <div class="card" id="s4">
      <h2><span class="no">4</span>校准管理</h2>
      <p class="sub">校准记录与台账互通：登记校准自动回写器具「下次校准日期 / 校准状态」，不合格自动停用。</p>
      <div class="step"><div class="n">1</div><div class="t"><b>登记校准</b><span>点击「＋登记校准」，选择器具，填写校准日期、机构、证书编号、依据规程、结果、费用；提交后自动按校准周期生成下次校准日期并回写台账。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>到期校准计划</b><span>系统按周期自动列出到期清单（逾期 / 30 天内 / 90 天内），逐台「登记校准」即可闭环。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>查询筛选</b><span>支持关键词、校准结果、校准方式、校准状态（正常 / 临期 / 超期）筛选；查询 / 重置位于操作区最前。</span></div></div>
      <img class="img" src="{{IMG_03}}" alt="校准管理">
      <div class="imgcap">▲ 校准管理：校准记录台账（6 条）＋ 到期校准计划（5 条），无分页签</div>
    </div>

    <!-- 五、检验标准维护 -->
    <div class="card" id="s5">
      <h2><span class="no">5</span>检验标准维护</h2>
      <p class="sub">检验标准定义在「零件 / 工序」上（不直接绑器具），并可按「绑定器具组」为周期自动选样做准备。</p>
      <div class="step"><div class="n">1</div><div class="t"><b>新增标准</b><span>填写检验项目号、项目名、零件名称、工序名称、检验标准、检验方法、测量人数 / 次数、样本数量、分辨率、判定准则，以及质检区划、工厂、分厂等。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>查看准则 / 修订</b><span>「查看准则」查看判定阈值与依据（如 %GRR&lt;10% 可接受）；「修订」变更版本并记录修订日志。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>绑定器具组</b><span>编辑标准时可多选「绑定器具组」，为将来按组自动选样、批量生成计划做准备。</span></div></div>
      <div class="note">创建 MSA 计划时：<b>先选零件 → 再选该零件下的一个检验标准</b>（一个计划一个标准）；标准不是从器具选出来的，而是从零件/工序带出来的。</div>
      <img class="img" src="{{IMG_04}}" alt="检验标准维护">
      <div class="imgcap">▲ 检验标准维护：6 条标准，字段按业务口径展开</div>
    </div>

    <!-- 六、MSA 计划 -->
    <div class="card" id="s6">
      <h2><span class="no">6</span>MSA 计划</h2>
      <p class="sub">计划即分析任务：一个计划 = 一台器具的一次分析；创建时可直接勾选分析方法（立即定型并生成台账待采集记录），也可不勾选生成「未定型」计划稍后转 GRR / KAPPA。</p>

      <h3>6.1 创建 MSA 计划</h3>
      <div class="step"><div class="n">1</div><div class="t"><b>选零件/工序</b><span>在弹窗「① 零件/工序」下拉选择零件（检验标准定义在此）。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>选检验标准</b><span>「② 检验标准」自动解锁为该零件适用标准，选择 1 个（一个计划一个标准）。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>勾选分析方法</b><span>勾选 GRR / KAPPA / 线性·偏移 / 稳定性 / Cg·Cgk / 分辨率（可多选，勾 N 个方法按每台器具生成 N 个计划；GRR 与 KAPPA 不同时勾选）。</span></div></div>
      <div class="step"><div class="n">4</div><div class="t"><b>选器具组 → 勾器具</b><span>左侧选「器具组」，右侧列出该组全部器具，默认选中该组「样机」器具，可增选同组器具。</span></div></div>
      <div class="step"><div class="n">5</div><div class="t"><b>调节取样参数（可选）</b><span>器具清单每行有 人数 / 次数 / 样本数 三列：按勾选方法带出业务速查默认值（GRR 3人×3次×10件、KAPPA 3人×3次×50件、线性 5 件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次），可在允许范围内调整，提交后按新参数生成录入矩阵。</span></div></div>
      <div class="step"><div class="n">6</div><div class="t"><b>确认创建</b><span>点击「确认创建」：生成 N 个计划，并自动生成对应台账「待采集」记录，可直接到台账录入样本。</span></div></div>
      <div class="note">复评状态（查询条件）：正常 / 0-15天 / 16-30天 / 超期，按「上次 MSA 日期＋复评周期」推算下次复评；复评周期与提前提醒天数可自定义（默认 12 个月 / 提前 20 天）。</div>
      <div class="note red">防重复规则：校准已过期、或该器具存在未闭环计划（未定型 / 待采集 / 待审核 / 需整改）时，器具不可勾选；已批准 / 已闭环 / 已关闭后即可重新发起周期复评。</div>
      <img class="img" src="{{IMG_06}}" alt="创建MSA计划弹窗">
      <div class="imgcap">▲ 创建 MSA 计划弹窗：左器具组面板、右器具明细；复评状态/周期/提前提醒；校准状态与复评提醒列</div>

      <h3>6.2 计划列表与定型</h3>
      <div class="step"><div class="n">1</div><div class="t"><b>查询</b><span>按计划号 / 量具号 / 器具名称 / 零件，或分析类型、计划状态筛选。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>转 GRR / 转 KAPPA</b><span>勾选「未定型」计划，点顶部「转 GRR」或「转 KAPPA」→ 批量定型并生成台账待采集记录 → 自动跳转对应台账。若无匹配标准或已生成记录，系统会明确提示并中止。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>行操作</b><span>每行固定「台账 / 编辑 / 详情」三按钮（操作列在列表最前）；「台账」跳转该计划的分析台账。</span></div></div>
      <div class="step"><div class="n">4</div><div class="t"><b>详情 / 关闭</b><span>详情内可补录信息或定型；admin / 审核员可「关闭」已结束计划（关闭会同步关闭其全部台账记录）。</span></div></div>
      <img class="img" src="{{IMG_05}}" alt="MSA计划列表">
      <div class="imgcap">▲ MSA 计划列表：查询 / 操作 / 列表三面板，操作列最前，状态为 待开始 / 进行中 / 已完成</div>
    </div>

    <!-- 七、分析台账 -->
    <div class="card" id="s7">
      <h2><span class="no">7</span>台账与分析结果</h2>
      <p class="sub">取数/录入与结果展示按分析方法拆分为 5 套独立页面（GRR / KAPPA / 线性·偏移 / 稳定性 / Cg·Cgk），分辨率分析保留原样。闭环：<b>计划定型生成「待采集」→ 在对应「台账」页录入并提交 → 在对应「分析结果」页审核通过（已批准）｜ 退回整改（需整改）→ 纠正措施 → 整改完成·复测 → 已闭环</b>。</p>

      <h3>7.1 通用操作流程</h3>
      <div class="step"><div class="n">1</div><div class="t"><b>进入台账页</b><span>菜单「台账」下按分析方法分 5 个独立页面（GRR / KAPPA / 线性偏移 / 稳定性 / Cg·Cgk）；「待采集」记录行点「录入数据」，按业务速查默认值生成录入矩阵（GRR 3人×3次×10件、KAPPA 3人×3次×50件、线性 5 件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次），人数/次数/样本数可调后点「重新生成」按新参数展开矩阵，填写测量值；GRR 为操作员×样本×试验的交叉矩阵，完整性校验不通过会被拦截。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>提交分析</b><span>点击「提交分析」，系统按标准自动计算并给出结论（如 %GRR / NDC / KAPPA / Cg·Cgk / 线性 R² / 控制图出界点数），记录进入「待审核」并跳转对应「分析结果」页。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>审核</b><span>在「分析结果」页（GRR / KAPPA / 线性偏移 / 稳定性 / Cg·Cgk 各为独立页面）打开「详情/审核」：审核员「审核通过」→ 已批准（一次通过）；「退回整改」→ 需整改。</span></div></div>
      <div class="step"><div class="n">4</div><div class="t"><b>整改闭环</b><span>「需整改」记录在「分析结果」页添加纠正措施（类型 / 内容 / 责任人 / 计划完成）→ 复测验证后点「整改完成 · 复测验证 · 闭环」→ 已闭环。</span></div></div>
      <div class="note">闭环回写：分析达到「已批准 / 已闭环」终态时，系统自动将该器具「上次 MSA」更新为当天，复评周期随之滚动，进入下一轮周期复评。</div>

      <h3>7.2 各类分析取样与判定口径</h3>
      <table class="tbl">
        <tr><th>分析类型</th><th>取样策略（固化）</th><th>判定口径</th></tr>
        <tr><td>GRR（计量型）</td><td>10 个生产件 × 3 人 × 每件 2~3 次（60~90 组）；交叉表＋ANOVA，不做嵌套</td><td>%GRR&lt;10% 可接受；10%~30% 有条件；&gt;30% 不可接受；NDC≥5</td></tr>
        <tr><td>KAPPA（计数型）</td><td>50 件 × 3 人 × 每件 3 次（20~50 件、2~5 人可调，多数裁决为该件结论）</td><td>业务三档表：Kappa≥0.75 且有效性≥90%、错误率≤2%、错误警报率≤5% → 可接受；Kappa 0.40~0.75 / 有效性 80%~90% / 错误率 2%~5% / 错误警报率 5%~10% → 边缘；Kappa&lt;0.40 或有效性&lt;80% 或错误率&gt;5% 或错误警报率&gt;10% → 不可接受-需改进（取最差档）</td></tr>
        <tr><td>线性 / 偏移</td><td>线性：5 个标准件覆盖 0~100% 量程，每件 12 次（10~12 次可调，读数 50~60）；偏倚：1 件标准件重复测 15 次（10~15 次可调，真值可追溯），先正态性检验（P&gt;0.05）</td><td>业务 4 条：①"0"水平线完全包围在 95% 置信区间内 → 非常理想可接受；②"0"出区间、常量显著≠0、斜率显著=0 → 固定偏倚可修正（可接受）；③"0"出区间、斜率显著≠0、平均偏倚在区间内 → 线性偏倚可修正（较理想）；④"0"出区间、斜率≈0、出界点位于不同侧 → 不可接受</td></tr>
        <tr><td>稳定性</td><td>长周期跨 4 周~3 个月，固定参照仪工位，25 个子组 × 每期 5 次（3~5 次可调，读数 75~125），SPC 判异</td><td>X̄-R 控制图无出界点可接受；出界需查因纠偏</td></tr>
        <tr><td>Cg / Cgk（VDA）</td><td>1 件标准件（中值）独立装夹连续测 50 次（50~200 次可调），偏倚打包进 Cgk</td><td>① Cg、Cgk 均≥1.33 → 可接受（能力充足，可用于量产判定）；② Cg 偏小 → 重复性差，需检修/更换；③ Cg 合格、Cgk 偏小 → 系统性偏倚，需重新校准；④ 负 Cgk → 偏倚超 10% 公差，不可使用立即整改；⑤ 6σ/T≤15% 优秀、≤20% 可接受</td></tr>
        <tr><td>分辨率</td><td>不取样，直接录入分辨力值</td><td>分辨率 ≤ 1/10 过程公差</td></tr>
      </table>

      <img class="img" src="{{IMG_07}}" alt="GRR台账">
      <div class="imgcap">▲ GRR 台账页：待采集记录展开录入面板（操作员×样本×试验交叉矩阵），提交后自动计算并跳转「GRR 分析结果」</div>
      <img class="img" src="{{IMG_08}}" alt="KAPPA台账">
      <div class="imgcap">▲ KAPPA 台账页：检验员判定矩阵（合格/不合格，盲测）；结果在「KAPPA 分析结果」页展示总体 KAPPA、有效性、漏判/误判</div>
      <img class="img" src="{{IMG_09}}" alt="CgCgk台账">
      <div class="imgcap">▲ Cg/Cgk 台账页（VDA Type1）：1 件标准件连续测 50 次（次数可调）；结果在「Cg/Cgk 分析结果」页展示</div>
      <img class="img" src="{{IMG_12}}" alt="线性台账">
      <div class="imgcap">▲ 线性/偏移台账页：标准件数与每件次数可调（默认 5 件 × 12 次），「重新生成」按新参数展开录入矩阵</div>
      <img class="img" src="{{IMG_11}}" alt="GRR分析结果">
      <div class="imgcap">▲ GRR 分析结果页：展示 %GRR / NDC / 公差%GRR / 变差分解与判定；「待采集」行提供「去录入」快捷跳转取数页</div>
    </div>

    <!-- 八、样本管理 -->
    <div class="card" id="s8">
      <h2><span class="no">8</span>样本管理</h2>
      <p class="sub">为 GRR / KAPPA 分析准备样本组：样本需覆盖过程变差（低 / 中 / 高），参考值由更高等级测量设备测定并记录来源，保证可溯源。</p>
      <div class="step"><div class="n">1</div><div class="t"><b>新增样本组</b><span>填写样本组编号 / 名称，关联器具与计划，录入样本数与覆盖范围，登记参考值来源。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>查看明细 / 编辑</b><span>「查看明细」查看每个样本的参考值与状态；「编辑」调整样本与覆盖范围。</span></div></div>
      <img class="img" src="{{IMG_10}}" alt="样本管理">
      <div class="imgcap">▲ 样本管理：5 个样本组，覆盖低/中/高变差，参考值来源可追溯</div>
    </div>

    <!-- 九、仪表盘 -->
    <div class="card" id="s9">
      <h2><span class="no">9</span>仪表盘总览</h2>
      <div class="step"><div class="n">1</div><div class="t"><b>统计卡片</b><span>计量器具总数、30 天内到期校准、MSA 计划（分析任务）进行中/已归档、GRR/KAPPA 可接受率。</span></div></div>
      <div class="step"><div class="n">2</div><div class="t"><b>预警与进度</b><span>校准到期/逾期预警列表（点击进入校准管理）；MSA 计划执行进度表；计划分析类型分布（GRR/KAPPA/线性·偏移/稳定性/Cg·Cgk/分辨率/未定型）；定型率。</span></div></div>
      <div class="step"><div class="n">3</div><div class="t"><b>审计日志</b><span>最近动态记录所有关键操作（计划编制/定型、数据提交、审核、校准状态变更等），全程可追溯。</span></div></div>
      <img class="img" src="{{IMG_01}}" alt="仪表盘">
      <div class="imgcap">▲ 仪表盘：统计卡、校准预警、计划执行进度、分析类型分布、审计日志</div>
    </div>

    <!-- 十、业务规则 -->
    <div class="card" id="s10">
      <h2><span class="no">10</span>业务规则与防漏洞清单</h2>
      <table class="tbl">
        <tr><th>#</th><th>规则</th><th>位置/实现</th></tr>
        <tr><td>1</td><td>校准逾期器具自动预警并应停用，禁止选入新计划</td><td>台账校准状态列 / 创建弹窗勾选拦截</td></tr>
        <tr><td>2</td><td>同一器具存在未闭环计划（未定型/待采集/待审核/需整改）时禁止重复创建；已批准/已闭环/已关闭后可重新发起周期复评</td><td>instHasActivePlan 状态机</td></tr>
        <tr><td>3</td><td>检验标准定义在零件/工序上，创建/定型先选零件，标准限该零件适用；一个计划一个标准；GRR 与 KAPPA 标准不混用</td><td>创建弹窗 / 转 GRR·KAPPA 校验</td></tr>
        <tr><td>4</td><td>样本录入强制交叉型结构，提交前完整性校验，缺失即拦截</td><td>分析台账录入表单</td></tr>
        <tr><td>5</td><td>不合格分析必须关联纠正措施并经复测验证方可闭环</td><td>需整改 → 措施 → 闭环 状态机</td></tr>
        <tr><td>6</td><td>分析达终态（已批准/已闭环）自动回写器具「上次 MSA」，复评周期滚动</td><td>backfillMsa 闭环回写</td></tr>
        <tr><td>7</td><td>关闭计划同步关闭其全部六类台账记录，避免数据不一致</td><td>关闭计划逻辑（六数组全覆盖）</td></tr>
        <tr><td>8</td><td>所有关键操作写入审计日志，可追溯</td><td>logAction 审计日志</td></tr>
      </table>
    </div>

    <!-- 十一、速查表 -->
    <div class="card" id="s11">
      <h2><span class="no">11</span>速查表</h2>
      <h3>11.1 状态字典</h3>
      <table class="tbl">
        <tr><th>对象</th><th>状态</th><th>说明</th></tr>
        <tr><td rowspan="3">计划状态</td><td>待开始（未定型 / 待采集）</td><td>已建计划未定型，或已生成台账记录待录入</td></tr>
        <tr><td>进行中（待审核 / 需整改）</td><td>样本已提交待审核，或已退回整改</td></tr>
        <tr><td>已完成（已批准 / 已闭环 / 已关闭）</td><td>审核通过、整改闭环或人工关闭，之后器具可重新发起</td></tr>
        <tr><td rowspan="2">记录状态</td><td>待采集 / 待审核 / 需整改</td><td>未闭环</td></tr>
        <tr><td>已批准 / 已闭环 / 已关闭</td><td>终态（批准一次通过；闭环整改通过；关闭人工结束）</td></tr>
        <tr><td rowspan="2">校准状态</td><td>正常 / 临期（30 天内）</td><td>可用</td></tr>
        <tr><td>超期</td><td>应停用并安排校准</td></tr>
      </table>
      <h3>11.2 常用操作入口速查</h3>
      <table class="tbl">
        <tr><th>要做什么</th><th>入口</th></tr>
        <tr><td>维护器具组 / 样机属性</td><td>计量器具台账 → 上方器具组列表 / 下方器具明细（样机列）</td></tr>
        <tr><td>登记一台器具校准</td><td>校准管理 → ＋登记校准（或到期计划行内）</td></tr>
        <tr><td>新建一条检验标准</td><td>检验标准维护 → ＋新增标准</td></tr>
        <tr><td>给一台器具创建 MSA 计划</td><td>MSA 计划 → 创建MSA计划 → 选零件/标准/方法/器具组 → 确认</td></tr>
        <tr><td>把未定型计划定为 GRR/KAPPA</td><td>MSA 计划 → 勾选计划 → 转 GRR / 转 KAPPA</td></tr>
        <tr><td>录入 GRR 样本</td><td>台账 → GRR 台账 → 待采集行「录入数据」</td></tr>
        <tr><td>录入 KAPPA 判定</td><td>台账 → KAPPA 台账 → 待采集行「录入数据」</td></tr>
        <tr><td>审核一条分析</td><td>分析执行 → 对应分析结果页 → 详情/审核 → 审核通过 / 退回整改</td></tr>
        <tr><td>不合格整改</td><td>详情/审核 → ＋添加纠正措施 → 整改完成 · 复测验证 · 闭环</td></tr>
        <tr><td>查看器具复评提醒</td><td>计量器具台账明细「复评提醒」列；创建弹窗可按复评状态筛选</td></tr>
      </table>
      <div class="note">本手册界面截图取自系统演示数据（2026-09-08），仅用于说明操作位置与流程，不代表真实业务结果。</div>
    </div>

  </main>
</div>

<button class="toTop" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑ 顶部</button>
<script>
  // 目录高亮
  (function(){
    var links = Array.prototype.slice.call(document.querySelectorAll('.sider a'));
    var map = {};
    links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
    function mark(){
      var y = window.scrollY + 90, cur = 's1';
      Object.keys(map).forEach(function(id){
        var el = document.getElementById(id);
        if(el && el.offsetTop <= y) cur = id;
      });
      links.forEach(function(a){ a.className = (a.getAttribute('href').slice(1) === cur) ? 'on' : ''; });
    }
    window.addEventListener('scroll', mark, {passive:true});
    mark();
  })();
</script>
</body>
</html>
'''

for k, v in b64.items():
    html = html.replace('{{IMG_' + k.split('-')[0] + '}}', v)

out = os.path.join(BASE, 'MSA系统操作手册.html')
with io.open(out, 'w', encoding='utf-8') as fp:
    fp.write(html)
print('manual saved:', out, len(html)//1024, 'KB')
# 校验占位符是否全部替换
left = html.count('{{IMG_')
print('left placeholders:', left)
