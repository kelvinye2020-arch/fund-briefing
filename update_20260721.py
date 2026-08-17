# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
s = open(PATH, encoding='utf-8').read()

def gbal(t):
    return t.count('<div'), t.count('</div>')

o0, c0 = gbal(s)
# Known pre-existing -1 imbalance (inherited S8 historical quirk, does not affect rendering)
print("ORIGINAL div counts opens", o0, "closes", c0, "delta", o0 - c0)

KWS = "A股深V反转双创领涨|主动ETF材料获证监会接收|二季报AI布局思路|绩优基金松绑限购|公募自购5000万"

# 1) daily-update marker
assert s.count('<!-- daily-update: 2026-07-20 -->') == 1
s = s.replace('<!-- daily-update: 2026-07-20 -->', '<!-- daily-update: 2026-07-21 -->', 1)

# 2) meta keywords (line 6 & 7)
old_kw = '二季报首披十年业绩超600%|发起式清盘占比超50%|A股07-17暴跌沪指-3.05%失守3800|18家公募上报主动ETF|公募FOF破3700亿'
assert s.count(old_kw) == 2, f"meta kw count = {s.count(old_kw)}"
s = s.replace(old_kw, KWS)

# 3) date badge
old_badge = '数据区间：2026.07.06 — 2026.07.20（每日更新）'
assert s.count(old_badge) == 1
s = s.replace(old_badge, '数据区间：2026.07.07 — 2026.07.21（每日更新）', 1)

# 4) section 0 title
old_t = '今日焦点（7月20日·周一·A股放量反弹半导体领涨·AI行情现分歧基金经理调仓差异·主动ETF落地倒计时·长跑翻倍基逆势减仓）'
assert s.count(old_t) == 1
s = s.replace(old_t, '今日焦点（7月21日·周二·A股深V反转双创领涨·主动ETF材料获证监会接收·二季报AI布局思路·绩优基金松绑限购公募自购）', 1)

# 5) S0 block: from S0 Card 1 comment to just before Section 1 comment
s0_start = s.index('          <!-- S0 Card 1: A股周一放量反弹')
s0_end = s.index('\n  <!-- ============ Section 1: 重磅信息 ============ -->')
assert s0_start < s0_end
old_s0 = s[s0_start:s0_end]

NEW_S0 = '''          <!-- S0 Card 1: A股深V反转·双创领涨·政策资金共振 (T+0 07-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 A股"深V"反转·双创领涨·沪指+1.30%·创业板+6.22%·科创50+8.45%·半导体深V反弹</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-21</span>
          </div>
        </div>
        <div class="card-body">
          <b>深V反转：</b>7月21日早盘三大指数一度翻绿（科创50盘中跌超3%），10:10后AI、半导体设备、晶圆制造率先拉升，市场上演"深V"反转；午间创业板指涨5.2%、科创50涨近7%，截至盘中沪指<b>+1.30%</b>报3845点、创业板<b>+6.22%</b>、科创50<b>+8.45%</b>，成交放量。<br>
          <b>机构解读：</b>多家机构"力挺"A股，国信证券荀玉根判断本轮为牛市运行中的调整而非结束，上周宽基ETF净申购超2000亿；华西证券李立峰称回调属技术性调整、已具备修复条件，反弹将延续并向中小市值扩散。<br>
          <b>对基金行业影响：</b>急跌后强劲修复→腾安应引导客户理性看待波动、把握结构性反弹中的科技+顺周期配置机会，避免追涨杀跌。
        </div>
        <div class="card-footer">
          <a href="https://news.sina.com.cn/o/2026-07-21/doc-iniiptrf2606265.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经·新浪财经</span></a>
          <span class="impact-tag medium">市场反弹：中</span>
        </div>
      </div>
    <!-- S0 Card 2: 主动ETF申报材料获证监会接收·权益工具创新里程碑 (T+0 07-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 首批18只主动ETF申报材料获证监会接收·A股权益投资工具创新里程碑</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-21</span>
          </div>
        </div>
        <div class="card-body">
          <b>里程碑：</b>据上证报7月21日报道，近日首批18只主动ETF申报材料获中国证监会接收，A股权益投资工具创新取得里程碑式进展；从监管6月17日首提"支持推出主动ETF"到材料齐挂，不到一个月。<br>
          <b>框架升级：</b>主动ETF融合"主动选股+ETF交易"双重优势，将搭建"被动ETF捕捉贝塔、主动ETF挖掘阿尔法"的核心卫星配置框架；产品策略以稳健均衡、价值、红利为主，严格准入门槛保障规范运作。<br>
          <b>对基金行业影响：</b>主动投资"透明厨房"时代来临→有望吸引保险、养老金等中长线资金入市、优化A股资金结构，腾安应前瞻储备主动ETF货架与投教内容。
        </div>
        <div class="card-footer">
          <a href="https://cj.sina.com.cn/article/norm_detail?url=https%3A%2F%2Ffinance.sina.com.cn%2Froll%2F2026-07-21%2Fdoc-iniinwmu8194938.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">主动ETF：中</span>
        </div>
      </div>
    <!-- S0 Card 3: 基金二季报密集披露·AI布局思路浮出水面 (T+0 07-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 基金二季报密集披露·AI布局思路浮出水面·产业链结构性分化·资金向硬环节集中</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-21</span>
          </div>
        </div>
        <div class="card-body">
          <b>思路浮现：</b>伴随二季报披露大幕拉开，基金经理在AI浪潮中的最新布局思路浮出水面，AI产业链内部正经历结构性分化，资金加速向确定性更高的"硬环节"集中，部分前期涨幅较大细分领域被果断兑现。<br>
          <b>具体打法：</b>金信稳健策略孔学兵维持半导体国产替代长期积极展望、淡化短期景气；融通先进制造王迪二季度将组合进一步向AI产业链集中、增配PCB上游与半导体；融通产业趋势李进关注算力板块业绩兑现。<br>
          <b>对基金行业影响：</b>AI主线进入"去伪存真"阶段→腾安推荐需强化中报业绩兑现与估值风险揭示，弱化纯赛道叙事。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-07-21/doc-iniippii2639622.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·环球网</span></a>
          <span class="impact-tag medium">二季报AI：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 绩优基金放松限购·博时自购5000万·李晓星看多创新药 (T+0 07-21 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多只绩优基金放松限购·博时自购5000万·国金1500万·李晓星看多创新药</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-21</span>
          </div>
        </div>
        <div class="card-body">
          <b>松绑限购：</b>近期多只绩优基金宣布放松限购，财通价值动量混合自7月15日起限购金额由100元上调至1万元，华商基金多只产品自7月16日起由1000元调整至10万元，部分基金更直接取消限购。<br>
          <b>自购潮起：</b>7月20日博时基金公告运用固有资金5000万元投资旗下权益类基金；国金基金此前亦公告自购不低于1500万元并持有不少于1年，机构逆势展示信心。<br>
          <b>观点：</b>银华李晓星表示创新药板块上半年回撤较深、当前估值已具性价比，将持续关注基本面优质、股价位置合适的龙头择机建仓。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_3026a5ec50e00252" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">自购/限购：低</span>
        </div>
      </div>
    </div>
  </div>'''

