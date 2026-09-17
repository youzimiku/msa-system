# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('sampling')", 1)
tmp_path = os.path.join(tempfile.gettempdir(), 'msa_sampling_check.html')
io.open(tmp_path, 'w', encoding='utf-8').write(tmp)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=10000', '--dump-dom', url],
                   capture_output=True, timeout=120)
dom = r.stdout.decode('utf-8', errors='replace')
print('DOM len:', len(dom))
print('has html:', '<html' in dom)
for k in ['抽样方法维护', '分析方法', 'MSA 管理系统', '菜单', '台账', 'base-data', 'index.html', 'Application error', 'Uncaught']:
    print(k, '->', k in dom)
# 打印 body 前 300 字符
m = re.search(r'<body[\s\S]{0,300}', dom)
print('BODY HEAD:', (m.group(0) if m else 'NONE')[:300])
print('STDERR:', r.stderr.decode('utf-8', errors='replace')[-500:])
