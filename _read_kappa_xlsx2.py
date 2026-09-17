# -*- coding: utf-8 -*-
import openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'C:\Users\youzi\xwechat_files\wxid_y2a1nw2f8c9u22_67ae\msg\file\2026-09\MCU6焊接KAPPA报告1.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb['AXI Kappa ']
for row in ws.iter_rows(min_row=80, max_row=174):
    vals = []
    for c in row:
        v = c.value
        if v is not None:
            vals.append('%s=%r' % (c.coordinate, v))
    if vals:
        print(' | '.join(vals))
