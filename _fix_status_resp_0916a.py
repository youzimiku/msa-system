# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. 本地快照
snap = os.path.join(BASE, f'index_备份_{ts}_状态只读责任人改造前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()

EDITS = []

# A. MSA计划列表 状态列 -> 只读彩色标签
EDITS.append((
"""    {title:'状态', width:112, render:(_,r)=>{ const v=planStatusView(r.status); return <Select size="small" style={{width:98}} value={v.text} options={['待开始','进行中','已完成'].map(c=>({value:c,label:c}))} onChange={x=>{ const cand=STATUS_BACK[x]||[]; const cur=r.status; setF(r,'status', cand.indexOf(cur)>=0? cur : (x==='待开始'?'未定型':x==='已完成'?'已闭环':'待分析')); }}/>; }},""",
"""    {title:'状态', width:112, render:(_,r)=>{ const v=planStatusView(r.status); return <Tag color={v.color} style={{marginRight:0}}>{v.text}</Tag>; }},""", 1))

# B. MSA计划列表 分析人列 -> 责任人
EDITS.append((
"""    {title:'分析人', width:116, render:(_,r)=><Select size="small" value={r.analyst||r.observer||undefined} style={{width:106}} options={ANALYST_OPT} onChange={x=>setF(r,'analyst',x)}/>},""",
"""    {title:'责任人', width:116, render:(_,r)=><Select size="small" value={r.analyst||r.observer||undefined} style={{width:106}} options={ANALYST_OPT} onChange={x=>setF(r,'analyst',x)}/>},""", 1))

# C. 创建弹窗"计划填写信息"：分析人 label -> 责任人
EDITS.append((
"""<span className="flt-label">分析人 <b style={{color:'#cf1322'}}>*</b></span><Select size="small" style={{width:140}} placeholder="选择分析人" value={meta.analyst||undefined}""",
"""<span className="flt-label">责任人 <b style={{color:'#cf1322'}}>*</b></span><Select size="small" style={{width:140}} placeholder="选择责任人" value={meta.analyst||undefined}""", 1))

# D. 创建弹窗"计划填写信息"：删除责任人下拉（整行）
EDITS.append((
"""        <Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">责任人 <b style={{color:'#cf1322'}}>*</b></span><Select size="small" style={{width:140}} placeholder="选择责任人" value={meta.owner||undefined} options={['李工程师','王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'].map(c=>({value:c,label:c}))} onChange={v=>setMetaK('owner',v)}/></Col>
""", "", 1))

# E. 计划详情抽屉 分析人 -> 责任人
EDITS.append((
"""      {key:'analyst', label:'分析人', children:plan.analyst||plan.observer||'暂无'},""",
"""      {key:'analyst', label:'责任人', children:plan.analyst||plan.observer||'暂无'},""", 1))

# F. 编辑计划信息弹窗 Form 分析人 -> 责任人
EDITS.append((
"""<Col span={8}><Form.Item name="analyst" label="分析人"><Input/></Form.Item></Col>""",
"""<Col span={8}><Form.Item name="analyst" label="责任人"><Input/></Form.Item></Col>""", 1))

# G. 台账列表列 分析人 -> 责任人（3 处相同）
EDITS.append((
"""    {title:'分析人', dataIndex:'analyst', width:90},""",
"""    {title:'责任人', dataIndex:'analyst', width:90},""", 3))

# H. 台账详情 key 分析人 -> 责任人（3 处相同）
EDITS.append((
"""      {key:'分析人', label:'分析人', children:rec.analyst||'暂无'},""",
"""      {key:'责任人', label:'责任人', children:rec.analyst||'暂无'},""", 3))

# I. 台账查询条件 分析人 -> 责任人
EDITS.append((
"""<span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>分析人</span><Select allowClear style={{width:140}} value={fanl}""",
"""<span style={{marginRight:4,color:'#666666',fontSize:14,whiteSpace:'nowrap'}}>责任人</span><Select allowClear style={{width:140}} value={fanl}""", 1))

# J. 台账页面说明权限文案 分析人 -> 责任人
EDITS.append((
"①「查看全部台账」权限：可查看所有分析人的全部台账记录；",
"①「查看全部台账」权限：可查看所有责任人的全部台账记录；", 1))

# K. 注释统一
EDITS.append((
"// 分析人（观察员改分析人）/ 分辨力（文本录入，非分析方法）",
"// 责任人（观察员改责任人）/ 分辨力（文本录入，非分析方法）", 1))

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
    # 归档
    folder = os.path.join(BASE, 'backups', ts + '_状态只读责任人统一')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：状态列只读 + 责任人术语统一（2026-09-16）

## 改动清单（精确到位置）
1. MSA计划列表"状态"列：Select 下拉 → 只读彩色状态标签（待开始/进行中/已完成，不再可编辑）
2. MSA计划列表"分析人"列（analyst）→ 列名改"责任人"（控件、字段不变）
3. 创建MSA计划-器具/人员弹窗"计划填写信息"模块：
   - 删除"责任人"下拉框（meta.owner，创建时 owner 回落为当前登录人）
   - "分析人"（必填）label → "责任人"
4. 计划详情抽屉（PlanDetail）："分析人" → "责任人"
5. 编辑计划信息弹窗（PlanEditModal）：Form"分析人" → "责任人"
6. 台账页面（5 个台账）：列表列"分析人" → "责任人"（3 处）；详情"分析人" → "责任人"（3 处）；查询条件"分析人" → "责任人"（1 处）
7. 台账页面说明-权限说明："所有分析人" → "所有责任人"
8. 源码注释统一

## 说明
- 仅改显示文案与状态列控件，数据字段 analyst/owner 与交互逻辑不变
- 数据字段名保持 analyst（英文）不变，避免影响既有逻辑
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} MSA计划状态列只读；创建弹窗去责任人下拉、分析人改责任人；列表/详情/查询/权限说明全站'分析人'→'责任人'\n")
    print('已写回 + 归档:', folder)
