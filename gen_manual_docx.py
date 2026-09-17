# -*- coding: utf-8 -*-
"""生成 MSA 系统操作手册（本地 Word）"""
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\MSA系统操作手册.docx"
doc = Document()

# 页面设置 A4 边距 2.5cm
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2.5)

HEI, SONG, ARIAL = "黑体", "宋体", "Arial"

def set_run(run, font=SONG, size=12, bold=False, color=RGBColor(0, 0, 0)):
    run.font.name = ARIAL
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color

def para(text="", font=SONG, size=12, bold=False, align=None, indent=True, space_after=0, line=1.5):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    if indent:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    p.paragraph_format.space_after = Pt(space_after)
    if line:
        p.paragraph_format.line_spacing = line
    if text:
        set_run(p.add_run(text), font, size, bold)
    return p

def h1(text):
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    set_run(p.add_run(text), HEI, 16, True)
    return p

def h2(text):
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(5)
    set_run(p.add_run(text), HEI, 14, True)
    return p

def h3(text):
    p = doc.add_paragraph(style="Heading 3")
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(4)
    set_run(p.add_run(text), HEI, 12, True)
    return p

def bullet(text, bold_head=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing = 1.5
    if bold_head:
        set_run(p.add_run(bold_head), SONG, 12, True)
    set_run(p.add_run(text), SONG, 12, False)
    return p

def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), color)
    tcPr.append(shd)

def fill_cell(cell, text, bold=False, size=10.5, fill=None, center=True):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    set_run(p.add_run(text), SONG, size, bold)
    if fill:
        shade(cell, fill)

def table(headers, rows, widths=None, size=10.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, htxt in enumerate(headers):
        fill_cell(t.rows[0].cells[j], htxt, bold=True, fill="D9D9D9", size=size)
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            fill_cell(cells[j], str(v), size=size, center=(j == 0 or len(str(v)) <= 12))
    if widths:
        for j, w in enumerate(widths):
            for r in t.rows:
                r.cells[j].width = Cm(w)
    return t

# 页脚页码
def add_page_number():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    set_run(run, SONG, 9)

def add_toc():
    p = doc.add_paragraph()
    run = p.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = 'TOC \\o "1-2" \\h \\z \\u'
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "（在 Word 中打开文档或按 F9 更新目录）"
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2); run._r.append(t); run._r.append(f3)
    # 打开时自动更新域
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
    settings.append(uf)

# ================= 封面 =================
p = para("MSA 测量系统分析管理系统", HEI, 18, True, WD_ALIGN_PARAGRAPH.CENTER, indent=False, space_after=6)
para("操 作 手 册", HEI, 16, True, WD_ALIGN_PARAGRAPH.CENTER, indent=False, space_after=6)
para("从零上手 · 标准操作动线", SONG, 12, False, WD_ALIGN_PARAGRAPH.CENTER, indent=False, space_after=6)
para("适用于质量工程师、检验员、计量管理员", SONG, 12, False, WD_ALIGN_PARAGRAPH.CENTER, indent=False)
doc.add_page_break()

# ================= 目录 =================
h1("目  录")
add_toc()
doc.add_page_break()

