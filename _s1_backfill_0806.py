# -*- coding: utf-8 -*-
"""S1 补位：清理 07-22 过期卡后回补一条 T-14 内新条目（指数增强基金规模首破3200亿·上证报07-29）"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'index.html'
s = open(P, encoding='utf-8').read()
O0, C0 = s.count('<div'), s.count('</div>')
print('before:', O0, C0)
assert O0 == C0

ANCHOR = '      <!-- S1 Card NEW: 半年报披露公募布局绩优股'
assert s.count(ANCHOR) == 1, 'S1 anchor not unique'

CARD = '''      <!-- S1 Card NEW: 指数增强基金规模首破3200亿元 (07-29) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">07-29</span>
          </div>
          <div class="card-title">🟡 指数增强基金规模首破3200亿元·二季度末3233.02亿环比增12%·连续5个季度增长</div>
        </div>
        <div class="card-body">
          上海证券报7月29日报道，Choice数据显示截至二季度末公募指数增强基金规模达3233.02亿元，较一季度末的2886.73亿元增长12%，为该品类连续第5个季度实现规模增长，数量同步突破千只。业绩驱动明显：近一年回报跑赢同期业绩比较基准的指增产品达670只、占比超六成，其中88只跑赢基准10个百分点以上；嘉实中证半导体产业指数增强发起式近一年回报约166%居同类第一、二季度规模增47.7亿元晋级百亿，汇添富中证芯片产业指数增强发起式近一年回报超130%、二季度规模增幅约150%。截至7月28日年内新成立指增基金110只（份额分开计算），涉及约40家基金公司；已布局该赛道的基金公司超百家、全行业占比逾六成，华泰保兴、泰信等中小公募借此填补纯指数工具空白、打造差异化第二增长曲线。业内认为，指增兼具贝塔跟踪与阿尔法挖掘双重特性，适配机构与长期资金配置需求，但竞争核心已转向长期稳定超额收益能力，需严格控制行业与市值偏离度。
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-07/29/content_2249584.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">产品趋势：中</span>
        </div>
      </div>

'''
assert CARD.count('<div') == CARD.count('</div>') == 6, 'new card must be 6/6 self-balanced'

s = s.replace(ANCHOR, CARD + ANCHOR, 1)

O1, C1 = s.count('<div'), s.count('</div>')
print('after :', O1, C1, 'delta', O1 - O0)
assert O1 == C1 and O1 - O0 == 6, 'unexpected div delta'

sg = s[s.index('Section 1'):s.index('Section 2')]
ds = re.findall(r'date-tag">([^<]*)', sg)
print('S1 dates:', ds, 'links:', sg.count('source-tag'))
assert len(ds) == 4 and all(d >= '07-23' for d in ds), 'S1 date rule violated'
assert sg.count('source-tag') == 4, 'S1 links mismatch'
assert sg.count('card-meta') == 4, 'S1 card-meta mismatch'
assert '\ufffd' not in s, 'U+FFFD corruption detected'

open(P, 'w', encoding='utf-8').write(s)
print('WRITTEN OK')
