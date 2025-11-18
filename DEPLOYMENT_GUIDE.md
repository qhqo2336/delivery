# Streamlit Cloud 배포 가이드

## 🌐 배포된 앱

**라이브 URL**: https://delivery-6b8aksjtxpc2767pwr49fg.streamlit.app/

## 🚀 배포 방법

### 1. GitHub 레포지토리 준비
- ✅ 이미 완료: https://github.com/qhqo2336/delivery

### 2. Streamlit Cloud 설정

1. **Streamlit Cloud 접속**
   - https://share.streamlit.io/ 방문
   - GitHub 계정으로 로그인

2. **New app 생성**
   - "New app" 버튼 클릭
   - Repository: `qhqo2336/delivery`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: 원하는 URL 입력

3. **Secrets 설정 (중요!)**
   - Deploy 전에 "Advanced settings" 클릭
   - "Secrets" 섹션에서 다음 내용 입력:
   
   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   ```
   
   - OpenAI API 키는 https://platform.openai.com/api-keys 에서 발급

4. **Deploy 클릭**
   - 앱이 자동으로 빌드되고 배포됩니다
   - 약 2-3분 소요

### 3. 배포 후 확인사항

✅ **정상 작동 확인:**
- 메인 페이지 로딩 확인
- 🤖 AI 메뉴 추천 기능 테스트
- 📊 히스토리 페이지 작동 확인
- 🗳️ 그룹 투표 페이지 확인
- 🗺️ 주변 음식점 검색 확인

### 4. 문제 해결

#### ❌ Healthcheck 실패 시
```
Get "http://localhost:8501/healthz": dial tcp 127.0.0.1:8501: connect: connection refused
```

**원인:**
1. API 키가 설정되지 않음
2. `st.set_page_config()` 중복 호출

**해결:**
1. Streamlit Cloud > Settings > Secrets에서 API 키 확인
2. 코드에서 `st.set_page_config()`는 app.py에만 존재해야 함

#### ⚠️ API 키 오류
```
OPENAI_API_KEY가 설정되지 않았습니다
```

**해결:**
- Streamlit Cloud > App Settings > Secrets 확인
- API 키 형식 확인 (따옴표로 감싸기)
- 앱 재시작 (Reboot app)

#### 🔄 코드 업데이트
```bash
git add .
git commit -m "Update code"
git push origin main
```
- Push 후 자동으로 재배포됨

### 5. 성능 최적화

- **캐싱 활용**: `@st.cache_data`, `@st.cache_resource` 사용
- **리소스 제한**: Streamlit Cloud는 무료 플랜에서 1GB RAM 제한
- **외부 API 호출 최소화**: 필요한 경우에만 API 호출

## 📝 환경 변수 목록

필수:
- `OPENAI_API_KEY`: OpenAI GPT API 키

선택:
- 추가 API 키는 필요에 따라 설정

## 🔗 유용한 링크

- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets 관리](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [OpenAI API](https://platform.openai.com/docs)

