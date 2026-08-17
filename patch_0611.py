#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基金看板 2026-06-11 补位更新 patch 脚本（automation-8 兜底）"""

HTML_PATH = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'

def read():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def write(content):
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def do(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f'  OK {label}')
        return content
    else:
        print(f'  MISS {label}')
        # Find near-match
        idx = content.find(old[:40])
        print(f'    old[:40] = {old[:40]!r}')
        print(f'    found at index: {idx}')
        return content

def main():
    c = read()
    print(f'原始长度: {len(c)}')

    # ---- S8 待办事项：完全替换 tbody 内容 ----
    # 找到 <tbody> ... </tbody> 在 S8 中的位置
    # S8 从 <!-- =========== Section 8: 待办事项 =========== --> 开始
    s8_start = c.find('<!-- =========== Section 8')
    if s8_start == -1:
        print('ERROR: S8 section not found!')
        return

    tbody_start = c.find('<tbody>', s8_start)
    tbody_end = c.find('</tbody>', tbody_start) + len('</tbody>')
    print(f'S8 tbody: {tbody_start} -> {tbody_end}')

    new_tbody = '''        <tbody>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">美国CPI=4.2%结果应对：符合预期但绝对值高位→美联储加息预期升温，部分机构开始定价"重启加息"风险→提前准备QDII/港股ETF客户应急话术+市场波动客户沟通模板</td>
            <td style="padding:10px 12px;color:var(--gray-500);">CPI昨夜20:30已公布=4.2%</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">今日完成</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">SpaceX IPO明日（6/12）正式挂牌纳斯达克：史上最大IPO（750亿美元·估值1.77万亿）→全球科技资金虹吸效应持续→关注纳斯达克100 QDII和美股ETF的申购/赎回异动</td>
            <td style="padding:10px 12px;color:var(--gray-500);">SpaceX今日定价135美元/股</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月12日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">指数样本调整应对（6/12）：沪深300换19只/中证500换50只→被动资金千亿级调仓，评估腾安代销ETF受影响情况，做好投资者沟通</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/12收盘后生效</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月12日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">宇树科技明日（6/12）科创板上市：人形机器人第一股→科技成长双催化，关注相关主题基金机会+炒作风险</td>
            <td style="padding:10px 12px;color:var(--gray-500);">宇树6/12科创板挂牌</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月12日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">QDII限购+LOF溢价风险管控：全市场近半QDII限购+财通福鑫LOF溢价51%被交易所重点监控→检查腾安代销产品溢价情况，及时更新客户限额/溢价提示</td>
            <td style="padding:10px 12px;color:var(--gray-500);">LOF非理性炒作+QDII额度紧张</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">立即</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">A股量能萎缩应对：今日成交2.64万亿较昨日（2.9万亿）萎缩→科技虹吸效应持续，关注客户持仓集中度风险，主动提示分散配置</td>
            <td style="padding:10px 12px;color:var(--gray-500);">今日量能2.64万亿</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">今日收盘后</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">美联储6/18议息会议准备：鲍什上任后首次季度会议+点阵图→评估利率路径对QDII/港股产品影响，准备客户沟通材料</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/16-17会议·6/18公布</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月17日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">基准换新第三周跟踪：195只基金6/1生效已两周→收集客户咨询情况，确认超额收益展示逻辑已切换新基准</td>
            <td style="padding:10px 12px;color:var(--gray-500);">195只基金基准6/1生效</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">跨境券商整治客户承接：八部门整治（富途/老虎罚22亿）+2年过渡期→华盛6/15起暂停内地新开仓，评估腾安承接外流客户策略</td>
            <td style="padding:10px 12px;color:var(--gray-500);">八部门整治+华盛6/15</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月15日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">中基协换届后续跟踪：刘晓艳当选会长+吴清"四个坚持"定调→关注新一届理事会对代销机构的政策倾向，投教/投顾支持方向</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/6换届</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">持续关注</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">基金清盘潮排查：年内124只基金清盘创同期新高+20只预警→排查腾安代销产品中是否有清盘风险基金，做好客户预警</td>
            <td style="padding:10px 12px;color:var(--gray-500);">清盘同比+16%</td>
            <td style="padding:10px 12px;color:var(--primary);font-weight:600;">本周</td>
          </tr>
          <tr>
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">国办私募指导意见研读：23万亿私募全链条监管升级→评估高净值客户资金转公募/代销渠道机会，关注三年行动方案细则</td>
            <td style="padding:10px 12px;color:var(--gray-500);">国办函〔2026〕54号</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月中旬</td>
          </tr>
        </tbody>'''

    old_tbody = c[tbody_start:tbody_end]
    if len(old_tbody) < 100:
        print(f'ERROR: old_tbody too short ({len(old_tbody)} chars)')
        return

    c = c[:tbody_start] + new_tbody + c[tbody_end:]
    print(f'  OK S8 tbody 替换成功 ({len(old_tbody)} -> {len(new_tbody)} chars)')

    # 更新 S8 标题
    c = do(c,
        '<span class="section-title">下周待办建议清单</span>',
        '<span class="section-title">今日待办建议清单（6月11日更新）</span>',
        'S8 标题')

    print(f'最终长度: {len(c)}')
    write(c)
    print('写入完成！')

if __name__ == '__main__':
    main()
