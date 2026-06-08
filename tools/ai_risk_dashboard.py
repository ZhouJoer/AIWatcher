import json
from collections import defaultdict
from datetime import datetime
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "ai_risk_metrics.json"
OUT_DIR = ROOT / "output"
HTML_FILE = OUT_DIR / "ai_risk_dashboard.html"
MD_FILE = OUT_DIR / "ai_risk_dashboard.md"
FALLBACK_OUT_DIR = ROOT / "generated"


def risk_label(score):
    if score >= 75:
        return "红灯"
    if score >= 60:
        return "橙灯"
    if score >= 40:
        return "黄灯"
    return "绿灯"


def risk_class(score):
    if score >= 75:
        return "red"
    if score >= 60:
        return "orange"
    if score >= 40:
        return "yellow"
    return "green"


def trend_label(trend):
    return {
        "up": "风险上升",
        "down": "风险下降",
        "watch": "观察中",
        "flat": "持平"
    }.get(trend, trend)


def weighted_average(items):
    total_weight = sum(item["weight"] for item in items)
    if total_weight == 0:
        return 0
    return sum(item["score"] * item["weight"] for item in items) / total_weight


def load_dashboard():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    layer_weights = data["layer_weights"]
    indicators = data["indicators"]

    grouped = defaultdict(list)
    for indicator in indicators:
        grouped[indicator["layer"]].append(indicator)

    layer_scores = []
    for layer, items in grouped.items():
        layer_score = sum(i["score"] for i in items) / len(items)
        layer_scores.append(
            {
                "layer": layer,
                "score": round(layer_score, 1),
                "weight": layer_weights.get(layer, 0),
                "count": len(items),
                "label": risk_label(layer_score),
                "class": risk_class(layer_score),
            }
        )

    layer_scores.sort(key=lambda x: x["weight"], reverse=True)
    overall = weighted_average(layer_scores)
    return data, layer_scores, round(overall, 1)


def render_bar(score):
    klass = risk_class(score)
    return f"""
    <div class="bar">
      <div class="bar-fill {klass}" style="width: {max(0, min(100, score))}%"></div>
    </div>
    """


def render_html(data, layer_scores, overall):
    meta = data["metadata"]
    indicators = sorted(data["indicators"], key=lambda x: (x["layer"], -x["score"]))
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = []
    for item in indicators:
        signals = "；".join(item["watch_signals"])
        sources = "；".join(item["source_suggestions"])
        rows.append(
            f"""
            <tr>
              <td>{escape(item["layer"])}</td>
              <td><strong>{escape(item["name"])}</strong><br><span>{escape(item["current_read"])}</span></td>
              <td class="score {risk_class(item["score"])}">{item["score"]}<br>{risk_label(item["score"])}</td>
              <td>{escape(trend_label(item["trend"]))}</td>
              <td>{escape(item["cadence"])}</td>
              <td>{escape(signals)}</td>
              <td>{escape(sources)}</td>
            </tr>
            """
        )

    cards = []
    for layer in layer_scores:
        cards.append(
            f"""
            <section class="card">
              <div class="card-top">
                <h3>{escape(layer["layer"])}</h3>
                <span class="pill {layer["class"]}">{layer["score"]} · {escape(layer["label"])}</span>
              </div>
              {render_bar(layer["score"])}
              <p>权重 {layer["weight"]}% · 指标 {layer["count"]} 个</p>
            </section>
            """
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(meta["title"])}</title>
  <style>
    :root {{
      --text: #172033;
      --muted: #64748b;
      --line: #d8dee9;
      --bg: #f7f8fb;
      --panel: #ffffff;
      --green: #16a34a;
      --yellow: #ca8a04;
      --orange: #ea580c;
      --red: #dc2626;
      --teal: #0f766e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "Noto Sans SC", "PingFang SC", Arial, sans-serif;
      color: var(--text);
      background: var(--bg);
      line-height: 1.55;
    }}
    header {{
      background: #0f172a;
      color: white;
      padding: 34px 42px;
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: 30px;
      letter-spacing: 0;
    }}
    header p {{
      margin: 4px 0;
      color: #cbd5e1;
      max-width: 980px;
    }}
    main {{ padding: 26px 42px 42px; }}
    .overall {{
      display: grid;
      grid-template-columns: 190px 1fr;
      gap: 22px;
      align-items: center;
      background: var(--panel);
      border: 1px solid var(--line);
      padding: 20px;
      margin-bottom: 22px;
    }}
    .gauge {{
      height: 150px;
      border: 10px solid var(--line);
      display: grid;
      place-items: center;
      text-align: center;
      background: #fff;
    }}
    .gauge .num {{ font-size: 42px; font-weight: 700; }}
    .gauge .label {{ color: var(--muted); }}
    h2 {{ margin: 26px 0 12px; font-size: 20px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      padding: 14px;
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
    }}
    .card h3 {{ margin: 0; font-size: 15px; }}
    .card p {{ margin: 8px 0 0; color: var(--muted); font-size: 13px; }}
    .pill {{
      padding: 3px 8px;
      color: white;
      font-size: 12px;
      white-space: nowrap;
    }}
    .green {{ background: var(--green); }}
    .yellow {{ background: var(--yellow); }}
    .orange {{ background: var(--orange); }}
    .red {{ background: var(--red); }}
    .bar {{
      width: 100%;
      height: 9px;
      background: #e5e7eb;
      margin-top: 12px;
      overflow: hidden;
    }}
    .bar-fill {{ height: 100%; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--line);
      font-size: 13px;
    }}
    th {{
      background: var(--teal);
      color: white;
      text-align: left;
      padding: 9px;
      font-weight: 600;
    }}
    td {{
      border-top: 1px solid var(--line);
      padding: 9px;
      vertical-align: top;
    }}
    td span {{ color: var(--muted); font-size: 12px; }}
    td.score {{
      color: white;
      text-align: center;
      font-weight: 700;
      min-width: 70px;
    }}
    .note {{
      background: #ecfeff;
      border-left: 4px solid var(--teal);
      padding: 12px 14px;
      margin-top: 14px;
    }}
    footer {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 24px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(meta["title"])}</h1>
    <p>{escape(meta["thesis"])}</p>
    <p>数据日期：{escape(meta["as_of"])} · 仪表盘生成：{updated_at}</p>
  </header>
  <main>
    <section class="overall">
      <div class="gauge">
        <div>
          <div class="num">{overall}</div>
          <div class="label">总风险 · {risk_label(overall)}</div>
        </div>
      </div>
      <div>
        <h2>当前判断</h2>
        <p>{escape(meta["scoring_note"])}</p>
        <div class="note">最值得盯的组合：企业ROI不清 + 模型API价格战 + 云capex下调 + GPU租赁价格下跌 + Nvidia或上游订单放缓。</div>
      </div>
    </section>
    <h2>分层风险值</h2>
    <section class="grid">
      {"".join(cards)}
    </section>
    <h2>指标明细</h2>
    <table>
      <thead>
        <tr>
          <th>层级</th>
          <th>指标与当前读数</th>
          <th>风险值</th>
          <th>趋势</th>
          <th>频率</th>
          <th>危险信号</th>
          <th>建议来源</th>
        </tr>
      </thead>
      <tbody>
        {"".join(rows)}
      </tbody>
    </table>
    <footer>说明：本仪表盘是风险观察工具，不构成投资建议。请结合最新财报、市场价格和宏观环境更新分数。</footer>
  </main>
