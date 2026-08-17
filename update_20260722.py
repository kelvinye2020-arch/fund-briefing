# -*- coding: utf-8 -*-
import io, sys

p = 'index.html'
s = open(p, encoding='utf-8').read()
orig_opens = s.count('<div')
orig_closes = s.count('</div>')

def repl(s, old, new, label):
    c = s.count(old)
    assert c == 1, f"[{label}] expected exactly 1 match, got {c}"
    return s.replace(old, new, 1)

# ---------- 1. daily-update marker ----------
s = repl(s, '<!-- daily-update: 2026-07-21 -->', '<!-- daily-update: 2026-07-22 -->', 'marker')

# ---------- 2. date-badge ----------
s = repl(s,
    '\U0001F4C5 数据区间：2026.07.07 — 2026.07.21（每日更新）',
    '\U0001F4C5 数据区间：2026.07.08 — 2026.07.22（每日更新）',
    'badge')

# ---------- 3. meta keywords (two identical lines) ----------
old_kw = '首批18只主动ETF获证监会接收|A股07-21深V反转双创领涨|宽基ETF单日净流入590亿次新高|证监会座谈会规范量化与AI|绩优基金松绑限购+自购'
new_kw = '公募二季报收官|二季度盈利近2万亿|中际旭创居首重仓|证监会密集座谈会维稳|A股07-22低开高走科创50领涨'
kc = s.count(old_kw)
assert kc == 2, f"keywords count={kc}"
s = s.replace(old_kw, new_kw)

# ---------- 4. Stats Bar ----------
STATS = '''<div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">3875.21</div>
      <div class="stat-label">上证综指 · 07-22低开高走收+0.28%·科创50+1.23%领涨·半导体设备逆市走强</div>
      <div class="stat-change up">\u25b2 A股分化延续·硬科技结构行情·增量资金仍借道ETF</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1.94万亿</div>
      <div class="stat-label">公募二季度盈利19390亿·扭转一季度亏损·权益类成主力（二季报收官）</div>
      <div class="stat-change up">\u25b2 中际旭创1662亿居首·硬科技主导重仓·消费医药集体出局前十</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">72只</div>
      <div class="stat-label">百亿主动权益基金·较一季度末32只+125%·科技主题包揽规模前三</div>
      <div class="stat-change up">\u25b2 东方人工智能351亿/永赢科技智选346亿/永赢先锋半导体329亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1500亿+</div>
      <div class="stat-label">创新药主题基金总规模破1500亿·月内增逾180亿·流动性改善+政策预期</div>
      <div class="stat-change up">\u25b2 港股通创新药ETF领涨·板块估值与基本面共振</div>
    </div>
  </div>
'''
ss = s.index('<div class="stats-bar">')
sem = '  </div>\n<div class="main">'
se = s.index(sem, ss)
s = s[:ss] + STATS + s[se:]

# ---------- 5. S0 section-title ----------
s = repl(s,
    '\u4eca\u65e5\u7126\u70b9\uff087\u670821\u65e5\u00b7\u5468\u4e8c\u00b7\u9996\u627918\u53ea\u4e3b\u52a8ETF\u83b7\u8bc1\u76d1\u4f1a\u63a5\u6536\u00b7\u8bc1\u76d1\u4f1a\u5ea7\u8c08\u4f1a\u89c4\u8303\u91cf\u5316\u4e0eAI\u00b7\u5bbd\u57faETF\u5355\u65e5\u51c0\u6d41\u5165590\u4ebf\u00b7\u7ee9\u4f18\u57fa\u91d1\u677e\u7ed1\u9650\u8d2d\uff09',
    '\u4eca\u65e5\u7126\u70b9\uff087\u670822\u65e5\u00b7\u5468\u4e09\u00b7\u516c\u52df\u4e8c\u5b63\u62a5\u6536\u5b8cQ2\u76c8\u5229\u8fd1\u4e07\u4ebf\u00b7\u4e2d\u9645\u65ed\u521b\u5c45\u9996\u91cd\u4ed3\u00b7\u57fa\u91d1\u6295\u987e\u6269\u5bb9\u7a97\u53e3\u00b7A\u80a1\u4f4e\u5f00\u9ad8\u8d70\u79d1\u521b50\u9886\u6da8\uff09',
    's0title')

