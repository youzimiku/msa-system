# -*- coding: utf-8 -*-
import subprocess, io, re

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
    # 提取检验方法列的 DOM
    i = out.find('msa-method-select')
    print('found at:', i)
    if i >= 0:
        seg = out[max(0, i-300): i+900]
        print(seg)
    else:
        # 找检验方法标题后的内容
        j = out.find('检验方法')
        print('检验方法 title at:', j)
        if j >= 0:
            print(out[j: j+1500])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
