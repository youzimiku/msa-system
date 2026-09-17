# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open(r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html', encoding='utf-8').read()
checks = {
    '器具类型Select': s.count('placeholder="器具类型"'),
    '器具组工厂Select': s.count('placeholder="工厂" options={PLANTS_OPT} value={fPlant}'),
    '任务来源Select': s.count('placeholder="任务来源"'),
    '特性类别Select': s.count('placeholder="特性类别"'),
    '工序Select': s.count('placeholder="工序"'),
    '方法名称Select': s.count('placeholder="方法名称"'),
    '可否合并Select': s.count('placeholder="可否合并取样"'),
    '关联标准Select': s.count('placeholder="关联检验标准"'),
    '分析人Select': s.count('placeholder="分析人"'),
    'conclOpts定义': s.count('const conclOpts='),
    'anlOpts定义': s.count('const anlOpts='),
    '待分析Radio': s.count('value="待分析">待分析'),
    '待采集Radio': s.count('value="待采集">待采集'),
}
for k, v in checks.items():
    print(k, v)
