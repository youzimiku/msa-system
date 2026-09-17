# -*- coding: utf-8 -*-
import io, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('char')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
    body = out[out.find('<body'):] if '<body' in out else out
    # 打印"绑定器具组"前后各120字符上下文
    idx = 0
    while True:
        i = body.find('绑定器具组', idx)
        if i < 0: break
        print('--- 上下文 @', i, '---')
        print(body[max(0,i-130):i+80].replace('\n',' '))
        idx = i + 1
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
