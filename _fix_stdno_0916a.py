# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_检验标准号字段前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. 检验标准列表（char页 stdCols）：操作列后新增只读"检验标准号"列（自动编号）
EDITS.append((
"""    {title:'操作', width:110, render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveStdRow(r)}>保存</Button>
      <Button size="small" type="link" danger disabled={stdRef(r)} onClick={()=>delStd(r)}>删除</Button>
    </Space>},
    {title:'检验标准', dataIndex:'basis', width:200, ellipsis:true, render:(_,r)=><Select size="small" showSearch optionFilterProp="label" style={{width:190}} placeholder="选择检验标准" value={r.basis||undefined} options={(d.standards||[]).map(s=>({value:s.id,label:(s.basis||s.name||s.id)}))} onChange={id=>{const st=(d.standards||[]).find(s=>s.id===id); setStdF(r,'basis',st?st.basis:id);}}/>},""",
"""    {title:'操作', width:110, render:(_,r)=><Space size={0}>
      <Button size="small" type="link" onClick={()=>saveStdRow(r)}>保存</Button>
      <Button size="small" type="link" danger disabled={stdRef(r)} onClick={()=>delStd(r)}>删除</Button>
    </Space>},
    {title:'检验标准号', dataIndex:'id', width:120, render:v=><span className="mono">{v}</span>},
    {title:'检验标准', dataIndex:'basis', width:220, ellipsis:true, render:(_,r)=><Input size="small" value={r.basis||''} onChange={e=>setStdF(r,'basis',e.target.value)}/>},""", 1))

# 2. MSA计划列表：被测参数列后新增只读"检验标准号/检验标准"两列
EDITS.append((
"""    {title:'被测参数', width:190, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); const cur=(r.instIds||[]).length>1? recs.map(x=>x.object).filter(Boolean).join('、') : (r.object||''); return <span>{cur||'—'}</span>; }},
    {title:'CG/CGK', width:68, align:'center', render:fenCell('cgcgk','CG/CGK')},""",
"""    {title:'被测参数', width:190, ellipsis:true, render:(_,r)=>{ const recs=planRecords(d,r.id); const cur=(r.instIds||[]).length>1? recs.map(x=>x.object).filter(Boolean).join('、') : (r.object||''); return <span>{cur||'—'}</span>; }},
    {title:'检验标准号', width:120, render:(_,r)=>{ const st=(d.standards||[]).find(x=>x.id===r.standard); return <span className="mono">{st?st.id:'—'}</span>; }},
    {title:'检验标准', width:200, ellipsis:true, render:(_,r)=>{ const st=(d.standards||[]).find(x=>x.id===r.standard); return <span>{st?(st.basis||st.name||''):'—'}</span>; }},
    {title:'CG/CGK', width:68, align:'center', render:fenCell('cgcgk','CG/CGK')},""", 1))

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
    folder = os.path.join(BASE, 'backups', ts + '_检验标准号字段')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：检验标准号字段（2026-09-16）

## 改动清单
1. 被测参数维护页面 · 检验标准列表：
   - 新增"检验标准号"列：显示系统自动编号（STD-MSA-xxx），纯文本只读，不可修改
   - "检验标准"列：控件由下拉框改为文本框（直接手输检验标准内容）
2. MSA计划页面 · MSA计划列表：
   - "被测参数"列后新增两列："检验标准号"、"检验标准"，均为只读
   - 取值：按计划关联的检验标准（plan.standard）从检验标准数据带出——检验标准号=标准自动编号、检验标准=标准内容（basis）；未关联显示"—"
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 检验标准列表新增只读检验标准号列、检验标准列改文本框；MSA计划列表被测参数后新增只读检验标准号/检验标准两列\n")
    print('已写回 + 归档:', folder)
