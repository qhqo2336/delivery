# 🚀 빠른 설치 가이드

## 1️⃣ Python 및 패키지 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Git Bash)
source venv/Scripts/activate

# 패키지 설치
pip install -r requirements.txt
```

## 2️⃣ OpenAI API Key 설정

### Option 1: .env 파일 생성 (권장)

프로젝트 루트에 `.env` 파일을 직접 생성하고 다음 내용 추가:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Option 2: Streamlit Secrets 사용

`.streamlit/secrets.toml` 파일 생성:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

그리고 `app.py`의 18번째 줄을 다음과 같이 수정:

```python
# 기존
api_key = os.getenv("OPENAI_API_KEY")

# 변경
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
```

## 3️⃣ API Key 발급 받기

1. [OpenAI Platform](https://platform.openai.com/) 접속
2. 회원가입/로그인
3. [API Keys](https://platform.openai.com/api-keys) 메뉴 클릭
4. "Create new secret key" 버튼 클릭
5. 생성된 키를 복사하여 `.env` 파일에 붙여넣기

> ⚠️ **중요**: API Key는 절대 공개하지 마세요! Git에 커밋되지 않도록 `.gitignore`에 이미 설정되어 있습니다.

## 4️⃣ 앱 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 `http://localhost:8501`로 열립니다! 🎉

## 5️⃣ 테스트

1. 컨디션, 스트레스 수준 등을 입력
2. "AI 메뉴 추천 받기" 버튼 클릭
3. GPT가 3가지 메뉴를 추천해줍니다!

## 🐛 문제 발생 시

### ImportError: No module named 'openai'
```bash
pip install --upgrade openai
```

### API Key 에러
- `.env` 파일이 프로젝트 루트에 있는지 확인
- API Key가 `sk-`로 시작하는지 확인
- API Key에 공백이나 따옴표가 없는지 확인

### Streamlit 실행 안됨
```bash
pip install --upgrade streamlit
```

## 💰 비용 관련

- GPT-4o-mini 모델 사용 시 매우 저렴합니다 (요청당 약 $0.0001~0.0003)
- 테스트 용도로는 OpenAI 무료 크레딧으로 충분합니다
- 프로덕션 환경에서는 사용량에 따라 과금됩니다

## ✅ 체크리스트

- [ ] Python 3.8+ 설치 확인
- [ ] 가상환경 생성 및 활성화
- [ ] 패키지 설치 완료
- [ ] OpenAI API Key 발급
- [ ] `.env` 파일 생성 및 API Key 설정
- [ ] `streamlit run app.py` 실행
- [ ] 브라우저에서 앱 접속 확인
- [ ] 메뉴 추천 테스트 완료

완료하셨나요? 이제 AI 메뉴 추천 서비스를 즐겨보세요! 🍽️



