# -*- coding: utf-8 -*-
# 批量拉取 2026-09-11 三场腾讯会议：智能纪要 + 完整文字转写
import subprocess, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_meeting_0911'

def run(args):
    p = subprocess.run(['tmeet'] + args, capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        return None, p.stdout + p.stderr
    try:
        return json.loads(p.stdout), None
    except Exception as e:
        return None, 'parse err: ' + str(e) + ' raw: ' + p.stdout[:200]

def fetch_minutes(rid, tag):
    data, err = run(['record', 'smart-minutes', '--record-file-id', str(rid), '--compact'])
    if err or data is None:
        print(tag, 'minutes FAIL:', (err or '')[:200])
        return
    mm = data.get('data', {}).get('meeting_minute', {})
    txt = mm.get('minute', '')
    with open(OUT + '_minutes_' + tag + '.txt', 'w', encoding='utf-8') as f:
        f.write(txt)
    print(tag, 'minutes OK, len=', len(txt))

def fetch_transcript(rid, tag):
    all_paras = []
    pid = ''
    guard = 0
    while True:
        guard += 1
        if guard > 60:
            print(tag, 'transcript loop guard hit'); break
        args = ['record', 'transcript-get', '--record-file-id', str(rid), '--limit', '300', '--compact']
        if pid:
            args += ['--pid', str(pid)]
        data, err = run(args)
        if err or data is None:
            print(tag, 'transcript FAIL:', (err or '')[:200]); break
        paras = data.get('data', {}).get('minutes', {}).get('paragraphs', [])
        if not paras:
            break
        all_paras.extend(paras)
        last = paras[-1].get('pid')
        # pid 是字符串编号，直接+1 尝试下一页
        try:
            nxt = str(int(last) + 1)
        except Exception:
            nxt = last
        if nxt == pid:
            break
        pid = nxt
    with open(OUT + '_transcript_' + tag + '.txt', 'w', encoding='utf-8') as f:
        for p in all_paras:
            sp = p.get('speaker', {}).get('user_name', '?')
            st = p.get('start_time', '')
            et = p.get('end_time', '')
            txt = ' '.join(s.get('text', '') for s in p.get('sentences', []))
            f.write('[%s-%s] %s: %s\n' % (st, et, sp, txt))
    print(tag, 'transcript OK, paragraphs=', len(all_paras))

# 会议1：15:37 元工国际-林学晖的快速会议
fetch_minutes('2098315508316327937', 'm1_1537')
fetch_transcript('2098315508316327937', 'm1_1537')
# 会议2：16:18 高国翔的个人会议室（纪要已单独拉取，这里拉转写）
fetch_transcript('2098325276869709825', 'm2_1618')
# 会议3：16:58 高国翔的个人会议室
fetch_transcript('2098335391678861313', 'm3_1658')
print('DONE')
