# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
src = io.open(base + r'\index.html', encoding='utf-8').read()
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# 源码 JSX 中 summary 文本出现 1 次；页面说明渲染成功后 DOM 再出现 1 次 -> 有说明页=2，无说明页=1
cases = {
    'instgroup': 2,   # 有说明（text+logic）
    'data_grr': 2,    # 有说明（logic）
    'entry_grr': 2,   # 有说明（perm）
    'ledger': 1,      # 已删除说明
    'anl_grr': 1,     # 已删除说明（anl 键已删）
}
allok = True
for page, expect in cases.items():
    html = src.replace("useState('instgroup')", "useState('%s')" % page)
    tmp = base + r'\_check_tmp_%s.html' % page
    io.open(tmp, 'w', encoding='utf-8').write(html)
    out = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                          '--virtual-time-budget=10000', '--dump-dom', 'file:///' + tmp.replace('\\', '/')],
                         capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90)
    dom = out.stdout
    n = dom.count('>页面说明</summary>')
    ok = (n == expect)
    allok = allok and ok
    print(page, 'summary次数=', n, '期望=', expect, '=>', 'OK' if ok else 'FAIL')
print('ALL OK' if allok else 'SOME FAILED')
