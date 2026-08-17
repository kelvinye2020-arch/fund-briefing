#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补位更新 index.html S0第3张卡片（科创50暴涨）"""

with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查当前S0第3张卡片内容
marker = 'QDII科技ETF高溢价警示'
if marker in content:
    print("找到第3张卡片，开始替换...")
    # 找第3张卡片的起止位置
    # 卡片开始：找到 class="card p1" 且包含该标题的div
    # 用更简单的方式：找到该卡片的 card p1 div 起始位置
    
    # 策略：找到 QDII科技ETF 后面的 </div>   </div> 结束 S0 的部分
    # 实际上第3张卡片后面紧跟的是 </div>   </div> 然后是 Section 1
    
    # 更简单：直接替换卡片 body + footer + action-box
    old_body = '''<b>复牌后续：</b>6月16日10:30起，纳指ETF易方达(159696)、纳指ETF国泰(513100)、纳指科技ETF景顺(159807)、创业板ETF富国(159971)等集体复牌。复牌后高溢价有所回落，但部分产品溢价率仍高于理性区间，需持续关注。<br>
          <b>监管态度：</b>深交所已对纳指ETF广发等溢价严重的基金发出关注函，要求基金公司说明溢价原因及风险提示措施。监管对QDII ETF异常溢价的关注度明显上升，后续可能出台规范措施。<br>
          <b>市场背景：</b>QDII科技ETF高溢价反映境内投资者对美股科技板块的追捧情绪，但溢价率超10%已明显偏离理性区间。美联储议息结果（6/18公布）将影响美股走势，进而传导至QDII产品溢价水平。<br>
          <b>风险警示：</b>高溢价QDII ETF存在溢价回落导致的价格下跌风险，投资者需谨慎。腾安代销的相关产品需做好风险提示和客户解释准备。'''

    new_body = '''<b>6/17收盘：</b>A股低开后震荡走高，沪指<b>4108.57点(+0.40%)</b>，深成指<b>15775.03点(+1.31%)</b>，创业板指<b>4120.18点(+1.56%)</b>，科创50指数<b>涨超4%</b>，芯片股午后大幅走强（兆易创新涨停+10%，普冉股份+20%涨停）。<br>
          <b>资金背离信号：</b>6月17日，4只沪深300ETF合计<b>净流出超137亿元</b>（前一交易日净流出超100亿元），机构资金在指数上涨背景下高位兑现，显示机构对后市看法分歧加大。<br>
          <b>端午前效应：</b>6月19-21日端午休市，节前避险情绪升温，机构选择落袋为安。历史规律显示端午假期后A股上涨概率偏高，但需关注节日期间海外市场波动风险（特别是美联储议息结果）。<br>
          <b>对基金行业影响：</b>芯片/科创基金单日大涨→科技主题基金净值大幅回升，客户关注度上升；但机构资金净流出→指数基金申赎波动加大，代销平台需做好流动性管理。'''

    if old_body in content:
        content = content.replace(old_body, new_body)
        print("  卡片body替换成功")
    else:
        print("  WARNING: 卡片body未找到，尝试模糊匹配...")
        # 打印实际内容用于调试
        idx = content.find(marker)
        print("实际内容片段：", repr(content[idx:idx+500]))
    
    # 替换标题
    old_title = 'QDII科技ETF高溢价警示：纳指ETF易方达等6/16复牌后溢价回落，监管关注持续'
    new_title = '6/17 A股科创50暴涨超4%！但沪深300ETF净流出137亿，机构资金高位兑现'
    content = content.replace(old_title, new_title)
    
    # 替换 date-tag
    old_date = '<span class="date-tag">06-16</span>'
    new_date = '<span class="date-tag">06-17</span>'
    # 只替换第3张卡片内的（第2个匹配）
    parts = content.split(marker)
    if len(parts) > 1:
        parts[1] = parts[1].replace(old_date, new_date, 1)
        content = marker.join(parts)
        print("  date-tag替换成功")
    
    # 替换 card-footer 链接
    old_footer = '''<a href="https://www.egsea.com/news/detail/2302695.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯·纳指ETF停牌</span></a>
          <span class="impact-tag medium">溢价风险：持续</span>'''
    new_footer = '''<a href="https://finance.eastmoney.com/a/202606173774635827.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·资金流向</span></a>
          <a href="https://www.nbd.com.cn/articles/2026-06-18/4430113.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经·ETF净流出</span></a>
          <span class="impact-tag high">资金背离：高</span>'''
    
    if old_footer in content:
        content = content.replace(old_footer, new_footer)
        print("  card-footer替换成功")
    else:
        print("  WARNING: card-footer未找到")
    
    # 去掉 action-box（第3张卡片不需要action-box，或者更新它）
    # 先检查是否有 action-box
    old_action = '''        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 高溢价QDII ETF→提前准备客户解释话术；<br>
            ② 美联储议息结果今日公布→关注美股走势对QDII产品的影响；<br>
            ③ 监管关注溢价→腾安代销的相关产品需做好风险提示。
          </div>
        </div>'''
    new_action = '''        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 科创50大涨→科技主题基金客户关注度上升，准备净值解读话术；<br>
            ② 机构高位兑现→指数基金申赎波动加大，做好流动性管理准备；<br>
            ③ 端午前效应→节前权益基金销售承压，固收+产品性价比凸显。
          </div>
        </div>'''
    if old_action in content:
        content = content.replace(old_action, new_action)
        print("  action-box替换成功")
    else:
        print("  INFO: action-box未找到（可能已不存在）")
    
    # 更新 S0 标题
    old_s0 = '今日焦点（6月17日·周二·陆家嘴论坛开幕·公募自购75亿·QDII溢价后续）'
    new_s0 = '今日焦点（6月18日·周三·美联储议息结果落地·陆家嘴论坛收官·沪深300ETF净流出137亿）'
    content = content.replace(old_s0, new_s0)
    print("  S0标题更新")
    
else:
    print("未找到第3张卡片标记，可能已替换或文件结构变化")
    # 检查是否已经是新内容
    if '科创50暴涨超4%' in content:
        print("  第3张卡片似乎已是最新内容")
    else:
        print("  无法确定当前状态，请手动检查")

# 写回文件
with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n补位更新完成！")
print("验证：")
print("  S0第3张卡片标题：", '科创50暴涨超4%' in content)
print("  S0标题：", '6月18日·周三' in content)
print("  Header日期：", '06.04 — 2026.06.18' in content)
print("  daily-update标记：", 'daily-update: 2026-06-18' in content)