# ================= 1 手册说明 =================
h1("1  手册说明与使用路线")
para("本手册面向从未接触过 MSA（测量系统分析）的人员。阅读并照做本手册，即可从零开始完成一次完整的 MSA 分析：从维护基础数据、创建 MSA 计划开始，经过定型生成台账、设置操作人、录入样本数据、手动分析、审核闭环，直到计划完成归档。")
h2("1.1  系统能做什么")
para("本系统覆盖 MSA 的五性一力（重复性、再现性、偏倚、线性、稳定性）与 Cg/Cgk 共 6 类分析方法，支持计量型（GRR、线性/偏移、稳定性、Cg/Cgk）与计数型（KAPPA）分析；按“特性驱动（从 CP 同步特殊特性）+ 量具驱动（按台账校准周期与风险等级）”两层逻辑生成 MSA 计划；一个计划可对应多个分析方法（分计划），台账生成后经历“待采集→待分析→待审核→已批准/需整改→已闭环”的完整状态流转。")
h2("1.2  本手册怎么用")
bullet("第一次使用：按第 4 章准备好基础数据，再按第 5 章的 8 步动线走完一次完整分析；", "新手：")
bullet("日常使用：查第 6 章各页面操作速查、第 7 章判定准则速查；", "有经验后：")
bullet("遇到异常：查第 8 章常见问题。", "出问题时：")
h2("1.3  一次完整闭环的 8 步总览")
bullet("打开系统（浏览器打开 index.html）", "第 0 步 ")
bullet("创建 MSA 计划：选零件、选检验标准（自动带出取样参数）、勾分析方法与器具", "第 1 步 ")
bullet("计划定型，自动生成台账“待采集”记录", "第 2 步 ")
bullet("在台账中设置操作人 / 测量对象", "第 3 步 ")
bullet("录入样本实测值（手动矩阵或 Excel 导入）", "第 4 步 ")
bullet("保存后手动触发分析，系统按判定准则出结论", "第 5 步 ")
bullet("审核：通过、退回整改或完成闭环", "第 6 步 ")
bullet("MSA 计划页查看判定结果汇总，计划完成", "第 7 步 ")

# ================= 2 系统与角色 =================
h1("2  系统与角色")
h2("2.1  打开方式与界面布局")
para("用浏览器打开系统主页（演示环境为本地 index.html）。页面左侧是功能菜单，自上而下分为：基础数据维护（计量器具台账、校准管理、检验标准维护、质量特性维护、抽样方法维护、样本管理、样本库管理）、MSA 计划、五类台账（GRR/KAPPA/线性偏移/稳定性/CgCgk）、五类数据录入、五类分析结果。顶部为系统标题与当前用户。")
h2("2.2  角色权限")
para("演示环境当前角色为质量工程师（李工程师），可执行创建计划、录入数据、手动分析、提交审核等全部日常操作；审核动作由评审角色完成（演示数据中已内置若干已批准/需整改记录供查看）。")
h2("2.3  演示数据")
para("系统内置计量器具 11 台、检验标准 6 条、质量特性、抽样方法、样本与各台账演示数据。首次打开自动写入浏览器本地存储（localStorage），操作结果会持久化；如需恢复初始演示数据，清除浏览器该站点数据后重新打开即可。注意：请勿多开页面同时操作，多标签页可能互相覆盖演示数据。")

# ================= 3 术语速查 =================
h1("3  MSA 术语速查")
table(
    ["术语", "含义"],
    [
        ["GRR（重复性与再现性）", "同一量具多位操作员多次测量同批样本，评估测量系统重复性与再现性变差占比"],
        ["KAPPA（一致性分析）", "计数型（合格/不合格判定）分析，评估检验员判定与参考值的一致性"],
        ["偏倚（Bias）", "测量平均值与参考值（真值）的差值"],
        ["线性（Linearity）", "偏倚在量程范围内的变化情况"],
        ["稳定性（Stability）", "测量系统随时间（跨日/跨周）保持恒定的能力"],
        ["Cg / Cgk", "量具能力指数：Cg 反映重复性，Cgk 综合重复性与偏倚（VDA 方法）"],
        ["NDC（可区分类别数）", "测量系统能区分的零件类别数，GRR 判定指标之一"],
        ["真值 / 参考值", "样本的真实量值，来自标准件、计量校准或专家仲裁"],
        ["待采集", "台账已生成，等待录入实测数据"],
        ["待分析", "数据已录入保存，等待执行分析"],
        ["待审核", "分析完成，等待审核人确认"],
        ["已批准 / 需整改", "审核通过；或退回整改（可添加纠正措施）"],
        ["已闭环", "整改完成复测并最终确认"],
    ],
    widths=[5.0, 11.0],
)

