# -*- coding: utf-8 -*-
"""更新手册模板文字 + b64.json 截图映射，然后重新生成手册"""
import io, json, os, subprocess, base64

BASE = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统'
IMG = os.path.join(BASE, 'manual-img')
b64p = os.path.join(IMG, 'b64.json')
genp = os.path.join(BASE, '_gen_manual.py')

# 1) 更新 b64.json：删 06/08 旧键（旧图已被新文件覆盖同名），加 12
b64 = json.load(io.open(b64p, encoding='utf-8'))
for k in list(b64.keys()):
    if k.split('-')[0] in ('06', '08'):
        del b64[k]
def add(key, fname):
    with io.open(os.path.join(IMG, fname), 'rb') as fp:
        b64[key] = base64.b64encode(fp.read()).decode()
add('06-创建MSA计划弹窗', '06-创建MSA计划弹窗.png')
add('08-KAPPA取数录入', '08-KAPPA取数录入.png')
add('12-线性取数录入', '12-线性取数录入.png')
json.dump(b64, io.open(b64p, 'w', encoding='utf-8'), ensure_ascii=False)
print('b64 keys:', list(b64.keys()))

# 2) 更新 _gen_manual.py 模板文字
s = io.open(genp, encoding='utf-8').read()
def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, ('MISS %r -> %d' % (old[:60], n))
    s = s.replace(old, new)

rep('版本 V2.3 ｜ 2026-09-08 会议对齐（特性-量具-方法 一器一计划一方法）＋ 流程断点修复版 ｜ 设计依据：AIAG MSA 第4版 / IATF 16949 / ISO 10012',
    '版本 V2.4 ｜ 取样数量规则对齐版（AIAG 五性 vs VDA Cgk 业务速查表：样品数/人数/次数可调）｜ 设计依据：AIAG MSA 第4版 / IATF 16949 / ISO 10012')
rep('<div class="node"><b>计量器具台账</b>器具组＋默认器具·样机标记·校准状态</div>',
    '<div class="node"><b>计量器具台账</b>器具组＋样机标记·校准状态</div>')
rep('勾选组内成员器具并指定「默认器具」（默认器具在创建 MSA 计划时自动选中）。',
    '勾选组内成员器具并标记「样机」（样机器具在创建 MSA 计划时默认选中）。')
rep('行内「编辑」可调整成员与默认器具；',
    '行内「编辑」可调整成员与样机标记；')
rep('左侧选「器具组」，右侧列出该组全部器具，默认选中「默认器具」，可增选同组器具。',
    '左侧选「器具组」，右侧列出该组全部器具，默认选中该组「样机」器具，可增选同组器具。')
rep('''      <div class="step"><div class="n">5</div><div class="t"><b>确认创建</b><span>点击「确认创建」：生成 N 个计划，并自动生成对应台账「待采集」记录，可直接到台账录入样本。</span></div></div>''',
'''      <div class="step"><div class="n">5</div><div class="t"><b>调节取样参数（可选）</b><span>器具清单每行有 人数 / 次数 / 样本数 三列：按勾选方法带出业务速查默认值（GRR 3人×3次×10件、KAPPA 3人×3次×50件、线性 5 件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次），可在允许范围内调整，提交后按新参数生成录入矩阵。</span></div></div>
      <div class="step"><div class="n">6</div><div class="t"><b>确认创建</b><span>点击「确认创建」：生成 N 个计划，并自动生成对应台账「待采集」记录，可直接到台账录入样本。</span></div></div>''')
rep('<tr><td>KAPPA（计数型）</td><td>50 件 × 3 人盲测判定（业务样例 50 件/3 人/每件 3 次；系统演示每件 1 次二分类判定）</td>',
    '<tr><td>KAPPA（计数型）</td><td>50 件 × 3 人 × 每件 3 次（20~50 件、2~5 人可调，多数裁决为该件结论）</td>')
rep('<tr><td>线性 / 偏移</td><td>线性：5 个标准件覆盖 0/25/50/75/100% 量程，每件 10~12 次；偏倚：以标准件为对象重复测 15 次，先正态性检验（P&gt;0.05）</td>',
    '<tr><td>线性 / 偏移</td><td>线性：5 个标准件覆盖 0~100% 量程，每件 12 次（10~12 次可调，读数 50~60）；偏倚：1 件标准件重复测 15 次（10~15 次可调，真值可追溯），先正态性检验（P&gt;0.05）</td>')
rep('<tr><td>稳定性</td><td>长周期跨 4 周~3 个月，固定参照仪工位，25 个子组 × 每期 3 次，SPC 判异</td>',
    '<tr><td>稳定性</td><td>长周期跨 4 周~3 个月，固定参照仪工位，25 个子组 × 每期 5 次（3~5 次可调，读数 75~125），SPC 判异</td>')
rep('<tr><td>Cg / Cgk（VDA）</td><td>标准件独立装夹连续测 50 次</td>',
    '<tr><td>Cg / Cgk（VDA）</td><td>1 件标准件（中值）独立装夹连续测 50 次（50~200 次可调），偏倚打包进 Cgk</td>')
rep('「待采集」记录行点「录入数据」，按固化取样策略生成默认行数（可增减），填写测量值；GRR 为操作员×样本×试验的交叉矩阵，完整性校验不通过会被拦截。',
    '「待采集」记录行点「录入数据」，按业务速查默认值生成录入矩阵（GRR 3人×3次×10件、KAPPA 3人×3次×50件、线性 5 件×12 次、稳定性 25 子组×5 次、Cg/Cgk 50 次），人数/次数/样本数可调后点「重新生成」按新参数展开矩阵，填写测量值；GRR 为操作员×样本×试验的交叉矩阵，完整性校验不通过会被拦截。')
rep('''      <img class="img" src="{{IMG_09}}" alt="CgCgk取数录入">
      <div class="imgcap">▲ Cg/Cgk 取数录入页（VDA Type1）：固化取样规则；结果在「Cg/Cgk 分析结果」页展示</div>''',
'''      <img class="img" src="{{IMG_09}}" alt="CgCgk取数录入">
      <div class="imgcap">▲ Cg/Cgk 取数录入页（VDA Type1）：1 件标准件连续测 50 次（次数可调）；结果在「Cg/Cgk 分析结果」页展示</div>
      <img class="img" src="{{IMG_12}}" alt="线性取数录入">
      <div class="imgcap">▲ 线性/偏移取数录入页：标准件数与每件次数可调（默认 5 件 × 12 次），「重新生成」按新参数展开录入矩阵</div>''')

io.open(genp, 'w', encoding='utf-8').write(s)
print('gen_manual.py updated')

# 3) 重新生成手册
r = subprocess.run(['python', '_gen_manual.py'], cwd=BASE, capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip())
if r.returncode != 0:
    print('STDERR:', r.stderr[-2000:])
