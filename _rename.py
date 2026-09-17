# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()

repl = [
    ("label:'质量特性维护', group:'基础数据'", "label:'被测参数维护', group:'基础数据'"),
    ("'char':'质量特性维护',", "'char':'被测参数维护',"),
    ('>质量特性 <b style={{color:\'#cf1322\'}}>*</b></span><Select size="small" style={{width:140}} placeholder="选择质量特性"', '>被测参数 <b style={{color:\'#cf1322\'}}>*</b></span><Select size="small" style={{width:140}} placeholder="选择被测参数"'),
    ('先选择质量特性', '先选择被测参数'),
    ("{key:'质量特性', label:'质量特性'", "{key:'被测参数', label:'被测参数'}"),
    ("title:'关联质量特性'", "title:'关联被测参数'"),
    ("{key:'关联质量特性', label:'关联质量特性'", "{key:'关联被测参数', label:'关联被测参数'}"),
    ('label="关联质量特性"', 'label="关联被测参数"'),
    ('<PageHead title="质量特性维护"/>', '<PageHead title="被测参数维护"/>'),
    ('<ImportBtn title="质量特性维护"/>', '<ImportBtn title="被测参数维护"/>'),
    ("'质量特性列表（'+rows.length+' 条）'", "'被测参数列表（'+rows.length+' 条）'"),
    ("'编辑质量特性':'新增质量特性'", "'编辑被测参数':'新增被测参数'"),
    ("title:'质量特性维度'", "title:'对应被测项目'"),
    ('label="质量特性维度（真值对应测量项目）"', 'label="对应被测项目"'),
    ("title:'特性编号'", "title:'被测参数编号'"),
    ("title:'特性名称'", "title:'被测参数名称'"),
    ('placeholder="特性编号 / 名称 / 零件 / 工序"', 'placeholder="被测参数编号 / 名称 / 零件 / 工序"'),
    ("{key:'id',label:'特性编号'", "{key:'id',label:'被测参数编号'}"),
    ("{key:'name',label:'特性名称'", "{key:'name',label:'被测参数名称'}"),
    ('label="特性编号"', 'label="被测参数编号"'),
    ('label="特性名称"', 'label="被测参数名称"'),
]

cnt = 0
for a, b in repl:
    n = src.count(a)
    if n == 0:
        print('NOT FOUND:', a[:60])
    else:
        src = src.replace(a, b)
        cnt += n
        print('OK x%d:' % n, a[:60])
open(p, 'w', encoding='utf-8').write(src)
print('total replaced:', cnt)
