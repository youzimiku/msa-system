# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
src = io.open(base + r'\index.html', encoding='utf-8').read()
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
checks = {
    'instgroup': ['维护测量器具组与人员组（岗位）。', '被计划引用的器具组不可删除。', '维度列状态标识'],
    'data_grr': ['采用多操作员 × 多样本二维录入：每人只看/只改本人数据；录入人仅可录入测量数据'],
    'entry_grr': ['权限说明', '查看全部台账'],
    'ledger': ['维度列状态标识'],
}
for page, needles in checks.items():
    html = src.replace("useState('instgroup')", "useState('%s')" % page)
    tmp = base + r'\_check_tmp_%s.html' % page
    io.open(tmp, 'w', encoding='utf-8').write(html)
    out = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                          '--virtual-time-budget=10000', '--dump-dom', 'file:///' + tmp.replace('\\', '/')],
                         capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90)
    dom = out.stdout
    ok = []
    for n in needles:
        hit = n in dom
        ok.append((n, hit))
    print(page, '=>', ok)
    if 'PageGuide' not in dom and '页面说明' not in dom:
        print('  !! 页面说明容器未渲染')
