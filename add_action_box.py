#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 S0 第3张卡片（科创50暴涨）添加 action-box"""

with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 在第3张卡片的 </div> 之前（S0 section 结束前）插入 action-box
# 找到第3张卡片的 card-footer，在它后面加 action-box

old_footer_end = '''          <span class="impact-tag high">资金背离：高</span>
        </div>
      </div>

    </div>
  </div>'''

new_footer_end = '''          <span class="impact-tag high">资金背离：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 科创50大涨→科技主题基金客户关注度上升，准备净值解读话术；<br>
            ② 机构高位兑现→指数基金申赎波动加大，做好流动性管理准备；<br>
            ③ 端午前效应→节前权益基金销售承压，固收+产品性价比凸显。
          </div>
        </div>
      </div>

    </div>
  </div>'''

if old_footer_end in content:
    content = content.replace(old_footer_end, new_footer_end)
    print("action-box 添加成功！")
else:
    print("WARNING: 未找到匹配片段，尝试模糊匹配...")
    # 打印实际内容
    idx = content.find('资金背离：高')
    if idx > 0:
        print("实际片段：", repr(content[idx:idx+300]))

# 写回文件
with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("验证 action-box：", '科创50大涨→科技主题基金' in content)
