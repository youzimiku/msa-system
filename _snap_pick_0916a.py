# -*- coding: utf-8 -*-
import io, os, sys, datetime, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
src = os.path.join(BASE, 'index.html')
snap = os.path.join(BASE, 'index_备份_%s_台账选择样本前.html' % ts)
shutil.copy2(src, snap)
print('快照:', os.path.basename(snap))
