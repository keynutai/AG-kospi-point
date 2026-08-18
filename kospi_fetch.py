"""
코스피 지수 일별 마감가 수집 프로그램
- 기간: 2026년 1월 1일 ~ 오늘
- 데이터 소스: Yahoo Finance (^KS11)
- 저장 형식: 텍스트 파일 (kospi_closing_prices.txt)
            + HTML 파일 (kospi_closing_prices.html, index.html)
"""

import yfinance as yf
from datetime import date, datetime, timedelta
import os

# ── 설정 ────────────────────────────────────────────────────
TICKER           = "^KS11"
START_DATE       = "2026-01-01"
END_DATE         = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
OUTPUT_FILE      = "kospi_closing_prices.txt"
OUTPUT_FILE_HTML = "kospi_closing_prices.html"
OUTPUT_FILE_INDEX= "index.html"                 # GitHub Pages 기본 인덱스 파일
# ────────────────────────────────────────────────────────────


def fetch_kospi_data(ticker, start, end):
    """야후 파이낸스에서 코스피 일별 데이터를 가져옵니다."""
    print(f"📡 코스피 데이터 다운로드 중... ({start} ~ {end})")
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError("데이터를 가져오지 못했습니다. 인터넷 연결 및 날짜 범위를 확인하세요.")
    return df


