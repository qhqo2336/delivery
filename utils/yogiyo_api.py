"""
요기요 API 연동 모듈
"""
import requests
from typing import List, Dict, Optional
import os

def get_category_code(category_name: str) -> Optional[str]:
    """
    카테고리 이름을 요기요 API category_code로 변환
    
    Args:
        category_name: 카테고리 이름 (예: "치킨", "피자/양식" 등)
    
    Returns:
        category_code 또는 None (전체)
    """
    category_map = {
        "치킨": "chicken",
        "피자/양식": "pizza",
        "중국집": "chinese_dish",
        "한식": "korean_dish",
        "일식/돈까스": "japanese_dish",
        "족발/보쌈": "pig_trotter",
        "야식": "late_night_snack",
        "분식": "korean_snack",
        "카페/디저트": "cafe_dessert"
    }
    
    return category_map.get(category_name)

def get_yogiyo_shops_by_search(
    lat: float = 35.1409461,
    lng: float = 126.92566432,
    search: str = "",
    items: int = 60,
    order: str = "rank",
    page: int = 0
) -> Optional[Dict]:
    """
    요기요 검색 API를 사용하여 음식점 검색 (검색어 기반)
    
    Args:
        lat: 위도
        lng: 경도
        search: 검색어
        items: 가져올 개수
        order: 정렬 방식 (rank, distance 등)
        page: 페이지 번호
    
    Returns:
        API 응답 데이터 또는 None
    """
    url = "https://api.yogiyo.co.kr/discovery/search/restaurant"
    
    headers = {
        "accept": "application/json",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjMzOTA5MTEsImV4cCI6MTc2MzM5ODExMSwicGxhdGZvcm0iOiJZR1kiLCJyb2xlIjoidXNlciIsInN1Yl9pZCI6IjkxMjMwOTM0NSIsImJhc2VfdXJsIjoiaHR0cHM6Ly93d3cueW9naXlvLmNvLmtyIn0.vbMrLWY4evw2ErPHjvFIlTXAwn3niUXcto25-YaYjZGbdj36bmdrDMBfVwYbqAN6TGP4lBj04_cxPtcJOHLP71aibvIvCWZzO19CxMHEfG8Rbhh-E_b-ianZut-gkOSRBMVEY11fUlaXmowReM9cJUlKPDfEeOolgPNviSKhTb8BZDV5X0li7Cgp5t6_2SipwjxIboPLKpTpt88iHzNNiBz07FKFlNTzTSrlU8nK0cCPTJT1cmJsq1K9jUUxwg_vviskZa_9eTWQT7JyOJ8UR1dSU8rDvPllU2yGpu3XjYrYZKHvtsIzTPGtvpW0ZhxxRGYy3zz2OJCV5UINUNQoIA",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.yogiyo.co.kr",
        "referer": "https://www.yogiyo.co.kr/",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36",
        "x-apikey": "iphoneap",
        "x-apisecret": "fe5183cc3dea12bd0ce299cf110a75a2"
    }
    
    params = {
        "incoming_service_type": "YGY_WEB",
        "items": str(items),
        "lat": str(lat),
        "lng": str(lng),
        "order": order,
        "page": str(page),
        "search": search,
        "serving_type": "vd"  # 배달 가능한 곳만
    }
    
    try:
        print(f"[DEBUG] 검색 API 호출: search='{search}', lat={lat}, lng={lng}")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"[DEBUG] 응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[DEBUG] 응답 데이터 키: {list(data.keys()) if isinstance(data, dict) else '리스트'}")
            if isinstance(data, dict) and 'restaurant' in data:
                restaurant_data = data.get('restaurant', [])
                print(f"[DEBUG] restaurant 데이터 타입: {type(restaurant_data)}, 길이: {len(restaurant_data) if isinstance(restaurant_data, (list, dict)) else 'N/A'}")
            return data
        else:
            print(f"요기요 검색 API 오류: {response.status_code}")
            print(f"응답 내용: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"요기요 검색 API 요청 오류: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_yogiyo_shops(
    lat: float = 35.1409461,
    lng: float = 126.92566432,
    search: str = "",
    adm_code: str = "2911065500",
    length: int = 60,
    sort: str = "RANK_DESC",
    category_code: Optional[str] = None
) -> Optional[Dict]:
    """
    요기요 API를 사용하여 주변 음식점 목록 가져오기
    
    Args:
        lat: 위도 (기본값: 광주 조선대)
        lng: 경도 (기본값: 광주 조선대)
        search: 검색 키워드
        adm_code: 행정구역 코드
        length: 가져올 개수 (최대 60)
        sort: 정렬 방식 (RANK_DESC, DISTANCE_ASC 등)
        category_code: 카테고리 코드 (chicken, pizza, chinese_dish 등)
    
    Returns:
        API 응답 데이터 또는 None
    """
    url = "https://shopyo.yogiyo.co.kr/v1/shops"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "origin": "https://www.yogiyo.co.kr",
        "referer": "https://www.yogiyo.co.kr/",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36",
        "x-api-key": "qua9EeW1ohth4ain",
        "x-ygy-app-version": "8.50.0",
        "x-ygy-os-type": "IOS",
        "x-ygy-route": "v2"
    }
    
    params = {
        "adm_code": adm_code,
        "customer_id": "912309345",  # 기본값
        "lat": str(lat),
        "lng": str(lng),
        "length": str(length),
        "membership_code": "NONE",
        "search": search,
        "serving_types": "VD",  # 배달 가능한 곳만
        "sort": sort,
        "start": "0",
        "use_bargainyo": "false",
        "vertical_types": "FOOD"
    }
    
    # category_code가 있으면 추가
    if category_code:
        params["category_code"] = category_code
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"요기요 API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"요기요 API 요청 오류: {e}")
        return None

