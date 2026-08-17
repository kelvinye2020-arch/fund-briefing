import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义S1部分的新内容
new_s1 = '''  <!-- ============ Section 1: 重磅信息 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏆</div>
      <span class="section-title">重磅信息</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">近两周核心</span>
    </div>

    <div class="card-grid">

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 多只纳指ETF 6/22集体临停！溢价率最高超22%·QDII溢价风险集中爆发</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>集体临停：</b>6月22日，汇添富纳指ETF、纳指ETF广发、纳指ETF嘉实、纳指ETF易方达、纳斯达克100ETF大成相继公告，基金于今日开市起停牌，<b>10:30起复牌</b>。停牌原因：二级市场交易价格明显高于IOPV，出现较大幅度溢价。<br>
          <b>风险提示：</b>基金公司郑重提醒，若6/22二级市场交易价格溢价幅度未有效回落，基金有权申请盘中临时停牌、延长停牌时间及连续停牌等措施。<br>
          <b>对基金行业影响：</b>①QDII溢价风险集中爆发→节后美股产品客户可能集中咨询；②高溢价不可持续→投资者教育需求上升；③监管对QDII溢价监控趋严。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.cn/2026-06-22/detail-iniefqsa0460126.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·21世纪</span></a>
          <span class="impact-tag high">QDII溢价：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 纳指ETF集体临停→提前准备QDII溢价风险解释话术；<br>
            ② 在App/公众号发布QDII溢价风险投教内容；<br>
            ③ 监控其他QDII产品溢价情况，提前预警。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 多只LOF连续涨停·高溢价20%+·极小流通盘催生虚假繁荣</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>LOF异动：</b>近期，财通基金旗下多只LOF产品场内份额连续涨停，溢价率飙升至<b>20%以上</b>。表面看与基金经理金梓才押注AI算力赛道、近一年回报近<b>530%</b>相关。<br>
          <b>高溢价真相：</b>实则是<b>极小流通盘下的资金博弈</b>——部分产品仅需数十万元即可拉涨停。基金公司虽已紧急限购、频频停牌，但社交媒体放大效应下，"堵住场外"反而可能加剧投机情绪。<br>
          <b>风险警示：</b>此类脱离基本面的高溢价犹如"流沙上的博弈"，一旦情绪退潮，投资者将面临<b>价格回归与溢价破裂的双重风险</b>。
        </div>
        <div class="card-footer">
          <a href="https://admin@stcn.com/article/detail/3970809.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag high">LOF溢价：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 排查腾安代销的LOF产品是否存在类似溢价；<br>
            ② 制作"LOF溢价风险识别"投教内容；<br>
            ③ 关注舆情，防止投机情绪蔓延。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 FOF上半年新发规模1137亿·超越2021年峰值·低利率催化+银行渠道发力</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>爆发式增长：</b>Wind数据显示，截至6月20日，2026年以来新成立FOF基金已达<b>88只</b>，合计发行规模高达<b>1137.69亿元</b>，超越2021年创下的<b>1083.62亿元</b>历史峰值。<br>
          <b>业绩支撑：</b>全市场FOF基金平均收益率达<b>5.28%</b>，易方达优势回报A以<b>52.20%</b>收益率位居榜首。<br>
          <b>对基金行业影响：</b>FOF从"配角"走向舞台中央→资产配置需求上升→腾安可加大FOF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3970656.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">FOF爆发：高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批REITs指数基金获批！证监会6/17批准4只跟踪中证REITs全收益指数产品</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>产品获批：</b>6月17日，中国证监会官网显示，<b>首批4只跟踪中证REITs全收益指数的公募基金产品获批</b>。这是REITs指数基金这一创新产品的首次落地。<br>
          <b>政策背景：</b>2025年12月，证监会发布通知，指出丰富覆盖REITs的指数体系，支持基金管理人开发挂钩相关指数的基金产品。<br>
          <b>对基金行业影响：</b>①REITs指数基金获批→丰富资产配置选择；②未来REITs ETF可期；③腾安可提前布局REITs指数基金代销。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag medium">产品创新：中高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 国家外汇局将发放新一批QDII投资额度·QDII产品供给将增加</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-18~22</span>
          </div>
        </div>
        <div class="card-body">
          <b>额度发放：</b>近日，中国人民银行副行长、国家外汇管理局局长朱鹤新在2026陆家嘴论坛上表示，将围绕"四个深化"，持续提升资本项目开放水平，<b>将发放新一批QDII投资额度</b>。<br>
          <b>市场影响：</b>新一批QDII额度发放→QDII产品供给将增加→投资者海外资产配置选择进一步扩大。<br>
          <b>对基金行业影响：</b>①腾安可丰富QDII产品货架；②此前因额度不足暂停申购的QDII产品可能重新开放；③竞争加剧→QDII产品费率可能进一步下行。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag medium">QDII扩容：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多元策略基金业绩承压·多元与赛道策略走向融合·投研框架升级</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>策略失效：</b>近两年来，随着A股市场结构性行情极致演绎，基金的多元配置策略越来越难。公募、游资等机构高度聚焦AI、算力等少数赛道，导致固守分散持仓策略的基金收益持续低迷。<br>
          <b>融合趋势：</b>业内普遍认为，公募投研正在打破赛道和均衡二选一的固有认知，两种投资框架逐步融合发展。<br>
          <b>对基金行业影响：</b>多元与赛道策略融合→基金经理投资框架升级→腾安在基金筛选和推荐时，需关注基金经理的框架进化能力。
        </div>
        <div class="card-footer">
          <a href="https://egs.stcn.com/news/detail/2304821.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯</span></a>
          <span class="impact-tag low">策略演变：低</span>
        </div>
      </div>

    </div>
  </div>'''

# 使用正则表达式替换S1部分
pattern = r'(?s)<!-- ============ Section 1: 重磅信息 ============ -->.*?<!-- ============ Section 2: 监管政策 ============ -->'
replacement = new_s1 + '\n  <!-- ============ Section 2: 监管政策 ============ -->'
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("S1部分已更新")
