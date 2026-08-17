#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S7时间线清理：删除重复条目和超期条目"""
import re

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 删除重复的06-16条目（第3条，L1298-1306）
# ============================================================
dup_0616 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-16（多只QDII科技ETF停牌·6月新基发行创同期新高·A股科技延续强势）</div>
          <div class="timeline-title">纳指ETF易方达/国泰/景顺+创业板ETF富国因高溢价6/16停牌（10:30复牌）/ 6月前11天114只新基发行创历史同期新高 / A股今日上午创业板指+2.05%</div>
          <div class="timeline-desc">多只QDII科技ETF因二级市场交易价格明显高于IOPV（溢价率最高超22%）于6/16开市起停牌，10:30起复牌，停牌期间赎回业务照常办理。6月前11天114只新基发行创历史同期新高，上半年主动权益基金发行数量同比翻倍。A股今日上午科技延续强势，创业板指+2.05%，建筑材料板块领涨。</div>
        </div>
      </div>'''

# ============================================================
# 删除重复的06-15条目（第4条）
# ============================================================
dup_0615 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-15（多项公募新规落地·A股普涨科技收敛·中期分红热潮来袭）</div>
          <div class="timeline-title">主题投资风格管理指引+适当性细则修订+公私兼任禁令三文同落 / A股沪指4096(+1.61%)普涨 / 中期分红热潮数百家上市公司</div>
          <div class="timeline-desc">多项公募基金新规同日公布（新华社报道）：主题投资风格管理指引（12/1施行，12个月过渡期）将风格漂移软约束转为硬约束；适当性细则修订加强65周岁以上高风险基金销售管理；公私兼任禁令防范利益冲突。A股今日普涨，科技板块一枝独秀行情收敛，非科技板块获机构密集调研。中期分红热潮来袭，数百家上市公司发布中期分红预案。</div>
        </div>
      </div>'''

# ============================================================
# 删除06-02超期条目（第15条）
# ============================================================
old_0602 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-02（腾讯暴涨10.46%创2021来最大涨幅·恒生科技+4.72%·AI Agent突破）</div>
          <div class="timeline-title">腾讯控股+10.46%（AI Agent开发平台+云降价97.5%）/ 恒生科技+4.72% / A股创业板+2.66%深V修复</div>
          <div class="timeline-desc">腾讯单日暴涨10%创4年来最大涨幅，AI Agent开发平台+云降价97.5%双重催化。恒生科技大涨，美团+9%。A股探底回升，MLCC/CPO/机器人爆发。成交2.79万亿。成交额前20科技股全部收红。</div>
        </div>
      </div>'''

# 执行删除
if dup_0616 in content:
    content = content.replace(dup_0616, '\n')
    print('[OK] 删除重复06-16条目')
else:
    print('[WARN] 未找到重复06-16条目')

if dup_0615 in content:
    content = content.replace(dup_0615, '\n')
    print('[OK] 删除重复06-15条目')
else:
    print('[WARN] 未找到重复06-15条目')

if old_0602 in content:
    content = content.replace(old_0602, '\n')
    print('[OK] 删除超期06-02条目')
else:
    print('[WARN] 未找到超期06-02条目')

# 验证结果
s7_start = content.find('Section 7')
s7_end = content.find('Section 8')
s7 = content[s7_start:s7_end]
dates = re.findall(r'<div class="timeline-date">([^<]+)</div>', s7)
print(f'\n清理后S7时间线条目数: {len(dates)}')
for i, d in enumerate(dates):
    print(f'  {i+1}. {d}')

# 检查是否有超期（T-14=06-02）
overdue = [d for d in dates if ('06-01' in d or '05-' in d or '06-02' in d)]
if overdue:
    print(f'\n[WARN] 仍有超期条目: {overdue}')
else:
    print('\n[OK] 无超期条目')

# 写入文件
with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('\n[OK] index.html 已更新并保存')