def format_shop_info(shop: Dict) -> Dict:
    """
    음식점 정보를 포맷팅
    검색 API와 일반 API 두 가지 형식을 모두 지원
    
    Args:
        shop: API 응답의 개별 음식점 데이터
    
    Returns:
        포맷팅된 음식점 정보
    """
    # ID 처리 (검색 API는 문자열, 일반 API는 숫자)
    shop_id = shop.get('id')
    if isinstance(shop_id, str):
        shop_id = int(shop_id) if shop_id.isdigit() else shop_id
    
    # 검색 API 형식인지 확인 (review_avg 필드가 있으면 검색 API)
    is_search_api = 'review_avg' in shop
    
    if is_search_api:
        # 검색 API 형식
        rating = shop.get('review_avg', 0)
        review_count = shop.get('review_count', 0)
        is_open = shop.get('is_open', False) or shop.get('open', False)
        categories = shop.get('categories', [])
        thumbnail_url = shop.get('thumbnail_url', '')
        logo_url = shop.get('logo_url', '') or shop.get('new_logo_url', '')
        
        # 배달비 (직접 필드)
        delivery_fee = shop.get('delivery_fee', 0) or shop.get('adjusted_delivery_fee', 0)
        
        # 배달 시간 파싱 ("24~39분" 형식)
        delivery_time_str = shop.get('estimated_delivery_time', '')
        min_time, max_time = 0, 0
        if delivery_time_str and '~' in delivery_time_str:
            try:
                parts = delivery_time_str.replace('분', '').split('~')
                min_time = int(parts[0].strip())
                max_time = int(parts[1].strip()) if len(parts) > 1 else min_time
            except:
                pass
        
        # 거리 (km 단위를 미터로 변환)
        distance_km = shop.get('distance', 0)
        distance_m = distance_km * 1000 if distance_km else 0
        
        # 위치 정보
        location = {
            'lat': shop.get('lat', 0),
            'lng': shop.get('lng', 0)
        }
        
        # 프랜차이즈 정보
        franchise = {}
        if shop.get('franchise_id'):
            franchise = {
                'id': shop.get('franchise_id'),
                'name': shop.get('franchise_name', '')
            }
        
        # 쿠폰 할인
        coupon_discount = shop.get('additional_discount') or shop.get('maximum_discount_coupon_price') or 0
        if coupon_discount is None:
            coupon_discount = 0
        
    else:
        # 일반 API 형식 (/v1/shops)
        serving_type = shop.get('serving_type', {})
        vd_info = serving_type.get('vd', {})
        
        # 배달비 정보
        delivery_fees = vd_info.get('delivery_fee_by_order_amounts', [])
        delivery_fee = min([df['delivery_fee'] for df in delivery_fees]) if delivery_fees else 0
        
        # 예상 배달 시간
        delivery_time = vd_info.get('estimated_delivery_minute', {})
        min_time = delivery_time.get('minimum', 0)
        max_time = delivery_time.get('maximum', 0)
        
        # 리뷰 정보
        review = shop.get('review', {})
        rating = review.get('average_rating', 0)
        review_count = review.get('count', 0)
        
        # 영업 상태
        open_status = shop.get('open_status', {})
        is_open = open_status.get('current_open_status') == 'OPENING_TIME'
        
        # 카테고리
        categories = shop.get('vendor_categories', [])
        
        # 이미지
        image = shop.get('image', {})
        thumbnail_url = image.get('thumbnail_url', '')
        logo_url = image.get('logo_url', '')
        
        # 거리 (미터)
        distance_m = round(shop.get('distance', 0), 0) if shop.get('distance') else 0
        
        # 위치 정보
        location = shop.get('location', {})
        
        # 프랜차이즈 정보
        franchise = shop.get('franchise', {})
        
        # 쿠폰 할인
        coupon_discount = 0
        if vd_info.get('coupon_discount'):
            coupon_discount = vd_info.get('coupon_discount', {}).get('maximum_amount', 0) or 0
    
    return {
        'id': shop_id,
        'name': shop.get('name', '이름 없음'),
        'categories': categories,
        'rating': round(rating, 1) if rating else 0,
        'review_count': review_count or 0,
        'distance': round(distance_m, 0),
        'min_delivery_fee': delivery_fee or 0,
        'delivery_time_min': min_time or 0,
        'delivery_time_max': max_time or 0,
        'is_open': is_open,
        'thumbnail_url': thumbnail_url or '',
        'logo_url': logo_url or '',
        'location': location,
        'franchise': franchise,
        'tags': shop.get('tags', []),
        'coupon_discount': coupon_discount or 0
    }

