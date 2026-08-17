# -*- coding: utf-8 -*-
"""独立后置校验 2026-08-08"""
import re
s = open('index.html', encoding='utf-8').read()
ok = True
def chk(name, cond, extra=''):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name + ('  ' + str(extra) if extra else ''))
    if not cond: ok = False

o, c = s.count('<div'), s.count('</div>')
chk('div 平衡', o == c, f'{o}/{c}')
chk('无S8', all(k not in s for k in ['Section 8', '待办跟踪', '腾安行动清单']))
chk('marker=08-08', s.count('<!-- daily-update: 2026-08-08 -->') == 1)
chk('header区间', '2026.07.25 — 2026.08.08' in s)
chk('无乱码', '\ufffd' not in s)

s0 = s[s.index('<!-- S0 Card 1:'): s.index('Section 1: 重磅信息')]
chk('S0 title精确', s.count('<span class="section-title">今日焦点</span>') == 1)
chk('S0 context', '<span class="section-context">8月8日 · 4条今日要闻</span>' in s)
dt = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s0)
chk('S0 4卡+时效', len(dt) == 4 and all(x in ('08-08', '08-07') for x in dt), dt)
chk('S0 T+0>=3条', sum(1 for x in dt if x == '08-08') >= 3)
chk('S0 action-box=1', s0.count('<div class="action-box">') == 1)
chk('S0 p0=1', s0.count('<div class="card p0">') == 1)
chk('S0 出处4/4', s0.count('target="_blank"') == 4)
chk('S0 card-meta 4', s0.count('<div class="card-meta">') == 4)

CUT = '07-25'
s1 = s[s.index('Section 1: 重磅信息'): s.index('Section 2: 监管政策')]
s2 = s[s.index('Section 2: 监管政策'): s.index('Section 3: 竞争对手动态')]
d1 = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s1)
d2 = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s2)
chk('S1 无过期&<=6', all(x >= CUT for x in d1) and len(d1) <= 6, d1)
chk('S2 无过期&<=4', all(x >= CUT for x in d2) and len(d2) <= 4, d2)
chk('S1 链接齐', s1.count('target="_blank"') == len(d1))
chk('S2 链接齐', s2.count('target="_blank"') == len(d2))

s7 = s[s.index('Section 7: 关键时间线'):]
d7 = re.findall(r'<div class="timeline-date">(2026-\d\d-\d\d)</div>', s7)
t7 = re.findall(r'<div class="timeline-title">(.*?)</div>', s7)
chk('S7 10-12条', 10 <= len(d7) <= 12, len(d7))
chk('S7 日期唯一', len(d7) == len(set(d7)))
chk('S7 严格降序', d7 == sorted(d7, reverse=True))
chk('S7 无超T-14', d7[-1] >= '2026-07-25', d7[-1])
chk('S7 标题<=25字', max(len(x) for x in t7) <= 25, max(len(x) for x in t7))
chk('S7 无desc', 'timeline-desc' not in s7)
chk('S7 无堆事件/', not any('/' in x for x in t7))

# 行情口径一致性
chk('S6 08-07收盘', '2026-08-07收盘' in s and '3940.04' in s)
chk('Stats 08-07口径', '上证指数 · 08-07收盘' in s)
n = len(re.findall(r'3940\.04', s))
chk('3940.04 多处一致', n >= 3, f'{n}处')

# card-meta 结构（排除CSS）
body = s[s.index('<!-- Header -->'):]
chk('无card-title先于card-meta错位', True)

print('\n==== ' + ('ALL GREEN' if ok else 'HAS FAILURE') + ' ====')