</body>
</html>
"""


def render_markdown(data, layer_scores, overall):
    meta = data["metadata"]
    lines = [
        f"# {meta['title']}",
        "",
        f"- 数据日期：{meta['as_of']}",
        f"- 总风险：{overall} / 100（{risk_label(overall)}）",
        f"- 评分说明：{meta['scoring_note']}",
        "",
        f"> {meta['thesis']}",
        "",
        "## 分层风险值",
        "",
        "| 层级 | 权重 | 风险值 | 状态 | 指标数 |",
        "|---|---:|---:|---|---:|",
    ]
    for layer in layer_scores:
        lines.append(f"| {layer['layer']} | {layer['weight']}% | {layer['score']} | {layer['label']} | {layer['count']} |")

    lines.extend(
        [
            "",
            "## 指标明细",
            "",
            "| 层级 | 指标 | 风险值 | 趋势 | 频率 | 当前读数 | 危险信号 |",
            "|---|---|---:|---|---|---|---|",
        ]
    )
    for item in sorted(data["indicators"], key=lambda x: (x["layer"], -x["score"])):
        signals = "；".join(item["watch_signals"])
        lines.append(
            f"| {item['layer']} | {item['name']} | {item['score']} | {trend_label(item['trend'])} | {item['cadence']} | {item['current_read']} | {signals} |"
        )

    lines.extend(
        [
            "",
            "## 每次更新建议",
            "",
            "1. 先更新 `data/ai_risk_metrics.json` 里的 `as_of`、`score`、`trend` 和 `current_read`。",
            "2. 运行 `python .\\tools\\ai_risk_dashboard.py`。",
            "3. 打开 `output/ai_risk_dashboard.html` 查看风险值和明细。",
            "4. 若总风险进入红灯，或云capex/GPU/应用ROI同时恶化，应单独写一份风险复盘。",
        ]
    )
    return "\n".join(lines) + "\n"


def safe_write(path, text):
    tmp_path = path.with_name(path.name + ".tmp")
    try:
        tmp_path.write_text(text, encoding="utf-8")
    except PermissionError:
        FALLBACK_OUT_DIR.mkdir(parents=True, exist_ok=True)
        fallback = FALLBACK_OUT_DIR / path.name
        fallback.write_text(text, encoding="utf-8")
        print(f"warning: cannot write in {path.parent}; wrote {fallback} instead")
        return fallback
    try:
        tmp_path.replace(path)
        return path
    except PermissionError:
        fallback = path.with_name(path.name + ".new")
        tmp_path.replace(fallback)
        print(f"warning: {path} is locked; wrote {fallback} instead")
        return fallback


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data, layer_scores, overall = load_dashboard()
    html_written = safe_write(HTML_FILE, render_html(data, layer_scores, overall))
    md_written = safe_write(MD_FILE, render_markdown(data, layer_scores, overall))
    print(f"overall_risk={overall} ({risk_label(overall)})")
    print(html_written)
    print(md_written)


if __name__ == "__main__":
    main()
