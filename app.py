import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="AI 메뉴 추천 서비스",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 UI
st.title("🍽️ AI 메뉴 추천 서비스")
st.markdown("### 오늘 뭐 먹지? 고민은 이제 그만!")

st.markdown("---")

# 환영 메시지
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("""
    ## 👋 환영합니다!
    
    AI가 당신의 상황에 딱 맞는 메뉴를 추천해드립니다.
    
    ### 🎯 주요 기능
    
    - **🤖 AI 메뉴 추천**: 맞춤형 메뉴 추천
    - **📊 히스토리**: 추천 기록 분석
    - **🗳️ 그룹 투표**: 친구들과 메뉴 투표
    - **🗺️ 주변 음식점**: 실시간 음식점 검색
    
    ### 🚀 시작하기
    
    좌측 사이드바에서 원하는 기능을 선택해주세요!
    """)
    
    st.info("💡 **Tip**: '🤖 AI 메뉴 추천' 페이지에서 시작해보세요!")

st.markdown("---")

# 푸터
st.caption("Made with ❤️ using Streamlit & OpenAI GPT | 매일의 메뉴 고민을 AI가 해결해드립니다")

