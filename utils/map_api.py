"""
지도 API 연동 모듈 (Kakao Map API)
API 키가 있을 때만 작동하는 고급 기능
"""
import os
import requests
from typing import List, Dict, Optional

def get_kakao_api_key() -> Optional[str]:
    """Kakao Map API 키 가져오기"""
    return os.getenv("KAKAO_MAP_API_KEY")

def search_places_by_keyword(keyword: str, x: str = "127.0276", y: str = "37.4979", radius: int = 5000) -> List[Dict]:
    """
    Kakao Map API를 사용하여 키워드로 장소 검색
    
    Args:
        keyword: 검색 키워드 (예: "강남 맛집")
        x: 중심 좌표 X (경도, 기본값: 강남역)
        y: 중심 좌표 Y (위도, 기본값: 강남역)
        radius: 검색 반경 (미터, 최대 20000)
    
    Returns:
        검색 결과 리스트
    """
    api_key = get_kakao_api_key()
    
    if not api_key:
        return []
    
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {
        "query": keyword,
        "x": x,
        "y": y,
        "radius": radius,
        "size": 15  # 결과 개수 (최대 15)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('documents', [])
    except Exception as e:
        print(f"Kakao Map API 오류: {e}")
    
    return []

def format_place_info(place: Dict) -> Dict:
    """
    장소 정보를 포맷팅
    
    Args:
        place: Kakao Map API 응답의 개별 장소 데이터
    
    Returns:
        포맷팅된 장소 정보
    """
    return {
        'name': place.get('place_name', '이름 없음'),
        'category': place.get('category_name', ''),
        'address': place.get('address_name', ''),
        'road_address': place.get('road_address_name', ''),
        'phone': place.get('phone', '정보 없음'),
        'place_url': place.get('place_url', ''),
        'distance': place.get('distance', ''),
        'x': place.get('x', ''),  # 경도
        'y': place.get('y', '')   # 위도
    }

def get_category_code(category: str) -> str:
    """
    카테고리명을 Kakao Map 카테고리 코드로 변환
    
    카테고리 코드:
    - FD6: 음식점
    - CE7: 카페
    - HP8: 병원
    - PM9: 약국
    """
    category_map = {
        '음식점': 'FD6',
        '카페': 'CE7',
        '한식': 'FD6',
        '중식': 'FD6',
        '일식': 'FD6',
        '양식': 'FD6',
    }
    
    return category_map.get(category, 'FD6')

def is_api_available() -> bool:
    """API 키가 설정되어 있는지 확인"""
    return get_kakao_api_key() is not None



