# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统_backup_20260911_101042\index.html'
NEW = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
old = open(OLD, encoding='utf-8').read().split('\n')
new = open(NEW, encoding='utf-8').read().split('\n')

PAGES = ['LedgerPage','InstGroupPage','PlanPage','BatchPlanModal','CharPage','SamplingPage','SampleLibPage','EntryPage','DataEntryPage','GrrPage','KappaPage']

def find_ranges(lines, names):
    out = {}
    for name in names:
        start = None
        depth = 0
        for i, l in enumerate(lines):
            if re.search(r'function '+name+r'\(', l):
                start = i
                depth = 0
            if start is not None and i >= start:
                depth += l.count('{') - l.count('}')
                if depth == 0 and i > start:
                    out[name] = (start, i)
                    break
    return out

def collect(lines, start, end):
    src = '\n'.join(lines[start:end+1])
    titles = re.findall(r"title:'([^']{2,40})'", src)
    labels = re.findall(r'label="([^"]{2,40})"', src)
    btns = re.findall(r'>([^<>{]{2,24}?)</Button>', src)
    desc = re.findall(r'<Descriptions\.Item\s+label="([^"]{2,40})"', src)
    return titles, labels, [b.strip() for b in btns], desc

for page in PAGES:
    ro = find_ranges(old, [page]).get(page)
    rn = find_ranges(new, [page]).get(page)
    if not ro or not rn:
        print('###', page, 'range missing', bool(ro), bool(rn)); continue
    ot, ol, ob, od = collect(old, *ro)
    nt, nl, nb, nd = collect(new, *rn)
    print('#'*16, page, '(旧%d-%d 新%d-%d)' % (ro[0], ro[1], rn[0], rn[1]))
    def d(name, os_, ns_):
        add = [x for x in ns_ if x not in os_]
        rem = [x for x in os_ if x not in ns_]
        if add: print('  +%s:' % name, ' | '.join(add))
        if rem: print('  -%s:' % name, ' | '.join(rem))
    d('列/标题', ot, nt)
    d('表单标签', ol, nl)
    d('按钮', ob, nb)
    d('描述项', od, nd)
