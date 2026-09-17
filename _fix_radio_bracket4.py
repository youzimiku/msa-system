# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
lines = open(p, encoding='utf-8').read().split('\n')
# 1476 行（1-based）修正
i = 1475
l = lines[i]
print('原行:', l[-100:])
lines[i] = '        <Radio.Group size="small" optionType="button" buttonStyle="solid" value={fStatus||\'\'} onChange={e=>setFStatus(e.target.value||undefined)} options={[{value:\'\',label:\'全部\'}].concat(ENUM.instStatus.map(c=>({value:c,label:c})))}/>'
print('新行:', lines[i][-100:])
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('OK')
