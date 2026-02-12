# 🚀 배포 가이드 (Deployment Guide)

이 문서는 예배 슬라이드 생성기를 다양한 환경에 배포하는 방법을 설명합니다.

## 📑 목차

1. [로컬 사용 (개인 컴퓨터)](#1-로컬-사용)
2. [교회 네트워크 공유](#2-교회-네트워크-공유)
3. [클라우드 배포 (인터넷 공개)](#3-클라우드-배포)
4. [Docker 컨테이너](#4-docker-컨테이너)

---

## 1. 로컬 사용

가장 간단한 방법입니다. 개인 컴퓨터에서만 사용합니다.

### Windows

```batch
# 1. Python 설치 확인 (python.org에서 다운로드)
python --version

# 2. 프로젝트 폴더로 이동
cd sermon-slide-generator

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
python backend/main.py
```

### Mac/Linux

```bash
# 1. Python 설치 확인
python3 --version

# 2. 프로젝트 폴더로 이동
cd sermon-slide-generator

# 3. 패키지 설치
pip3 install -r requirements.txt

# 4. 서버 실행 (스크립트 사용)
chmod +x start_server.sh
./start_server.sh
```

### 웹 인터페이스 접속

1. 서버 실행 후 `frontend/index.html` 파일을 브라우저에서 엽니다
2. 또는 브라우저에서 `file:///경로/sermon-slide-generator/frontend/index.html` 직접 입력

---

## 2. 교회 네트워크 공유

같은 Wi-Fi 네트워크의 다른 사람들도 사용할 수 있게 합니다.

### 서버 실행

```bash
# 모든 네트워크 인터페이스에서 접속 가능하도록 실행
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 클라이언트 접속

1. 서버 컴퓨터의 IP 주소 확인:
   ```bash
   # Windows
   ipconfig

   # Mac/Linux
   ifconfig
   # 예: 192.168.1.100
   ```

2. `frontend/index.html` 파일을 수정:
   ```javascript
   // 기존
   const API_URL = 'http://localhost:8000';

   // 변경 (서버 IP로 변경)
   const API_URL = 'http://192.168.1.100:8000';
   ```

3. 수정한 `index.html`을 다른 사람들과 공유
4. 브라우저에서 파일 열기

### 보안 고려사항

- 방화벽 설정: 8000 포트 허용 필요
- 공용 Wi-Fi에서는 사용하지 마세요 (보안 위험)
- 신뢰할 수 있는 네트워크에서만 사용

---

## 3. 클라우드 배포

인터넷을 통해 누구나 접속할 수 있도록 배포합니다.

### Option A: Render.com (무료, 추천)

1. **GitHub 저장소 생성**
   - sermon-slide-generator 폴더를 GitHub에 업로드

2. **render.com 가입 및 설정**
   ```yaml
   # render.yaml 파일 생성
   services:
     - type: web
       name: sermon-slide-generator
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

3. **프론트엔드 수정**
   ```javascript
   // frontend/index.html에서 API_URL 변경
   const API_URL = 'https://sermon-slide-generator.onrender.com';
   ```

4. **Render에 배포**
   - GitHub 저장소 연결
   - 자동 배포 설정
   - URL 받기 (예: https://sermon-slide-generator.onrender.com)

### Option B: Railway.app (간단함)

1. **Railway CLI 설치**
   ```bash
   npm install -g railway
   ```

2. **프로젝트 배포**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **환경 변수 설정**
   - Railway 대시보드에서 PORT 자동 설정됨

### Option C: Heroku (유료)

1. **Procfile 생성**
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. **배포**
   ```bash
   heroku login
   heroku create sermon-slide-generator
   git push heroku main
   ```

### Option D: Vercel (프론트엔드) + Railway (백엔드)

**백엔드 (Railway)**
- 위의 Railway 배포 과정 따라하기
- API URL 기록 (예: https://api.railway.app)

**프론트엔드 (Vercel)**

1. `vercel.json` 생성:
   ```json
   {
     "cleanUrls": true,
     "trailingSlash": false
   }
   ```

2. 배포:
   ```bash
   npm install -g vercel
   cd frontend
   vercel
   ```

3. `index.html`에서 API_URL을 Railway URL로 변경

---

## 4. Docker 컨테이너

컨테이너화하여 어디서든 동일하게 실행합니다.

### Dockerfile 생성

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (프론트엔드 + 백엔드)

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend
```

### 실행

```bash
# 빌드 및 실행
docker-compose up -d

# 중지
docker-compose down
```

### 클라우드 Docker 배포

**AWS ECS, Google Cloud Run, Azure Container Instances**

```bash
# Docker 이미지 빌드
docker build -t sermon-slide-generator .

# 클라우드 레지스트리에 푸시
docker tag sermon-slide-generator:latest your-registry/sermon-slide-generator:latest
docker push your-registry/sermon-slide-generator:latest
```

---

## 5. 성능 최적화

### 프로덕션 설정

```bash
# Gunicorn + Uvicorn workers
pip install gunicorn

# 실행
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Nginx 리버스 프록시

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 6. 보안 체크리스트

배포 전 확인 사항:

- [ ] HTTPS 설정 (Let's Encrypt 무료)
- [ ] CORS 설정 검토
- [ ] API Rate Limiting 설정
- [ ] 환경 변수로 민감 정보 관리
- [ ] 정기 업데이트 및 패치
- [ ] 백업 전략 수립
- [ ] 모니터링 설정 (Sentry, LogRocket 등)

---

## 7. 비용 예상

### 무료 옵션
- Render.com: 무료 티어 (750시간/월)
- Railway: 월 $5 크레딧 제공
- Vercel: 무료 (개인 프로젝트)
- GitHub Pages: 무료 (정적 사이트만)

### 유료 옵션
- AWS/GCP/Azure: 월 $5-20 (사용량에 따라)
- Heroku: 월 $7부터
- 도메인: 연 $10-15

---

## 8. 트러블슈팅

### 문제: CORS 오류
```python
# backend/main.py에서 CORS 설정 확인
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 문제: 한글 폰트 깨짐
- 서버에 한글 폰트 설치 필요
- Ubuntu: `sudo apt-get install fonts-nanum`

### 문제: PPT 다운로드 안됨
- 브라우저 팝업 차단 확인
- HTTPS 사용 여부 확인

---

## 9. 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [python-pptx 문서](https://python-pptx.readthedocs.io/)
- [Render 배포 가이드](https://render.com/docs)
- [Docker 공식 문서](https://docs.docker.com/)

---

## 💬 도움이 필요하신가요?

- GitHub Issues로 질문하기
- 이메일: [your-email@example.com]
- Discord 커뮤니티: [초대 링크]

**목회자와 예배 인도자들을 위해 만들어졌습니다 ❤️**
