#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - S1重磅信息 + S2监管政策 更新脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# S1 重磅信息 - 新内容 (6 cards, T-14 内）
s1_new_cards = """
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
          <b>对基金行业影响：</b>FOF从"配角"走向舞台中央→资产配置需求上升→腾安可加大FOF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3970656.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">FOF爆发：高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批REITs指数基金获批·证监会6/17批准4只产品·商业REITs试点同步推出</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>产品获批：</b>6月17日，中国证监会批准<b>首批4只跟踪中证REITs全收益指数的公募基金产品</b>。同日，证监会宣布推出商业不动产REITs试点。<br>
          <b>政策背景：</b>2026陆家嘴论坛上，证监会主席吴清宣布支持推出主动ETF和商业REITs试点。<br>
          <b>对基金行业影响：</b>REITs指数基金+商业REITs试点→产品创新加速→腾安可提前布局相关产品代销。
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
          <b>额度发放：</b>央行副行长朱鹤新在2026陆家嘴论坛上表示，将<b>发放新一批QDII投资额度</b>。<br>
          <b>市场影响：</b>新一批QDII额度发放→QDII产品供给将增加→投资者海外资产配置选择进一步扩大。<br>
          <b>对基金行业影响：</b>①腾安可丰富QDII产品货架；②此前因额度不足暂停申购的QDII产品可能重新开放。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag medium">QDII扩容：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 德邦基金迎新董事长·年内近20家公募"换帅"·行业高管变更保持高频</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-19</span>
          </div>
        </div>
        <div class="card-body">
          <b>高管变更：</b>6月19日，德邦基金公告，尉迟平新任公司董事长，原代董事长武晓春于同日卸任。<br>
          <b>行业趋势：</b>2026年以来，公募行业高管变更保持高频，年内近20家公募"换帅"。反映出行业在转型期的治理调整需求。<br>
          <b>对基金行业影响：</b>高管变更高频→行业转型深化→公司治理结构优化→长期有利于行业健康发展。
        </div>
        <div class="card-footer">
          <a href="https://tanliu@stcn.com/article/detail/3970658.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag low">高管变更：低</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 从千亿抢购到千元限购·公募行业从"重规模"向"重回报"转型</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>行业转型：</b>证监会主席吴清强调基金行业应坚持客户为本，增强逆周期思维，遏制"冲规模、赚快钱"等顽疾。标志着公募从"重规模"向"重回报""以持有人利益为本"转型。<br>
          <b>新发克制：</b>2026年以来，新成立基金729只，合计规模5696亿元，不足2021年同期一半。百亿级"大爆款"未再出现。<br>
          <b>限购潮：</b>多只绩优基金将单日申购上限降至1万元甚至1000元。今年业绩排名前十的主动权益基金中，七只处于暂停申购或暂停大额申购状态。<br>
          <b>对基金行业影响：</b>"限购"是投资者保护机制→行业理念变革→腾安在基金筛选时应更关注长期业绩和投资者回报。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/wm/2026-06-22/doc-iniefzfw0327924.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag low">理念转型：低</span>
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
          <b>策略失效：</b>近两年来，随着A股市场结构性行情极致演绎，基金的多元配置策略越来越难。<br>
          <b>融合趋势：</b>业内普遍认为，公募投研正在打破赛道和均衡二选一的固有认知，两种投资框架逐步融合发展。<br>
          <b>对基金行业影响：</b>多元与赛道策略融合→基金经理投资框架升级→腾安在基金筛选和推荐时，需关注基金经理的框架进化能力。
        </div>
        <div class="card-footer">
          <a href="https://egs.stcn.com/news/detail/2304821.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯</span></a>
          <span class="impact-tag low">策略演变：低</span>
        </div>
      </div>
"""

