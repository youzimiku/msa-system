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

# 1) 新增黄色感叹号图标（有条件接受）
rep("""const NaSvg=()=> <svg width="16" height="16" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#e5e7eb"/><path d="M7 12h10" stroke="#9ca3af" strokeWidth="2.4" strokeLinecap="round"/></svg>;""",
"""const NaSvg=()=> <svg width="16" height="16" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#e5e7eb"/><path d="M7 12h10" stroke="#9ca3af" strokeWidth="2.4" strokeLinecap="round"/></svg>;
const CondSvg=()=> <DimBadge bg="#fadb14" stroke="M12 7.5v4.2M12 16.2h.01"/>;""",
"新增 CondSvg", cnt=1)

# 2) MSA计划列表分项列（fenCell）：加有条件接受
rep("""    const worst= concls.includes('不可接受')? 'fail' : (concls.length? 'pass' : '');
    const jump=()=>{ const rec=recs[0]; if(rec){ recJump(rec); } else { NavAPI.go(DIM_ENTRY[kind]||'entry_grr'); } };
    if(!inScope) return <Tooltip title={label+'：不做（不在本计划范围）'}><NaSvg/></Tooltip>;
    if(!worst) return <Tooltip title={label+'：未做（计划范围内尚未完成分析）'}><span style={{cursor:'pointer'}} onClick={jump}><TodoSvg/></span></Tooltip>;
    return <Tooltip title={label+'：'+(worst==='fail'?'不通过':'通过')}><span style={{cursor:'pointer'}} onClick={jump}>{worst==='fail'?<FailSvg/>:<PassSvg/>}</span></Tooltip>;""",
"""    const worst= concls.includes('不可接受')? 'fail' : (concls.includes('有条件接受')? 'cond' : (concls.length? 'pass' : ''));
    const jump=()=>{ const rec=recs[0]; if(rec){ recJump(rec); } else { NavAPI.go(DIM_ENTRY[kind]||'entry_grr'); } };
    if(!inScope) return <Tooltip title={label+'：不做（不在本计划范围）'}><NaSvg/></Tooltip>;
    if(!worst) return <Tooltip title={label+'：未做（计划范围内尚未完成分析）'}><span style={{cursor:'pointer'}} onClick={jump}><TodoSvg/></span></Tooltip>;
    return <Tooltip title={label+'：'+(worst==='fail'?'不通过':(worst==='cond'?'有条件接受':'通过'))}><span style={{cursor:'pointer'}} onClick={jump}>{worst==='fail'?<FailSvg/>:(worst==='cond'?<CondSvg/>:<PassSvg/>)}</span></Tooltip>;""",
"fenCell 有条件接受", cnt=1)

# 3) 详情抽屉 dimStatus：加有条件接受
rep("""    const concls=rs.map(x=>x.conclusion).filter(c=>c&&c!=='-'&&c!=='待采集');
    const worst=concls.includes('不可接受')?'fail':(concls.length?'pass':'');
    if(!inScope) return '不做';
    if(!worst) return '未做';
    return worst==='fail'?'不通过':'通过';
  };
  const dimTag=(kind,label)=>{ const s=dimStatus(kind,label); const color=s==='通过'?'green':s==='不通过'?'red':s==='未做'?'orange':'default'; return <Tag color={color} style={{marginRight:0}}>{s}</Tag>; };""",
"""    const concls=rs.map(x=>x.conclusion).filter(c=>c&&c!=='-'&&c!=='待采集');
    const worst=concls.includes('不可接受')?'fail':(concls.includes('有条件接受')?'cond':(concls.length?'pass':''));
    if(!inScope) return '不做';
    if(!worst) return '未做';
    return worst==='fail'?'不通过':(worst==='cond'?'有条件接受':'通过');
  };
  const dimTag=(kind,label)=>{ const s=dimStatus(kind,label); const color=s==='通过'?'green':s==='不通过'?'red':s==='有条件接受'?'#fadb14':s==='未做'?'orange':'default'; return <Tag color={color} style={{marginRight:0}}>{s}</Tag>; };""",
"dimStatus/dimTag 有条件接受", cnt=1)

# 4) 页面说明状态标识表：加一行有条件接受
rep("""          <tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>通过（绿色对勾）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为可接受 / 有条件接受</td></tr>
          <tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>不通过（红色叉）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为不可接受，需整改；多个分计划以最差结论为准</td></tr>""",
"""          <tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>通过（绿色对勾）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为可接受</td></tr>
          <tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>有条件接受（黄色感叹号）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为有条件接受（可接受但需关注）；多个分计划以最差结论为准</td></tr>
          <tr><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>不通过（红色叉）</td><td style={{border:'1px solid #d9d9d9',padding:'4px 10px'}}>对应台账分析已完成，结论为不可接受，需整改；多个分计划以最差结论为准</td></tr>""",
"说明表加有条件接受", cnt=1)

io.open(P, 'w', encoding='utf-8').write(t)
print('完成')
