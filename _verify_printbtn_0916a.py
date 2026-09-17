# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

c = orig.replace("useState('instgroup')", "useState('samplelib')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
    body = out[out.find('<body'):] if '<body' in out else out
    btns = []
    for m in re.finditer(r'<button[^>]*>(.*?)</button>', body, re.S):
        txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if txt:
            btns.append(txt)
    print('渲染按钮:', btns)
    print('补打出现次数:', btns.count('补打'))
    print('更多折叠残留:', '更多' in btns)
    # 检查按钮板顺序：新增样本 后紧跟 补打
    if '新增样本' in btns:
        i = btns.index('新增样本')
        print('新增样本后按钮:', btns[i+1:i+3])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
