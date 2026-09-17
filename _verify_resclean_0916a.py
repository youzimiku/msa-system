# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

# 渲染 MSA计划页（分辨力列取器具 res），确认页面正常且分辨力列无 mm 后缀
c = orig.replace("useState('instgroup')", "useState('plan')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
    print('plan页渲染OK:', 'MSA计划' in out)
    # 检查页面中分辨力单元格是否还残留 mm 单位（提取渲染后的 td 文本）
    tds = re.findall(r'<td[^>]*>(.*?)</td>', out, re.S)
    res_vals = []
    for t in tds:
        txt = re.sub(r'<[^>]+>', '', t).strip()
        if re.match(r'^0\.\d+(mm|g|℃|MPa|N·m)?$', txt):
            res_vals.append(txt)
    print('分辨力类单元格值样本:', res_vals[:20])
    bad = [x for x in res_vals if re.search(r'(mm|g|℃|MPa|N·m)$', x)]
    print('残留单位数量:', len(bad), bad[:5])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
