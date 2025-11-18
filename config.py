"""
설정 파일 로더
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 기본 설정
DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 1500
TEMPERATURE = 0.8



