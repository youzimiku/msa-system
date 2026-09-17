# -*- coding: utf-8 -*-
"""创建MSA计划弹窗：把「将生成N个分计划」一行文字提示，升级为「总计划层/分计划层」层级树预览"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'FAIL %s: 期望 %d 实际 %d | %s' % (tag, cnt, c, old[:100])
    s = s.replace(old, new, cnt)

# ① Alert 预览条 → 层级树预览
OLD = """        {mMethods.length>0 && <Col span={24}><Alert type="info" showIcon message={'将生成 '+mMethods.length+' 个分计划（取样计划）：'+mMethods.map(an=>ANAL_SHORT[an]+'（'+subRuleBrief(an)+'）').join(' / ')} style={{marginTop:8}}/></Col>}"""
NEW = """        {mMethods.length>0 && <Col span={24}>
          <div className="plan-level-box">
            <div className="plan-level-title">计划层级预览</div>
            <div className="plan-level-top">
              <span className="pl-node pl-top">总计划</span>
              <span style={{marginLeft:8}}>共 <b>{Math.max(selKeys.length,1)}</b> 个（每台器具 1 个总计划）{selKeys.length>1? '，器具：'+selKeys.map(id=>(d.instruments.find(i=>i.id===id)||{}).name).join('、') : (selKeys.length===1? '，器具：'+(d.instruments.find(i=>i.id===selKeys[0])||{}).name : '')}</span>
            </div>
            <div className="plan-level-children">
              {mMethods.map(an=>(
                <div className="plan-level-child" key={an}>
                  <span className="pl-line">└─</span>
                  <Tag color={ANAL_COLOR[an]||'blue'}>{ANAL_SHORT[an]}</Tag>
                  <span className="pl-rule">取样：{subRuleBrief(an)}</span>
                  <span className="tiny">→ 生成 {ANAL_SHORT[an]}台账「待采集」分析单</span>
                </div>
              ))}
            </div>
            <div className="tiny plan-level-foot">每个总计划下挂 {mMethods.length} 个分计划（一个方法一个分计划/分析单）；创建后在「MSA计划」页可查看该层级</div>
          </div>
        </Col>}"""
rep(OLD, NEW, 1, 'level-tree')

# ② CSS
OLD2 = """.row-selected{background:#e6f4ff !important;cursor:pointer}
"""
NEW2 = """.row-selected{background:#e6f4ff !important;cursor:pointer}
.plan-level-box{border:1px solid #d9d9d9;border-radius:8px;padding:10px 12px;background:#fafafa;margin-top:8px}
.plan-level-title{font-weight:600;color:#1F4E79;font-size:14px;margin-bottom:8px}
.plan-level-top{display:flex;align-items:center;padding:8px 10px;border:1px solid #91caff;border-radius:6px;background:#e6f4ff;margin-bottom:6px;font-size:13px}
.pl-node{display:inline-block;padding:2px 10px;border-radius:4px;font-size:13px}
.pl-top{background:#1677ff;color:#fff;font-weight:600}
.plan-level-children{padding-left:8px}
.plan-level-child{display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid #e5e7eb;border-radius:6px;background:#fff;margin-top:6px;font-size:13px;color:#333333}
.pl-line{color:#bfbfbf;font-family:Consolas,Monaco,monospace}
.pl-rule{color:#333333;font-weight:600}
.plan-level-foot{color:#666666;margin-top:8px}
"""
rep(OLD2, NEW2, 1, 'css')

open(P, 'w', encoding='utf-8').write(s)
print('level-tree OK 长度', len(s))
