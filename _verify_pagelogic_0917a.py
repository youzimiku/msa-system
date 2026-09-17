# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ok = True
def dom_of(init):
    tmp = src.replace("useState('instgroup')", "useState('%s')" % init, 1)
    tp = os.path.join(DIR, '_check_tmp_%s.html' % init)
    io.open(tp, 'w', encoding='utf-8').write(tmp)
    url = 'file:///' + tp.replace('\\', '/')
    r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--virtual-time-budget=10000', '--dump-dom', url],
                       capture_output=True, timeout=180)
    d = r.stdout.decode('utf-8', errors='replace')
    os.remove(tp)
    return re.sub(r'<script[\s\S]*?</script>', '', d)
def chk(name, cond, reverse=False):
    global ok
    hit = (cond in cond_dom) if not reverse else (cond not in cond_dom)
    print(('PASS' if hit else 'FAIL'), name)
    if not hit: ok = False

cond_dom = dom_of('instgroup')
chk('器具组：页面说明出现', '页面说明')
chk('器具组：关键逻辑', '组类型决定用途')
chk('器具组：逻辑含人员组说明', '人员组')
cond_dom = dom_of('sampling')
chk('抽样方法：关键逻辑', '分析方法为固定代码表')
chk('抽样方法：判断规则三档', '判定结论固定三档')
cond_dom = dom_of('plan')
chk('MSA计划：关键逻辑', '维度列状态按计划勾选的方法范围')
chk('MSA计划：状态标识表', '不做（灰色横线）')
cond_dom = dom_of('data_grr')
chk('数据录入：关键逻辑', '多操作员')
chk('数据录入：关键操作', '录入人')
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
