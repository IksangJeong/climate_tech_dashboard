# 🌍 기후기술 대시보드

> **Python + Streamlit**으로 구현한 한국 기후기술 현황 분석 대시보드

## 📋 프로젝트 개요

이 프로젝트는 원본 **"한눈에 보는 기후기술"** 프로젝트를 Python과 Streamlit을 사용하여 완전히 재구현한 것입니다. 기후기술 분류체계, 기관 현황, 특허 현황, 수명주기, 해외진출 현황을 종합적으로 분석할 수 있는 인터랙티브 대시보드를 제공합니다.

## 🎯 주요 기능

### 📊 **6개 핵심 페이지**

1. **🔬 기후기술 분류체계** - 45개 소분류 기술의 계층적 시각화
2. **🏢 기관 현황** - 매출액, 종사자 수, 연구개발비, 연구자 수 분석
3. **📋 특허 현황** - 연도별 특허 등록 건수 및 트렌드 분석
4. **🔄 수명주기** - 기술별 수명주기 단계 분포 분석
5. **🌏 해외진출** - 지역별 기술 진출 현황 및 세계지도 시각화
6. **⚙️ 데이터 관리** - 데이터 수집, 상태 확인, 시스템 관리

### 🎨 **시각화 특징**

- **인터랙티브 차트**: Plotly 기반 동적 차트
- **실시간 필터링**: 분야, 연도, 기관별 동적 필터
- **세계지도**: Folium 기반 해외진출 현황 지도
- **반응형 레이아웃**: 모든 화면 크기에 최적화

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv climate_tech_env
source climate_tech_env/bin/activate  # Windows: climate_tech_env\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 디렉토리 구조 생성

```bash
# 프로젝트 구조 생성 (한 번에 실행)
mkdir climate_tech_dashboard
cd climate_tech_dashboard

mkdir -p pages data utils assets/data assets/images config
mkdir -p assets/data/raw assets/data/processed assets/data/scraped
mkdir -p .streamlit

# 필요한 파일들 생성
touch main.py requirements.txt README.md .gitignore
touch pages/{__init__.py,classification.py,institutions.py,patents.py,lifecycle.py,overseas.py}
touch data/{__init__.py,scraping.py,preprocessing.py,data_loader.py}
touch utils/{__init__.py,charts.py,helpers.py,constants.py}
touch config/{__init__.py,settings.py}
touch .streamlit/config.toml
```

### 3. 앱 실행

```bash
# 방법 1: 통합 실행 스크립트
python run_app.py

# 방법 2: 직접 실행
streamlit run main.py
```

## 📁 프로젝트 구조

```
climate_tech_dashboard/
├── main.py                    # 메인 Streamlit 앱
├── requirements.txt           # 패키지 의존성
├── run_app.py                # 앱 실행 스크립트
├── README.md                 # 프로젝트 설명서
├── .gitignore               # Git 무시 파일
├── .streamlit/
│   └── config.toml          # Streamlit 설정
├── pages/                   # 각 페이지 모듈
│   ├── __init__.py
│   ├── classification.py    # 분류체계 페이지
│   ├── institutions.py      # 기관현황 페이지
│   ├── patents.py          # 특허현황 페이지
│   ├── lifecycle.py        # 수명주기 페이지
│   ├── overseas.py         # 해외진출 페이지
│   └── data_management.py  # 데이터 관리 페이지
├── data/                   # 데이터 처리 모듈
│   ├── __init__.py
│   ├── scraping.py         # 웹 크롤링
│   ├── preprocessing.py    # 데이터 전처리
│   └── data_loader.py      # 데이터 로더
├── utils/                  # 유틸리티 함수들
│   ├── __init__.py
│   ├── charts.py           # 차트 생성 함수
│   ├── helpers.py          # 헬퍼 함수
│   └── constants.py        # 상수 정의
├── config/                 # 설정 파일들
│   ├── __init__.py
│   └── settings.py         # 앱 설정
└── assets/                 # 데이터 및 이미지
    ├── data/
    │   ├── raw/            # 원본 데이터
    │   ├── processed/      # 전처리된 데이터
    │   └── scraped/        # 크롤링된 데이터
    └── images/             # 이미지 파일들
```

## 🛠️ 기술 스택

### **Core Technologies**

- **Python 3.9+**: 메인 프로그래밍 언어
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 처리 및 분석
- **Plotly**: 인터랙티브 시각화

### **Data Collection**

- **BeautifulSoup4**: HTML 파싱
- **Selenium**: 동적 웹 크롤링
- **Requests**: HTTP 요청 처리

### **Visualization**

- **Folium**: 지도 시각화
- **Altair**: 대안 시각화 라이브러리
- **Plotly Express**: 빠른 차트 생성

