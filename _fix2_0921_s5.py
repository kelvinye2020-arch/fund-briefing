# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P='index.html'; h=open(P,encoding='utf-8').read()
def drift(t):
    o=len(re.findall(r'<div\b',h)); c=len(re.findall(r'</div>',h)); print(f'  [{t}] {o}/{c} {o-c}')
drift('base')

XING = '''<div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 兴证全球以"可信AI"构建资管流水线·取数有界生成有据输出可溯·责任在岗</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-15</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月15日报道：兴证全球基金本轮AI建设的核心并非模型能力堆叠，而是一套贯穿全流程的统一约束机制——<b>取数有界、生成有据、输出可溯、责任在岗</b>，AI不绕过、不修改、不替代既有业务规则体系。<br>
          <b>场景落地：</b>①自研<b>兴全AIWork</b>办公平台依托本地部署的Hermes为每位员工构建个人AI助理，邮箱/日程/文档按需逐项授权、助理空间相互隔离、全程留痕；②<b>营销物料智作平台</b>以可信结构化数据限定取数范围，实现"一份可信数据、多种物料形态"（文案、季报解读、PPT、长图、海报）；③风控AI助手<b>"风小应"</b>自动解析基金合同合规要素并映射为风控条目与参数方案，输出止步于"条目建议+参数方案"、须风控人员人工确认；④<b>头寸AI助理</b>实时预警缺口并推荐处置方案；⑤直销App上线AI诊基与AI持仓分析，形成"<b>AI生成→AI审校→人工终审</b>"三层机制；⑥数据侧"数小智"提供7×24小时数据故障诊断与血缘解析。<br>
          <b>演进脉络：</b>早在2023年公司即推出AI资金交易机器人"兴宝"，为业内首家将AI技术应用于资金交易领域的基金公司，此后由投研、交易逐步延伸至办公、营销、风控、电商与数据。<br>
          <b>对腾安启示：</b>行业AI竞争的胜负手正从"模型有多强"转向"责任边界有多清晰"——腾安若上线AI诊基/陪伴，须先定义取数边界、AI数字事实审核与人工终审链路，把留痕可审计做成对客合规卖点，而非只比拼生成速度。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/790576" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-15</span></a>
          <span class="impact-tag high">AI治理：高</span>
        </div>
      </div>

'''
anchor = '\n    </div>\n  </div>\n<!-- ============ Section 6'
assert h.count(anchor) == 1
h = h.replace(anchor, '\n' + XING + '    </div>\n  </div>\n<!-- ============ Section 6', 1)
drift('after')
s5 = h[h.find('Section 5'):h.find('Section 6')]
print('  S5 date-tags:', re.findall(r'date-tag">(\d{2})-(\d{2})</span>', s5))
open(P,'w',encoding='utf-8').write(h)
print('OK')
