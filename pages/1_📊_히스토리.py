"""
히스토리 페이지 - 과거 선택 기록 및 분석
"""
import streamlit as st
import sys
import os

# 상위 디렉토리의 utils 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.history import get_recent_history, get_stats, clear_history

st.title("📊 추천 히스토리")
st.markdown("과거에 받았던 메뉴 추천 기록과 통계를 확인할 수 있습니다.")
st.markdown("---")

# 통계 정보
stats = get_stats()

if stats['total_count'] == 0:
    st.info("📭 아직 추천 받은 기록이 없습니다. 메인 페이지에서 메뉴를 추천받아보세요!")
else:
    # 통계 카드
    st.subheader("📈 나의 선택 통계")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 추천 횟수",
            value=f"{stats['total_count']}회"
        )
    
    with col2:
        st.metric(
            label="평균 예산",
            value=f"{stats['avg_budget']:,}원"
        )
    
    with col3:
        favorite_foods = ", ".join(stats['favorite_food_types'][:2]) if stats['favorite_food_types'] else "없음"
        st.metric(
            label="선호 음식",
            value=favorite_foods
        )
    
    with col4:
        st.metric(
            label="주요 식사 시간",
            value=stats['most_common_time']
        )
    
    st.markdown("---")
    
    # 최근 히스토리
    st.subheader("📜 최근 추천 기록")
    
    # 필터 옵션
    col_filter1, col_filter2 = st.columns([3, 1])
    
    with col_filter1:
        limit = st.slider("표시할 기록 수", 5, 50, 10)
    
    with col_filter2:
        if st.button("🗑️ 히스토리 전체 삭제", type="secondary"):
            if st.session_state.get('confirm_delete', False):
                clear_history()
                st.success("✅ 히스토리가 삭제되었습니다.")
                st.rerun()
            else:
                st.session_state['confirm_delete'] = True
                st.warning("⚠️ 한 번 더 클릭하면 모든 히스토리가 삭제됩니다.")
    
    history = get_recent_history(limit)
    
    # 히스토리 표시
    for idx, item in enumerate(history):
        timestamp = item.get('timestamp', '알 수 없음')
        user_data = item.get('user_data', {})
        recommendation = item.get('recommendation', '')
        
        with st.expander(f"🕐 {timestamp} - {user_data.get('meal_time', '식사')} / {user_data.get('budget', 0):,}원"):
            # 사용자 입력 정보
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("**📝 입력 정보**")
                st.write(f"- 컨디션: {user_data.get('condition', '보통')}")
                st.write(f"- 스트레스: {user_data.get('stress_level', 5)}/10")
                st.write(f"- 인원: {user_data.get('people_count', 1)}명")
                st.write(f"- 음식 종류: {user_data.get('food_type', '제한 없음')}")
            
            with col_info2:
                st.markdown("**🎯 선호도**")
                st.write(f"- 매운맛: {user_data.get('spicy_level', '보통')}")
                st.write(f"- 제약사항: {user_data.get('constraints', '없음')}")
                if user_data.get('additional_notes'):
                    st.write(f"- 추가 요청: {user_data.get('additional_notes')}")
            
            # AI 추천 결과
            st.markdown("---")
            st.markdown("**🤖 AI 추천 결과**")
            st.markdown(recommendation)

# 푸터
st.markdown("---")
st.caption("💡 Tip: 히스토리를 분석하여 더 정확한 추천을 제공할 수 있습니다.")



