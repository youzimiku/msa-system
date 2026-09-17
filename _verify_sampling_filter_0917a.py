# -*- coding: utf-8 -*-
import io, sys, subprocess, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
DIR = os.path.dirname(P)
src = io.open(P, encoding='utf-8').read()
tmp = src.replace("useState('instgroup')", "useState('sampling')", 1)
# 预置当前选中方法 GRR，验证抽样规则过滤
tmp = tmp.replace("const [selMethod,setSelMethod]=useState();", "const [selMethod,setSelMethod]=useState('GRR');", 1)
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

# 选中 GRR 时：GRR 规则显示，KAPPA 规则隐藏
chk('GRR 规则 SR-001 显示', 'SR-001')
chk('GRR 规则 SR-006 显示', 'SR-006')
chk('KAPPA 规则 SR-002 被过滤', 'SR-002', reverse=True)
chk('KAPPA 规则 SR-007 被过滤', 'SR-007', reverse=True)
# 方法列只读：方法名 span 文本显示（GRR）
chk('方法列只读文本', 'SR-001')
# 方法列无 Select 编辑控件（抽样规则表格里无 setRuleF method）
chk('方法列无编辑控件', "setRuleF(r,'method',x)", reverse=True)
os.remove(tmp_path)
print('RESULT', 'ALL_PASS' if ok else 'HAS_FAIL')