# ---------- 6. S0 cards (replace whole card-grid inner) ----------
S0 = '''    <div class="card-grid">

                    <!-- S0 Card 1: 公募二季报收官·Q2盈利近2万亿·重仓洗牌 (T+0 07-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F53C 公募二季报收官·二季度盈利近2万亿·中际旭创1662亿居首·硬科技主导重仓</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>盈利大反转：</b>天相投顾数据，2026年二季度公募基金合计盈利<b>19390.35亿元</b>，一举扭转一季度亏损2029.42亿元的局面，权益类产品贡献关键增量。<br>
          <b>重仓洗牌：</b>二季报披露收官，中际旭创以1662.53亿元持仓市值稳居第一大重仓股；公募前十大重仓股全部为硬科技（新易盛、寒武纪、北方华创、兆易创新等），消费、医药龙头近十年首次集体退出前十，腾讯控股、贵州茅台等港股互联网龙头亦淡出。<br>
          <b>对基金行业影响：</b>持仓高度集中于AI硬科技→行业"抱团"与估值泡沫风险上升，腾安应强化分散配置与风险提示，引导客户理性看待科技主线拥挤度。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260722A03DVU00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·上证报</span></a>
          <span class="impact-tag high">行业拐点：高</span>
        </div>
      </div>
    <!-- S0 Card 2: A股07-22低开后分化·半导体设备ETF涨超5%·科创50收涨 (T+0 07-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F53C A股07-22低开后分化·半导体设备ETF盘中涨超5%·科创50收涨1.23%领涨</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>低开高走：</b>7月22日三大指数集体低开（沪指-0.64%·深成指-0.66%·创业板-1.11%），盘中分化震荡，截至收盘沪指<b>+0.28%</b>（3875.21）·深成指<b>+0.50%</b>（14335.84）·创业板<b>-0.29%</b>（3675.36）·科创50<b>+1.23%</b>（1926.63）·沪深300+0.45%。<br>
          <b>结构主线：</b>半导体设备板块逆市走强，半导体设备ETF国泰盘中涨超5%、近20日净流入156.73亿、规模达423亿；有色矿业ETF盘中涨近3%；贵金属盘初走高。医药、消费、港股互联网回调。<br>
          <b>对基金行业影响：</b>科技硬件主线延续→腾安可顺势强化半导体/AI主题ETF货架与定投话术，但需提示板块拥挤与波动风险。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260722A04X2N00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">市场分化：中</span>
        </div>
      </div>
    <!-- S0 Card 3: 基金投顾试点扩容窗口期·券商外资加速 (T+0 07-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F53C 基金投顾试点迎扩容窗口·券商外资加速申报·监管严查大V合作与利益冲突隔离</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>扩容提速：</b>21世纪经济报道，基金投顾试点迎来扩容窗口期，各地方监管统筹辖区内机构材料上报，多家券商加速推进申报；分类评级A类及以上券商有望获资格。截至2026年初，基金投顾行业管理规模约<b>4500亿元</b>、累计服务客户近<b>1000万户</b>。<br>
          <b>对外开放：</b>监管鼓励外资持牌机构参与基金投顾业务扩大试点，部分外资资管机构正积极筹备布局。<br>
          <b>合规收紧：</b>监管新增关注重点——尤其重视机构与大V合作情况，强调业务隔离、防范利益冲突要求更细化，严禁"出借牌照"式合规流于形式。<br>
          <b>对基金行业影响：</b>投顾扩容→腾安可前瞻储备"诊断+配置+陪伴"账户服务能力，同时严守大V合作合规边界。
        </div>
        <div class="card-footer">
          <a href="https://guba.eastmoney.com/news,cjpl,1747476772.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">21世纪经济报道</span></a>
          <span class="impact-tag medium">投顾扩容：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 创新药主题基金总规模破1500亿 (T+0 07-22 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F534 创新药主题基金总规模突破1500亿元·月内增逾180亿·港股通创新药ETF领涨</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模跃升：</b>Wind数据显示，截至7月20日，64只创新药主题基金月内净值全部走高，总规模已突破<b>1500亿元</b>，较月初增长逾180亿元；港股通创新药ETF整体涨幅居前，科创板创新药ETF表现相对滞后。<br>
          <b>驱动逻辑：</b>板块受流动性改善及政策预期提振，业内认为创新药行业基本面持续改善，相关ETF后续表现仍值得关注；但不同指数编制方案及底层资产差异或致业绩分化。<br>
          <b>对基金行业影响：</b>创新药成新主线→腾安可补充创新药/医药主题ETF货架，契合客户对高景气赛道的配置需求。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260722A03VWM00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">创新药：中</span>
        </div>
      </div>
    </div>
'''
s0s = s.index('    <div class="card-grid">\n')
s0e_marker = '  </div>\n<!-- ============ Section 1: 重磅信息'
s0e = s.index(s0e_marker, s0s)
s = s[:s0s] + S0 + s[s0e:]

