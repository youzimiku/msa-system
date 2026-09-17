# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
src = open(p, encoding='utf-8').read()
print('GRR台账种子:', sorted(set(re.findall(r"id:'(GRR-[^']+)'", src))))
print('KPA台账种子:', sorted(set(re.findall(r"id:'(KPA-[^']+)'", src))))
print('Linear台账种子:', sorted(set(re.findall(r"id:'(LIN-[^']+)'", src))))
print('Stab台账种子:', sorted(set(re.findall(r"id:'(STB-[^']+)'", src))))
print('CgCgk台账种子:', sorted(set(re.findall(r"id:'(CGK-[^']+)'", src))))
