# Weekly AI Risk Review Prompt

You are operating the AIWatcher repository as an AI research agent.

## Objective

Assess whether AI bubble risk has changed since the baseline in `data/ai_risk_metrics.json`, update the dashboard if justified, and produce a concise alert.

## Required Steps

1. Read:
   - `AGENTS.md`
   - `docs/agent_runbook.md`
   - `data/ai_risk_metrics.json`
   - `docs/AI风险基准评估_2026-06-08.md`
   - `output/ai_risk_dashboard.md`

2. Research the latest public signals for:
   - Application ROI and enterprise adoption quality
   - Model company ARR, margin, API pricing, cash burn
   - Microsoft, Amazon, Alphabet, Meta, Oracle capex guidance
   - Nvidia data center revenue, guidance, backlog, inventory
   - GPU delivery time and cloud GPU rental prices
   - Data center project delays, cancellations, power constraints, PPA and financing
   - Frontier model private valuations and secondary market discounts
   - Mag 7 concentration and market breadth
   - Open-source/small-model commoditization
   - Interest rates, credit spreads, regulation and legal risk

3. Classify evidence:
   - Hard data
   - Strong signal
   - Weak signal
   - Inference

4. Decide whether any indicator score should change.

5. If scores change:
   - Update `data/ai_risk_metrics.json`
   - Update `metadata.as_of`
   - Run `python .\tools\ai_risk_dashboard.py`
   - Create `reports/YYYY-MM-DD_agent_alert.md`

6. If scores do not change:
   - Do not edit the JSON.
   - Still produce a short no-change alert.

## Alert Must Include

- Current total risk score and status
- Change versus baseline
- Red/orange layers
- Top 3-5 changes
- Whether the red alert combination has appeared
- Data sources used
- Files changed

## Red Alert Combination

```text
Enterprise ROI unclear
+ model API price war
+ hyperscaler capex cut
+ GPU rental prices falling
+ Nvidia or upstream order slowdown
```

