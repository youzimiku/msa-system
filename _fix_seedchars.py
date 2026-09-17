# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

# 1) 模块级中转变量
old1 = "function buildSeed(){"
new1 = "let G_SEED_CHARS=[];\nfunction buildSeed(){"
assert src.count(old1) == 1, ('old1', src.count(old1))
src = src.replace(old1, new1, 1)

# 2) buildSeed 内 characteristics 定义后赋值
old2 = """  const characteristics = [
    {id:'CHAR-2026-001', name:'轴径 φ50±0.05',"""
# 直接在数组结束处赋值：找 471 行结尾 '];' 后
old2b = "    {id:'CHAR-2026-007', name:'液压试验压力 1.0MPa', type:'SC', partName:'轴类件', partNo:'PN-1007', processName:'检验', category:'计量型', unit:'MPa', target:'1.0', usl:'1.05', lsl:'0.95', source:'CP-液压控制计划', methods:[{method:'cgcgk', standardId:'STD-MSA-001'}], plant:'青岛工厂', subplant:'二分厂', status:'启用', note:'精密压力表，Cg/Cgk', editor:'李工程师', editorDate:'2026-09-09'}\n  ];"
assert src.count(old2b) == 1, ('old2b', src.count(old2b))
src = src.replace(old2b, old2b + "\n  G_SEED_CHARS=characteristics;", 1)

# 3) SEED_CHARS 用中转变量
old3 = "  const SEED_CHARS={}; (typeof characteristics!=='undefined'?characteristics:[]).forEach(c=>{ SEED_CHARS[c.id]=c; });"
new3 = "  const SEED_CHARS={}; (G_SEED_CHARS||[]).forEach(c=>{ SEED_CHARS[c.id]=c; });"
assert src.count(old3) == 1, ('old3', src.count(old3))
src = src.replace(old3, new3, 1)

open(p, 'w', encoding='utf-8').write(src)
print('ok')
