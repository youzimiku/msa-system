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
        # 提取渲染后按钮文本（剥离源码区：只取 <body> 之后部分）
        body = out[out.find('<body'):] if '<body' in out else out
        btns = []
        for m in re.finditer(r'<button[^>]*>(.*?)</button>', body, re.S):
            txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if txt:
                btns.append(txt)
        return btns
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

b = render('entry_kappa')
print('entry_kappa 渲染按钮:', b)
print('手动分析按钮残留:', '手动分析' in b)
print('更多折叠残留:', '更多' in b)
print('分析按钮存在:', '分析' in b)
print('RESTORED')
