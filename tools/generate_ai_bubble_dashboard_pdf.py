from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "AI泡沫观察指标手册.pdf"


def register_fonts():
    candidates = [
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ]
    for path in candidates:
        if path.exists():
            pdfmetrics.registerFont(TTFont("CJK", str(path)))
            return "CJK"
    return "Helvetica"


FONT = register_fonts()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName=FONT,
        fontSize=25,
        leading=34,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#111827"),
        wordWrap="CJK",
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        fontName=FONT,
        fontSize=11,
        leading=18,
        textColor=colors.HexColor("#374151"),
        wordWrap="CJK",
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="H1CJK",
        fontName=FONT,
        fontSize=17,
        leading=24,
        textColor=colors.HexColor("#111827"),
        wordWrap="CJK",
        spaceBefore=10,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="H2CJK",
        fontName=FONT,
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#0f766e"),
        wordWrap="CJK",
        spaceBefore=8,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCJK",
        fontName=FONT,
        fontSize=9.4,
        leading=15,
        textColor=colors.HexColor("#1f2937"),
        wordWrap="CJK",
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallCJK",
        fontName=FONT,
        fontSize=7.6,
        leading=11,
        textColor=colors.HexColor("#4b5563"),
        wordWrap="CJK",
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        fontName=FONT,
        fontSize=7.8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.white,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        fontName=FONT,
        fontSize=7.4,
        leading=10.5,
        textColor=colors.HexColor("#111827"),
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="Source",
        fontName=FONT,
        fontSize=7,
        leading=10,
        textColor=colors.HexColor("#6b7280"),
        wordWrap="CJK",
    )
)


def P(text, style="BodyCJK"):
    return Paragraph(text, styles[style])


def cell(text):
    return Paragraph(text, styles["TableCell"])


def head(text):
    return Paragraph(text, styles["TableHead"])


