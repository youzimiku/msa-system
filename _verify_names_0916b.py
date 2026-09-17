# -*- coding: utf-8 -*-
import io, subprocess, sys, re
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
    b = r.stdout or ''
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)

ths = re.findall(r'<th[^>]*>\s*([^<]+?)\s*</th>', b)
print('页面所有表头:', ths)
print('分析方法 表头出现次数:', ths.count('分析方法'))
print('检验方法 表头出现次数:', ths.count('检验方法'))
