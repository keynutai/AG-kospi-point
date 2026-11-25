# 📊 AG-kospi-point (코스피 일별 마감가 수집 프로그램)

> **Antigravity와 함께 바이브코딩 첫 경험하기** 🚀

대한민국 코스피(^KS11) 지수의 일별 마감가를 수집하여 **SQLite 데이터베이스(`kospi.db`)**에 안전하게 보관하고, **시각화된 반응형 웹 HTML 파일(.html)**로 자동 생성해 주는 Python 프로그램입니다.

🌐 **웹 페이지 링크**: [https://keynutai.github.io/AG-kospi-point/](https://keynutai.github.io/AG-kospi-point/)

---

## 🌟 주요 기능

- **SQLite 데이터베이스(`kospi.db`) 기반 스마트 증분 업데이트**:
  - 매번 과거 전체 데이터를 반복 다운로드하지 않고, 데이터베이스에 누적 저장.
  - 기존 마지막 저장 데이터 기준 **일주일 전부터 오늘까지의 최신 데이터만 증분 수집(Upsert)**하여 처리 속도와 효율성을 극대화.
- **데이터베이스 기반 HTML 생성**:
  - 저장된 데이터베이스를 바탕으로 웹 리포트(`index.html`)를 신속하게 빌드.
- **이중 데이터 소스 자동 선택 및 보완**:
  - Yahoo Finance(`yfinance`)와 FinanceDataReader 두 소스에서 데이터를 수집하여 결측치나 새벽 시간대 임시 롤백을 상호 보완.
- **2025년 마지막 거래일 종가 기준** 첫 거래일(2026-01-02) 전일대비 등락률 정확히 계산.
- **전일 대비 등락률(%)** 표시:
  - 🔴 **상승** (`▲ +X.XX%`): 빨간색
  - 🔵 **하락** (`▼ -X.XX%`): 파란색
- **월별 구분선** 제공 (중앙 정렬 + 흰색 텍스트).
- **인터랙티브 정렬 기능**: HTML 페이지에서 버튼 클릭 한 번으로 **`⏳ 최신순`** / **`⌛ 과거순`** 날짜 정렬 전환 가능.
- **밝게/어둡게 테마 토글**: `☀️ 밝게` / `🌙 어둡게` 버튼으로 즉시 테마 전환 (기본값: 밝은 테마).
- **테마 설정 자동 저장**: 선택한 테마가 `localStorage`에 저장되어 다음 방문 시에도 유지됨.
- 모던한 인터랙티브 HTML 결과물 및 주요 통계 카드 (최고가, 최저가, 평균가, 최근가) 제공.
- **GitHub Pages 연동**: 웹 주소를 통해 누구나 실시간 마감가 페이지 접속 가능.
- **간편한 실행 환경**: macOS Finder에서 더블클릭만으로 데이터 수집이 가능한 `.command` 실행 파일 제공.

---

## 📁 파일 구성

1. `kospi.db`: 코스피 일별 마감가를 영구 저장하는 SQLite 데이터베이스 파일
2. `kospi_fetch.py`: 증분 데이터 수집 및 HTML 리포트 생성 메인 스크립트
3. `run_kospi.command`: 더블클릭하여 프로그램을 바로 실행하는 macOS 전용 실행 파일
4. `index.html`: 모던 웹 스타일의 인터랙티브 리포트 (GitHub Pages용)

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
*(실행 후 `kospi.db`에 증분 업데이트되며, `index.html`이 자동 갱신됩니다.)*
