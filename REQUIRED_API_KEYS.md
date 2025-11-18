# 📋 필요한 API 키 및 자료 목록

## ✅ 이미 설정된 것

- [x] **OpenAI API Key** - GPT 메뉴 추천에 사용 중

## 📝 추가 기능 구현을 위해 필요한 것들

### 1. 🌦️ 날씨 자동 반영 기능

**필요한 것:**
- OpenWeatherMap API Key (무료)

**발급 방법:**
1. [OpenWeatherMap](https://openweathermap.org/api) 접속
2. 회원가입 후 로그인
3. API Keys 메뉴에서 무료 키 발급
4. `.env` 파일에 추가:
   ```
   OPENWEATHER_API_KEY=your_key_here
   ```

**무료 플랜 제한:**
- 1분당 60회 요청
- 현재 날씨, 5일 예보 제공

---

### 2. 🗺️ 지도 연동 기능

**필요한 것:**
- Kakao Map API Key (무료) - 한국 지역에 최적화

**발급 방법:**
1. [Kakao Developers](https://developers.kakao.com/) 접속
2. 로그인 후 '내 애플리케이션' 생성
3. '앱 키' 섹션에서 'JavaScript 키' 복사
4. `.env` 파일에 추가:
   ```
   KAKAO_MAP_API_KEY=your_key_here
   ```

**또는 Google Maps API 사용 (선택사항):**
- [Google Cloud Console](https://console.cloud.google.com/)
- Places API, Maps JavaScript API 활성화
- 카드 등록 필요 (무료 크레딧 $200/월)

**추천:** Kakao Map (한국 지역, 카드 등록 불필요)

---

### 3. 🗳️ 그룹 투표 기능

**필요한 것:**
- ❌ 추가 API 키 불필요
- Streamlit의 session_state와 URL 파라미터만으로 구현 가능

**구현 방법:**
- URL 기반 세션 공유
- 로컬 메모리 또는 JSON 파일로 투표 데이터 저장

---

### 4. 📊 히스토리 저장 기능

**필요한 것:**
- ❌ 추가 API 키 불필요
- Streamlit의 session_state 또는 SQLite로 구현

**구현 방법:**
- 옵션 1: SQLite 로컬 DB (권장)
- 옵션 2: JSON 파일 저장
- 옵션 3: Session state (세션 종료 시 삭제)

---

### 5. 📱 배달앱 연동 기능

**필요한 것:**
- ❌ 공식 API 키 불필요
- 딥링크 및 검색 URL로 구현

**지원 예정 앱:**
- 배달의민족 (검색 URL)
- 쿠팡이츠 (검색 URL)
- 요기요 (검색 URL)

**참고:** 공식 API는 사업자 등록이 필요하므로, 웹 검색 링크로 구현

---

## 🚀 우선순위 구현 순서

1. **📊 히스토리 저장** ← API 키 불필요, 가장 빠르게 구현 가능
2. **🌦️ 날씨 자동 반영** ← OpenWeatherMap API 키 필요
3. **🗳️ 그룹 투표 기능** ← API 키 불필요
4. **📱 배달앱 연동** ← API 키 불필요
5. **🗺️ 지도 연동** ← Kakao Map API 키 필요

---

## 📝 .env 파일 최종 형태

```env
# OpenAI (이미 설정됨)
OPENAI_API_KEY=sk-your-openai-key

# 날씨 API (필요 시)
OPENWEATHER_API_KEY=your-openweather-key

# 지도 API (필요 시)
KAKAO_MAP_API_KEY=your-kakao-key
```

---

## ✅ 체크리스트

### 당장 필요한 것:
- [ ] 히스토리 저장 - API 키 불필요 ✅
- [ ] 그룹 투표 - API 키 불필요 ✅
- [ ] 배달앱 연동 - API 키 불필요 ✅

### 나중에 필요한 것:
- [ ] OpenWeatherMap API Key 발급 (날씨 기능)
- [ ] Kakao Map API Key 발급 (지도 기능)

**참고:** API 키 없이도 3개 기능은 바로 구현 가능합니다!