# S2 监管政策 - 新内容 (4 cards, T-14 内）
s2_new_cards = """
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会6/13发布《公募基金高质量发展三年行动计划（2026-2028）》+销售费用管理规定同步实施</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>三年行动计划：</b>6月13日，证监会正式发布《公开募集证券投资基金行业高质量发展三年行动计划（2026-2028）》，明确2026-2028年行业改革路线图。<br>
          <b>销售费用新规：</b>同步实施《公募基金销售与服务费用管理规定》，进一步压降认申购费及销售服务费。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">行业纲领：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 研究三年行动计划对腾安代销业务模式的影响；<br>
            ② 销售费用新规实施→评估腾安代销佣金结构是否需要调整。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 中基协6/12连发两文：适当性管理细则（6个月改造期）+可持续投资策略指引</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-12</span>
          </div>
        </div>
        <div class="card-body">
          <b>适当性管理细则：</b>要求销售机构在<b>6个月内</b>（2026年12月12日前）完成基金风险等级划分体系完善和系统改造。<br>
          <b>可持续投资策略指引：</b>同日发布并即日实施。不符合指引的基金需在<b>一年内</b>完成调整。
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
          <div class="card-title">🟡 沪深交易所6/17发布主动ETF业务指引·管理人准入：5年经验+100亿规模</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>指引落地：</b>6月17日，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。<br>
          <b>准入门槛：</b>管理人需具备<b>5年以上</b>主动权益公募基金管理运作经验，近3年平均主动权益公募基金管理规模不少于<b>100亿元</b>。<br>
          <b>投资要求：</b>基金投资组合持有证券数量不少于<b>30只</b>，前十大持仓合计占比不超过60%。<br>
          <b>对基金行业影响：</b>主动ETF有望成为ETF市场新增长引擎→产品创新加速→腾安可关注主动ETF产品布局机会。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/730782" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">产品创新：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 37万亿公募基金行业迎信披新规：新增披露7年、10年长期业绩</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>信披新规：</b>证监会修订《公开募集证券投资基金信息披露内容与格式准则第2号》，自2026年5月1日起实施。新规核心变化：不再披露过去1个月的业绩，但需披露产品在过去<b>7年、10年</b>的中长期业绩。<br>
          <b>对基金行业影响：</b>信披新规引导长期投资→腾安在基金评价和推荐时，应更关注中长期业绩，减少短期排名导向。
        </div>
        <div class="card-footer">
          <a href="https://www.yicai.com/news/103086023.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经</span></a>
          <span class="impact-tag low">信披改革：低</span>
        </div>
      </div>
"""

# 更新 S1
s1_start = html.find('<!-- ============ Section 1: 重磅信息 ============ -->')
s2_start = html.find('<!-- ============ Section 2: 监管政策 ============ -->')

if s1_start > 0 and s2_start > 0:
    # 提取 S1 之前的 HTML
    html_before_s1 = html[:s1_start]
    
    # 构建新的 S1 部分
    new_s1 = f'''  <!-- ============ Section 1: 重磅信息 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏆</div>
      <span class="section-title">重磅信息</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">近两周核心</span>
    </div>

    <div class="card-grid">
{s1_new_cards}
    </div>
  </div>

'''
    
    # 提取 S2 及之后的 HTML
    html_from_s2 = html[s2_start:]
    
    # 合并（暂时不包含新 S2）
    html_temp = html_before_s1 + new_s1 + html_from_s2
    
    print("✅ S1 重磅信息已更新（6张卡片）")
else:
    print("❌ 未找到 S1 或 S2 标记，S1 更新失败")
    html_temp = html

# 更新 S2
s2_start_new = html_temp.find('<!-- ============ Section 2: 监管政策 ============ -->')
s3_start_new = html_temp.find('<!-- ============ Section 3: 竞争对手动态 ============ -->')

if s2_start_new > 0 and s3_start_new > 0:
    # 提取 S2 之前的 HTML
    html_before_s2 = html_temp[:s2_start_new]
    
    # 构建新的 S2 部分
    new_s2 = f'''  <!-- ============ Section 2: 监管政策 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏛️</div>
      <span class="section-title">监管政策动态</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">最高优先级</span>
    </div>

    <div class="card-grid">
{s2_new_cards}
    </div>
  </div>

'''
    
    # 提取 S3 及之后的 HTML
    html_from_s3 = html_temp[s3_start_new:]
    
    # 合并
    new_html = html_before_s2 + new_s2 + html_from_s3
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("✅ S2 监管政策已更新（4张卡片）")
    print("   - 三年行动计划 (06-13)")
    print("   - 适当性细则 (06-12)")
    print("   - 主动ETF业务指引 (06-17)")
    print("   - 信披新规 (06-22报道)")
else:
    print("❌ 未找到 S2 或 S3 标记，S2 更新失败")
