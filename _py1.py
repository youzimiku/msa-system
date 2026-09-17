# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
a = '''        <Button type="primary" onClick={()=>setModal({record:null,revise:false})}>新增样本</Button>
        {canDo(d.me.role,'edit') && <ImportBtn title="样本库管理"/>}
        <Button>导出</Button>'''
b = '''        <Button type="primary" onClick={()=>setModal({record:null,revise:false})}>新增样本</Button>
        <Button onClick={()=>setLogOpen(true)}>日志查询</Button>
        {canDo(d.me.role,'edit') && <ImportBtn title="样本库管理"/>}
        <Button>导出</Button>'''
assert src.count(a) == 1, src.count(a)
src = src.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
