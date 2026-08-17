# -*- coding: utf-8 -*-
"""用逐行方式精准替换S2第一个卡片的body/footer/action-box"""

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到S2部分第一个卡片的 card-body 起始行
in_s2_card1 = False
in_card1_body = False
body_start = -1
body_end = -1

for i, line in enumerate(lines):
    if '跨境券商禁令今日正式执行' in line or '八部门联合整治' in line:
        # 找到这个卡片的位置
        # 往后找 card-body
        for j in range(i+1, min(i+30, len(lines))):
            if 'card-body' in lines[j] and '<div' in lines[j]:
                body_start = j
                print(f"找到 card-body 起始行: {j}: {lines[j].strip()}")
                break
        break

if body_start > 0:
    # 找到该卡片的 action-box 结束位置（下一个 </div> 后跟 </div> 关闭 card）
    # 策略：找到 action-text 结束后，找到下一个 </div> 的结束
    for j in range(body_start+1, min(body_start+80, len(lines))):
        if '</div>' in lines[j] and 'action-box' not in lines[j] and 'action-text' not in lines[j]:
            # 检查是否 action-box 已经结束
            pass
    
    print(f"需要手动替换：card-body 在第{body_start}行")
    print("该卡片当前内容：")
    for j in range(body_start-2, min(body_start+60, len(lines))):
        print(f"  {j}: {lines[j].rstrip()}")
else:
    print("未找到目标卡片")
