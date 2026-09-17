# -*- coding: utf-8 -*-
"""创建弹窗：4列→6列；测量人员改多选下拉(显示名字)；分析方法占整行(已有)；去掉重复的提示Tag"""
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()
orig = len(s)

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:60], n, cnt)
    s = s.replace(old, new)

# 1) 测量人员：Input → 多选 Select（先做，用当前 lg={6} 文本）
rep("""<Col xs={24} sm={12} md={8} lg={6}><span className="flt-label">测量人员</span><Input size="small" style={{width:140}} placeholder="参与测量人员（如：操作员A·王强）" value={meta.measurers} onChange={e=>setMetaK('measurers',e.target.value)}/></Col>""",
    """<Col xs={24} sm={12} md={8} lg={4}><span className="flt-label">测量人员</span><Select mode="multiple" size="small" style={{width:140}} placeholder="选择测量人员（可多选）" value={meta.measurers||[]} options={['王强','李娜','张伟','刘洋','陈静','赵磊','孙丽','周涛','吴敏','郑凯'].map(n=>({value:n,label:n}))} onChange={v=>setMetaK('measurers',v)}/></Col>""")

# 2) 其余字段 4列→6列（lg={6}→lg={4}，14处）
n6 = s.count('<Col xs={24} sm={12} md={8} lg={6}>')
s = s.replace('<Col xs={24} sm={12} md={8} lg={6}>', '<Col xs={24} sm={12} md={8} lg={4}>')
print('cols lg6->lg4:', n6)

# 3) 重复 Tag 两行 → 单行条件渲染（未选零件时不显示）
rep("""    <div style={{marginBottom:8}}>{stdSel? <Tag color="blue">本次创建：1 个检验标准 · 1 个质量特性 · 创建后类型为空，待「转 GRR / 转 KAPPA」定型（生成台账待采集记录）</Tag> : <Tag>请先选零件与检验标准</Tag>}</div>
    <div style={{marginBottom:8}}>{stdSel? <Tag color="blue">本次创建：1 个检验标准 · 1 个质量特性 · 创建后类型为空，待「转 GRR / 转 KAPPA」定型（生成台账待采集记录）</Tag> : <Tag>请先选零件与检验标准</Tag>}</div>""",
    """    {stdSel && <div style={{marginBottom:8}}><Tag color="blue">本次创建：1 个检验标准 · 1 个质量特性 · 创建后类型为空，待「转 GRR / 转 KAPPA」定型（生成台账待采集记录）</Tag></div>}""")

# 4) meta 初始测量人员 → 数组
rep("measurers:'操作员A·王强 / 操作员B·刘青 / 操作员C·陈杰'", "measurers:[]")

# 5) 创建计划写入时数组→字符串（下游显示/编辑零改动）
rep("measurers:meta.measurers,", "measurers:Array.isArray(meta.measurers)? meta.measurers.join('、') : (meta.measurers||''),")

io.open(p, 'w', encoding='utf-8').write(s)
print('patched OK, len', len(s), '(was', orig, ')')
