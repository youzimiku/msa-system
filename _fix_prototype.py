# -*- coding: utf-8 -*-
"""去除「默认器具」概念，统一为「样机」属性：
- 器具组不再维护默认器具（去掉组表单字段/校验/列/排序/日志）
- 器具明细保留样机列；创建MSA计划时默认勾选组内样机器具"""
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, ('MISS %r -> %d (want %d)' % (old[:70], n, cnt))
    s = s.replace(old, new)

# A. 器具组列表：默认器具两列 -> 样机列
rep("""    {title:'默认器具编号', width:120, render:(_,g)=><span className="mono">{g.defaultInstId||'-'}</span>},
    {title:'默认器具名称', width:150, render:(_,g)=>{ const it=d.instruments.find(i=>i.id===g.defaultInstId); return it?it.name:'-'; }},
""",
"""    {title:'样机', width:150, render:(_,g)=>{ const ps=(g.memberIds||[]).filter(id=>(d.instruments.find(i=>i.id===id)||{}).prototype==='是'); return ps.length? <span className="tiny">{ps.map(id=>id).join('、')}</span> : <span className="tiny">—</span>; }},
""")

# B. 明细排序：样机优先
rep("""    .sort((a,b)=>{ const g=d.instGroups.find(x=>x.id===effGroup); if(!g||!g.defaultInstId) return 0; return (a.id===g.defaultInstId?-1:0)-(b.id===g.defaultInstId?-1:0); });""",
"""    .sort((a,b)=>{ const g=d.instGroups.find(x=>x.id===effGroup); if(!g) return 0; const aP=((d.instruments.find(x=>x.id===a.id)||{}).prototype==='是')?1:0; const bP=((d.instruments.find(x=>x.id===b.id)||{}).prototype==='是')?1:0; return bP-aP; });""")

# C. 删除器具：去掉 defaultInstId 处理（该行内联在长行中，用片段匹配）
rep("; if(g.defaultInstId===r.id) g.defaultInstId=g.memberIds[0]||'';", ";")

# D. 明细列表去掉「是否默认器具」列
rep("""    {title:'是否默认器具', width:100, render:(_,r)=><span>{d.instGroups.some(g=>g.defaultInstId===r.id)?<Tag color="blue">是</Tag>:'否'}</span>},
""", "")

# E/F. 台账页说明文字
rep("""<span className="tiny">查询 / 重置 对所有列表生效；一级按钮在下方各自列表区。台账页分为上「器具组列表」、下「器具明细列表」：器具组维护组与默认器具；器具明细维护每台器具，并标注所属器具组 / 是否默认器具。</span>""",
"""<span className="tiny">查询 / 重置 对所有列表生效；一级按钮在下方各自列表区。台账页分为上「器具组列表」、下「器具明细列表」：器具组维护组与成员；器具明细维护每台器具，并标注所属器具组 / 样机标记。</span>""")
rep("""<span className="tiny">为组配置成员器具并指定「默认器具」；创建 MSA 计划时先选器具组，系统拉出该组全部器具并默认选中默认器具。</span>""",
"""<span className="tiny">为组配置成员器具；创建 MSA 计划时先选器具组，系统拉出该组全部器具并默认选中样机器具。</span>""")

# G. 组表单回填去掉 defaultInstId
rep("""form.setFieldsValue({ id:value.id||('G-'+String(d.instGroups.length+1).padStart(2,'0')), name:value.name||'', defaultInstId:value.defaultInstId||'', note:value.note||'' });""",
"""form.setFieldsValue({ id:value.id||('G-'+String(d.instGroups.length+1).padStart(2,'0')), name:value.name||'', note:value.note||'' });""")

# G2. 删除 memInsts 定义（仅用于默认器具选择）
rep("""  const memInsts = d.instruments.filter(i=>sel.indexOf(i.id)>=0);
""", "")

# H. 去掉默认器具校验
rep("""    if(v.defaultInstId && sel.indexOf(v.defaultInstId)<0){ toast.warn('默认器具必须属于该器具组成员'); return; }
""", "")

# I. 保存 rec 去掉 defaultInstId
rep("""      const rec={ id:v.id, name:v.name, defaultInstId:v.defaultInstId||sel[0], memberIds:sel, note:v.note||'', editor:s.me.name, editorDate:TODAY };""",
"""      const rec={ id:v.id, name:v.name, memberIds:sel, note:v.note||'', editor:s.me.name, editorDate:TODAY };""")

# J. 日志去掉默认
rep("""(isEdit?'更新':'新建')+'器具组 '+rec.name+'（成员 '+sel.length+' 台，默认 '+rec.defaultInstId+'）'""",
"""(isEdit?'更新':'新建')+'器具组 '+rec.name+'（成员 '+sel.length+' 台）'""")

