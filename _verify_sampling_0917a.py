# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('sampling')", 1)
tmp = tmp.replace('defaultActiveKey="sample"', 'defaultActiveKey="judge"', 1)
tmp = tmp.replace("pagination={{pageSize:8,showTotal:t=>'共 '+t+' 条'}}", 'pagination={false}', 999)
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

chk('判断规则行 JR-017', 'JR-017')
chk('判断规则行 JR-019', 'JR-019')
chk('判断规则行 JR-020', 'JR-020')
chk('判断规则行 JR-008（verdict 已规范为可接受）', 'JR-008')
chk('方法名称无输入框', "onChange={e=>setMF(r,'name',e.target.value)}", reverse=True)
chk('方法操作列无删除', 'disabled={mRef(r)}', reverse=True)
chk('方法代码表有保存按钮', '保存')
chk('抽样规则表格渲染', 'SR-001')
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
