# -*- coding: utf-8 -*-
"""
_update_0907.py — 2026-09-07（周一）daily-update
范围：header 数据区间 + S0 今日焦点(4条T+0) + S7 时间线(12条)
S1/S2/S6/Stats Bar 本次不动（周末无新交易日；S1=6/S2=4 均 T-14 内）
"""
import re
from datetime import date, timedelta

HTML = 'index.html'
src = open(HTML, encoding='utf-8').read()
orig_len = len(src)

today = date.today()
assert today == date(2026, 9, 7), f'日期不符：{today}'
upper = today.strftime('%Y.%m.%d')
lower = (today - timedelta(days=14)).strftime('%Y.%m.%d')

# ---------- 1. header 数据区间（动态正则，不依赖旧值） ----------
badge_new = f'📅 数据区间：{lower} — {upper}（每日更新）'
src2 = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge_new, src)
assert src2 != src, 'header 数据区间未命中替换'
src = src2

# ---------- 2. daily-update 注释 ----------
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', f'<!-- daily-update: {today.strftime("%Y-%m-%d")} -->', src)

# ---------- 3. S0 今日焦点 整块替换 ----------
S0_NEW = '''        <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月7日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
      <!-- S0 Card 1 (09-07 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会就《私募投资基金募集监督管理办法（征求意见稿）》公开征求意见·私募募集入口“设卡”</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          证监会9月4日就《私募投资基金募集监督管理办法（征求意见稿）》公开征求意见，共七章45条，意见反馈截止2026年10月4日；这是6月国办《关于加强监管防范风险促进私募投资基金高质量发展的指导意见》印发后私募领域首个管理办法。<br>
          <b>合格投资者标准：</b>个人须具有2年以上证券/基金/期货/股权投资经历，且满足家庭金融资产≥500万、家庭金融净资产≥300万、近三年年均收入≥50万之一；投向单一标的、境外资产、场外衍生品等高风险产品门槛更高（4年经历＋金融资产≥1000万/净资产≥600万）。<br>
          <b>募集规范：</b>管理人应自行募集或委托持牌机构募集，严禁通过其他机构或个人募集；严禁保本保收益、诱导性宣传、虚假宣传；单只基金投资者≤200人、首期实缴≥100万；不得通过互联网平台向不特定对象推介。<br>
          <b>对腾安启示：</b>私募“1+N+X”规则体系加速成型，合格投资者门槛抬升＋募集端从自律升级为行政监管，代销合作须严把私募管理人合规与适当性准入。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/786251" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-07</span></a>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 合规前置→跟踪私募募集办法正式稿，梳理代销私募产品的合格投资者核验与适当性流程；<br>
            ② 货架体检→对在售私募产品做募集合规性自查，剔除不合规合作机构；<br>
            ③ 投教联动→借“合格投资者门槛抬升”节点，强化高净值客户适当性教育与风险揭示。
          </div>
        </div>
      </div>

      <!-- S0 Card 2 (09-07 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 个人养老金基金扩容“固收+”·含权二级债基/偏债混合纳入·首批每家限报1只</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报9月7日电，多家基金公司收到监管《做好含权二级债基、偏债混合基金纳入个人养老金基金产品名录工作的通知》，推动符合条件的含权二级债基、偏债混合基金纳入名录。<br>
          <b>六项标准：</b>①成立满3年且每日开放申购②最近4季度末规模均≥5亿③偏股仓位（二级债基/偏债FOF≥5%、普通偏债混合≥10%）且偏股+转债合计≤20%/30%④近3年最大回撤优于同类中位数⑤机构持有≤80%且前五大≤50%⑥管理人最近一期分类评价不为C类。<br>
          <b>节奏安排：</b>首批每家限报1只、9月8日前报送，后续按季度常态化筛选＋动态评估奖优惩劣；支持Y份额管理费/托管费费率优惠。截至二季度末个人养老金基金321只、Y份额规模284.92亿元（较年末+99.48亿）。<br>
          <b>对腾安启示：</b>养老金产品谱系补齐“固收+”中低波品类，代销货架与税优投教场景同步打开，应前置评估符合六标准产品的引入。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/etf/2026/09/07/detail_2026090710037207.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·09-07</span></a>
        </div>
      </div>

      <!-- S0 Card 3 (09-07 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 农业板块异军突起·公募逆周期布局效果显现·多只粮食ETF两位数涨幅</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          证券时报9月7日（记者赵梦桥），冷门农业板块近期异军突起，种业、生猪养殖细分领域成震荡市亮点，一批逆势布局的主题产品实现业绩与规模共振。<br>
          <b>涨幅表现：</b>下半年以来招商国证粮食产业指数基金涨超12.9%、景顺长城国证粮食产业ETF涨超18%、广发国证粮食产业ETF联接涨逾21%、汇添富中证畜牧养殖ETF联接涨逾15%。<br>
          <b>共性逻辑：</b>多数成立于5—7月板块低位，建仓期不受老基金高位套牢拖累；公募在产品发行上开始“自我克制”、落实逆周期布局，不再盲目追逐高热度赛道。<br>
          <b>对腾安启示：</b>冷门主题逆周期布局获验证，代销端可引导客户关注低位行业ETF性价比，避免追高热门赛道。
        </div>
        <div class="card-footer">
          <a href="https://m.10jqka.com.cn/20260907/c679632237.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·09-07</span></a>
        </div>
      </div>

      <!-- S0 Card 4 (09-07 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 QDII纳指ETF溢价风险升温·多只停复牌·新额度难平高溢价</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          经济参考报9月7日（新华社旗下），QDII基金高溢价风险持续发酵——富国纳指ETF（513870）、嘉实纳指ETF（159501）因二级市场价格明显高于IOPV发布溢价风险提示，嘉实纳指ETF定于9月7日开市停牌、10:30复牌。<br>
          <b>溢价程度：</b>截至9月3日华泰柏瑞中韩半导体ETF（QDII）年内已发317条溢价风险提示/停牌公告，5月15日溢价率一度达35.94%；10只场内QDII基金年内申赎净流入超10亿元。<br>
          <b>额度落地：</b>QDII额度扩容后“刚放开又限流”——汇添富纳指100ETF联接9月4日申购上限再次压回10元；截至7月底QDII基金份额8629亿份、净值10165亿元。<br>
          <b>对腾安启示：</b>跨境ETF高溢价是代销端重点风险提示场景，应引导客户规避溢价追高、理性配置海外资产。
        </div>
        <div class="card-footer">
          <a href="http://jjckb.xinhuanet.com/20260907/08b620a0a3294f2e89bf0d4dd7ba4e13/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济参考报·09-07</span></a>
        </div>
      </div>
    </div>
  </div>

'''

