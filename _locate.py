# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
pats = ['renderPage', 'pageRender', 'const RENDER', 'switch(page', 'case "plan"', 'case "sample"', 'case "kappa"', 'case "entry_kappa"', 'case "data_kappa"', 'case "anl_resolution"']
for pat in pats:
    idxs = []
    st = 0
    while True:
        i = s.find(pat, st)
        if i < 0:
            break
        idxs.append(i)
        st = i + 1
    print(pat, idxs[:14])