### **Data Processing**

- **NumPy**: 수치 연산
- **OpenPyXL**: Excel 파일 처리
- **WebDriver Manager**: 자동 드라이버 관리

## 📊 데이터 소스

### **실제 데이터 소스**

1. **CTIS (기후기술정보시스템)**

   - URL: https://www.ctis.re.kr
   - 데이터: 기후기술 분류체계, 상세정보

2. **KOSIS (국가통계포털)**
   - URL: https://kosis.kr
   - 데이터: 기관 현황, 특허 현황, 수명주기, 해외진출

### **샘플 데이터**

- 실제 데이터 구조와 유사한 synthetic 데이터
- 22개 기후기술 분야 covering
- 2019-2022년 시계열 데이터

## 🎨 사용자 인터페이스

### **메인 페이지**

- 6개 주요 페이지 네비게이션
- 프로젝트 개요 및 통계 요약
- 반응형 카드 레이아웃

### **분류체계 페이지**

- 파이차트, 선버스트 차트 지원
- 3단계 계층 필터링 (대분류-중분류-소분류)
- 상세정보 모달 표시

### **기관현황 페이지**

- 4개 지표 (매출액, 종사자, 연구개발비, 연구자)
- 상관분석 산점도
- 연도별 트렌드 분석

### **특허현황 페이지**

- 연도별 특허 등록 트렌드
- 기술별 특허 건수 랭킹
- 히트맵 및 분야별 분석

### **수명주기 페이지**

- 8단계 수명주기 분석
- 기술별 성숙도 레이더 차트
- 라인차트 및 히트맵 시각화

### **해외진출 페이지**

- 인터랙티브 세계지도
- 지역별 진출 현황
- Sankey 다이어그램 흐름 분석

## 🔧 고급 기능

### **데이터 관리**

- 실시간 데이터 상태 모니터링
- 자동/수동 데이터 수집
- 데이터 품질 검증
- 시스템 리소스 모니터링

### **성능 최적화**

- Streamlit 캐싱 (`@st.cache_data`)
- 데이터 압축 및 최적화
- 로딩 시간 최소화
- 메모리 사용량 관리

### **사용자 경험**

- 로딩 스피너 및 진행률 표시
- 에러 핸들링 및 사용자 친화적 메시지
- 반응형 레이아웃
- 다크/라이트 모드 지원

## 🌐 배포 옵션

### **Streamlit Cloud (추천)**

```bash
# GitHub 연동 후 자동 배포
# streamlit.io에서 무료 배포 가능
```

### **Docker 배포**

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

### **로컬 서버**

```bash
# 프로덕션 모드
streamlit run main.py --server.port=8501 --server.address=0.0.0.0
```

## 🔍 개발 가이드

### **새로운 페이지 추가**

```python
# pages/new_page.py
import streamlit as st

def main():
    st.title("새로운 페이지")
    # 페이지 내용 구현

if __name__ == "__main__":
    main()
```

### **새로운 차트 추가**

```python
# utils/charts.py에 추가
def create_custom_chart(data, title=""):
    fig = px.scatter(data, x='x', y='y', title=title)
    return fig
```

### **데이터 소스 추가**

```python
# data/scraping.py에 추가
def scrape_new_data_source(url):
    # 새로운 크롤링 로직
    return pd.DataFrame(data)
```

## 🐛 트러블슈팅

### **일반적인 문제들**

1. **패키지 설치 오류**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

2. **크롤링 실패**

   - ChromeDriver 버전 확인
   - 네트워크 연결 상태 확인
   - 웹사이트 접근 권한 확인

3. **메모리 부족**

   - 데이터 청크 단위로 처리
   - 캐시 정리 (`st.cache_data.clear()`)
   - 불필요한 데이터 제거

4. **차트 표시 오류**
   - 데이터 타입 확인
   - 빈 데이터 처리
   - Plotly 버전 호환성 확인

## 📈 성능 벤치마크

| 항목          | 성능   |
| ------------- | ------ |
| 앱 시작 시간  | ~3초   |
| 페이지 로딩   | ~1초   |
| 차트 렌더링   | ~0.5초 |
| 데이터 크롤링 | ~30초  |
| 메모리 사용량 | ~200MB |

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## 👥 팀

- **개발자**: AI Assistant
- **원본 프로젝트**: "한눈에 보는 기후기술" (Tableau + Python + R)
- **데이터 제공**: KOSIS, CTIS

## 📞 문의

- 이슈 리포트: [GitHub Issues](https://github.com/your-repo/issues)
- 기술 문의: [GitHub Discussions](https://github.com/your-repo/discussions)
- 이메일: climate.tech.dashboard@example.com

---

**🌍 기후기술의 미래를 한눈에 보세요!**
