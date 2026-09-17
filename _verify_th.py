# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'

orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('plan')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
    ths = re.findall(r'<th[^>]*>(.*?)</th>', out, re.S)
    heads = []
    for t in ths:
        txt = re.sub(r'<[^>]+>', '', t).strip()
        if txt:
            heads.append(txt)
    print('表格表头数量:', len(heads))
    print('表头列表:', heads)
    print('操作方法在表头中:', '操作方法' in heads)
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
