# -*- coding: utf-8 -*-
"""独立复验（不依赖 update 脚本内部状态）"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = open('index.html', encoding='utf-8').read()
ok = True


def chk(cond, msg):
    global ok
    print(('  OK  ' if cond else ' FAIL ') + msg)
    if not cond:
        ok = False


print('=== 1. 结构 ===')
chk(s.count('<div') == s.count('</div>'),
    f"div 平衡 {s.count('<div')}/{s.count('</div>')}")
for k in ['Section 8', '待办跟踪', '腾安行动清单']:
    chk(k not in s, f'S8 残留检查: {k} 不存在')
for m in ['Section 0', 'Section 1', 'Section 2', 'Section 6', 'Section 7']:
    chk(m in s, f'marker {m} 存在')

print('=== 2. S0 ===')
a = s.index('<!-- S0 Card 1:'); b = s.index('Section 1: 重磅信息')
g = s[a:b]
d = re.findall(r'date-tag">([^<]*)', g)
chk(g.count('<div class="card ') == 4, f'卡片数=4 (实际{g.count(chr(60)+chr(100)+chr(105)+chr(118)+chr(32)+chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(61)+chr(34)+chr(99)+chr(97)+chr(114)+chr(100)+chr(32))})')
chk(all(x == '08-06' for x in d), f'date-tag 全 T+0: {d}')
chk(g.count('card-meta') == 4, f'card-meta 包裹 4/4 (实际{g.count("card-meta")})')
chk(g.count('source-tag') == 4, f'出处链接 4/4 (实际{g.count("source-tag")})')
chk(g.count('<div class="card p0">') == 1, 'P0 卡恰好 1 张')
chk(g.count('action-title') == 1, 'S0 段 action-box 恰好 1 个')
chk('<span class="section-title">今日焦点</span>' in s, 'section-title 精确等于「今日焦点」')
chk('<span class="section-context">8月6日 · 4条今日要闻</span>' in s, 'section-context 日期与条数正确')

print('=== 3. S1/S2 时效 (T-14 = 07-23) ===')
for nm, x, y, cap in [('S1', 'Section 1', 'Section 2', 6), ('S2', 'Section 2', 'Section 3', 4)]:
    sg = s[s.index(x):s.index(y)]
    ds = re.findall(r'date-tag">([^<]*)', sg)
    chk(len(ds) <= cap, f'{nm} 条数 {len(ds)} ≤ {cap}')
    chk(all(v >= '07-23' for v in ds), f'{nm} 无过期条目: {ds}')
    chk(sg.count('source-tag') >= len(ds), f'{nm} 出处链接齐备')

print('=== 4. S7 ===')
sg = s[s.index('Section 7'):]
d7 = re.findall(r'timeline-date">([^<]*)', sg)
t7 = re.findall(r'timeline-title">([^<]*)', sg)
chk(10 <= len(d7) <= 12, f'条数 {len(d7)} 在 10-12')
chk(len(d7) == len(set(d7)), '日期无重复')
chk(d7 == sorted(d7, reverse=True), '严格降序')
chk(all(v >= '2026-07-23' for v in d7), '无超 T-14 条目')
chk('timeline-desc' not in sg, '无 timeline-desc')
chk(max(len(x) for x in t7) <= 25, f'标题最长 {max(len(x) for x in t7)} 字 ≤25')
chk(len(d7) == len(t7), 'date/title 数量匹配')

print('=== 5. 行情口径一致性 ===')
chk(s.count('3878.43') >= 2, '沪指 3878.43 同时出现在 Stats Bar 与 S6')
chk('25915.82' in s and '54349.12' in s, '港股/美股 08-05 收盘已写入')
chk('08-05收盘' in s, 'S6 标注为收盘口径')

print()
print('RESULT:', 'ALL PASS' if ok else 'HAS FAILURES')
sys.exit(0 if ok else 1)