s = s[:s0_start] + NEW_S0 + s[s0_end:]

# 6) S6 block: from S6 card p3 open to just before Section 7 comment
s6_start = s.index('          <div class="card p3">')
s6_end = s.index('\n  <!-- ============ Section 7: 关键时间线 ============ -->')
assert s6_start < s6_end
old_s6 = s[s6_start:s6_end]

NEW_S6 = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月21日（周二·盘中）·A股深V反转·沪指+1.30%·创业板+6.22%·科创50+8.45%领涨</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股07-21盘中（深V反转·双创领涨）：</b><br>
              ▪ 沪指 <b>+1.30%</b>（3845.62）·深成指 <b>+4.23%</b>（14186.61）<br>
              ▪ 创业板指 <b>+6.22%</b>（3657.34）·科创50 <b>+8.45%</b>（1863.86）·成交放量<br>
              ▪ 早盘探底翻绿后10:10拉升，半导体/芯片/算力租赁领涨；油气、电力调整
            </div>
            <div>
              <b>📉 港股07-20收盘（反弹）：</b><br>
              ▪ 恒指 <b>+2.36%</b>（25143.05）·恒生科技 <b>+2.79%</b>（4752.15）·国企指数+3.01%<br>
              <b>📉 美股07-20收盘（中东局势拖累）：</b>道指-0.59%（51839.26）·标普-0.19%（7443.28）·纳指-0.05%（25508.07）；芯片高开低走·中概走强
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：A股深V反转、政策资金共振，机构"力挺"称牛市中调整；7月股票型ETF净流入超3200亿、逆周期布局蓄力；首批18只主动ETF材料获证监会接收，有望10交易日内落地。
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-21（周二盘中）</span>
            <span class="source-tag">数据来源：新浪财经/第一财经/港交所/东方财富</span>
          </div>
      </div>
  </div>'''

s = s[:s6_start] + NEW_S6 + s[s6_end:]

# 7) S7 timeline: insert 07-21, remove 07-06 (expired T-14) and stray 07-02 comment
anchor_0720 = '    <!-- 07-20 时间线条目 (NEW) -->\n      <div class="timeline-item">'
assert s.count(anchor_0720) == 1
new_0721 = ('    <!-- 07-21 时间线条目 (NEW) -->\n'
            '      <div class="timeline-item">\n'
            '        <div class="timeline-dot red"></div>\n'
            '        <div class="timeline-date">2026-07-21</div>\n'
            '        <div class="timeline-title">A股深V反转·双创领涨·科创50涨8.45%</div>\n'
            '      </div>\n\n') + anchor_0720
s = s.replace(anchor_0720, new_0721, 1)

old_0706 = ('    <!-- 07-06 时间线条目 (NEW) -->\n'
            '      <div class="timeline-item">\n'
            '        <div class="timeline-dot red"></div>\n'
            '        <div class="timeline-date">2026-07-06</div>\n'
            '        <div class="timeline-title">A股交易新规7月6日正式实施</div>\n'
            '      </div>\n')
assert s.count(old_0706) == 1
s = s.replace(old_0706, '', 1)

stray_0702 = '    <!-- 07-02 时间线条目 (NEW) -->\n'
assert s.count(stray_0702) >= 1
s = s.replace(stray_0702, '', 1)

# Final div balance check — must preserve the pre-existing delta (balanced edits)
o1, c1 = gbal(s)
assert o1 == o0 and c1 == c0, f"div counts changed {o0}/{c0} -> {o1}/{c1}"
print("OK: div counts preserved", o1, c1, "delta", o1 - c1)
print("old_s0_len", len(old_s0), "old_s6_len", len(old_s6))
