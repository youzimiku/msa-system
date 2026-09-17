# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
ok = 'placeholder="支持：' not in src and src.count('placeholder="') >= 13
print('PASS' if ok else 'FAIL', '无支持：前缀且占位符保留')
tmp_path = os.path.join(DIR, '_check_tmp_kw.html')
io.open(tmp_path, 'w', encoding='utf-8').write(src)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=10000', '--dump-dom', url],
                   capture_output=True, timeout=180)
dom = r.stdout.decode('utf-8', errors='replace')
dom_noscript = re.sub(r'<script[\s\S]*?</script>', '', dom)
ok2 = '组编码/组名称/说明' in dom_noscript and '支持：组编码' not in dom_noscript
print('PASS' if ok2 else 'FAIL', '渲染：无前缀提示可见')
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if (ok and ok2) else 'HAS_FAIL')
