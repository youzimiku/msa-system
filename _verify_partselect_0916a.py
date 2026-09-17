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
        has_input = '选择零件号' in body
        has_partsel = body.count('选择零件号')
        # 零件名称纯文字：检查是否还有 PARTNAME 下拉（零件名称列 Select）——渲染后无明显标志，检查列头
        return heads, has_input, has_partsel
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

for p in ['plan', 'char', 'samplelib']:
    h, hi, hp = render(p)
    print(p, '| 列头含零件号:', '零件号' in h, '| 含零件名称:', '零件名称' in h, '| 零件号Input出现次数(含表头说明):', hp)
print('RESTORED')
