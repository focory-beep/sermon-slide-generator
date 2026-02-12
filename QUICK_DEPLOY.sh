#!/bin/bash

echo "🚀 예배 슬라이드 생성기 - GitHub 업로드 스크립트"
echo "=================================================="
echo ""

# Git 확인
if ! command -v git &> /dev/null; then
    echo "❌ Git이 설치되어 있지 않습니다."
    echo "   https://git-scm.com/downloads 에서 Git을 설치해주세요."
    exit 1
fi

echo "✅ Git 확인 완료"
echo ""

# GitHub 사용자 이름 입력
read -p "GitHub 사용자 이름을 입력하세요: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ 사용자 이름이 입력되지 않았습니다."
    exit 1
fi

echo ""
echo "📦 Git 저장소 초기화 중..."

# Git 초기화
git init

# .gitignore 확인
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore 파일이 없습니다. 생성합니다..."
fi

# 모든 파일 추가
echo "📁 파일 추가 중..."
git add .

# 커밋
echo "💾 커밋 생성 중..."
git commit -m "Initial commit: Sermon Slide Generator v2.0 - Cloud Ready"

# 원격 저장소 설정
echo "🔗 GitHub 저장소 연결 중..."
git remote add origin "https://github.com/${GITHUB_USERNAME}/sermon-slide-generator.git"

echo ""
echo "⚠️  다음 단계:"
echo "1. GitHub에서 새 저장소를 만드세요:"
echo "   https://github.com/new"
echo ""
echo "2. Repository name: sermon-slide-generator"
echo "3. Public 선택"
echo "4. Create repository 클릭 (README, .gitignore 추가하지 마세요!)"
echo ""
echo "5. 저장소를 만든 후, 아래 명령어를 실행하세요:"
echo ""
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "6. 그 다음 Render.com으로 이동:"
echo "   https://render.com"
echo ""
echo "자세한 가이드: START_HERE.md 또는 CLOUD_DEPLOY.md"
echo ""
echo "=================================================="