# ================= 4 基础数据准备 =================
h1("4  使用前的基础数据准备")
para("以下 5 个页面是 MSA 的“地基”，首次使用前先确认数据齐备；演示环境已内置示例，可先直接进入第 5 章。")
h2("4.1  计量器具台账")
para("维护所有量具：编号、名称、型号、测量范围、分辨率、精度、校准状态、校准时间与下次校准、是否做 MSA、是否样机、所属器具组等。只有“在用/待校准”且“无未闭环计划”的器具可纳入新 MSA 计划；计划页会校验，避免重复生成。")
h2("4.2  抽样方法维护")
para("维护分析方法代码（GRR/KAPPA/LINEAR/BIAS/STABILITY/CGCGK）与取样规则。默认取样速查：GRR 10 件×3 人×3 次；KAPPA 50 件×3 人×3 次；线性 5 个标准件×12 次（覆盖量程）；稳定性 25 个子组×5 次（跨 4 周~3 个月）；Cg/Cgk 标准件连续测量 50 次。规则为三级继承：抽样方法规则 → 检验标准 → 计划行内可调。")
h2("4.3  检验标准维护")
para("维护检验项目（零件/工序/标准依据/检验方法/测量人数/测量次数/样本数量/分辨率/单位/标准值/目标上下限/分析类型/关联质量特性等）。创建 MSA 计划选择检验标准后，系统自动带出测量人数、测量次数、样本数量，可在计划中修改。")
h2("4.4  质量特性维护")
para("维护质量特性（编号/名称/特性类型 SC/CC/普通/所属零件/工序/特性类别 计量型或计数型/单位/标准值/USL/LSL/来源/关联检验标准）。SC/CC 特殊特性用于“特性驱动层”自动生成 MSA 计划。")
h2("4.5  样本库与样本管理")
para("样本库管理维护标准件与生产件的真值（参考值/单位/上下限/来源/有效期），供偏倚、线性、Cg/Cgk 等分析引用；样本管理维护一次分析实际使用的样本组（关联器具与计划、参考值来源、覆盖范围）。")

