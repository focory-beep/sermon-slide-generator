# 📖 예배 슬라이드 생성기 (Sermon Slide Generator)

목회자를 위한 자동 예배 PPT 생성 도구입니다. 성경 본문과 예배 순서를 입력하면 전문적인 프레젠테이션을 자동으로 생성합니다.

## ✨ 주요 기능

- 🌍 **다국어 지원**: 한국어(개역개정, 공동번역 등), 영어(NIV, ESV, KJV), 독일어(Luther 1984/2017)
- 🎨 **커스터마이징**: 폰트, 색상, 크기 자유롭게 조정
- 📝 **자동 분할**: 긴 본문은 자동으로 여러 슬라이드로 분할
- ⚡ **즉시 생성**: 웹 브라우저에서 바로 사용 가능
- 🆓 **완전 무료**: 오픈소스, 광고 없음

## 🚀 빠른 시작

### 1. 필요 사항

- Python 3.8 이상
- 웹 브라우저 (Chrome, Firefox, Safari 등)

### 2. 설치

```bash
# 저장소 다운로드 (또는 파일들을 복사)
cd sermon-slide-generator

# Python 패키지 설치
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
# 백엔드 서버 시작
python backend/main.py

# 또는 스크립트 사용 (Linux/Mac)
chmod +x start_server.sh
./start_server.sh
```

서버가 실행되면 `http://localhost:8000`에서 API가 작동합니다.

### 4. 웹 인터페이스 열기

`frontend/index.html` 파일을 웹 브라우저에서 엽니다.

```bash
# Mac
open frontend/index.html

# Linux
xdg-open frontend/index.html

# Windows
start frontend/index.html
```

## 📖 사용 방법

### 웹 인터페이스 사용

1. **기본 정보 입력**: 예배 제목과 날짜 입력
2. **예배 순서 작성**: 각 순서 항목 추가 (찬송, 기도, 설교 등)
3. **성경 본문 추가**:
   - 성경 참조 (예: 요한복음 3:16)
   - 번역본 선택 (개역개정, NIV, Luther 등)
   - 본문 텍스트 입력 또는 붙여넣기
4. **디자인 커스터마이징**: 폰트, 색상 등 조정
5. **PPT 생성하기** 버튼 클릭
6. 자동으로 PPT 파일이 다운로드됩니다!

### API 직접 사용

```python
import requests

data = {
    "title": "주일 예배",
    "date": "2026년 2월 16일",
    "scriptures": [
        {
            "reference": "요한복음 3:16",
            "translation": "개역개정",
            "text": "하나님이 세상을 이처럼 사랑하사..."
        }
    ],
    "config": {
        "font_size": 32,
        "background_color": "#FFFFFF"
    }
}

response = requests.post("http://localhost:8000/generate-presentation", json=data)
with open("presentation.pptx", "wb") as f:
    f.write(response.content)
```

## 🏗️ 프로젝트 구조

```
sermon-slide-generator/
├── backend/
│   └── main.py              # FastAPI 백엔드 서버
├── frontend/
│   └── index.html           # 웹 인터페이스
├── requirements.txt         # Python 의존성
├── test_api.py             # API 테스트 스크립트
├── start_server.sh         # 서버 실행 스크립트
└── README.md
```

## 🔧 기술 스택

- **백엔드**: FastAPI, python-pptx
- **프론트엔드**: HTML, TailwindCSS, Vanilla JavaScript
- **PPT 생성**: python-pptx 라이브러리

## 📋 API 문서

서버 실행 후 `http://localhost:8000/docs`에서 자동 생성된 API 문서를 확인할 수 있습니다.

### 주요 엔드포인트

- `POST /generate-presentation`: PPT 생성
- `GET /`: API 상태 확인

## 🌐 배포 옵션

### Option 1: 로컬 사용 (현재 상태)
- 개인 컴퓨터에서만 사용
- 가장 간단하고 빠름

### Option 2: 교회 네트워크 공유
```bash
# 로컬 네트워크에서 접근 가능하도록 실행
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
같은 Wi-Fi 네트워크의 다른 기기에서 접근 가능

### Option 3: 클라우드 배포 (공개 서비스)

#### Heroku 배포
1. `Procfile` 생성:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

2. Heroku에 배포:
```bash
heroku create sermon-slide-generator
git push heroku main
```

#### Vercel/Netlify 배포 (프론트엔드)
- Frontend를 Vercel에 배포
- Backend는 별도 서버 (Railway, Render 등)에 배포

#### Docker 배포
1. `Dockerfile` 생성:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. 실행:
```bash
docker build -t sermon-slide-generator .
docker run -p 8000:8000 sermon-slide-generator
```

## 🔮 향후 개선 계획

### Phase 2: 성경 API 통합
- [ ] API.Bible 통합으로 성경 구절 자동 조회
- [ ] 대한성서공회 데이터 연동 (라이선스 획득 시)
- [ ] 성경 검색 기능

### Phase 3: 고급 기능
- [ ] 찬송가 가사 자동 추가
- [ ] 이미지/배경 삽입
- [ ] 다양한 템플릿 제공
- [ ] 사용자 계정 및 저장 기능
- [ ] 주보 PDF 생성

### Phase 4: 모바일 지원
- [ ] 반응형 웹 디자인 개선
- [ ] 모바일 앱 (React Native)

## 🤝 기여하기

이 프로젝트는 오픈소스입니다. 개선 사항이나 버그 리포트는 언제나 환영합니다!

### 기여 방법
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스로 제공됩니다.

**주의사항**:
- 성경 번역본은 각 출판사의 저작권이 적용됩니다
- 개역개정: 대한성서공회 (비상업적 사용 허용)
- NIV, ESV: 상업적 사용 시 라이선스 필요
- Luther 2017: Deutsche Bibelgesellschaft

## 💬 문의 및 지원

- 버그 리포트: GitHub Issues
- 기능 제안: GitHub Discussions
- 이메일: [your-email@example.com]

## 🙏 감사의 말

이 프로젝트는 전 세계 목회자들의 사역을 돕기 위해 만들어졌습니다.
사용하시면서 도움이 되셨다면, 별표⭐를 눌러주세요!

---

**Made with ❤️ for pastors and worship leaders worldwide**

🇰🇷 한국어 | 🇬🇧 English | 🇩🇪 Deutsch
