# -*- coding: utf-8 -*-
"""精准替换S2第一个卡片的card-body到action-box结束部分"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 旧内容（从card-body开始到第一个卡片的action-box结束）
old_body = '''        <div class="card-body">
          <b>5月22日重磅落地：</b>证监会等八部门联合印发《综合整治非法跨境证券期货基金经营活动实施方案》，设置<b>2年集中整治期</b>，全面取缔境外机构非法跨境展业。同日证监会对富途控股拟罚没<b>18.5亿元</b>、老虎证券<b>4.1亿元</b>，合计超22亿元。<br>
          <b>整治措施：</b>期内仅允许存量账户单向卖出并转出资金，全链条穿透监管覆盖营销招揽、开户、交易处理全流程。长桥证券亦被同步处罚。<br>
          <b>行业影响：</b>非法跨境渠道被清退→境外投资需求向港股通、QDII、跨境理财通等合规渠道转移，利好持牌代销机构。
        </div>
        <div class="card-footer">
          <a href="http://www.ce.cn/xwzx/gnsez/gdxw/202605/t20260525_2986368.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <a href="https://news.qq.com/rain/a/20260524A08BB700" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中信建投点评</span></a>
          <span class="impact-tag high">跨境监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跨境渠道清退→关注QDII产品需求激增，提前准备额度和营销话术；<br>
            ② 港股通/跨境理财通合规渠道利好→评估腾安相关产品推广机会。
          </div>
        </div>'''

new_body = '''        <div class="card-body">
          <b>今日正式执行：</b>6月12日起，富途控股、老虎国际、长桥证券三家头部跨境互联网券商对<b>中国大陆境内账户</b>的服务调整正式生效。核心限制：<b>暂停股票等所有品种的新开仓、加仓交易</b>，仅支持卖出、平仓操作；暂停资金转入，转出功能保持正常。<br>
          <b>政策依据：</b>5月22日证监会等八部门联合印发《综合整治非法跨境证券期货基金经营活动实施方案》，设置<b>2年集中整治期</b>，全面取缔境外机构非法跨境展业。富途被罚没18.5亿元、老虎4.1亿元，合计超22亿元。<br>
          <b>艾德证券6/15跟进：</b>艾德证券将于6月15日起暂停向现有受影响客户于中国内地境内提供任何产品之买入及存入资金之服务，跨境券商整治全面落地。<br>
          <b>行业影响：</b>非法跨境渠道被清退→境外投资需求向<b>港股通、QDII、跨境理财通</b>等合规渠道转移，利好持牌代销机构。腾安作为腾讯系合规平台，有望承接从跨境券商流出的客户资源。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867065335216314660" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·腾讯新闻</span></a>
          <a href="http://finance.ce.cn/stock/gsgdbd/202606/t20260603_3008090.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <span class="impact-tag high">跨境监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跨境券商禁令生效→境外投资需求向合规渠道转移，主动营销腾安QDII/港股通产品；<br>
            ② 承接流出客户→制定跨境券商存量客户迁移承接方案和营销话术；<br>
            ③ 关注艾德6/15跟进情况，跨境整治可能在2年过渡期内持续加码。
          </div>
        </div>'''

if old_body in content:
    content = content.replace(old_body, new_body)
    print("✅ S2 第一个卡片 body/footer/action-box 已更新")
else:
    print("❌ 未找到旧 body 内容")
    # 尝试模糊查找
    if '5月22日重磅落地' in content:
        print("  → 找到了 '5月22日重磅落地'")
        # 打印该位置附近内容
        pos = content.find('5月22日重磅落地')
        print("  附近内容:", repr(content[pos-50:pos+200]))
    else:
        print("  → 未找到 '5月22日重磅落地'")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件已保存")
