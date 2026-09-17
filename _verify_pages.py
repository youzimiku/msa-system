# -*- coding: utf-8 -*-
import subprocess, io

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'

orig = io.open(path, encoding='utf-8').read()
pages = {
    'char': '被测参数列表',
    'sampling': '分析方法列表',
    'samplelib': '样本列表',
    'plan': '计划列表',
}
try:
    for key, feat in pages.items():
        c = orig.replace("useState('instgroup')", "useState('" + key + "')")
        assert c != orig
        io.open(path, 'w', encoding='utf-8').write(c)
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        print(key, '| 页面特征词命中:', feat in out, '| 标题命中:', 'MSA 测量系统分析管理系统' in out, '| dom长度:', len(out))
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
