# AI Agent Runbook

This runbook turns AIWatcher into an out-of-the-box agent workflow.

The agent's role is to research, score, update, render, and alert.

## 1. Start Here

Open and read:

```text
AGENTS.md
data/ai_risk_metrics.json
docs/AI风险基准评估_2026-06-08.md
docs/AI风险观察工作流.md
output/ai_risk_dashboard.md
```

The current baseline is:

```text
Baseline date: 2026-06-08
Baseline total risk: 67.8 / 100
Baseline status: Orange
```

Do not reset the baseline unless explicitly asked.

## 2. Research Sources

Prefer primary sources where available:

| Layer | Sources |
|---|---|
| Cloud capex | Microsoft, Amazon, Alphabet, Meta, Oracle earnings releases, 10-Q, 10-K, investor calls |
| GPU demand | Nvidia, Broadcom, TSMC, memory suppliers, cloud GPU price pages |
| Application ROI | SaaS company earnings, CIO surveys, McKinsey, Stanford AI Index, NBER |
| Model economics | OpenAI, Anthropic, xAI, Mistral, Reuters, The Information, PitchBook |
| Data centers | CBRE, JLL, Data Center Dynamics, REIT filings, utility interconnection queues |
| Financing | PitchBook, S&P Global Market Intelligence, Reuters, private credit reports |
| Market concentration | S&P factsheets, Wilshire 5000, Buffett Indicator, market breadth data |
| Macro | FRED, BEA, Treasury yields, credit spreads |

When using non-primary sources, identify them as secondary sources.

## 3. Evidence Classification

Classify each finding as one of:

- Hard data: financial statement, filing, company guidance, official pricing.
- Strong signal: repeated company commentary, multiple independent reports, confirmed project cancellation.
- Weak signal: media speculation, anonymous source, one-off anecdote.
- Inference: your judgment derived from multiple signals.

Only hard data and strong signals should usually change scores.

## 4. Score Update Logic

Use the existing layer and indicator weights in `data/ai_risk_metrics.json`.

Score change guidance:

| Change | Meaning |
|---:|---|
| 1-3 | Minor signal, watchlist update |
| 4-7 | Meaningful change in a layer |
| 8-12 | Major evidence shift |
| 13+ | Confirmed breakpoint |

Examples:

- A single CEO says demand is strong: usually no score change.
- Hyperscaler raises capex without revenue acceleration: +2 to +5 for cloud capex.
- Hyperscaler cuts capex due to weaker AI demand: +8 to +15 for cloud capex.
- GPU rental prices fall for several months: +4 to +8 for GPU layer.
- Enterprise AI renewals fall across several SaaS vendors: +8 to +12 for application ROI.
- Open-source models force repeated API price cuts: +4 to +8 for model economics and competition.

## 5. Files To Update

Required if evidence changed:

```text
data/ai_risk_metrics.json
output/ai_risk_dashboard.html
output/ai_risk_dashboard.md
```

Optional but recommended:

```text
reports/YYYY-MM-DD_agent_alert.md
```

Do not overwrite the baseline report unless the user asks to create a new baseline.

## 6. Render Dashboard

Run:

```powershell
python .\tools\ai_risk_dashboard.py
```

On Linux/macOS:

```bash
python tools/ai_risk_dashboard.py
```

If `output/` is locked locally, the script may write fallback files under `generated/`.

## 7. Alert Format

Use:

```text
templates/agent_alert_template.md
```

The alert must be short enough to read quickly, but specific enough to explain why scores changed.

## 8. Do Not Do These

- Do not change scores just because AI stock prices moved.
- Do not treat adoption as ROI.
- Do not treat capex growth as automatically good or bad. Compare it with revenue, FCF, depreciation, and utilization.
- Do not hide uncertainty.
- Do not reset the baseline casually.
- Do not update generated files without checking whether the source JSON changed.

