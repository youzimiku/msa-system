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
    # 只看 body 部分
    b = out.find('<body>')
    body = out[b:] if b >= 0 else out
    print('body len:', len(body))
    print('body msa-method-select count:', body.count('msa-method-select'))
    # 提取 body 中带 ant-select-selection-item 的 class 属性
    items = re.findall(r'class="[^"]*ant-select-selection-item[^"]*"', body)
    print('selection-item class attrs:', len(items))
    for it in items[:6]:
        print(' ', it)
    # 找包含 GRR 文本的 selection-item 内容
    segs = re.findall(r'ant-select-selection-item-content[^<]*<[^>]*>([^<]*)<', body)
    print('item contents sample:', segs[:10])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
