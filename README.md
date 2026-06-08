# AIWatcher

AIWatcher 是一个用于跟踪 AI 泡沫和资本开支风险的轻量仪表盘工作流。

它不是预测工具，也不是投资建议。它的目标是把一组容易分散在财报、新闻、私募融资、GPU 价格、数据中心和宏观数据里的风险信号，固化成一个可定期更新、可比较的基准仪表盘。

## 开箱即用的 AI Agent 工作流

本仓库的核心是 AI agent 工作流。

任何支持读取仓库文件、检索公开资料、编辑文件和运行本地命令的 AI agent，都可以按下面入口直接执行巡检：

```text
AGENTS.md
docs/agent_runbook.md
prompts/weekly_ai_risk_review.md
```

推荐 agent 任务：

```text
按 AGENTS.md 和 prompts/weekly_ai_risk_review.md 执行一次 AI 风险巡检。读取最新公开信息，判断风险是否较基准变化；如有必要，更新 data/ai_risk_metrics.json，运行 python .\tools\ai_risk_dashboard.py，并在 reports/ 下生成本次提醒。
```

Agent 要做的不是简单渲染，而是：

1. 读取基准和指标 JSON。
2. 检索最新财报、公司指引、GPU 价格、数据中心、电力、融资和市场集中度变化。
3. 区分硬数据、强信号、弱信号和推断。
4. 判断是否需要调整分数。
5. 更新 JSON 和仪表盘。
6. 生成一份可读的风险提醒。

## 当前基准

- 基准日期：2026-06-08
- 总风险值：67.8 / 100
- 状态：橙灯偏高
- 核心判断：AI 技术长期真实，但短中期资产定价、云资本开支、私募估值和市场集中度已经提前计入了很高的未来兑现率。

## 仓库结构

```text
AIWatcher/
  data/
    ai_risk_metrics.json              # 指标、权重、分数、趋势和观察备注
  tools/
    ai_risk_dashboard.py              # 生成 HTML/Markdown 仪表盘
    generate_ai_bubble_dashboard_pdf.py# 生成 PDF 手册
  docs/
    AI风险观察工作流.md
    AI风险基准评估_2026-06-08.md
  output/
    ai_risk_dashboard.html
    ai_risk_dashboard.md
    pdf/
      AI泡沫观察指标手册.pdf
```

## 快速开始

安装依赖：

```powershell
pip install -r requirements.txt
```

刷新风险仪表盘：

```powershell
python .\tools\ai_risk_dashboard.py
```

生成 PDF 手册：

```powershell
python .\tools\generate_ai_bubble_dashboard_pdf.py
```

输出文件：

- `output/ai_risk_dashboard.html`
- `output/ai_risk_dashboard.md`
- `output/pdf/AI泡沫观察指标手册.pdf`

## 如何更新风险基准

编辑 `data/ai_risk_metrics.json`：

- `metadata.as_of`：数据日期。
- `score`：0-100，越高表示泡沫和回撤风险越高。
- `trend`：`up`、`down`、`watch`、`flat`。
- `current_read`：当前判断。
- `watch_signals`：值得提醒的危险信号。

然后运行：

```powershell
python .\tools\ai_risk_dashboard.py
```

## 评分规则

| 分数 | 状态 | 含义 |
|---:|---|---|
| 0-39 | 绿灯 | 风险低 |
| 40-59 | 黄灯 | 需要观察 |
| 60-74 | 橙灯 | 风险偏高 |
| 75-100 | 红灯 | 需要重点警惕 |

## 最重要的预警组合

如果同时出现以下信号，应把总风险上调到红灯区间：

```text
企业 ROI 不清
+ 模型 API 价格战
+ 云 capex 下调
+ GPU 租赁价格下跌
+ Nvidia 或上游订单放缓
```

## 定时巡检

本仓库不绑定任何特定 agent 或托管地址。推荐在你选择的 agent 环境里配置定时任务，让 agent 按 `AGENTS.md` 执行完整巡检。

定时任务提示词见：

```text
prompts/weekly_ai_risk_review.md
docs/scheduled_agent_prompt.md
```

定时 agent 应该完成：

1. 读取基准和指标。
2. 检索最新公开资料。
3. 判断风险是否变化。
4. 必要时更新 `data/ai_risk_metrics.json`。
5. 重新生成仪表盘。
6. 在 `reports/` 下输出本次提醒。

## 重要说明

AIWatcher 的分数是研究和复盘工具，不是交易信号。它适合用来回答：

- AI 风险是否比上周升温？
- 风险来自应用端、模型端、云 capex，还是市场估值？
- 有没有出现类似 2000 年互联网泡沫中“应用端证伪后传导到铲子端”的组合？
