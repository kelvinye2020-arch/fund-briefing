import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', encoding='utf-8') as f:
    c = f.read()
# Fix date-tag
c = c.replace('<span class="date-tag">06-16</span>', '<span class="date-tag">06-17</span>', 1)
# Add action-box after card-footer of card 3
action = """        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 科创50大涨→科技主题基金客户关注度上升，准备净值解读话术；<br>
            ② 机构高位兑现→指数基金申赎波动加大，做好流动性管理准备；<br>
            ③ 端午前效应→节前权益基金销售承压，固收+产品性价比凸显。
          </div>
        </div>"""
# Find the position after card-footer of card 3
marker = '资金背离：高</span>\n        </div>\n      </div>'
idx = c.find(marker)
if idx > 0:
    insert_pos = idx + len(marker)
    c = c[:insert_pos] + "\n" + action + c[insert_pos:]
    print("action-box added")
else:
    print("marker not found")
with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("date-tag fixed:", '"06-17" in c')
