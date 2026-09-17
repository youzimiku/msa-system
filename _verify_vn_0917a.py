# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('plan')", 1)
tmp_path = os.path.join(DIR, '_check_tmp_vn.html')
io.open(tmp_path, 'w', encoding='utf-8').write(tmp)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=12000', '--dump-dom', url],
                   capture_output=True, timeout=180)
dom = r.stdout.decode('utf-8', errors='replace')
dom_noscript = re.sub(r'<script[\s\S]*?</script>', '', dom)
ok = True
def chk(name, cond, reverse=False):
    global ok
    hit = (cond in dom_noscript) if not reverse else (cond not in dom_noscript)
    print(('PASS' if hit else 'FAIL'), name)
    if not hit: ok = False
chk('判定结果有条件接受标签', '有条件接受')
chk('无纯文字待采集span', 'tiny">待采集', reverse=True)
chk('页面无undefined残留', 'undefined', reverse=True)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