# ================= 5 标准操作动线 =================
h1("5  标准操作动线（从零开始做一次 MSA）")
para("本章以一个完整示例贯穿：用数显卡尺（编号 JJQ-2024-001）对“轴径 φ50±0.05”这一测量特性做一次 GRR 分析。其他分析方法在第 5.8 节说明差异。")
h2("5.1  第 0 步：打开系统")
para("浏览器打开系统首页，确认左侧菜单完整、右上角显示当前用户“李工程师”。")
h2("5.2  第 1 步：创建 MSA 计划")
para("点击“MSA 计划”菜单，进入计划页，点击“创建 MSA 计划”按钮，在弹出的创建窗口中按顺序操作：")
bullet("选择器具筛选条件（复评状态、厂商、型号、产线、工序、部门），点查询，下方器具列表出现可选量具；器具列表显示量具编号、名称、型号、范围、分辨率、精度、是否样机、部门、上次 MSA、校准状态、复评提醒、状态及每台器具的测量对象、人数、次数、样本数、责任人；", "第一步 ")
bullet("填写计划信息：零件/工序、检验标准（选择 STD-MSA-001 后自动带出测量人数 3、测量次数 3、样本数量 10，可修改）、质量特性、触发依据、计划检期、部门、零件号；质检区划、工厂、分厂自动带出；分析人单选；分辨力按文本填写；", "第二步 ")
bullet("勾选分析方法（本示例勾选 GRR；可多选，一个计划可对应多个分析方法）；", "第三步 ")
bullet("勾选器具列表中的卡尺（JJQ-2024-001）；", "第四步 ")
bullet("点击确定创建。", "第五步 ")
para("创建后计划状态为“待开始”，计划行显示分析人、器具、零件、特性、检验标准、取样参数等关键信息。")
h2("5.3  第 2 步：定型并生成台账")
para("若创建时未勾选分析方法，计划类型为空（未定型），可在计划列表操作列执行定型（转 GRR / 转 KAPPA 等）。定型后系统自动在对应台账生成一条“待采集”记录。示例：进入左侧“台账 → GRR 台账”，可看到该计划对应的 GRR 记录，状态为“待采集”，取样规则显示“3 人×3 次×10 件”。")
h2("5.4  第 3 步：设置操作人与测量对象")
para("在 GRR 台账行内点击“操作人”，多选实际参与测量的操作员（GRR/KAPPA 选人；线性/偏移选件；稳定性选标准件、人、工位；Cg/Cgk 选件与人，详见 5.8 差异表）。")
h2("5.5  第 4 步：录入样本实测值")
para("在 GRR 台账行内点击“录入数据”，进入录入页。系统按人数×次数×件数自动生成操作员×样本×试验的交叉矩阵，测量人员按盲测方式录入（系统默认隐藏操作员与样本序号等干扰信息，可按需关闭隐藏）。")
para("也可点击“导入”用 Excel 批量导入样本录入结果：选择本地 xlsx 文件，先预览确认，再写入台账。录入完成后点击保存，记录状态变为“待分析”。")
h2("5.6  第 5 步：手动分析")
para("样本录入/导入完成后，需手动执行分析：在台账行内或分析结果页点击“手动分析”（或“查看结果”）。系统自动计算 %GRR、NDC、公差 %GRR，并按判定准则给出结论（可接受/有条件接受/不可接受）。确认后点击“提交审核”，状态变为“待审核”。")
h2("5.7  第 6 步：审核与整改闭环")
para("进入对应“分析结果”页，打开记录“详情/审核”：")
bullet("审核人确认分析结果与判定结论；", "审核通过：")
bullet("系统要求填写整改措施（如重新校准、检修量具、培训操作员），措施完成后可发起复测，复测通过后记录“已闭环”；", "退回整改：")
bullet("可在操作记录中查看完整时间线与纠正措施。", "追溯：")
h2("5.8  第 7 步：计划完成与判定汇总")
para("回到“MSA 计划”页，选中该计划，下方展示该计划的各分析单（分计划）行信息；列表的“判定结果”按当前计划分析单的结论汇总显示一个结果，检验标准相同只显示一个。计划全部分析单闭环后，计划状态完成。")
h2("5.9  其他四种分析方法与 GRR 的差异")
table(
    ["分析方法", "默认取样", "台账操作人/对象规则", "关键判定"],
    [
        ["KAPPA（计数型）", "50 件×3 人×3 次", "选人（多选）", "Kappa>0.75；有效性/错误率/错误报警率"],
        ["线性/偏移", "5 标准件×12 次（覆盖量程）", "选件（多选）", "线性回归+偏倚 t 检验，4 种情形判定"],
        ["稳定性", "25 子组×5 次（跨 4 周~3 个月）", "选标准件+选人+选工位（均多选）", "均值-极差控制图 SPC 判异"],
        ["Cg/Cgk", "标准件连续测量 50 次", "选件+选人（均多选）", "Cg、Cgk≥1.33；6σ/T≤15% 优秀、≤20% 可接受"],
    ],
    widths=[3.2, 4.4, 4.0, 4.4],
)

# ================= 6 功能页速查 =================
h1("6  各功能页操作速查")
table(
    ["页面", "主要操作", "入口"],
    [
        ["计量器具台账", "新增/编辑/删除器具、登记校准、状态变更", "左侧菜单：计量器具台账"],
        ["校准管理", "登记校准记录、查看到期统计", "左侧菜单：校准管理"],
        ["检验标准维护", "新增/修订检验标准（含判定准则）", "左侧菜单：检验标准维护"],
        ["质量特性维护", "新增/编辑/停用特性", "左侧菜单：质量特性维护"],
        ["抽样方法维护", "维护分析方法代码、取样规则、判断规则（页签）", "左侧菜单：抽样方法维护"],
        ["样本管理", "新增样本组、查看样本明细", "左侧菜单：样本管理"],
        ["样本库管理", "维护标准件/生产件真值", "左侧菜单：样本库管理"],
        ["MSA 计划", "创建/编辑/详情/删除计划；选中计划查看分析单列表", "左侧菜单：MSA 计划"],
        ["GRR 台账等五台账", "设置操作人/对象、录入数据、导入、查看结果、审核", "左侧菜单：台账"],
        ["数据录入", "矩阵/表格录入、修改实测值", "左侧菜单：录入数据（或台账行内进入）"],
        ["分析结果", "手动分析、详情审核、整改闭环", "左侧菜单：分析执行"],
    ],
    widths=[3.6, 7.0, 5.4],
)

