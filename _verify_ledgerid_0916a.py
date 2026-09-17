# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

def render(page):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    io.open(path, 'w', encoding='utf-8').write(c)
    try:
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        body = out[out.find('<body'):] if '<body' in out else out
        ths = re.findall(r'<th[^>]*>(.*?)</th>', body, re.S)
        heads = []
        for t in ths:
            txt = re.sub(r'<[^>]+>', '', t).strip()
            if txt and txt not in heads:
                heads.append(txt)
        return heads
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

for p in ['entry_grr','entry_kappa','entry_linear','entry_stability','entry_cgcgk']:
    h = render(p)
    print(p, '| 台账编号:', '台账编号' in h, '| 编号列位置(操作后):', h[h.index('操作')+1] if '操作' in h and len(h)>h.index('操作')+1 else '?', '| 残留GRR编号:', 'GRR 编号' in h or 'GRR编号' in h)
print('RESTORED')
