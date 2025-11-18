"""
사용자 히스토리 관리 모듈
"""
import json
import os
from datetime import datetime
from typing import List, Dict

HISTORY_FILE = "data/history.json"

def ensure_data_dir():
    """데이터 디렉토리 생성"""
    os.makedirs("data", exist_ok=True)

def load_history() -> List[Dict]:
    """히스토리 로드"""
    ensure_data_dir()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history_item(user_data: Dict, recommendation: str, selected_menu: str = None):
    """히스토리 아이템 저장"""
    ensure_data_dir()
    
    history = load_history()
    
    history_item = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_data': user_data,
        'recommendation': recommendation,
        'selected_menu': selected_menu
    }
    
    history.append(history_item)
    
    # 최근 50개만 유지
    if len(history) > 50:
        history = history[-50:]
    
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_recent_history(limit: int = 10) -> List[Dict]:
    """최근 히스토리 가져오기"""
    history = load_history()
    return history[-limit:][::-1]  # 최근 것부터

def get_stats() -> Dict:
    """통계 정보 반환"""
    history = load_history()
    
    if not history:
        return {
            'total_count': 0,
            'favorite_food_types': [],
            'avg_budget': 0,
            'most_common_time': '없음'
        }
    
    # 음식 종류 통계
    food_types = {}
    budgets = []
    meal_times = {}
    
    for item in history:
        user_data = item.get('user_data', {})
        
        # 음식 종류
        food_type = user_data.get('food_type', '')
        for ft in food_type.split(', '):
            food_types[ft] = food_types.get(ft, 0) + 1
        
        # 예산
        budget = user_data.get('budget', 0)
        if budget:
            budgets.append(budget)
        
        # 식사 시간
        meal_time = user_data.get('meal_time', '')
        if meal_time:
            meal_times[meal_time] = meal_times.get(meal_time, 0) + 1
    
    # 가장 많이 선택한 음식 종류 (상위 3개)
    favorite_food_types = sorted(food_types.items(), key=lambda x: x[1], reverse=True)[:3]
    favorite_food_types = [ft[0] for ft in favorite_food_types if ft[0] and ft[0] != '제한 없음']
    
    # 평균 예산
    avg_budget = sum(budgets) / len(budgets) if budgets else 0
    
    # 가장 많은 식사 시간
    most_common_time = max(meal_times.items(), key=lambda x: x[1])[0] if meal_times else '없음'
    
    return {
        'total_count': len(history),
        'favorite_food_types': favorite_food_types,
        'avg_budget': int(avg_budget),
        'most_common_time': most_common_time
    }

def clear_history():
    """히스토리 전체 삭제"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)




