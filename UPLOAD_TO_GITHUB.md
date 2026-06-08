# 上传到 GitHub

目标仓库：

```text
https://github.com/ZhouJoer/AIWatcher.git
```

## 方法一：命令行上传

在 PowerShell 中运行：

```powershell
cd E:\ai\作文\AIWatcher
git init
git branch -M main
git remote add origin https://github.com/ZhouJoer/AIWatcher.git
git add .
git commit -m "Initialize AIWatcher workflow"
git push -u origin main
```

如果远程仓库已经有内容，先拉取并合并：

```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 方法二：网页上传

1. 打开 https://github.com/ZhouJoer/AIWatcher
2. 选择 `Add file` -> `Upload files`
3. 上传 `E:\ai\作文\AIWatcher` 目录中的文件
4. 提交 commit

## 上传后检查

上传后确认：

- README 能正常显示中文。
- `output/ai_risk_dashboard.html` 存在。
- `docs/AI风险基准评估_2026-06-08.md` 存在。
- GitHub Actions 页面能看到 `Render AI risk dashboard` 工作流。

## GitHub Pages 可选设置

如果想让仪表盘变成网页：

1. 进入仓库 Settings -> Pages。
2. Source 选择 `Deploy from a branch`。
3. Branch 选择 `main`，目录可以选 `/root`。
4. 访问 `output/ai_risk_dashboard.html`。

更正式的方式是把 HTML 放到 `docs/index.html`，然后 Pages 指向 `/docs`。
