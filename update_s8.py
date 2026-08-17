import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义S8部分的新内容（根据6月22日最新资讯更新待办事项）
new_s8 = '''  <!-- ============ Section 8: 待办跟踪 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fffbeb;color:var(--warning);">📋</div>
      <span class="section-title">腾安行动建议待办</span>
      <span class="section-badge" style="background:var(--warning-light);color:var(--warning);">Action Required</span>
    </div>

    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 纳指ETF溢价风险→提前准备客户解释话术</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>背景：</b>6月22日，多只纳指ETF因高溢价集体临停（10:30复牌），QDII溢价风险集中爆发。节后美股产品客户可能集中咨询。<br>
          <b>行动：</b>① 提前准备纳指ETF溢价风险解释话术；② 在App/公众号发布QDII溢价风险投教内容；③ 监控其他QDII产品溢价情况，提前预警。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">优先级：极高</span>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 LOF高溢价风险→排查腾安代销产品+制作投教内容</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>背景：</b>财通多只LOF连续涨停，溢价率飙升至20%+，极小流通盘催生虚假繁荣。此类脱离基本面的高溢价犹如"流沙上的博弈"。<br>
          <b>行动：</b>① 排查腾安代销的LOF产品是否存在类似溢价；② 制作"LOF溢价风险识别"投教内容；③ 关注舆情，防止投机情绪蔓延至腾安平台。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">优先级：极高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 FOF产品推荐→加大FOF产品推荐权重</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>背景：</b>FOF上半年新成立88只，合计发行规模1137.69亿，超越2021年历史峰值。全市场FOF基金平均收益率达5.28%，展现出稳健的抗风险能力。<br>
          <b>行动：</b>① 加大FOF产品推荐权重，特别是稳健型客户；② 评估腾安FOF产品货架是否齐备；③ 制作FOF产品投资指南投教内容。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">优先级：中高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 REITs指数基金→提前布局代销</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>背景：</b>首批4只跟踪中证REITs全收益指数的公募基金产品获批，REITs指数基金正式落地。未来REITs ETF可期。<br>
          <b>行动：</b>① 关注首批REITs指数基金发行进度；② 评估腾安代销REITs产品的可行性；③ 提前准备REITs产品投教内容。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">优先级：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 信披新规→调整基金评价逻辑</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>背景：</b>证监会发布修订后的信披准则，新增披露7年、10年长期业绩，删除1个月短期业绩披露要求。引导行业重视长期投资理念。<br>
          <b>行动：</b>① 调整腾安基金评价逻辑，更关注中长期业绩；② 减少短期排名导向；③ 在基金详情页突出显示7年/10年业绩。
        </div>
        <div class="card-footer">
          <span class="impact-tag low">优先级：低</span>
        </div>
      </div>

    </div>
  </div>'''

# 使用正则表达式替换S8部分
# 注意：S8部分在S7之后、Footer之前
pattern = r'(?s)<!-- ============ Section 8: 待办跟踪 ============ -->.*?<!-- Footer -->'
replacement = new_s8 + '\n  <!-- Footer -->'
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("S8待办跟踪已更新")
