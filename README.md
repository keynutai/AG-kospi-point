# 📊 AG-kospi-point (코스피 일별 마감가 수집 프로그램)

> **Antigravity와 함께 바이브코딩 첫 경험하기** 🚀

대한민국 코스피(^KS11) 지수의 일별 마감가를 수집하여 **텍스트 파일(.txt)** 및 **시각화된 HTML 파일(.html)**로 저장해 주는 Python 프로그램입니다.

🌐 **웹 페이지 링크**: [https://keynutai.github.io/AG-kospi-point/](https://keynutai.github.io/AG-kospi-point/)

---

## 🌟 주요 기능

- **이중 데이터 소스 자동 선택**: Yahoo Finance(`yfinance`)와 FinanceDataReader 두 소스에서 데이터를 수집한 뒤, **더 최신 데이터를 제공하는 소스를 자동으로 채택**하여 항상 최신 데이터를 보장
- 2026년 1월 1일부터 오늘 날짜까지의 코스피 일별 마감가 수집
- **2025년 마지막 거래일 종가 기준** 첫 거래일(2026-01-02) 전일대비 등락률 정확히 계산
- **전일 대비 등락률(%)** 표시:
  - 🔴 **상승** (`▲ +X.XX%`): 빨간색
  - 🔵 **하락** (`▼ -X.XX%`): 파란색
- **월별 구분선** 제공 (중앙 정렬 + 흰색 텍스트)
- **인터랙티브 정렬 기능**: HTML 페이지에서 버튼 클릭 한 번으로 **`⏳ 최신순`** / **`⌛ 과거순`** 날짜 정렬 전환 가능
- **밝게/어둡게 테마 토글**: `☀️ 밝게` / `🌙 어둡게` 버튼으로 즉시 테마 전환 (기본값: 밝은 테마)
- **테마 설정 자동 저장**: 선택한 테마가 `localStorage`에 저장되어 다음 방문 시에도 유지됨
- 모던한 인터랙티브 HTML 결과물 및 주요 통계 카드 (최고가, 최저가, 평균가, 최근가) 제공
- **GitHub Pages 연동**: 웹 주소를 통해 누구나 실시간 마감가 페이지 접속 가능
- **간편한 실행 환경**: macOS Finder에서 더블클릭만으로 데이터 수집이 가능한 `.command` 실행 파일 제공

---

## 📁 파일 구성 및 결과물 예시

1. `run_kospi.command`: 더블클릭하여 프로그램을 바로 실행하는 macOS 전용 실행 파일
2. `kospi_closing_prices.txt`: 깔끔하게 정렬된 콘솔용 텍스트 문서
3. `kospi_closing_prices.html` / `index.html`: 모던 웹 스타일의 인터랙티브 리포트 (GitHub Pages용)

---

## 🚀 실행 방법

### 🖱️ 방법 A: 마우스 더블클릭으로 실행 (추천)
Finder에서 `run_kospi.command` 파일을 더블클릭하면 터미널 창이 열리면서 자동으로 데이터를 최신 상태로 수집 및 갱신합니다.

---

### 💻 방법 B: 터미널에서 직접 실행

#### 1. 저장소 클론
```bash
git clone https://github.com/keynutai/AG-kospi-point.git
cd AG-kospi-point
```

#### 2. 가상환경 생성 및 패키지 설치
```bash
python3 -m venv kospi_venv
source kospi_venv/bin/activate
pip install yfinance finance-datareader pandas
```

#### 3. 스크립트 실행
```bash
python kospi_fetch.py
```
*(실행 후 해당 폴더에 `kospi_closing_prices.txt`, `kospi_closing_prices.html`, `index.html`이 자동 생성/업데이트됩니다.)*
