# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P='index.html'; h=open(P,encoding='utf-8').read()
def drift(t):
    o=len(re.findall(r'<div\b',h)); c=len(re.findall(r'</div>',h)); print(f'  [{t}] {o}/{c} {o-c}')
drift('base')

NEW = '''<div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 头部公募抢滩智能体入口·AI陪伴服务成新战场·自研企业级AI平台成"试验田"</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          21世纪经济报道（记者易妍君）9月17日报道：AI平台正成为大众获取财经信息的重要入口，公募基金的服务阵地随之迁移。9月初<b>易方达基金正式入驻腾讯WorkBuddy平台</b>，成为首家入驻该平台的公募基金公司，其"易方达Buddy应用"设置"看懂机会、挑选基金、持有陪伴"三大模式，覆盖投前、投中、投后核心需求，所有内容均源自官微、官网、ima知识号、指数直通车小程序等官方数据源以保证可追溯。<br>
          <b>行业动作：</b>广发、华夏、鹏华等公司已陆续将官方知识库向腾讯ima的C端用户开放；易方达旗下指数直通车AI Skills此前已完成与OpenClaw、Hermes Agent、字节ArkClaw等主流智能体的对接。汇添富、南方、嘉实等多家大型公募也搭建了企业级AI能力平台——汇添富涵盖知识库管理、模型接入与评测、智能体开发，南方按"统一建设、分层应用"推动模型能力与投研系统衔接。<br>
          <b>冷思考：</b>讯兔科技联合创始人崔予淳指出公募入驻AI平台本质是为其潜在客户提供AI能力、最终形成销售转化，但也提出"AI到底是手段、工具还是解决根本问题的钥匙"；易方达首席信息官刘硕凌认为行业共同课题是在短期投入与长期能力建设之间取得平衡，把阶段性技术热点转化为安全可信、可持续积淀的组织级AI能力。<br>
          <b>对腾安启示：</b>基金公司正把"官方内容+AI入口"直接送到基民面前，代销平台的内容护城河被进一步压缩——腾安须尽快把选基框架与陪伴话术封装为可被外部智能体调用的标准资产，同时在自有App内提供AI原生入口，避免成为单纯的交易通道。
        </div>
        <div class="card-footer">
          <a href="https://fund.10jqka.com.cn/20260917/c680030279.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">21世纪经济报道·09-17</span></a>
          <span class="impact-tag high">AI入口争夺：高</span>
        </div>
      </div>

'''
a = h.find('<div class="card p1">\n        <div class="card-top">\n          <div class="card-title">🟡 基金公司全员用Skill')
assert a>0, '旧 S5 卡锚点未找到'
b = h.find('\n    </div>\n  </div>\n<!-- ============ Section 6', a)
assert b>a
h = h[:a] + NEW + h[b+1:]
drift('after')
s5 = h[h.find('Section 5'):h.find('Section 6')]
print('  S5 date-tags:', re.findall(r'date-tag">(\d{2})-(\d{2})</span>', s5))
open(P,'w',encoding='utf-8').write(h)
print('OK')
