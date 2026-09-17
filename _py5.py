# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
a = '''    {detail && <KappaDetail rec={detail} onClose={()=>setDetail(null)}/>}
    
  </div>;'''
b = '''    {detail && <KappaDetail rec={detail} onClose={()=>setDetail(null)}/>}
    {anlRec && <AnalyzeModal rec={anlRec} kind="kappa" onClose={()=>setAnlRec(null)}/>}
  </div>;'''
print('count:', src.count(a))
assert src.count(a) == 1, 'not unique'
src = src.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(src)
print('ok')
