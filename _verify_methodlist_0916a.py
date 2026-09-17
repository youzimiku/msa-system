# -*- coding: utf-8 -*-
import io, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\index.html'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
URL = 'file:///C:/Users/youzi/Doubao/chats/2026-09-03/new-chat/MSA%E7%B3%BB%E7%BB%9F/index.html'
orig = io.open(path, encoding='utf-8').read()

# ---- 静态断言 ----
checks = [
    ("const [methodRows,setMethodRows]=useState([]);", "methodRows state"),
    ("onClick={addMethods}>确定</Button>", "确定按钮"),
    ("const addMethods=()=>{", "addMethods"),
    ("disabled:methodRows.some(r=>r.method===m)", "勾选框禁用联动"),
    ("const saveRow=(r)=>{", "saveRow"),
    ("const delRow=(r)=>{", "delRow"),
    ("setMethodRows(rs=>rs.filter(x=>x.method!==r.method)); setChecked(c=>c.filter(x=>x!==r.method));", "删除联动取消勾选"),
    ("locale={{emptyText:'未添加分析方法，请在上方勾选后点击「确定」'}}", "空态文案"),
    ("savedRows=methodRows.filter(r=>r.saved)", "提交取已保存行"),
    ("setMethodRows([]);", "切换清空列表"),
]
for k, n in checks:
    print('断言', n, ':', '存在' if k in orig else '缺失!!')
print('旧“勾选即展开”残留:', 'filter(m=>(isPersonGroup?[\'KAPPA\']:checked).indexOf(m)>=0).map(m=>{' in orig)

# ---- 渲染验证 ----
def render(page, mode='inst'):
    c = orig.replace("useState('instgroup')", "useState('" + page + "')")
    c = c.replace("const [batchModal,setBatchModal]=useState(null);",
                  "const [batchModal,setBatchModal]=useState({mode:'" + mode + "'});")
    io.open(path, 'w', encoding='utf-8').write(c)
    try:
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=8000', '--dump-dom', URL],
                           capture_output=True, encoding='utf-8', errors='replace', timeout=90)
        out = r.stdout or ''
        return out[out.find('<body'):] if '<body' in out else out
    finally:
        io.open(path, 'w', encoding='utf-8').write(orig)

def strip_scripts(s):
    return re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)

b = strip_scripts(render('plan'))
print('=== 器具弹窗 ===')
print('确定按钮:', '>确定<' in b)
print('表格表头 分析方法/人数/次数/样本数/操作:', all(x in b for x in ['>分析方法<','>人数<','>次数<','>样本数<','>操作<']))
print('空态文案:', '未添加分析方法' in b)
print('勾选框标签(GRR):', 'GRR' in b)

b2 = strip_scripts(render('plan', mode='person'))
print('=== 人员弹窗 ===')
print('KAPPA 勾选框存在:', 'KAPPA' in b2)
print('人员弹窗无 ant-checkbox-wrapper-disabled(初始应可勾选):', 'ant-checkbox-wrapper-disabled' not in b2)
print('RESTORED')
