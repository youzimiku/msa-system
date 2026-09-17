# -*- coding: utf-8 -*-
import io

p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(p, encoding='utf-8').read()

# 1) calcGRR 缺收尾 }：在 return 行后补 }
ret = '  return {EV,AV,GRR,PV,TV,Rbar,Xdiff,partMeans,Xbars,opStats,pctEv,pctAv,pctGrr,pctPv,ndc,pctGrrTol,verdict,level,reasons};'
assert s.count(ret) == 1, 'ret not unique: %d' % s.count(ret)
s = s.replace(ret, ret + '\n}', 1)

# 2) 删除 786 行多余 }（位于 recCalc 收尾 } 与 KAPPA 注释之间）
old = '''  return null;
}
}

/* KAPPA 二分类一致性（参考 vs 检验员） */'''
new = '''  return null;
}

/* KAPPA 二分类一致性（参考 vs 检验员） */'''
assert s.count(old) == 1, 'dup brace block not found: %d' % s.count(old)
s = s.replace(old, new, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('fixed, len', len(s))
