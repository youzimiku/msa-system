# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new, tag, cnt=1):
    global t
    n = t.count(old)
    assert n == cnt, '锚点数量不符 %s: 期望 %d 实际 %d' % (tag, cnt, n)
    t = t.replace(old, new)
    print('OK:', tag)

# 1) 结论归一化函数 + VerdictTag 改为四档
rep("""function VerdictTag({v}){ const vv=(!v||v==='-')?'待采集':v; return <Tooltip title={TIPS.verdict[vv]||TIPS.verdict[v]||vv}><Tag color={verdictColor(vv)} className="spec-tag" style={{minWidth:84,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{vv}</Tag></Tooltip>; }""",
"""const normVerdict=v=>{
  if(!v||v==='-'||v==='待采集') return '待采集';
  if(String(v).indexOf('不可接受')>=0) return '不可接受';
  if(String(v).indexOf('有条件')>=0||String(v).indexOf('边缘')>=0||String(v).indexOf('较理想')>=0) return '有条件接受';
  if(String(v).indexOf('可接受')>=0||String(v).indexOf('优秀')>=0||String(v).indexOf('理想')>=0||String(v).indexOf('评价人')>=0||String(v).indexOf('好')>=0) return '可接受';
  return v;
};
function VerdictTag({v}){ const vv=normVerdict(v); return <Tooltip title={TIPS.verdict[vv]||vv}><Tag color={verdictColor(vv)} className="spec-tag" style={{minWidth:84,display:'inline-flex',justifyContent:'center',marginRight:0,textAlign:'center'}}>{vv}</Tag></Tooltip>; }""",
"VerdictTag 归一四档", cnt=1)

# 2) MSA计划列表判定结果列：纯文字待采集 → 标签
rep("""return recs.length? <VerdictTag v={sv}/> : (r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:<span className="tiny">待采集</span>); }},
    {title:'状态',""",
"""return recs.length? <VerdictTag v={sv}/> : (r.result&&r.result!=='-'?<VerdictTag v={r.result}/>:<VerdictTag v="待采集"/>); }},
    {title:'状态',""",
"计划列表判定结果待采集标签", cnt=1)

# 3) 详情抽屉判定结果：纯文字待采集 → 标签
rep("""children: recs.length? <VerdictTag v={sumVerdict(recs)}/> : (plan.result&&plan.result!=='-'?<VerdictTag v={plan.result}/>:<span className="tiny">待采集</span>)},""",
"""children: recs.length? <VerdictTag v={sumVerdict(recs)}/> : (plan.result&&plan.result!=='-'?<VerdictTag v={plan.result}/>:<VerdictTag v="待采集"/>)},""",
"详情抽屉判定结果待采集标签", cnt=1)

# 4) 计划列表 测量人数/次数/样本数量：无值显示 -
def fix_numcol(old, new, tag):
    rep(old, new, tag, 1)

fix_numcol("""const recs=planRecords(d,r.id); return <span className="mono">{String(recs.length? recs[0].numOps : (r.params&&r.params.ops!==undefined? r.params.ops : ''))}</span>; }""",
"""const recs=planRecords(d,r.id); const v=recs.length&&recs[0].numOps!=null? recs[0].numOps : (r.params&&r.params.ops!=null? r.params.ops : ''); return <span className="mono">{v===''?'-':v}</span>; }""",
"测量人数判空")

fix_numcol("""const recs=planRecords(d,r.id); return <span className="mono">{String(recs.length? recs[0].numTrials : (r.params&&r.params.trials!==undefined? r.params.trials : ''))}</span>; }""",
"""const recs=planRecords(d,r.id); const v=recs.length&&recs[0].numTrials!=null? recs[0].numTrials : (r.params&&r.params.trials!=null? r.params.trials : ''); return <span className="mono">{v===''?'-':v}</span>; }""",
"测量次数判空")

fix_numcol("""const recs=planRecords(d,r.id); return <span className="mono">{String(recs.length? recs[0].numParts : (r.params&&r.params.parts!==undefined? r.params.parts : ''))}</span>; }""",
"""const recs=planRecords(d,r.id); const v=recs.length&&recs[0].numParts!=null? recs[0].numParts : (r.params&&r.params.parts!=null? r.params.parts : ''); return <span className="mono">{v===''?'-':v}</span>; }""",
"样本数量判空")

io.open(P, 'w', encoding='utf-8').write(t)
print('完成')
