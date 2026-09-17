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
    print('selection-item count:', out.count('ant-select-selection-item'))
    print('msa-method-select count:', out.count('msa-method-select'))
    print('ant-select-selection__choice count:', out.count('ant-select-selection__choice'))
    print('ant-select-selector count:', out.count('ant-select-selector'))
    # 找检验方法列表区域：搜被测参数列表表头
    j = out.find('被测参数列表')
    print('被测参数列表 title at:', j)
    if j >= 0:
        seg = out[j: j+3000]
        # 找 GRR 或 selection
        k = seg.find('GRR')
        print('GRR in seg:', k)
        print(seg[k-400:k+600] if k>=0 else seg[:1200])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