# ================= 7 判定准则 =================
h1("7  判定准则速查")
h2("7.1  GRR")
table(
    ["判定项", "阈值", "结论"],
    [
        ["NDC", "≥ 5", "接受"],
        ["%GRR", "< 10%", "可接受"],
        ["%GRR", "10% ~ 30%", "可接受或不接受（有条件）"],
        ["%GRR", "> 30%", "不能接受"],
    ],
    widths=[2.8, 4.6, 8.6],
)
h2("7.2  KAPPA（计数型）")
table(
    ["判定项", "阈值", "结论"],
    [
        ["Kappa", "> 0.75", "满足要求"],
        ["有效性", "正确决定次数 / 总决定次数", "评估检验能力"],
        ["错误率 / 错误报警率", "按判定矩阵计算", "评估误判风险"],
    ],
    widths=[2.8, 5.4, 7.8],
)
h2("7.3  线性 + 偏倚")
table(
    ["情形", "结论"],
    [
        ["偏倚 0 水平线完全在置信区间内，各点平均偏倚均在区间内", "非常理想，可接受"],
        ["若干点出区间，常量显著≠0、斜率不显著", "固定偏倚，易纠偏，理想可接受"],
        ["回归效果显著（斜率≠0），各点平均偏倚均在区间内", "线性偏倚，可按回归修正，较理想可接受"],
        ["不能拒绝斜率为 0，且若干点平均偏倚出区间且位于不同侧", "有偏倚且无法修正，不能接受"],
    ],
    widths=[9.6, 6.4],
)
h2("7.4  Cg / Cgk")
table(
    ["情形", "结论"],
    [
        ["Cg、Cgk 均 ≥ 1.33", "能力充足，可用于日常检验与量产判定"],
        ["Cg 偏小", "重复性差，需检修/清洁/更换量具或提升装夹稳定性"],
        ["Cg 合格、Cgk 偏小", "存在系统性偏倚，需重新校准、修正补偿、核对标准件真值"],
        ["Cgk 为负数", "偏倚超出 10% 公差，量具不可使用，立即整改复测"],
        ["重复性误差占比 6σ/T", "≤15% 优秀；≤20% 可接受"],
    ],
    widths=[6.4, 9.6],
)
h2("7.5  稳定性")
para("以均值-极差控制图（Xbar-R）判定：无出界点、无异常规则即过程稳定，可接受；出现判异信号需查明原因（漂移、磨损、环境等）后复测。")

# ================= 8 常见问题 =================
h1("8  常见问题与提示")
table(
    ["问题", "处理方式"],
    [
        ["计划删除不了", "只有“待开始”状态的计划可删除；进入执行阶段后仅可修改基本信息"],
        ["计划创建后还能改什么", "只能修改基本信息（零件、标准、计划检期等），分析方法与台账按创建时定型"],
        ["实测值录错了", "待分析状态可直接修改；已提交审核需先退回再修改"],
        ["导入 Excel 报错", "使用系统要求的 xlsx 模板（列与台账字段一致），先预览确认再写入"],
        ["台账行“操作人”为何不能选人", "不同台账规则不同：GRR/KAPPA 选人；线性/偏移选件；稳定性选标准件+人+工位；Cg/Cgk 选件+人"],
        ["状态显示为“待采集”", "台账已生成、等待录入数据，录入并保存后进入“待分析”"],
        ["数据会不会丢", "演示环境数据保存在浏览器 localStorage；多开标签页会互相覆盖，请单页使用；清除站点数据可恢复初始演示数据"],
        ["样机标注", "器具列表“样机”列标注哪些器具是样机，样机参与分析时系统正常处理"],
        ["判定结果汇总", "MSA 计划列表的判定结果按当前计划分析单的结论汇总为一个；检验标准相同只显示一个标准"],
    ],
    widths=[5.6, 10.4],
)

add_page_number()

# 修正 Heading 颜色为黑色（样式级）
for hs in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
    try:
        st = doc.styles[hs]
        st.font.color.rgb = RGBColor(0, 0, 0)
    except Exception:
        pass
# Normal 基础
n = doc.styles["Normal"]
n.font.name = ARIAL
n._element.rPr.rFonts.set(qn("w:eastAsia"), SONG)
n.font.size = Pt(12)

doc.save(OUT)
print("saved", OUT)
