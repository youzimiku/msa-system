# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    cnt = s.count(old)
    if cnt != 1:
        print('WARN count=%d for: %s' % (cnt, old[:60])); return
    s = s.replace(old, new)
    print('OK:', old[:46])

rep("""  /* 企业字段口径补全：台账 / 检验标准 / MSA 计划 缺失字段给默认值（新增字段统一在此兜底） */
  applyFieldDefaults({instruments, standards, plans, grr, kappa});""",
    """  /* 新增分析方法台账（2026-09-08 会议口径：线性/偏移、稳定性、Cg/Cgk、分辨率；一器一计划一方法） */
  const linear=[], stability=[], cgcgk=[], resolution=[];

  /* 企业字段口径补全：台账 / 检验标准 / MSA 计划 缺失字段给默认值（新增字段统一在此兜底） */
  applyFieldDefaults({instruments, standards, plans, grr, kappa});""")

open(p, 'w', encoding='utf-8').write(s)
print('done, len', len(s))
