"""
날씨 정보 가져오기 모듈
"""
import requests
import os
from typing import Dict, Optional

def get_weather_data(city: str = "Seoul", api_key: Optional[str] = None) -> Optional[Dict]:
    """
    OpenWeatherMap API를 사용하여 날씨 정보 가져오기
    
    Args:
        city: 도시 이름 (기본값: Seoul)
        api_key: OpenWeatherMap API 키
    
    Returns:
        날씨 정보 딕셔너리 또는 None
    """
    if not api_key:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return None
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=kr"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            return {
                'temp': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
    except Exception as e:
        print(f"날씨 정보 가져오기 오류: {e}")
    
    return None

def get_weather_emoji(description: str) -> str:
    """날씨 설명에 따른 이모지 반환"""
    description_lower = description.lower()
    
    if '맑' in description_lower or 'clear' in description_lower:
        return "☀️"
    elif '비' in description_lower or 'rain' in description_lower:
        return "🌧️"
    elif '눈' in description_lower or 'snow' in description_lower:
        return "❄️"
    elif '구름' in description_lower or 'cloud' in description_lower:
        return "☁️"
    elif '안개' in description_lower or 'fog' in description_lower or 'mist' in description_lower:
        return "🌫️"
    elif '번개' in description_lower or 'thunder' in description_lower:
        return "⚡"
    else:
        return "🌤️"

def get_weather_recommendation(weather_data: Dict) -> str:
    """
    날씨에 따른 메뉴 추천 힌트 생성
    
    Args:
        weather_data: get_weather_data()의 반환값
    
    Returns:
        날씨 기반 추천 힌트
    """
    if not weather_data:
        return ""
    
    temp = weather_data['temp']
    description = weather_data['description']
    
    hints = []
    
    # 온도에 따른 추천
    if temp < 5:
        hints.append("추운 날씨에는 뜨끈한 국물 요리가 좋아요")
    elif temp < 15:
        hints.append("쌀쌀한 날씨에 따뜻한 음식이 어울려요")
    elif temp > 28:
        hints.append("더운 날씨에 시원한 음식이 좋아요")
    elif temp > 25:
        hints.append("더운 날씨에 가볍고 상큼한 메뉴가 어울려요")
    
    # 날씨 상태에 따른 추천
    if '비' in description or 'rain' in description.lower():
        hints.append("비 오는 날엔 전이나 따뜻한 국물 요리가 생각나죠")
    elif '눈' in description or 'snow' in description.lower():
        hints.append("눈 오는 날엔 뜨끈한 찌개나 전골이 최고예요")
    
    return " / ".join(hints) if hints else "날씨에 맞는 메뉴를 추천해드릴게요"

def format_weather_info(weather_data: Dict) -> str:
    """날씨 정보를 포맷팅된 문자열로 반환"""
    if not weather_data:
        return "날씨 정보를 가져올 수 없습니다"
    
    emoji = get_weather_emoji(weather_data['description'])
    
    return f"{emoji} {weather_data['description']} | {weather_data['temp']}°C (체감 {weather_data['feels_like']}°C)"



