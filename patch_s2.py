import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换card-footer
old_footer = '''        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867065335216314660" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·腾讯新闻</span></a>
          <a href="http://finance.ce.cn/stock/gsgdbd/202606/t20260603_3008090.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <span class="impact-tag high">跨境监管：极高</span>
        </div>'''

new_footer = '''        <div class="card-footer">
          <span class="impact-tag high">行业纲领：极高</span>
        </div>'''

if old_footer in content:
    content = content.replace(old_footer, new_footer, 1)
    print('[OK] card-footer replaced')
else:
    print('[WARN] card-footer NOT found, trying alternative match...')
    # 尝试找包含"跨境监管"的card-footer
    if '跨境监管：极高' in content:
        print('[INFO] found 跨境监管 in content, but footer format differs')

# 替换action-box
old_action = '''        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跨境券商禁令生效→境外投资需求向合规渠道转移，主动营销腾安QDII/港股通产品；<br>
            ② 承接流出客户→制定跨境券商存量客户迁移承接方案和营销话术；<br>
            ③ 关注艾德6/15跟进情况，跨境整治可能在2年过渡期内持续加码。
          </div>
        </div>'''

new_action = '''        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 研究三年行动计划对腾安代销业务模式的影响，提前规划收费模式转型；<br>
            ② 销售费用新规实施→评估腾安代销佣金结构是否需要调整。
          </div>
        </div>'''

if old_action in content:
    content = content.replace(old_action, new_action, 1)
    print('[OK] action-box replaced')
else:
    print('[WARN] action-box NOT found, searching...')
    if '跨境券商禁令生效' in content:
        print('[INFO] found 跨境券商禁令生效 in content')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('[DONE] patch_s2.py completed')
