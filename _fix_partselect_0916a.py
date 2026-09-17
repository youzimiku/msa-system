# -*- coding: utf-8 -*-
import io, os, sys, datetime, difflib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
CUR = os.path.join(BASE, 'index.html')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

snap = os.path.join(BASE, f'index_备份_{ts}_零件号联动下拉前.html')
shutil.copy2(CUR, snap)

src = io.open(CUR, encoding='utf-8').read()
EDITS = []

# 1. 顶层新增 PART_PAIRS（零件号-零件名称 模拟映射）+ PartSelect 组件
EDITS.append((
"""const PARTNO_OPT = ['PN-1000','PN-1001','PN-1002','PN-1003','PN-1004','PN-1005','PN-1006','PN-1007','PN-2001','PN-3001','PN-4001','PN-5001'].map(v=>({value:v,label:v}));
const PARTNAME_OPT = ['轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴'].map(v=>({value:v,label:v}));""",
"""const PARTNO_OPT = ['PN-1000','PN-1001','PN-1002','PN-1003','PN-1004','PN-1005','PN-1006','PN-1007','PN-2001','PN-3001','PN-4001','PN-5001'].map(v=>({value:v,label:v}));
const PARTNAME_OPT = ['轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴'].map(v=>({value:v,label:v}));
/* 零件号↔零件名称 模拟映射（样本库/被测参数/MSA计划 联动选择共用） */
const PART_PAIRS=['PN-1000','PN-1001','PN-1002','PN-1003','PN-1004','PN-1005','PN-1006','PN-1007','PN-2001','PN-3001','PN-4001','PN-5001'].map((no,i)=>({no, name:['轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴','轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴'][i]}));
/* 零件号选择控件：下拉选项显示「零件号-零件名称」，可搜索零件号/名称；选中后只显示零件号并联动零件名称 */
function PartSelect({value, onChange, width}){
  const [open,setOpen]=useState(false);
  const [kw,setKw]=useState('');
  const list=PART_PAIRS.filter(p=>!kw||(p.no+p.name).toLowerCase().includes(kw.toLowerCase()));
  return <Popover trigger="click" open={open} onOpenChange={o=>{setOpen(o); if(o) setKw('');}} placement="bottomLeft" content={<div style={{width:240}}>
    <Input size="small" autoFocus allowClear placeholder="搜索零件号 / 零件名称" value={kw} onChange={e=>setKw(e.target.value)}/>
    <div style={{maxHeight:200,overflow:'auto',marginTop:4}}>
      {list.length===0? <div style={{padding:'6px 8px',color:'#999',fontSize:12}}>无匹配零件</div> : list.map(p=>(
        <div key={p.no} onClick={()=>{onChange(p.no,p.name); setOpen(false);}} style={{padding:'5px 8px',cursor:'pointer',borderRadius:4,fontSize:13,whiteSpace:'nowrap'}} onMouseEnter={e=>e.currentTarget.style.background='#f5f5f5'} onMouseLeave={e=>e.currentTarget.style.background=''}>{p.no}-{p.name}</div>
      ))}
    </div>
  </div>}>
    <Input size="small" readOnly value={value||''} placeholder="选择零件号" style={{width}} suffix={<span style={{fontSize:10,color:'#999'}}>▾</span>}/>
  </Popover>;
}""", 1))

# 2. applyFieldDefaults 内新增零件号映射常量（局部，避免 TDZ）
EDITS.append((
"""  const LINES=['1号线','2号线','3号线','4号线','5号线','6号线'];
  const PRODS=['压铸线','机加线','装配线','冲压线','热处理线','注塑线'];
  const PROCESSES=['下料','粗加工','精加工','装配','检验','包装'];
  const PLANTS=['青岛工厂','烟台工厂']; const SUBPLANTS=['一分厂','二分厂'];""",
"""  const LINES=['1号线','2号线','3号线','4号线','5号线','6号线'];
  const PRODS=['压铸线','机加线','装配线','冲压线','热处理线','注塑线'];
  const PROCESSES=['下料','粗加工','精加工','装配','检验','包装'];
  const PLANTS=['青岛工厂','烟台工厂']; const SUBPLANTS=['一分厂','二分厂'];
  const PARTMAP={'PN-1000':'轴类件','PN-1001':'孔类件','PN-1002':'标准件','PN-1003':'轴端盖','PN-1004':'壳体','PN-1005':'齿轮轴','PN-1006':'轴类件','PN-1007':'孔类件','PN-2001':'标准件','PN-3001':'轴端盖','PN-4001':'壳体','PN-5001':'齿轮轴'};""", 1))

