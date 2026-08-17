# -*- coding: utf-8 -*-
import re

PATH = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
html = open(PATH, encoding='utf-8').read()

problems = []

# global balance
o, c = html.count('<div'), html.count('</div>')
print('global div balance: %d / %d' % (o, c))
if o != c:
    problems.append('DIV IMBALANCE')

# split cards
cards = re.findall(r'<div class="card[^"]*">.*?</div>\s*</div>', html, re.S)
# more reliable: find each card block by rough detection
card_blocks = re.split(r'(?=<div class="card )', html)
card_blocks = [b for b in card_blocks if b.startswith('<div class="card ')]

print('card blocks found:', len(card_blocks))

s0_region = html[html.find('今日焦点'):html.find('重磅信息')]
s1_region = html[html.find('重磅信息'):html.find('监管政策动态')]
s2_region = html[html.find('监管政策动态'):html.find('竞争对手动态')]
s7_region = html[html.find('关键时间线'):html.find('待办跟踪与行动建议')]
s8_region = html[html.find('待办跟踪与行动建议'):html.find('</body>')]

def date_tags(region):
    return re.findall(r'<span class="date-tag">([\d.-]+)</span>', region)

print('\n=== date-tag audit ===')
print('S0 date-tags:', date_tags(s0_region))
print('S1 date-tags:', date_tags(s1_region))
print('S2 date-tags:', date_tags(s2_region))
print('S7 timeline dates:', re.findall(r'timeline-date">(\d{4}-\d{2}-\d{2})', s7_region))
print('S8 date-tags:', date_tags(s8_region))

# S0 must be all 07-13
for d in date_tags(s0_region):
    if d != '07-13':
        problems.append('S0 has non-07-13 date-tag: %s' % d)

# S1/S2 must be >= 06-29 (T-14 from 07-13)
def to_ymd(s):
    parts = s.split('-')
    if len(parts) == 3:
        y, m, dd = parts
    else:
        y, m, dd = '2026', parts[0], parts[1]
    return int(y), int(m), int(dd)
def ge(d, lim):
    return to_ymd(d) >= to_ymd(lim)
for d in date_tags(s1_region) + date_tags(s2_region):
    if not ge(d, '06-29'):
        problems.append('S1/S2 date-tag older than T-14: %s' % d)

# S7 timeline oldest
s7dates = re.findall(r'timeline-date">(\d{4}-\d{2}-\d{2})', s7_region)
if s7dates:
    oldest = min(s7dates)
    if to_ymd(oldest) < to_ymd('06-29'):
        problems.append('S7 has item older than T-14: %s' % oldest)
    print('S7 item count:', len(s7dates), '| oldest:', oldest, '| newest:', max(s7dates))
    if len(s7dates) > 12:
        problems.append('S7 exceeds 12 items: %d' % len(s7dates))

# structural: each card top must contain card-meta with priority-tag + date-tag
for i, blk in enumerate(card_blocks):
    if '<div class="card-top">' not in blk:
        problems.append('card %d missing card-top' % i)
        continue
    if '<div class="card-meta">' not in blk:
        problems.append('card %d missing card-meta wrapper' % i)
    if '<div class="card-body">' not in blk:
        problems.append('card %d missing card-body' % i)
    # P0 must have action-box
    if 'priority-tag urgent' in blk and 'action-box' not in blk:
        problems.append('card %d is P0 but missing action-box' % i)

# S8 P0 card (上半年公募业绩出炉 07-01) must still have action-box
if '腾安行动建议' not in s8_region:
    problems.append('S8 missing action content')

print('\n=== counts ===')
print('S0 cards:', s0_region.count('<!-- S0 Card'))
print('S1 cards:', s1_region.count('<!-- S1 Card'))
print('S2 cards:', s2_region.count('<!-- S2' ) )
print('S8 cards:', s8_region.count('<!-- S8 Card'))
print('S7 timeline items:', len(s7dates))

print('\n=== RESULT ===')
if problems:
    print('PROBLEMS FOUND:')
    for p in problems:
        print('  -', p)
else:
    print('ALL CHECKS PASSED ✅')
