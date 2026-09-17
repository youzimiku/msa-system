# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = io.open(P, encoding='utf-8').read()
ok = True
def chk(name, cond, reverse=False):
    global ok
    hit = (cond in src) if not reverse else (cond not in src)
    print(('PASS' if hit else 'FAIL'), name)
    if not hit: ok = False
chk('过滤含 partName', "+(r.partName||'')+")
chk('placeholder 含零件名称', '样本编号/样本名称/零件号/零件名称/被测项目')
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