def filter_shops(shops: List[Dict], category: str = "", min_rating: float = 0.0, max_distance: float = 0.0) -> List[Dict]:
    """
    음식점 목록 필터링
    
    Args:
        shops: 포맷팅된 음식점 목록
        category: 카테고리 필터
        min_rating: 최소 평점
        max_distance: 최대 거리 (미터)
    
    Returns:
        필터링된 음식점 목록
    """
    filtered = shops
    
    if category:
        filtered = [s for s in filtered if category in s.get('categories', [])]
    
    if min_rating > 0:
        filtered = [s for s in filtered if s.get('rating', 0) >= min_rating]
    
    if max_distance > 0:
        filtered = [s for s in filtered if s.get('distance', 0) <= max_distance]
    
    return filtered

def get_yogiyo_shop_url(shop_id: int) -> str:
    """
    요기요 음식점 상세 페이지 URL 생성
    """
    return f"https://www.yogiyo.co.kr/mobile/#/{shop_id}/"

def get_restaurant_menus(shop_id: int, lat: float = 35.1409461, lng: float = 126.92566432) -> Optional[Dict]:
    """
    요기요 API를 사용하여 음식점의 메뉴 목록 가져오기
    
    Args:
        shop_id: 음식점 ID
        lat: 위도
        lng: 경도
    
    Returns:
        메뉴 데이터 (menu_sections, menu, option 포함) 또는 None
    """
    url = f"https://frontyo.yogiyo.co.kr/v1/aggregation/shops/{shop_id}/menus"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjMzOTY2MjIsImV4cCI6MTc2MzQwMzgyMiwicGxhdGZvcm0iOiJZR1kiLCJyb2xlIjoidXNlciIsInN1Yl9pZCI6IjkxMjMxMTUzMyIsImJhc2VfdXJsIjoiaHR0cHM6Ly93d3cueW9naXlvLmNvLmtyIn0.eQs4HEypDH0fHrvqJnqfYzI7LBwslZ6IX0OiIZv1AeP76dYz6VR6rie8J42smJTW-ClE5E63FdQwGLm3Efk0y37wDizpnQRYzcERYHvdLoMX3UjKIJa8h82mPHlFOMqYWBN050uXj6qYzDS2Zuc7x-NGGc4rhqdWut5KJAQjZzRNfipK3X4hFkqlOyjQofSFc9uxB96bkLwHaCwGQ9V79gz_tMG0j1A29638ezfUuzFvEkfFRAiKruXePAdnbnjvMn9T_W5p0em1S-obsUn29GNXn8q88zG2i62EJdZs6VuCLgE0C65Y91NF4XrYV5L74EgTdBhzgZrMl8DCVw-mBQ",
        "origin": "https://www.yogiyo.co.kr",
        "referer": "https://www.yogiyo.co.kr/",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36",
        "x-ygy-app-version": "8.50.0",
        "x-ygy-device-id": "MOBILE-WEB",
        "x-ygy-device-model": "MOBILE-WEB",
        "x-ygy-locale": "ko",
        "x-ygy-os-type": "IOS",
        "x-ygy-os-version": "18"
    }
    
    params = {
        "lat": str(lat),
        "lng": str(lng),
        "order_serving_type": "delivery"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"요기요 메뉴 API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"요기요 메뉴 API 요청 오류: {e}")
        return None

def get_location_coordinates(location_name: str) -> tuple:
    """
    위치 이름을 좌표로 변환 (간단한 매핑)
    실제로는 Geocoding API를 사용해야 함
    """
    location_map = {
        "광주": (35.1595, 126.8526),  # 광주시청
        "광주 동구": (35.1460, 126.9230),  # 동구청
        "광주 서구": (35.1520, 126.8880),  # 서구청
        "광주 남구": (35.1330, 126.9010),  # 남구청
        "광주 북구": (35.1740, 126.9120),  # 북구청
        "광주 광산구": (35.1390, 126.7940),  # 광산구청
        "조선대": (35.1409461, 126.92566432),  # 조선대학교
        "서울": (37.5665, 126.9780),
        "강남": (37.4979, 127.0276),
        "홍대": (37.5563, 126.9236),
        "이태원": (37.5345, 126.9946),
        "신촌": (37.5551, 126.9368),
        "명동": (37.5636, 126.9826),
        "잠실": (37.5133, 127.1028),
        "판교": (37.3947, 127.1112),
        "분당": (37.3597, 127.1115),
    }
    
    # 정확한 매칭 우선
    if location_name in location_map:
        return location_map[location_name]
    
    # 부분 매칭
    for key, coords in location_map.items():
        if key in location_name:
            return coords
    
    # 기본값: 광주 조선대
    return (35.1409461, 126.92566432)