# ---------- 7. S2 add new card (证监会维稳座谈会) ----------
S2_CARD = '''      <!-- S2 Card NEW: 证监会党委班子密集座谈会·增强市场内在稳定性 (07-22) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F53C 证监会党委班子密集召开座谈会·增强市场内在稳定性·稳市信号延续</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>密集座谈：</b>7月20日下午至21日，证监会党委班子成员分别召开座谈会，就促进资本市场稳定健康发展听取上市公司、证券基金机构和专家学者意见建议；7月20日吴清主席还赴证券营业部调研并主持召开投资者座谈会。<br>
          <b>政策导向：</b>证监会表示将认真研究吸收各方建议，统筹防风险、强监管、促高质量发展，持续加强市场基础制度建设，增强市场内在稳定性，完善投资者合法权益保护长效机制。<br>
          <b>对基金行业影响：</b>稳市信号密集释放→利好权益产品风险偏好修复，腾安可借势强化长期配置与定投投教，引导客户理性看待波动。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260722A043CZ00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">金融界·经济参考报</span></a>
          <span class="impact-tag medium">稳市信号：中</span>
        </div>
      </div>'''
s2_marker = '    </div>\n  </div>\n\n<!-- ============ Section 3: 竞争对手动态'
assert s.count(s2_marker) == 1, f"s2_marker count={s.count(s2_marker)}"
s = s.replace(s2_marker, S2_CARD + '\n' + s2_marker, 1)

# ---------- 8. S6 replace card ----------
S6 = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月22日（周三·收盘）·A股低开高走分化·沪指+0.28%·科创50+1.23%领涨·半导体设备逆市走强</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>\U0001F4C8 A股07-22收盘（低开高走·分化）：</b><br>
              ▪ 沪指 <b>+0.28%</b>（3875.21）·深成指 <b>+0.50%</b>（14335.84）<br>
              ▪ 创业板指 <b>-0.29%</b>（3675.36）·科创50 <b>+1.23%</b>（1926.63）·沪深300 +0.45%<br>
              ▪ 半导体设备ETF盘中涨超5%、有色矿业ETF涨近3%；医药/消费/港股互联网回调
            </div>
            <div>
              <b>\U0001F4C9 港股07-21收盘（分化）：</b><br>
              ▪ 恒指 <b>-0.04%</b>（25132.29）·恒生科技 <b>+1.32%</b>（4814.83）·国企指数-0.25%<br>
              <b>\U0001F4C9 美股07-21收盘（全线大涨·半导体反攻）：</b>道指+0.74%（52224.64）·标普+0.89%（7509.20）·纳指+1.29%（25837.21）；费城半导体+5.21%、美光+12%
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            \U0001F4A1 焦点：公募二季报收官·二季度盈利近2万亿、中际旭创居首重仓、硬科技主导；证监会密集座谈会释放稳市信号；基金投顾试点扩容、创新药基金破1500亿；A股低开后分化、科创50领涨，美股半导体大反攻提振风险偏好。
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-22（周三收盘）</span>
            <span class="source-tag">数据来源：新浪财经/东方财富/港交所/新华社</span>
          </div>
'''
s6s = s.index('          <div class="card p3">')
s6e_marker = '      </div>\n  </div>\n<!-- ============ Section 7: 关键时间线'
s6e = s.index(s6e_marker, s6s)
s = s[:s6s] + S6 + s[s6e:]

# ---------- 9. S7 insert 07-22 + delete 07-07 ----------
s7_ins_anchor = '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-21</div>'
assert s.count(s7_ins_anchor) == 1
s7_new = '      <!-- 07-22 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-22</div>\n        <div class="timeline-title">公募二季报收官·二季度盈利近2万亿·中际旭创居首重仓</div>\n      </div>\n\n'
s = s.replace(s7_ins_anchor, s7_new + s7_ins_anchor, 1)

s7_del = '    <!-- 07-07 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-07</div>\n        <div class="timeline-title">A股三大指数集体低开·半导体芯片领跌</div>\n      </div>\n'
assert s.count(s7_del) == 1, f"s7_del count={s.count(s7_del)}"
s = s.replace(s7_del, '', 1)

# ---------- final assertions ----------
opens = s.count('<div')
closes = s.count('</div>')
assert opens == closes, f"DIV IMBALANCE: opens={opens} closes={closes}"
assert 'Section 8' not in s, "S8 section reappeared!"
assert '待办跟踪' not in s, "S8 待办跟踪 reappeared!"
assert '腾安行动清单' not in s, "S8 腾安行动清单 reappeared!"
# S0 date-tags must be 07-22 (no T-2 leak)
assert '07-20' not in s.split('Section 0')[1].split('Section 1')[0], "S0 has 07-20 leak"
# S7 must have 07-22 and not 07-07
assert '2026-07-22' in s and '2026-07-07' not in s, "S7 date check failed"

open(p, 'w', encoding='utf-8').write(s)
print("OK: written. opens=closes=%d (orig %d/%d)" % (opens, orig_opens, orig_closes))
print("S8 absent:", ('Section 8' not in s))
