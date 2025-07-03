import streamlit as st

# ✅ 반드시 가장 먼저 실행되어야 함
st.set_page_config(
    page_title="한눈에 보는 기후기술 🌍",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from pathlib import Path

# ✅ 파일 경로 설정
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "assets" / "data" / "processed"

institution_file = DATA_DIR / "institution_data.csv"
patent_file = DATA_DIR / "patent_data.csv"

# ✅ 파일 존재 확인
if not institution_file.exists():
    st.error(f"❌ 기관 데이터 파일이 없습니다: {institution_file}")
    st.stop()

if not patent_file.exists():
    st.error(f"❌ 특허 데이터 파일이 없습니다: {patent_file}")
    st.stop()

# ✅ 데이터 불러오기
try:
    institution_data = pd.read_csv(institution_file)
    patent_data = pd.read_csv(patent_file)
except Exception as e:
    st.error("❌ 데이터 불러오는 중 오류 발생")
    st.exception(e)
    st.stop()

# ✅ 메인 UI 출력
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f4e79;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin: 1rem 0;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌍 한눈에 보는 기후기술</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h3>📊 프로젝트 개요</h3>
    <p>이 대시보드는 한국의 기후기술 현황을 한눈에 파악할 수 있도록 구성된 종합 분석 도구입니다.</p>
    <p><strong>주요 기능:</strong></p>
    <ul>
        <li>🔬 기후기술 분류체계 및 상세정보</li>
        <li>🏢 기관별 매출액, 종사자 수, 연구개발비 현황</li>
        <li>📋 연도별 특허 등록 현황</li>
        <li>🔄 기술 수명주기 단계별 분석</li>
        <li>🌏 해외 진출 현황 및 지역별 분포</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ✅ 메뉴 버튼
st.markdown('<h2 class="sub-header">📋 메뉴</h2>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔬 기후기술 분류체계"):
        st.switch_page("pages/classification.py")
    if st.button("📋 특허 현황"):
        st.switch_page("pages/patents.py")

with col2:
    if st.button("🏢 기관 현황"):
        st.switch_page("pages/institutions.py")
    if st.button("🔄 수명주기"):
        st.switch_page("pages/lifecycle.py")

with col3:
    if st.button("🌏 해외 진출"):
        st.switch_page("pages/overseas.py")
    if st.button("⚙️ 데이터 관리"):
        st.switch_page("pages/data_management.py")

# ✅ 데이터 요약 카드
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <h4>📊 데이터 현황</h4>
        <p>• 기관 수: {len(institution_data)}개</p>
        <p>• 특허 수: {len(patent_data)}건</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h4>🔄 업데이트 정보</h4>
        <p>• 마지막 업데이트: 2024년</p>
        <p>• 데이터 소스: KOSIS, CTIS</p>
        <p>• 업데이트 주기: 연 1회</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h4>📞 문의사항</h4>
        <p>• 기술지원: Python + Streamlit</p>
        <p>• 데이터 문의: KOSIS 통계청</p>
        <p>• 버전: v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

# ✅ 사이드바
with st.sidebar:
    st.markdown("### 🌍 기후기술 대시보드")
    st.markdown("---")
    st.markdown("#### 📈 빠른 통계")
    st.metric("기관 수", f"{len(institution_data)}개")
    st.metric("특허 수", f"{len(patent_data)}건")
    st.markdown("---")
    st.markdown("#### 🔗 참고 링크")
    st.markdown("- [KOSIS 통계청](https://kosis.kr)")
    st.markdown("- [CTIS 기후기술정보시스템](https://www.ctis.re.kr)")
    st.markdown("- [Streamlit 문서](https://docs.streamlit.io)")
