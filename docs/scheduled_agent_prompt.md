# Scheduled Agent Prompt

Use this prompt with any scheduled AI agent that can read repository files, search public sources, edit files, and run local commands.

```text
Execute one AIWatcher risk review according to `AGENTS.md` and `prompts/weekly_ai_risk_review.md`.

First read:
- `docs/agent_runbook.md`
- `data/ai_risk_metrics.json`
- `docs/AI风险基准评估_2026-06-08.md`
- `docs/AI风险观察工作流.md`
- `output/ai_risk_dashboard.md`

Then review the latest public information and company updates. Focus on:
- application ROI
- model company ARR and margin
- cloud capex guidance
- GPU delivery time and rental pricing
- data center projects
- power and financing
- private valuations
- market concentration
- model price competition
- macro liquidity
- regulatory and legal risk

Classify evidence as hard data, strong signal, weak signal, or inference.

If there is a meaningful change, update `data/ai_risk_metrics.json`, including `score`, `trend`, `current_read`, `watch_signals`, and `metadata.as_of`.

Run:

`python ./tools/ai_risk_dashboard.py`

Create a report at:

`reports/YYYY-MM-DD_agent_alert.md`

Use `templates/agent_alert_template.md` as the report structure.

The final alert must include:
- total risk score
- change versus baseline
- red/orange layers
- top 3-5 changes
- whether the red alert combination appeared
- main sources used
- files changed
```

