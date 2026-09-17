# -*- coding: utf-8 -*-
import subprocess, io, re

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'

orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('char')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=9000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=120)
    out = r.stdout or ''
    b = out.find('<body>')
    body = out[b:] if b >= 0 else out
    # 找第一个 msa-method-select 元素，打印其外层 HTML（最多2000字符）
    i = body.find('msa-method-select')
    print('first at:', i)
    # 往前找 <div class="ant-select
    start = body.rfind('<div class="ant-select', 0, i)
    print(body[start: start+2200])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
