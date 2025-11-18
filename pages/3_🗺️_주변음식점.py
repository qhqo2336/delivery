"""
주변 음식점 찾기 페이지
"""
import streamlit as st
import sys
import os

# 상위 디렉토리의 utils 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.delivery import get_naver_map_search_url, get_kakao_map_search_url, get_google_search_url
from utils.yogiyo_api import (
    get_yogiyo_shops, 
    get_yogiyo_shops_by_search,
    format_shop_info, 
    filter_shops, 
    get_yogiyo_shop_url,
    get_location_coordinates,
    get_category_code,
    get_restaurant_menus
)

st.title("🗺️ 주변 음식점 찾기")
st.markdown("원하는 메뉴와 위치를 입력하면 주변 음식점을 찾아드립니다.")
st.markdown("---")

# 위치 옵션 리스트 (초기화에서 사용)
LOCATION_OPTIONS = [
    "조선대",
    "광주 동구",
    "광주 서구",
    "광주 남구",
    "광주 북구",
    "광주 광산구",
    "광주",
    "서울"
]

# session_state 초기화
if 'menu_search' not in st.session_state:
    st.session_state.menu_search = ''
if 'location_search' not in st.session_state:
    st.session_state.location_search = LOCATION_OPTIONS[0]  # 기본값: 조선대
if 'do_search' not in st.session_state:
    st.session_state.do_search = False
if 'category_filter' not in st.session_state:
    st.session_state.category_filter = '전체'


# 음식 종류 필터 (배지 형태) - 검색 입력 위에 배치
st.markdown("### 🍽️ 음식 종류")
categories = ["전체", "치킨", "피자/양식", "한식", "중국집", "일식/돈까스", "분식", "족발/보쌈", "카페/디저트"]
category_filter = st.session_state.category_filter