s0_start = src.find('        <!-- ============ Section 0: 今日焦点 ============ -->')
s0_end = src.find('<!-- ============ Section 1: 重磅信息 ============ -->')
assert s0_start != -1 and s0_end != -1 and s0_start < s0_end, 'S0 边界定位失败'
src = src[:s0_start] + S0_NEW + src[s0_end:]

# ---------- 4. S7 时间线整块替换 ----------
S7_NEW = '''<!-- ============ Section 7: 关键时间线 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--primary-light);color:var(--primary);">📅</div>
      <span class="section-title">关键时间线（近两周）</span>
      <span class="section-badge" style="background:var(--primary-light);color:var(--primary);">事件脉络</span>
    </div>

    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-07</div>
        <div class="timeline-title">证监会就私募募集办法公开征求意见</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-07</div>
        <div class="timeline-title">个人养老金扩容“固收+”赛道</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-06</div>
        <div class="timeline-title">下周44只新基金启动发售</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-05</div>
        <div class="timeline-title">首批10家基金上报科创债场外指数基金</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-04</div>
        <div class="timeline-title">A股放量下跌·沪指3930.12收跌0.30%</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-04</div>
        <div class="timeline-title">单周82只新基金启动发行·创单周纪录</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-03</div>
        <div class="timeline-title">公募参与A股定增获配超451亿·同比+160%</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-03</div>
        <div class="timeline-title">交易外接新规落地·中证协中基协联合发布</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-02</div>
        <div class="timeline-title">A股缩量普跌·沪指3941.39 -0.97%</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-02</div>
        <div class="timeline-title">公募上半年利润1.73万亿创历史最佳</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-02</div>
        <div class="timeline-title">本周12只FOF开募创9周新高·年内137只</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-01</div>
        <div class="timeline-title">盈利占比成绩单·中位数92.52%·120只满盈</div>
      </div>
    </div>

  </div>

</div>

</body>
</html>
'''

s7_start = src.find('<!-- ============ Section 7: 关键时间线 ============ -->')
assert s7_start != -1, 'S7 边界定位失败'
src = src[:s7_start] + S7_NEW

# ---------- 写入 ----------
open(HTML, 'w', encoding='utf-8').write(src)
print(f'写入完成：{orig_len} -> {len(src)} 字节')

# ---------- 自检 ----------
errors = []
# div 平衡
opens = len(re.findall(r'<div\b', src))
closes = len(re.findall(r'</div>', src))
print(f'div 开 {opens} / 闭 {closes}')
if opens != closes:
    errors.append(f'div 不平衡：{opens} vs {closes}')

# S8 不存在
for kw in ['Section 8', '待办跟踪', '腾安行动清单']:
    if kw in src:
        errors.append(f'S8 残留：{kw}')

# S0 标题
if '<span class="section-title">今日焦点</span>' not in src:
    errors.append('S0 section-title != 今日焦点')
if '今日焦点（' in src or '今日焦点 (' in src:
    errors.append('S0 标题出现堆料')

# section-context
if '9月7日 · 4条今日要闻' not in src:
    errors.append('S0 context 不对')

# S0 date-tag 数量
s0_seg = src[src.find('Section 0'):src.find('Section 1')]
dtags = re.findall(r'<span class="date-tag">(\d{2}-\d{2})</span>', s0_seg)
print('S0 date-tags:', dtags)
if len(dtags) != 4:
    errors.append(f'S0 卡片数 != 4（{len(dtags)}）')
for d in dtags:
    if d < '09-07':
        errors.append(f'S0 出现 T-1 及更早 date-tag：{d}')

# 乱码
if '\ufffd' in src:
    errors.append('存在 U+FFFD 乱码')

# 黑名单域名（新写段）
for bad in ['stcn.com', 'cls.cn', '21jingji', 'yicai.com', 'guba.eastmoney']:
    if bad in s0_seg:
        errors.append(f'S0 新写段出现黑名单域名：{bad}')

# section 标记完整性
for mk in ['Section 0: 今日焦点', 'Section 1: 重磅信息', 'Section 2: 监管政策',
           'Section 6: 市场行情速览', 'Section 7: 关键时间线']:
    if mk not in src:
        errors.append(f'缺 section 标记：{mk}')

if errors:
    print('\n❌ 自检失败：')
    for e in errors:
        print('  -', e)
    raise SystemExit(1)
print('\n✅ 自检全部通过')