# ──────────────────────────────────────────────────────────────
#  텍스트 저장
# ──────────────────────────────────────────────────────────────
def save_to_file(df, output_path):
    """데이터프레임을 텍스트 파일로 저장합니다."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("  대한민국 코스피 지수 일별 마감가\n")
        f.write(f"  수집 기간 : {START_DATE} ~ {END_DATE}\n")
        f.write(f"  생성 일시 : {now_str}\n")
        f.write(f"  데이터 건수: {len(df)}건\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"{'날짜':<14}{'마감가 (KRW)':>15}{'전일대비':>12}\n")
        f.write("-" * 42 + "\n")

        current_month = None
        for idx, row in df.iterrows():
            date_str  = idx.strftime("%Y-%m-%d")
            month_key = (idx.year, idx.month)
            if month_key != current_month:
                if current_month is not None:
                    f.write("\n")
                label = f"  {idx.year}년 {idx.month:02d}월  "
                f.write(f"{'─' * 14}{label}{'─' * (28 - len(label))}\n")
                current_month = month_key
            close_val = float(row["Close"])
            pct       = row["Pct_Change"]
            pct_str   = "-" if pct != pct else f"{pct:+.2f}%"
            f.write(f"{date_str:<14}{close_val:>15,.2f}{pct_str:>12}\n")

    print(f"✅ 저장 완료: {output_path}  ({len(df)}건)")


# ──────────────────────────────────────────────────────────────
#  HTML 저장
# ──────────────────────────────────────────────────────────────
def save_to_html(df, output_path, last_2025_date, last_2025):
    """데이터프레임을 스타일링된 HTML 파일로 저장합니다."""
    now_str      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    close_series = df["Close"]

    # ── 월별 테이블 행 생성 (과거순 asc / 최신순 desc 준비) ──
    MONTH_KO = ["", "1월", "2월", "3월", "4월", "5월", "6월",
                "7월", "8월", "9월", "10월", "11월", "12월"]

    def build_rows(data_df):
        rows = []
        current_month = None
        for idx, row in data_df.iterrows():
            month_key = (idx.year, idx.month)
            if month_key != current_month:
                label = f"{idx.year}년 {MONTH_KO[idx.month]}"
                rows.append(
                    f'<tr class="month-sep"><td colspan="3">📅 {label}</td></tr>'
                )
                current_month = month_key

            date_str  = idx.strftime("%Y-%m-%d")
            close_val = float(row["Close"])
            pct       = row["Pct_Change"]

            if pct != pct:
                pct_cell = '<span class="flat">—</span>'
            elif pct > 0:
                pct_cell = f'<span class="up">▲ {pct:+.2f}%</span>'
            elif pct < 0:
                pct_cell = f'<span class="down">▼ {pct:+.2f}%</span>'
            else:
                pct_cell = '<span class="flat">0.00%</span>'

            rows.append(
                f'<tr>'
                f'<td class="date">{date_str}</td>'
                f'<td class="close">{close_val:,.2f}</td>'
                f'<td class="pct">{pct_cell}</td>'
                f'</tr>'
            )
        return "\n        ".join(rows)

    rows_asc_html  = build_rows(df)
    rows_desc_html = build_rows(df.iloc[::-1])

    # ── 통계 값 미리 계산 ──
    val_high   = f"{close_series.max():,.0f}"
    val_low    = f"{close_series.min():,.0f}"
    val_avg    = f"{close_series.mean():,.0f}"
    val_recent = f"{close_series.iloc[-1]:,.0f}"
    val_last   = f"{last_2025:,.2f}"

    # ── HTML 생성 ──
    html = """\
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>코스피 지수 일별 마감가 (2026)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* ── CSS 변수: 다크 테마 (기본) ── */
    :root {
      --bg:           #0d1117;
      --bg-card:      #161b22;
      --bg-card2:     #1c2333;
      --border:       #30363d;
      --border-sep:   #30363d;
      --text:         #e6edf3;
      --text-muted:   #8b949e;
      --text-footer:  #484f58;
      --text-strong:  #e6edf3;
      --month-sep-bg: #1c2333;
      --month-sep-fg: #ffffff;
      --row-hover:    #1c2333;
      --thead-bg:     #1c2333;
      --btn-bg:       #161b22;
      --btn-fg:       #8b949e;
      --btn-hover-fg: #e6edf3;
      --h1-color:     #58a6ff;
      --close-fg:     #e6edf3;
      --date-fg:      #8b949e;
      --title-fg:     #8b949e;
      --transition:   background 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }

    /* ── CSS 변수: 라이트 테마 ── */
    body.light {
      --bg:           #f6f8fa;
      --bg-card:      #ffffff;
      --bg-card2:     #eaf0f6;
      --border:       #d0d7de;
      --border-sep:   #d0d7de;
      --text:         #1f2328;
      --text-muted:   #656d76;
      --text-footer:  #aaaaaa;
      --text-strong:  #1f2328;
      --month-sep-bg: #eaf0f6;
      --month-sep-fg: #1f2328;
      --row-hover:    #eaf0f6;
      --thead-bg:     #f0f4f8;
      --btn-bg:       #f0f4f8;
      --btn-fg:       #656d76;
      --btn-hover-fg: #1f2328;
      --h1-color:     #0969da;
      --close-fg:     #1f2328;
      --date-fg:      #656d76;
      --title-fg:     #656d76;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1rem;
      transition: var(--transition);
    }
    .container { max-width: 780px; margin: 0 auto; }
    .header-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2rem 2.5rem;
      margin-bottom: 1.2rem;
      position: relative;
      overflow: hidden;
      transition: var(--transition);
    }
    .header-card::after {
      content: '';
      position: absolute;
      top: -80px; right: -80px;
      width: 220px; height: 220px;
      background: radial-gradient(circle, rgba(88,166,255,0.10) 0%, transparent 70%);
      pointer-events: none;
    }
    .header-card h1 {
      font-size: 1.55rem;
      font-weight: 700;
      color: var(--h1-color);
      letter-spacing: -0.02em;
      margin-bottom: 1rem;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 0.5rem 2rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
    .meta-grid div { white-space: nowrap; }
    .meta-grid strong { color: var(--text-strong); font-weight: 500; }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
      margin-bottom: 1.2rem;
    }
    .stat-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 0.8rem;
      text-align: center;
      transition: var(--transition), border-color 0.2s;
    }
    .stat-card:hover { border-color: var(--h1-color); }
    .stat-label {
      font-size: 0.68rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 0.4rem;
    }
    .stat-value {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.05rem;
      font-weight: 600;
    }
    .stat-card.high .stat-value { color: #f85149; }
    .stat-card.low  .stat-value { color: #58a6ff; }
    .stat-card.avg  .stat-value { color: var(--text); }
    .stat-card.last .stat-value { color: var(--text); }

    /* ── 컨트롤 바 (정렬 + 테마) ── */
    .controls-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.8rem;
      padding: 0 0.4rem;
      gap: 0.6rem;
    }
    .controls-title {
      font-size: 0.85rem;
      color: var(--title-fg);
      font-weight: 500;
      flex: 1;
    }
    .controls-right {
      display: flex;
      gap: 0.5rem;
    }
    .btn-group {
      display: flex;
      gap: 0.4rem;
      background: var(--btn-bg);
      padding: 4px;
      border: 1px solid var(--border);
      border-radius: 10px;
      transition: var(--transition);
    }
    .ctrl-btn {
      background: transparent;
      border: none;
      color: var(--btn-fg);
      font-family: 'Inter', sans-serif;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.4rem 0.85rem;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .ctrl-btn:hover { color: var(--btn-hover-fg); }
    .ctrl-btn.active {
      background: #238636;
      color: #ffffff;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .theme-btn.active {
      background: #6e40c9;
    }

    .table-wrapper {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      transition: var(--transition);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
    }
    thead th {
      background: var(--thead-bg);
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      padding: 0.9rem 1.4rem;
      text-align: right;
      transition: var(--transition);
    }
    thead th:first-child { text-align: left; }
    tbody tr {
      border-top: 1px solid var(--border);
      transition: background 0.12s;
    }
    tbody tr:hover:not(.month-sep) { background: var(--row-hover); }
    tr.month-sep td {
      background: var(--month-sep-bg);
      color: var(--month-sep-fg);
      text-align: center;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      padding: 0.6rem 1.4rem;
      border-top: 2px solid var(--border-sep);
      transition: var(--transition);
    }
    td {
      padding: 0.6rem 1.4rem;
      font-family: 'JetBrains Mono', monospace;
      text-align: right;
    }
    td.date  { text-align: left; color: var(--date-fg); font-size: 0.82rem; }
    td.close { color: var(--close-fg); }
    td.pct   { min-width: 110px; }
    .up   { color: #f85149; font-weight: 600; }
    .down { color: #4a9eff; font-weight: 600; }
    .flat { color: var(--text-muted); }
    .footer {
      text-align: center;
      margin-top: 1.2rem;
      font-size: 0.73rem;
      color: var(--text-footer);
    }
    @media (max-width: 580px) {
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .header-card { padding: 1.3rem 1.5rem; }
      thead th, td { padding-left: 0.8rem; padding-right: 0.8rem; }
      .controls-bar { flex-wrap: wrap; }
    }
  </style>
</head>
<body>
<div class="container">

  <div class="header-card">
    <h1>📊 코스피 지수 일별 마감가</h1>
    <div class="meta-grid">
      <div>수집 기간 &nbsp;<strong>%%START_DATE%% ~ %%END_DATE%%</strong></div>
      <div>데이터 건수 &nbsp;<strong>%%TOTAL%%건</strong></div>
      <div>전일 기준일 &nbsp;<strong>%%LAST_DATE%% (%%LAST_VAL%% pt)</strong></div>
      <div>생성 일시 &nbsp;<strong>%%NOW%%</strong></div>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card high">
      <div class="stat-label">최고가</div>
      <div class="stat-value">%%HIGH%%</div>
    </div>
    <div class="stat-card low">
      <div class="stat-label">최저가</div>
      <div class="stat-value">%%LOW%%</div>
    </div>
    <div class="stat-card avg">
      <div class="stat-label">평 균</div>
      <div class="stat-value">%%AVG%%</div>
    </div>
    <div class="stat-card last">
      <div class="stat-label">최근가</div>
      <div class="stat-value">%%RECENT%%</div>
    </div>
  </div>

  <div class="controls-bar">
    <div class="controls-title">📈 일별 거래 내역</div>
    <div class="controls-right">
      <div class="btn-group">
        <button id="btnDesc" class="ctrl-btn active" onclick="setSortOrder('desc')">⏳ 최신순</button>
        <button id="btnAsc"  class="ctrl-btn"        onclick="setSortOrder('asc')">⌛ 과거순</button>
      </div>
      <div class="btn-group">
        <button id="btnDark"  class="ctrl-btn theme-btn active" onclick="setTheme('dark')">🌙 어둡게</button>
        <button id="btnLight" class="ctrl-btn theme-btn"        onclick="setTheme('light')">☀️ 밝게</button>
      </div>
    </div>
  </div>

  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th>날짜</th>
          <th>마감가 (pt)</th>
          <th>전일대비</th>
        </tr>
      </thead>
      <tbody id="tableBody">
        %%ROWS_DESC%%
      </tbody>
    </table>
  </div>

  <div class="footer">
    데이터 출처: Yahoo Finance (^KS11) &nbsp;·&nbsp; 자동 생성됨
  </div>

</div>

<script>
  const rowsAsc  = `%%ROWS_ASC%%`;
  const rowsDesc = `%%ROWS_DESC%%`;

  function setSortOrder(order) {
    const tableBody = document.getElementById('tableBody');
    const btnAsc  = document.getElementById('btnAsc');
    const btnDesc = document.getElementById('btnDesc');
    if (order === 'desc') {
      tableBody.innerHTML = rowsDesc;
      btnDesc.classList.add('active');
      btnAsc.classList.remove('active');
    } else {
      tableBody.innerHTML = rowsAsc;
      btnAsc.classList.add('active');
      btnDesc.classList.remove('active');
    }
  }

  function setTheme(theme) {
    const body      = document.body;
    const btnDark   = document.getElementById('btnDark');
    const btnLight  = document.getElementById('btnLight');
    if (theme === 'light') {
      body.classList.add('light');
      btnLight.classList.add('active');
      btnDark.classList.remove('active');
    } else {
      body.classList.remove('light');
      btnDark.classList.add('active');
      btnLight.classList.remove('active');
    }
  }
</script>

</body>
</html>
"""

    # 플레이스홀더를 실제 값으로 치환
    html = (
        html
        .replace("%%START_DATE%%", START_DATE)
        .replace("%%END_DATE%%",   END_DATE)
        .replace("%%TOTAL%%",      str(len(df)))
        .replace("%%NOW%%",        now_str)
        .replace("%%LAST_DATE%%",  last_2025_date)
        .replace("%%LAST_VAL%%",   val_last)
        .replace("%%HIGH%%",       val_high)
        .replace("%%LOW%%",        val_low)
        .replace("%%AVG%%",        val_avg)
        .replace("%%RECENT%%",     val_recent)
        .replace("%%ROWS_ASC%%",   rows_asc_html)
        .replace("%%ROWS_DESC%%",  rows_desc_html)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML 저장 완료: {output_path}  ({len(df)}건)")


# ──────────────────────────────────────────────────────────────
#  메인
# ──────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  코스피 마감가 수집 프로그램")
    print("=" * 50)

    import pandas as pd

    # 2025년 마지막 거래일 마감가 조회 (첫날 전일대비 계산용)
    print("📡 2025년 마지막 거래일 데이터 조회 중...")
    df_prev  = fetch_kospi_data(TICKER, "2025-12-01", "2025-12-31")
    prev_col = df_prev["Close"]
    if isinstance(prev_col, pd.DataFrame):
        prev_col = prev_col.iloc[:, 0]
    last_2025      = float(prev_col.iloc[-1])
    last_2025_date = prev_col.index[-1].strftime("%Y-%m-%d")
    print(f"   └ 2025년 마지막 거래일: {last_2025_date}  종가: {last_2025:,.2f} pt")

    # 본 데이터 수집 (2026-01-01 ~ 오늘)
    df = fetch_kospi_data(TICKER, START_DATE, END_DATE)

    close_col = df["Close"]
    if isinstance(close_col, pd.DataFrame):
        close_col = close_col.iloc[:, 0]
    df = close_col.to_frame(name="Close")

    # 2025년 마지막 거래일을 임시로 앞에 붙여 첫 행 전일대비 계산
    prev_row = pd.DataFrame(
        {"Close": [last_2025]},
        index=pd.DatetimeIndex([last_2025_date])
    )
    df = pd.concat([prev_row, df])
    df["Pct_Change"] = df["Close"].pct_change() * 100
    df = df.iloc[1:]  # 임시 행 제거

    base = os.path.dirname(os.path.abspath(__file__))

    # 텍스트 저장
    save_to_file(df, os.path.join(base, OUTPUT_FILE))

    # HTML 저장
    save_to_html(df, os.path.join(base, OUTPUT_FILE_HTML), last_2025_date, last_2025)
    save_to_html(df, os.path.join(base, OUTPUT_FILE_INDEX), last_2025_date, last_2025)

    # 통계 출력
    close_series = df["Close"]
    print(f"\n📊 기간 내 통계")
    print(f"   최고가 : {close_series.max():,.2f} pt")
    print(f"   최저가 : {close_series.min():,.2f} pt")
    print(f"   평  균 : {close_series.mean():,.2f} pt")
    print(f"   최근가 : {close_series.iloc[-1]:,.2f} pt  ({df.index[-1].strftime('%Y-%m-%d')})")


if __name__ == "__main__":
    main()
