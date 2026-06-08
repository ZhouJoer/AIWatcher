# Codex 定时巡检提示词

如果需要在 Codex 里重新创建定时巡检，可以使用以下任务说明。

```text
检查 AI 泡沫风险观察工作流的最新变化。先阅读 `docs/AI风险观察工作流.md`、`data/ai_risk_metrics.json` 和 `output/pdf/AI泡沫观察指标手册.pdf` 的核心框架；然后核对最近公开信息和公司动态，重点关注应用端 ROI、模型公司 ARR 和毛利率、云厂商 capex 指引、GPU 交付周期和租赁价格、数据中心项目、电力和融资、私募估值、市场集中度、模型价格战、宏观流动性与监管风险。

若发现指标有实质变化，更新 `data/ai_risk_metrics.json` 中对应 `score`、`trend`、`current_read`、`watch_signals` 和 `metadata.as_of`，运行 `python .\tools\ai_risk_dashboard.py` 生成 `output/ai_risk_dashboard.html` 和 `output/ai_risk_dashboard.md`。

最后给出简洁提醒：总风险值、红灯/橙灯层级、较上次最值得注意的 3-5 个变化、是否出现“企业 ROI 不清 + 模型 API 价格战 + 云 capex 下调 + GPU 租赁价格下跌 + Nvidia 或上游订单放缓”的组合。
```
