# 📊 AG-kospi-point (코스피 일별 마감가 수집 프로그램)

> **Antigravity와 함께 바이브코딩 첫 경험하기** 🚀

대한민국 코스피(^KS11) 지수의 일별 마감가를 수집하여 **텍스트 파일(.txt)** 및 **시각화된 HTML 파일(.html)**로 저장해 주는 Python 프로그램입니다.

---

## 🌟 주요 기능

- **Yahoo Finance (`yfinance`)** 기반의 실시간/과거 데이터 자동 수집
- 2026년 1월 1일부터 오늘 날짜까지의 코스피 일별 마감가 수집
- **2025년 마지막 거래일 종가 기준** 첫 거래일(2026-01-02) 전일대비 등락률 정확히 계산
- **전일 대비 등락률(%)** 표시:
  - 🔴 **상승** (`▲ +X.XX%`): 빨간색
  - 🔵 **하락** (`▼ -X.XX%`): 파란색
- **월별 구분선** 제공 (중앙 정렬 + 깔끔한 파분 라인)
- 모던한 **다크 모드 HTML 결과물** 및 주요 통계 카드 (최고가, 최저가, 평균가, 최근가) 제공

---

## 📁 결과물 예시

1. **텍스트 파일 (`kospi_closing_prices.txt`)**: 깔끔하게 정렬된 콘솔용 텍스트 문서
2. **HTML 파일 (`kospi_closing_prices.html`)**: 모던 웹 스타일의 인터랙티브 리포트

---

## 🚀 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/keynutai/AG-kospi-point.git
cd AG-kospi-point
```

### 2. 가상환경 생성 및 패키지 설치
```bash
python3 -m venv kospi_venv
source kospi_venv/bin/activate
pip install yfinance
```

### 3. 스크립트 실행
```bash
python kospi_fetch.py
```
*(실행 후 해당 폴더에 `kospi_closing_prices.txt`와 `kospi_closing_prices.html`이 자동 생성/업데이트됩니다.)*
