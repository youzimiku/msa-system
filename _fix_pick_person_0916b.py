# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global t
    assert t.count(old) == 1, ('锚点不唯一或不存在: %s...' % old[:70])
    t = t.replace(old, new)

# 1) 删 OPS 常量行
rep("  const OPS=['王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'];\n", "")

# 2) selP 改为 empNo 数组（兼容旧已选按姓名反查）
rep("  const [selP,setSelP]=useState(picked&&picked.ops?picked.ops:[]);",
    "  const [selP,setSelP]=useState(picked&&picked.ops? picked.ops.map(n=>{const p=(d.personnel||[]).find(x=>x.name===n); return p?p.empNo:null;}).filter(Boolean) : []);")

# 3) onOk：人员按 empNo 反查姓名数组传出
rep("      const chosenSamples=samples.filter(s=>selS.includes(s.id)); onOk(chosenSamples, selP); toast.ok('已选择 '+chosenSamples.length+' 个样本、'+selP.length+' 名人员'); }}",
    "      const chosenSamples=samples.filter(s=>selS.includes(s.id));\n      const chosenOps=(d.personnel||[]).filter(x=>selP.includes(x.empNo)).map(x=>x.name);\n      onOk(chosenSamples, chosenOps); toast.ok('已选择 '+chosenSamples.length+' 个样本、'+chosenOps.length+' 名人员'); }}")

# 4) 第二步：Tag 点选 → 多选列表（人员编号/姓名/部门/岗位）
rep("""    <div style={{marginBottom:8,fontSize:14,color:'#333333'}}>第二步：选择操作/分析人员（可多选）</div>
    <Space wrap>
      {OPS.map(n=>{ const on=selP.includes(n); return <Tag key={n} color={on?'blue':'default'} style={{cursor:'pointer',padding:'3px 12px',fontSize:13}} onClick={()=>setSelP(on?selP.filter(x=>x!==n):[...selP,n])}>{n}</Tag>; })}
    </Space>""",
    """    <div style={{marginBottom:8,fontSize:14,color:'#333333'}}>第二步：选择操作/分析人员（可多选）</div>
    <Table size="small" rowKey="empNo" dataSource={(d.personnel||[])} pagination={{pageSize:5,showTotal:t=>'共 '+t+' 人'}} scroll={{y:170}}
      rowSelection={{selectedRowKeys:selP, onChange:setSelP}}
      columns={[
        {title:'人员编号', dataIndex:'empNo', width:90},
        {title:'姓名', dataIndex:'name', width:90},
        {title:'部门', dataIndex:'dept', width:120},
        {title:'岗位', dataIndex:'postName', width:120}
      ]}/>""")

io.open(P, 'w', encoding='utf-8').write(t)
print('替换完成', len(t))
