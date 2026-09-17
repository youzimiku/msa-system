# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'

orig = io.open(path, encoding='utf-8').read()
c = orig.replace("useState('instgroup')", "useState('samplelib')")
io.open(path, 'w', encoding='utf-8').write(c)
try:
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                       capture_output=True, encoding='utf-8', errors='replace', timeout=90)
    out = r.stdout or ''
    print('页面标题渲染:', '样本库管理' in out)
    print('页面说明文案:', '样本新增时，触发打印事件，打印样本编号二维码，支持补打' in out)
    print('details说明容器:', 'ant-page-guide' in out or '页面说明' in out)
    print('操作列表头:', '操作' in out, '| 样本编号:', '样本编号' in out)
    print('更多按钮渲染:', '>更多</button>' in out or '更多' in out)
    # 提取表头确认列表结构完整
    ths = re.findall(r'<th[^>]*>(.*?)</th>', out, re.S)
    heads = []
    for t in ths:
        txt = re.sub(r'<[^>]+>', '', t).strip()
        if txt and txt not in heads:
            heads.append(txt)
    print('表头前8:', heads[:8])
finally:
    io.open(path, 'w', encoding='utf-8').write(orig)
print('RESTORED')
