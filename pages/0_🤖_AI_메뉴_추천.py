import streamlit as st
import os
from datetime import datetime
from openai import OpenAI
import json
from dotenv import load_dotenv
import sys

# 상위 디렉토리의 utils 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.history import save_history_item, get_stats
from utils.weather import get_weather_data, format_weather_info, get_weather_recommendation
from utils.delivery import get_all_delivery_links, extract_menu_name_from_recommendation

# .env 파일 로드 (로컬 환경용)
load_dotenv()

# OpenAI API 키 확인
@st.cache_resource
def get_api_key():
    """API 키 가져오기 (없으면 None 반환)"""
    api_key = None
    
    # 1. Streamlit secrets에서 시도
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except:
        pass
    
    # 2. 환경 변수에서 시도
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    return api_key

# OpenAI 클라이언트 초기화
def get_openai_client():
    """OpenAI 클라이언트 생성 (API 키 없으면 None 반환)"""
    api_key = get_api_key()
    
    if not api_key:
        return None
    
    return OpenAI(api_key=api_key)

# GPT를 사용한 메뉴 추천 함수
def get_menu_recommendation(user_data, weather_data=None):
    client = get_openai_client()
    
    if client is None:
        st.error("""
        ⚠️ **OPENAI_API_KEY가 설정되지 않았습니다.**
        
        AI 메뉴 추천 기능을 사용하려면 API Key를 설정해주세요:
        
        **Streamlit Cloud에서 설정:**
        1. App 메뉴(⋮) > Settings > Secrets
        2. 다음 내용 입력:
        ```
        OPENAI_API_KEY = "sk-your-api-key-here"
        ```
        3. Save 후 앱 재시작
        
        **로컬 환경에서 설정:**
        - 프로젝트 루트에 `.env` 파일 생성
        - `OPENAI_API_KEY=your_api_key_here` 추가
        
        API Key는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.
        """)
        return None
    
    # 날씨 정보 추가
    weather_info = ""
    if weather_data:
        weather_info = f"""
- 현재 날씨: {weather_data['description']}, 기온 {weather_data['temp']}°C (체감 {weather_data['feels_like']}°C)
- 날씨 힌트: {get_weather_recommendation(weather_data)}"""
    
    # 프롬프트 생성
    prompt = f"""
당신은 맞춤형 메뉴 추천 전문가입니다. 사용자의 현재 상황과 선호도를 분석하여 최적의 메뉴를 추천해주세요.

[사용자 정보]
- 현재 컨디션: {user_data['condition']}
- 스트레스 수준: {user_data['stress_level']}/10
- 예산: {user_data['budget']}원
- 선호 음식 종류: {user_data['food_type']}
- 동행 인원: {user_data['people_count']}명
- 식사 시간대: {user_data['meal_time']}
- 매운맛 선호도: {user_data['spicy_level']}
- 제약사항: {user_data['constraints']}
- 추가 요청사항: {user_data['additional_notes']}{weather_info}

위 정보를 바탕으로 다음 형식으로 3가지 메뉴를 추천해주세요:

1. **추천 메뉴명**
   - 추천 이유: (사용자 상황과 연관지어 설명)
   - 예상 가격: (1인 기준)
   - 추천 음식점 종류: (예: 한식당, 분식집, 일식당 등)
   - 특별 팁: (주문 시 유의사항이나 추가 추천)

2. **추천 메뉴명**
   - 추천 이유:
   - 예상 가격:
   - 추천 음식점 종류:
   - 특별 팁:

3. **추천 메뉴명**
   - 추천 이유:
   - 예상 가격:
   - 추천 음식점 종류:
   - 특별 팁:

각 추천은 사용자의 현재 컨디션, 스트레스 수준, 예산, 제약사항 등을 반영하여 구체적이고 공감되는 이유와 함께 제시해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친근하고 전문적인 메뉴 추천 AI입니다. 사용자의 상황을 공감하며 실용적인 추천을 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        st.error(f"❌ 추천 생성 중 오류가 발생했습니다: {str(e)}")
        return None

# 메인 UI
st.title("🍽️ AI 기반 맞춤형 메뉴 추천 서비스")
st.markdown("**오늘 뭐 먹지?** 고민은 이제 그만! AI가 당신의 상황에 딱 맞는 메뉴를 추천해드립니다.")

# API 키 상태 확인 및 경고 표시
if get_api_key() is None:
    st.warning("""
    ⚠️ **OpenAI API 키가 설정되지 않았습니다.** 
    AI 메뉴 추천 기능을 사용하려면 API 키를 설정해주세요.
    
    **설정 방법:** 
    - Streamlit Cloud: App Settings > Secrets에서 `OPENAI_API_KEY` 설정
    - 로컬: 프로젝트 루트에 `.env` 파일 생성 후 `OPENAI_API_KEY=your-key` 추가
    """)

# 날씨 정보 표시
weather_data = get_weather_data("Seoul")
if weather_data:
    weather_info = format_weather_info(weather_data)
    weather_hint = get_weather_recommendation(weather_data)
    
    col_weather1, col_weather2 = st.columns([1, 2])
    with col_weather1:
        st.info(f"**현재 날씨**: {weather_info}")
    with col_weather2:
        st.success(f"💡 **날씨 추천**: {weather_hint}")

st.markdown("---")

# 사이드바 - 서비스 소개 및 통계
with st.sidebar:
    st.header("📱 서비스 소개")
    st.markdown("""
    ### 주요 기능
    - 🎯 맞춤형 AI 추천
    - 🌡️ 상황 인지형 추천
    - 🚫 제약 조건 반영
    - ⚡ 빠른 결정 지원
    - 📊 히스토리 분석
    
    ### 사용 방법
    1. 현재 상태 입력
    2. 선호 조건 설정
    3. AI 추천 받기
    4. 메뉴 선택 & 주문
    """)
    
    st.markdown("---")
    
    # 간단한 통계 표시
    try:
        stats = get_stats()
        if stats['total_count'] > 0:
            st.markdown("### 📊 나의 통계")
            st.metric("총 추천 횟수", f"{stats['total_count']}회")
            if stats['favorite_food_types']:
                st.write(f"🍽️ 선호 음식: {', '.join(stats['favorite_food_types'][:2])}")
            st.markdown("*자세한 내용은 [히스토리 페이지](/히스토리)에서 확인하세요*")
            st.markdown("---")
    except:
        pass
    
    st.info("💡 **Tip**: 더 구체적인 정보를 입력할수록 정확한 추천을 받을 수 있어요!")

# 메인 콘텐츠 - 입력 폼
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 현재 상황을 알려주세요")
    
    condition = st.select_slider(
        "지금 컨디션은 어떠신가요?",
        options=["매우 안좋음", "안좋음", "보통", "좋음", "매우 좋음"],
        value="보통"
    )
    
    stress_level = st.slider(
        "오늘 스트레스 수준은? (0: 전혀 없음, 10: 매우 높음)",
        0, 10, 5
    )
    
    meal_time = st.radio(
        "언제 식사하실 건가요?",
        ["아침", "점심", "저녁", "야식/간식"],
        horizontal=True
    )
    
    people_count = st.number_input(
        "몇 명이서 드실 건가요?",
        min_value=1, max_value=20, value=1
    )
    
    budget = st.select_slider(
        "1인당 예산은?",
        options=[5000, 8000, 10000, 15000, 20000, 30000, 50000],
        value=10000,
        format_func=lambda x: f"{x:,}원"
    )

with col2:
    st.subheader("🎯 선호도 & 제약사항")
    
    food_type = st.multiselect(
        "어떤 종류의 음식을 좋아하시나요?",
        ["한식", "중식", "일식", "양식", "분식", "치킨", "피자", "햄버거", "디저트", "아무거나"],
        default=["아무거나"]
    )
    
    spicy_level = st.select_slider(
        "매운맛 선호도",
        options=["전혀 못먹음", "약간만", "보통", "매운 것 좋아함", "아주 매운 것"],
        value="보통"
    )
    
    constraints = st.multiselect(
        "제약사항이 있나요?",
        ["없음", "채식주의", "해산물 알레르기", "견과류 알레르기", "유당불내증", "글루텐 프리", "저칼로리", "고단백"]
    )
    
    additional_notes = st.text_area(
        "추가로 고려해야 할 사항이 있나요?",
        placeholder="예: 따뜻한 국물 요리가 좋아요, 빨리 먹을 수 있는 메뉴, 건강한 음식..."
    )

# 추천 받기 버튼
st.markdown("---")
col_button1, col_button2, col_button3 = st.columns([1, 1, 1])

with col_button2:
    recommend_button = st.button(
        "🎯 AI 메뉴 추천 받기",
        type="primary",
        use_container_width=True
    )

# 추천 결과 표시
if recommend_button:
    # 입력 데이터 수집
    user_data = {
        'condition': condition,
        'stress_level': stress_level,
        'budget': budget,
        'food_type': ", ".join(food_type) if food_type else "제한 없음",
        'people_count': people_count,
        'meal_time': meal_time,
        'spicy_level': spicy_level,
        'constraints': ", ".join(constraints) if constraints else "없음",
        'additional_notes': additional_notes if additional_notes else "없음"
    }
    
    with st.spinner("🤔 AI가 최적의 메뉴를 고민 중입니다..."):
        # 날씨 정보를 함께 전달
        weather_data_for_ai = get_weather_data("Seoul")
        recommendation = get_menu_recommendation(user_data, weather_data_for_ai)
    
    if recommendation:
        # 히스토리에 저장
        save_history_item(user_data, recommendation)
        
        st.success("✅ 추천이 완료되었습니다! (히스토리에 저장됨)")
        st.markdown("---")
        
        # 추천 결과 표시
        st.subheader("🎉 당신을 위한 맞춤 메뉴 추천")
        st.markdown(recommendation)

# 푸터
st.markdown("---")
st.caption("Made with ❤️ using Streamlit & OpenAI GPT | 매일의 메뉴 고민을 AI가 해결해드립니다")