# K. 组表单：删默认器具项，备注占整行
rep("""      <Row gutter={12} style={{marginTop:12}}>
        <Col span={14}><Form.Item name="defaultInstId" label="默认器具（创建 MSA 计划时自动选中）">
          <Select allowClear placeholder="从成员器具中选择" options={memInsts.map(i=>({value:i.id,label:i.id+' '+i.name}))}/>
        </Form.Item></Col>
        <Col span={10}><Form.Item name="note" label="备注"><Input/></Form.Item></Col>
      </Row>""",
"""      <Row gutter={12} style={{marginTop:12}}>
        <Col span={24}><Form.Item name="note" label="备注"><Input/></Form.Item></Col>
      </Row>""")

# L. 创建弹窗 groupItems 去 def/defName
rep("""...(d.instGroups||[]).map(g=>{ const it=d.instruments.find(i=>i.id===g.defaultInstId); return {id:g.id, name:g.name, count:g.memberIds.length, def:g.defaultInstId, defName:it?it.name:''}; })""",
"""...(d.instGroups||[]).map(g=>({id:g.id, name:g.name, count:g.memberIds.length}))""")

# M. 注释
rep("""  // 选择器具组：拉出该组全部器具并默认勾选默认器具""",
"""  // 选择器具组：拉出该组全部器具并默认勾选样机器具""")

# N. pickGroup 默认勾选样机
rep("""    const defOk = g.defaultInstId && d.instruments.find(i=>i.id===g.defaultInstId && (i.status==='在用'||i.status==='待校准') && daysBetween(TODAY,i.nextCal||'')>=0 && !instHasActivePlan(d,i.id));
    setSelKeys(defOk?[g.defaultInstId]:[]);""",
"""    const protoIds=(g.memberIds||[]).filter(id=>(d.instruments.find(x=>x.id===id)||{}).prototype==='是');
    const protoOk=protoIds.filter(id=>{ const it=d.instruments.find(x=>x.id===id); return it && (it.status==='在用'||it.status==='待校准') && daysBetween(TODAY,it.nextCal||'')>=0 && !instHasActivePlan(d,id); });
    setSelKeys(protoOk);""")

# O. Alert 文案
rep("""（默认选中该组「默认器具」）""", """（默认选中该组「样机」器具）""")

# P/Q. 左侧面板去默认
rep("""<div><b>{item.name}</b>{item.id!=='all'? <Tag color="blue" style={{marginLeft:4}}>默认</Tag>:null}</div>""",
"""<div><b>{item.name}</b></div>""")
rep("""<div className="tiny">{item.count} 台器具{item.id!=='all'? ' · 默认 '+item.def+(item.defName?' '+item.defName:''):''}</div>""",
"""<div className="tiny">{item.count} 台器具</div>""")

# R. 右侧表头显示样机
rep("""<span>当前：器具组 <b>{curGroupObj?curGroupObj.id:''} {curGroupObj?curGroupObj.name:''}</b> ｜ 成员 {curGroupObj?curGroupObj.memberIds.length:0} 台 ｜ 默认器具 <b>{curGroupObj?curGroupObj.defaultInstId:''}</b>（已默认勾选，可改）</span>""",
"""<span>当前：器具组 <b>{curGroupObj?curGroupObj.id:''} {curGroupObj?curGroupObj.name:''}</b> ｜ 成员 {curGroupObj?curGroupObj.memberIds.length:0} 台 ｜ 样机 <b>{(curGroupObj?(curGroupObj.memberIds||[]).filter(id=>(d.instruments.find(x=>x.id===id)||{}).prototype==='是').length:0)} 台</b>（已默认勾选，可改）</span>""")

# T. 注释
rep("""  /* ---------------- 器具组（在台账中维护：组内成员 + 默认器具） ---------------- */""",
"""  /* ---------------- 器具组（在台账中维护：组内成员；器具明细标注样机属性） ---------------- */""")

# W. 器具表单「样机」label 简化
rep("""<Col span={6}><Form.Item name="prototype" label="样机（周期校验自动筛选）" tooltip="标记为样机的器具：周期性 MSA 校验时系统自动筛选带样机标记的器具生成计划，无需每次手动挑选"><Select options={[{value:'是',label:'是（样机）'},{value:'否',label:'否'}]}/></Form.Item></Col>""",
"""<Col span={6}><Form.Item name="prototype" label="样机" tooltip="标记为样机的器具：周期性 MSA 校验时系统自动筛选带样机标记的器具生成计划，无需每次手动挑选"><Select options={[{value:'是',label:'是（样机）'},{value:'否',label:'否'}]}/></Form.Item></Col>""")

# W2. 详情「样机标记」label -> 「样机」
rep("""{key:'样机', label:'样机标记', children:r.prototype==='是'?<Tag color="orange">样机（周期校验自动筛选）</Tag>:'否'}""",
"""{key:'样机', label:'样机', children:r.prototype==='是'?<Tag color="orange">样机（周期校验自动筛选）</Tag>:'否'}""")

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
