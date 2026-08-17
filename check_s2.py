# -*- coding: utf-8 -*-
"""专门更新S2第一个卡片的body/footer/action-box部分"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找S2中第一个卡片的位置（标题已更新为"跨境券商禁令今日正式执行"）
marker = '🔴 跨境券商禁令今日正式执行'
pos = content.find(marker)
print("找到跨境券商卡片位置:", pos)

if pos > 0:
    # 找到该卡片的 card-body 开始位置
    body_start = content.find('<div class="card-body">', pos)
    # 找到该卡片的结束位置（下一个 </div> 后跟 </div> 关闭 card）
    # 策略：找到 card-body 后，找到对应的 action-box 结束位置
    action_end = content.find('      </div>\n      <div class="card p0">\n        <div class="card-top">\n          <div class="card-title">🔴 国办发文', pos)
    
    if action_end > body_start:
        old_card_content = content[body_start:action_end]
        print("找到旧body内容，长度:", len(old_card_content))
        print("前100字符:", repr(old_card_content[:100]))
    else:
        print("未找到action_end，尝试其他方法")
        # 打印从body_start开始的300字符
        print("body_start附近:", repr(content[body_start:body_start+500]))
else:
    print("未找到跨境券商禁令卡片标题")
