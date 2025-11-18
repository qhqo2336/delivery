# 🍽️ AI 기반 맞춤형 메뉴 추천 서비스

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://delivery-6b8aksjtxpc2767pwr49fg.streamlit.app/)

**오늘 뭐 먹지?** 고민은 이제 그만! AI가 당신의 상황에 딱 맞는 메뉴를 추천해드립니다.

## 🌐 라이브 데모

🚀 **지금 바로 사용해보세요**: https://delivery-6b8aksjtxpc2767pwr49fg.streamlit.app/

## 📋 서비스 소개

매일 반복되는 "오늘 뭐 먹지?" 고민과 메뉴 선택의 스트레스를 AI가 해결해드립니다.
사용자의 현재 컨디션, 스트레스 수준, 예산, 식사 제약사항 등을 고려하여 
가장 적합한 메뉴를 GPT가 추천해드립니다.

### 🎯 주요 기능

- **맞춤형 AI 추천**: GPT-4를 활용한 상황 맞춤형 메뉴 추천
- **상황 인지형 추천**: 컨디션, 스트레스 수준, 식사 시간대 등을 반영
- **제약 조건 반영**: 알레르기, 채식, 칼로리/단백질 목표 등 고려
- **빠른 결정 지원**: 메뉴 선택 시간을 70% 단축

## 📋 요구사항

- Python 3.8 이상
- OpenAI API Key (GPT 사용을 위해 필요)

## 🚀 시작하기

### 1. 가상환경 생성 및 활성화

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. OpenAI API Key 설정

두 가지 방법 중 하나를 선택하세요:

#### 방법 1: 환경 변수 사용 (권장)

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가:

```env
OPENAI_API_KEY=your_api_key_here
```

#### 방법 2: Streamlit Secrets 사용

`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 추가:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

> 💡 **API Key 발급 방법**: [OpenAI Platform](https://platform.openai.com/api-keys)에서 무료로 발급받을 수 있습니다.

### 4. 앱 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리면서 `http://localhost:8501`에서 앱이 실행됩니다! 🎉

## 📁 프로젝트 구조

```
delivery/
├── app.py                      # 메인 Streamlit 앱 (AI 메뉴 추천)
├── pages/                      # 멀티페이지
│   ├── 1_📊_히스토리.py        # 히스토리 및 통계
│   ├── 2_🗳️_그룹투표.py        # 그룹 메뉴 투표
│   └── 3_🗺️_주변음식점.py      # 주변 음식점 검색
├── utils/                      # 유틸리티 모듈
│   ├── __init__.py
│   ├── history.py             # 히스토리 관리
│   ├── weather.py             # 날씨 API
│   ├── delivery.py            # 배달앱 링크 생성
│   └── map_api.py             # 지도 API (고급 기능)
├── data/                       # 데이터 저장 (자동 생성)
│   ├── history.json           # 사용자 히스토리
│   └── votes/                 # 투표 세션 데이터
├── config.py                  # 설정 파일 로더
├── requirements.txt           # Python 패키지
├── prd.md                     # 제품 요구사항 정의서
├── README.md                  # 프로젝트 소개
├── FEATURE_GUIDE.md           # 전체 기능 가이드 ⭐
├── SETUP_GUIDE.md             # 빠른 설치 가이드
├── REQUIRED_API_KEYS.md       # 필요한 API 키 안내
├── .env                       # 환경 변수 (로컬)
├── .gitignore                # Git 제외 파일
└── .streamlit/               # Streamlit 설정
    └── config.toml           # 테마 설정
```

## 💡 사용 방법

### 메인 기능 - AI 메뉴 추천
1. **현재 상황 입력**: 컨디션, 스트레스 수준, 식사 시간대 등을 입력
2. **선호도 설정**: 음식 종류, 예산, 매운맛 선호도, 제약사항 등을 선택
3. **AI 추천 받기**: 버튼 클릭 시 GPT가 3가지 맞춤 메뉴를 추천 (날씨 자동 반영!)
4. **메뉴 선택**: 추천된 메뉴 선택 → 배달앱/지도 링크로 바로 연결

### 추가 기능
- **📊 히스토리**: 사이드바에서 과거 추천 기록 및 통계 확인
- **🗳️ 그룹투표**: 친구들과 메뉴 투표 생성 및 참여
- **🗺️ 주변음식점**: 위치 + 메뉴로 주변 맛집 검색

**📖 전체 기능 가이드**: [`FEATURE_GUIDE.md`](./FEATURE_GUIDE.md)

## 🎨 주요 기술 스택

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o-mini
- **Language**: Python 3.8+

## 📖 유용한 명령어

```bash
# 기본 실행
streamlit run app.py

# 특정 포트에서 실행
streamlit run app.py --server.port 8502

# 브라우저 자동 열기 비활성화
streamlit run app.py --server.headless true

# 패키지 업데이트
pip install --upgrade -r requirements.txt
```

## 🔧 커스터마이징

### 테마 변경

`.streamlit/config.toml` 파일에서 색상과 폰트를 변경할 수 있습니다:

```toml
[theme]
primaryColor = "#FF4B4B"        # 주요 색상
backgroundColor = "#FFFFFF"      # 배경색
secondaryBackgroundColor = "#F0F2F6"  # 사이드바 배경색
textColor = "#262730"           # 텍스트 색상
font = "sans serif"             # 폰트
```

### GPT 모델 변경

`app.py`의 67번째 라인에서 모델을 변경할 수 있습니다:

```python
model="gpt-4o-mini"  # gpt-4, gpt-3.5-turbo 등으로 변경 가능
```

## 🐛 문제 해결

### API Key 오류
```
⚠️ OPENAI_API_KEY가 설정되지 않았습니다.
```
→ `.env` 파일에 올바른 API Key가 설정되어 있는지 확인하세요.

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔗 참고 자료

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [프로젝트 PRD](./prd.md)

## ✅ 구현 완료된 기능

- [x] 🎯 **맞춤형 AI 추천** - GPT-4o-mini 활용
- [x] 📊 **히스토리 저장 기능** - 과거 선택 기록 분석
- [x] 🌦️ **날씨 자동 반영** - 실시간 날씨 API 연동
- [x] 🗳️ **그룹 투표 기능** - 친구들과 메뉴 투표
- [x] 🗺️ **지도 연동** - 주변 음식점 찾기
- [x] 📱 **배달앱 연동** - 배달의민족, 쿠팡이츠 등 바로 연결

**📖 자세한 사용법**: [`FEATURE_GUIDE.md`](./FEATURE_GUIDE.md) 참고

## 📝 라이선스

MIT License

---

Made with ❤️ using Streamlit & OpenAI GPT

