"""
그룹 투표 페이지 - 친구들과 메뉴 투표
"""
import streamlit as st
import sys
import os
import json
from datetime import datetime
import hashlib

# 상위 디렉토리의 utils 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="그룹 투표 - AI 메뉴 추천",
    page_icon="🗳️",
    layout="wide"
)

# 세션 스토리지 (간단한 JSON 파일 기반)
VOTE_DIR = "data/votes"

def ensure_vote_dir():
    """투표 디렉토리 생성"""
    os.makedirs(VOTE_DIR, exist_ok=True)

def create_vote_session(menus: list, creator_name: str) -> str:
    """투표 세션 생성"""
    ensure_vote_dir()
    
    # 고유 ID 생성
    session_id = hashlib.md5(f"{datetime.now().isoformat()}{creator_name}".encode()).hexdigest()[:8]
    
    vote_data = {
        'session_id': session_id,
        'creator': creator_name,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'menus': menus,
        'votes': {menu: [] for menu in menus},
        'status': 'active'
    }
    
    with open(f"{VOTE_DIR}/{session_id}.json", 'w', encoding='utf-8') as f:
        json.dump(vote_data, f, ensure_ascii=False, indent=2)
    
    return session_id

def load_vote_session(session_id: str):
    """투표 세션 로드"""
    try:
        with open(f"{VOTE_DIR}/{session_id}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def save_vote(session_id: str, menu: str, voter_name: str):
    """투표 저장"""
    vote_data = load_vote_session(session_id)
    if not vote_data:
        return False
    
    # 이미 투표했는지 확인
    for m in vote_data['votes']:
        if voter_name in vote_data['votes'][m]:
            vote_data['votes'][m].remove(voter_name)
    
    # 새 투표 추가
    vote_data['votes'][menu].append(voter_name)
    
    with open(f"{VOTE_DIR}/{session_id}.json", 'w', encoding='utf-8') as f:
        json.dump(vote_data, f, ensure_ascii=False, indent=2)
    
    return True

def close_vote_session(session_id: str):
    """투표 종료"""
    vote_data = load_vote_session(session_id)
    if not vote_data:
        return False
    
    vote_data['status'] = 'closed'
    
    with open(f"{VOTE_DIR}/{session_id}.json", 'w', encoding='utf-8') as f:
        json.dump(vote_data, f, ensure_ascii=False, indent=2)
    
    return True

def get_all_active_votes():
    """진행 중인 모든 투표 가져오기"""
    ensure_vote_dir()
    
    active_votes = []
    
    if not os.path.exists(VOTE_DIR):
        return active_votes
    
    try:
        for filename in os.listdir(VOTE_DIR):
            if filename.endswith('.json'):
                session_id = filename.replace('.json', '')
                vote_data = load_vote_session(session_id)
                
                if vote_data and vote_data.get('status') == 'active':
                    # 총 투표 수 계산
                    total_votes = sum(len(voters) for voters in vote_data.get('votes', {}).values())
                    active_votes.append({
                        'session_id': session_id,
                        'vote_data': vote_data,
                        'total_votes': total_votes
                    })
        
        # 생성일 기준 최신순 정렬
        active_votes.sort(key=lambda x: x['vote_data'].get('created_at', ''), reverse=True)
    except Exception as e:
        print(f"투표 목록 가져오기 오류: {e}")
    
    return active_votes

# UI
st.title("🗳️ 그룹 메뉴 투표")
st.markdown("친구들과 함께 메뉴를 정하세요! 투표를 만들고 링크를 공유하면 됩니다.")
st.markdown("---")

# URL 파라미터에서 세션 ID 가져오기
query_params = st.query_params
session_id = query_params.get('session', None)

if session_id:
    # 투표 참여 모드
    vote_data = load_vote_session(session_id)
    
    if not vote_data:
        st.error("❌ 존재하지 않는 투표 세션입니다.")
    elif vote_data['status'] == 'closed':
        st.warning("⚠️ 이미 종료된 투표입니다.")
        
        # 최종 결과 표시
        st.subheader("📊 최종 결과")
        
        votes = vote_data['votes']
        sorted_menus = sorted(votes.items(), key=lambda x: len(x[1]), reverse=True)
        
        if sorted_menus:
            winner = sorted_menus[0]
            st.success(f"🎉 **최종 선택**: {winner[0]} ({len(winner[1])}표)")
        
        for menu, voters in sorted_menus:
            with st.expander(f"{menu} - {len(voters)}표"):
                if voters:
                    st.write(", ".join(voters))
                else:
                    st.write("투표 없음")
    
    else:
        st.success(f"✅ 투표 세션: **{vote_data['creator']}**님이 만든 투표")
        st.info(f"📅 생성일: {vote_data['created_at']}")
        
        st.markdown("---")
        st.subheader("🍽️ 메뉴 선택")
        
        # 투표자 이름 입력
        voter_name = st.text_input("당신의 이름을 입력하세요", key="voter_name")
        
        if voter_name:
            # 현재 투표 상황
            st.markdown("### 📊 현재 투표 현황")
            
            votes = vote_data['votes']
            sorted_menus = sorted(votes.items(), key=lambda x: len(x[1]), reverse=True)
            
            for menu, voters in sorted_menus:
                vote_count = len(voters)
                voted_by_me = voter_name in voters
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{menu}** - {vote_count}표")
                    if voters:
                        st.caption(f"투표자: {', '.join(voters)}")
                
                with col2:
                    button_label = "✅ 선택됨" if voted_by_me else "투표하기"
                    button_type = "primary" if not voted_by_me else "secondary"
                    
                    if st.button(button_label, key=f"vote_{menu}", type=button_type, disabled=voted_by_me):
                        if save_vote(session_id, menu, voter_name):
                            st.success(f"✅ '{menu}'에 투표했습니다!")
                            st.rerun()
            
            st.markdown("---")
            
            # 투표 종료 버튼 (생성자만 가능)
            if st.session_state.get('is_creator', False):
                if st.button("🔒 투표 종료", type="secondary"):
                    if close_vote_session(session_id):
                        st.success("✅ 투표가 종료되었습니다!")
                        st.rerun()
        
        else:
            st.warning("⚠️ 이름을 입력하면 투표할 수 있습니다.")

else:
    # 투표 생성 모드
    st.subheader("📝 새 투표 만들기")
    
    with st.form("create_vote"):
        creator_name = st.text_input("당신의 이름", placeholder="예: 홍길동")
        
        st.markdown("**투표할 메뉴 목록 (최대 5개)**")
        
        menus = []
        for i in range(5):
            menu = st.text_input(f"메뉴 {i+1}", key=f"menu_{i}", placeholder="예: 짜장면, 짬뽕, 탕수육...")
            if menu:
                menus.append(menu)
        
        submitted = st.form_submit_button("🎯 투표 생성", type="primary")
        
        if submitted:
            if not creator_name:
                st.error("❌ 이름을 입력해주세요.")
            elif len(menus) < 2:
                st.error("❌ 최소 2개의 메뉴를 입력해주세요.")
            else:
                new_session_id = create_vote_session(menus, creator_name)
                
                # 생성자 플래그 설정
                st.session_state['is_creator'] = True
                st.session_state['creator_name'] = creator_name
                st.session_state['new_vote_created'] = new_session_id
                
                st.success("✅ 투표가 생성되었습니다!")
                st.rerun()
    
    # Form 밖에서 생성된 투표 링크 표시
    if 'new_vote_created' in st.session_state:
        new_session_id = st.session_state['new_vote_created']
        
        # 공유 링크 생성
        base_url = "http://localhost:8501/그룹투표"  # 배포 시 실제 URL로 변경
        share_link = f"{base_url}?session={new_session_id}"
        
        st.markdown("---")
        st.subheader("📤 친구들에게 공유하세요")
        
        st.code(share_link, language=None)
        
        st.info("💡 위 링크를 복사해서 친구들에게 공유하세요!")
        
        # Form 밖이므로 일반 버튼 사용 가능
        if st.button("🗳️ 투표 페이지로 이동", type="primary"):
            # session_state 정리
            del st.session_state['new_vote_created']
            st.query_params['session'] = new_session_id
            st.rerun()
    
    st.markdown("---")
    st.info("""
    ### 💡 사용 방법
    1. 당신의 이름을 입력하고 투표할 메뉴 목록을 작성하세요
    2. '투표 생성' 버튼을 클릭하면 고유 링크가 생성됩니다
    3. 생성된 링크를 친구들에게 공유하세요
    4. 친구들이 투표하면 실시간으로 결과가 업데이트됩니다
    5. 투표가 끝나면 '투표 종료' 버튼을 눌러 결과를 확정하세요
    """)

# 진행 중인 투표 목록 표시
st.markdown("---")
st.subheader("📋 진행 중인 투표 목록")

active_votes = get_all_active_votes()

if not active_votes:
    st.info("📭 현재 진행 중인 투표가 없습니다. 위에서 새 투표를 만들어보세요!")
else:
    st.write(f"**총 {len(active_votes)}개의 진행 중인 투표**")
    st.markdown("")
    
    # 각 투표를 카드 형태로 표시
    for idx, vote_info in enumerate(active_votes):
        vote_data = vote_info['vote_data']
        session_id = vote_info['session_id']
        total_votes = vote_info['total_votes']
        
        with st.container():
            # 투표 정보 카드
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"#### 🗳️ {vote_data.get('creator', '알 수 없음')}님의 투표")
                st.caption(f"📅 생성일: {vote_data.get('created_at', '알 수 없음')}")
                
                # 메뉴 목록 표시
                menus = vote_data.get('menus', [])
                menu_tags = " | ".join([f"**{menu}**" for menu in menus])
                st.markdown(f"🍽️ 메뉴: {menu_tags}")
            
            with col2:
                st.metric("총 투표", f"{total_votes}표")
            
            with col3:
                # 투표 현황 요약
                votes = vote_data.get('votes', {})
                if votes:
                    # 최다 득표 메뉴 찾기
                    max_votes = max(len(voters) for voters in votes.values())
                    if max_votes > 0:
                        leading_menus = [menu for menu, voters in votes.items() if len(voters) == max_votes]
                        st.markdown(f"**🥇 1위**: {leading_menus[0] if leading_menus else '없음'}")
                        st.caption(f"({max_votes}표)")
                    else:
                        st.caption("아직 투표 없음")
            
            # 투표 현황 상세
            with st.expander(f"📊 투표 현황 보기 (ID: {session_id})", expanded=False):
                votes = vote_data.get('votes', {})
                sorted_menus = sorted(votes.items(), key=lambda x: len(x[1]), reverse=True)
                
                for menu, voters in sorted_menus:
                    vote_count = len(voters)
                    vote_percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
                    
                    st.markdown(f"**{menu}** - {vote_count}표 ({vote_percentage:.0f}%)")
                    if voters:
                        st.caption(f"투표자: {', '.join(voters)}")
                    else:
                        st.caption("투표 없음")
                    st.progress(vote_percentage / 100 if total_votes > 0 else 0)
            
            # 액션 버튼
            action_col1, action_col2 = st.columns([1, 2])
            
            with action_col1:
                if st.button("🔗 투표 참여하기", key=f"join_{session_id}", use_container_width=True, type="primary"):
                    st.query_params['session'] = session_id
                    st.rerun()
            
            with action_col2:
                # 링크 복사
                base_url = "http://localhost:8501/그룹투표"
                share_link = f"{base_url}?session={session_id}"
                st.markdown("**공유 링크:**")
                st.code(share_link, language=None)
            
            # 구분선
            if idx < len(active_votes) - 1:
                st.markdown("---")

# 푸터
st.markdown("---")
st.caption("🗳️ 그룹 투표 기능으로 친구들과 쉽게 메뉴를 결정하세요!")

