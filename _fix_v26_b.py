# -*- coding: utf-8 -*-
"""Step2：需求1 所有状态/结论加 Tooltip 悬停说明"""
import io, re

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# 1) 插入 TIPS 字典（放在 roleOptions 定义结束后）
anchor = "{value:'viewer', label:'只读(评审/查看)'}\n  ]\n};"
tips = anchor + """
const TIPS = {
  status: {'待采集':'台账记录已生成，等待录入样本/测量数据','待审核':'数据已提交，等待审核员审核','已批准':'审核通过，结论生效并回写计划/器具','需整改':'审核退回，需添加纠正措施并复测','已闭环':'纠正措施完成、复测通过，已归档','已关闭':'人工关闭归档','在用':'可正常使用','待校准':'已到/即将到校准周期','送检中':'正在送检','封存':'封存保管，暂停使用','停用':'暂停使用，需整改后启用','报废':'已报废'},
  verdict: {'可接受':'测量系统能力合格，可用于日常检验与量产判定','有条件接受':'能力处于边缘，需结合过程能力/公差评估后批准','不可接受':'能力不足，必须整改后重新分析','待采集':'样本未录完，尚无分析结论','优秀(可接受)':'各项指标显著优于阈值，可接受','良好(有条件接受)':'处于边缘档，需评估后批准','优秀':'测量系统能力合格','良好':'处于边缘，需评估后批准'},
  plan: {'待开始':'计划已创建/已定型，等待采集样本','进行中':'样本采集中或结论审核中','已完成':'计划已闭环归档'},
  calib: {'正常':'在检定/校准周期内','临期':'距校准到期不足30天，请安排送检','超期':'已超过校准日期，应停用并送检'},
  sample: {'已测量':'该样本已完成测量','待测量':'该样本等待测量','已作废':'该样本已作废'}
};"""
n = s.count(anchor)
assert n == 1, ('anchor', n)
s = s.replace(anchor, tips)

# 2) StatusTag 包 Tooltip
old_st = "function StatusTag({s}){ return <Tag color={ENUM.statusColor[s]||'default'}>{s}</Tag>; }"
n = s.count(old_st)
if n == 0:
    # 可能带 style
    m = re.search(r"function StatusTag\(\{s\}\)\{ return <Tag color=\{ENUM\.statusColor\[s\]\|\|'default'\}[^>]*>\{s\}</Tag>; \}", s)
    old_st = m.group(0) if m else old_st
    n = s.count(old_st)
assert n == 1, ('StatusTag', n, old_st[:80])
s = s.replace(old_st, "function StatusTag({s}){ return <Tooltip title={TIPS.status[s]||s}><Tag color={ENUM.statusColor[s]||'default'}>{s}</Tag></Tooltip>; }")

# 3) VerdictTag 包 Tooltip + '-'->待采集
old_vt = "function VerdictTag({v}){ return <Tag color={verdictColor(v)} className=\"spec-tag\">{v}</Tag>; }"
n = s.count(old_vt)
if n == 0:
    m = re.search(r"function VerdictTag\(\{v\}\)\{[^}]*\}", s)
    old_vt = m.group(0) if m else old_vt
    n = s.count(old_vt)
assert n == 1, ('VerdictTag', n, old_vt[:80])
s = s.replace(old_vt, "function VerdictTag({v}){ const vv=(!v||v==='-')?'待采集':v; return <Tooltip title={TIPS.verdict[vv]||TIPS.verdict[v]||vv}><Tag color={verdictColor(vv)} className=\"spec-tag\">{vv}</Tag></Tooltip>; }")

# 4) 计划状态 Tag（PlanPage 列表与详情）
# 列表
old_p = "return <Tag color={v.color} className=\"spec-tag\" style={{\" + TAGW + \"}}>{v.text}</Tag>"
# 实际样式是 v2.5 写死的，用正则找 planStatusView 渲染
m = re.search(r"\{const v=planStatusView\(r\.status\); return <Tag[^>]*>\{v\.text\}</Tag>;\}", s)
if m:
    seg = m.group(0)
    new_seg = seg.replace("<Tag", "<Tooltip title={TIPS.plan[v.text]||v.text}><Tag", 1).replace("</Tag>;}", "</Tag></Tooltip>;}", 1)
    s = s.replace(seg, new_seg)
    print('OK 计划列表状态 Tag')
else:
    print('WARN 计划列表状态 Tag 未匹配')

# 5) 校准状态 Tag（2 处：台账 + 创建弹窗）—— 包裹 Tooltip
old_c = "<Tag color=\"volcano\">超期</Tag>"
n = s.count(old_c)
assert n == 2, ('calib超期', n)
s = s.replace(old_c, "<Tooltip title={TIPS.calib['超期']}><Tag color=\"volcano\">超期</Tag></Tooltip>")
old_l = "<Tag color=\"orange\">临期</Tag>"
n = s.count(old_l)
assert n == 2, ('calib临期', n)
s = s.replace(old_l, "<Tooltip title={TIPS.calib['临期']}><Tag color=\"orange\">临期</Tag></Tooltip>")
old_n = "<Tag style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>正常</Tag>"
n = s.count(old_n)
assert n == 2, ('calib正常', n)
s = s.replace(old_n, "<Tooltip title={TIPS.calib['正常']}><Tag style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>正常</Tag></Tooltip>")

# 6) 样本状态 Tag（列表）
old_s1 = "render:s=><Tag color={s==='已测量'?'green':s==='待测量'?'orange':'default'} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{s}</Tag>"
n = s.count(old_s1)
assert n == 1, ('sample列表', n)
s = s.replace(old_s1, "render:s=><Tooltip title={TIPS.sample[s]||s}><Tag color={s==='已测量'?'green':s==='待测量'?'orange':'default'} style={{display:'inline-flex',justifyContent:'center',minWidth:78,marginRight:0,textAlign:'center'}}>{s}</Tag></Tooltip>")

# 7) 样本详情 Drawer Tag
old_s2 = "<Tag color={detail.status==='已测量'?'green':'orange'}>{detail.status}</Tag>"
n = s.count(old_s2)
assert n == 1, ('sample详情', n)
s = s.replace(old_s2, "<Tooltip title={TIPS.sample[detail.status]||detail.status}><Tag color={detail.status==='已测量'?'green':'orange'}>{detail.status}</Tag></Tooltip>")

io.open(P, 'w', encoding='utf-8').write(s)
print('saved delta:', len(s)-len(orig))