# 3. sampleLib 兜底后：历史数据按映射补齐零件名称（plans/characteristics/sampleLib）
EDITS.append((
"""  if(!d.sampleLibLogs) d.sampleLibLogs=[];""",
"""  if(!d.sampleLibLogs) d.sampleLibLogs=[];
  /* 零件号↔零件名称：历史数据按映射补齐零件名称（与 PartSelect 联动同一映射） */
  (['plans','characteristics','sampleLib']).forEach(k=>{ (d[k]||[]).forEach(o=>{ if(o.partNo&&(!o.partName||o.partName==='—')){ const pn=PARTMAP[o.partNo]; if(pn) o.partName=pn; } }); });""", 1))

# 4. MSA计划列表：零件号 → PartSelect 联动；零件名称 → 纯文字
EDITS.append((
"""    {title:'零件号', width:110, dataIndex:'partNo', render:(_,r)=><Select size="small" value={r.partNo||undefined} style={{width:100}} options={PARTNO_OPT} onChange={x=>setF(r,'partNo',x)}/>},
    {title:'零件名称', width:120, dataIndex:'partName', render:(_,r)=><Select size="small" value={(r.partName&&r.partName!=='—')?r.partName:undefined} style={{width:110}} options={PARTNAME_OPT} onChange={x=>setF(r,'partName',x)}/>},""",
"""    {title:'零件号', width:110, dataIndex:'partNo', render:(_,r)=><PartSelect value={r.partNo} width={100} onChange={(no,name)=>{setF(r,'partNo',no); setF(r,'partName',name);}}/>},
    {title:'零件名称', width:120, dataIndex:'partName', render:(_,r)=><span>{r.partName||'—'}</span>},""", 1))

# 5. 被测参数列表 + 样本列表：零件号 → PartSelect 联动；零件名称 → 纯文字（两处相同写法）
EDITS.append((
"""    {title:'零件号', dataIndex:'partNo', width:110, render:(_,r)=><Select size="small" value={r.partNo||undefined} style={{width:100}} options={PARTNO_OPT} onChange={x=>setF(r,'partNo',x)}/>},
    {title:'零件名称', dataIndex:'partName', width:120, ellipsis:true, render:(_,r)=><Select size="small" value={r.partName||undefined} style={{width:110}} options={PARTNAME_OPT} onChange={x=>setF(r,'partName',x)}/>},""",
"""    {title:'零件号', dataIndex:'partNo', width:110, render:(_,r)=><PartSelect value={r.partNo} width={100} onChange={(no,name)=>{setF(r,'partNo',no); setF(r,'partName',name);}}/>},
    {title:'零件名称', dataIndex:'partName', width:120, ellipsis:true, render:(_,r)=><span>{r.partName||'—'}</span>},""", 2))

fail = False
for i, (old, new, exp) in enumerate(EDITS):
    cnt = src.count(old)
    if cnt != exp:
        print(f"[FAIL] #{i} 期望 {exp} 实际 {cnt} | old[:60]={old[:60]!r}")
        fail = True
    else:
        src = src.replace(old, new)
        print(f"[OK] #{i} 替换 {cnt} 处")

if fail:
    print('存在未匹配项，未写回')
else:
    io.open(CUR, 'w', encoding='utf-8', newline='').write(src)
    folder = os.path.join(BASE, 'backups', ts + '_零件号联动下拉')
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(CUR, os.path.join(folder, 'index.html'))
    md = """# 调整内容：零件号联动下拉（2026-09-16）

## 改动清单
1. 新增 PartSelect 零件号选择控件 + PART_PAIRS 零件号↔零件名称模拟映射：
   - 下拉选项显示「零件号-零件名称」（如 PN-1000-轴类件），可搜索零件号或零件名称
   - 选中收起后输入框只显示零件号
   - 选中后自动联动：把对应零件名称写入零件名称列
2. 三个页面列表统一应用：
   - 样本库管理 · 样本列表：零件号改 PartSelect 联动；零件名称列改为纯文字不可编辑
   - 被测参数维护 · 被测参数列表：同上
   - MSA计划 · 计划列表：同上
3. 历史数据补齐：applyFieldDefaults 中 plans/characteristics/sampleLib 已有零件号但零件名称为空或「—」的行，按映射自动补齐零件名称
"""
    io.open(os.path.join(folder, '调整内容.md'), 'w', encoding='utf-8').write(md)
    a = io.open(snap, encoding='utf-8').read().splitlines()
    b = io.open(CUR, encoding='utf-8').read().splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=os.path.basename(snap), tofile='index.html', lineterm=''))
    io.open(os.path.join(folder, '调整内容.diff.txt'), 'w', encoding='utf-8').write('\n'.join(diff))
    cl = os.path.join(BASE, 'backups', 'CHANGELOG.md')
    io.open(cl, 'a', encoding='utf-8').write(f"- {ts} 三个页面零件号改联动下拉（选项显零件号-零件名称、可搜索、选中只显零件号并联动名称），零件名称列改纯文字\n")
    print('已写回 + 归档:', folder)
