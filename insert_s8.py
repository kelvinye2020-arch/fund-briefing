#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在 S7 和 Footer 之间插入 S8 待办跟踪
"""

filepath = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# S8 待办跟踪 HTML
s8_html = """
  <!-- ============ Section 8: 待办跟踪 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#eef2ff;color:var(--info);">📋</div>
      <span class="section-title">待办跟踪与行动建议</span>
      <span class="section-badge" style="background:var(--info-light);color:var(--info);">腾安行动清单</span>
    </div>

    <div class="card-grid">
      
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 浮费基金业绩分化·三倍基诞生·费率机制正式生效</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>首批浮费基金一周年，华商致远回报A成"三倍基"（316.56%），6只产品仍亏损（最高-12.84%）。运作满一年后费率按业绩分档：1.5%（跑赢基准6%+）/ 1.2%（介于之间）/ 0.6%（跑输基准3%+）。<br>
          <b>腾安行动建议：</b>① 评估腾安代销的浮费基金业绩表现，准备客户沟通话术；② 在基金详情页突出费率机制说明，避免销售误导；③ 关注浮动费率基金作为差异化产品卖点的营销机会。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理腾安代销浮费基金清单及业绩表现→产品部<br>
            ② 制作浮费基金费率机制说明话术→营销部<br>
            ③ 评估浮费基金作为差异化卖点的营销方案→运营部
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>QDII限购力度再加码，易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>，华宝海外科技股票(QDII-LOF)降至20元。超百只QDII限购百元及以下。近一年QDII平均收益22%，45只净值翻倍。<br>
          <b>腾安行动建议：</b>① 梳理腾安可代销的有额度QDII产品清单；② 准备QDII替代方案话术（港股通、互认基金、跨境ETF等）；③ 关注新一批QDII额度发放进展，提前布局。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理有额度的QDII产品清单→产品部<br>
            ② 制作QDII替代方案话术（港股通/互认基金）→营销部<br>
            ③ 跟踪新一批QDII额度发放进展→产品部
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 央行5000亿MLF操作·净投放2000亿·连续两月加量续作</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-25</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>6月25日央行开展5000亿元1年期MLF操作，净投放2000亿元，为连续第二个月加量续作。市场流动性偏松局面已扭转，MLF加量旨在应对季末流动性压力、支持政府债券发行、助力银行加大信贷投放。<br>
          <b>腾安行动建议：</b>① 债市环境友好→债券基金和货币基金管理难度下降→可适当增加债券基金推荐权重；② 关注季末资金面波动对货币基金收益的影响。
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 主动ETF业务指引落地·沪深交易所6/17发布·腾安可关注产品布局机会</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>沪深交易所发布《主动管理交易型开放式证券投资基金业务指引》，管理人需具备5年以上主动权益经验+近3年平均规模不少于100亿元。主动ETF有望成为ETF市场新增长引擎。<br>
          <b>腾安行动建议：</b>① 跟踪符合准入门槛的基金公司主动ETF产品申报进展；② 提前研究主动ETF的代销价值和客户接受度；③ 关注主动ETF与指数ETF的差异化定位。
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 债券ETF规模首超8500亿·科创债ETF+基准做市信用债ETF双引擎</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>债券ETF总规模突破8500亿元，同比增180%。科创债ETF（2941亿元）和基准做市信用债ETF（1413亿元）是双引擎。头部公司份额超70%。<br>
          <b>腾安行动建议：</b>① 加大债券ETF产品推荐权重；② 重点布局科创债ETF和基准做市信用债ETF；③ 关注债券ETF作为"交易+配置"双功能载体的客户价值。
        </div>
      </div>

    </div>
  </div>
"""

# 在 S7 结束和 Footer 之间插入 S8
# 找到 S7 的结束位置：</div>\n  </div>\n<!-- Footer -->
marker = '  </div>\n<!-- Footer -->'
if marker in content:
    new_content = content.replace(marker, s8_html + '\n  </div>\n<!-- Footer -->', 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ S8 待办跟踪插入成功！")
    print(f"   插入位置：S7 结束后、Footer 前")
else:
    print("❌ 插入标记未找到，尝试备用方案...")
    # 备用方案：查找 "<!-- Footer -->" 并向前插入
    footer_pos = content.find('<!-- Footer -->')
    if footer_pos > 0:
        new_content = content[:footer_pos] + s8_html + '\n' + content[footer_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ S8 待办跟踪插入成功（备用方案）！")
    else:
        print("❌ Footer 标记也未找到，需要手动插入 S8")
