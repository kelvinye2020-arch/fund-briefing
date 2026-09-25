import re
h = open('index.html', encoding='utf-8').read()
bounds = [('S0', '今日焦点'), ('S1', '重磅信息'), ('S2', '监管政策动态'),
          ('S3', '竞争对手动态'), ('S4', '行业趋势与市场数据'), ('S5', '金融科技与AI投顾'),
          ('S6', '市场行情速览'), ('S7', '关键时间线')]
pos = []
for n, t in bounds:
    pos.append((n, h.index(t)))
pos.append(('END', len(h)))
for i in range(len(pos) - 1):
    n, s = pos[i]
    e = pos[i + 1][1]
    seg = h[s:e]
    print('== %s: cards=%d date-tags=%s links=%d actionbox=%d timeline=%d' % (
        n, seg.count('<div class="card'), re.findall(r'date-tag">(\d{2}-\d{2})<', seg),
        len(re.findall(r'href="http', seg)), seg.count('action-box'),
        seg.count('<div class="timeline-item')))
s0 = h[pos[0][1]:pos[1][1]]
print('S0 titles:')
for t in re.findall(r'class="card-title">(.*?)</div>', s0):
    print('   ', t[:56])
print('S0 date-tag seq:', re.findall(r'date-tag">(\d{2}-\d{2})<', s0))
print('S7 items:')
for d, t in re.findall(r'timeline-date">(.*?)</div>\s*<div class="timeline-title">(.*?)</div>', h[pos[7][1]:]):
    print('   ', d, '|', t)
print('S1 titles:')
for t in re.findall(r'class="card-title">(.*?)</div>', h[pos[1][1]:pos[2][1]]):
    print('   ', t[:56])
print('S2 titles:')
for t in re.findall(r'class="card-title">(.*?)</div>', h[pos[2][1]:pos[3][1]]):
    print('   ', t[:56])
print('S5 titles:')
for t in re.findall(r'class="card-title">(.*?)</div>', h[pos[5][1]:pos[6][1]]):
    print('   ', t[:56])
