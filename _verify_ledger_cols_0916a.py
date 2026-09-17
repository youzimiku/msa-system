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

# MSA计划页
o1, h1 = render('plan')
print('== plan ==')
print('录入时间列:', '录入时间' in h1, '| 录入人+录入时间相邻:', '录入人' in h1 and '录入时间' in h1)

# KAPPA台账
o2, h2 = render('entry_kappa')
print('== entry_kappa ==')
print('被测参数:', '被测参数' in h2, '| 测量对象:', '测量对象' in h2)
print('分辨力残留:', '分辨力' in h2, '| 标准值残留:', '标准值' in h2, '| 上限残留:', '上限' in h2, '| 下限残留:', '下限' in h2)
print('审核时间:', '审核时间' in h2, '| 确认人:', '确认人' in h2, '| 确认时间:', '确认时间' in h2)
print('手动分析残留:', '手动分析' in o2, '| 分析按钮:', '>分析<' in o2, '| 更多折叠残留:', '>更多<' in o2)

# 稳定性台账
o3, h3 = render('entry_stability')
print('== entry_stability ==')
print('被测参数:', '被测参数' in h3, '| 分辨力残留:', '分辨力' in h3)

# 线性/偏移台账
o4, h4 = render('entry_linear')
print('== entry_linear ==')
print('被测参数:', '被测参数' in h4, '| 分辨力保留:', '分辨力' in h4)

# CG/CGK台账
o5, h5 = render('entry_cgcgk')
print('== entry_cgcgk ==')
print('被测参数:', '被测参数' in h5, '| 分辨力保留:', '分辨力' in h5)

# GRR台账
o6, h6 = render('entry_grr')
print('== entry_grr ==')
print('被测参数:', '被测参数' in h6, '| 分辨力保留:', '分辨力' in h6, '| 手动分析残留:', '手动分析' in o6)
print('RESTORED')
