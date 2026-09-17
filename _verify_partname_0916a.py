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
        return body
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

b = render('samplelib')
# 零件名称纯文字：样本名称列应为 span 文本；检查样本行是否出现零件名称（轴类件/孔类件等）
for nm in ['轴类件','孔类件','标准件','轴端盖','壳体','齿轮轴']:
    print(nm, '出现次数:', b.count(nm))
# SPL-001 行区域检查
i = b.find('SPL-001')
print('SPL-001 行区域:', re.sub(r'<[^>]+>', ' ', b[i:i+700])[:300])
print('RESTORED')
