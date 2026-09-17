# -*- coding: utf-8 -*-
"""Step3 修复未命中项"""
import io

P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
s = io.open(P, encoding='utf-8').read()
orig = s
log = []

def rep(old, new, expect=1, tag=''):
    global s
    n = s.count(old)
    if n != expect:
        log.append('FAIL[%s] count=%d expect=%d :: %s' % (tag, n, expect, old[:50]))
        return
    s = s.replace(old, new)
    log.append('OK[%s] x%d' % (tag, n))

# 1) EntryPage state（唯一上下文）
rep("function EntryPage({kind}){\n  const CFG=ENTRY_CFG[kind];\n  const d=Store.get();\n  const [entryRec,setEntryRec]=useState(null);\n  const [fkw",
    "function EntryPage({kind}){\n  const CFG=ENTRY_CFG[kind];\n  const d=Store.get();\n  const [fkw", 1, 'EntryPage state')

# 2) EntryPage 录入按钮（多行上下文，避免与 AnlPage 混淆）
rep("onClick={()=>setEntryRec(r)}>录入数据</Button>}\n      <Button size=\"small\" type=\"link\" onClick={()=>goResult(r)}>查看结果</Button>",
    "onClick={()=>{DataOpen={kind,id:r.id}; NavAPI.go('data_'+kind);}}>录入数据</Button>}\n      <Button size=\"small\" type=\"link\" onClick={()=>goResult(r)}>查看结果</Button>", 1, 'EntryPage录入按钮')

# 3) GrrPage state + Drawer
rep("function GrrPage(){\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [entryRec,setEntryRec]=useState(null); // 待采集记录 → 台账内录入\n  const [fkw",
    "function GrrPage(){\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [fkw", 1, 'GrrPage state')
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · GRR 数据录入<StatusTag s=\"待采集\"/></Space>} width={1000} open onClose={()=>setEntryRec(null)}>\n      <GrrEntry rec={entryRec} onClose={()=>setEntryRec(null)}/>\n    </Drawer>}",
    "", 1, 'GrrPage Drawer')

# 4) KappaPage state + Drawer
rep("function KappaPage(){\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [entryRec,setEntryRec]=useState(null); // 待采集记录 → 台账内录入\n  const [fkw",
    "function KappaPage(){\n  const d=Store.get();\n  const [detail,setDetail]=useState(null);\n  const [fkw", 1, 'KappaPage state')
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · KAPPA 判定数据录入<StatusTag s=\"待采集\"/></Space>} width={1000} open onClose={()=>setEntryRec(null)}>\n      <KappaEntry rec={entryRec} onClose={()=>setEntryRec(null)}/>\n    </Drawer>}",
    "", 1, 'KappaPage Drawer')

# 5) AnlPage Drawer 加 resolution 条件
rep("{entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s=\"待采集\"/></Space>}",
    "{kind==='resolution' && entryRec && <Drawer title={<Space>{entryRec.id} · {entryRec.instName} · {CFG.name} 数据录入<StatusTag s=\"待采集\"/></Space>}", 1, 'AnlPage Drawer')

io.open(P, 'w', encoding='utf-8').write(s)
print('\n'.join(log))
print('saved delta:', len(s)-len(orig))
