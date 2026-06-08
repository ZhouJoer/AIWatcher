# Publish To A Remote Git Repository

This file does not assume any hosting provider or fixed repository URL.

Replace `<REMOTE_URL>` with your own remote repository URL.

## Command Line

Run these commands from the project root:

```bash
git init
git branch -M main
git remote add origin <REMOTE_URL>
git add .
git commit -m "Initialize AIWatcher workflow"
git push -u origin main
```

If the remote repository already has content:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Web Upload

1. Open your remote repository page.
2. Choose the provider's file upload option.
3. Upload the files from this project directory.
4. Commit the upload.

## After Publishing

Confirm that these files exist:

- `README.md`
- `AGENTS.md`
- `docs/agent_runbook.md`
- `prompts/weekly_ai_risk_review.md`
- `data/ai_risk_metrics.json`
- `output/ai_risk_dashboard.html`
- `docs/AI风险基准评估_2026-06-08.md`

## Optional Static Hosting

If your Git host supports static hosting, publish:

```text
output/ai_risk_dashboard.html
```

For a cleaner static site, copy or generate the dashboard as:

```text
docs/index.html
```
