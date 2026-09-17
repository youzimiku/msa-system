# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('sampling')", 1)
tmp_path = os.path.join(DIR, '_check_tmp_sampling.html')
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

chk('查询条件车间下拉存在', '车间')
chk('车间下拉选项渲染', '二分厂')
# 工厂在车间之前
fi = dom_noscript.find('>工厂<')
si = dom_noscript.find('>车间<')
print('PASS' if 0 <= fi < si else 'FAIL', '工厂在车间前')
if not (0 <= fi < si): ok = False
chk('抽样规则按工厂车间过滤逻辑存在', "r.plant===fQPlant")
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
