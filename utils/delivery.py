"""
배달앱 연동 모듈 - 검색 링크 생성
"""
import urllib.parse

def get_baemin_search_url(menu_name: str) -> str:
    """
    배달의민족 검색 URL 생성
    배민은 웹 검색 기능이 있음
    """
    encoded_menu = urllib.parse.quote(menu_name)
    return f"https://www.baemin.com/search?query={encoded_menu}"

def get_coupang_eats_search_url(menu_name: str) -> str:
    """
    쿠팡이츠 검색 URL 생성
    """
    encoded_menu = urllib.parse.quote(menu_name)
    return f"https://www.coupangeats.com/search?q={encoded_menu}"

def get_yogiyo_search_url(menu_name: str) -> str:
    """
    요기요 검색 URL 생성
    """
    encoded_menu = urllib.parse.quote(menu_name)
    return f"https://www.yogiyo.co.kr/mobile/#/search/?keyword={encoded_menu}"

def get_naver_map_search_url(menu_name: str, location: str = "") -> str:
    """
    네이버 지도 검색 URL 생성 (주변 음식점 찾기)
    """
    search_query = f"{location} {menu_name}" if location else menu_name
    encoded_query = urllib.parse.quote(search_query)
    return f"https://map.naver.com/v5/search/{encoded_query}"

def get_kakao_map_search_url(menu_name: str, location: str = "") -> str:
    """
    카카오맵 검색 URL 생성
    """
    search_query = f"{location} {menu_name}" if location else menu_name
    encoded_query = urllib.parse.quote(search_query)
    return f"https://map.kakao.com/?q={encoded_query}"

def get_google_search_url(menu_name: str, location: str = "서울") -> str:
    """
    구글 검색 URL 생성 (주변 음식점 찾기)
    """
    search_query = f"{location} {menu_name} 맛집"
    encoded_query = urllib.parse.quote(search_query)
    return f"https://www.google.com/search?q={encoded_query}"

def extract_menu_name_from_recommendation(recommendation_text: str, menu_number: int = 1) -> str:
    """
    GPT 추천 텍스트에서 메뉴명 추출
    
    Args:
        recommendation_text: GPT가 생성한 추천 텍스트
        menu_number: 추출할 메뉴 번호 (1, 2, 3)
    
    Returns:
        추출된 메뉴명 또는 빈 문자열
    """
    try:
        lines = recommendation_text.split('\n')
        for line in lines:
            # "1. **메뉴명**" 형식 찾기
            if line.strip().startswith(f"{menu_number}. **"):
                # ** 사이의 텍스트 추출
                start = line.find('**') + 2
                end = line.find('**', start)
                if start > 1 and end > start:
                    return line[start:end].strip()
    except:
        pass
    
    return ""

def get_all_delivery_links(menu_name: str, location: str = "서울") -> dict:
    """
    모든 배달앱 및 지도 링크 생성
    
    Args:
        menu_name: 메뉴 이름
        location: 위치 (기본값: 서울)
    
    Returns:
        앱별 링크 딕셔너리
    """
    return {
        'baemin': {
            'name': '배달의민족',
            'url': get_baemin_search_url(menu_name),
            'emoji': '🛵'
        },
        'coupang': {
            'name': '쿠팡이츠',
            'url': get_coupang_eats_search_url(menu_name),
            'emoji': '🚀'
        },
        'yogiyo': {
            'name': '요기요',
            'url': get_yogiyo_search_url(menu_name),
            'emoji': '🍽️'
        },
        'naver': {
            'name': '네이버 지도',
            'url': get_naver_map_search_url(menu_name, location),
            'emoji': '🗺️'
        },
        'kakao': {
            'name': '카카오맵',
            'url': get_kakao_map_search_url(menu_name, location),
            'emoji': '🗺️'
        },
        'google': {
            'name': '구글 검색',
            'url': get_google_search_url(menu_name, location),
            'emoji': '🔍'
        }
    }




