# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

c = orig.replace("useState('instgroup')", "useState('plan')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=10000', '--enable-logging=stderr', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=120)
    out = r.stdout or ''
    err = r.stderr or ''
    print('=== 长度 ===', len(out))
    # 是否有表格
    print('表格:', '<table' in out, '| 行:', out.count('<tr'))
    # 错误信息
    for kw in ['Uncaught', 'ReferenceError', 'TypeError', 'SyntaxError', 'is not defined', 'not a function']:
        if kw in err or kw in out:
            i = (err+out).find(kw)
            print('发现错误关键词:', kw, '>>>', (err+out)[i:i+160].replace('\n',' '))
    # th 片段
    m = re.search(r'<th[^>]*>.*?</th>', out, re.S)
    print('首个th片段:', m.group(0)[:200] if m else '无th')
    # 找列头区域：antd table thead
    ti = out.find('<thead')
    print('thead区域前300:', out[ti:ti+300] if ti>=0 else '无thead')
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
