# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('plan')", 1)
tmp_path = os.path.join(DIR, '_check_tmp_sz.html')
io.open(tmp_path, 'w', encoding='utf-8').write(tmp)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=12000', '--dump-dom', url],
                   capture_output=True, timeout=180)
dom = r.stdout.decode('utf-8', errors='replace')
ok = True
def chk(name, cond, reverse=False):
    global ok
    hit = (cond in dom) if not reverse else (cond not in dom)
    print(('PASS' if hit else 'FAIL'), name)
    if not hit: ok = False
chk('维度图标 20px', 'width="20" height="20" viewBox="0 0 24 24"')
chk('无 16px 残留', 'width="16" height="16" viewBox="0 0 24 24"', reverse=True)
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
