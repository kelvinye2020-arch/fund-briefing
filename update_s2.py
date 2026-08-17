import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义S2部分的新内容（删除06-05条目，保留06-12和06-13的条目）
new_s2 = '''  <!-- ============ Section 2: 监管政策 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏛️</div>
      <span class="section-title">监管政策动态</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">最高优先级</span>
    </div>

    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会6/13发布《公募基金高质量发展三年行动计划（2026-2028）》+销售费用管理规定同步实施</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>三年行动计划：</b>6月13日，证监会正式发布《公开募集证券投资基金行业高质量发展三年行动计划（2026-2028）》，明确2026-2028年行业改革路线图，是继2025年5月《推动公募基金高质量发展行动方案》后首份<b>三年期系统性纲领文件</b>。重点方向：完善业绩比较基准约束、深化费率改革、强化长期评价导向、提升合规风控、支持中长期资金入市。<br>
          <b>销售费用新规：</b>同步实施《公募基金销售与服务费用管理规定》，进一步压降认申购费及销售服务费。这是费率改革"三步走"的<b>第三阶段</b>。各基金公司需在3个月内提交落实方案。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">行业纲领：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 研究三年行动计划对腾安代销业务模式的影响，提前规划收费模式转型；<br>
            ② 销售费用新规实施→评估腾安代销佣金结构是否需要调整。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 中基协6/12连发两文：适当性管理细则（6个月改造期）+可持续投资策略指引（即日实施）</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-12</span>
          </div>
        </div>
        <div class="card-body">
          <b>适当性管理细则（中基协发〔2026〕13号）：</b>6月12日发布，要求销售机构在<b>6个月内</b>（2026年12月12日前）完成基金风险等级划分体系完善和系统改造。<br>
          <b>可持续投资策略指引（中基协发〔2026〕15号）：</b>同日发布并即日实施。不符合指引的基金需在<b>一年内</b>完成调整。<br>
          <b>合规成本双升：</b>适当性改造+可持续投资调整→IT和合规成本上升→中小代销机构压力加大→行业集中度进一步提升。
        </div>
        <div class="card-footer">
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27826.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·适当性细则</span></a>
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27825.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·可持续指引</span></a>
          <span class="impact-tag high">合规升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 立即启动适当性系统改造项目，确保12月12日前完成；<br>
            ② 评估腾安ESG/可持续主题基金产品线布局机会。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 37万亿公募基金行业迎信披新规：新增披露7年、10年长期业绩</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>信披新规：</b>3月13日，证监会发布修订后的《公开募集证券投资基金信息披露内容与格式准则第2号—定期报告的内容与格式》，自2026年5月1日起实施。新规核心变化：不再披露过去1个月的业绩，但需披露产品在过去<b>7年、10年</b>的中长期业绩。<br>
          <b>行业影响：</b>①引导行业重视长期投资理念→缓解追逐短期排名的浮躁心态；②新增股票换手率数据披露→强化投资行为稳定性信息揭示；③删除大量重复信披内容→减轻行业机构负担。<br>
          <b>对基金行业影响：</b>信披新规引导长期投资→腾安在基金评价和推荐时，应更关注中长期业绩，减少短期排名导向。
        </div>
        <div class="card-footer">
          <a href="https://www.yicai.com/news/103086023.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经</span></a>
          <span class="impact-tag medium">信披改革：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 首批REITs指数基金获批·证监会6/17批准4只产品</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>产品获批：</b>6月17日，中国证监会官网显示，<b>首批4只跟踪中证REITs全收益指数的公募基金产品获批</b>。这是REITs指数基金这一创新产品的首次落地。<br>
          <b>政策意义：</b>丰富REITs投资工具→降低投资门槛→扩大投资者群体→提升REITs市场流动性。<br>
          <b>对基金行业影响：</b>REITs指数基金获批→丰富资产配置选择→腾安可提前布局代销。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag low">产品创新：低</span>
        </div>
      </div>



    </div>
  </div>'''

# 使用正则表达式替换S2部分
pattern = r'(?s)<!-- ============ Section 2: 监管政策 ============ -->.*?<!-- ============ Section 3: 竞争对手动态 ============ -->'
replacement = new_s2 + '\n  <!-- ============ Section 3: 竞争对手动态 ============ -->'
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("S2部分已更新")
