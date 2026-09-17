# -*- coding: utf-8 -*-
"""修复 TDZ：把 cur 派生值移到 rows 定义之后"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = open(P, encoding='utf-8').read()

old = """  const [curPlan,setCurPlan]=useState(null); // 当前选中计划（下栏展示其分析单）
  const cur = curPlan && rows.some(p=>p.id===curPlan.id) ? curPlan : (rows[0]||null);
"""
new = """  const [curPlan,setCurPlan]=useState(null); // 当前选中计划（下栏展示其分析单）
"""
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)

# 在 rows 定义结束后插入 cur
old2 = """    return kwMatch && typeMatch && statusMatch;
  });

  const instCell=(r,fn)=>"""
new2 = """    return kwMatch && typeMatch && statusMatch;
  });
  const cur = curPlan && rows.some(p=>p.id===curPlan.id) ? curPlan : (rows[0]||null);

  const instCell=(r,fn)=>"""
assert s.count(old2) == 1, s.count(old2)
s = s.replace(old2, new2, 1)

open(P, 'w', encoding='utf-8').write(s)
print('tdz-fix OK 长度', len(s))