def make_table(rows, widths, header=True, small=False):
    data = []
    for r, row in enumerate(rows):
        if r == 0 and header:
            data.append([head(x) for x in row])
        else:
            data.append([cell(x) for x in row])
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e") if header else colors.white),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white if header else colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d1d5db")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def on_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, height - 12 * mm, "AI泡沫观察指标手册")
    canvas.drawRightString(width - 18 * mm, height - 12 * mm, "第 %d 页" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#e5e7eb"))
    canvas.line(18 * mm, height - 15 * mm, width - 18 * mm, height - 15 * mm)
    canvas.restoreState()


def build_story():
    story = []

    story.append(Spacer(1, 18 * mm))
    story.append(P("AI泡沫观察指标手册", "CoverTitle"))
    story.append(P("用应用现金流、模型经济性、云资本开支、GPU供需和融资环境，跟踪 AI 是否从真实建设走向泡沫反噬。", "CoverSub"))
    story.append(P("版本日期：2026-06-08。口径：美国和全球公开市场为主，结合私募模型公司、云厂商、半导体、数据中心和企业采用指标。", "SmallCJK"))
    story.append(Spacer(1, 10 * mm))

    summary_rows = [
        ["观察层级", "核心问题", "最重要的信号", "我的态度"],
        ["应用端", "企业是否真的省钱或赚钱", "续费率、付费席位、AI attach rate、AI 带来的 EBIT 或收入贡献", "这是第一领先指标"],
        ["模型层", "收入是否覆盖推理和训练成本", "ARR、毛利率、API 价格、推理成本、现金消耗", "最容易高收入但低利润"],
        ["云和基建", "capex 是否有可见回收期", "capex/revenue、折旧、自由现金流、订单 backlog、capex 指引", "泡沫温度计"],
        ["铲子端", "GPU 是否仍供不应求", "Nvidia 数据中心收入、交付周期、云 GPU 租赁价、库存", "会滞后反应"],
        ["资本市场", "估值是否脱离现金流", "Mag 7 权重、AI IPO 质量、私募估值、二级折价、信用利差", "会放大拐点"],
    ]
    story.append(make_table(summary_rows, [2.3 * cm, 4.0 * cm, 6.6 * cm, 3.0 * cm]))
    story.append(Spacer(1, 8 * mm))
    story.append(
        P(
            "一句话框架：不要问 AI 有没有未来，当然有。要问未来现金流是否足以支付今天的芯片、数据中心、电力、折旧和融资成本。",
            "BodyCJK",
        )
    )
    story.append(PageBreak())

    story.append(P("1. 总仪表盘：先看 12 个核心指标", "H1CJK"))
    story.append(
        P(
            "这些指标按领先性排序。越靠前越接近真实需求，越靠后越接近市场价格。观察时不要只看单个指标，要看组合是否同时转弱。",
            "BodyCJK",
        )
    )
    dashboard_rows = [
        ["优先级", "指标", "正常信号", "危险信号", "频率"],
        ["1", "企业 AI 续费率和席位净扩张", "续费稳定、席位增加、从试点转正式预算", "续费下降、席位缩减、项目回到试点", "季度"],
        ["2", "AI attach rate", "客户愿意为 AI 功能单独付费或升档", "AI 被免费捆绑，价格无法独立体现", "季度"],
        ["3", "企业级 ROI 案例", "能量化减少工时、提高转化率、降低客服成本", "只讲效率故事，不披露财务影响", "季度"],
        ["4", "模型公司 ARR 与毛利率", "收入增长同时毛利改善", "收入增长靠亏损推理和补贴换来", "季度"],
        ["5", "API 单位价格与用量", "价格下降但用量和收入更快增长", "价格战导致收入增速下滑", "月度"],
        ["6", "云 AI 收入增速", "云收入和 AI 相关收入同步加速", "capex 加速但云收入不加速", "季度"],
        ["7", "云 capex/revenue", "资本开支占收入比例稳定或下降", "capex 增速长期显著高于收入增速", "季度"],
        ["8", "自由现金流与折旧", "FCF 保持韧性，折旧可控", "利润好看但 FCF 被 capex 吃掉", "季度"],
        ["9", "GPU 交付周期与租赁价格", "高利用率、交付仍紧、租赁价稳定", "交付周期缩短、租赁价连续下跌", "月度"],
        ["10", "数据中心项目状态", "签约、上电、租赁和客户需求匹配", "项目延期、取消、空置率上升", "月度/季度"],
        ["11", "私募融资质量", "估值跟收入和毛利同步，条款干净", "估值跳涨、结构复杂、二级折价扩大", "月度"],
        ["12", "股票市场集中度", "上涨扩散到非 AI 行业盈利", "少数 AI 股支撑指数，市场宽度变差", "周度"],
    ]
    story.append(make_table(dashboard_rows, [1.05 * cm, 3.0 * cm, 4.35 * cm, 5.0 * cm, 1.55 * cm]))

    story.append(PageBreak())
    story.append(P("2. 应用端：第一领先指标", "H1CJK"))
    story.append(
        P(
            "应用端决定 AI 是否是生产力革命，还是昂贵玩具。2000 年互联网泡沫最先出问题的不是路由器，而是应用公司无法把用户和流量变成利润。AI 也一样，企业是否续费、扩容、独立付费，比模型 benchmark 更重要。",
            "BodyCJK",
        )
    )
    app_rows = [
        ["指标", "怎么观察", "健康状态", "危险状态"],
        ["续费率 / 净收入留存", "看 SaaS、AI 工具、企业 agent 平台披露；重点看 cohort 而非新增客户", "NRR 高于传统 SaaS，老客户扩容", "续费率下滑，客户从企业版降级到个人版或免费版"],
        ["AI attach rate", "看 Microsoft 365、Google Workspace、Salesforce、Adobe、ServiceNow 等 AI 加购率", "AI 成为付费模块，客户愿意为功能升档", "AI 功能被迫免费打包，只能作为防流失工具"],
        ["每席位收入", "看 AI 版价格相对普通版是否能长期维持溢价", "ARPU 上升，席位数也上升", "ARPU 靠短期促销或捆绑维持"],
        ["核心流程嵌入", "看 AI 是否进入客服、代码、营销投放、风控、财务、研发流程", "工作流被重写，形成系统性依赖", "只停留在写文案、总结会议、聊天问答"],
        ["可审计 ROI", "看客户案例是否披露节省金额、转化率、处理时长、缺陷率", "ROI 可复验，且多行业出现", "案例只讲百分比和愿景，不讲基数和成本"],
        ["预算来源", "看 AI 预算是新增预算，还是从软件/人力/咨询预算里替代", "从实验预算进入经营预算", "CFO 要求冻结新项目，AI 回归创新预算"],
    ]
    story.append(make_table(app_rows, [3.0 * cm, 5.1 * cm, 3.8 * cm, 4.0 * cm]))
    story.append(P("重点判断：如果客户愿意把 AI 写进年度预算，并把工作流迁到 AI 系统里，这是强信号；如果只是员工个人尝鲜，这是弱信号。", "BodyCJK"))

    story.append(P("3. 模型经济：收入增长不能替代利润质量", "H1CJK"))
    model_rows = [
        ["指标", "看什么", "危险信号", "为什么重要"],
        ["ARR", "OpenAI、Anthropic、xAI、Mistral、Perplexity 等收入运行率", "ARR 增速从三位数快速降到两位数", "高估值需要极高增速消化"],
        ["毛利率", "收入扣除推理成本、云成本和折扣后的真实毛利", "用量越大亏得越多", "模型公司可能高收入但低利润"],
        ["推理成本/百万 token", "单位 token 成本是否持续下降", "成本下降慢于 API 降价", "决定价格战能否承受"],
        ["API 价格", "主流模型输入/输出价格、批处理价格、长上下文价格", "连续降价但客户不明显扩量", "商品化压力直接打毛利"],
        ["训练资本开支", "新一代模型训练和数据成本", "每代模型成本上升，但能力边际提升变小", "容易形成军备竞赛"],
        ["客户集中度", "前 10 大客户收入占比、云伙伴贡献", "少数客户或关联交易撑 ARR", "会放大收入波动"],
        ["现金消耗", "年度亏损、融资间隔、可用现金 runway", "融资越来越大，亏损也越来越大", "泡沫会先在融资端断裂"],
    ]
    story.append(make_table(model_rows, [2.9 * cm, 4.4 * cm, 4.3 * cm, 4.3 * cm]))
    story.append(P("重点判断：模型公司的危险不是没有收入，而是收入真实但经济性不真实。若推理价格战先于成本下降，利润池会向云、芯片或应用入口转移。", "BodyCJK"))

    story.append(PageBreak())
    story.append(P("4. 云厂商和 capex：AI 泡沫的温度计", "H1CJK"))
    story.append(
        P(
            "四大云厂商的资本开支是本轮 AI 周期最关键的宏观变量。它连接上游 GPU、数据中心、电力和下游企业需求。观察重点不是 capex 大不大，而是收入、利用率、折旧和自由现金流能不能承接。",
            "BodyCJK",
        )
    )
    capex_rows = [
        ["指标", "计算方式", "健康状态", "危险状态"],
        ["capex/revenue", "资本开支 / 总收入，或 AI capex / 云收入", "短期上升后趋稳，收入开始跟上", "连续数年上升，收入增速落后"],
        ["capex 增速 - 云收入增速", "资本开支同比减云收入同比", "差值收窄", "capex 增速长期高出收入 30 个点以上"],
        ["自由现金流", "经营现金流 - capex", "FCF 仍为正且可解释", "利润增长但 FCF 接近零或转负"],
        ["折旧压力", "折旧摊销 / 收入或营业利润", "折旧被新增收入吸收", "折旧开始压缩云利润率"],
        ["backlog 质量", "云订单 backlog、剩余履约义务、客户承诺期", "backlog 可转收入，客户多元", "backlog 依赖少数 AI 公司或循环交易"],
        ["管理层措辞", "财报电话会中的需求和供给描述", "仍明确 capacity constrained", "开始说优化节奏、重新评估、延后项目"],
        ["融资方式", "经营现金流、发债、增发、售后回租、项目融资", "现金流覆盖大部分投入", "越来越依赖债务、增发和结构化融资"],
    ]
    story.append(make_table(capex_rows, [2.8 * cm, 4.2 * cm, 4.2 * cm, 4.7 * cm]))
    story.append(P("重点判断：真正的拐点往往不是第一家芯片公司收入下滑，而是某个 hyperscaler 首次明确下调下一年度 capex。", "BodyCJK"))

    story.append(P("5. GPU、半导体和设备：铲子端信号", "H1CJK"))
    gpu_rows = [
        ["指标", "领先/滞后", "健康状态", "危险状态"],
        ["Nvidia 数据中心收入", "偏滞后", "增速虽放缓但订单可见性强", "收入指引低于预期，客户推迟订单"],
        ["HBM 和先进封装供需", "领先", "仍紧缺，价格稳定", "供应紧张缓解但终端需求未同步扩大"],
        ["GPU 交付周期", "领先", "交付仍排队", "从缺货转现货，渠道库存上升"],
        ["云 GPU 租赁价", "领先", "高端卡租价稳定，利用率高", "租价连续下跌，短租折扣扩大"],
        ["库存天数", "偏领先", "库存随收入增长可控", "库存和应收账款快于收入增长"],
        ["客户集中度", "风险项", "大型云厂商需求均衡", "少数客户贡献过高，任一客户砍单即冲击"],
        ["毛利率", "滞后", "高毛利可维持", "价格压力或产品转换导致毛利下滑"],
    ]
    story.append(make_table(gpu_rows, [3.0 * cm, 2.0 * cm, 5.0 * cm, 5.9 * cm]))
    story.append(P("重点判断：铲子端崩得通常比应用端晚，但一旦应用端需求被证伪，铲子端会用库存、毛利率和订单取消的形式快速补跌。", "BodyCJK"))

    story.append(PageBreak())
    story.append(P("6. 数据中心、电力和地产：重资产链条", "H1CJK"))
    infra_rows = [
        ["指标", "观察点", "危险信号"],
        ["数据中心空置率", "北美主要市场、欧洲 FLAP-D、亚太核心城市", "新项目交付后空置率上行，预租率下降"],
        ["租金和租期", "批发数据中心租金、长期租约、续约价", "租金见顶，短租或灵活租约增加"],
        ["上电时间", "电网接入、变压器、冷却、许可", "项目延期不是需求问题时可中性；需求弱导致延期才危险"],
        ["PPA 电力协议", "长期购电、核电、燃气、电池储能", "以高价锁定长期电力，但算力需求不确定"],
        ["项目取消", "数据中心、园区、GPU 集群、海底光缆", "取消从小项目扩散到头部云厂商项目"],
        ["融资成本", "REIT、项目债、私募信贷、设备租赁", "信用利差扩大，融资期限缩短，抵押品折价"],
        ["水和环保约束", "冷却用水、地方许可、社区反对", "监管导致建设节奏低于收入承诺"],
    ]
    story.append(make_table(infra_rows, [3.2 * cm, 5.6 * cm, 7.1 * cm]))

    story.append(P("7. 融资和资本市场：泡沫的放大器", "H1CJK"))
    finance_rows = [
        ["指标", "健康状态", "危险状态"],
        ["私募估值 / ARR", "估值倍数随毛利、留存、增长而分化", "亏损公司仍以极高 PS 融资"],
        ["二级市场折价", "员工和早期投资人小幅流动性交易", "二级价格显著低于上一轮估值"],
        ["融资条款", "普通优先股条款清晰", "清算优先权、保底收益、结构化条款复杂化"],
        ["债务融资", "资产和现金流匹配", "GPU 抵押、云承诺、项目债形成影子杠杆"],
        ["IPO 质量", "有收入、有毛利、有留存", "亏损公司靠 AI 叙事高估值上市"],
        ["并购", "能力互补型并购", "大量 acqui-hire、低价收购、人才回收"],
        ["信用利差", "AI 数据中心和科技债利差稳定", "利差上行但股价仍乐观"],
    ]
    story.append(make_table(finance_rows, [3.4 * cm, 5.6 * cm, 6.9 * cm]))

    story.append(PageBreak())
    story.append(P("8. 市场价格和情绪：结果指标，但不能忽略", "H1CJK"))
    market_rows = [
        ["指标", "看什么", "危险信号"],
        ["Mag 7 占 S&P 500 权重", "少数科技股对指数贡献", "权重继续上升，但市场宽度变差"],
        ["AI 产业链相关性", "Nvidia、Broadcom、TSMC、内存、数据中心 REIT、云厂商", "全链条同涨同跌，相关性接近单一交易"],
        ["估值口径", "PE、PS、EV/EBITDA、FCF yield", "从利润转向 TAM、token、算力份额等叙事指标"],
        ["分析师一致预期", "未来 2-3 年收入和利润预测", "盈利预测过度依赖远期毛利率改善"],
        ["市场宽度", "等权指数、非科技盈利增长、上涨家数", "指数创新高但多数股票疲弱"],
        ["散户和媒体情绪", "AI 概念搜索量、开户、期权交易", "小市值公司改名 AI 后暴涨"],
    ]
    story.append(make_table(market_rows, [3.2 * cm, 5.2 * cm, 7.5 * cm]))

    story.append(P("9. 竞争和商品化：技术进步也可能杀估值", "H1CJK"))
    comp_rows = [
        ["指标", "为什么重要", "危险信号"],
        ["开源模型差距", "若开源逼近闭源，闭源 API 定价权下降", "企业用开源或小模型替代高价 API"],
        ["小模型能力", "推理成本可能被边缘端和小模型压低", "高端大模型只剩少数复杂任务可收费"],
        ["模型切换成本", "决定模型公司护城河", "开发者可在多模型平台低成本切换"],
        ["入口控制", "办公套件、浏览器、手机、云平台是否锁住分发", "模型公司被入口平台抽成或压价"],
        ["价格战", "最直接伤害毛利", "主流模型连续降价，仍无法扩大付费需求"],
        ["监管和数据权利", "影响训练数据和企业部署", "版权、隐私、跨境数据限制提高成本"],
    ]
    story.append(make_table(comp_rows, [3.0 * cm, 5.2 * cm, 7.7 * cm]))

    story.append(PageBreak())
    story.append(P("10. 情景矩阵：如何判断泡沫是否正在破", "H1CJK"))
    scenario_rows = [
        ["情景", "组合信号", "判断"],
        ["健康建设期", "企业续费强，AI 单独收费成功；云收入加速；capex/revenue 开始趋稳；GPU 租价稳定；模型毛利改善", "技术和商业同时兑现，估值仍可能高，但不是典型泡沫破裂"],
        ["温和降温", "capex 增速下降；GPU 交付缓解；估值回落；但企业续费和云收入保持健康", "泡沫挤压，但产业继续扩张"],
        ["应用端证伪", "AI 工具续费下降；客户削减试点；模型 API 降价；AI 收入披露模糊；企业 ROI 案例减少", "这是最值得警惕的第一阶段"],
        ["铲子端反噬", "云 capex 下调；GPU 租价下跌；订单推迟；库存增加；半导体毛利下降", "类似 2001 年电信设备链条，杀伤力大"],
        ["资本市场踩踏", "私募二级折价扩大；IPO 失败；AI 信用利差上升；Mag 7 权重回落拖累指数", "泡沫从产业问题变成资产负债表问题"],
    ]
    story.append(make_table(scenario_rows, [3.0 * cm, 8.3 * cm, 4.6 * cm]))

    story.append(P("11. 每月/每季跟踪模板", "H1CJK"))
    tracking_rows = [
        ["周期", "必看事项", "记录方式"],
        ["每周", "Nvidia、云厂商、AI 软件股相对表现；GPU 租赁价格；AI 相关新闻中的项目取消和融资失败", "写 5 行周记：价格、需求、融资、监管、异常事件"],
        ["每月", "云 GPU 价格、数据中心租赁、AI 私募融资、API 价格表、开源模型进展", "更新趋势表，标红连续 2 个月恶化的指标"],
        ["每季", "Microsoft、Amazon、Alphabet、Meta、Nvidia、Broadcom、TSMC 财报和电话会", "提取 capex、收入增速、FCF、库存、管理层措辞"],
        ["半年", "企业 AI 调查、CIO 预算、AI ROI 案例、就业和生产率研究", "判断 AI 是否从工具采用进入组织级财务贡献"],
    ]
    story.append(make_table(tracking_rows, [2.3 * cm, 9.1 * cm, 4.5 * cm]))

    story.append(PageBreak())
    story.append(P("12. 关键阈值：我的个人红黄绿灯", "H1CJK"))
    lights_rows = [
        ["层级", "绿灯", "黄灯", "红灯"],
        ["应用端", "续费强，AI 升档带来 ARPU 上升", "试点多但预算转化慢", "续费下降，AI 功能免费化"],
        ["模型端", "ARR 增长且毛利改善", "ARR 高增但亏损扩大", "价格战叠加现金消耗扩大"],
        ["云端", "capex 增速逐步低于云收入增速", "capex 和收入都高增但 FCF 承压", "capex 下调因为需求不及预期"],
        ["GPU", "高利用率，租价稳，交付紧", "租价松动，交付周期缩短", "订单取消、库存上升、毛利率下滑"],
        ["数据中心", "预租率高，上电瓶颈是供给约束", "项目延期但客户仍在", "空置率上升，项目取消扩散"],
        ["融资", "估值与收入质量分化", "结构化条款增加", "二级大幅折价，债务融资收紧"],
        ["市场", "盈利扩散，AI 股不再独撑指数", "指数集中但基本面仍强", "少数 AI 股下跌拖累全市场"],
    ]
    story.append(make_table(lights_rows, [2.5 * cm, 4.4 * cm, 4.4 * cm, 4.6 * cm]))
    story.append(
        P(
            "最强预警组合：企业 ROI 不清 + 模型 API 价格战 + 云 capex 下调 + GPU 租赁价格下跌 + Nvidia 或上游订单放缓。这个组合出现时，应把 AI 从成长故事重新定价为资本开支过剩故事。",
            "BodyCJK",
        )
    )

    story.append(P("13. 数据来源建议", "H1CJK"))
    source_rows = [
        ["类别", "建议来源"],
        ["公司财报", "Microsoft、Amazon、Alphabet、Meta、Nvidia、Broadcom、TSMC、Oracle、CoreWeave 等财报、10-Q/10-K、电话会文字稿"],
        ["宏观和估值", "FRED、BEA、IMF WEO、Wilshire 5000、Buffett Indicator、S&P 500 sector factsheets"],
        ["企业采用", "McKinsey State of AI、Stanford AI Index、NBER firm AI surveys、CIO survey、Ramp AI Index"],
        ["私募融资", "PitchBook、S&P Global Market Intelligence、Crunchbase、The Information、Reuters、Axios"],
        ["算力价格", "云厂商公开价格、GPU 租赁平台、neocloud 报价、二手 GPU 市场、行业渠道数据"],
        ["数据中心", "CBRE、JLL、Data Center Dynamics、REIT 财报、电力公司 interconnection queue、PPA 公告"],
    ]
    story.append(make_table(source_rows, [3.0 * cm, 12.9 * cm]))
    story.append(P("说明：本手册是观察框架，不构成投资建议。指标阈值应结合利率、会计口径、海外收入占比和行业生命周期动态调整。", "Source"))

    return story


def main():
    frame = Frame(18 * mm, 16 * mm, A4[0] - 36 * mm, A4[1] - 34 * mm, id="normal")
    doc = BaseDocTemplate(
        str(OUT_FILE),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="AI泡沫观察指标手册",
        author="Codex",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    doc.build(build_story())
    print(OUT_FILE)


if __name__ == "__main__":
    main()
