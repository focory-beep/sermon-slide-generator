#!/bin/bash

echo "📖 Sermon Slide Generator - 서버 시작"
echo "======================================"
echo ""

# Python 버전 확인
echo "🐍 Python 버전 확인..."
python3 --version

# 의존성 설치
echo ""
echo "📦 필요한 패키지 설치 중..."
pip install -r requirements.txt

# 서버 실행
echo ""
echo "🚀 서버 시작..."
echo "API 문서: http://localhost:8000/docs"
echo "웹 인터페이스: frontend/index.html 파일을 브라우저에서 열어주세요"
echo ""

cd backend
python3 main.py