# 배지 형태로 카테고리 표시
category_cols = st.columns(len(categories))
for idx, category in enumerate(categories):
    with category_cols[idx]:
        is_selected = category_filter == category
        button_type = "primary" if is_selected else "secondary"
        if st.button(
            category,
            key=f"category_{category}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state.category_filter = category
            st.rerun()

st.markdown("---")

# 입력 폼
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    menu_name = st.text_input(
        "🍽️ 찾고 싶은 음식이나 메뉴를 입력하세요",
        placeholder="예: 짜장면, 삼겹살, 초밥, 파스타...",
        key="menu_search"
    )

with col2:
    location = st.selectbox(
        "📍 위치를 선택하세요",
        options=LOCATION_OPTIONS,
        key="location_search"
    )

with col3:
    search_button = st.button("🔍 검색", type="primary", use_container_width=True)
    if search_button:
        st.session_state.do_search = True
        st.rerun()

st.markdown("---")

# 추가 필터 옵션
with st.expander("🔧 추가 필터 옵션", expanded=False):
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        min_rating = st.slider("최소 평점", 0.0, 5.0, 0.0, 0.1, key="rating_filter")
    
    with filter_col2:
        max_distance = st.slider("최대 거리 (m)", 0, 5000, 5000, 100, key="distance_filter")

# 검색 실행 조건: 검색 버튼이 클릭되었을 때
should_search = st.session_state.do_search

# 검색 실행 후 플래그 초기화
if should_search:
    st.session_state.do_search = False

# 요기요 API로 실제 음식점 검색
if should_search:
    st.markdown("---")
    
    # 위치 좌표 변환
    lat, lng = get_location_coordinates(location)
    
    # 검색어가 있으면 검색 API 사용, 없으면 일반 API 사용
    with st.spinner("🔍 주변 음식점을 검색 중입니다..."):
        if menu_name and menu_name.strip():
            # 검색어가 있으면 검색 API 사용
            search_term = menu_name.strip()
            st.info(f"🔍 검색어 '{search_term}'로 검색 중...")
            
            api_data = get_yogiyo_shops_by_search(
                lat=lat,
                lng=lng,
                search=search_term,
                items=60,
                order="rank"
            )
            
            # 검색 API 응답 형식에 맞게 shops 추출
            if api_data:
                # 응답 구조: { "restaurant": { "restaurants": [...] }, ... }
                if isinstance(api_data, dict):
                    restaurant_obj = api_data.get('restaurant', {})
                    if isinstance(restaurant_obj, dict):
                        # restaurant.restaurants 배열에서 데이터 추출
                        shops = restaurant_obj.get('restaurants', [])
                    elif isinstance(restaurant_obj, list):
                        shops = restaurant_obj
                    else:
                        shops = []
                elif isinstance(api_data, list):
                    shops = api_data
                else:
                    shops = []
                
                if not shops:
                    st.warning(f"⚠️ '{search_term}'에 대한 검색 결과가 없습니다.")
            else:
                shops = []
                st.error("⚠️ 검색 API 요청에 실패했습니다. 네트워크 연결을 확인해주세요.")
        else:
            # 검색어가 없으면 일반 API 사용 (카테고리 필터 지원)
            category_code = None
            selected_category = st.session_state.category_filter
            if selected_category != "전체":
                category_code = get_category_code(selected_category)
            
            api_data = get_yogiyo_shops(
                lat=lat,
                lng=lng,
                search="",
                length=60,
                category_code=category_code
            )
            shops = api_data.get('shops', []) if api_data else []
    
    if shops:
        
        # 포맷팅
        formatted_shops = [format_shop_info(shop) for shop in shops]
        
        # 추가 필터링 (평점, 거리만 - 카테고리는 API에서 이미 필터링됨)
        filtered_shops = filter_shops(
            formatted_shops,
            category="",  # API에서 이미 필터링했으므로 빈 문자열
            min_rating=min_rating,
            max_distance=max_distance if max_distance > 0 else 0
        )
        
        st.subheader(f"📍 '{location}' 주변 음식점 ({len(filtered_shops)}개)")
        
        if not filtered_shops:
            st.warning("⚠️ 조건에 맞는 음식점이 없습니다. 필터를 조정해보세요.")
        else:
            # 정렬 옵션
            sort_option = st.selectbox(
                "정렬 기준",
                ["평점 높은 순", "거리 가까운 순", "리뷰 많은 순", "배달비 낮은 순"],
                key="sort_option"
            )
            
            if sort_option == "평점 높은 순":
                filtered_shops.sort(key=lambda x: x.get('rating', 0), reverse=True)
            elif sort_option == "거리 가까운 순":
                filtered_shops.sort(key=lambda x: x.get('distance', 999999))
            elif sort_option == "리뷰 많은 순":
                filtered_shops.sort(key=lambda x: x.get('review_count', 0), reverse=True)
            elif sort_option == "배달비 낮은 순":
                filtered_shops.sort(key=lambda x: x.get('min_delivery_fee', 999999))
            
            # 음식점 목록 표시
            for idx, shop in enumerate(filtered_shops[:30]):  # 최대 30개만 표시
                with st.container():
                    col_img, col_info, col_action = st.columns([1.5, 3, 1])
                    
                    with col_img:
                        # 썸네일 이미지
                        thumbnail_url = shop.get('thumbnail_url')
                        if thumbnail_url:
                            try:
                                st.image(thumbnail_url, width=200, use_container_width=True)
                            except:
                                st.write("📷")
                        else:
                            st.write("📷")
                    
                    with col_info:
                        # 음식점 이름
                        name_display = shop['name']
                        if shop.get('franchise'):
                            franchise_name = shop['franchise'].get('special_title', '')
                            if franchise_name:
                                name_display = f"**{franchise_name}** {name_display}"
                        
                        st.markdown(f"### {name_display}")
                        
                        # 평점 및 리뷰
                        rating = shop.get('rating', 0)
                        review_count = shop.get('review_count', 0)
                        stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                        
                        info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                        
                        with info_col1:
                            st.markdown(f"**{stars}** {rating} ({review_count}개 리뷰)")
                        
                        with info_col2:
                            distance = shop.get('distance', 0)
                            st.markdown(f"📍 {distance:.0f}m")
                        
                        with info_col3:
                            delivery_fee = shop.get('min_delivery_fee', 0)
                            st.markdown(f"💰 배달비: {delivery_fee:,}원")
                        
                        with info_col4:
                            time_min = shop.get('delivery_time_min', 0)
                            time_max = shop.get('delivery_time_max', 0)
                            if time_min and time_max:
                                st.markdown(f"⏱️ {time_min}~{time_max}분")
                        
                        # 카테고리
                        categories = shop.get('categories', [])
                        if categories:
                            category_tags = " | ".join(categories[:3])
                            st.caption(f"🏷️ {category_tags}")
                        
                        # 영업 상태
                        if shop.get('is_open'):
                            st.success("✅ 영업 중")
                        else:
                            st.warning("⏸️ 영업 종료")
                        
                        # 쿠폰 할인
                        coupon = shop.get('coupon_discount', 0) or 0
                        if coupon and coupon > 0:
                            st.info(f"🎟️ 최대 {coupon:,}원 할인 쿠폰")
                    
                    with col_action:
                        shop_id = shop.get('id')
                        shop_name = shop.get('name', '')
                        
                        if shop_id:
                            yogiyo_url = get_yogiyo_shop_url(shop_id)
                            st.markdown(f"[🍽️ 요기요에서 주문]({yogiyo_url})")
                        
                        # 지도 링크
                        naver_url = get_naver_map_search_url(shop_name, location)
                        st.markdown(f"[🗺️ 네이버 지도]({naver_url})")
                    
                    # 메뉴 보기 expander - 카드 하단에 전체 width로 배치
                    if shop_id:
                        with st.expander("📋 메뉴 상세보기", expanded=False):
                            lat, lng = get_location_coordinates(location)
                            
                            with st.spinner("메뉴 정보를 불러오는 중..."):
                                menu_data = get_restaurant_menus(shop_id, lat, lng)
                            
                            if menu_data:
                                menu_sections = menu_data.get('menu_sections', [])
                                menus = menu_data.get('menu', {})
                                
                                if menu_sections:
                                    # 섹션별로 메뉴 표시
                                    for section in menu_sections:
                                        section_title = section.get('title', '메뉴')
                                        section_type = section.get('type', 'LIST')
                                        section_items = section.get('items', [])
                                        section_desc = section.get('description', '')
                                        
                                        # 섹션 헤더
                                        if section_type == 'CURATION':
                                            st.markdown(f"### ⭐ {section_title}")
                                        else:
                                            st.markdown(f"### 📋 {section_title}")
                                        
                                        if section_desc:
                                            st.caption(section_desc)
                                        
                                        # 메뉴 아이템을 4열 그리드로 표시
                                        if section_items:
                                            menu_cols = st.columns(4)
                                            
                                            for menu_idx, item_id in enumerate(section_items):
                                                col = menu_cols[menu_idx % 4]
                                                menu_item = menus.get(str(item_id))
                                                
                                                if menu_item:
                                                    with col:
                                                        # 메뉴 카드
                                                        with st.container():
                                                            # 메뉴 이미지
                                                            thumbnail = menu_item.get('thumbnail', {})
                                                            image_url = thumbnail.get('image', '')
                                                            if image_url:
                                                                try:
                                                                    st.image(image_url, use_container_width=True)
                                                                except:
                                                                    pass
                                                            
                                                            # 메뉴 이름 + 베스트 뱃지
                                                            menu_name = menu_item.get('name', '')
                                                            badges = menu_item.get('badges', [])
                                                            badge_text = ""
                                                            for badge in badges:
                                                                if badge.get('label') == '베스트':
                                                                    badge_text = " 🔥"
                                                            
                                                            st.markdown(f"**{menu_name}**{badge_text}")
                                                            
                                                            # 설명 (짧게만)
                                                            description = menu_item.get('description', '')
                                                            if description:
                                                                if len(description) > 30:
                                                                    description = description[:30] + "..."
                                                                st.caption(description)
                                                            
                                                            # 가격
                                                            price_info = menu_item.get('price', {})
                                                            final_price = price_info.get('final_price', 0)
                                                            origin_price = price_info.get('origin_price', 0)
                                                            
                                                            if final_price != origin_price and origin_price > 0:
                                                                st.markdown(f"~~{origin_price:,}원~~ **{final_price:,}원**")
                                                            else:
                                                                st.markdown(f"**{final_price:,}원**")
                                                            
                                                            # 리뷰 수
                                                            review_count = menu_item.get('review_count', 0)
                                                            if review_count > 0:
                                                                st.caption(f"💬 리뷰 {review_count}개")
                                                            
                                                            # 품절 여부
                                                            if menu_item.get('soldout'):
                                                                st.error("❌ 품절")
                                                            
                                                            st.markdown("---")
                                        
                                        st.markdown("")
                                    
                                    # 전체 메뉴 링크
                                    st.info(f"📱 전체 메뉴 및 주문은 [요기요에서 확인하기]({yogiyo_url})")
                                else:
                                    st.warning("메뉴 정보가 없습니다.")
                                    st.markdown(f"[🍽️ 요기요에서 확인하기]({yogiyo_url})")
                            else:
                                st.error("메뉴를 불러올 수 없습니다.")
                                st.markdown(f"[🍽️ 요기요에서 확인하기]({yogiyo_url})")
                    
                    if idx < len(filtered_shops) - 1:
                        st.markdown("---")
    
    else:
        st.warning("⚠️ 음식점을 찾을 수 없습니다. 위치나 검색어를 확인해주세요.")

