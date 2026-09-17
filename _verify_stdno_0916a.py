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
        ths = re.findall(r'<th[^>]*>(.*?)</th>', out, re.S)
        heads = []
        for t in ths:
            txt = re.sub(r'<[^>]+>', '', t).strip()
            if txt and txt not in heads:
                heads.append(txt)
        return out, heads
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

out1, heads1 = render('char')
print('== char 页面 ==')
print('检验标准号列表头:', '检验标准号' in heads1)
print('检验标准列表头:', '检验标准' in heads1)
print('表头:', heads1)

out2, heads2 = render('plan')
print('== plan 页面 ==')
print('检验标准号列表头:', '检验标准号' in heads2)
print('检验标准列表头:', '检验标准' in heads2)
idx_obj = heads2.index('被测参数') if '被测参数' in heads2 else -1
print('被测参数位置:', idx_obj, '| 其后:', heads2[idx_obj+1:idx_obj+4] if idx_obj>=0 else 'N/A')
print('RESTORED')
