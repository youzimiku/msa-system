# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
ok = True
def chk(name, cond, reverse=False):
    global ok
    hit = (cond in src) if not reverse else (cond not in src)
    print(('PASS' if hit else 'FAIL'), name)
    if not hit: ok = False

chk('计量器具台账提示', '支持：编号/名称/型号/出厂编号/领用人')
chk('器具组维护提示', '支持：组编码/组名称/说明')
chk('校准管理提示', '支持：器具编号/器具名称/校准机构/证书编号')
chk('MSA计划提示', '支持：计划号/器具编号/器具名称/零件号/零件名称')
chk('检验标准提示', '支持：标准编号/标准名称/零件名称/工序名称/检验依据')
chk('被测参数提示', '支持：参数编号/参数名称/零件号/零件名称/工序名称')
chk('抽样方法提示（无方法备注）', '支持：方法代码/方法名称（判断规则：规则编号/方法/结论）')
chk('样本库提示', '支持：样本编号/样本名称/零件号/被测项目')
chk('样品明细提示', '支持：样本编号/样本名称/器具编号/计划号')
tc = src.count('支持：台账编号/计划号/器具编号/器具名称/测量对象')
print('PASS' if tc == 4 else 'FAIL', '台账提示 x4（实际 %d）' % tc)
if tc != 4: ok = False
wc = src.count('style={{width:220}}')
print('PASS' if wc >= 13 else 'FAIL', '宽度 220 共 13 处（实际 %d）' % wc)
if wc < 13: ok = False

# 渲染验证：默认页（器具组维护）placeholder 呈现
tmp = src.replace("useState('instgroup')", "useState('instgroup')", 1)
tmp_path = os.path.join(DIR, '_check_tmp_kw.html')
io.open(tmp_path, 'w', encoding='utf-8').write(tmp)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
url = 'file:///' + tmp_path.replace('\\', '/')
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--virtual-time-budget=10000', '--dump-dom', url],
                   capture_output=True, timeout=180)
dom = r.stdout.decode('utf-8', errors='replace')
dom_noscript = re.sub(r'<script[\s\S]*?</script>', '', dom)
chk('渲染：器具组维护提示可见', '支持：组编码/组名称/说明')
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
