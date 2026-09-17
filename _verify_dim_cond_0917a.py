# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('plan')", 1)
tmp_path = os.path.join(DIR, '_check_tmp_dim.html')
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
chk('有条件接受黄色图标渲染', 'M12 7.5v4.2')
chk('tooltip 有条件接受', '有条件接受')
chk('页面说明表含黄色行', '有条件接受（黄色感叹号）')
chk('不通过红叉仍渲染', 'M8.5 8.5l7 7')
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
